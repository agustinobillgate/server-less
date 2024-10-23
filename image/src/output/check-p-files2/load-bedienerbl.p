DEF TEMP-TABLE t-bediener LIKE bediener
    FIELD rec-id AS INT.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER int1        AS INT.
DEF INPUT PARAMETER int2        AS INT.
DEF INPUT PARAMETER char1       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH bediener WHERE bediener.flag = int1
            AND username GE char1 NO-LOCK:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
            t-bediener.rec-id = RECID(bediener).
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH bediener NO-LOCK:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
            t-bediener.rec-id = RECID(bediener).
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH bediener WHERE bediener.flag = int1 NO-LOCK:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
            t-bediener.rec-id = RECID(bediener).
        END.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST bediener WHERE bediener.user-group = int1
            AND bediener.flag = int2 NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN 
        DO:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
            t-bediener.rec-id = RECID(bediener).
        END.
    END.
    WHEN 5 THEN
    DO: 
        FIND FIRST bediener WHERE RECID(bediener) = int1 NO-LOCK.
        IF AVAILABLE bediener THEN 
        DO:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
            t-bediener.rec-id = RECID(bediener).
        END.
    END.
    WHEN 6 THEN
    DO:
        FOR EACH bediener WHERE bediener.nr NE 0 NO-LOCK:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
            t-bediener.rec-id = RECID(bediener).
        END.
    END.

END CASE.
