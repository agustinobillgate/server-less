DEFINE TEMP-TABLE cost-list 
  FIELD rec-id AS INTEGER 
  FIELD zone  AS CHAR    FORMAT "x(4)" LABEL "Zone Name" 
  FIELD grace AS INTEGER FORMAT ">>9" LABEL "Grace" 
  FIELD wday  AS INTEGER FORMAT "9" LABEL "Day" 
  FIELD ftime AS INTEGER FORMAT "9999" LABEL "FTime" 
  FIELD ttime AS INTEGER FORMAT "9999" LABEL "TTime" 
  FIELD tdura AS INTEGER FORMAT "999999" LABEL "ToDurat" 
  FIELD dura  AS INTEGER FORMAT "999999" LABEL "Duration" 
  FIELD cost  AS DECIMAL FORMAT ">,>>>,>>9.99" LABEL "GuestAmount" 
  FIELD info  AS CHAR FORMAT "x(20)" LABEL "Last Changed". 

DEF INPUT PARAMETER zone1 AS CHAR.
DEF INPUT PARAMETER grace1 AS INT.
DEF INPUT PARAMETER wday1 AS INT.
DEF INPUT PARAMETER ftime1 AS INT.
DEF INPUT PARAMETER ttime1 AS INT.
DEF INPUT PARAMETER tdura1 AS INT.
DEF INPUT PARAMETER dura1 AS INT.
DEF INPUT PARAMETER cost1 AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR cost-list.

RUN add-costlist. 

PROCEDURE add-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE k AS INTEGER. 
  create parameters. 
  parameters.progname = "interface". 
  parameters.section = "zone". 
  parameters.varname = zone1. 
  parameters.vtype = 1. 
  parameters.vstring = STRING(grace1) + ";" 
                     + STRING(wday1)  + ";" 
                     + STRING(ftime1,"9999") + ";" 
                     + STRING(ttime1,"9999") + ";" 
                     + STRING(tdura1) + ";" 
                     + STRING(dura1)  + ";" 
                     + STRING(cost1,">>>>>>9.99") + ";". 
 
  create cost-list. 
  cost-list.rec-id = RECID(parameters). 
  cost-list.zone = parameters.varname. 
  i = 1. 
  n = 0. 
  m = 1. 
  DO WHILE i LE 7: 
    n = n + 1. 
    IF SUBSTR(parameters.vstring, n, 1) = ";" THEN 
    DO: 
      IF i = 1 THEN 
        cost-list.grace = INTEGER(SUBSTR(parameters.vstring, m, n - m)). 
      ELSE IF i = 2 THEN 
        cost-list.wday = INTEGER(SUBSTR(parameters.vstring, m, n - m)). 
      ELSE IF i = 3 THEN 
        cost-list.ftime = INTEGER(SUBSTR(parameters.vstring, m, n - m)). 
      ELSE IF i = 4 THEN 
        cost-list.ttime = INTEGER(SUBSTR(parameters.vstring, m, n - m)). 
      ELSE IF i = 5 THEN 
        cost-list.tdura = INTEGER(SUBSTR(parameters.vstring, m, n - m)). 
      ELSE IF i = 6 THEN 
        cost-list.dura = INTEGER(SUBSTR(parameters.vstring, m, n - m)). 
      ELSE IF i = 7 THEN 
      DO: 
        s = "". 
        DO k = m TO (n - 3): 
          IF SUBSTR(parameters.vstring, k, 1) = "." OR 
            SUBSTR(parameters.vstring, k, 1) = "," THEN 
            s = s + ",". 
          ELSE s = s + SUBSTR(parameters.vstring,k,1). 
        END. 
/*      cost-list.cost = DECIMAL(SUBSTR(parameters.vstring, m, n - m - 3)). */ 
        cost-list.cost = DECIMAL(s). 
        cost-list.cost = cost-list.cost 
          + DECIMAL(SUBSTR(parameters.vstring, n - 2, 2)) / 100. 
      END. 
      m = n + 1. 
      i = i + 1. 
    END. 
  END.
END. 
