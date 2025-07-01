
DEFINE TEMP-TABLE a-list
  FIELD artnr  AS INTEGER
  FIELD anzahl AS INTEGER INITIAL 0
  FIELD preis  AS DECIMAL INITIAL 0.

DEF INPUT  PARAMETER veran-nr           AS INT.
DEF INPUT  PARAMETER veran-seite        AS INT.
DEF INPUT  PARAMETER sub-group          AS INT.
DEF INPUT  PARAMETER ba-dept            AS INT.
DEF INPUT  PARAMETER exchg-rate         AS DECIMAL.
DEF INPUT  PARAMETER curr-date          AS DATE.
DEF INPUT  PARAMETER bill-date          AS DATE.
DEF INPUT  PARAMETER double-currency    AS LOGICAL.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF OUTPUT PARAMETER done               AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER price              AS DECIMAL. 
DEF OUTPUT PARAMETER amount             LIKE bill.saldo. 
DEF OUTPUT PARAMETER amount-foreign     LIKE bill.saldo. 

DEF VAR void-flag           AS LOGICAL.
DEF VAR answer              AS LOGICAL INITIAL YES. 
DEF BUFFER rbuff            FOR bk-rart.

FIND FIRST a-list NO-ERROR.
void-flag = AVAILABLE a-list.

FIND FIRST bk-rart WHERE bk-rart.veran-nr = veran-nr 
    AND bk-rart.veran-seite = veran-seite AND bk-rart.zwkum = sub-group 
    AND bk-rart.preis NE 0 AND bk-rart.fakturiert = 0 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bk-rart AND NOT void-flag THEN RETURN. 


FIND FIRST nightaudit WHERE nightaudit.programm = "nt-bapostbill.p"
    NO-LOCK NO-ERROR.
IF NOT AVAILABLE nightaudit THEN RETURN.


IF AVAILABLE bk-rart THEN
DO:
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE "Charge the unposted articles to the banquet bill NOW?" 
      VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
    IF NOT answer THEN 
    DO: 
      done = NO. 
      RETURN. 
    END. 
END.


FIND FIRST bk-veran WHERE bk-veran.veran-nr = veran-nr NO-LOCK. 
IF bk-veran.rechnr = 0 THEN 
DO: 
    FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnrver NO-LOCK. 
    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
    counters.counter = counters.counter + 1. 
    FIND CURRENT counter NO-LOCK. 
    CREATE bill. 
    ASSIGN 
      bill.gastnr = guest.gastnr 
      bill.billtyp = ba-dept 
      bill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma 
          + " " + guest.vorname1 
     bill.reslinnr = 1 
      bill.rgdruck = 1 
      bill.rechnr = counters.counter 
    . 
    FIND CURRENT bk-veran EXCLUSIVE-LOCK. 
    bk-veran.rechnr = bill.rechnr. 
    FIND CURRENT bk-veran NO-LOCK. 
END. 
ELSE FIND FIRST bill WHERE bill.rechnr = bk-veran.rechnr EXCLUSIVE-LOCK. 

FOR EACH bk-rart WHERE bk-rart.veran-nr = veran-nr 
    AND bk-rart.veran-seite = veran-seite AND bk-rart.zwkum = sub-group 
    AND bk-rart.preis NE 0 AND bk-rart.fakturiert = 0 
    USE-INDEX nr-pg-ug-ix NO-LOCK, 
    FIRST bk-reser WHERE bk-reser.veran-nr = veran-nr 
    AND bk-reser.veran-resnr = bk-rart.veran-resnr 
    AND bk-reser.resstatus LE 3 AND bk-reser.datum = curr-date NO-LOCK 
    BY bk-rart.veran-artnr: 
    price = bk-rart.preis. 
    amount = bk-rart.preis * bk-rart.anzahl. 
    amount-foreign = amount / exchg-rate. 
    RUN create-bill-line(bk-rart.veran-artnr, bk-rart.anzahl, NO). 
    FIND FIRST rbuff WHERE ROWID(rbuff) = ROWID(bk-rart) EXCLUSIVE-LOCK. 
    rbuff.fakturiert = 1. 
    FIND CURRENT rbuff NO-LOCK. 
END.

FOR EACH a-list WHERE a-list.anzahl NE 0:
    price = a-list.preis. 
    amount = a-list.preis * a-list.anzahl. 
    amount-foreign = amount / exchg-rate. 
    RUN create-bill-line(a-list.artnr, a-list.anzahl, NO). 
END.

FIND CURRENT bill NO-LOCK. 

PROCEDURE create-bill-line: 
DEFINE INPUT PARAMETER artikel-no LIKE artikel.artnr. 
DEFINE INPUT PARAMETER qty AS INTEGER. 
DEFINE INPUT PARAMETER deposit-flag AS LOGICAL. 
DEFINE VARIABLE bezeich AS CHAR. 
 
  FIND FIRST artikel WHERE artikel.departement = ba-dept 
    AND artikel.artnr = artikel-no NO-LOCK. 
  bezeich = bk-reser.raum + "> " + artikel.bezeich. 
 
  IF artikel.umsatzart = 1 
    THEN bill.logisumsatz = bill.logisumsatz + amount. 
  ELSE IF artikel.umsatzart = 2 
    THEN bill.argtumsatz = bill.argtumsatz + amount. 
  ELSE IF artikel.umsatzart = 3 
    THEN bill.f-b-umsatz = bill.f-b-umsatz + amount. 
  ELSE IF artikel.umsatzart = 4 
    THEN bill.sonst-umsatz = bill.sonst-umsatz + amount. 
  IF artikel.umsatzart GE 1 AND artikel.umsatzart LE 4 THEN 
 
  bill.gesamtumsatz = bill.gesamtumsatz + amount. 
  bill.rgdruck = 0. 
  bill.datum = bill-date. 
  bill.saldo = bill.saldo + amount. 
  IF double-currency THEN bill.mwst[99] = bill.mwst[99] + amount-foreign. 
 
  CREATE bill-line. 
  ASSIGN 
      bill-line.rechnr = bill.rechnr 
      bill-line.artnr = artikel.artnr 
      bill-line.anzahl = qty 
      bill-line.epreis = price 
      bill-line.betrag = amount 
      bill-line.fremdwbetrag = amount-foreign 
      bill-line.bezeich = bezeich 
      bill-line.departement = artikel.departement 
      bill-line.zeit = TIME 
      bill-line.userinit = user-init 
      bill-line.bill-datum = bill-date 
  . 
  FIND CURRENT bill-line NO-LOCK. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
      AND umsatz.departement = artikel.departement 
      AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    create umsatz. 
    ASSIGN 
      umsatz.artnr = artikel.artnr 
      umsatz.datum = bill-date 
      umsatz.departement = artikel.departement. 
  END. 
  umsatz.betrag = umsatz.betrag + amount. 
  umsatz.anzahl = umsatz.anzahl + qty. 
  FIND CURRENT umsatz NO-LOCK. 
 
  CREATE billjournal. 
  ASSIGN 
      billjournal.rechnr = bill.rechnr 
      billjournal.artnr = artikel.artnr 
      billjournal.anzahl = qty 
      billjournal.fremdwaehrng = amount-foreign 
      billjournal.betrag = amount 
      billjournal.bezeich = bezeich 
      billjournal.departement = artikel.departement 
      billjournal.epreis = price 
      billjournal.zeit = TIME 
      billjournal.userinit = user-init 
      billjournal.bill-datum = bill-date 
  . 
  FIND CURRENT billjournal NO-LOCK. 
END. 

