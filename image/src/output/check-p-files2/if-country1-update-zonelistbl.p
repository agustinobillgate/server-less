
DEF INPUT PARAMETER zone-list-rec-id AS INT.
DEF INPUT PARAMETER city1 AS CHAR.
DEF INPUT PARAMETER acode1 AS CHAR.
DEF INPUT PARAMETER s AS CHAR.

RUN update-zonelist.

PROCEDURE update-zonelist:
  FIND FIRST parameters WHERE RECID(parameters) = zone-list-rec-id 
    EXCLUSIVE-LOCK. 
  parameters.vstring = city1 + ";" + acode1 + ";" + s. 
  FIND CURRENT parameters NO-LOCK. 
END.
