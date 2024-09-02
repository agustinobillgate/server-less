DEFINE TEMP-TABLE t-parameters LIKE parameters
  FIELD rec-id AS INTEGER.

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
 
DEFINE TEMP-TABLE zone-list 
  FIELD rec-id AS INTEGER 
  FIELD zone AS CHAR 
  FIELD city  AS CHAR FORMAT "x(20)" LABEL "City Name" 
  FIELD acode AS CHAR FORMAT "x(16)" LABEL "Dialed Code" 
  FIELD info  AS CHAR FORMAT "x(20)" LABEL "Last Changed". 

DEF INPUT PARAMETER fl-run-proc AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR cost-list.
DEF OUTPUT PARAMETER TABLE FOR zone-list.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.

IF fl-run-proc THEN RUN cleanup-zonelist.

RUN create-costlist. 
RUN create-zonelist. 

FOR EACH parameters WHERE parameters.progname = "interface"
    AND parameters.section = "zone" NO-LOCK:
    CREATE t-parameters.
    BUFFER-COPY parameters TO t-parameters.
    ASSIGN t-parameters.rec-id = RECID(parameters).
END.

PROCEDURE cleanup-zonelist: 
  FIND FIRST parameters WHERE progname = "if-internal" 
    AND section = "Dcode" AND varname GT "" NO-LOCK NO-ERROR. 
  IF AVAILABLE parameters THEN 
  FOR EACH parameters WHERE progname = "if-internal" 
    AND section = "Dcode" AND varname GT "": 
    delete parameters. 
  END. 
END. 
 
PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE k AS INTEGER. 
  FOR EACH parameters WHERE progname = "if-internal" 
    AND section = "zone" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.rec-id = RECID(parameters). 
    cost-list.zone = parameters.varname. 
    i = 1. 
    n = 0. 
    m = 1. 
    DO WHILE i LE 8 AND n LT length(vstring): 
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
          IF SUBSTR(parameters.vstring, n - 3, 1) = "." OR 
             SUBSTR(parameters.vstring, n - 3, 1) = "," THEN 
          DO: 
            cost-list.cost = DECIMAL(SUBSTR(parameters.vstring, m, n - m - 3)). 
            cost-list.cost = cost-list.cost 
              + DECIMAL(SUBSTR(parameters.vstring, n - 2, 2)) / 100. 
          END. 
          ELSE 
          DO: 
            cost-list.cost = DECIMAL(SUBSTR(parameters.vstring, m, n - m - 2)). 
            cost-list.cost = cost-list.cost 
              + DECIMAL(SUBSTR(parameters.vstring, n - 2, 2)) / 100. 
          END. 
        END. 
/* 
        ELSE IF i = 7 THEN 
        DO: 
          s = "". 
          DO k = m TO (n - 3): 
            IF SUBSTR(parameters.vstring, k, 1) = "." OR 
              SUBSTR(parameters.vstring, k, 1) = "," THEN 
              s = s + ",". 
            ELSE s = s + SUBSTR(parameters.vstring,k,1). 
          END. 
          cost-list.cost = DECIMAL(s). 
          cost-list.cost = cost-list.cost 
            + DECIMAL(SUBSTR(parameters.vstring, n - 2, 2)) / 100. 
        END. 
*/ 
        ELSE IF i = 8 THEN cost-list.info = SUBSTR(parameters.vstring, m, n - m). 
        m = n + 1. 
        i = i + 1. 
      END. 
    END. 
  END. 
END. 
 
PROCEDURE create-zonelist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE ifname AS CHAR INITIAL "if-internal" NO-UNDO. 
 
  &IF SUBSTRING(PROVERSION, 1, 1) >= "9" OR SUBSTRING(PROVERSION, 1, 1) = "1" &THEN 
    ifname = "interface". 
  &ENDIF. 
 
  FOR EACH parameters WHERE progname = ifname 
    AND section = "Dcode" AND varname GT "" NO-LOCK: 
    create zone-list. 
    zone-list.rec-id = RECID(parameters). 
    zone-list.zone = parameters.varname. 
    i = 1. 
    n = 0. 
    m = 1. 
    DO WHILE i LE 3 AND n LT length(vstring): 
      n = n + 1. 
      IF SUBSTR(parameters.vstring, n, 1) = ";" THEN 
      DO: 
        IF i = 1 THEN 
          zone-list.city = SUBSTR(parameters.vstring, m, n - m). 
        ELSE IF i = 2 THEN 
          zone-list.acode = SUBSTR(parameters.vstring, m, n - m). 
        ELSE IF i = 3 THEN 
          zone-list.info = SUBSTR(parameters.vstring, m, n - m). 
        m = n + 1. 
        i = i + 1. 
      END. 
    END. 
  END. 
END. 

