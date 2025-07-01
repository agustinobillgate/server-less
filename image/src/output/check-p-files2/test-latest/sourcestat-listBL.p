DEFINE TEMP-TABLE room-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD bezeich AS CHAR FORMAT "x(16)" LABEL "Source" BGCOLOR 7 FGCOLOR 15 
  FIELD summe AS INTEGER FORMAT ">>>>9" LABEL "Total" BGCOLOR 7 FGCOLOR 15 
  FIELD room AS INTEGER EXTENT 31 FORMAT ">>>9" LABEL  ""
.


DEFINE INPUT PARAMETER from-month       AS CHAR.
DEFINE INPUT PARAMETER ci-date          AS DATE.
DEFINE INPUT PARAMETER sorttype         AS INTEGER.
DEFINE INPUT PARAMETER hide-zero        AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.

DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE from-date AS DATE.
DEFINE VARIABLE to-date AS DATE.

FOR EACH room-list: 
    delete room-list. 
END.
mm = INTEGER(SUBSTR(from-month,1,2)). 
yy = INTEGER(SUBSTR(from-month,3,4)). 

/*IF mm GE 13 OR mm LE 0 THEN 
DO: 
    mm = 1. 
    yy = yy + 1. 
END.*/ 

IF mm NE 12 THEN
 ASSIGN
   from-date = DATE(mm, 1, yy)
   mm = mm + 1
   to-date = DATE(mm, 1, yy) - 1. 
ELSE
 ASSIGN
   from-date = DATE(mm, 1, yy)
   to-date = DATE(1,1, yy + 1) - 1.  /*FT 08/01/15*/

IF to-date GT ci-date THEN to-date = ci-date. 

FOR EACH sourccod NO-LOCK BY sourccod.bezeich: 
    create room-list. 
    room-list.bezeich = sourccod.bezeich. 
    DO datum = from-date TO to-date: 
      i = day(datum). 
      FOR EACH sources WHERE sources.source-code = sourccod.source-code 
        AND sources.datum = datum NO-LOCK: 
        IF sorttype = 1 THEN 
        DO: 
          room-list.room[i] =  sources.zimmeranz. 
          room-list.summe = room-list.summe + sources.zimmeranz . 
        END. 
        ELSE 
        DO: 
          room-list.room[i] =  sources.persanz. 
          room-list.summe = room-list.summe + sources.persanz . 
        END. 
      END. 
    END. 
END. 

IF hide-zero = YES THEN
DO:
  FOR EACH room-list WHERE room-list.summe = 0:
      DELETE room-list.
  END.
END.

