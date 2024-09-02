
DEFINE TEMP-TABLE room-list 
  FIELD recid1  AS INTEGER EXTENT 18 
  FIELD etage   AS INTEGER FORMAT "99 " LABEL "FL " 
  FIELD zinr    AS CHAR FORMAT "x(5)" LABEL "RmNo" 
  FIELD c-char  AS CHAR FORMAT "x(3)" LABEL " C " 
  FIELD i-char  AS CHAR FORMAT "x(3)" LABEL " I " 
  FIELD zikatnr AS INTEGER 
  FIELD rmcat   AS CHAR FORMAT "x(5)" LABEL "RmCat" 
  FIELD gstatus AS INTEGER EXTENT 18 
  FIELD room    AS CHAR EXTENT 18 FORMAT "x(5)". 

DEF INPUT PARAMETER from-room        AS CHAR NO-UNDO.
DEF INPUT-OUTPUT PARAMETER curr-date AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR room-list.

IF curr-date = ? THEN RUN htpdate.p(87, OUTPUT curr-date).
RUN create-browse.

PROCEDURE create-browse: 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE VARIABLE to-date AS DATE. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  
  FOR EACH zimmer WHERE zimmer.zinr GE from-room NO-LOCK: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    CREATE room-list. 
    ASSIGN
      room-list.etage  = zimmer.etage
      room-list.zinr   = zimmer.zinr 
      room-list.c-char = " " + zimmer.zikennz + " "
      room-list.rmcat  = zimkateg.kurzbez 
    . 
    IF NOT zimmer.sleeping THEN room-list.i-char = " I ". 
  END. 

  to-date = curr-date + 17. 
    
  FOR EACH zinrstat WHERE (zinrstat.datum GE curr-date AND zinrstat.datum LE to-date) 
    AND zinrstat.zinr GE from-room AND zinrstat.zimmeranz GT 0 NO-LOCK:  
    FIND FIRST room-list WHERE room-list.zinr = zinrstat.zinr NO-ERROR.
    IF AVAILABLE room-list THEN
    DO:
      datum1 = curr-date. 
      datum2 = to-date. 
      i = zinrstat.datum - datum1 + 1. 
      room-list.room[i] = STRING(zinrstat.zimmeranz,">9") + "/" + STRING(zinrstat.personen, "99"). 
      room-list.gstatus[i] = 9. 
    END. 
  END. 
END. 
 
