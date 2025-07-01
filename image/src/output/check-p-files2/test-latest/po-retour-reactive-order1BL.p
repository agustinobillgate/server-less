
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF OUTPUT PARAMETER avail-l-od AS LOGICAL INIT NO.

DEFINE buffer l-od FOR l-order.

IF case-type = 1 THEN
DO:
    FIND FIRST l-od WHERE l-od.docu-nr = docu-nr AND 
        l-od.pos GT 0 AND (l-od.anzahl GT l-od.geliefert) NO-LOCK NO-ERROR.
    IF AVAILABLE l-od THEN avail-l-od = YES.
END.
ELSE IF case-type = 2 THEN
DO:
    FOR EACH l-od WHERE l-od.docu-nr = docu-nr AND 
        l-od.pos GE 0 AND l-od.loeschflag EQ 1 EXCLUSIVE-LOCK: 
        l-od.loeschflag = 0.
        release l-od.
    END.
END.
