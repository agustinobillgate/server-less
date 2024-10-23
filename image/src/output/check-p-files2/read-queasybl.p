
DEF TEMP-TABLE t-queasy    LIKE queasy.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER intkey     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER inpInt1    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER inpChar1   AS CHAR     NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-queasy.

/*Eko 18 Juli 2016*/
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE sumUser     AS INTEGER.
DEFINE VARIABLE sumAppr     AS INTEGER.
DEFINE VARIABLE p-786       AS CHARACTER.
            
CASE case-type:
  WHEN 1 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = intKey 
      AND queasy.number1 = inpInt1 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
    END.
  END.
  WHEN 2 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = intKey AND queasy.char1 = inpChar1 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
    END.
  END.
  WHEN 3 THEN
  FOR EACH queasy WHERE queasy.KEY = intKey NO-LOCK BY queasy.char1:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
  END.
  WHEN 4 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = intKey 
      AND queasy.char1 = inpChar1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    FIND FIRST queasy WHERE queasy.KEY = intKey 
      AND SUBSTR(queasy.char1, 1, LENGTH(inpChar1)) = inpChar1 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
    END.
  END.
  WHEN 5 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = intKey NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
    END.
  END.
  WHEN 6 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = intKey 
      AND queasy.char3 NE "" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
    END.
  END.
  WHEN 7 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = intKey 
      AND queasy.number1 EQ inpInt1 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
    END.
  END.
  WHEN 8 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = intKey 
      AND queasy.number1 EQ inpInt1 AND queasy.char1 = inpChar1 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
    END.
  END.
  WHEN 9 THEN
  DO:
      FIND FIRST queasy WHERE queasy.KEY = 18 
          AND queasy.number1 = intKey 
          AND queasy.char3 NE "" NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
          CREATE t-queasy.
          BUFFER-COPY queasy TO t-queasy.
      END.
  END.
  WHEN 10 THEN
  DO:
      FOR EACH queasy WHERE queasy.KEY = intKey 
          AND queasy.number3 = inpInt1 NO-LOCK:
          CREATE t-queasy.
          BUFFER-COPY queasy TO t-queasy.
      END.
  END.
  WHEN 11 THEN
  DO:
      FIND FIRST queasy WHERE RECID(queasy) = intKey NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
          CREATE t-queasy.
          BUFFER-COPY queasy TO t-queasy.
      END.
  END.
  WHEN 12 THEN
  DO:
      FIND FIRST queasy WHERE queasy.number1 = inpInt1
          AND queasy.number2 = 0 AND queasy.deci2 = 0
          AND queasy.key = intkey NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
          CREATE t-queasy.
          BUFFER-COPY queasy TO t-queasy.
      END.
  END.
  WHEN 13 THEN
  DO:
      FIND FIRST queasy WHERE queasy.KEY = intKey
          AND queasy.number1 NE inpInt1 
          AND queasy.char3 = inpChar1 NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
          CREATE t-queasy.
          BUFFER-COPY queasy TO t-queasy.
      END.
  END.
  WHEN 14 THEN
  DO:
      FIND FIRST queasy WHERE queasy.KEY = 25
          AND queasy.number1 = intKey
          AND queasy.number2 = inpInt1 
          AND queasy.char3 = inpChar1 NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
          CREATE t-queasy.
          BUFFER-COPY queasy TO t-queasy.
      END.
  END.
  WHEN 15 THEN /* for MICROS - FO PMS */
  DO:
      FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
      IF inpInt1 = 0 THEN
      FIND FIRST queasy WHERE queasy.KEY       = 37
          AND queasy.betriebsnr                = intKey
          AND queasy.date1                     = htparam.fdate
          AND queasy.logi1                     = TRUE
          AND queasy.char1                     = "micros"
          NO-LOCK NO-ERROR.
      ELSE
      FIND FIRST queasy WHERE queasy.KEY       = 37
          AND queasy.betriebsnr                = intKey
          AND queasy.date1                     = htparam.fdate
          AND queasy.logi1                     = TRUE
          AND queasy.char1                     = "micros"
          AND queasy.number1                   = inpInt1
          NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
        CREATE t-queasy.
        BUFFER-COPY queasy TO t-queasy.
        /*FIND CURRENT queasy SHARE-LOCK.
        MESSAGE "bb" VIEW-AS ALERT-BOX INFO.
        DELETE queasy.*/
        RELEASE queasy.
      END.
  END.
    WHEN 16 THEN /* for MICROS - FO PMS */
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
        FOR EACH queasy WHERE queasy.KEY       = 37
            AND queasy.betriebsnr                = intKey
            AND queasy.date1                     = htparam.fdate
            AND queasy.logi1                     = TRUE
            AND queasy.char1                     = "micros"
            AND queasy.number1                   GT inpInt1
            NO-LOCK:
              CREATE t-queasy.
              BUFFER-COPY queasy TO t-queasy.
              /*FIND CURRENT queasy SHARE-LOCK.
              DELETE queasy.*/
              RELEASE queasy.
        END.
    END.
END CASE.

