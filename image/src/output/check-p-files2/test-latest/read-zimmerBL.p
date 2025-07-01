DEF TEMP-TABLE t-zimmer LIKE zimmer.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER rmNo       AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER zikatNo    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER setupNo    AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.

DEF VAR counter AS INT.
DEF VAR str AS CHAR.

CASE case-type:
  WHEN 1 THEN
  DO:
    IF NUM-ENTRIES(rmNo, ";") GT 1 THEN
    DO:
      DO counter = 1 TO NUM-ENTRIES(rmNo, ";"):
        str = ENTRY(counter, rmNo, ";").
        FIND FIRST zimmer WHERE zimmer.zinr = str NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN
        DO:
          FIND FIRST t-zimmer WHERE t-zimmer.zinr = str NO-LOCK NO-ERROR.
          IF NOT AVAILABLE t-zimmer THEN
          DO:
            CREATE t-zimmer.
            BUFFER-COPY zimmer TO t-zimmer.
          END.
        END.
      END.
    END.
    ELSE
    DO:
      FIND FIRST zimmer WHERE zimmer.zinr = rmNo NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
        CREATE t-zimmer.
        BUFFER-COPY zimmer TO t-zimmer.
      END.
    END.
    
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST zimmer WHERE zimmer.zikatnr = zikatNo
      AND zimmer.setup = setupNo  NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:
      CREATE t-zimmer.
      BUFFER-COPY zimmer TO t-zimmer.
    END.
  END.
  WHEN 3 THEN
  FOR EACH zimmer WHERE zimmer.zikatnr = zikatNo NO-LOCK BY zimmer.zinr:
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
  END.
  WHEN 4 THEN
  FOR EACH zimmer WHERE zimmer.house-status NE 0 NO-LOCK BY zimmer.zinr: 
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
  END.
  WHEN 5 THEN
  DO:
      FIND LAST zimmer NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN
        DO:
          CREATE t-zimmer.
          BUFFER-COPY zimmer TO t-zimmer.
        END.
  END.
  WHEN 6 THEN
  DO:
      FIND FIRST zimmer WHERE zimmer.zikatnr = zikatNo
          AND zimmer.sleeping NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
          CREATE t-zimmer.
          BUFFER-COPY zimmer TO t-zimmer.
      END.
  END.
  WHEN 7 THEN
  DO:
      FOR EACH zimmer NO-LOCK:
          CREATE t-zimmer.
          BUFFER-COPY zimmer TO t-zimmer.
      END.
  END.
  WHEN 8 THEN
  DO:
      FOR EACH zimmer NO-LOCK WHERE zimmer.zistatus GE 2 
          AND zimmer.zistatus LE 4:
          CREATE t-zimmer.
          BUFFER-COPY zimmer TO t-zimmer.
      END.
  END.
  WHEN 9 THEN
  DO:
      FIND FIRST zimmer WHERE zimmer.typ = zikatNo NO-LOCK NO-ERROR. 
      IF AVAILABLE zimmer THEN
      DO:
        CREATE t-zimmer.
        BUFFER-COPY zimmer TO t-zimmer.
      END.
  END.
  WHEN 10 THEN
  DO:
      FIND FIRST zimmer WHERE (zimmer.setup + 9200) = setupNo NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
        CREATE t-zimmer.
        BUFFER-COPY zimmer TO t-zimmer.
      END.
  END.
  WHEN 11 THEN
  DO:
      FIND FIRST zimmer WHERE zimmer.nebenstelle NE "" NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
        CREATE t-zimmer.
        BUFFER-COPY zimmer TO t-zimmer.
      END.
  END.
END CASE.
