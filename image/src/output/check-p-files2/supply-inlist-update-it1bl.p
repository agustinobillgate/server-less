
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-op WHERE RECID(l-op) = rec-id.

FOR EACH l-order WHERE l-order.docu-nr = l-op.docu-nr 
    AND l-order.lief-nr = l-op.lief-nr 
    AND l-order.pos GE 0 AND l-order.loeschflag = 1 EXCLUSIVE-LOCK: 
    l-order.loeschflag = 0. 
    RELEASE l-order. 
END. 
