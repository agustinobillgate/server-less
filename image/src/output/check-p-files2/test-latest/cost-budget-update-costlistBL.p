
DEF INPUT PARAMETER cost-list-rec-id AS INT.
DEF INPUT PARAMETER name1 AS CHAR.

RUN update-costlist.

PROCEDURE update-costlist: 
  FIND FIRST parameters WHERE RECID(parameters) = cost-list-rec-id 
    EXCLUSIVE-LOCK. 
  parameters.vstring = name1. 
  FIND CURRENT parameters NO-LOCK.
END. 
