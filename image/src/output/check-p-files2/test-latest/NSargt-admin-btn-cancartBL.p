
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST argt-line WHERE RECID(argt-line) = rec-id NO-LOCK.
FIND CURRENT argt-line EXCLUSIVE-LOCK. 
delete argt-line. 
