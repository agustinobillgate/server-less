
DEF TEMP-TABLE t-bill LIKE bill.

DEF INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER b-rechnr        AS INT.
DEF INPUT  PARAMETER b-artnr         AS INT.
DEF INPUT  PARAMETER bil-flag        AS INT.
DEF INPUT  PARAMETER amount          AS DECIMAL.
DEF INPUT  PARAMETER amount-foreign  AS DECIMAL.
DEF INPUT  PARAMETER price-decimal   AS INT.
DEF INPUT  PARAMETER double-currency AS LOGICAL.
DEF INPUT  PARAMETER foreign-rate    AS LOGICAL.
DEF INPUT  PARAMETER bill-date       AS DATE.
DEF INPUT  PARAMETER transdate       AS DATE.
DEF INPUT  PARAMETER billart         AS INT.
DEF INPUT  PARAMETER description     AS CHAR.
DEF INPUT  PARAMETER qty             AS INT.
DEF INPUT  PARAMETER curr-room       AS CHAR.
DEF INPUT  PARAMETER user-init       AS CHAR.
DEF INPUT  PARAMETER artnr           AS INTEGER.
DEF INPUT  PARAMETER price           AS DECIMAL.
DEF INPUT  PARAMETER cancel-str      AS CHAR.
DEF INPUT  PARAMETER currZeit        AS INTEGER.
DEF INPUT  PARAMETER voucher-nr      AS CHAR.
DEF INPUT  PARAMETER exchg-rate      AS DECIMAL.
DEF INPUT  PARAMETER bil-recid       AS INT.
DEF INPUT  PARAMETER curr-department AS INT.

DEF OUTPUT PARAMETER msg-str         AS CHAR.
DEF OUTPUT PARAMETER balance         AS DECIMAL.
DEF OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEF OUTPUT PARAMETER cancel-flag     AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER void-approve    AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER flag1           AS INT INIT 0.
DEF OUTPUT PARAMETER flag2           AS INT INIT 0.
DEF OUTPUT PARAMETER flag3           AS INT INIT 0.
DEF OUTPUT PARAMETER rechnr          AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-bill.

DEFINE VARIABLE r-recid         AS INT.
DEFINE VARIABLE na-running      AS LOGICAL. 
DEFINE VARIABLE gastnrmember    AS INTEGER. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fo-invoice".

FIND FIRST artikel WHERE artikel.artnr = b-artnr 
    AND artikel.departement = curr-department NO-LOCK.
FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
r-recid = RECID(bill).

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
bill-date = vhp.htparam.fdate.

DO TRANSACTION:
    FIND FIRST bill WHERE RECID(bill) = r-recid EXCLUSIVE-LOCK. 
    IF bill.flag = 1 AND bil-flag = 0 THEN 
    DO: 
      msg-str = translateExtended ("The Bill was closed / guest checked out",lvCAREA,"") 
              + CHR(10)
              + "Bill entry is no longer possible!".
      FIND CURRENT bill NO-LOCK. 
      /*RUN clear-bill-display. */
      RETURN. 
    END. 
    ELSE 
    DO:
      IF artikel.umsatzart = 1 THEN
      ASSIGN
        bill.logisumsatz = bill.logisumsatz + amount
        bill.argtumsatz = bill.argtumsatz + amount
      . 
      ELSE IF artikel.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + amount. 
      ELSE IF (artikel.umsatzart = 3 OR artikel.umsatzart = 5 
        OR artikel.umsatzart = 6) 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + amount. 
      ELSE IF artikel.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + amount. 
      IF artikel.umsatzart GE 1 AND artikel.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + amount. 

      balance = balance + amount. 
      balance-foreign = balance-foreign + amount-foreign. 
      IF NOT artikel.autosaldo THEN bill.rgdruck = 0. 
      ELSE IF artikel.artart = 6 THEN bill.rgdruck = 0. 

      bill.saldo = bill.saldo + amount. 
      IF price-decimal = 0 AND bill.saldo LE 0.4 AND bill.saldo GE -0.4 THEN 
          bill.saldo = 0. 
      IF double-currency OR foreign-rate THEN 
        bill.mwst[99] = bill.mwst[99] + amount-foreign. 

      IF bill.datum LT bill-date OR bill.datum = ? THEN bill.datum = bill-date. 
      IF bill.rechnr = 0 THEN 
      DO: 
        FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
        counters.counter = counters.counter + 1. 
        bill.rechnr = counters.counter. 
        FIND CURRENT counter NO-LOCK. 
      END.

      IF rechnr = 0 AND bill.rechnr NE 0 THEN
      DO:
        flag1 = 1.
        rechnr = bill.rechnr. 
        /*MT
        IF double-currency THEN 
          b11:TITLE IN FRAME frame1 = b-title + "     BillNo: " + STRING(rechnr). 
        ELSE b1:TITLE IN FRAME frame1 = b-title + "     BillNo: " + STRING(rechnr). 
        */
      END.

      FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
      na-running = htparam.flogical. 
      /* FDL comment move above ticket 3BF19F
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
      bill-date = vhp.htparam.fdate. 
      */
      IF transdate NE ? THEN bill-date = transdate. 
      ELSE
      DO:
        IF na-running AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
      END.

      FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN gastnrmember = res-line.gastnrmember. 
      ELSE gastnrmember = bill.gastnr. 
      
      CREATE bill-line. 
      ASSIGN
          bill-line.rechnr = bill.rechnr
          bill-line.artnr = billart
          bill-line.bezeich = DESCRIPTION 
          bill-line.anzahl = qty
          bill-line.betrag = amount 
          bill-line.fremdwbetrag = amount-foreign
          bill-line.zinr = curr-room 
          bill-line.departement = artikel.departement
          bill-line.bill-datum = bill-date
          bill-line.zeit = currZeit
          bill-line.userinit = user-init 
      . 
      
      IF voucher-nr NE "" THEN bill-line.bezeich = bill-line.bezeich 
        + "/" + voucher-nr. 

      IF artikel.artart = 9 THEN 
      DO:
        FIND FIRST arrangement WHERE arrangement.argt-artikelnr 
          = artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement AND AVAILABLE res-line THEN 
          bill-line.epreis = res-line.zipreis.
      END.
      ELSE IF artikel.artart NE 2 AND artikel.artart NE 4 AND artikel.artart NE 6 
        AND artikel.artart NE 7 THEN bill-line.epreis = price. 

      IF AVAILABLE res-line THEN 
      ASSIGN 
        bill-line.massnr = res-line.resnr
        bill-line.billin-nr = res-line.reslinnr 
        bill-line.arrangement = res-line.arrangement
      . 

      IF artikel.artart = 9 AND artikel.artgrp = 0 AND AVAILABLE res-line THEN 
      DO: 
        FIND FIRST arrangement WHERE 
          arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 
        IF AVAILABLE arrangement THEN
        bill-line.bezeich = arrangement.argt-rgbez.
      END. 
      FIND CURRENT bill-line NO-LOCK. 

      FIND FIRST umsatz WHERE umsatz.artnr = billart 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz. 
        ASSIGN
          umsatz.artnr = billart
          umsatz.datum = bill-date 
          umsatz.departement = artikel.departement
        . 
      END.
      ASSIGN
        umsatz.betrag = umsatz.betrag + amount
        umsatz.anzahl = umsatz.anzahl + qty
      . 
      FIND CURRENT umsatz NO-LOCK. 
      
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = bill.rechnr
        billjournal.artnr = billart
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = amount-foreign
        billjournal.betrag = amount
        billjournal.bezeich = DESCRIPTION 
        billjournal.zinr = curr-room
        billjournal.departement = artikel.departement
        billjournal.epreis = price
        billjournal.zeit = currZeit 
        billjournal.stornogrund = cancel-str 
        billjournal.userinit = user-init
        billjournal.bill-datum = bill-date
        cancel-str   = ""
        cancel-flag  = NO 
        void-approve = NO
      . 
      
      IF AVAILABLE res-line THEN
      billjournal.comment = STRING(res-line.resnr) + ";" 
        + STRING(res-line.reslinnr).

      IF voucher-nr NE "" THEN billjournal.bezeich = billjournal.bezeich 
        + "/" + voucher-nr. 
      FIND CURRENT billjournal NO-LOCK. 
    END. 
    
    IF artikel.artart = 2 OR artikel.artart = 7 THEN 
      RUN inv-ar(billart, curr-room, bill.gastnr, gastnrmember, bill.rechnr, 
      amount, amount-foreign, bill-date, bill.name, user-init, voucher-nr). 
    
    IF artikel.artart = 9 THEN 
    DO: 
      IF artikel.artgrp = 0 THEN RUN rev-bdown(currZeit). 
      ELSE RUN rev-bdown1(currZeit). 
    END. 
    

    balance = bill.saldo. 
    IF double-currency OR foreign-rate THEN balance-foreign = bill.mwst[99]. 
    
    flag3 = 1.
    /*MT
    IF balance LE kreditlimit THEN bcol = 2. 
    ELSE RUN red-bcol. 
    */
    FIND CURRENT bill NO-LOCK NO-ERROR. 
    CREATE t-bill.
    BUFFER-COPY bill TO t-bill.

    /*MT
    IF artikel.artart = 6 AND amount GT 0 THEN RUN print-receipt.

    IF AVAILABLE bill AND bill.flag = 0 AND bill.billnr GT 1 THEN 
      MENU-ITEM mi-close:SENSITIVE IN MENU mbar = (bill.saldo = 0). 
    ELSE MENU-ITEM mi-close:SENSITIVE IN MENU mbar = NO. 
    IF AVAILABLE bill THEN RUN disp-bill-line. 
    */
END.

PROCEDURE inv-ar:
  DEFINE INPUT PARAMETER curr-art       AS INTEGER.
  DEFINE INPUT PARAMETER zinr           LIKE zimmer.zinr.   /*MT 20/07/12 change zinr format */
  DEFINE INPUT PARAMETER gastnr         AS INTEGER.
  DEFINE INPUT PARAMETER gastnrmember   AS INTEGER.
  DEFINE INPUT PARAMETER rechnr         AS INTEGER.
  DEFINE INPUT PARAMETER saldo          AS DECIMAL.
  DEFINE INPUT PARAMETER saldo-foreign  AS DECIMAL.
  DEFINE INPUT PARAMETER bill-DATE      AS DATE.
  DEFINE INPUT PARAMETER billname       AS CHAR.
  DEFINE INPUT PARAMETER userinit       AS CHAR FORMAT "x(2)".
  DEFINE INPUT PARAMETER voucher-nr     AS CHAR.

  DEFINE VARIABLE comment               AS CHAR INITIAL "".
  DEFINE VARIABLE verstat               AS INTEGER INITIAL 0.
  DEFINE VARIABLE fsaldo                AS DECIMAL INITIAL 0.
  DEFINE VARIABLE lsaldo                AS DECIMAL INITIAL 0.
  DEFINE VARIABLE FOReign-rate          AS LOGICAL.  
  DEFINE VARIABLE currency-nr           AS INTEGER INITIAL 0 NO-UNDO.
  DEFINE VARIABLE double-currency       AS LOGICAL.  

  DEFINE BUFFER debt                    FOR debitor.
  DEFINE BUFFER debt1                   FOR debitor.
  DEFINE BUFFER main-res                FOR reservation.
  DEFINE BUFFER resline                 FOR res-line.
  DEFINE BUFFER bill1                   FOR bill.
  DEFINE BUFFER bline                   FOR bill-line.
  DEFINE BUFFER guest1                  FOR guest.

  FIND FIRST htparam WHERE paramnr = 143 NO-LOCK.
  foreign-rate = htparam.flogical.

  FIND FIRST htparam WHERE paramnr = 240 NO-LOCK.
  double-currency = htparam.flogical.

  FIND FIRST bediener WHERE bediener.userinit = userinit NO-LOCK.
  
  FIND FIRST htparam WHERE paramnr = 997 NO-LOCK.
  IF NOT htparam.flogical THEN RETURN.

  FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
  billname = STRING(guest.name + ", " + guest.vorname1 + " " 
    + guest.anrede1 + guest.anredefirma, "x(36)").
      
  FIND FIRST debt WHERE debt.artnr = curr-art
    AND debt.rechnr = rechnr AND debt.opart = 0 
    AND debt.rgdatum = bill-DATE AND debt.counter = 0 
    AND debt.saldo = saldo NO-LOCK NO-ERROR.

  IF AVAILABLE debt THEN
  DO:
    /*FIND CURRENT debt EXCLUSIVE-LOCK.
    DELETE debt.
    RETURN.*/
    FIND FIRST debt1 WHERE RECID(debt1) = RECID(debt) EXCLUSIVE-LOCK
        NO-ERROR.
    IF AVAILABLE debt1 THEN
    DO:
      DELETE debt1.
      RELEASE debt1.
      RETURN.
    END.
    ELSE
    DO:
        CREATE debt1.
        BUFFER-COPY debt TO debt1.
        ASSIGN 
            debt1.saldo       = - debt1.saldo
            debt1.bediener-nr = bediener.nr
            debt1.transzeit   = TIME
        .
        FIND CURRENT debt1 NO-LOCK.
        RELEASE debt1.
        RETURN.
    END.
  END.

  FIND FIRST bill1 WHERE bill1.rechnr = rechnr NO-LOCK NO-ERROR.

  IF AVAILABLE bill1 AND bill1.resnr NE 0 THEN
  DO:
    FIND FIRST resline WHERE resline.resnr = bill1.resnr
      AND resline.active-flag LE 2 AND resline.resstatus LE 8 
      AND resline.zipreis NE 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    FIND FIRST resline WHERE resline.resnr = bill1.resnr
      AND resline.active-flag LE 2 AND resline.resstatus LE 8 
      NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN currency-nr = resline.betriebsnr. 
    
    FIND FIRST main-res WHERE main-res.resnr = bill1.resnr NO-LOCK NO-ERROR.
    IF AVAILABLE main-res THEN comment = main-res.groupname.
    IF comment = "" AND gastnrmember NE gastnr THEN
    DO:
      FIND FIRST guest1 WHERE guest1.gastnr = gastnrmember NO-LOCK NO-ERROR.
      IF AVAILABLE guest1 THEN
      DO:
        comment = STRING(guest1.name + "," + guest1.vorname1,"x(20)").
        IF AVAILABLE resline THEN
          comment = comment + " " + STRING(resline.ankunft) + "-"
            + STRING(resline.abreise).
      END.
    END.

    IF bill1.reslinnr = 0 THEN verstat = 1. 

    IF AVAILABLE main-res AND main-res.insurance THEN
    DO:
      FIND FIRST resline WHERE resline.resnr = main-res.resnr
        AND resline.reserve-dec NE 0 AND resline.reserve-dec NE 1
        NO-LOCK NO-ERROR.
      IF AVAILABLE resline THEN saldo-foreign = saldo / resline.reserve-dec.
    END.
  END.
  ELSE IF AVAILABLE bill1 AND bill1.resnr = 0 THEN
    comment = bill1.bilname.

  CREATE debitor.
  ASSIGN
    debitor.artnr           = curr-art
    debitor.betrieb-gastmem = currency-nr
    debitor.zinr            = zinr
    debitor.gastnr          = gastnr
    debitor.gastnrmember    = gastnrmember
    debitor.rechnr          = rechnr
    debitor.saldo           = - saldo
    debitor.transzeit       = TIME
    debitor.rgdatum         = bill-DATE
    debitor.bediener-nr     = bediener.nr
    debitor.name            = billname
    /*debitor.vesrcod         = comment*/
    debitor.verstat         = verstat
  .

  IF double-currency or foreign-rate THEN 
      debitor.vesrdep    = - saldo-foreign.
  debitor.vesrcod = comment + ";" + voucher-nr + ";".
  
  /*IF voucher-nr NE "" THEN
  DO:
      IF comment NE "" THEN 
          ASSIGN debitor.vesrcod = voucher-nr + ";" + debitor.vesrcod + ";".
      ELSE ASSIGN debitor.vesrcod = voucher-nr + ";".
  END.*/

  RELEASE debitor.
  
END. 


PROCEDURE rev-bdown1: 
DEFINE INPUT PARAMETER currZeit AS INTEGER.
DEFINE BUFFER artikel1 FOR artikel. 
DEFINE VARIABLE rest-betrag AS DECIMAL. 
DEFINE VARIABLE argt-betrag AS DECIMAL. 
DEFINE VARIABLE p-sign AS INTEGER INITIAL 1 NO-UNDO. 
  
  rest-betrag = amount. 
  IF qty LT 0 THEN p-sign = -1. 
  
  FIND FIRST arrangement WHERE arrangement.argtnr = artikel.artgrp NO-LOCK. 
  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK: 
    IF argt-line.betrag NE 0 THEN 
    DO: 
      argt-betrag = argt-line.betrag * qty. 
      IF double-currency OR artikel.pricetab THEN 
        argt-betrag = round(argt-betrag * exchg-rate, price-decimal). 
    END. 
    ELSE 
    DO: 
      argt-betrag = amount * argt-line.vt-percnt / 100. 
      argt-betrag = round(argt-betrag, price-decimal). 
    END. 
    rest-betrag = rest-betrag - argt-betrag. 
    FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr 
      AND artikel1.departement = argt-line.departement NO-LOCK. 
    FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
      AND umsatz.departement = artikel1.departement 
      AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE umsatz THEN 
    DO: 
      CREATE umsatz. 
      ASSIGN
        umsatz.artnr = artikel1.artnr
        umsatz.datum = bill-date
        umsatz.departement = artikel1.departement
      . 
    END.
    ASSIGN
      umsatz.betrag = umsatz.betrag + argt-betrag
      umsatz.anzahl = umsatz.anzahl + qty
    . 
    FIND CURRENT umsatz NO-LOCK. 
    
    
    CREATE billjournal. 
    ASSIGN
      billjournal.rechnr = bill.rechnr
      billjournal.artnr = artikel1.artnr 
      billjournal.anzahl = qty
      billjournal.fremdwaehrng = argt-line.betrag
      billjournal.betrag = argt-betrag
      billjournal.bezeich = artikel1.bezeich
      billjournal.zinr = curr-room
      billjournal.departement = artikel1.departement
      billjournal.epreis = 0 
      billjournal.zeit = currZeit
      billjournal.stornogrund = cancel-str 
      billjournal.userinit = user-init
      billjournal.bill-datum = bill-date
    . 
    FIND CURRENT billjournal NO-LOCK. 
    
  END. 
 
  FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
    AND artikel1.departement = arrangement.intervall NO-LOCK. 
  FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
    AND umsatz.departement = artikel1.departement 
    AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz.
    ASSIGN
      umsatz.artnr = artikel1.artnr
      umsatz.datum = bill-date
      umsatz.departement = artikel1.departement
    . 
  END.
  ASSIGN
    umsatz.betrag = umsatz.betrag + rest-betrag
    umsatz.anzahl = umsatz.anzahl + qty
  . 
  FIND CURRENT umsatz NO-LOCK. 
  
  CREATE billjournal. 
  ASSIGN
    billjournal.rechnr = bill.rechnr
    billjournal.artnr = artikel1.artnr 
    billjournal.anzahl = qty
    billjournal.betrag = rest-betrag
    billjournal.bezeich = artikel1.bezeich 
    billjournal.zinr = curr-room
    billjournal.departement = artikel1.departement 
    billjournal.epreis = 0
    billjournal.zeit = currZeit
    billjournal.stornogrund = cancel-str
    billjournal.userinit = user-init 
    billjournal.bill-datum = bill-date
  . 
  
  IF double-currency THEN 
    billjournal.fremdwaehrng = round(rest-betrag / exchg-rate, 6). 
  
  FIND CURRENT billjournal NO-LOCK. 
END. 

PROCEDURE rev-bdown:
DEFINE INPUT PARAMETER currZeit AS INTEGER.
  RUN fo-invoice-rev-bdownbl.p
      (bil-recid, currZeit, exchg-rate, amount, artikel.artnr,
       artikel.departement, arrangement.argtnr, price-decimal, bill-date, 
       curr-room, cancel-str, user-init, curr-department, qty,
       double-currency, foreign-rate, price, balance-foreign, OUTPUT balance).
  flag2 = 1.
  /*MT
  IF balance LE kreditlimit THEN bcol = 2. 
  ELSE RUN red-bcol. 
  */
END. 
