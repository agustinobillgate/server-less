
DEF INPUT  PARAMETER docu-nr LIKE l-orderhdr.docu-nr.

FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK NO-ERROR.

FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
ASSIGN
    l-orderhdr.gedruckt = ?.
FIND CURRENT l-orderhdr NO-LOCK.
