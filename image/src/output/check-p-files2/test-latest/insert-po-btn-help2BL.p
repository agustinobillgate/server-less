
DEF INPUT PARAMETER s-artnr AS INT.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
l-artikel.lief-einheit = 1. 
FIND CURRENT l-artikel NO-LOCK.
