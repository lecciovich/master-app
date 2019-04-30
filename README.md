# Master Module for Calls activity management 
A new odoo based module for calls project management

------
## Object to model:
**CALENDAR** courses where individual records are composed by:
+ date;
+ starting time;
+ end time (how to do these? two datetime fields or one datetime and one float for the duration and the end time is calculated?);
+ classroom (place where the lession happen);
+ recipients (typically the alumni, one2many);
+ teacher;
+ course of which the lession is part;
+ project of which the course is part;
+ lession edition (This represent the n-repetition of the same course in the project, typically with the same teachers but different recipients);
Is mandatory to model this with the thought of using import functions: the user shall do imports to update present data and, more importantly, creating or importing records there have to be some verification if resources for that day/time are still available or occupied.


**CONTACTS** are another important part, they are: courses recipients, courses teacher, project partners, project heads. It can inherit much from the HR Odoo standard module. Viewing the Contact details the user shall see in which project the contact has been involved. A person contact can be a course recipient AND a course teacher (not within the same project), a company contact can be a project head AND a project partner (not within the same project). In detail:
+ if company
    + company name
    + legal form
    + VAT number
    + legal office
    + CEO
    + company dimension (a list(select) of sizes)
    + fund subscription (a list(select) of funds the company have subscribed)
    + social security drawer (given data, amount of money used in the last 3 years)
    + IBAN
    + attachments (files with description, type and validity date)
    + projects involved in (query/view)
    + referent (name + number OR another contact)
+ if person
    + personal data (social security number, date of birth, VAT)
    + job status
    + company who works for
    + IBAN
    + attachments (files with description, type and validity date)
    + projects involved in (query/view)
    + (if teacher) topics of the teaching

**PROJECTS** are the container of the lessions/courses and they defines with what rules the courses are made. The default view can be like the kanban of CRM module. In details:
+ project company head;
+ project company partners;
+ entitled project fund;
+ project submission date;
+ project ammission date;
+ deadlines (this is an important part. A project, based on which funds is submitted, have deadlines in which all the courses and other activities have to be completed. Instead of making things complicated, we can let the user put those deadline creating a new project);
+ budget (it won't be surely only a single money input);
+ provided lession hours (calculated based on the current date, number of recipients multiplied for the hours of completed lessions);
+ project progress/stage (in the kanban view the user have to see the completion stage of the project);


## Classes
*records with `**` should point to other object (One2Many, Many2One, Many2Many)*

+ `class projects():`
    + project code (string, input given)
    + `**` fund (user chioce)
    + financing amount (float)
    + budgeted lessions hours (float, input given)
    + budgeted other activities (float, input given)
    + calls (string, user choice)
    + submission_date (datetime)
    + admittance_date (datetime)
    + agreement_date (datetime)
    + account_request_date (datetime)
    + `**` attachments (ref attachment model)
    + `**` project_head (ref contact)
    + `**` project_partners (ref contact)
    + `**` recipients (ref anagrafe)
    + `**` courses (ref ???)
    + end_date (datetime)(calculated depending from admittance_date and with the fund and call rules )
    + insurance_policy (string)
    + `**` tutor (ref anagrafe)
    + `**` coordinators (ref contact)
    + `**` administrators (ref contact)

+ `class module():`
    + title (string)
    + repetitions (???)
    + single edition hours (num)
    + `**` lessions (ref calendar)
    + UFC (string list, uncertain)
    + teaching method (string user choice)

+ `class calendars():`
    + lession_date (datetime)
    + start_time (datetime/float)
    + end_time (datetime/float)
    + classroom (string/ ref places?)
    + `**` recipients (ref anagrafe)
    + `**` module (ref module)
    + `**` teacher (ref contact)

+ `class funds():`
    + nome (string)
    + area \[region,state,....\]

+ `class call():` *//not sure about this*
    + deadline_funding (datetime/float)
    + deadline_accounting (datetime/float)
    + lessions_start (datetime/float)
    + `**` fund (ref fondi)

+ `class places():` 
    + name (string)
    + seats (int)
    + inventory (string)
    + address (string)
    + city (string)
    + `**` referent (ref contact)

+ `class contacts():`
    >*res.partner and res.company can be overloaded for this with some more fields and file attachments*

+ `class attachments():` *//ir.attachments?*
    + type (string)
    + description (string)
    + validity (data) *//based on this there has to be a warinng if one attachment is going to and validity*
    + file (file or blog)

<!------
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
    
-->
