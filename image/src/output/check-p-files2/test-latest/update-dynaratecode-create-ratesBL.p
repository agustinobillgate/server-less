DEFINE TEMP-TABLE rate-list1
    FIELD origcode  AS CHAR
    FIELD counter   AS INTEGER
    FIELD w-day     AS INTEGER FORMAT "9" COLUMN-LABEL "WD" INIT 0
    FIELD rooms     AS CHAR FORMAT "x(8)" COLUMN-LABEL "Rooms"
    FIELD rcode     AS CHAR FORMAT "x(8)" EXTENT 31 COLUMN-LABEL "Rcode"
.

DEFINE TEMP-TABLE dynaRate-list
  FIELD counter AS INTEGER
  FIELD rCode   AS CHAR    FORMAT "x(10)" LABEL "RateCode"
  FIELD w-day   AS INTEGER FORMAT "9"     INIT 0
  FIELD fr-room AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
  FIELD to-room AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
  FIELD days1   AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
  FIELD days2   AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
  FIELD rmType  AS CHAR    FORMAT "x(10)" LABEL "Room Type"
  FIELD s-recid AS INTEGER
.
           
DEF INPUT  PARAMETER TABLE FOR dynaRate-list.
DEF INPUT  PARAMETER rmtype          AS CHAR.
DEF INPUT  PARAMETER currcode        AS CHAR.
DEF INPUT  PARAMETER from-date       AS DATE.
DEF INPUT  PARAMETER to-date         AS DATE.
DEF INPUT  PARAMETER market-number   AS INT.
DEF OUTPUT PARAMETER TABLE FOR rate-list1.

DEF VAR curr-date   AS DATE     NO-UNDO.  
DEF VAR curr-i      AS INTEGER  NO-UNDO.
DEF VAR w-day       AS INTEGER  NO-UNDO.
DEF VAR inp-zikatnr AS INTEGER  NO-UNDO INIT 0.
DEF VAR wd-array    AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 


FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmtype NO-LOCK NO-ERROR.
IF AVAILABLE zimkateg THEN inp-zikatnr = zimkateg.zikatnr.

FOR EACH dynarate-list WHERE dynarate-list.rmtype = rmtype
    BY dynarate-list.w-day
    BY dynarate-list.fr-room BY dynarate-list.days1
    BY dynarate-list.days2:
    CREATE rate-list1.
    ASSIGN 
        rate-list1.counter  = dynarate-list.counter
        rate-list1.origcode = dynarate-list.rcode
        rate-list1.w-day    = dynarate-list.w-day
        rate-list1.rooms    = STRING(dynaRate-list.fr-room) 
                            + "-" + STRING(dynaRate-list.to-room)
    .
    curr-date = from-date - 1.
    DO curr-i = 1 TO DAY(to-date):
      ASSIGN 
          curr-date = curr-date + 1
          w-day = wd-array[WEEKDAY(curr-date)] 
      .
      IF dynarate-list.w-day GT 0 AND dynarate-list.w-day NE w-day 
        THEN rate-list1.rcode[curr-i] = ?.
      ELSE
      DO:
        RELEASE ratecode.
        /* SY 20/09/2014 */
        IF AVAILABLE zimkateg THEN
        FIND FIRST ratecode WHERE ratecode.CODE = dynarate-list.rCode
          AND ratecode.startperiode LE curr-date
          AND ratecode.endperiode GE curr-date
          AND ratecode.zikatnr = inp-zikatnr
          AND ratecode.marknr  = market-number NO-LOCK NO-ERROR.
        ELSE
        FIND FIRST ratecode WHERE ratecode.CODE = dynarate-list.rCode
          AND ratecode.startperiode LE curr-date
          AND ratecode.endperiode GE curr-date
          AND ratecode.marknr  = market-number NO-LOCK NO-ERROR.
        IF NOT AVAILABLE ratecode THEN rate-list1.rcode[curr-i] = ?.
        ELSE 
        DO:    
          rate-list1.rcode[curr-i] = dynarate-list.rcode.
          FIND FIRST queasy WHERE queasy.KEY  = 145
            AND queasy.char1                  = currcode
            AND queasy.char2                  = rate-list1.origcode
            AND queasy.number1                = inp-zikatnr
            AND queasy.deci1                  = dynarate-list.w-day
            AND queasy.deci2                  = dynarate-list.counter
            AND queasy.date1                  = curr-date 
            NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          ASSIGN rate-list1.rcode[curr-i] = queasy.char3.
        END.
      END.
    END.
END.
