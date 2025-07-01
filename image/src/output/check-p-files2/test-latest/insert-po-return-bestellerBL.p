
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER bemerkung AS CHAR.

FIND FIRST l-order WHERE l-order.artnr = rec-id EXCLUSIVE-LOCK. 
ASSIGN l-order.besteller = bemerkung.
FIND CURRENT l-order NO-LOCK.
