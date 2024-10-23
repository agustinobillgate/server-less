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

DEFINE TEMP-TABLE rsl 
    FIELD resnr         AS INTEGER 
    FIELD reslinnr      AS INTEGER 
    FIELD resstatus     AS INTEGER 
    FIELD sdate         AS DATE COLUMN-LABEL "Beg-Date" /*FONT 2 */
    FIELD ndate         AS DATE COLUMN-LABEL "End-Date" /*FONT 2 */
    FIELD stime         LIKE bk-reser.von-zeit COLUMN-LABEL "Start" /*FONT 2 */
    FIELD ntime         LIKE bk-reser.bis-zeit COLUMN-LABEL " End" /*FONT 2*/
    FIELD created-date  AS DATE COLUMN-LABEL "Created" /*FONT 2*/
    FIELD venue         LIKE bk-raum.raum COLUMN-LABEL "Venue" /*FONT 2*/
    FIELD userinit      AS CHAR FORMAT "x(4)" COLUMN-LABEL "ID" /*FONT 2*/
    FIELD mess-str      AS CHAR    
    FIELD info1         AS CHAR     
    FIELD info2         AS CHAR     
    FIELD info3         AS CHAR     
    FIELD t-veran-nr    AS INT      
    FIELD efield        AS CHARACTER
.

DEFINE TEMP-TABLE rsv-line 
    FIELD resnr         AS INTEGER 
    FIELD reslinnr      AS INTEGER 
    FIELD resstatus     AS INTEGER 
    FIELD sdate         AS DATE COLUMN-LABEL "Beg-Date" /*FONT 2 */
    FIELD ndate         AS DATE COLUMN-LABEL "End-Date" /*FONT 2 */
    FIELD stime         LIKE bk-reser.von-zeit COLUMN-LABEL "Start" /*FONT 2 */
    FIELD ntime         LIKE bk-reser.bis-zeit COLUMN-LABEL " End" /*FONT 2*/
    FIELD created-date  AS DATE COLUMN-LABEL "Created" /*FONT 2*/
    FIELD venue         LIKE bk-raum.raum COLUMN-LABEL "Venue" /*FONT 2*/
    FIELD userinit      AS CHAR FORMAT "x(4)" COLUMN-LABEL "ID" /*FONT 2*/
.

/**/
DEFINE INPUT PARAMETER curr-view        AS CHAR.
DEFINE INPUT PARAMETER from-date        AS DATE. 
DEFINE OUTPUT PARAMETER run-beowarning  AS LOGICAL.
DEFINE OUTPUT PARAMETER ba-dept         AS INTEGER.
DEFINE OUTPUT PARAMETER p-900           AS INTEGER.
DEFINE OUTPUT PARAMETER ci-date         AS DATE. 
DEFINE OUTPUT PARAMETER mess-str        AS CHAR.
DEFINE OUTPUT PARAMETER info1           AS CHAR.
DEFINE OUTPUT PARAMETER info2           AS CHAR.
DEFINE OUTPUT PARAMETER info3           AS CHAR.
DEFINE OUTPUT PARAMETER t-veran-nr      AS INT.
DEFINE OUTPUT PARAMETER avail-mainres   AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER efield          AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR rsl.
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

DEFINE VARIABLE zugriff     AS LOGICAL. 
DEFINE VARIABLE main-exist  AS LOGICAL INITIAL NO. 
DEFINE VARIABLE curr-resnr  AS INTEGER INITIAL 0. 
DEFINE VARIABLE count-j     AS INTEGER.
DEFINE VARIABLE counter     AS INTEGER.
DEFINE VARIABLE str         AS CHARACTER.
DEFINE VARIABLE gstat-found AS LOGICAL.
DEFINE VARIABLE end-gstat   AS LOGICAL.


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

/*FDL July 03, 2024*/
FOR EACH ba-plan NO-LOCK:
    counter = 0.
    gstat-found = NO.

    DO count-j = 1 TO 48:
        counter = counter + 1.
        IF ba-plan.gstatus[count-j] NE 0 THEN 
        DO:
            IF count-j LE 47 THEN
            DO:
                IF ba-plan.gstatus[count-j + 1] EQ 0 THEN
                DO:
                    gstat-found = YES.
                    LEAVE.
                END.
            END.            
            ELSE IF count-j EQ 48 AND ba-plan.gstatus[count-j] NE 0 THEN
            DO:
                gstat-found = YES.
                LEAVE.
            END.
        END.
    END.
    IF gstat-found THEN
    DO:
        DO count-j = 1 TO 48:
            IF ba-plan.resnr[count-j] EQ 0 THEN NEXT.
            ELSE
            DO:
                RUN get-banquet-plan-infobl.p(curr-view, ba-plan.bezeich, ba-plan.raum, ba-plan.nr, ba-plan.blocked[count-j],
                                              ba-plan.resnr[count-j], ba-plan.reslinnr[count-j], counter, from-date,
                                              OUTPUT mess-str, OUTPUT info1, OUTPUT info2, OUTPUT info3, OUTPUT TABLE rsv-line).
                RUN ba-plan-btn-notebl.p(ba-plan.resnr[count-j], OUTPUT t-veran-nr, OUTPUT avail-mainres).
                IF avail-mainres THEN RUN edit-baresnotebl.p(ba-plan.resnr[count-j], OUTPUT efield).

                FOR EACH rsv-line NO-LOCK:
                    CREATE rsl.
                    BUFFER-COPY rsv-line TO rsl.
                    ASSIGN
                        rsl.mess-str    = mess-str
                        rsl.info1       = info1
                        rsl.info2       = info2
                        rsl.info3       = info3
                        rsl.t-veran-nr  = t-veran-nr
                        rsl.efield      = efield
                        .
                END.
            END.
        END.
    END.    
END.
/************************************** PROCEDURES **************************************/
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
