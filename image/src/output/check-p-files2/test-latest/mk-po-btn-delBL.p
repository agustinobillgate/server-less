
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-order WHERE RECID(l-order) = rec-id.
FIND CURRENT l-order EXCLUSIVE-LOCK. 
delete l-order.
