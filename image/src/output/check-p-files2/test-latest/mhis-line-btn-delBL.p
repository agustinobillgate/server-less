
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST mhis-line WHERE RECID(mhis-line) = rec-id EXCLUSIVE-LOCK.
delete mhis-line.
