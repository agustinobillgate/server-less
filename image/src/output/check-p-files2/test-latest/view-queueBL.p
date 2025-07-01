
DEFINE TEMP-TABLE t-queasy    LIKE queasy.

DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.


FOR EACH queasy WHERE queasy.KEY = 162 NO-LOCK BY queasy.char1:
    FIND FIRST zimmer WHERE zimmer.zinr = queasy.char1 NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer AND zimmer.zistatus LT 3 THEN DO:
        CREATE t-queasy.
        BUFFER-COPY queasy TO t-queasy.
    END.
END.
