# Master Module for italians Calls activity management 
A new odoo based module for calls project management

------
🇮🇹
## Oggetti da modellare:
**CALENDARIO** corsi le cui i singoli record sono composti da:
+ data;
+ orario inizio;
+ orario fine (vedere se da gestire avendo una durata e calcolando poi inizio e fine o se fare due dati separati);
+ luogo svolgimento corso
+ destinatari corso (ovvero gli alunni);
+ docente;
+ progetto in cui è inserita la lezione;
+ modulo formativo in cui rientra la lezione;
+ edizione della lezione (cioè n-ripetizione della stessa lezione all’interno del progetto, di solito con destinatari diversi ma stesso docente);
È necessario prevedere che ci sarà una procedura di import dei calendari che dovrà controllare se una risorsa (docente, alunno, sede ecc) sia già impegnata per ogni data importata.

**ANAGRAFE** in cui ci sono destinatari corsi, partner nei progetti, aziende e docenti (è possibile che qui dovremo solo modificare un po’ il modulo HR di odoo. Ovviamente bisognerà poi mettere delle viste sulla singola anagrafica per far vedere in quali progetti quel singolo record è stato intestatario (docente/destinatario/partner)
+ se azienda
    + denominazione
    + forma giuridica
    + p.iva/c.f.
    + sede legale
    + legale rappresentante
    + dimensione (micro, piccola, media, grande)
    + a che fondo è iscritta
    + cassetto previdenziale
    + sede legale
    + IBAN
    + zona documenti (documenti con scadenza)
    + progetti a cui ha partecipato (query)
    + interlocutore
+ se persona fisica
    + dati personali (cf, data di nascita, p.iva)
    + azienda in cui lavora
    + (se destinatario) stato occupazionale
    + IBAN
    + zona documenti (documenti con data scadenza)
    + progetti a cui ha partecipato (query)
    + (se docente) cosa insegna

i **PROGETTI** formativi (che verranno resi in una dashboard) in cui vengono specificati:
+ azienda proponente (intestatario del progetto);
+ partner progetto (chi partecipa, di solito altre aziende);
+ fondo in cui viene presentato il progetto;
+ data presentazione progetto;
+ data ammissione progetto;
+ scadenza/scadenze (questa è una cosa molto importante. Un progetto una volta ammesso al finanziamento ha un termine massimo per svolgere tutte le attività che vengono finanziate, inoltre ci sono scadenze intermedie per la presentazione al fondo di anticipi di finanziamento ecc. Tutte queste scadenze variano da fondo a fondo. Utilizzando il modulo CRM come base dovremmo riuscire a implementare una cosa del genere);
+ budget di spesa (ce ne sarà più di uno probabilmente di voci di budget, al momento non lo so);
+ ore formazione erogate (che sarà un campo calcolato, alla data corrente, in base al [numero di destinatari]*[ore di corso effettuate]);
+ avanzamento progetto (indicativo di una view per dire che bisognerà mostrare il grado di avanzamento del progetto. Dipendentemente da più fattori, uno su tutti il fondo su cui è stato presentato, bisognerà dare all’utente la percezione del grado di avanzamento del progetto);


## Classi
*i campi con `**` sono possibilmente puntatori a campi di altre classi (One2Many, Many2One, Many2Many)*

+ `class progetti():`
    + codice progetto (string)
    + `**` fondo  (ref fondi)
    + importo finanziamento (float)
    + ore di formazione da budget (float)
    + ore operatori da budget (float)
    + dgr di riferimento (string)
    + sportello di presentazione (string)
    + data di presentazione (data)
    + data notifica finanziamento (datetime)
    + data convenzione (datetime)
    + data richiesta acconto/anticipo (datetime)
    + allegati (file)
    + `**` titolare progetto (ref contatto)
    + `**` partner progetto (ref contatto)
    + `**` destinatari (ref anagrafe)
    + `**` corsi/lezioni (ref ???)
    + data chiusura progetto calcolata da data inizio e scadenza finanziamento in base a fondo e avviso/dgr (datetime)
    + polizza (string)
    + operatori (???)
    + `**` tutor (ref anagrafe)
    + `**` coordinatori (ref contatto)
    + `**` amministratori (ref contatto)
    + `**` queo_che_serve (ref contatto)

+ `class moduli():`
    + titolo (string)
    + edizione (id edizione incrementale)
    + ore singola edizione (num)
    + `**` calendari (ref calendari)
    + UFC (boh)
    + metodologia intervento (boh)

+ `class calendari():`
    + data (datetime)
    + ora inizio (datetime/float)
    + ora fine (datetime/float)
    + sede (string/ ref sedi?)
    + `**` destinatari (ref anagrafe)
    + `**` modulo (ref moduli)
    + `**` docente (ref contatto)

+ `class fondi():`
    + nome (string)
    + area \[regione,nazione,interprofessionale\]

+ `class avviso/dgr():`
    + data scadenza finanziamento (datetime/float)
    + data scadenza richiesta anticipo (datetime/float)
    + data avvio formazione (datetime/float)
    + `**` fondo (ref fondi)

+ `class sedi():`
    + nome (string)
    + posti (int)
    + dotazione (string)
    + via (string)
    + comune (string)
    + `**` referente (ref contatto)

+ `class anagrafe():`
    >*in realtà ci sono già res.partner e res.company che sarebbero da overloaddare con i dati in più che ci servono e con una parte per gli attachments*

+ `class allegati():` *//ci sarebbe ir.attachments*
    + nome (string)
    + validità (data) *//da capire come triggerare un avviso sugli allegati in scadenza*
    + file (binary)
    