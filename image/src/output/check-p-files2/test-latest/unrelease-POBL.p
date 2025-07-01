

DEF INPUT  PARAMETER docu-nr LIKE l-orderhdr.docu-nr.
DEF OUTPUT PARAMETER flag AS INT INIT 0.


FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK NO-ERROR.
IF NOT AVAILABLE l-orderhdr THEN
DO:
    flag = 1.
    RETURN NO-APPLY.
END.
ELSE
DO:
    IF l-orderhdr.gedruckt = ? THEN
    DO:
        flag = 2.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
        flag = 3.
        RETURN NO-APPLY.
    END.
END.
