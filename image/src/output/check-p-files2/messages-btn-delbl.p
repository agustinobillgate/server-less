
DEFINE INPUT  PARAMETER rec-id AS INTEGER.

FIND FIRST messages WHERE RECID(messages) = rec-id NO-LOCK.
FIND CURRENT messages EXCLUSIVE-LOCK. 
delete messages. 
RELEASE messages.

