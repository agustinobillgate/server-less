

DEF INPUT PARAMETER zone-list-rec-id AS INT.
DEF INPUT PARAMETER city1 AS CHAR.
DEF INPUT PARAMETER acode1 AS CHAR.

RUN update-zonelist.

PROCEDURE update-zonelist: 
DEFINE VARIABLE s AS CHAR INITIAL "". 
  FIND FIRST parameters WHERE RECID(parameters) = zone-list-rec-id NO-LOCK NO-ERROR. /* Malik Serverless : EXCLUSIVE-LOCK -> NO-LOCK NO-ERROR */ 
  /* Malik Serverless */
  IF AVAILABLE parameters THEN
  DO:
    FIND CURRENT parameters EXCLUSIVE-LOCK.
    parameters.vstring = city1 + ";" + acode1 + ";". 
    FIND CURRENT parameters NO-LOCK. 
    RELEASE parameters.
  END.
  /* END Malik */

  /* parameters.vstring = city1 + ";" + acode1 + ";". */
  /* FIND CURRENT parameters NO-LOCK. */
  /*MTzone-list.city = city1. 
  zone-list.acode = acode1. 
  zone-list.info = s. 
  b2:REFRESH() IN FRAME frame1. 
  city1 = "". 
  acode1 = "".*/
END. 
