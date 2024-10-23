
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER bemerkung AS CHAR.

FIND FIRST l-order WHERE RECID(l-order) = rec-id.
FIND CURRENT l-order EXCLUSIVE-LOCK. 
ASSIGN l-order.besteller = bemerkung.
FIND CURRENT l-order NO-LOCK.
