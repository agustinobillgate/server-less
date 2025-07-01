
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id.

FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
l-orderhdr.gedruckt = today.
FIND CURRENT l-orderhdr NO-LOCK.
