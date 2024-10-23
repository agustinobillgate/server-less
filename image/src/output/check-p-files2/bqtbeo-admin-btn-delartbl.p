

DEF INPUT PARAMETER recid-queasy AS INT.

FIND FIRST queasy WHERE RECID(queasy) = recid-queasy EXCLUSIVE-LOCK.
DELETE queasy.
RELEASE queasy.

