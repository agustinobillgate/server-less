
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id EXCLUSIVE-LOCK. 
delete l-ophdr. 
