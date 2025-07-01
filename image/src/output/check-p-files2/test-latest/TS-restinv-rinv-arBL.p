

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
DEFINE INPUT PARAMETER deptname       AS CHAR.

RUN inv-ar.

procedure inv-ar:

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
