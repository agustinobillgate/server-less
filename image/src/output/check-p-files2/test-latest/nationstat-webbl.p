
/*******************TEMP TABLE************/

DEFINE TEMP-TABLE room-list 
  FIELD nationnr    AS INTEGER
  FIELD NAME        AS CHAR FORMAT "x(24)" 
  FIELD bezeich     AS CHAR FORMAT "x(5)" LABEL "Code" BGCOLOR 7 FGCOLOR 15 
  FIELD summe       AS INTEGER FORMAT ">>>>9" LABEL "Total" BGCOLOR 7 FGCOLOR 15 
  FIELD room        AS INTEGER EXTENT 31 FORMAT ">>9" LABEL  ""
  FIELD proz        AS DECIMAL FORMAT ">>9.99" LABEL "(%)"
  FIELD d-percent   AS DECIMAL EXTENT 31 FORMAT ">9.99".  

DEFINE TEMP-TABLE total-per-day
  FIELD date-day    AS INTEGER
  FIELD total-nat   AS INTEGER.

DEFINE INPUT  PARAMETER printer-nr        AS INTEGER.
DEFINE INPUT  PARAMETER call-from         AS INTEGER.
DEFINE INPUT  PARAMETER txt-file          AS CHAR.
DEFINE INPUT  PARAMETER from-month        AS CHAR.
DEFINE INPUT  PARAMETER hide-zero         AS LOGICAL.
DEFINE INPUT  PARAMETER mi-arrival        AS LOGICAL.
DEFINE INPUT  PARAMETER mi-comp           AS LOGICAL.
DEFINE INPUT  PARAMETER mi-show-d-percent AS LOGICAL.
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
    FOR EACH room-list WHERE room-list.summe = 0:
    DELETE room-list.
    END.

/************PROCEDURE*******/


PROCEDURE create-browse: 
  DEFINE VARIABLE mm AS INTEGER. 
  DEFINE VARIABLE yy AS INTEGER. 
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE incl-comp AS LOGICAL INITIAL YES.
  DEFINE VARIABLE bezeich AS CHARACTER.

  incl-comp = NOT mi-comp. 

  tot-all = 0.
  FOR EACH room-list: 
    delete room-list. 
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
  IF to-date GT ci-date THEN 
    to-date = ci-date. 

  bezeich = ?.
  i = 0.

  /* Oscar (12/12/2024) - 2BE1FA - modify looping method */
  /* FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich : 
    create room-list. 
    ASSIGN 
        room-list.NAME = ENTRY(1,nation.bezeich , ";")
        room-list.bezeich = nation.kurzbez. 
 
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
  END. */

  /* Oscar - simulate LEFT JOIN (nation is LEFT and nationstat is RIGHT) */
  FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich:
    CREATE room-list. 
    ASSIGN 
        room-list.NAME = ENTRY(1,nation.bezeich , ";")
        room-list.bezeich = nation.kurzbez
        room-list.nationnr = nation.nationnr. 
  END.

  FOR EACH room-list NO-LOCK,
    EACH nationstat WHERE nationstat.nationnr EQ room-list.nationnr
    AND nationstat.datum GE from-date
    AND nationstat.datum LE to-date NO-LOCK 
    BY room-list.bezeich BY nationstat.datum:
      i = DAY(nationstat.datum).
      
      FIND FIRST total-per-day WHERE total-per-day.date-day EQ i NO-LOCK NO-ERROR.
      IF NOT AVAILABLE total-per-day THEN
      DO:
        CREATE total-per-day.
        ASSIGN
          total-per-day.date-day = i.
      END.

      IF incl-comp THEN 
      DO: 
        room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
                          + nationstat.logkind2 + nationstat.loggratis. 
        room-list.summe = room-list.summe + nationstat.logerwachs 
                        + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis. 
        total-per-day.total-nat = total-per-day.total-nat + nationstat.logerwachs 
                                + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis.
      END. 
      ELSE 
      DO: 
        room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
                          + nationstat.logkind2. 
        room-list.summe = room-list.summe + nationstat.logerwachs 
                        + nationstat.logkind1 + nationstat.logkind2.
        total-per-day.total-nat = total-per-day.total-nat + nationstat.logerwachs 
                                + nationstat.logkind1 + nationstat.logkind2.
      END. 
  END.

  FOR EACH room-list WHERE room-list.summe NE 0 EXCLUSIVE-LOCK:
    tot-all = tot-all + room-list.summe.

    /* Oscar (12/12/2024) - 2BE1FA - add validation to calculate day percentage */
    IF mi-show-d-percent THEN
    DO:
      FOR EACH total-per-day NO-LOCK:
        i = total-per-day.date-day.
        room-list.d-percent[i] = (room-list.room[i] / total-per-day.total-nat) * 100.
      END.
    END.
  END.

  IF tot-all GT 0 THEN
    FOR EACH room-list WHERE room-list.summe NE 0:
      room-list.proz = room-list.summe / tot-all * 100.
    END.
END. 
 
PROCEDURE create-browse1: 
  DEFINE VARIABLE mm AS INTEGER. 
  DEFINE VARIABLE yy AS INTEGER. 
  DEFINE VARIABLE curr-datum AS DATE. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE incl-comp AS LOGICAL INITIAL YES.
  DEFINE VARIABLE bezeich AS CHARACTER.

  incl-comp = NOT mi-comp. 

  FOR EACH room-list: 
    delete room-list. 
  END. 

  tot-all = 0.
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

  /* Oscar (12/12/2024) - 2BE1FA - modify looping method */
  /* FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich : 
    create room-list. 
    room-list.NAME = ENTRY(1,nation.bezeich , ";").
    room-list.bezeich = nation.kurzbez.
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
  END. */ 

  /* Oscar - simulate LEFT JOIN (nation is LEFT and nationstat is RIGHT) */
  FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich:
    CREATE room-list. 
    ASSIGN 
        room-list.NAME = ENTRY(1,nation.bezeich , ";")
        room-list.bezeich = nation.kurzbez
        room-list.nationnr = nation.nationnr. 
  END.

  FOR EACH room-list NO-LOCK,
    EACH nationstat WHERE nationstat.nationnr EQ room-list.nationnr
    AND nationstat.datum GE from-date
    AND nationstat.datum LE to-date NO-LOCK 
    BY room-list.bezeich BY nationstat.datum:
      i = DAY(nationstat.datum).
      
      FIND FIRST total-per-day WHERE total-per-day.date-day EQ i NO-LOCK NO-ERROR.
      IF NOT AVAILABLE total-per-day THEN
      DO:
        CREATE total-per-day.
        ASSIGN
          total-per-day.date-day = i.
      END.

      IF incl-comp THEN 
      DO: 
        room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
                          + nationstat.logkind2 + nationstat.loggratis. 
        room-list.summe = room-list.summe + nationstat.logerwachs 
                        + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis. 
        total-per-day.total-nat = total-per-day.total-nat + nationstat.logerwachs 
                                + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis.
      END. 
      ELSE 
      DO: 
        room-list.room[i] = nationstat.logerwachs + nationstat.logkind1 
                          + nationstat.logkind2. 
        room-list.summe = room-list.summe + nationstat.logerwachs 
                        + nationstat.logkind1 + nationstat.logkind2.
        total-per-day.total-nat = total-per-day.total-nat + nationstat.logerwachs 
                                + nationstat.logkind1 + nationstat.logkind2.
      END. 
  END.

  FOR EACH room-list WHERE room-list.summe NE 0 EXCLUSIVE-LOCK:
    tot-all = tot-all + room-list.summe.

    /* Oscar (12/12/2024) - 2BE1FA - add validation to calculate day percentage */
    IF mi-show-d-percent THEN
    DO:
      FOR EACH total-per-day NO-LOCK:
        i = total-per-day.date-day.
        room-list.d-percent[i] = (room-list.room[i] / total-per-day.total-nat) * 100.
      END.
    END.
  END.

  IF tot-all GT 0 THEN
    FOR EACH room-list WHERE room-list.summe NE 0:
      room-list.proz = room-list.summe / tot-all * 100.
    END.
END. 

