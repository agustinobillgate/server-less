
DEF INPUT PARAMETER s-recid AS INT.
DEF INPUT PARAMETER bez     AS CHAR.

DEFINE buffer l-od FOR l-order.

FIND FIRST l-od WHERE RECID(l-od) = s-recid EXCLUSIVE-LOCK. 
l-od.quality = STRING(SUBSTR(l-od.quality,1,11), "x(11)") + bez. 
FIND CURRENT l-od NO-LOCK. 
