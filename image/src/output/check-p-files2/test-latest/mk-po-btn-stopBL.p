
DEF INPUT PARAMETER po-type AS INT.
DEF INPUT PARAMETER rec-id  AS INT.
DEF INPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER docu-nr AS CHAR.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id.

IF po-type = 1 THEN
DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK. 
    delete l-orderhdr.
END.

FOR EACH l-order WHERE l-order.lief-nr = lief-nr
    AND l-order.loeschflag = 0 AND l-order.pos GE 0
    AND l-order.docu-nr = docu-nr AND l-order.betriebsnr = 2:
    delete l-order.
END.
