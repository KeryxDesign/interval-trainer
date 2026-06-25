-- Huermony — alza il limite nickname a 28 e rinomina i 5 bot demo
-- Eseguire una volta nel SQL Editor di Supabase.

-- 1) rimuovi i vecchi vincoli di check sul nickname (erano senza nome, max 16)
do $$
declare c record;
begin
  for c in select conname from pg_constraint
           where conrelid = 'public.profiles'::regclass and contype = 'c' loop
    execute 'alter table public.profiles drop constraint ' || quote_ident(c.conname);
  end loop;
end $$;

-- 2) nuovo vincolo: 2-28 caratteri, stesso charset sicuro
alter table public.profiles
  add constraint profiles_nickname_chk
  check (char_length(nickname) between 2 and 28
         and nickname ~ '^[A-Za-z0-9_ ]{2,28}$');

-- 3) rinomina i bot (in ordine di classifica)
update public.profiles set nickname = 'Peccallo'                  where nickname = 'AlexTune';
update public.profiles set nickname = 'Alluminum Maiden'          where nickname = 'MajorSeventh';
update public.profiles set nickname = 'Woodallica'                where nickname = 'EarHero';
update public.profiles set nickname = 'Giorgio Gerardo Giostraio' where nickname = 'PitchCat';
update public.profiles set nickname = 'Pdor figlio di Kmer'       where nickname = 'NoteNinja';
