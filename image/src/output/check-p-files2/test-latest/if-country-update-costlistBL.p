
DEF INPUT PARAMETER cost-list-rec-id AS INT.
DEF INPUT PARAMETER zone1 AS CHAR.
DEF INPUT PARAMETER grace1 AS INT.
DEF INPUT PARAMETER wday1 AS INT.
DEF INPUT PARAMETER ftime1 AS INT.
DEF INPUT PARAMETER ttime1 AS INT.
DEF INPUT PARAMETER tdura1 AS INT.
DEF INPUT PARAMETER dura1 AS INT.
DEF INPUT PARAMETER cost1 AS DECIMAL.

RUN update-costlist.

PROCEDURE update-costlist: 
DEFINE VARIABLE s AS CHAR INITIAL "". 
/* 
  s = user-init + " " + STRING(TODAY) + " " + STRING(TIME,"HH:MM") + ";". 
*/ 
  FIND FIRST parameters WHERE RECID(parameters) = cost-list-rec-id 
    EXCLUSIVE-LOCK. 
  /* Rd, #751, 27Mar25, if available parameters, update parameters */
  IF AVAILABLE parameters THEN 
  DO:
    ASSIGN
      parameters.vstring = STRING(grace1) + ";" 
                     + STRING(wday1)  + ";" 
                     + STRING(ftime1,"9999") + ";" 
                     + STRING(ttime1,"9999") + ";" 
                     + STRING(tdura1) + ";" 
                     + STRING(dura1)  + ";" 
                     + STRING(cost1,">>>>>>9.99") + ";" 
                     + s. 
    FIND CURRENT parameters NO-LOCK. 
  /*
    FIND FIRST parameters WHERE RECID(parameters) = cost-list-rec-id 
      EXCLUSIVE-LOCK. 
    parameters.vstring = STRING(grace1) + ";" 
                      + STRING(wday1)  + ";" 
                      + STRING(ftime1,"9999") + ";" 
                      + STRING(ttime1,"9999") + ";" 
                      + STRING(tdura1) + ";" 
                      + STRING(dura1)  + ";" 
                      + STRING(cost1,">>>>>>9.99") + ";" 
                      + s. 
    FIND CURRENT parameters NO-LOCK. 
  */
  END. 
END. 
