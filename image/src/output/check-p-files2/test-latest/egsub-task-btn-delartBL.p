
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST eg-subtask WHERE RECID(eg-subtask) = rec-id.
FIND CURRENT eg-subtask EXCLUSIVE-LOCK.  
DELETE eg-subtask.  
RELEASE eg-subtask.
