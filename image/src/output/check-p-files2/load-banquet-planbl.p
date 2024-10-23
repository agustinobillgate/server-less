DEFINE TEMP-TABLE t-bk-raum LIKE bk-raum.
DEFINE TEMP-TABLE ba-plan 
  FIELD nr          AS INTEGER 
  FIELD raum        AS CHAR 
  FIELD bezeich     AS CHAR FORMAT "x(32)" LABEL "Room" 
  FIELD departement AS INTEGER
  FIELD resnr       AS INTEGER EXTENT 48 
  FIELD reslinnr    AS INTEGER EXTENT 48 
  FIELD gstatus     AS INTEGER EXTENT 48 
  FIELD room        AS CHAR    EXTENT 48 FORMAT "x(1)"
  FIELD blocked     AS INTEGER EXTENT 48
. 


DEFINE VARIABLE zugriff     AS LOGICAL. 

 

DEFINE VARIABLE main-exist  AS LOGICAL INITIAL NO. 
DEFINE VARIABLE curr-resnr  AS INTEGER INITIAL 0. 

/**/
DEFINE INPUT PARAMETER curr-view        AS CHAR.
DEFINE INPUT PARAMETER from-date        AS DATE. 
DEFINE OUTPUT PARAMETER run-beowarning  AS LOGICAL.
DEFINE OUTPUT PARAMETER ba-dept         AS INTEGER.
DEFINE OUTPUT PARAMETER p-900           AS INTEGER.
DEFINE OUTPUT PARAMETER ci-date         AS DATE. 
DEFINE OUTPUT PARAMETER TABLE FOR ba-plan.
/*
DEFINE VARIABLE run-beowarning  AS LOGICAL.
DEFINE VARIABLE from-date       AS DATE. 
DEFINE VARIABLE curr-view       AS CHAR INIT "daily". /*daily, weekly*/ 
DEFINE VARIABLE ba-dept         AS INTEGER.
DEFINE VARIABLE p-900           AS INTEGER.
DEFINE VARIABLE ci-date         AS DATE. 
*/
/*===============================================*/
/*===============================================*/
RUN prepare-ba-planbl.p
    (OUTPUT ci-date, OUTPUT ba-dept, OUTPUT run-beowarning, OUTPUT p-900, OUTPUT TABLE t-bk-raum).
/*from-date = ci-date. 
curr-view = "daily".*/

RUN create-rlist.

IF from-date GE ci-date THEN 
DO: 
    IF curr-view = "daily" THEN RUN create-dlist. 
    ELSE RUN create-wlist.
END.
ELSE
DO:
    /*from-date = from-date - 1. */
    IF curr-view = "daily" THEN RUN create-dlist-prev. 
    ELSE RUN create-wlist-prev.
END.


PROCEDURE create-rlist: 
  FOR EACH t-bk-raum NO-LOCK BY t-bk-raum.bezeich: 
      CREATE ba-plan. 
          ba-plan.nr          = 1. 
          ba-plan.raum        = t-bk-raum.raum. 
          ba-plan.bezeich     = t-bk-raum.bezeich. 
          ba-plan.departement = t-bk-raum.departement.
      CREATE ba-plan. 
          ba-plan.nr          = 2. 
          ba-plan.raum        = t-bk-raum.raum. 
          ba-plan.bezeich     = t-bk-raum.bezeich. 
          ba-plan.departement = t-bk-raum.departement.
      CREATE ba-plan. 
          ba-plan.nr          = 3. 
          ba-plan.raum        = t-bk-raum.raum. 
          ba-plan.bezeich     = t-bk-raum.bezeich. 
          ba-plan.departement = t-bk-raum.departement.
   END. 
END. 
 
PROCEDURE create-dlist-prev: /*Actual*/
    DEFINE VARIABLE i AS INTEGER.
    IF NOT main-exist THEN curr-resnr = 0.

    FOR EACH ba-plan:
        DO i = 1 TO 48:
            ASSIGN
                ba-plan.gstatus[i]  = 0 
                ba-plan.room[i]     = "" 
                ba-plan.resnr[i]    = 0 
                ba-plan.reslinnr[i] = 0
                ba-plan.blocked[i]  = 0
                .
        END.
        i = 1.
    END.
    RUN ba-plan-create-dlist-prevbl.p (INPUT-OUTPUT TABLE ba-plan, from-date).
END.

PROCEDURE create-dlist: 
    DEFINE VARIABLE i AS INTEGER. 
    IF NOT main-exist THEN curr-resnr = 0. 
    FOR EACH ba-plan: 
        DO i = 1 TO 48: 
            ASSIGN
            ba-plan.gstatus[i]  = 0 
            ba-plan.room[i]     = "" 
            ba-plan.resnr[i]    = 0 
            ba-plan.reslinnr[i] = 0
            ba-plan.blocked[i]  = 0.
        END. 
    END.
    RUN ba-plan-create-dlistbl.p (INPUT-OUTPUT TABLE ba-plan, from-date).
END. 


PROCEDURE create-wlist-prev: 
    DEFINE VARIABLE i     AS INTEGER. 
    DEFINE BUFFER rmBuff  FOR bk-raum.
    DEFINE BUFFER childRM FOR bk-raum.
    curr-resnr = 0. 
        FOR EACH ba-plan: 
            DO i = 1 TO 48:
                ASSIGN
                ba-plan.gstatus[i]  = 0
                ba-plan.room[i]     = "" 
                ba-plan.resnr[i]    = 0 
                ba-plan.reslinnr[i] = 0
                ba-plan.blocked[i]  = 0
                . 
            END. 
        END. 
    RUN ba-plan-create-wlist-prevbl.p (INPUT-OUTPUT TABLE ba-plan, from-date).
END. 

PROCEDURE create-wlist: 
    DEFINE VARIABLE i     AS INTEGER. 
    DEFINE BUFFER rmBuff  FOR bk-raum.
    DEFINE BUFFER childRM FOR bk-raum.
    curr-resnr = 0. 
    FOR EACH ba-plan: 
        DO i = 1 TO 48:
            ASSIGN
            ba-plan.gstatus[i]  = 0
            ba-plan.room[i]     = "" 
            ba-plan.resnr[i]    = 0 
            ba-plan.reslinnr[i] = 0
            ba-plan.blocked[i]  = 0
            .
        END. 
    END.
    RUN ba-plan-create-wlistbl.p (INPUT-OUTPUT TABLE ba-plan, from-date).
END. 

/*
CURRENT-WINDOW:WIDTH = 241.
FOR EACH ba-plan BY ba-plan.bezeich:
    DISP ba-plan.bezeich FORMAT "x(10)" 
         ba-plan.room FORMAT "x(1)" LABEL "!" 
         /*ba-plan.gstatus*/
         WITH WIDTH 240.
END.
*/
