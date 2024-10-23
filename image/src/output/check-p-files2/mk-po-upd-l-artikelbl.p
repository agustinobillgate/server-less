
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-artikel WHERE RECID(l-artikel) = rec-id.

FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
l-artikel.lief-einheit = 1. 
FIND CURRENT l-artikel NO-LOCK.
