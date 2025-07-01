
DEFINE TEMP-TABLE t-artikel LIKE artikel.

DEF INPUT  PARAMETER artNo              AS INT.
DEF OUTPUT PARAMETER long-digit         AS LOGICAL.
DEF OUTPUT PARAMETER to-date            AS DATE.
DEF OUTPUT PARAMETER double-currency    AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.


FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
to-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 

IF artNo GT 0 THEN 
    FOR EACH artikel WHERE artikel.departement = 0 
        AND artikel.artnr = artNo NO-LOCK:
        CREATE t-artikel.
        BUFFER-COPY artikel TO t-artikel.
    END.
ELSE 
    FOR EACH artikel WHERE artikel.departement = 0 
        AND (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.activeflag = YES NO-LOCK BY artikel.artnr:
        CREATE t-artikel.
        BUFFER-COPY artikel TO t-artikel.
    END.
