DEFINE TEMP-TABLE s-list
  FIELD argtnr      LIKE arrangement.argtnr
  FIELD arrangement LIKE arrangement.arrangement
  FIELD argt-bez    LIKE arrangement.argt-bez
  FIELD reihenfolge AS INTEGER INITIAL 0 
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD marknr      AS INTEGER FORMAT ">>>9" LABEL "No" 
  FIELD market      AS CHAR FORMAT "x(24)" 
.

DEFINE INPUT  PARAMETER new-contrate     AS LOGICAL NO-UNDO.
DEFINE INPUT  PARAMETER prcode           AS CHAR.
DEFINE INPUT  PARAMETER ankunft          AS DATE.
DEFINE INPUT  PARAMETER abreise          AS DATE.
DEFINE INPUT  PARAMETER curr-marknr      AS INTEGER.
DEFINE INPUT  PARAMETER pax              AS INTEGER.
DEFINE INPUT  PARAMETER nightstay        AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.


IF new-contrate THEN RUN new-create-list. 
ELSE RUN create-list.

PROCEDURE create-list: 
  FOR EACH pricecod WHERE pricecod.code = prcode NO-LOCK: 
 
    FIND FIRST arrangement WHERE arrangement.argtnr = pricecod.argtnr NO-LOCK 
        NO-ERROR. 
    IF AVAILABLE arrangement AND NOT arrangement.weeksplit THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.marknr EQ pricecod.marknr 
        AND s-list.argtnr EQ arrangement.argtnr NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        create s-list. 
        BUFFER-COPY arrangement TO s-list.
        ASSIGN 
          s-list.marknr  = pricecod.marknr 
          s-list.flag    = 2 
        . 
        FIND FIRST prmarket WHERE prmarket.nr = pricecod.marknr NO-LOCK 
          NO-ERROR. 
        IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
      END. 
      IF s-list.flag GE 1 AND zikatnr = pricecod.zikatnr 
        AND ankunft GE pricecod.startperiode 
        AND ankunft LE pricecod.endperiode THEN s-list.flag = s-list.flag - 1. 
      IF s-list.flag GE 1 AND zikatnr = pricecod.zikatnr 
        AND abreise GE pricecod.startperiode 
        AND abreise LE pricecod.endperiode THEN s-list.flag = s-list.flag - 1. 
    END. 
  END. 
  FOR EACH arrangement WHERE arrangement.segmentcode = 0 NO-LOCK:
    FIND FIRST s-list WHERE s-list.argtnr = arrangement.argtnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list AND NOT arrangement.weeksplit THEN 
    DO: 
      create s-list. 
      BUFFER-COPY arrangement TO s-list.
      s-list.flag    = 2. 
    END. 
  END. 
 
  IF curr-marknr NE 0 THEN 
  FOR EACH s-list WHERE s-list.marknr = curr-marknr: 
    s-list.reihenfolge = curr-marknr. 
  END. 
END. 
PROCEDURE new-create-list: 
  
  FOR EACH ratecode WHERE ratecode.code = prCode NO-LOCK:
    FIND FIRST arrangement WHERE arrangement.argtnr = ratecode.argtnr NO-ERROR.
    IF AVAILABLE arrangement AND NOT arrangement.weeksplit THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.marknr EQ ratecode.marknr 
        AND s-list.argtnr EQ arrangement.argtnr NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        CREATE s-list. 
        BUFFER-COPY arrangement TO s-list.
        ASSIGN 
          s-list.marknr  = ratecode.marknr 
          s-list.flag    = 2 
        . 
        
        FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-ERROR.
        IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
      END. 
      IF s-list.flag GE 1 AND zikatnr = ratecode.zikatnr 
        AND ankunft GE ratecode.startperiode 
        AND ankunft LE ratecode.endperiode THEN s-list.flag = s-list.flag - 1. 
      IF s-list.flag GE 1 AND zikatnr = ratecode.zikatnr 
        AND abreise GE ratecode.startperiode 
        AND abreise LE ratecode.endperiode THEN s-list.flag = s-list.flag - 1. 
    END. 
  END. 

  IF pax = 0 AND nightstay = 0 THEN
  FOR EACH arrangement WHERE arrangement.segmentcode = 0
    AND NOT arrangement.weeksplit NO-LOCK,
    FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr NO-LOCK
    BY arrangement.argtnr:
    FIND FIRST s-list WHERE s-list.argtnr = arrangement.argtnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list AND NOT arrangement.weeksplit THEN 
    DO: 
      CREATE s-list. 
      BUFFER-COPY arrangement TO s-list.
      ASSIGN
        s-list.flag    = 2
      . 
    END. 
  END.
  ELSE
  FOR EACH arrangement WHERE arrangement.segmentcode = 0
    AND (arrangement.waeschewechsel = pax OR arrangement.waeschewechsel = 0)
    AND (arrangement.handtuch = nightstay OR arrangement.handtuch = 0)
    AND NOT arrangement.weeksplit NO-LOCK,
    FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr NO-LOCK
    BY arrangement.argtnr:
    FIND FIRST s-list WHERE s-list.argtnr = arrangement.argtnr 
    NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list AND NOT arrangement.weeksplit THEN 
    DO: 
      CREATE s-list. 
      BUFFER-COPY arrangement TO s-list.
      ASSIGN
        s-list.flag    = 2
      . 
    END. 
  END.
 
  IF curr-marknr NE 0 THEN 
  FOR EACH s-list WHERE s-list.marknr = curr-marknr: 
    s-list.reihenfolge = curr-marknr. 
  END. 
END.
