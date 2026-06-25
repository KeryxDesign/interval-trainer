-- ============================================================================
-- Huermony — Classifica (Fase 1): account anonimo + nickname + XP settimanale
-- Eseguire nel SQL Editor di Supabase (una volta sola).
-- Sicurezza validata da SENTINEL: RLS ovunque, scrittura solo via RPC validata,
-- settimana calcolata server-side, XP monotòno + cappato + rate-limit, niente PII.
-- ============================================================================

-- 1) PROFILI: solo dati pubblici (nickname). Niente email/PII.
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nickname text not null
    check (char_length(nickname) between 2 and 16)
    check (nickname ~ '^[A-Za-z0-9_ ]{2,16}$'),   -- charset sicuro (anti-XSS lato dato)
  created_at timestamptz not null default now()
);
-- nickname unico (niente due "Mozart" in classifica)
do $$ begin
  alter table public.profiles add constraint profiles_nickname_unique unique (nickname);
exception when duplicate_object then null; end $$;

-- 2) PUNTEGGI SETTIMANALI: una riga per utente per settimana ISO
create table if not exists public.weekly_scores (
  user_id uuid not null references public.profiles(id) on delete cascade,
  week text not null,                              -- es. '2026-W26' (ISO week, UTC)
  xp integer not null default 0 check (xp >= 0 and xp <= 20000),  -- cap settimanale realistico
  updated_at timestamptz not null default now(),
  primary key (user_id, week)
);
create index if not exists weekly_scores_week_xp_idx on public.weekly_scores (week, xp desc);

-- 3) RLS
alter table public.profiles enable row level security;
alter table public.weekly_scores enable row level security;

-- profiles: lettura pubblica (per mostrare i nickname), scrittura SOLO della propria
drop policy if exists profiles_read_all on public.profiles;
create policy profiles_read_all on public.profiles for select using (true);
drop policy if exists profiles_insert_own on public.profiles;
create policy profiles_insert_own on public.profiles for insert with check (auth.uid() = id);
drop policy if exists profiles_update_own on public.profiles;
create policy profiles_update_own on public.profiles for update using (auth.uid() = id) with check (auth.uid() = id);

-- weekly_scores: lettura pubblica (classifica). NESSUNA policy insert/update:
-- si scrive SOLO via la RPC validata sotto. Niente delete per nessuno.
drop policy if exists scores_read_all on public.weekly_scores;
create policy scores_read_all on public.weekly_scores for select using (true);

-- 4) SCRITTURA PUNTEGGIO (unica via): security definer, settimana server-side,
--    profilo garantito, XP monotòno, cappato e con rate-limit anti-script.
create or replace function public.submit_weekly_xp(p_xp integer)
returns void language plpgsql security definer set search_path = public as $$
declare
  wk text := to_char(now() at time zone 'UTC','IYYY"-W"IW');
  v_prev integer; v_last timestamptz;
begin
  if auth.uid() is null then raise exception 'not authenticated'; end if;
  if p_xp is null or p_xp < 0 or p_xp > 20000 then raise exception 'xp out of range'; end if;

  -- garantisce il profilo (placeholder; l'utente sceglie il nickname dopo)
  insert into public.profiles(id, nickname)
    values (auth.uid(), 'anon_' || substr(replace(auth.uid()::text,'-',''),1,8))
  on conflict (id) do nothing;

  -- rate-limit sul DELTA: max ~500 xp/min + burst 300 (taratura sul gameplay reale)
  select xp, updated_at into v_prev, v_last
    from public.weekly_scores where user_id = auth.uid() and week = wk;
  if found and (p_xp - v_prev) > (extract(epoch from (now() - v_last)) / 60.0) * 500 + 300 then
    raise exception 'xp delta too fast';
  end if;

  insert into public.weekly_scores(user_id, week, xp, updated_at)
    values (auth.uid(), wk, p_xp, now())
  on conflict (user_id, week) do update
    set xp = greatest(weekly_scores.xp, excluded.xp), updated_at = now();
end; $$;

revoke all on function public.submit_weekly_xp(integer) from public, anon;
grant execute on function public.submit_weekly_xp(integer) to authenticated;

-- 5) CANCELLA IL MIO ACCOUNT (GDPR / diritto all'oblio): l'utente pulisce i propri dati
create or replace function public.delete_my_account()
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'not authenticated'; end if;
  delete from public.profiles where id = auth.uid();  -- cascade pulisce weekly_scores
end; $$;
revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;

-- NOTE
-- * Se in futuro crei una VIEW per la classifica: SEMPRE `with (security_invoker = true)`
--   altrimenti bypassa la RLS. (Per ora il client fa la join: from('weekly_scores')
--   .select('xp, profiles(nickname)').eq('week', wk).gt('xp', 0).order('xp',{ascending:false}).limit(100))
-- * Il client deve renderizzare il nickname con textContent, MAI innerHTML.
-- * anon key nel client = OK (pubblica per design). MAI service_role nel client/repo.
