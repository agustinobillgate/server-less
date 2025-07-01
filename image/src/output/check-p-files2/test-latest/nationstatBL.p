
/*******************TEMP TABLE************/

DEFINE TEMP-TABLE room-list 
  FIELD NAME        AS CHAR FORMAT "x(24)" 
  FIELD bezeich     AS CHAR FORMAT "x(5)" LABEL "Code" BGCOLOR 7 FGCOLOR 15 
  FIELD summe       AS INTEGER FORMAT ">>>>9" LABEL "Total" BGCOLOR 7 FGCOLOR 15 
  FIELD room        AS INTEGER EXTENT 31 FORMAT ">>9" LABEL  ""
  FIELD proz        AS DECIMAL FORMAT ">>9.99" LABEL "(%)". 

DEFINE INPUT  PARAMETER printer-nr       AS INTEGER.
DEFINE INPUT  PARAMETER call-from        AS INTEGER.
DEFINE INPUT  PARAMETER txt-file         AS CHAR.
DEFINE INPUT  PARAMETER from-month       AS CHAR.
DEFINE INPUT  PARAMETER hide-zero        AS LOGICAL.
DEFINE INPUT  PARAMETER mi-arrival       AS LOGICAL.
DEFINE INPUT  PARAMETER mi-comp          AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.
/*************VARIABLES*****/
DEFINE STREAM s1.
DEFINE VARIABLE tot-all          AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE from-date        AS DATE. 
DEFINE VARIABLE to-date          AS DATE. 
DEFINE VARIABLE ci-date          AS DATE. 
DEFINE VARIABLE curr-day         AS INTEGER. 
DEFINE VARIABLE diff-one         AS INTEGER INITIAL 0. 
DEFINE VARIABLE ok               AS LOGICAL. 
DEFINE VARIABLE i                AS INTEGER. 

/************MAIN LOGIC********/
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

IF NOT mi-arrival THEN RUN create-browse.
ELSE RUN create-browse1.

IF hide-zero THEN
DO:
    FOR EACH room-list WHERE room-list.summe = 0:
        DELETE room-list.
    END.
END.    

/************PROCEDURE*******/

PROCEDURE create-browse: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE incl-comp AS LOGICAL INITIAL YES.
  
  incl-comp = NOT mi-comp. 
  tot-all = 0.
  FOR EACH room-list: 
    DELETE room-list. 
  END. 

  mm = INTEGER(SUBSTR(from-month,1,2)). 
  yy = INTEGER(SUBSTR(from-month,3,4)). 
  from-date = DATE(mm, 1, yy). 
  mm = mm + 1. 
  IF mm = 13 THEN 
  DO: 
    mm = 1. 
    yy = yy + 1. 
  END. 
  to-date = DATE(mm, 1, yy) - 1. 
  IF to-date GT ci-date THEN to-date = ci-date. 

  FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich: 
    create room-list. 
    ASSIGN 
        room-list.NAME = ENTRY(1,nation.bezeich , ";")
        room-list.bezeich = nation.kurzbez. 
 
    /* FDL Comment 3AF3E4
    DO datum = from-date TO to-date: 
      i = day(datum). 
      FOR EACH nationstat WHERE nationstat.nationnr = nation.nationnr 
        AND nationstat.datum = datum NO-LOCK: 
        IF incl-comp THEN 
        DO: 
          room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
            + nationstat.logkind2 + nationstat.loggratis. 
          room-list.summe = room-list.summe + nationstat.logerwachs 
            + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis. 
        END. 
        ELSE 
        DO: 
          room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
            + nationstat.logkind2. 
          room-list.summe = room-list.summe + nationstat.logerwachs 
            + nationstat.logkind1 + nationstat.logkind2. 
        END. 
      END. 
    END. 
    */
    /*FDL: 3AF3E4 - Optimasi for .py*/
    FOR EACH nationstat WHERE nationstat.nationnr = nation.nationnr 
        AND nationstat.datum GE from-date
        AND nationstat.datum LE to-date NO-LOCK BY nationstat.datum: 
        i = day(nationstat.datum).         
        IF incl-comp THEN 
        DO: 
          room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
            + nationstat.logkind2 + nationstat.loggratis. 
          room-list.summe = room-list.summe + nationstat.logerwachs 
            + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis. 
        END. 
        ELSE 
        DO: 
          room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
            + nationstat.logkind2. 
          room-list.summe = room-list.summe + nationstat.logerwachs 
            + nationstat.logkind1 + nationstat.logkind2. 
        END. 
    END. 
  END. 
  FOR EACH room-list WHERE room-list.summe NE 0:
      tot-all = tot-all + room-list.summe.
  END.
  IF tot-all GT 0 THEN
  DO:
      FOR EACH room-list WHERE room-list.summe NE 0:
        room-list.proz = room-list.summe / tot-all * 100.
      END.
  END.      
END. 
 
PROCEDURE create-browse1: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE curr-datum AS DATE. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE incl-comp AS LOGICAL INITIAL YES.
  
  incl-comp = NOT mi-comp. 
  tot-all = 0.
  FOR EACH room-list: 
    DELETE room-list. 
  END. 
  
  mm = INTEGER(SUBSTR(from-month,1,2)). 
  yy = INTEGER(SUBSTR(from-month,3,4)). 
  from-date = DATE(mm, 1, yy). 
  mm = mm + 1. 
  IF mm = 13 THEN 
  DO: 
    mm = 1. 
    yy = yy + 1. 
  END. 
  to-date = DATE(mm, 1, yy) - 1. 
  IF to-date GT ci-date THEN to-date = ci-date. 

  FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich : 
    create room-list. 
    room-list.NAME = ENTRY(1,nation.bezeich , ";").
    room-list.bezeich = nation.kurzbez.

    /* FDL Comment 3AF3E4
    DO curr-datum = from-date TO to-date: 
      i = day(curr-datum). 
    
      FOR EACH nationstat WHERE nationstat.nationnr = nation.nationnr 
        AND nationstat.datum = curr-datum NO-LOCK: 
        IF incl-comp THEN 
        DO: 
          room-list.room[i] = nationstat.ankerwachs + nationstat.ankkind1 
            + nationstat.ankkind2 + nationstat.ankgratis. 
          room-list.summe = room-list.summe + nationstat.ankerwachs 
            + nationstat.ankkind1 + nationstat.ankkind2 + nationstat.ankgratis. 
        END. 
        ELSE 
        DO: 
          room-list.room[i] = nationstat.ankerwachs + nationstat.ankkind1 
            + nationstat.ankkind2. 
          room-list.summe = room-list.summe + nationstat.ankerwachs 
            + nationstat.ankkind1 + nationstat.ankkind2. 
        END. 
      END. 
    END. 
    */
    /*FDL: 3AF3E4 - Optimasi for .py*/
    FOR EACH nationstat WHERE nationstat.nationnr = nation.nationnr 
        AND nationstat.datum GE from-date
        AND nationstat.datum LE to-date NO-LOCK BY nationstat.datum: 
        i = day(nationstat.datum).         
        IF incl-comp THEN 
        DO: 
          room-list.room[i] = nationstat.ankerwachs + nationstat.ankkind1 
            + nationstat.ankkind2 + nationstat.ankgratis. 
          room-list.summe = room-list.summe + nationstat.ankerwachs 
            + nationstat.ankkind1 + nationstat.ankkind2 + nationstat.ankgratis. 
        END. 
        ELSE 
        DO: 
          room-list.room[i] = nationstat.ankerwachs + nationstat.ankkind1 
            + nationstat.ankkind2. 
          room-list.summe = room-list.summe + nationstat.ankerwachs 
            + nationstat.ankkind1 + nationstat.ankkind2. 
        END. 
    END. 
  END. 
  FOR EACH room-list WHERE room-list.summe NE 0:
      tot-all = tot-all + room-list.summe.
  END.
  IF tot-all GT 0 THEN
  DO:
      FOR EACH room-list WHERE room-list.summe NE 0:
        room-list.proz = room-list.summe / tot-all * 100.
      END.
  END.      
END. 
