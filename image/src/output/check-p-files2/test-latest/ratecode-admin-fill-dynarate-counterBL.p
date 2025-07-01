
DEF INPUT PARAMETER r-code AS CHAR.
DEF INPUT PARAMETER dynaRate-list-rmType AS CHAR.
DEF INPUT PARAMETER dynaRate-list-rCode AS CHAR.
DEF INPUT PARAMETER dynarate-list-w-day AS INT.
DEF OUTPUT PARAMETER curr-counter AS INTEGER NO-UNDO.

RUN fill-dynarate-counter.

PROCEDURE fill-dynarate-counter:
  FIND FIRST counters WHERE counters.counter-no = 50 NO-ERROR.
  IF NOT AVAILABLE counters THEN
  DO:
    CREATE counters.
    ASSIGN
        counters.counter-no  = 50
        counters.counter-bez = "Counter for Dynamic Ratecode"
        counters.counter     = 0
    .
  END.
  counters.counter = counters.counter + 1.
  FIND CURRENT counters NO-LOCK.
  curr-counter = counters.counter.
  FIND FIRST ratecode WHERE ratecode.code = r-code.
  FIND CURRENT ratecode EXCLUSIVE-LOCK.
  ASSIGN ratecode.char1[5] = "CN" + STRING(curr-counter) + ";"
      + ratecode.char1[5].
  FIND CURRENT ratecode NO-LOCK.

/* SY 16/09/2014 */
  IF dynaRate-list-rmType = "*" THEN
  DO:
    FOR EACH queasy WHERE queasy.KEY  = 145
      AND queasy.char1                  = ratecode.code
      AND queasy.char2                  = dynaRate-list-rCode
      AND queasy.number1                = 0
      AND queasy.deci1                  = dynarate-list-w-day:
      ASSIGN queasy.deci2 = curr-counter.
    END.
  END.
  ELSE
  DO:
    FIND FIRST zimkateg WHERE zimkateg.kurzbez = dynaRate-list-rmType
      NO-LOCK.
    FOR EACH queasy WHERE queasy.KEY  = 145
      AND queasy.char1                  = ratecode.code
      AND queasy.char2                  = dynaRate-list-rCode
      AND queasy.number1                = zimkateg.zikatnr
      AND queasy.deci1                  = dynarate-list-w-day:
      ASSIGN queasy.deci2 = curr-counter.
    END.
  END.
END.
