
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER bez    AS CHAR.

DEFINE buffer l-od FOR l-order.

FIND FIRST l-order WHERE RECID(l-order) = rec-id.

FIND FIRST l-od WHERE RECID(l-od) = RECID(l-order) EXCLUSIVE-LOCK. 
l-od.quality = SUBSTR(l-od.quality,1,11) + bez. 
FIND CURRENT l-od NO-LOCK.
