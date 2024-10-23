DEF TEMP-TABLE t-argt-line LIKE argt-line.

DEFINE INPUT PARAMETER case-type    AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER argtNo       AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER artNo        AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER dept         AS INTEGER  NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR t-argt-line.



CASE case-type :
    WHEN 1 THEN
    DO: 
        IF artNo = ? THEN
        DO:
          FOR EACH argt-line WHERE argt-line.argtnr = argtNo NO-LOCK:
            CREATE t-argt-line.
            BUFFER-COPY argt-line TO t-argt-line.
          END.
          RETURN.
        END.

        FIND FIRST argt-line WHERE argt-line.argtnr = argtNo 
            AND argt-line.argt-artnr = artNo 
            AND argt-line.departement = dept NO-LOCK NO-ERROR.
        IF AVAILABLE argt-line THEN
        DO:
          CREATE t-argt-line.
          BUFFER-COPY argt-line TO t-argt-line.
        END.                 
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST argt-line WHERE argt-line.argtnr = argtNo
            AND argt-line.betrag NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE argt-line THEN
        DO:
            CREATE t-argt-line.
            BUFFER-COPY argt-line TO t-argt-line.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST argt-line WHERE RECID(argt-line) EQ argtNo NO-LOCK NO-ERROR.
        IF AVAILABLE argt-line THEN
        DO:
            CREATE t-argt-line.
            BUFFER-COPY argt-line TO t-argt-line.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH argt-line WHERE argt-line.argtnr = argtNo
            AND NOT argt-line.kind2 NO-LOCK :
            CREATE t-argt-line.
            BUFFER-COPY argt-line TO t-argt-line.
        END.
    END.    

END CASE.

