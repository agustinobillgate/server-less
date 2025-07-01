
DEFINE TEMP-TABLE t-messages LIKE messages
    FIELD rec-id AS INT.

DEFINE INPUT  PARAMETER m-mess-recid AS INTEGER.
DEFINE OUTPUT PARAMETER username     AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-messages.

FIND FIRST messages WHERE RECID(messages) = m-mess-recid NO-LOCK. 
FIND FIRST bediener WHERE bediener.usercode = messages.usre NO-LOCK 
  NO-ERROR. 
IF AVAILABLE bediener THEN username = bediener.username. 
ELSE 
DO: 
  FIND FIRST bediener WHERE bediener.userinit = messages.usre NO-LOCK 
    NO-ERROR. 
  IF AVAILABLE bediener THEN username = bediener.username. 
  ELSE username = "". 
END. 

CREATE t-messages.
BUFFER-COPY messages TO t-messages.
ASSIGN t-messages.rec-id = RECID(messages).
