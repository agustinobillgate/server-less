
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER comments-screen-value AS CHAR.
DEF INPUT PARAMETER datum AS DATE.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id NO-LOCK.
IF case-type = 1 THEN
DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    l-orderhdr.angebot-lief[1] = dept.
    FIND CURRENT l-orderhdr NO-LOCK.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    l-orderhdr.lief-fax[3] = comments-screen-value.
    FIND CURRENT l-orderhdr NO-LOCK.
END.
ELSE IF case-type = 3 THEN
DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    l-orderhdr.lieferdatum = datum.
    FIND CURRENT l-orderhdr NO-LOCK.
END.
ELSE IF case-type = 4 THEN
DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    DELETE l-orderhdr.
END.
