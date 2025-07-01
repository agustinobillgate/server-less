
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER rec-id      AS INT.
DEF INPUT PARAMETER datum       AS DATE.
DEF INPUT PARAMETER dept        AS INT.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id.

IF case-type = 1 THEN
DO :
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    l-orderhdr.lieferdatum = datum.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    l-orderhdr.angebot-lief[1] = dept.
END.
ELSE IF case-type = 3 THEN
DO :
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    l-orderhdr.gedruckt = today.
END.

FIND CURRENT l-orderhdr NO-LOCK.
