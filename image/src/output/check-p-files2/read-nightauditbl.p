DEF TEMP-TABLE t-nightaudit LIKE nightaudit
    FIELD n-recid AS INTEGER.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER int1      AS INTEGER.
DEFINE INPUT PARAMETER int2      AS INTEGER.
DEFINE INPUT PARAMETER char1     AS CHAR.
DEFINE INPUT PARAMETER log1      AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-nightaudit.


CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH nightaudit WHERE abschlussart AND selektion NO-LOCK:
            CREATE t-nightaudit.
            BUFFER-COPY nightaudit TO t-nightaudit.
            ASSIGN t-nightaudit.n-recid = RECID(nightaudit).
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH nightaudit NO-LOCK:
            CREATE t-nightaudit.
            BUFFER-COPY nightaudit TO t-nightaudit.
            ASSIGN t-nightaudit.n-recid = RECID(nightaudit).
        END.
    END.
END CASE.
