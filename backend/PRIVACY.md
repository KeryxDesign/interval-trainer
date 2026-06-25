# Huermony — testo privacy classifica (pronto da LEX, 2026-06-25)

La riga corta è già live nell'app (sotto al form nickname). Questo paragrafo lungo
va messo in una pagina/sezione privacy quando la creerai.

Titolare: Davide Filippini — info@keryxdesign.com. Dati su Supabase, server UE.
Base giuridica: consenso (l'utente sceglie nickname ed entra in classifica).
C'è la funzione in-app `delete_my_account()` per la cancellazione.

## IT

Privacy

Per la classifica raccogliamo solo questo: un identificativo anonimo generato in
automatico al primo accesso, il nickname che scegli (anche di fantasia) e i tuoi
punti XP della settimana. Non raccogliamo email, nome reale, dati di pagamento, ne
usiamo cookie di tracciamento o analytics di terze parti. La base giuridica e il tuo
consenso, espresso scegliendo un nickname ed entrando in classifica. I dati sono
ospitati su Supabase, su server nell'Unione Europea. I punteggi XP si riferiscono alla
settimana in corso e si azzerano al reset settimanale. Puoi cancellare il tuo profilo
e tutti i punteggi in qualsiasi momento dalla funzione "elimina account" dentro l'app.
Titolare del trattamento: Davide Filippini, contatto info@keryxdesign.com.

## EN

Privacy

For the leaderboard we collect only this: an anonymous identifier generated
automatically on first access, the nickname you choose (a made-up one is fine) and your
weekly XP score. We do not collect email, real name or payment data, and we use no
tracking cookies or third-party analytics. The legal basis is your consent, given when
you choose a nickname and join the leaderboard. Data is hosted on Supabase, on servers
in the European Union. XP scores refer to the current week and reset at the weekly
reset. You can delete your profile and all scores at any time using the "delete account"
function inside the app. Data controller: Davide Filippini, contact info@keryxdesign.com.

## Da fare quando crei la pagina privacy
- Aggiungere link/sezione nell'app (es. dal Profilo o footer) che mostri questo testo.
- Opzionale (LEX): riga sui diritti GDPR (accesso, rettifica, reclamo all'autorita).
- La funzione `delete_my_account()` esiste nel backend ma NON ha ancora un bottone UI:
  serve un pulsante "elimina account" che chiami supa.rpc('delete_my_account').
