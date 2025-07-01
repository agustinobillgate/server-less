DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id.
FIND CURRENT l-ophdr EXCLUSIVE-LOCK.
DELETE l-ophdr.
RELEASE l-ophdr.
