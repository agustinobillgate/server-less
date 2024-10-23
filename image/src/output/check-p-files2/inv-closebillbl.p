DEFINE INPUT PARAMETER invoice-type AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER s-recid      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER curr-dept    AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER transdate    AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER bill-recid  AS INTEGER  NO-UNDO.

DEFINE VARIABLE bill-date   AS DATE    NO-UNDO. 
DEFINE VARIABLE ba-dept     AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-billnr AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-anzahl AS INTEGER NO-UNDO.
DEFINE VARIABLE max-anzahl  AS INTEGER NO-UNDO.

DEFINE BUFFER bill1 FOR bill.

FIND FIRST bill WHERE RECID(bill) = s-recid NO-LOCK.
/*FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK.*/
/*ITA 300617*/
FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN RETURN.

FIND FIRST htparam WHERE htparam.paramnr = 985 no-lock. /* Banquet License */ 
IF htparam.flogical THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK. 
  IF htparam.finteger NE 0 THEN ba-dept = htparam.finteger. 
END. 

FIND FIRST htparam WHERE paramnr = 1002 no-lock. /* license Sales */ 
IF htparam.flogical AND invoice-type NE "guest" THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
  bill-date = vhp.htparam.fdate. 
  IF transdate NE ? THEN bill-date = transdate. 
  ELSE
  DO:
    FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
    IF htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
  END.
                  
  FIND FIRST guestat WHERE guestat.gastnr = bill.gastnr 
      AND guestat.monat = month(bill-date) 
      AND guestat.jahr = year(bill-date) 
      AND guestat.betriebsnr = 0 EXCLUSIVE-LOCK NO-ERROR. 
          
  IF NOT AVAILABLE guestat THEN 
  DO: 
    CREATE guestat. 
    ASSIGN
        guestat.gastnr = bill.gastnr 
        guestat.monat  = MONTH(bill-date) 
        guestat.jahr   = YEAR(bill-date)
    . 
  END. 
  ASSIGN
      guestat.logisumsatz  = guestat.logisumsatz + bill.logisumsatz 
      guestat.argtumsatz   = guestat.argtumsatz + bill.argtumsatz
      guestat.f-b-umsatz   = guestat.f-b-umsatz + bill.f-b-umsatz 
      guestat.sonst-umsatz = guestat.sonst-umsatz + bill.sonst-umsatz 
      guestat.gesamtumsatz = guestat.gesamtumsatz + bill.gesamtumsatz
  . 
  FIND CURRENT guestat NO-LOCK. 
END. 
 
IF curr-dept = ba-dept AND invoice-type = "NS" THEN RUN close-banquet. 
ELSE IF invoice-type = "master" THEN
DO:
DEF BUFFER usrbuff FOR bediener.
DEF BUFFER rguest  FOR guest.
    FIND FIRST akt-cust WHERE akt-cust.gastnr = bill.gastnr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE akt-cust THEN 
    DO: 
      FIND FIRST usrbuff WHERE usrbuff.userinit = akt-cust.userinit 
        NO-LOCK NO-ERROR. 
    END. 
    IF NOT AVAILABLE akt-cust OR NOT AVAILABLE usrbuff THEN 
    DO: 
      FIND FIRST rguest WHERE rguest.gastnr = bill.gastnr NO-LOCK. 
      IF rguest.phonetik3 NE "" THEN 
      DO: 
        FIND FIRST usrbuff WHERE usrbuff.userinit = rguest.phonetik3 
          NO-LOCK NO-ERROR. 
      END. 
    END. 
    IF AVAILABLE usrbuff THEN 
    DO: 
      FIND FIRST salestat WHERE salestat.bediener-nr = usrbuff.nr 
        AND salestat.jahr = YEAR(bill-date) 
        AND salestat.monat = MONTH(bill-date) EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE salestat THEN 
      DO: 
        CREATE salestat. 
        ASSIGN 
          salestat.bediener-nr = usrbuff.nr 
          salestat.jahr = YEAR(bill-date) 
          salestat.monat = MONTH(bill-date) 
        . 
      END. 
      ASSIGN 
        salestat.logisumsatz = salestat.logisumsatz + bill.logisumsatz 
        salestat.argtumsatz = salestat.argtumsatz + bill.argtumsatz 
        salestat.f-b-umsatz = salestat.f-b-umsatz + bill.f-b-umsatz 
        salestat.sonst-umsatz = salestat.sonst-umsatz + bill.sonst-umsatz 
        salestat.gesamtumsatz = salestat.gesamtumsatz + bill.gesamtumsatz 
      . 
      FIND CURRENT salestat NO-LOCK. 
    END. 
END.

IF invoice-type EQ "guest" THEN 
DO:
  ASSIGN
    curr-billnr = bill.billnr 
    bill-anzahl = 0
  . 
  FOR EACH bill1 WHERE bill1.resnr = bill.resnr 
    AND bill1.parent-nr = bill.parent-nr 
    AND bill1.parent-nr NE 0 
    AND bill1.flag = 0 AND bill1.zinr = bill.zinr NO-LOCK: 
    bill-anzahl = bill-anzahl + 1. 
  END. 
  IF bill-anzahl NE curr-billnr THEN 
  DO: 
    FIND FIRST bill1 WHERE bill1.resnr = bill.resnr 
      AND bill1.parent-nr = bill.parent-nr AND bill1.billnr EQ bill-anzahl 
      AND bill1.flag = 0 AND bill1.zinr = bill.zinr EXCLUSIVE-LOCK. 
    bill1.billnr = curr-billnr. 
    FIND CURRENT bill1 NO-LOCK. 
  END. 
  max-anzahl = bill-anzahl + 1. 
  IF max-anzahl LT 5 THEN max-anzahl = 5. 
  FOR EACH bill1 WHERE bill1.resnr = bill.resnr 
    AND bill1.parent-nr = bill.parent-nr 
    AND bill1.parent-nr NE 0 
    AND bill1.flag = 1 AND bill1.zinr = bill.zinr NO-LOCK: 
    max-anzahl = max-anzahl + 1. 
  END. 
  FIND CURRENT bill EXCLUSIVE-LOCK. 
  ASSIGN
    bill.billnr  = max-anzahl
    bill.vesrcod = user-init
  . 
  FIND CURRENT bill NO-LOCK. 
 
  FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.reslinnr 
    AND res-line.zinr = bill.zinr EXCLUSIVE-LOCK. 
  ASSIGN
    res-line.abreise     = bill-date 
    res-line.abreisezeit = TIME
    res-line.changed     = TODAY 
    res-line.changed-id  = user-init 
    res-line.active-flag = 2
  . 
  FIND CURRENT res-line NO-LOCK. 
 
  FIND FIRST bill1 WHERE bill1.resnr = bill.resnr 
    AND bill1.parent-nr = bill.parent-nr AND bill1.billnr = 1 
    AND bill1.flag = 0 AND bill1.zinr = bill.zinr NO-LOCK. 
  ASSIGN bill-recid = RECID(bill1). 
END.

FIND CURRENT bill EXCLUSIVE-LOCK. 
bill.flag = 1. 

/************************online tax vanguard (pengiriman realtime)*****************/
CREATE INTERFACE.
ASSIGN
    INTERFACE.KEY         = 38
    INTERFACE.action      = YES
    INTERFACE.nebenstelle = ""
    INTERFACE.parameters = "close-bill"
    INTERFACE.intfield    = bill.rechnr
    INTERFACE.decfield    = bill.billtyp
    INTERFACE.int-time    = TIME
    INTERFACE.intdate     = TODAY
    INTERFACE.resnr       = bill.resnr
    INTERFACE.reslinnr    = bill.reslinnr
  .
  FIND CURRENT INTERFACE NO-LOCK.
  RELEASE INTERFACE.
FIND CURRENT bill NO-LOCK.

PROCEDURE close-banquet: 
DEF VAR ci-date AS DATE NO-UNDO. 
/* 
  IF SUBSTR(bediener.perm, 45, 1) LT "2" THEN RETURN. 
*/ 
  FIND FIRST bk-veran WHERE bk-veran.rechnr = bill.rechnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE bk-veran THEN RETURN. 
 

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
  ci-date = htparam.fdate. 
 
  DO TRANSACTION: 
    FIND CURRENT bk-veran EXCLUSIVE-LOCK. 
    bk-veran.activeflag = 1. 
    FIND CURRENT bk-veran NO-LOCK. 
 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
      AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE bk-reser: 
      FIND CURRENT bk-reser EXCLUSIVE-LOCK. 
      bk-reser.resstatus = 8. 
      FIND CURRENT bk-reser NO-LOCK. 
      FIND NEXT bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
        AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
    END. 
 
    FIND FIRST bk-func WHERE bk-func.veran-nr = bk-veran.veran-nr 
      AND bk-func.resstatus = 1 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE bk-func: 
      RUN create-bahistory. 
      FIND CURRENT bk-func EXCLUSIVE-LOCK. 
      ASSIGN 
        bk-func.resstatus = 8 
        bk-func.c-resstatus[1] = "I" 
        bk-func.r-resstatus[1] = 8 
      . 
      FIND CURRENT bk-func NO-LOCK. 
 
      FIND NEXT bk-func WHERE bk-func.veran-nr = bk-veran.veran-nr 
        AND bk-func.resstatus = 1 NO-LOCK NO-ERROR. 
    END. 
 
    IF bk-veran.rechnr > 0 THEN 
    DO: 
      FIND CURRENT bill EXCLUSIVE-LOCK. 
      ASSIGN 
        bill.flag    = 1 
        bill.datum   = ci-date 
        bill.vesrcod = user-init 
      . 
      FIND CURRENT bill NO-LOCK. 
    END. 
  END. 
END. 
 

PROCEDURE create-bahistory: 
  CREATE b-history. 
  BUFFER-COPY bk-func TO b-history. 
  ASSIGN 
    b-history.deposit = bk-veran.deposit 
    b-history.limit-date          = bk-veran.limit-date 
    b-history.deposit-payment[1]  = bk-veran.deposit-payment[1] 
    b-history.deposit-payment[2]  = bk-veran.deposit-payment[2] 
    b-history.deposit-payment[3]  = bk-veran.deposit-payment[3] 
    b-history.deposit-payment[4]  = bk-veran.deposit-payment[4] 
    b-history.deposit-payment[5]  = bk-veran.deposit-payment[5] 
    b-history.deposit-payment[6]  = bk-veran.deposit-payment[6] 
    b-history.deposit-payment[7]  = bk-veran.deposit-payment[7] 
    b-history.deposit-payment[8]  = bk-veran.deposit-payment[8] 
    b-history.deposit-payment[9]  = bk-veran.deposit-payment[9] 
    b-history.payment-date[1]     = bk-veran.payment-date[1] 
    b-history.payment-date[2]     = bk-veran.payment-date[2] 
    b-history.payment-date[3]     = bk-veran.payment-date[3] 
    b-history.payment-date[4]     = bk-veran.payment-date[4] 
    b-history.payment-date[5]     = bk-veran.payment-date[5] 
    b-history.payment-date[6]     = bk-veran.payment-date[6] 
    b-history.payment-date[7]     = bk-veran.payment-date[7] 
    b-history.payment-date[8]     = bk-veran.payment-date[8] 
    b-history.payment-date[9]     = bk-veran.payment-date[9] 
    b-history.payment-userinit[1] = bk-veran.payment-userinit[1] 
    b-history.payment-userinit[2] = bk-veran.payment-userinit[2] 
    b-history.payment-userinit[3] = bk-veran.payment-userinit[3] 
    b-history.payment-userinit[4] = bk-veran.payment-userinit[4] 
    b-history.payment-userinit[5] = bk-veran.payment-userinit[5] 
    b-history.payment-userinit[6] = bk-veran.payment-userinit[6] 
    b-history.payment-userinit[7] = bk-veran.payment-userinit[7] 
    b-history.payment-userinit[8] = bk-veran.payment-userinit[8] 
    b-history.payment-userinit[9] = bk-veran.payment-userinit[9] 
    b-history.total-paid          = bk-veran.total-paid 
  . 
  FIND CURRENT b-history NO-LOCK. 
  RELEASE b-history. 
END. 
