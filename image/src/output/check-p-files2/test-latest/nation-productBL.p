DEFINE TEMP-TABLE room-list 
    FIELD flag  AS INTEGER
    FIELD num   AS INTEGER 
    FIELD natnr AS INTEGER
    FIELD nr    AS INTEGER FORMAT ">>>" LABEL "No" BGCOL 7 FGCOL 15
    FIELD bezeich   AS CHAR FORMAT "x(24)" LABEL "NATION" BGCOL 7 FGCOL 15
    FIELD room      AS INTEGER EXTENT 12 FORMAT "->>,>>9" INITIAL 
      [0,0,0,0,0,0,0,0,0,0,0,0] 
    FIELD ytd AS INTEGER  FORMAT "->>>,>>9"  LABEL "Total YTD" 
    FIELD lytd AS INTEGER  FORMAT "->>>,>>9" LABEL "Tot LYTD"
.

DEFINE TEMP-TABLE tt-nation LIKE nation.
DEFINE TEMP-TABLE tt-natbuff LIKE nation.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER mm           AS INTEGER. 
DEFINE INPUT PARAMETER yy           AS INTEGER. 
DEFINE INPUT PARAMETER sorttype     AS INTEGER. 

DEFINE OUTPUT PARAMETER TABLE FOR room-list.

DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE from-date AS DATE.
DEFINE VARIABLE to-date AS DATE.
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE do-it AS LOGICAL.
DEFINE BUFFER r-list FOR room-list.
DEFINE BUFFER natbuff FOR nation.

DEFINE VARIABLE Lfr-date AS DATE.
DEFINE VARIABLE Lto-date AS DATE.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "nation-product". 
/******************Main Logic*********************/

FOR EACH room-list:
    DELETE room-list.
END.

ASSIGN
  from-date = DATE(1,1, yy)
  to-date   = (DATE(mm , 1, yy) + 32 )
  to-date   = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1
  Lfr-date  = DATE(1,1,yy - 1)
  Lto-date  = (DATE(mm , 1, yy - 1) + 32 )
  Lto-date  = DATE(MONTH(Lto-date), 1, YEAR(Lto-date)) - 1
.

/* Rulita 061224 | Fixing serverless issue git 128 */
FOR EACH nation WHERE nation.natcode EQ 0:
  CREATE tt-nation.
  BUFFER-COPY nation TO tt-nation.
END.

FOR EACH natbuff WHERE natbuff.natcode GT 0:
  CREATE tt-natbuff.
  BUFFER-COPY nation TO tt-natbuff.
END.
/* End Rulita */

DO:       
    FOR EACH natstat1 WHERE natstat1.datum GE from-date
        AND natstat1.datum LE to-date NO-LOCK BY natstat1.nationnr BY natstat1.datum :

        i = MONTH(natstat1.datum).  /* Malik serverless : MONTH(natstat.datum) -> MONTH(natstat1.datum) */     

        /* Rulita 061224 | Fixing serverless issue git 128 */
        FIND FIRST tt-nation WHERE tt-nation.nationnr EQ natstat1.nationnr NO-LOCK NO-ERROR.
        FIND FIRST tt-natbuff WHERE tt-natbuff.nationnr GT natstat1.nationnr NO-LOCK NO-ERROR.
        /* End Rulita */

        IF AVAILABLE tt-nation OR (NOT AVAILABLE tt-nation AND NOT AVAILABLE tt-natbuff) THEN
        DO:
          FIND FIRST room-list WHERE room-list.natnr = natstat1.nationnr 
            NO-LOCK NO-ERROR.
          IF NOT AVAILABLE room-list THEN
          DO:
            CREATE room-list.
            ASSIGN 
                room-list.natnr   = natstat1.nationnr.

             IF AVAILABLE tt-nation THEN room-list.bezeich = tt-nation.bezeich.
            ELSE room-list.bezeich = "UNKNOWN". 

            /*IF tt-nation.bezeich EQ "" THEN room-list.bezeich = "UNKNOWN". 
            ELSE room-list.bezeich = tt-nation.bezeich.*/

          END.
        
          IF sorttype = 0 THEN
            ASSIGN
            room-list.room[i] = room-list.room[i] + + natstat1.persanz
            room-list.ytd =  room-list.ytd + natstat1.persanz.
          ELSE
            ASSIGN
            room-list.room[i] = room-list.room[i] + + natstat1.zimmeranz
            room-list.ytd =  room-list.ytd + natstat1.zimmeranz.
        END.

    END.

    FOR EACH natstat1 WHERE natstat1.datum GE Lfr-date
        AND natstat1.datum LE Lto-date NO-LOCK BY natstat1.nationnr BY natstat1.datum :
        i = MONTH(natstat1.datum).      

        /* Rulita 061224 | Fixing serverless issue git 128 */
        FIND FIRST tt-nation WHERE tt-nation.nationnr EQ natstat1.nationnr NO-LOCK NO-ERROR.
        FIND FIRST tt-natbuff WHERE tt-natbuff.nationnr GT natstat1.nationnr NO-LOCK NO-ERROR.
        /* End Rulita */

        IF AVAILABLE tt-nation OR (NOT AVAILABLE tt-nation AND NOT AVAILABLE tt-natbuff) THEN
        DO:
          FIND FIRST room-list WHERE room-list.natnr = natstat1.nationnr 
            NO-LOCK NO-ERROR.
          IF NOT AVAILABLE room-list THEN
          DO:
            CREATE room-list.
            ASSIGN 
                room-list.natnr   = natstat1.nationnr.

             /*FIND FIRST nation WHERE nation.nationnr = natstat1.nationnr NO-LOCK NO-ERROR.*/
            IF AVAILABLE tt-nation THEN room-list.bezeich = tt-nation.bezeich.
            ELSE room-list.bezeich = "UNKNOWN". 
            /*IF tt-nation.bezeich EQ "" THEN room-list.bezeich = "UNKNOWN". 
            ELSE room-list.bezeich = tt-nation.bezeich.*/

          END.
        
          IF sorttype = 0 THEN
            ASSIGN
              room-list.lytd =  room-list.lytd + natstat1.persanz.
          ELSE
            ASSIGN
              room-list.lytd =  room-list.lytd + natstat1.zimmeranz.
        END.
    END.

    /**/


END.

i = 0. 
FOR EACH room-list WHERE room-list.ytd NE 0 OR room-list.lytd NE 0 
  BY room-list.ytd DESCENDING BY room-list.bezeich: 
    i = i + 1. 
    room-list.nr = i. 
    room-list.num = i. 
END.

FOR EACH room-list WHERE (room-list.nr = 0): 
  DELETE room-list. 
END.

CREATE room-list. 
ASSIGN 
  room-list.num  = 9999 
  room-list.flag = 1
  room-list.bezeich = translateExtended ("TOTAL",lvCAREA,""). 

FOR EACH r-list WHERE r-list.num LT 9999: 
  DO i = 1 TO 12: 
    room-list.room[i] = room-list.room[i] + r-list.room[i]. 
  END. 
  ASSIGN
    room-list.ytd = room-list.ytd + r-list.ytd
    room-list.lytd = room-list.lytd + r-list.lytd.
END. 


