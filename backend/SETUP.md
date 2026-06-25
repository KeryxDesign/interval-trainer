# Huermony — Classifica: setup Supabase (Fase 1)

Account leggeri (login anonimo + nickname) + classifica **XP settimanale**. Sito statico su GitHub Pages, niente server da gestire. La sicurezza sta nelle regole RLS (vedi `schema.sql`, validato da SENTINEL).

## Cosa devi fare tu (una volta sola)

1. **Crea il progetto Supabase**
   - Vai su https://supabase.com → New project (free tier va benissimo).
   - Scegli una region vicina (es. EU/Frankfurt) per latenza + GDPR.

2. **Abilita il login anonimo + bot protection**
   - Dashboard → Authentication → Providers/Sign In → abilita **Anonymous sign-ins**.
   - Dashboard → Authentication → **Bot protection (CAPTCHA)**: abilita Turnstile o hCaptcha (argine alla creazione massiva di account anonimi). Tienine da parte la *site key* (pubblica).

3. **Crea lo schema**
   - Dashboard → SQL Editor → incolla tutto `backend/schema.sql` → Run.

4. **Prendi le chiavi pubbliche** (NON sono segreti)
   - Dashboard → Project Settings → API:
     - **Project URL** (es. `https://xxxx.supabase.co`)
     - **anon public key** (chiave pubblica)
   - Mandami questi due valori (URL + anon key): li metto in un file di config del client. ⚠️ Il **service_role** NON va mai dato/usato nel client.

## Cosa faccio io dopo

- Integro `@supabase/supabase-js` (da CDN, caricato solo quando apri la classifica → l'app resta offline-first).
- Login anonimo automatico, schermata per scegliere il nickname.
- Dopo le partite invio l'XP della settimana con `submit_weekly_xp(xp)` (la RPC validata).
- Schermata Classifica (top 100 della settimana) + "tu sei qui".
- Verifico: nessun `service_role` nel bundle (`grep -rE 'service_role' dist/`), nickname renderizzato con `textContent`.

## Privacy (da rifinire con LEX)
Niente email/dati personali: solo un id anonimo + il nickname che scegli. Serve una riga in privacy policy ("usiamo un identificativo anonimo e il nickname scelto per la classifica; nessuna email"). C'è la funzione `delete_my_account()` per il diritto all'oblio.

## Modello di minaccia (onesto)
I punteggi arrivano dal client → un utente esperto può gonfiare il PROPRIO punteggio (entro cap 20k/sett + rate-limit). Per un ranking vanity gratuito è accettabile; difesa = cap realistico + rate-limit + ban manuale dei nickname palesemente fake. Anti-cheat totale richiederebbe ricalcolo server-side del gameplay (over-engineering per ora).
