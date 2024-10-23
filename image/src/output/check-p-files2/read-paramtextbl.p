DEF TEMP-TABLE t-paramtext LIKE paramtext.

DEF INPUT  PARAMETER case-type AS INTEGER       NO-UNDO.
DEF INPUT  PARAMETER p-txtNo   AS INTEGER       NO-UNDO.
DEF OUTPUT PARAMETER p-text    AS CHAR INIT ""  NO-UNDO.
DEF OUTPUT PARAMETER TABLE     FOR t-paramtext.

DEF VARIABLE from-number       AS INTEGER       NO-UNDO.
DEF VARIABLE to-number         AS INTEGER       NO-UNDO.
DEF VARIABLE do-it             AS LOGICAL       NO-UNDO.

CASE case-type:
  WHEN 1 THEN 
  DO:    
    FIND FIRST paramtext WHERE paramtext.txtnr = p-txtNo NO-LOCK NO-ERROR.
    IF AVAILABLE paramtext THEN ASSIGN p-text = paramtext.ptexte.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST paramtext WHERE paramtext.txtnr = p-txtNo NO-LOCK NO-ERROR.
    IF AVAILABLE paramtext THEN
    DO:
      ASSIGN p-text = paramtext.ptexte.
      CREATE t-paramtext.
      BUFFER-COPY paramtext TO t-paramtext.
    END.
  END.
  WHEN 3 THEN
  DO:
    ASSIGN
      from-number = p-txtNo
      to-number   = p-txtNo.
    IF from-number = 9201 THEN to-number = 9299.
    FOR EACH paramtext WHERE paramtext.txtnr GE from-number 
      AND paramtext.txtnr LE to-number NO-LOCK BY paramtext.txtnr: 
      do-it = YES.
      IF from-number = 9201 THEN do-it = (paramtext.notes NE "").
      IF do-it THEN
      DO:
        CREATE t-paramtext.
        BUFFER-COPY paramtext TO t-paramtext.
      END.
    END.
  END.
  WHEN 4 THEN 
  DO:    
    FIND FIRST paramtext WHERE paramtext.txtnr = p-txtNo NO-LOCK NO-ERROR.
    IF AVAILABLE paramtext THEN ASSIGN p-text = paramtext.notes.
  END.
  WHEN 5 THEN
  DO:
      FOR EACH paramtext WHERE paramtext.txtnr = p-txtNo NO-LOCK: 
          CREATE t-paramtext.
          BUFFER-COPY paramtext TO t-paramtext.
      END.
  END.
  WHEN 6 THEN
  DO:
      FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
          AND paramtext.txtnr LE 9299 NO-LOCK: 
          CREATE t-paramtext.
          BUFFER-COPY paramtext TO t-paramtext.
      END.
  END.
  WHEN 7 THEN
  DO:
      FOR EACH paramtext WHERE paramtext.txtnr = p-txtNo 
          AND paramtext.ptexte NE "" NO-LOCK: 
          CREATE t-paramtext.
          BUFFER-COPY paramtext TO t-paramtext.
      END.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST paramtext WHERE paramtext.txtnr = 200 NO-LOCK NO-ERROR.
      IF AVAILABLE paramtext THEN
      DO:
        CREATE t-paramtext.
        BUFFER-COPY paramtext TO t-paramtext.
      END.
      FIND FIRST paramtext WHERE paramtext.txtnr = 201 NO-LOCK NO-ERROR.
      IF AVAILABLE paramtext THEN
      DO:
        CREATE t-paramtext.
        BUFFER-COPY paramtext TO t-paramtext.
      END.
      FIND FIRST paramtext WHERE paramtext.txtnr = 204 NO-LOCK NO-ERROR.
      IF AVAILABLE paramtext THEN
      DO:
        CREATE t-paramtext.
        BUFFER-COPY paramtext TO t-paramtext.
      END.
  END.
  /* SY AUG 20 2017 */
    WHEN 9 THEN
    DO:
        do-it = NO.
        FIND FIRST paramtext WHERE paramtext.txtnr = 711
            AND paramtext.number = p-txtno NO-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN
        DO:
            do-it = YES.
            CREATE t-paramtext.
            BUFFER-COPY paramtext TO t-paramtext.
        END.
        FIND FIRST paramtext WHERE paramtext.txtnr = 712
            AND paramtext.number = p-txtno NO-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN
        DO:
            CREATE t-paramtext.
            BUFFER-COPY paramtext TO t-paramtext.
        END.
        IF do-it THEN
        DO:
            FIND FIRST paramtext WHERE paramtext.txtnr = 711
                AND paramtext.number = 0 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE paramtext THEN
            DO:
                DELETE paramtext.
                RELEASE paramtext.
            END.
            FIND FIRST paramtext WHERE paramtext.txtnr = 712
                AND paramtext.number = 0 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE paramtext THEN
            DO:
                DELETE paramtext.
                RELEASE paramtext.
            END.
        END.
    END.
 
END CASE.
