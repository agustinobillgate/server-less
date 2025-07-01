
DEF TEMP-TABLE t-bk-reser1
    FIELD veran-nr  LIKE bk-reser.veran-nr
    FIELD resstatus LIKE bk-reser.resstatus
    FIELD datum     LIKE bk-reser.datum
    FIELD bis-datum LIKE bk-reser.bis-datum
    FIELD raum      LIKE bk-reser.raum
    FIELD von-zeit  LIKE bk-reser.von-zeit
    FIELD bis-zeit  LIKE bk-reser.bis-zeit
    FIELD veran-resnr   LIKE bk-reser.veran-resnr.

DEF INPUT-OUTPUT PARAMETER curr-resnr   AS INT.
DEF INPUT  PARAMETER guest-gastnr   AS INT.
DEF INPUT  PARAMETER bkl-ftime      AS INT.
DEF INPUT  PARAMETER bkl-ttime      AS INT.
DEF INPUT  PARAMETER bkl-raum       AS CHAR.
DEF INPUT  PARAMETER bkl-datum      AS DATE.
DEF INPUT  PARAMETER bkl-tdatum     AS DATE.
DEF INPUT  PARAMETER bediener-nr    AS INT.
DEF INPUT  PARAMETER ba-dept        AS INT.
DEF INPUT  PARAMETER curr-resstatus AS INTEGER. 
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER guest-name     AS CHAR.
DEF OUTPUT PARAMETER reslinnr       AS INT.
DEF OUTPUT PARAMETER main-exist     AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-bk-reser1.

DEFINE VARIABLE name-contact LIKE guest.namekontakt INITIAL "". 
DEFINE VARIABLE telefon-contact LIKE akt-kont.telefon INITIAL "".
DEFINE VARIABLE email-contact   LIKE akt-kont.email-adr INITIAL "".

DEFINE VARIABLE ftime AS INTEGER. 
DEFINE VARIABLE ttime AS INTEGER. 
DEFINE VARIABLE v-zeit AS CHAR.
DEFINE VARIABLE b-zeit AS CHAR.

DEFINE VARIABLE week-list AS CHAR EXTENT 7 FORMAT "x(19)" 
  INITIAL ["Sunday   ", "Monday   ", "Tuesday  ", "Wednesday", "Thursday  ", 
           "Friday    ", "Saturday  "]. 

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN ci-date = htparam.fdate. 

ftime = round((bkl-ftime / 2), 0) - 1. 
ttime = round((bkl-ttime / 2), 0) - 1.
FIND FIRST guest WHERE guest.gastnr = guest-gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN guest-name = guest.name.

IF curr-resnr = 0 THEN 
DO: 
    FIND FIRST counters WHERE counters.counter-no = 16 NO-LOCK NO-ERROR. 
    IF AVAILABLE counters THEN FIND CURRENT counters EXCLUSIVE-LOCK. 
    ELSE 
    DO: 
      CREATE counters. 
      counters.counter-no = 16. 
      counters.counter-bez = "Banquet Reservation No.". 
    END. 
    counters.counter = counters.counter + 1. 
    curr-resnr = counters.counter. 
    FIND CURRENT counter NO-LOCK. 
    
END. 
RUN get-reslinnr(curr-resnr, OUTPUT reslinnr). 

CREATE bk-reser. 
IF round((bkl-ftime / 2) - 0.1, 0) * 2 LT bkl-ftime THEN 
  ASSIGN
    bk-reser.von-zeit = STRING(ftime,"99") + "00"
    v-zeit = STRING(ftime,"99") + "00". 
ELSE
  ASSIGN
    bk-reser.von-zeit = STRING(ftime,"99") + "30"
    v-zeit = STRING(ftime,"99") + "30". 
IF round((bkl-ttime / 2) - 0.1, 0) * 2 LT bkl-ttime THEN 
  ASSIGN
    bk-reser.bis-zeit = STRING(ttime,"99") + "30"
    b-zeit = STRING(ttime,"99") + "30". 
ELSE
  ASSIGN
    bk-reser.bis-zeit = STRING(ttime + 1,"99") + "00"
    b-zeit = STRING(ttime + 1,"99") + "00". 
ASSIGN
    bk-reser.von-i = bkl-ftime
    bk-reser.bis-i = bkl-ttime 
    bk-reser.raum = bkl-raum
    bk-reser.departement = ba-dept 
    bk-reser.resstatus = curr-resstatus 
    bk-reser.datum = bkl-datum
    bk-reser.bis-datum = bkl-tdatum 
    bk-reser.bediener-nr = bediener-nr
    bk-reser.veran-nr = curr-resnr
    bk-reser.veran-resnr = reslinnr 
    bk-reser.veran-seite = reslinnr
    bk-reser.limitdate = ci-date + 10.
  . 
 .
FIND CURRENT bk-reser NO-LOCK. 

FIND FIRST bk-raum WHERE bk-raum.raum = bkl-raum USE-INDEX raum-ix NO-LOCK NO-ERROR. 
FIND FIRST akt-kont WHERE akt-kont.gastnr = guest-gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE akt-kont THEN 
DO: 
    name-contact = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 
    telefon-contact = akt-kont.telefon.
    email-contact = akt-kont.email-adr.
END.
ELSE IF AVAILABLE guest THEN
DO:
    name-contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma. 
    telefon-contact = guest.telefon.
    email-contact = guest.email-adr.
END.      

CREATE bk-func. 
ASSIGN 
  bk-func.veran-nr = curr-resnr /*bk-reser.veran-nr FT serverless*/
  bk-func.veran-seite = reslinnr
  bk-func.resstatus = curr-resstatus /*bk-reser.resstatus */
  bk-func.datum = bkl-datum /*bk-reser.datum*/
  bk-func.bis-datum = bkl-tdatum /*bk-reser.bis-datum */
  /*bk-func.uhrzeit = STRING(bk-reser.von-zeit,"99:99" ) + " - " + STRING(bk-reser.bis-zeit,"99:99") FT serverless*/
  bk-func.uhrzeit = STRING(v-zeit,"99:99" ) + " - " + STRING(b-zeit,"99:99")
  /*bk-func.wochentag = week-list[WEEKDAY(bk-reser.datum)]*/
  bk-func.wochentag = week-list[WEEKDAY(bkl-datum)]
  bk-func.auf_datum = ci-date
  bk-func.resnr[1] = curr-resnr /*bk-reser.veran-resnr */
  bk-func.r-resstatus[1] = curr-resstatus /*bk-reser.resstatus*/
  /*bk-func.uhrzeiten[1] = STRING(bk-reser.von-zeit,"99:99") + " - " + STRING(bk-reser.bis-zeit,"99:99")*/
  bk-func.uhrzeiten[1] = STRING(v-zeit,"99:99" ) + " - " + STRING(b-zeit,"99:99")
  bk-func.vgeschrieben  = user-init 
  bk-func.vkontrolliert = user-init
  bk-func.betriebsnr = guest-gastnr
  bk-func.veranstalteranschrift[5] = email-contact
  bk-func.v-kontaktperson[1] = name-contact
  bk-func.v-telefon = telefon-contact  /*guest.telefon*/
  bk-func.v-telefax = telefon-contact
  bk-func.kontaktperson[1] = name-contact
  bk-func.telefon = telefon-contact
  bk-func.telefax = telefon-contact.

IF AVAILABLE bk-raum THEN
  ASSIGN
    bk-func.personen = bk-raum.personen
    bk-func.raeume[1] = bk-raum.raum
    bk-func.rpersonen[1] = bk-raum.personen
    bk-func.rpreis[1] = bk-raum.preis.

IF AVAILABLE guest THEN
  ASSIGN
    bk-func.bestellt_durch = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
    bk-func.veranstalteranschrift[1] = guest.adresse1
    bk-func.veranstalteranschrift[2] = guest.adresse2 
    bk-func.veranstalteranschrift[3] = guest.adresse3 
    bk-func.veranstalteranschrift[4] = guest.land + " - " + guest.plz + " - " + guest.wohnort
    bk-func.adurch = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
    bk-func.rechnungsanschrift[1] = guest.adresse1
    bk-func.rechnungsanschrift[2] = guest.adresse2 
    bk-func.rechnungsanschrift[3] = guest.adresse3 
    bk-func.rechnungsanschrift[4] = guest.land + " - " + guest.plz + " - " + guest.wohnort
    bk-func.nadkarte[1] = guest.NAME.
    

/*IF bk-reser.resstatus = 1 THEN bk-func.c-resstatus[1] = "F". 
ELSE IF bk-reser.resstatus = 2 THEN bk-func.c-resstatus[1] = "T". 
ELSE IF bk-reser.resstatus = 3 THEN bk-func.c-resstatus[1] = "W". */

IF curr-resstatus = 1 THEN bk-func.c-resstatus[1] = "F". 
ELSE IF curr-resstatus = 2 THEN bk-func.c-resstatus[1] = "T". 
ELSE IF curr-resstatus = 3 THEN bk-func.c-resstatus[1] = "W". 
 
/* %%% */ 
FIND FIRST bk-veran WHERE bk-veran.veran-nr = bk-reser.veran-nr 
    EXCLUSIVE-LOCK NO-ERROR. 
IF NOT AVAILABLE bk-veran THEN 
DO: 
    /*FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
    ci-date = htparam.fdate. */
    CREATE bk-veran. 
    ASSIGN
      bk-veran.gastnr = guest-gastnr
      bk-veran.gastnrver = guest-gastnr 
      bk-veran.veran-nr = curr-resnr /*bk-reser.veran-nr */
      bk-veran.resnr = reslinnr /*bk-reser.veran-resnr */
      bk-veran.bediener-nr = bediener-nr
      bk-veran.resstatus = curr-resstatus /*bk-reser.resstatus */
      bk-veran.departement = ba-dept
      bk-veran.kontaktfirst = ci-date
      bk-veran.resdat = bkl-tdatum /*bk-reser.bis-datum */
      bk-veran.limit-date = bkl-datum /*bk-reser.datum*/.
    IF AVAILABLE guest THEN
     bk-veran.payment-userinit[9] = guest.phonetik3 + CHR(2) + guest.phonetik2. 
    FIND CURRENT bk-veran NO-LOCK. 
    main-exist = YES. 
END. 
ELSE 
DO: 
  IF bk-veran.resdat LT bk-reser.bis-datum THEN 
    bk-veran.resdat = bkl-tdatum. /*bk-reser.bis-datum*/ 
  main-exist = YES. 
  FIND CURRENT bk-veran NO-LOCK. 
END. 
/** %%% */ 

CREATE t-bk-reser1.
ASSIGN
    t-bk-reser1.veran-nr    = curr-resnr /*bk-reser.veran-nr*/
    t-bk-reser1.resstatus   = curr-resstatus /*bk-reser.resstatus*/
    t-bk-reser1.datum       = bkl-datum /*bk-reser.datum*/
    t-bk-reser1.bis-datum   = bkl-tdatum /*bk-reser.bis-datum*/
    t-bk-reser1.raum        = bkl-raum /*bk-reser.raum*/
    t-bk-reser1.von-zeit    = v-zeit /*bk-reser.von-zeit*/
    t-bk-reser1.bis-zeit    = b-zeit /*bk-reser.bis-zeit*/
    t-bk-reser1.veran-resnr = reslinnr /*bk-reser.veran-resnr*/ .

PROCEDURE get-reslinnr: 
  DEFINE INPUT PARAMETER resnr AS INTEGER. 
  DEFINE OUTPUT PARAMETER reslinnr AS INTEGER INITIAL 1. 
  DEFINE buffer bk-res1 FOR bk-reser. 
  FOR EACH bk-res1 WHERE bk-res1.veran-nr = resnr NO-LOCK 
    BY bk-res1.veran-resnr descending: 
    reslinnr = bk-res1.veran-resnr + 1. 
    RETURN. 
  END. 
END. 

