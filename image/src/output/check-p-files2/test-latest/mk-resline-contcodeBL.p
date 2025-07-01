DEF TEMP-TABLE t-queasy   LIKE queasy.
DEF TEMP-TABLE t-ratecode LIKE ratecode.
DEF TEMP-TABLE t-prmarket LIKE prmarket.

DEF INPUT PARAMETER contcode     AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER currency    AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER currency-nr AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER TABLE  FOR t-queasy.
DEF OUTPUT PARAMETER TABLE  FOR t-ratecode.
DEF OUTPUT PARAMETER TABLE  FOR t-prmarket.

DEF VARIABLE ifTask     AS CHAR     NO-UNDO.
DEF VARIABLE statcode   AS CHAR     NO-UNDO INIT "".
DEF VARIABLE mesToken   AS CHAR     NO-UNDO.
DEF VARIABLE mesValue   AS CHAR     NO-UNDO.
DEF VARIABLE tokcounter AS INTEGER  NO-UNDO.
DEF VARIABLE dyna-flag  AS LOGICAL  NO-UNDO INIT NO.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = contcode 
   NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
FIND FIRST queasy WHERE queasy.KEY = 2 AND 
 SUBSTR(queasy.char1,1,LENGTH(contcode)) = contcode NO-LOCK NO-ERROR.

IF AVAILABLE queasy THEN
DO:
  FIND FIRST ratecode WHERE ratecode.CODE = contcode NO-LOCK NO-ERROR.
  IF AVAILABLE ratecode THEN
  DO:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    CREATE t-ratecode.
    BUFFER-COPY ratecode TO t-ratecode.

    IF queasy.logi2 THEN
    DO:
      ASSIGN
        dyna-flag = YES
        ifTask = ratecode.char1[5]
      .
      DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
        mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
        mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
        CASE mesToken:
          WHEN "RC" THEN statcode = mesValue.
          OTHERWISE .
        END CASE.
      END.
      IF statcode NE "" THEN FIND FIRST ratecode 
        WHERE ratecode.CODE = statcode NO-LOCK NO-ERROR.
    END.
      
    IF AVAILABLE ratecode THEN
    FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr 
        NO-LOCK NO-ERROR.
    IF AVAILABLE prmarket THEN
    DO:
      CREATE t-prmarket.
      BUFFER-COPY prmarket TO t-prmarket.
      IF dyna-flag THEN
      DO:
        FIND FIRST queasy WHERE queasy.KEY = 18
            AND queasy.number1 = prmarket.nr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN 
        DO:    
          currency = queasy.char3.
          FIND FIRST waehrung WHERE waehrung.wabkurz = currency
              NO-LOCK NO-ERROR.
          IF AVAILABLE waehrung THEN currency-nr = waehrung.waehrungsnr.
        END.
      END.
    END.
  END.

END.
