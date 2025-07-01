
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST queasy WHERE RECID(queasy) = rec-id.
FIND CURRENT queasy EXCLUSIVE-LOCK.
delete queasy.
