DEFINE TEMP-TABLE t-artikel LIKE artikel.

DEFINE INPUT PARAMETER artType  AS CHARACTER. /*Payments, etc*/
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.

IF artType EQ "payments" THEN
DO:
    FOR EACH artikel WHERE (artikel.artart EQ 6 OR artikel.artart EQ 7) NO-LOCK:
        CREATE t-artikel.
        BUFFER-COPY artikel TO t-artikel.
    END.
END.
