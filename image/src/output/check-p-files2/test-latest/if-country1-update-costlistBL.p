
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
  parameters.vstring = STRING(grace1) + ";" 
                     + STRING(wday1)  + ";" 
                     + STRING(ftime1,"9999") + ";" 
                     + STRING(ttime1,"9999") + ";" 
                     + STRING(tdura1) + ";" 
                     + STRING(dura1)  + ";" 
                     + STRING(cost1,">>>>>>9.99") + ";" 
                     + s. 
  FIND CURRENT parameters NO-LOCK. 
  /*MTcost-list.grace = grace1. 
  cost-list.wday = wday1. 
  cost-list.ftime = ftime1. 
  cost-list.ttime = ttime1. 
  cost-list.tdura = tdura1. 
  cost-list.dura = dura1. 
  cost-list.cost = cost1. 
  cost-list.info = s. 
  b1:REFRESH() IN FRAME frame1. 
  zone1 = "". 
  grace1 = 0. 
  wday1 = 0. 
  ftime1 = 0. 
  ttime1 = 0. 
  tdura1 = 0. 
  dura1 = 0. 
  cost1 = 0. 
  curr-select = "".(*/
END. 
