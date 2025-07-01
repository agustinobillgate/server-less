
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST queasy WHERE RECID(queasy) = rec-id NO-LOCK.
FIND CURRENT queasy EXCLUSIVE-LOCK. 
delete queasy.
RELEASE queasy.
