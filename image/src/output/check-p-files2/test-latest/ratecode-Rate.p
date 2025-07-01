/* calculate room rate based on the new conract rate setup for a certain date */

DEFINE INPUT PARAMETER ebdisc-flag  AS LOGICAL.
DEFINE INPUT PARAMETER kbdisc-flag  AS LOGICAL.
DEFINE INPUT PARAMETER resnr        AS INTEGER.
DEFINE INPUT PARAMETER reslinnr     AS INTEGER.
DEFINE INPUT PARAMETER prcode       AS CHAR.
DEFINE INPUT PARAMETER crdate       AS DATE.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE INPUT PARAMETER ankunft      AS DATE.
DEFINE INPUT PARAMETER abreise      AS DATE.
DEFINE INPUT PARAMETER marknr       AS INTEGER.
DEFINE INPUT PARAMETER argtNo       AS INTEGER.
DEFINE INPUT PARAMETER rmcatNo      AS INTEGER.
DEFINE INPUT PARAMETER adult        AS INTEGER.
DEFINE INPUT PARAMETER child1       AS INTEGER.
DEFINE INPUT PARAMETER child2       AS INTEGER.
DEFINE INPUT PARAMETER res-exrate   AS DECIMAL.
DEFINE INPUT PARAMETER wahrNo       AS INTEGER.
DEFINE OUTPUT PARAMETER rate-found  AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER rmRate      AS DECIMAL INITIAL 0.
DEFINE OUTPUT PARAMETER early-flag  AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER kback-flag  AS LOGICAL INITIAL NO.

/*
DEFINE VARIABLE ebdisc-flag  AS LOGICAL INITIAL NO.
DEFINE VARIABLE kbdisc-flag  AS LOGICAL INITIAL YES.
DEFINE VARIABLE resnr        AS INTEGER INITIAL 2208.
DEFINE VARIABLE reslinnr     AS INTEGER INITIAL 1.
DEFINE VARIABLE prcode       AS CHAR INITIAL "ALL2".
DEFINE VARIABLE datum        AS DATE INITIAL 12/27/2007.
DEFINE VARIABLE crdate              AS DATE INITIAL ?.
DEFINE VARIABLE ankunft             AS DATE INITIAL 12/27/07.
DEFINE VARIABLE abreise             AS DATE INITIAL 12/28/07.
DEFINE VARIABLE argtno              AS INTEGER INITIAL 8.
DEFINE VARIABLE rmcatNo             as INTEGER initial 1.
DEFINE VARIABLE marknr              AS INTEGER initial 4.
DEFINE VARIABLE adult               AS INTEGER initial 1.
DEFINE VARIABLE child1              AS INTEGER.
DEFINE VARIABLE child2              AS INTEGER.
DEFINE VARIABLE res-exrate          AS DECIMAL.
DEFINE VARIABLE wahrNo              AS INTEGER.
DEFINE VARIABLE rate-found   AS LOGICAL INITIAL NO.
DEFINE VARIABLE rmRate       AS DECIMAL INITIAL 0.
DEFINE VARIABLE early-flag   AS LOGICAL INITIAL NO.
DEFINE VARIABLE kback-flag   AS LOGICAL INITIAL NO.
*/

DEFINE VARIABLE occ-type            AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE restricted-disc     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE exrate1             AS DECIMAL INITIAL 1    NO-UNDO.
DEFINE VARIABLE ex2                 AS DECIMAL INITIAL 1    NO-UNDO.
DEFINE VARIABLE do-it               AS LOGICAL              NO-UNDO.
DEFINE VARIABLE add-it              AS LOGICAL              NO-UNDO.
DEFINE VARIABLE EBdisc-found        AS LOGICAL              NO-UNDO.
DEFINE VARIABLE KBdisc-found        AS LOGICAL              NO-UNDO.
DEFINE VARIABLE argt-defined        AS LOGICAL              NO-UNDO.
DEFINE VARIABLE qty                 AS INTEGER              NO-UNDO.
DEFINE VARIABLE compNo              AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE niteNo              AS INTEGER              NO-UNDO.
DEFINE VARIABLE book-date           AS DATE                 NO-UNDO.
DEFINE VARIABLE ci-date             AS DATE                 NO-UNDO.
DEFINE VARIABLE fdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE tdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE ct                  AS CHAR                 NO-UNDO.
DEFINE VARIABLE orig-prcode         AS CHAR                 NO-UNDO.
DEFINE VARIABLE RmOcc               AS DECIMAL INITIAL -1   NO-UNDO.

DEFINE VARIABLE avrgRate-Option     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE stay-nites          AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE bonus-nites         AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE bonus               AS LOGICAL              NO-UNDO.

DEFINE VARIABLE n                   AS INTEGER              NO-UNDO.
DEFINE VARIABLE w-day               AS INTEGER              NO-UNDO.
DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

/******************* TEMP TABLE **************************************/

DEFINE TEMP-TABLE early-discount
    FIELD disc-rate AS DECIMAL FORMAT " >>"   LABEL "Disc%"
    FIELD min-days  AS INTEGER FORMAT ">>>"   LABEL "Min to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ"
    FIELD from-date AS DATE    INITIAL ?
    FIELD to-date   AS DATE    INITIAL ?
    FIELD flag      AS LOGICAL INITIAL NO
    .

DEFINE TEMP-TABLE kickback-discount
    FIELD disc-rate AS DECIMAL FORMAT " >>"   LABEL "Disc%"
    FIELD max-days  AS INTEGER FORMAT ">>>"   LABEL "Max to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ"
    FIELD flag      AS LOGICAL INITIAL NO
    .

DEFINE TEMP-TABLE stay-pay
    FIELD f-date    AS DATE                      LABEL "FromDate"
    FIELD t-date    AS DATE                      LABEL "ToDate"
    FIELD stay      AS INTEGER FORMAT "     >>>" LABEL "Stay(Nights)"
    FIELD pay       AS INTEGER FORMAT "     >>>" LABEL "Pay(Nights)"
    .

DEF BUFFER kbuff FOR kickback-discount.
DEF BUFFER ebuff FOR early-discount.

/***********************************************************************/

FIND FIRST htparam WHERE htparam.paramnr = 933 NO-LOCK.
IF htparam.feldtyp = 4 THEN avrgRate-option = htparam.flogical.

RELEASE res-line.
IF resnr GT 0 THEN
FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr
    NO-LOCK NO-ERROR.

ASSIGN orig-prcode = prcode.
IF SUBSTR(prcode,1,1) = "!" THEN prcode = SUBSTR(prcode,2).
IF AVAILABLE res-line THEN 
DO:    
  rmRate = res-line.zipreis.
  IF SUBSTR(orig-prcode,1,1) NE "!" THEN
  DO:
    ct = res-line.zimmer-wunsch.
    IF ct MATCHES("*$CODE$*") THEN
    DO:
      ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
      prcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
    END.
  END.
END.

FIND FIRST htparam WHERE htparam.paramnr = 549 NO-LOCK.
occ-type = htparam.finteger. /* 0:avrg 1:as-is 2:min 3:max */

IF crdate = ? AND AVAILABLE res-line THEN
DO:
  n = 0.
  IF res-line.zimmer-wunsch MATCHES ("*DATE,*") THEN
  n = INDEX(res-line.zimmer-wunsch,"Date,").
  IF n > 0 THEN
  DO:
    ct = SUBSTR(res-line.zimmer-wunsch, n + 5, 8).
    crdate = DATE(INTEGER(SUBSTR(ct,5,2)), INTEGER(SUBSTR(ct,7,2)),
      INTEGER(SUBSTR(ct,1,4))).
  END.
  ELSE DO:
    FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK.
    crdate = reservation.resdat.
  END.
END.

/* check if rate is fixed for the whole stay */
FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
  = marknr NO-LOCK NO-ERROR. 
IF AVAILABLE queasy AND queasy.logi3 THEN datum = ankunft. 

w-day = wd-array[WEEKDAY(datum)]. 

IF argtNo NE 0 THEN
DO:
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.argtnr = argtNo
    AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = w-day AND ratecode.erwachs = adult
    AND ratecode.kind1 = child1 AND ratecode.kind2 = child2
    NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE ratecode THEN
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.argtnr = argtNo
    AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = 0 AND ratecode.erwachs = adult
    AND ratecode.kind1 = child1 AND ratecode.kind2 = child2
    NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE ratecode THEN
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.argtnr = argtNo
    AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = w-day AND ratecode.erwachs = adult
    NO-LOCK NO-ERROR. 
    
  IF NOT AVAILABLE ratecode THEN
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.argtnr = argtNo
    AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = 0 AND ratecode.erwachs = adult
    NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE ratecode THEN RETURN.
  rate-found = YES.
END.
ELSE
DO:
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = w-day AND ratecode.erwachs = adult
    AND ratecode.kind1 = child1 AND ratecode.kind2 = child2
    NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE ratecode THEN
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = 0 AND ratecode.erwachs = adult
    AND ratecode.kind1 = child1 AND ratecode.kind2 = child2
    NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE ratecode THEN
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = w-day AND ratecode.erwachs = adult
    NO-LOCK NO-ERROR. 
    
  IF NOT AVAILABLE ratecode THEN
  FIND FIRST ratecode WHERE ratecode.code = prcode 
    AND ratecode.marknr = marknr AND ratecode.zikatnr = rmcatNo
    AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
    AND ratecode.wday = 0 AND ratecode.erwachs = adult
    NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE ratecode THEN RETURN.
  rate-found = YES.
END.

/* look into stay/pay night setup first */
IF /*datum GT ankunft AND*/ (NUM-ENTRIES(ratecode.char1[3], ";") GE 2) THEN
DO:
  IF NOT avrgRate-option AND AVAILABLE res-line THEN /* means bonus night Option with Rate = 0 */
  DO:
    RUN ratecode-compli.p(resnr, reslinnr, prcode, rmcatNo, datum, OUTPUT bonus).
    IF bonus THEN
    DO:
      rmRate = 0.
      RETURN.
    END.
  END.
END.

rmRate = ratecode.zipreis + child1 * ratecode.ch1preis + child2 * ratecode.ch2preis. /* Malik Serverless 143 : ch2preis -> ratecode.ch2preis */
/* SY 05-08-2015 ratecode for compliment guest */
IF rmRate LE 0.1 THEN rmRate = 0.

/** additional charges IF argt-line price NOT included IN basic room rate **/ 
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.
book-date = crdate.
/*
IF AVAILABLE res-line AND res-line.reserve-char NE "" THEN 
  book-date = DATE(INTEGER(SUBSTR(res-line.reserve-char,3,2)),
                   INTEGER(SUBSTR(res-line.reserve-char,7,2)),
                   INTEGER(SUBSTR(res-line.reserve-char,1,2)) + 2000) NO-ERROR.
*/

FIND FIRST arrangement WHERE arrangement.argtnr = argtNo NO-LOCK NO-ERROR.

FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr NO-LOCK 
   NO-ERROR. 
IF AVAILABLE waehrung THEN exrate1 = waehrung.ankauf / waehrung.einheit. 
IF res-exrate NE 0 THEN ex2 = ex2 / res-exrate. 
ELSE 
DO: 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = wahrNo NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN ex2 = (waehrung.ankauf / waehrung.einheit). 
END. 
        
IF AVAILABLE arrangement THEN
FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
   AND NOT argt-line.kind1 AND NOT argt-line.kind2: 
   add-it = NO. 
   IF argt-line.vt-percnt = 0 THEN 
   DO: 
     IF argt-line.betriebsnr = 0 THEN qty = adult. 
     ELSE qty = argt-line.betriebsnr. 
  END. 
  ELSE IF argt-line.vt-percnt = 1 THEN qty = child1. 
  ELSE IF argt-line.vt-percnt = 2 THEN qty = child2. 
 
  IF qty GT 0 THEN 
  DO: 
    IF argt-line.fakt-modus = 1 THEN add-it = YES. /* daily */
    ELSE IF argt-line.fakt-modus = 2 THEN 
    DO: 
      IF ankunft EQ /*ci-date*/ datum THEN add-it = YES. 
    END.
    ELSE IF argt-line.fakt-modus = 3 THEN 
    DO: 
      IF (ankunft + 1) EQ /*ci-date*/ datum THEN add-it = YES. 
    END. 
    ELSE IF argt-line.fakt-modus = 4 AND DAY(datum) = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 5 AND DAY(datum + 1) = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 6 THEN 
    DO: 
      IF (ankunft + (argt-line.intervall - 1)) GE /*ci-date*/ datum THEN add-it = YES.  
    END.
  
    IF add-it THEN 
    DO: 
      argt-defined = NO. 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
        AND reslin-queasy.char1 = "" AND reslin-queasy.char1 = "" 
        AND reslin-queasy.number1 = argt-line.departement 
        AND reslin-queasy.number2 = argt-line.argtnr 
        AND reslin-queasy.resnr = resnr AND reslin-queasy.reslinnr = reslinnr 
        AND reslin-queasy.number3 = argt-line.argt-artnr 
        AND reslin-queasy.date1 LE datum
        AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        argt-defined = YES. 
        IF argt-line.vt-percnt = 0 THEN 
          rmRate = rmRate + reslin-queasy.deci1 * qty. 
        ELSE IF argt-line.vt-percnt = 1 THEN 
          rmRate = rmRate + reslin-queasy.deci2 * qty. 
        ELSE IF argt-line.vt-percnt = 2 THEN 
          rmRate = rmRate + reslin-queasy.deci3 * qty. 
      END. 
            
      IF NOT argt-defined THEN 
      DO: 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
          AND reslin-queasy.char1 = prcode AND reslin-queasy.number1 = marknr 
          AND reslin-queasy.number2 = argtnO AND reslin-queasy.reslinnr = rmcatNo 
          AND reslin-queasy.number3 = argt-line.argt-artnr 
          AND reslin-queasy.resnr = argt-line.departement 
          AND reslin-queasy.date1 LE datum
          AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO: 
          IF argt-line.vt-percnt = 0 THEN 
            rmRate = rmRate + reslin-queasy.deci1 * qty. 
          ELSE IF argt-line.vt-percnt = 1 THEN 
            rmRate = rmRate + reslin-queasy.deci2 * qty. 
          ELSE IF argt-line.vt-percnt = 2 THEN 
            rmRate = rmRate + reslin-queasy.deci3 * qty. 
        END. 
        ELSE 
        DO:    
            rmRate = rmRate + (argt-line.betrag * qty) * exrate1 / ex2. 
        END.
      END. /* not argt-defined   */ 
    END.   /* if do it           */
  END.     /* if qty NE 0        */
END.       /* for each argt-line */


KBdisc-found = NO.
IF NUM-ENTRIES(ratecode.char1[2], ";") GE 2 /* AND (ci-date LE ankunft) */
  AND kbdisc-flag THEN
DO:
  DO n = 1 TO NUM-ENTRIES(ratecode.char1[2], ";") - 1:
    ct = ENTRY(n, ratecode.char1[2], ";").
    CREATE kbuff.
    ASSIGN
      kbuff.disc-rate = INTEGER(ENTRY(1, ct, ",")) / 100
      kbuff.max-days  = INTEGER(ENTRY(2, ct, ","))
      kbuff.min-stay  = INTEGER(ENTRY(3, ct, ","))
      kbuff.max-occ   = INTEGER(ENTRY(4, ct, ","))
    .
  END.
  FOR EACH kbuff BY kbuff.max-occ:
    add-it = YES.
    IF kbuff.max-days > 0 THEN add-it = (ankunft - crdate) LE kbuff.max-days.
    IF add-it AND kbuff.min-stay > 0 THEN
      add-it = (abreise - ankunft) GE kbuff.min-stay.
    IF add-it AND kbuff.max-occ > 0  THEN
    DO:
      RUN calc-occupancy.
      add-it = RmOcc LE kbuff.max-occ.
    END.
    IF add-it THEN
    DO:
      KBdisc-found = YES.
      ASSIGN kbuff.flag = YES.
      IF NOT restricted-disc THEN restricted-disc = (kbuff.max-days > 0) 
        OR (kbuff.min-stay > 0) OR (kbuff.max-occ > 0).
      LEAVE.
    END.
  END.
END.

eBdisc-found = NO.
IF NUM-ENTRIES(ratecode.char1[1], ";") GE 2 /* AND (ci-date LE ankunft) */
  AND ebdisc-flag THEN
DO:
  DO n = 1 TO NUM-ENTRIES(ratecode.char1[1], ";") - 1:
    ct = ENTRY(n, ratecode.char1[1], ";").
    CREATE ebuff.
    ASSIGN
      ebuff.disc-rate = INTEGER(ENTRY(1, ct, ",")) / 100
      ebuff.min-days  = INTEGER(ENTRY(2, ct, ","))
      ebuff.min-stay  = INTEGER(ENTRY(3, ct, ","))
      ebuff.max-occ   = INTEGER(ENTRY(4, ct, ","))
    .
    IF NUM-ENTRIES(ct, ",") GE 5 AND TRIM(ENTRY(5,ct,",")) NE "" THEN
    ebuff.from-date = DATE(INTEGER(SUBSTR(ENTRY(5, ct, ","),5,2)),
                           INTEGER(SUBSTR(ENTRY(5, ct, ","),7,2)),
                           INTEGER(SUBSTR(ENTRY(5, ct, ","),1,4))).
    IF NUM-ENTRIES(ct, ",") GE 6 AND TRIM(ENTRY(6,ct,",")) NE "" THEN
    ebuff.to-date   = DATE(INTEGER(SUBSTR(ENTRY(6, ct, ","),5,2)),
                           INTEGER(SUBSTR(ENTRY(6, ct, ","),7,2)),
                           INTEGER(SUBSTR(ENTRY(6, ct, ","),1,4))).

  END.
  FOR EACH ebuff BY ebuff.from-date BY ebuff.to-date BY ebuff.max-occ:
    add-it = YES.
    IF ebuff.from-date NE ? THEN add-it = book-date GE ebuff.from-date
      AND book-date LE ebuff.to-date.
    IF add-it AND ebuff.min-days > 0 THEN 
      add-it = (ankunft - crdate) GE ebuff.min-days.
    IF add-it AND ebuff.min-stay > 0 THEN
      add-it = (abreise - ankunft) GE ebuff.min-stay.
    IF add-it AND ebuff.max-occ > 0 THEN
    DO:
      RUN calc-occupancy.
      add-it = RmOcc LE ebuff.max-occ.
    END.
    IF add-it THEN
    DO:
      eBdisc-found = YES.
      ASSIGN ebuff.flag = YES.
      IF NOT restricted-disc THEN restricted-disc = (ebuff.min-days > 0) 
        /* OR (ebuff.min-stay > 0) */ OR (ebuff.max-occ > 0).
      LEAVE.
    END.
  END.
END.

IF KBdisc-found THEN 
DO:    
  FIND FIRST kbuff WHERE kbuff.flag = YES.
  RmRate = RmRate * (1 - kbuff.disc-rate / 100).
  kback-flag = YES.
END.
IF EBdisc-found THEN 
DO:
  FIND FIRST ebuff WHERE ebuff.flag = YES.
  RmRate = RmRate * (1 - ebuff.disc-rate / 100).
  early-flag = YES.
END.

early-flag = restricted-disc.
IF KBdisc-found OR EBdisc-found THEN DO:
    IF RmRate GE 10000 THEN RmRate = ROUND(RmRate + 0.49, 0).
    ELSE RmRate = ROUND(RmRate + 0.0049, 2).
END.

IF NOT avrgRate-option THEN RETURN.
FIND FIRST stay-pay NO-ERROR.
IF NOT AVAILABLE stay-pay THEN RETURN.
ASSIGN stay-nites = abreise - ankunft.
FOR EACH stay-pay WHERE stay-nites GE stay-pay.stay BY stay-pay.stay DESCENDING:
  bonus-nites = stay-pay.stay - stay-pay.pay.
  ASSIGN rmRate = rmRate * (stay-nites - bonus-nites) / stay-nites.
  RETURN.
END.

PROCEDURE calc-occupancy:
DEF VAR zim100      AS INTEGER INITIAL 0.
DEF VAR curr-date   AS DATE.
DEF VAR from-date   AS DATE.
DEF VAR to-date     AS DATE.
DEF VAR TotOcc      AS DECIMAL INITIAL 0.
DEF VAR MinOcc      AS DECIMAL INITIAL 1000.
DEF VAR MaxOcc      AS DECIMAL INITIAL 0.

  IF RmOcc GE 0 THEN RETURN.
  IF ankunft = abreise THEN
  DO:
    RmOcc = 100.
    RETURN.
  END.
  IF occ-type = 1 THEN /* As is */ 
  DO:
    from-date = datum.
    to-date = datum.
  END.
  ELSE DO:
    from-date = ankunft.
    to-date = abreise - 1.
  END.
  FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
    zim100 = zim100 + 1.
  END.

  DO curr-date = from-date TO to-date:
    RmOcc = 0.
    FOR EACH res-line WHERE res-line.active-flag LE 1 
      AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
      AND res-line.resstatus NE 4 AND NOT (res-line.ankunft GT curr-date) 
      AND NOT (res-line.abreise LE curr-date) AND res-line.gastnr GT 0 
      AND res-line.kontignr GE 0 NO-LOCK:
      IF res-line.resnr NE resnr OR res-line.reslinnr NE reslinnr THEN
      DO:
        IF res-line.zinr NE "" THEN 
        DO: 
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK.
          IF zimmer.sleeping THEN RmOcc = RmOcc + res-line.zimmeranz.
        END.
        ELSE RmOcc = RmOcc + res-line.zimmeranz.
      END.
    END.
    FOR EACH kontline WHERE kontline.betriebsnr = 1
      AND kontline.ankunft LE curr-date AND kontline.abreise GE curr-date 
      AND kontline.kontstat = 1 NO-LOCK:
      RmOcc = RmOcc + kontline.zimmeranz.
    END.
    IF MinOcc GT RmOcc THEN MinOcc = RmOcc.
    IF MaxOcc LT RmOcc THEN MaxOcc = RmOcc.
    TotOcc = TotOcc + RmOcc.
  END.
  IF occ-type = 0 THEN RmOcc = TotOcc / (1 + to-date - from-date) / zim100 * 100.
  ELSE IF occ-type = 1 THEN RmOcc = RmOcc / zim100 * 100. /* as is */
  ELSE IF occ-type = 2 THEN RmOcc = MinOcc / zim100 * 100.
  ELSE IF occ-type = 3 THEN RmOcc = MaxOcc / zim100 * 100.
END.
