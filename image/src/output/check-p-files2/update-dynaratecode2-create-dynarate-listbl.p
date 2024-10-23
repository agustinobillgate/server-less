DEFINE TEMP-TABLE dynaRate-list
  FIELD counter AS INTEGER
  FIELD rCode   AS CHAR    FORMAT "x(15)" LABEL "RateCode"
  FIELD w-day   AS INTEGER INIT 0
  FIELD fr-room AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
  FIELD to-room AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
  FIELD days1   AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
  FIELD days2   AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
  FIELD s-recid AS INTEGER
  FIELD rmType  AS CHAR    FORMAT "x(10)" LABEL "Room Type"
.

DEF INPUT PARAMETER prcode AS CHAR.
DEF OUTPUT PARAMETER currency       AS CHAR.
DEF OUTPUT PARAMETER market         AS CHAR.
DEF OUTPUT PARAMETER market-number  AS INT.
DEF OUTPUT PARAMETER avail-queasy   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-prmarket AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR dynaRate-list.

DEF VAR ifTask              AS CHAR              NO-UNDO.
DEF VAR tokcounter          AS INTEGER           NO-UNDO.
DEF VAR mesToken            AS CHAR              NO-UNDO.
DEF VAR mesValue            AS CHAR              NO-UNDO.

FOR EACH ratecode WHERE ratecode.code = prcode NO-LOCK: 
    CREATE dynaRate-list.
    ASSIGN dynaRate-list.s-recid = RECID(ratecode).
    ifTask = ratecode.char1[5].
    DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
      mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
      mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
      CASE mesToken:
          WHEN "CN" THEN dynaRate-list.counter = INTEGER(mesValue).
          WHEN "RT" THEN dynaRate-list.rmType  = mesValue.
          WHEN "WD" THEN dynaRate-list.w-day   = INTEGER(mesValue).
          WHEN "FR" THEN dynaRate-list.fr-room = INTEGER(mesValue).
          WHEN "TR" THEN dynaRate-list.to-room = INTEGER(mesValue).
          WHEN "D1" THEN dynaRate-list.days1   = INTEGER(mesValue).
          WHEN "D2" THEN dynaRate-list.days2   = INTEGER(mesValue).
          WHEN "RC" THEN dynaRate-list.rCode   = mesValue.
      END CASE.
    END.
END.

FIND FIRST dynaRate-list NO-ERROR.
IF AVAILABLE dynaRate-list THEN
DO:
    FIND FIRST ratecode WHERE ratecode.CODE = dynaRate-list.rCode
      NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN
    DO:
      FIND FIRST queasy WHERE queasy.KEY = 18 
        AND queasy.number1 = ratecode.marknr NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
        avail-queasy = YES.
        currency = queasy.char3.
      END.
      FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK
        NO-ERROR.
      IF AVAILABLE prmarket THEN
      DO:
        avail-prmarket = YES.
        ASSIGN
          market        = prmarket.bezeich
          market-number = prmarket.nr
        .
      END.
    END.
END.
