
DEFINE TEMP-TABLE t-artikel     LIKE artikel.

DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

RUN htpdate.p(110, OUTPUT to-date).      /*Invoicing DATE */ 

FOR EACH artikel WHERE artikel.departement = 0
    AND (artikel.artart = 2 OR artikel.artart = 7)
    AND artikel.activeflag = YES NO-LOCK:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.
