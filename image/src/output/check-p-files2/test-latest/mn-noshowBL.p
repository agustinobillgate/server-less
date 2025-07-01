DEFINE WORKFILE reslist 
   FIELD resnr AS INTEGER. 

DEFINE INPUT  PARAMETER pvILanguage   AS INTEGER      NO-UNDO.
DEFINE OUTPUT PARAMETER i             AS INTEGER INIT 0 NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str       AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mn-start".

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN noshow.

PROCEDURE noshow: 
DEFINE VARIABLE res-recid1 AS INTEGER. 
DEFINE BUFFER rline        FOR res-line.

  FIND FIRST res-line NO-LOCK WHERE 
    res-line.active-flag = 0 AND 
    res-line.resstatus LE 5  AND 
    res-line.ankunft LT ci-date NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    DO TRANSACTION: 
      i = i + 1. 
      FIND FIRST reslist WHERE reslist.resnr = res-line.resnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reslist THEN 
      DO: 
        CREATE reslist. 
        reslist.resnr = res-line.resnr. 
      END. 
 
      IF res-line.zinr NE "" THEN 
      DO: 
        res-recid1 = RECID(res-line). 
        FOR EACH zimplan WHERE zimplan.zinr = res-line.zinr 
          AND zimplan.datum GE ci-date 
          AND zimplan.datum LE res-line.abreise 
          AND zimplan.res-recid = res-recid1 EXCLUSIVE-LOCK: 
          delete zimplan. 
        END. 
      END. 
 
      RUN check-noshow-deposit (res-line.resnr).
      FIND CURRENT res-line EXCLUSIVE-LOCK. 

      IF (res-line.resstatus LE 2 OR res-line.resstatus = 5) THEN
      DO:
        ASSIGN 
          res-line.betrieb-gastpay = res-line.resstatus
          res-line.resstatus = 10      /* noshow */ 
          res-line.active-flag = 2. 
        FIND CURRENT res-line NO-LOCK. 
 
        FOR EACH rline WHERE rline.resnr = res-line.resnr
          AND rline.resstatus = 11
          AND rline.kontakt-nr = res-line.reslinnr: /* roomshare and accompany */
          ASSIGN 
            rline.zimmerfix = YES
            rline.resstatus = 10      /* noshow */ 
            rline.active-flag = 2. 
          .
        END.

        FIND FIRST zinrstat WHERE zinrstat.zinr = "No-Show" 
          AND zinrstat.datum = res-line.ankunft NO-ERROR. 
        IF NOT AVAILABLE zinrstat THEN 
        DO: 
          CREATE zinrstat. 
          ASSIGN 
            zinrstat.datum = res-line.ankunft 
            zinrstat.zinr = "No-Show". 
        END.
        ASSIGN
          zinrstat.zimmeranz = zinrstat.zimmeranz + res-line.zimmeranz
          zinrstat.personen = zinrstat.personen + res-line.erwachs
        . 
 
        FIND FIRST guest WHERE guest.gastnr = 
          res-line.gastnrmember EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE guest THEN 
        DO: 
          guest.noshows = guest.noshows + 1. 
          FIND CURRENT guest NO-LOCK. 
        END. 
      END.
      ELSE
      DO:
        ASSIGN 
          res-line.betrieb-gastpay = res-line.resstatus
          res-line.resstatus       = 9      /* cancelled */ 
          res-line.cancelled-id    = "$$" 
             + ";" + STRING(TODAY) + "-" + STRING(TIME,"HH:MM:SS")
          res-line.active-flag     = 2
        . 
        FIND CURRENT res-line NO-LOCK. 
 
        FOR EACH rline WHERE rline.resnr = res-line.resnr
          AND rline.resstatus = 11
          AND rline.kontakt-nr = res-line.reslinnr: /* roomshare and accompany */
          ASSIGN 
            rline.zimmerfix          = YES
            rline.resstatus          = 9      /* cancelled */ 
            res-line.cancelled-id    = "$$" 
               + ";" + STRING(TODAY) + "-" + STRING(TIME,"HH:MM:SS")
            rline.active-flag        = 2
          . 
        END.
      END.
    END.
    
    FIND NEXT res-line NO-LOCK WHERE 
      res-line.active-flag = 0 AND 
      res-line.resstatus LE 5  AND 
      res-line.ankunft LT ci-date NO-ERROR. 

  END. 
  
/* remain no-show of room sharer as main guest already checked-in 
   and not found in previous loops */
  FIND FIRST res-line NO-LOCK WHERE 
    res-line.active-flag = 0 AND 
    res-line.resstatus EQ 11 AND 
    res-line.ankunft LT ci-date NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    DO TRANSACTION: 
      i = i + 1. 
      FIND CURRENT res-line EXCLUSIVE-LOCK. 
      ASSIGN 
          res-line.betrieb-gastpay = res-line.resstatus
          res-line.resstatus = 10      /* noshow */ 
          res-line.active-flag = 2. 
      FIND CURRENT res-line NO-LOCK. 
    END. 
    FIND NEXT res-line NO-LOCK WHERE 
      res-line.active-flag = 0 AND 
      res-line.resstatus EQ 11 AND 
      res-line.ankunft LT ci-date NO-ERROR. 
  END. 
  
  FOR EACH reslist: 
    FIND FIRST res-line WHERE res-line.resnr = reslist.resnr 
      AND res-line.active-flag LT 2 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN 
    DO TRANSACTION: 
      FIND FIRST reservation WHERE reservation.resnr = reslist.resnr 
        EXCLUSIVE-LOCK. 
      reservation.activeflag = 1. 
      FIND CURRENT reservation NO-LOCK. 
    END. 
    delete reslist. 
  END. 

  PAUSE 0. 
END. 


PROCEDURE check-noshow-deposit:
DEF INPUT PARAMETER resNo    AS INTEGER NO-UNDO.
DEF VARIABLE bill-date       AS DATE    NO-UNDO.
DEF VARIABLE deposit         AS DECIMAL NO-UNDO.
DEF VARIABLE deposit-foreign AS DECIMAL NO-UNDO.
DEF VARIABLE sys-id          AS CHAR    NO-UNDO. 

DEF BUFFER   depoArt         FOR artikel.
DEF BUFFER   art1            FOR artikel.
DEF BUFFER   gbuff           FOR guest.

  FIND FIRST reservation WHERE reservation.resnr = resNo NO-LOCK.
  IF reservation.depositbez EQ 0 OR reservation.bestat-datum NE ? THEN RETURN.
  FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
  FIND FIRST depoArt WHERE depoArt.artnr = htparam.finteger 
    AND depoArt.departement = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE depoArt THEN RETURN.

  FIND FIRST htparam WHERE htparam.paramnr = 104 NO-LOCK. 
  sys-id = htparam.fchar. 
  FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
  ASSIGN bill-date = htparam.fdate.
  FIND FIRST art1 WHERE art1.artnr = reservation.zahlkonto 
    AND art1.departement = 0 NO-LOCK NO-ERROR. 

  FIND CURRENT reservation EXCLUSIVE-LOCK. 
  ASSIGN reservation.bestat-dat = bill-date. 
  FIND CURRENT reservation NO-LOCK.

  RUN calculate-deposit-amount(bill-date, OUTPUT deposit, OUTPUT deposit-foreign).

  FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK.
  counters.counter = counters.counter + 1. 
  FIND CURRENT counter NO-LOCK.
  FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK.

  CREATE bill.
  ASSIGN
      bill.gastnr   = reservation.gastnr
      bill.rechnr   = counters.counter
      bill.datum    = bill-date
      bill.billtyp  = 0
      bill.NAME     = gbuff.NAME + ", " + gbuff.vorname1 + gbuff.anredefirma
      bill.bilname  = bill.NAME
      bill.resnr    = 0
      bill.reslinnr = 1
      bill.saldo    = deposit /* deposit value is negative */ 
      bill.mwst[99] = deposit-foreign
      bill.rgdruck  = 0
  . 
  FIND CURRENT bill NO-LOCK.

  FIND FIRST art1 WHERE art1.artnr = reservation.zahlkonto 
      AND art1.departement = 0 NO-LOCK NO-ERROR. 

  CREATE bill-line. 
  ASSIGN
    bill-line.rechnr        = bill.rechnr
    bill-line.artnr         = depoArt.artnr
    bill-line.bezeich       = depoArt.bezeich 
    bill-line.anzahl        = 1
    bill-line.betrag        = deposit 
    bill-line.fremdwbetrag  = deposit-foreign
    bill-line.zeit          = TIME
    bill-line.userinit      = sys-id 
    bill-line.zinr          = res-line.zinr
    bill-line.massnr        = res-line.resnr
    bill-line.billin-nr     = res-line.reslinnr 
    bill-line.arrangement   = res-line.arrangement 
    bill-line.bill-datum    = bill-date
  . 

  IF AVAILABLE art1 THEN 
      bill-line.bezeich = bill-line.bezeich + " [" + art1.bezeich + "]". 

  FIND CURRENT bill-line NO-LOCK. 

  CREATE billjournal. 
  ASSIGN
    billjournal.rechnr          = bill.rechnr
    billjournal.artnr           = depoArt.artnr 
    billjournal.anzahl          = 1
    billjournal.fremdwaehrng    = deposit-foreign
    billjournal.betrag          = deposit
    billjournal.bezeich         = depoArt.bezeich + " " 
                                + STRING(reservation.resnr) 
    billjournal.zinr            = res-line.zinr
    billjournal.epreis          = 0
    billjournal.zinr            = res-line.zinr
    billjournal.zeit            = TIME 
    billjournal.userinit        = sys-id
    billjournal.bill-datum      = bill-date
  . 

  IF AVAILABLE art1 THEN 
    billjournal.bezeich = billjournal.bezeich + " [" + art1.bezeich + "]". 

  FIND CURRENT billjournal NO-LOCK. 

  FIND FIRST umsatz WHERE umsatz.artnr = depoArt.artnr 
  AND umsatz.departement = 0 
  AND umsatz.datum = bill-date EXCLUSIVE-LOCK  NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz. 
    umsatz.artnr = depoArt.artnr. 
    umsatz.datum = bill-date. 
  END. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  umsatz.betrag = umsatz.betrag + deposit. 
  FIND CURRENT umsatz NO-LOCK. 

  msg-str = msg-str + CHR(2) + "&W"
          + translateExtended ("No-show guest with PAID deposit found:",lvCAREA,"")
          + CHR(10)
          + STRING(res-line.resnr) + " - " + res-line.NAME
          + CHR(10)
          + translateExtended ("Deposit amount automatically posted to bill number", lvCAREA,"")
          + " " + STRING(bill.rechnr).

END.


PROCEDURE calculate-deposit-amount: 
DEFINE INPUT  PARAMETER bill-date       AS DATE              NO-UNDO.
DEFINE OUTPUT PARAMETER deposit         AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE OUTPUT PARAMETER deposit-foreign AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE deposit-exrate          AS DECIMAL INITIAL 1 NO-UNDO. 
DEFINE VARIABLE exchg-rate              AS DECIMAL           NO-UNDO.    
  FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
  FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
    AND artikel.departement = 0 NO-LOCK. 
  
  IF NOT artikel.pricetab THEN
    ASSIGN deposit = - reservation.depositbez - reservation.depositbez2. 
  ELSE
  DO:
    deposit-exrate = 1.
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
      NO-LOCK NO-ERROR.
    IF reservation.zahldatum = bill-date THEN
    DO:
      IF AVAILABLE waehrung THEN 
        deposit-exrate = waehrung.ankauf / waehrung.einheit.
    END.
    ELSE
    DO:
      FIND FIRST exrate WHERE exrate.artnr = artikel.betriebsnr
        AND exrate.datum = reservation.zahldatum NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN deposit-exrate = exrate.betrag.
      ELSE IF AVAILABLE waehrung THEN
        deposit-exrate = waehrung.ankauf / waehrung.einheit.
    END.
    deposit = - reservation.depositbez * deposit-exrate.
    IF reservation.depositbez2 NE 0 THEN
    DO:
      deposit-exrate = 1.
      IF reservation.zahldatum = bill-date THEN
      DO:
        IF AVAILABLE waehrung THEN 
          deposit-exrate = waehrung.ankauf / waehrung.einheit.
      END.
      ELSE
      DO:
        FIND FIRST exrate WHERE exrate.artnr = artikel.betriebsnr
          AND exrate.datum = reservation.zahldatum2 NO-LOCK NO-ERROR.
        IF AVAILABLE exrate THEN deposit-exrate = exrate.betrag.
        ELSE IF AVAILABLE waehrung THEN 
          deposit-exrate = waehrung.ankauf / waehrung.einheit.
      END.
    END.
    deposit = deposit - reservation.depositbez2 * deposit-exrate.
  END.
    
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  ASSIGN deposit-foreign = ROUND(deposit / exchg-rate, 2).
END.
