
DEF INPUT PARAMETER recid-aktline AS INT.

FIND FIRST akt-line WHERE RECID(akt-line) = recid-aktline NO-LOCK.
FIND CURRENT akt-line EXCLUSIVE-LOCK. 
DELETE akt-line. 
