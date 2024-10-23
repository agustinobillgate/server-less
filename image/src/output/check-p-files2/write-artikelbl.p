DEFINE TEMP-TABLE t-artikel   LIKE artikel
    FIELD rec-id AS INT.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-artikel.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL INITIAL NO.

FIND FIRST t-artikel NO-LOCK NO-ERROR.
IF NOT AVAILABLE t-artikel THEN RETURN.

CASE case-type :
    WHEN 1 THEN
    DO:
        CREATE artikel.
        BUFFER-COPY t-artikel TO artikel.
        RELEASE artikel.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST artikel WHERE RECID(artikel) = t-artikel.rec-id EXCLUSIVE-LOCK.
        IF AVAILABLE artikel THEN
        DO:
            BUFFER-COPY t-artikel TO artikel.
            RELEASE artikel.
            success-flag = YES.
        END.
    END.

END CASE.
