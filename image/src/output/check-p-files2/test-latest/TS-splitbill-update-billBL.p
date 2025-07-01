
DEF INPUT PARAMETER rec-id-h-bill AS INT.
DEF INPUT PARAMETER rec-id-h-artikel AS INT.
DEF INPUT PARAMETER h-artart AS INTEGER. 
DEF INPUT PARAMETER h-artnrfront AS INTEGER. 
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER amount AS DECIMAL.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER billart AS INT.
DEF INPUT PARAMETER description AS CHAR.
DEF INPUT PARAMETER change-str AS CHAR.
DEF INPUT PARAMETER qty AS INT.
DEF INPUT PARAMETER tischnr AS INT.
DEF INPUT PARAMETER price AS DECIMAL.
DEF INPUT PARAMETER add-zeit AS INT.
DEF INPUT PARAMETER curr-select AS INT.
DEF INPUT PARAMETER hoga-card AS CHAR.
DEF INPUT PARAMETER cancel-str AS CHAR.
DEF INPUT PARAMETER curr-waiter AS INTEGER.
DEF INPUT PARAMETER amount-foreign AS DECIMAL.
DEF INPUT PARAMETER curr-room AS CHAR.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER cc-comment AS CHAR.
DEF INPUT PARAMETER guestnr AS INT.


DEF OUTPUT PARAMETER bill-date AS DATE.

DEFINE buffer kellner1 FOR vhp.kellner. 
DEFINE buffer bill-guest FOR vhp.guest. 

DEFINE VARIABLE deptname AS CHAR FORMAT "x(24)".
DEFINE VARIABLE foreign-rate AS LOGICAL. 
DEFINE VARIABLE exchg-rate AS DECIMAL INITIAL 1. 

FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = dept NO-LOCK. 
deptname = vhp.hoteldpt.depart.
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 143 NO-LOCK. 
foreign-rate = vhp.htparam.flogical. 
IF FOREIGN-RATE THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz 
    = vhp.htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.waehrung THEN exchg-rate 
    = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
END. 

/* FDL Comment Ticket Serverless #521
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill.*/
FIND FIRST h-artikel WHERE RECID(h-artikel) = rec-id-h-artikel NO-ERROR.

RUN update-bill.

PROCEDURE update-bill: 
  DEFINE VARIABLE closed AS LOGICAL. 

  FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill NO-LOCK NO-ERROR. /*FDL Ticket Serverless #521 - add if available*/
  IF AVAILABLE h-bill THEN
  DO: 
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK NO-ERROR. 
    vhp.h-bill.kellner-nr = curr-waiter. /*FT 101215*/
    FIND FIRST vhp.kellner1 WHERE vhp.kellner1.kellner-nr 
      = vhp.h-bill.kellner-nr 
      AND vhp.kellner1.departement = vhp.h-bill.departement NO-LOCK. 
 
    vhp.h-bill.saldo = vhp.h-bill.saldo + amount. 
    IF vhp.h-bill.saldo NE 0 THEN vhp.h-bill.rgdruck = 0. 
 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
    bill-date = vhp.htparam.fdate. 
    IF transdate NE ? THEN 
    DO:
      bill-date = transdate.
    END.
    ELSE
    DO:
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
      IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
    END.

    CREATE vhp.h-bill-line. 
    ASSIGN
      vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
      vhp.h-bill-line.artnr = billart
      vhp.h-bill-line.bezeich = description + change-str + cc-comment
      vhp.h-bill-line.anzahl = qty
      vhp.h-bill-line.nettobetrag = amount 
      vhp.h-bill-line.betrag = amount
      vhp.h-bill-line.tischnr = tischnr 
      vhp.h-bill-line.departement = vhp.h-bill.departement
      vhp.h-bill-line.epreis = price
      vhp.h-bill-line.zeit = TIME + add-zeit 
      vhp.h-bill-line.bill-datum = bill-date 
      vhp.h-bill-line.waehrungsnr = curr-select
      vhp.h-bill-line.fremdwbetrag = amount-foreign
    . 
    IF SUBSTR(description,1,5) = "RmNo " OR SUBSTR(description,1,5) = "Card " 
      THEN vhp.h-bill-line.segmentcode = INTEGER(SUBSTR(hoga-card,1,9)). 
    FIND CURRENT vhp.h-bill-line NO-LOCK. 
 
    IF billart NE 0 THEN 
    DO: 
      FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = billart 
        AND vhp.h-umsatz.departement = vhp.h-bill.departement 
        AND vhp.h-umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE vhp.h-umsatz THEN 
      DO: 
        CREATE vhp.h-umsatz. 
        vhp.h-umsatz.artnr = billart. 
        vhp.h-umsatz.datum = bill-date. 
       vhp.h-umsatz.departement = vhp.h-bill.departement. 
      END. 
      vhp.h-umsatz.betrag = vhp.h-umsatz.betrag + amount. 
      vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + qty. 
      FIND CURRENT vhp.h-umsatz NO-LOCK. 
    END. 
 
    CREATE vhp.h-journal. 
    ASSIGN
      vhp.h-journal.rechnr = vhp.h-bill.rechnr
      vhp.h-journal.artnr = billart
      vhp.h-journal.anzahl = qty
      vhp.h-journal.betrag = amount 
      vhp.h-journal.bezeich = description + change-str + cc-comment
      vhp.h-journal.tischnr = tischnr
      vhp.h-journal.departement = vhp.h-bill.departement 
      vhp.h-journal.epreis = price
      vhp.h-journal.zeit = TIME + add-zeit 
      vhp.h-journal.stornogrund = cancel-str 
      vhp.h-journal.kellner-nr = curr-waiter 
      vhp.h-journal.bill-datum = bill-date
      vhp.h-journal.artnrfront = h-artnrfront 
      vhp.h-journal.aendertext = ""
      vhp.h-journal.artart = h-artart
      vhp.h-journal.waehrungcode = curr-select
    . 
    IF AVAILABLE vhp.h-artikel THEN vhp.h-journal.artart = vhp.h-artikel.artart. 
 
    FIND CURRENT vhp.h-journal NO-LOCK. 
 
    IF h-artart = 6 THEN 
    DO: 
      FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.h-artikel.artnrfront 
        AND vhp.umsatz.departement = 0 
        AND vhp.umsatz.datum = bill-date NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.umsatz THEN 
      DO:
        FIND CURRENT vhp.umsatz EXCLUSIVE-LOCK.
      END.
      ELSE DO: 
        CREATE vhp.umsatz. 
        vhp.umsatz.artnr = vhp.h-artikel.artnrfront. 
        vhp.umsatz.datum = bill-date. 
        vhp.umsatz.departement = 0. 
      END. 
      vhp.umsatz.betrag = vhp.umsatz.betrag + amount. 
      vhp.umsatz.anzahl = vhp.umsatz.anzahl + 1. 
      FIND CURRENT vhp.umsatz NO-LOCK. 
    END. 
  
    closed = NO. 
    IF h-artart = 2 OR h-artart = 7 THEN 
    DO: 
      FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront 
        AND vhp.artikel.departement = 0 NO-LOCK. 
      amount-foreign = 0. 
      IF foreign-rate AND amount-foreign = 0 THEN 
        amount-foreign = amount / exchg-rate.
      FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK. 
      FIND FIRST bill-guest WHERE bill-guest.gastnr = vhp.htparam.finteger NO-LOCK. 
      RUN inv-ar(vhp.artikel.artnr, vhp.h-bill.departement, curr-room, 
        bill-guest.gastnr, bill-guest.gastnr, vhp.h-bill.rechnr, amount, 
        amount-foreign, bill-date, bill-guest.name, 
        user-init, cc-comment). 
    END. 
    FIND CURRENT vhp.h-bill NO-LOCK NO-ERROR. 

    IF curr-select GT 0 THEN 
    DO: 
      FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
        AND vhp.h-bill-line.waehrungsnr = curr-select 
        AND vhp.h-bill-line.departement = dept EXCLUSIVE-LOCK: 
        vhp.h-bill-line.paid-flag = 1. 
      END. 
      RELEASE vhp.h-bill-line.
    END. 
    ELSE DO: 
      FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
        AND vhp.h-bill-line.departement = dept EXCLUSIVE-LOCK: 
        vhp.h-bill-line.paid-flag = 1. 
      END. 
      RELEASE vhp.h-bill-line.
    END.     
  END. 
  /*MTRUN cal-balance. */
  /* FDL Comment Ticket Serverless #521 - Move Above takeout from procedure
  RUN put-paidflag. 
  */
  /*MTASSIGN
    cancel-str = ""
    cc-comment = "" 
    change-str = ""
  . */
END. 


procedure inv-ar:
  DEFINE INPUT PARAMETER curr-art       AS INTEGER.
  DEFINE INPUT PARAMETER curr-dept      AS INTEGER.
  DEFINE INPUT PARAMETER zinr           LIKE zimmer.zinr.
  DEFINE INPUT PARAMETER gastnr         AS INTEGER.
  DEFINE INPUT PARAMETER gastnrmember   AS INTEGER.
  DEFINE INPUT PARAMETER rechnr         AS INTEGER.
  DEFINE INPUT PARAMETER saldo          AS DECIMAL.
  DEFINE INPUT PARAMETER saldo-foreign  AS DECIMAL.
  DEFINE INPUT PARAMETER bill-DATE      AS DATE.
  DEFINE INPUT PARAMETER billname       AS CHAR.
  DEFINE INPUT PARAMETER userinit       AS CHAR FORMAT "x(2)".
  DEFINE INPUT PARAMETER voucher-nr     AS CHAR.

  DEFINE VARIABLE exchg-rate            AS DECIMAL INITIAL 1.
  DEFINE VARIABLE foreign-rate          AS LOGICAL.  
  DEFINE VARIABLE double-currency       AS LOGICAL.  
  DEFINE VARIABLE ar-license            AS LOGICAL.
  DEFINE BUFFER debt                    FOR vhp.debitor.  

  FIND FIRST vhp.htparam WHERE paramnr = 143 NO-LOCK.
  foreign-rate = vhp.htparam.fLOGICAL.

  FIND FIRST vhp.htparam WHERE paramnr = 240 NO-LOCK.
  double-currency = vhp.htparam.fLOGICAL.
  
  IF FOREIGN-RATE THEN
  DO:
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK.
    FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz = htparam.fchar 
      NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.waehrung THEN exchg-rate = 
      vhp.waehrung.ankauf / vhp.waehrung.einheit.
  END.
  IF exchg-rate NE 1 THEN saldo-foreign = ROUND(saldo / exchg-rate, 2).
  
  FIND FIRST vhp.bediener WHERE vhp.bediener.userinit = userinit NO-LOCK.
  
  FIND FIRST vhp.htparam WHERE paramnr = 997 NO-LOCK.
  ar-license = vhp.htparam.flogical.

  FIND FIRST vhp.artikel WHERE vhp.artikel.departement = 0 AND 
    vhp.artikel.artnr = curr-art NO-LOCK. 

  FIND FIRST vhp.guest WHERE vhp.guest.gastnr = gastnr NO-LOCK.
  billname = vhp.guest.name + ", " + vhp.guest.vorname1 + " " 
    + vhp.guest.anrede1 + vhp.guest.anredefirma.
      
  FIND FIRST debt WHERE debt.artnr = curr-art
    AND debt.rechnr = rechnr AND debt.opart = 0 
    AND debt.betriebsnr = curr-dept
    AND debt.rgdatum = bill-DATE AND debt.counter = 0 
    AND debt.saldo = saldo NO-LOCK NO-ERROR.

  IF AVAILABLE debt THEN
  DO:
    FIND CURRENT debt EXCLUSIVE-LOCK.
    DELETE debt.
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.departement = 0 
      AND vhp.umsatz.artnr = curr-art 
      AND vhp.umsatz.datum = bill-DATE EXCLUSIVE-LOCK.
    vhp.umsatz.anzahl = vhp.umsatz.anzahl - 1.
    vhp.umsatz.betrag = vhp.umsatz.betrag + saldo.
    FIND CURRENT vhp.umsatz NO-LOCK.
    RELEASE vhp.umsatz.
    CREATE vhp.billjournal.
    vhp.billjournal.rechnr = rechnr.
    vhp.billjournal.bill-datum = bill-DATE.
    vhp.billjournal.artnr = curr-art.
    vhp.billjournal.betriebsnr = curr-dept.
    vhp.billjournal.anzahl = 1.
    vhp.billjournal.betrag = saldo.
    IF double-currency THEN
      vhp.billjournal.fremdwaehrng = saldo-foreign.
    vhp.billjournal.bezeich = vhp.artikel.bezeich. 
    vhp.billjournal.zinr = zinr.
    vhp.billjournal.zeit = TIME.
    vhp.billjournal.bediener-nr = vhp.bediener.nr.
    vhp.billjournal.userinit = userinit.
    RELEASE vhp.billjournal.
    RETURN.
  END.

  IF ar-license THEN
  DO:
    IF voucher-nr NE "" THEN voucher-nr = "/" + voucher-nr.
    CREATE vhp.debitor.
    ASSIGN
      vhp.debitor.artnr           = curr-art
      vhp.debitor.betrieb-gastmem = vhp.artikel.betriebsnr
      vhp.debitor.betriebsnr      = curr-dept
      vhp.debitor.zinr            = zinr
      vhp.debitor.gastnr          = gastnr
      vhp.debitor.gastnrmember    = gastnrmember
      vhp.debitor.rechnr          = rechnr
      vhp.debitor.saldo           = - saldo
      vhp.debitor.transzeit       = TIME
      vhp.debitor.rgdatum         = bill-DATE
      vhp.debitor.bediener-nr     = vhp.bediener.nr
      vhp.debitor.name            = billname
      vhp.debitor.vesrcod         = deptname + voucher-nr
    .

    IF double-currency OR foreign-rate THEN
      vhp.debitor.vesrdep    = - saldo-foreign.

    RELEASE vhp.debitor.
  END.

  FIND FIRST vhp.umsatz WHERE vhp.umsatz.departement = 0 
    AND vhp.umsatz.artnr = curr-art 
    AND vhp.umsatz.datum = bill-DATE EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE vhp.umsatz THEN 
  DO:
    CREATE vhp.umsatz.
    vhp.umsatz.artnr = curr-art.
    vhp.umsatz.datum = bill-DATE.
  END.
  vhp.umsatz.anzahl = vhp.umsatz.anzahl + 1.
  vhp.umsatz.betrag = vhp.umsatz.betrag + saldo.
  FIND CURRENT vhp.umsatz NO-LOCK.
  RELEASE vhp.umsatz.

  CREATE vhp.billjournal.
  vhp.billjournal.rechnr = rechnr.
  vhp.billjournal.bill-datum = bill-DATE.
  vhp.billjournal.artnr = curr-art.
  vhp.billjournal.betriebsnr = curr-dept.
  vhp.billjournal.anzahl = 1.
  vhp.billjournal.betrag = saldo.
  IF double-currency THEN
    vhp.billjournal.fremdwaehrng = saldo-foreign.
  vhp.billjournal.bezeich = vhp.artikel.bezeich. 
  vhp.billjournal.zinr = zinr.
  vhp.billjournal.zeit = TIME.
  vhp.billjournal.bediener-nr = vhp.bediener.nr.
  vhp.billjournal.userinit = userinit.
  RELEASE vhp.billjournal.
END. 

/* FDL Comment Ticket Serverless #521 - Move Above takeout from procedure
PROCEDURE put-paidflag: 
  IF curr-select GT 0 THEN 
  DO: 
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
      AND vhp.h-bill-line.waehrungsnr = curr-select 
      AND vhp.h-bill-line.departement = dept EXCLUSIVE-LOCK: 
      vhp.h-bill-line.paid-flag = 1. 
    END. 
    RELEASE vhp.h-bill-line.
  END. 
  ELSE DO: 
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
      AND vhp.h-bill-line.departement = dept EXCLUSIVE-LOCK: 
      vhp.h-bill-line.paid-flag = 1. 
    END. 
    RELEASE vhp.h-bill-line.
  END. 
END. 
*/
