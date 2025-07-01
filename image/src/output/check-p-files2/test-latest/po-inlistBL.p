
DEF TEMP-TABLE t-l-op LIKE l-op
    FIELD l-artikel-artnr LIKE l-artikel.artnr
    FIELD l-artikel-bezeich LIKE l-artikel.bezeich.
DEF INPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER l-lieferant-firma AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-l-op.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
l-lieferant-firma = l-lieferant.firma.

FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
     AND l-op.op-art = 1 
     AND l-op.lief-nr = lief-nr AND l-op.docu-nr = docu-nr /* 
     AND l-op.loeschflag = 0 */ NO-LOCK, 
     FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK 
     BY l-op.datum BY l-op.artnr: 
    CREATE t-l-op.
    BUFFER-COPY l-op TO t-l-op.
    ASSIGN
        t-l-op.l-artikel-artnr = l-artikel.artnr
        t-l-op.l-artikel-bezeich = l-artikel.bezeich.
END.
