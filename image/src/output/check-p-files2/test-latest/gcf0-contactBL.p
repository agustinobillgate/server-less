
DEFINE TEMP-TABLE aktkont-list LIKE akt-kont
    FIELD nat   AS CHAR LABEL "Nat" FORMAT "x(3)"
    FIELD email AS CHAR LABEL "Email"
    FIELD rec-id AS INTEGER.

DEF INPUT-OUTPUT  PARAMETER TABLE FOR aktkont-list.
DEF INPUT  PARAMETER case-type   AS INTEGER.
DEF INPUT  PARAMETER gastnr      AS INTEGER.
DEF OUTPUT PARAMETER main-kont   AS CHAR.
DEF OUTPUT PARAMETER maincontact AS CHAR.

DEF BUFFER a-buff FOR akt-kont.
DEFINE VARIABLE kont-nr AS INTEGER.


IF case-type = 1 THEN   /*add*/
DO :
    FIND FIRST aktkont-list.
    kont-nr = 0. 
    FOR EACH a-buff WHERE a-buff.gastnr = gastnr NO-LOCK: 
      IF a-buff.kontakt-nr GT kont-nr THEN kont-nr = a-buff.kontakt-nr. 
    END.
    kont-nr = kont-nr + 1. 
    aktkont-list.kontakt-nr = kont-nr.
    CREATE akt-kont.
    RUN fill-aktkont.
    ASSIGN
      akt-kont.kategorie = 1
      akt-kont.kontakt-nr = kont-nr
      akt-kont.gastnr = gastnr.
END.
ELSE  IF case-type = 2 THEN   /*chg*/
DO :
    FIND FIRST aktkont-list.
    FIND FIRST akt-kont WHERE RECID(akt-kont) = aktkont-list.rec-id EXCLUSIVE-LOCK.
    IF AVAILABLE akt-kont THEN 
    DO:    
        BUFFER-COPY aktkont-list TO akt-kont.
        FIND CURRENT akt-kont NO-LOCK.
    END.
END.


PROCEDURE fill-aktkont:
  BUFFER-COPY aktkont-list TO akt-kont.
  ASSIGN
      akt-kont.funktion = aktkont-list.email + ";" + aktkont-list.nat.
  
  IF akt-kont.hauptkontakt = YES THEN
      main-kont = akt-kont.name + ", " + akt-kont.vorname + " " + akt-kont.anrede. 
  
  maincontact = main-kont.
END.
