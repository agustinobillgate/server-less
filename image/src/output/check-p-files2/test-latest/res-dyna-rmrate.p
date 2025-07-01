DEF INPUT PARAMETER resNo       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinNo    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER markNo      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER adult       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER child1      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER child2      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER wahrNo      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER argtnr      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER rmType      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER ankunft     AS DATE    NO-UNDO.
DEF INPUT PARAMETER abreise     AS DATE    NO-UNDO.
DEF INPUT PARAMETER prCode      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR    NO-UNDO.
DEF INPUT PARAMETER res-exrate  AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER ebdisc-flag AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER kbdisc-flag AS LOGICAL NO-UNDO.

DEF OUTPUT PARAMETER created    AS LOGICAL INITIAL NO NO-UNDO.
DEF OUTPUT PARAMETER zipreis    AS DECIMAL INITIAL ? NO-UNDO.

DEF VARIABLE datum              AS DATE    NO-UNDO.
DEF VARIABLE to-date            AS DATE    NO-UNDO.
DEF VARIABLE ci-date            AS DATE    NO-UNDO.
DEF VARIABLE rate-found         AS LOGICAL NO-UNDO.
DEF VARIABLE kback-flag         AS LOGICAL NO-UNDO.
DEF VARIABLE restricted-rate    AS LOGICAL NO-UNDO.
DEF VARIABLE rm-Rate            AS DECIMAL NO-UNDO.
DEF VARIABLE mapcode            AS CHAR    NO-UNDO.
DEF VAR w-day                   AS INTEGER  NO-UNDO.

DEF VARIABLE global-occ   AS LOGICAL INIT NO NO-UNDO.
DEF VARIABLE i-param439   AS INTEGER         NO-UNDO.
DEF VARIABLE arrival-date AS DATE            NO-UNDO.

DEFINE VARIABLE wd-array        AS INTEGER EXTENT 8 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE TEMP-TABLE dynaRate-list
  FIELD s-recid AS INTEGER
  FIELD counter AS INTEGER
  FIELD w-day   AS INTEGER
  FIELD rmType  AS CHAR    FORMAT "x(10)" LABEL "Room Type"
  FIELD fr-room AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
  FIELD to-room AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
  FIELD days1   AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
  FIELD days2   AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
  FIELD rCode   AS CHAR    FORMAT "x(10)" LABEL "RateCode"
.

DEFINE TEMP-TABLE r-qsy LIKE reslin-queasy.
DEFINE TEMP-TABLE n-qsy LIKE reslin-queasy.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = prCode NO-LOCK
    NO-ERROR.
IF NOT AVAILABLE queasy THEN RETURN.
IF NOT queasy.logi2 THEN RETURN.

IF ankunft = abreise THEN to-date = ankunft.
ELSE to-date = abreise - 1.
ASSIGN arrival-date = ankunft.

FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmType NO-LOCK.
RUN htpdate.p (87, OUTPUT ci-date).
RUN htpint.p(439,  OUTPUT i-param439).

FIND FIRST res-line WHERE res-line.resnr = resNo
    AND res-line.reslinnr = reslinNo NO-LOCK NO-ERROR.
IF AVAILABLE res-line AND res-line.active-flag = 1 THEN
    arrival-date = ci-date.

DO datum = ankunft TO to-date:
  RUN create-buffers(datum).
END.

RUN create-dynamic-fixrates.

PROCEDURE create-dynamic-fixrates:
/* SY 16 AUG 2015: create the rate for each single date */  
  FOR EACH r-qsy BY r-qsy.date1:
      CREATE reslin-queasy.
      BUFFER-COPY r-qsy TO reslin-queasy.
      created = YES.
  END.
END.

PROCEDURE create-buffers:
DEF INPUT PARAMETER datum AS DATE        NO-UNDO.

DEF VAR use-it      AS LOGICAL           NO-UNDO.
DEF VAR tokcounter  AS INTEGER           NO-UNDO.
DEF VAR ifTask      AS CHAR              NO-UNDO.
DEF VAR mesToken    AS CHAR              NO-UNDO.
DEF VAR mesValue    AS CHAR              NO-UNDO.
DEF VAR occ-rooms   AS INTEGER           NO-UNDO.
DEF BUFFER dybuff   FOR dynaRate-list.

  ASSIGN w-day = wd-array[WEEKDAY(datum)]. 

  FOR EACH dynaRate-list:
      DELETE dynaRate-list.
  END. 

/* SY 21/09/2014 */
  FOR EACH ratecode WHERE ratecode.code = prcode NO-LOCK: 
      CREATE dynaRate-list.
      ifTask = ratecode.char1[5].
      DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
          mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
          mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
          CASE mesToken:
              WHEN "CN" THEN dynarate-list.counter = INTEGER(mesValue).
              WHEN "RT" THEN dynaRate-list.rmType = mesValue.
              WHEN "WD" THEN dynarate-list.w-day   = INTEGER(mesValue).
              WHEN "FR" THEN dynaRate-list.fr-room = INTEGER(mesValue).
              WHEN "TR" THEN dynaRate-list.to-room = INTEGER(mesValue).
              WHEN "D1" THEN dynaRate-list.days1   = INTEGER(mesValue).
              WHEN "D2" THEN dynaRate-list.days2   = INTEGER(mesValue).
              WHEN "RC" THEN dynaRate-list.rCode   = mesValue.
          END CASE.
      END.
  END.

  FIND FIRST dynarate-list WHERE dynarate-list.rmtype EQ "*"
      NO-ERROR.
  global-occ = AVAILABLE dynarate-list AND i-param439 = 1.
  IF global-occ THEN
  FOR EACH dynarate-list WHERE dynarate-list.rmtype NE "*":
      DELETE dynarate-list.
  END.
  ELSE    
  FOR EACH dynarate-list WHERE dynarate-list.rmtype NE rmType:
      DELETE dynarate-list.
  END.

  RUN calculate-occupied-roomsbl.p(datum, rmType,
      global-occ, OUTPUT occ-rooms).

  /* in case from room starting with 1 and not zero */
  IF occ-rooms = 0 THEN
  DO:
    FIND FIRST dynaRate-list WHERE dynaRate-list.fr-room = 0 NO-ERROR.
    IF NOT AVAILABLE dynaRate-list THEN occ-rooms = 1.
  END.

  FOR EACH dynaRate-list BY dynaRate-list.w-day DESC:
    use-it = YES.
    IF dynaRate-list.days1 NE 0 AND (ankunft - ci-date) LE dynaRate-list.days1 
      THEN use-it = NO.
    IF use-it AND dynaRate-list.days2 NE 0 AND 
      (ankunft - ci-date) GE dynaRate-list.days2 THEN use-it = NO.
    IF use-it THEN use-it = (dynaRate-list.fr-room LE occ-rooms)
      AND (dynaRate-list.to-room GE occ-rooms).
    IF NOT use-it THEN DELETE dynaRate-list.
    ELSE 
    DO:    
      IF (dynaRate-list.days1 NE 0) OR (dynaRate-list.days2 NE 0) THEN
      FOR EACH dybuff WHERE dybuff.days1 = 0 AND dybuff.days2 = 0
        AND (dybuff.rmtype  EQ dynaRate-list.rmtype)
        AND (dybuff.fr-room LE occ-rooms)
        AND (dybuff.to-room GE occ-rooms):
        DELETE dybuff.
      END.
      IF dynaRate-list.w-day GT 0 THEN
      FOR EACH dybuff WHERE dybuff.w-day = 0
        AND (dybuff.rmtype  EQ dynaRate-list.rmtype)
        AND (dybuff.fr-room LE occ-rooms)
        AND (dybuff.to-room GE occ-rooms):
        DELETE dybuff.
      END.
    END.
  END.

  FIND FIRST dynaRate-list WHERE dynaRate-list.w-day = w-day
    AND dynaRate-list.days1 NE 0 NO-ERROR.
  IF NOT AVAILABLE dynaRate-list THEN
  FIND FIRST dynaRate-list WHERE dynaRate-list.w-day = w-day
    AND  dynaRate-list.days2 NE 0 NO-ERROR.
  IF NOT AVAILABLE dynaRate-list THEN
  FIND FIRST dynaRate-list WHERE dynaRate-list.w-day = w-day NO-ERROR.
  IF NOT AVAILABLE dynaRate-list THEN
  FIND FIRST dynaRate-list WHERE dynaRate-list.w-day = 0
    AND dynaRate-list.days1 NE 0 NO-ERROR.
  IF NOT AVAILABLE dynaRate-list THEN
  FIND FIRST dynaRate-list WHERE dynaRate-list.w-day = 0
    AND  dynaRate-list.days2 NE 0 NO-ERROR.
  IF NOT AVAILABLE dynaRate-list THEN
  FIND FIRST dynaRate-list WHERE dynaRate-list.w-day = 0 NO-ERROR.

  IF AVAILABLE dynaRate-list THEN
  DO:
    mapcode = dynaRate-list.rcode.
    IF global-occ THEN
    FIND FIRST queasy WHERE queasy.KEY  = 145
        AND queasy.char1                = prcode
        AND queasy.char2                = mapcode
        AND queasy.number1              = 0
        AND queasy.deci1                = dynarate-list.w-day
        AND queasy.deci2                = dynarate-list.counter
        AND queasy.date1                = datum 
        NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST queasy WHERE queasy.KEY  = 145
        AND queasy.char1                = prcode
        AND queasy.char2                = mapcode
        AND queasy.number1              = zimkateg.zikatnr
        AND queasy.deci1                = dynarate-list.w-day
        AND queasy.deci2                = dynarate-list.counter
        AND queasy.date1                = datum 
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN mapcode = queasy.char3.

    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, resNo, reslinNo, 
      ("!" + mapcode), ci-date, datum, ankunft,
      abreise, markNo, argtnr, zimkateg.zikatnr, adult, child1, 
      child2, res-exrate, wahrNo, OUTPUT rate-found, OUTPUT rm-Rate, 
      OUTPUT restricted-rate, OUTPUT kback-flag).
    CREATE r-qsy.
    ASSIGN
      r-qsy.key         = "arrangement"
      r-qsy.resnr       = resNo
      r-qsy.reslinnr    = reslinNo 
      r-qsy.date1       = datum
      r-qsy.date2       = datum 
      r-qsy.deci1       = rm-Rate 
      r-qsy.char2       = mapcode
      r-qsy.char3       = user-init
    . 
    IF datum = arrival-date THEN zipreis = rm-rate.
  END.
END.
