DEFINE TEMP-TABLE t-l-artikel LIKE l-artikel.  

DEF INPUT  PARAMETER sorttype AS INT.
DEF INPUT  PARAMETER int1       AS INT.
DEF INPUT  PARAMETER int2       AS INT.
DEF INPUT  PARAMETER chr1       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

DEF VAR a-bezeich AS CHAR.
a-bezeich = chr1.
IF sorttype = 1 THEN
DO :
    FOR EACH l-artikel WHERE l-artikel.artnr GE int1
        AND l-artikel.artnr LE int2 NO-LOCK:
        RUN create-art.
    END.
END.
ELSE
DO:
    IF SUBSTR(a-bezeich, length(a-bezeich), 1) NE "*" THEN 
        a-bezeich = a-bezeich + "*". 
    FOR EACH l-artikel WHERE l-artikel.bezeich MATCHES (a-bezeich) NO-LOCK:
        RUN create-art.
    END.
END.

PROCEDURE create-art:
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
END.
