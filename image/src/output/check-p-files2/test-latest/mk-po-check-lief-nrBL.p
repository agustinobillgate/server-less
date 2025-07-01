
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER lief-nr AS INT.

FOR EACH l-order WHERE l-order.docu-nr = docu-nr:
    l-order.lief-nr = lief-nr.
END.

FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE l-orderhdr THEN l-orderhdr.lief-nr = lief-nr.
