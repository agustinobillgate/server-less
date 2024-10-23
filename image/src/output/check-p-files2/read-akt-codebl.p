DEFINE TEMP-TABLE t-akt-code LIKE akt-code.

DEFINE INPUT PARAMETER case-type     AS INTEGER.
DEFINE INPUT PARAMETER bezeich       AS CHAR.
DEFINE INPUT PARAMETER aktionscode   AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-akt-code.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH akt-code WHERE akt-code.aktiongrup = 1 NO-LOCK:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST akt-code WHERE akt-code.aktiongrup = 1 
            AND akt-code.bezeich = bezeich NO-LOCK NO-ERROR.
        IF AVAILABLE akt-code THEN
        DO:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST akt-code WHERE akt-code.aktionscode = aktionscode 
            NO-LOCK NO-ERROR.
        IF AVAILABLE akt-code THEN
        DO:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST akt-code WHERE akt-code.aktiongrup = 1 AND 
            akt-code.aktionscode = aktionscode NO-LOCK NO-ERROR.
        IF AVAILABLE akt-code THEN
        DO:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH akt-code NO-LOCK:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST akt-code WHERE akt-code.aktiongrup = 2 
            AND akt-code.aktionscode = 1 NO-LOCK NO-ERROR.
        IF AVAILABLE akt-code THEN
        DO:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 7 THEN
    DO:
        FIND FIRST akt-code WHERE akt-code.aktiongrup = aktionscode 
            AND akt-code.bezeich = bezeich NO-LOCK NO-ERROR.
        IF AVAILABLE akt-code THEN
        DO:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 8 THEN
    DO:
        FIND FIRST akt-code WHERE akt-code.aktiongrup = 4 
            AND akt-code.aktionscode = aktionscode NO-LOCK NO-ERROR.
        IF AVAILABLE akt-code THEN
        DO:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
    WHEN 9 THEN
    DO:
        FOR EACH akt-code WHERE akt-code.aktiongrup = aktionscode NO-LOCK:
            CREATE t-akt-code.
            BUFFER-COPY akt-code TO t-akt-code.
        END.
    END.
END CASE.
