/* get ratecode record if any */

DEFINE INPUT PARAMETER resnr        AS INTEGER.
DEFINE INPUT PARAMETER reslinnr     AS INTEGER.
DEFINE INPUT PARAMETER prcode       AS CHAR.
DEFINE INPUT PARAMETER rmcatNo      AS INTEGER.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE OUTPUT PARAMETER bonus       AS LOGICAL INITIAL NO.
/*
DEFINE VARIABLE resnr               AS INTEGER INITIAL 31070.
DEFINE VARIABLE reslinnr            AS INTEGER INITIAL 1.
DEFINE VARIABLE prcode              AS CHAR INITIAL "ALL1".
DEFINE VARIABLE rmcatNo             AS INTEGER INITIAL 1.
DEFINE VARIABLE datum               AS DATE INITIAL 11/09/08.
DEFINE VARIABLE bonus               AS LOGICAL INITIAL NO.
*/

DEFINE VARIABLE ct                  AS CHAR                 NO-UNDO.
DEFINE VARIABLE n                   AS INTEGER              NO-UNDO.
DEFINE VARIABLE compNo              AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE niteNo              AS INTEGER              NO-UNDO.
DEFINE VARIABLE usedCompliment      AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE paidNite            AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE niteOfStay          AS INTEGER              NO-UNDO.
DEFINE VARIABLE fdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE tdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE argtNo              AS INTEGER NO-UNDO.
DEFINE VARIABLE w-day               AS INTEGER NO-UNDO.
DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE TEMP-TABLE stay-pay
    FIELD startDate AS DATE INITIAL ?
    FIELD f-date    AS DATE                      LABEL "FromDate"
    FIELD t-date    AS DATE                      LABEL "ToDate"
    FIELD stay      AS INTEGER FORMAT "     >>>" LABEL "Stay(Nights)"
    FIELD pay       AS INTEGER FORMAT "     >>>" LABEL "Pay(Nights)"
    .

/***********************************************************************/

/* check if Bonus Night Option is using average RoomRate */
FIND FIRST htparam WHERE htparam.paramnr = 933 NO-LOCK.
IF htparam.feldtyp = 4 AND htparam.flogical THEN RETURN.

FIND FIRST res-line WHERE res-line.resnr = resnr
    AND res-line.reslinnr = reslinnr NO-LOCK.
FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement
    NO-LOCK.

ASSIGN
  niteOfStay    = res-line.abreise - res-line.ankunft
  argtNo        = arrangement.argtnr 
  w-day         = wd-array[WEEKDAY(datum - 1)]
  ct            = res-line.zimmer-wunsch
.
IF ct MATCHES("*$CODE$*") THEN
DO:
  ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
  prcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
END.

FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = w-day AND ratecode.erwachs = res-line.erwachs
  AND ratecode.kind1 = res-line.kind1 AND ratecode.kind2 = res-line.kind2
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE ratecode THEN
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = 0 AND ratecode.erwachs = res-line.erwachs
  AND ratecode.kind1 = res-line.kind1 AND ratecode.kind2 = res-line.kind2
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE ratecode THEN
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = w-day AND ratecode.erwachs = res-line.erwachs
  NO-LOCK NO-ERROR. 
    
IF NOT AVAILABLE ratecode THEN
FIND FIRST ratecode WHERE ratecode.code = prcode 
  AND ratecode.marknr = res-line.reserve-int 
  AND ratecode.argtnr = argtNo AND ratecode.zikatnr = rmcatNo
  AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
  AND ratecode.wday = 0 AND ratecode.erwachs = res-line.erwachs
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE ratecode THEN RETURN.

/* look into stay/pay night setup first */
IF datum GT res-line.ankunft AND (NUM-ENTRIES(ratecode.char1[3], ";") GE 2) THEN
DO:
  DO n = 1 TO NUM-ENTRIES(ratecode.char1[3], ";") - 1:
    ct = ENTRY(n, ratecode.char1[3], ";").
    fdatum = DATE(INTEGER(SUBSTR(ENTRY(1, ct, ","),5,2)),
                  INTEGER(SUBSTR(ENTRY(1, ct, ","),7,2)), 
                  INTEGER(SUBSTR(ENTRY(1, ct, ","),1,4))).
    tdatum = DATE(INTEGER(SUBSTR(ENTRY(2, ct, ","),5,2)),
                  INTEGER(SUBSTR(ENTRY(2, ct, ","),7,2)), 
                  INTEGER(SUBSTR(ENTRY(2, ct, ","),1,4))).
    IF datum GT fdatum AND datum LE tdatum THEN
    DO:
      CREATE stay-pay.
      ASSIGN
        stay-pay.f-date    = fdatum
        stay-pay.t-date    = tdatum
        stay-pay.stay      = INTEGER(ENTRY(3, ct, ","))
        stay-pay.pay       = INTEGER(ENTRY(4, ct, ","))
      .
      IF res-line.ankunft LT fdatum THEN ASSIGN stay-pay.startDate = fdatum.
      ELSE stay-pay.startDate = res-line.ankunft.
      IF stay-pay.stay = stay-pay.pay THEN DELETE stay-pay.
    END.
  END.
END.
FIND FIRST stay-pay NO-ERROR.
IF NOT AVAILABLE stay-pay THEN RETURN.

FOR EACH stay-pay BY stay-pay.stay:
    ASSIGN
        niteNo       = datum - stay-pay.startDate + 1
        stay-pay.pay = stay-pay.pay + usedCompliment
        compNo       = stay-pay.stay - stay-pay.pay
    .
    IF stay-pay.stay LT niteNo THEN usedCompliment = usedCompliment + compNo.
    ELSE IF (niteOfStay GE stay-pay.stay) AND (niteNo GT stay-pay.pay) THEN
    DO:
        bonus = YES.
        LEAVE.
    END.
END.
