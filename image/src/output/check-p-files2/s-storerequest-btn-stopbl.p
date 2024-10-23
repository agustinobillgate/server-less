
DEF INPUT PARAMETER recid-l-ophdr AS INT.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = recid-l-ophdr.

FIND CURRENT l-ophdr EXCLUSIVE-LOCK.
DELETE l-ophdr.
