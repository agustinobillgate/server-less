 
DEFINE TEMP-TABLE argt-list 
  FIELD argtnr          AS INTEGER INITIAL 0 
  FIELD argt-artnr      AS INTEGER INITIAL 0 
  FIELD departement     AS INTEGER INITIAL 0
  FIELD is-charged      AS INTEGER INITIAL 0
  FIELD period          AS INTEGER INITIAL 0
  FIELD vt-percnt       AS INTEGER INITIAL 0
. 

DEFINE INPUT PARAMETER res-recid  AS INTEGER. 
DEFINE INPUT PARAMETER argt-recid AS INTEGER. 
DEFINE OUTPUT PARAMETER betrag    AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER ex-rate   AS DECIMAL INITIAL 1. 
 
DEFINE VARIABLE add-it          AS LOGICAL INITIAL NO. 
DEFINE VARIABLE marknr          AS INTEGER. 
DEFINE VARIABLE bill-date       AS DATE. 
DEFINE VARIABLE argt-defined    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE foreign-rate    AS LOGICAL. 
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ct              AS CHAR.
DEFINE VARIABLE contcode        AS CHAR.
DEFINE VARIABLE curr-zikatnr    AS INTEGER              NO-UNDO. 
DEFINE buffer w1                FOR waehrung. 
 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
bill-date = htparam.fdate. 
 
FIND FIRST htparam WHERE paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
 
FIND FIRST res-line WHERE RECID(res-line) = res-recid NO-LOCK. 
FIND FIRST argt-line WHERE RECID(argt-line) = argt-recid NO-LOCK. 
FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
FIND FIRST arrangement WHERE arrangement.argtnr = argt-line.argtnr NO-LOCK. 


IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
ELSE curr-zikatnr = res-line.zikatnr. 
 
IF argt-line.vt-percnt = 0 THEN 
DO: 
  IF argt-line.betriebsnr = 0 THEN qty = res-line.erwachs. 
  ELSE qty = argt-line.betriebsnr. 
END. 
ELSE IF argt-line.vt-percnt = 1 THEN qty = res-line.kind1. 
ELSE IF argt-line.vt-percnt = 2 THEN qty = res-line.kind2. 
IF qty = 0 THEN RETURN. 
 
IF argt-line.fakt-modus = 1 THEN add-it = YES. 
ELSE IF argt-line.fakt-modus = 2 THEN 
DO: 
  IF res-line.ankunft EQ bill-date THEN add-it = YES. 
END. 
ELSE IF argt-line.fakt-modus = 3 THEN 
DO: 
  IF (res-line.ankunft + 1) EQ bill-date THEN add-it = YES. 
END. 
ELSE IF argt-line.fakt-modus = 4 AND day(bill-date) = 1 THEN add-it = YES. 
ELSE IF argt-line.fakt-modus = 5 AND day(bill-date + 1) = 1 THEN add-it = YES. 
ELSE IF argt-line.fakt-modus = 6 THEN 
DO: 
  /* Dzikri 3DC423 - Repair Arrangemnt type 6
    IF (res-line.ankunft + (argt-line.intervall - 1)) GE bill-date 
      THEN add-it = YES. */
    FIND FIRST argt-list WHERE argt-list.argtnr EQ argt-line.argtnr 
      AND argt-list.departement EQ argt-line.departement 
      AND argt-list.argt-artnr  EQ argt-line.argt-artnr 
      AND argt-list.vt-percnt   EQ argt-line.vt-percnt
      AND argt-list.is-charged  EQ 0  NO-LOCK NO-ERROR.
    IF NOT AVAILABLE argt-list THEN
    DO:
      CREATE argt-list.
      ASSIGN
        argt-list.argtnr      = argt-line.argtnr 
        argt-list.departement = argt-line.departement 
        argt-list.argt-artnr  = argt-line.argt-artnr 
        argt-list.vt-percnt   = argt-line.vt-percnt
        argt-list.is-charged  = 0
        argt-list.period      = 0
      .
    END.
    IF argt-list.period LT argt-line.intervall THEN
    DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
        AND reslin-queasy.char1    = "" 
        AND reslin-queasy.number1  = argt-line.departement 
        AND reslin-queasy.number2  = argt-line.argtnr 
        AND reslin-queasy.resnr    = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        AND reslin-queasy.number3  = argt-line.argt-artnr 
        AND reslin-queasy.date1 LE res-line.abreise
        AND reslin-queasy.date2 GE res-line.ankunft NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO:
        IF reslin-queasy.date1 LE bill-date 
          AND reslin-queasy.date2 GE bill-date
          AND (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE bill-date THEN
        DO:
          add-it = YES.
          argt-list.period = argt-list.period + 1.
        END.
        ELSE
        DO:
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
            AND reslin-queasy.char1    = "" 
            AND reslin-queasy.number1  = argt-line.departement 
            AND reslin-queasy.number2  = argt-line.argtnr 
            AND reslin-queasy.resnr    = res-line.resnr 
            AND reslin-queasy.reslinnr = res-line.reslinnr 
            AND reslin-queasy.number3  = argt-line.argt-artnr 
            AND reslin-queasy.date1 LE bill-date
            AND reslin-queasy.date2 GE bill-date
            AND (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE bill-date NO-LOCK NO-ERROR.
          IF AVAILABLE reslin-queasy THEN
          DO:
            add-it = YES.
            argt-list.period = argt-list.period + 1.
          END.
        END.
      END.
      ELSE
      DO:
        IF res-line.ankunft + (argt-line.intervall - 1 /**/) GE bill-date THEN
        DO:
          add-it = YES.
          argt-list.period = argt-list.period + 1.
        END.
      END.
    END.
    
  /* Dzikri 3DC423 - END */
END. 
 
IF NOT add-it THEN RETURN. 
 
marknr = res-line.reserve-int. 
 
/* AdHoc Reservation */ 
FIND FIRST reslin-queasy WHERE key = "fargt-line" 
  AND reslin-queasy.char1 = "" 
  AND reslin-queasy.resnr = res-line.resnr 
  AND reslin-queasy.reslinnr = res-line.reslinnr 
  AND reslin-queasy.number1 = argt-line.departement 
  AND reslin-queasy.number2 =  argt-line.argtnr 
  AND reslin-queasy.number3 = argt-line.argt-artnr 
  AND reslin-queasy.date1 LE bill-date /* Malik Serverless : AND bill-date GE reslin-queasy.date1 -> AND reslin-queasy.date1 LE bill-date */
  AND reslin-queasy.date2 GE bill-date NO-LOCK NO-ERROR. /* Malik Serverless : AND bill-date LE reslin-queasy.date2 -> reslin-queasy.date2 GE bill-date */
IF AVAILABLE reslin-queasy THEN   /* AdHoc Ventillation */ 
DO: 
    argt-defined = YES. 
    IF reslin-queasy.char2 NE ""
        AND reslin-queasy.char2 NE "0" THEN betrag = (res-line.zipreis * INT(reslin-queasy.char2) / 100) * qty.  
    ELSE
    DO:
        /*betrag = reslin-queasy.deci1 * qty. */
        IF argt-line.vt-percnt = 0 THEN betrag = reslin-queasy.deci1 * qty. 
        ELSE IF argt-line.vt-percnt = 1 THEN betrag = reslin-queasy.deci2 * qty. 
        ELSE IF argt-line.vt-percnt = 2 THEN betrag = reslin-queasy.deci3 * qty. 
    END.
    RUN get-exrate1. 
    RETURN. 
END. 
 
/*  reservation under contract rates */ 
FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE guest-pr THEN 
DO:
  contcode = guest-pr.CODE.
  ct = res-line.zimmer-wunsch.
  IF ct MATCHES("*$CODE$*") THEN
  DO:
    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
  END.
END.

IF AVAILABLE guest-pr /*AND marknr NE 0*/ AND NOT argt-defined THEN 
DO: 
  FIND FIRST reslin-queasy WHERE key = "argt-line" 
    AND reslin-queasy.char1 = contcode 
    AND reslin-queasy.number1 = marknr 
    AND reslin-queasy.number2 =  argt-line.argtnr 
    AND reslin-queasy.reslinnr = /*res-line.zikatnr */ curr-zikatnr
    AND reslin-queasy.number3 = argt-line.argt-artnr 
    AND reslin-queasy.resnr = argt-line.departement 
    AND reslin-queasy.date1 LE bill-date /* Malik Serverless : AND bill-date GE reslin-queasy.date1 -> AND reslin-queasy.date1 LE bill-date */
    AND reslin-queasy.date2 GE bill-date NO-LOCK NO-ERROR. /* Malik Serverless : AND bill-date LE reslin-queasy.date2 -> reslin-queasy.date2 GE bill-date */
 
  IF AVAILABLE reslin-queasy THEN 
  DO: 
      IF reslin-queasy.char2 NE "" THEN betrag = (res-line.zipreis * INT(reslin-queasy.char2) / 100) * qty.  
      ELSE
      DO:
          /*betrag = reslin-queasy.deci1 * qty. */
          IF argt-line.vt-percnt = 0 THEN betrag = reslin-queasy.deci1 * qty. 
          ELSE IF argt-line.vt-percnt = 1 THEN betrag = reslin-queasy.deci2 * qty. 
          ELSE IF argt-line.vt-percnt = 2 THEN betrag = reslin-queasy.deci3 * qty.
      END.
      RUN get-exrate2. 
      
      RETURN. 
  END. 
END. 
/* other reservations  */
/*ITA 29/10/18 --> jika yang diisi in%*/
IF argt-line.betrag GT 0 THEN betrag = argt-line.betrag * qty. 
ELSE betrag = (res-line.zipreis * (- argt-line.betrag / 100)) * qty.


/*betrag = argt-line.betrag * qty. */
RUN get-exrate3. 
 
PROCEDURE get-exrate1: 
  IF reservation.insurance AND res-line.reserve-dec NE 0 THEN 
    ex-rate = res-line.reserve-dec. 
  ELSE IF res-line.betriebsnr NE 0 THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE IF res-line.adrflag OR NOT foreign-rate THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 
 
PROCEDURE get-exrate2: 
  IF reservation.insurance AND res-line.reserve-dec NE 0 THEN 
  DO: 
    ex-rate = res-line.reserve-dec. 
    RETURN. 
  END. 
  FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = marknr 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") THEN 
  FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = contcode 
    NO-LOCK. 
  IF queasy.KEY = 18 THEN FIND FIRST waehrung WHERE 
    waehrung.wabkurz = queasy.char3 NO-LOCK NO-ERROR. 
  ELSE
  DO:
    IF queasy.number1 NE 0 THEN FIND FIRST waehrung WHERE 
      waehrung.waehrungsnr = queasy.number1 NO-LOCK NO-ERROR. 
    ELSE IF queasy.logi1 /* local rate */ OR NOT foreign-rate THEN 
    DO: 
      FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
      FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK 
        NO-ERROR. 
    END. 
    ELSE 
    DO: 
      FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
      FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK 
        NO-ERROR. 
    END.
  END.
  IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
END. 
 
PROCEDURE get-exrate3: 
  DEFINE VARIABLE local-nr AS INTEGER. 
  DEFINE VARIABLE foreign-nr AS INTEGER. 
  IF arrangement.betriebsnr NE 0 THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
    DO: 
      ex-rate = waehrung.ankauf / waehrung.einheit. 
      RETURN. 
    END. 
  END. 
  IF foreign-rate THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 
