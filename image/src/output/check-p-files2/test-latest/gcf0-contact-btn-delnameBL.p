
DEF INPUT  PARAMETER gastnr         AS INTEGER.
DEF INPUT  PARAMETER kontnr         AS INTEGER.
DEF OUTPUT PARAMETER main-kont      AS CHAR.
DEF OUTPUT PARAMETER maincontact    AS CHAR.

DEF BUFFER akt-kont1 FOR akt-kont.

FIND FIRST akt-kont WHERE akt-kont.kontakt-nr = kontnr AND akt-kont.gastnr = gastnr.
IF akt-kont.hauptkontakt = YES THEN 
DO: 
    FIND FIRST akt-kont1 WHERE akt-kont1.gastnr = gastnr 
      AND akt-kont1.hauptkontakt = NO NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont1 THEN 
    DO: 
      main-kont = akt-kont1.name + ", " 
        + akt-kont1.vorname + " " + akt-kont1.anrede. 
      /*MTDISP main-kont WITH FRAME frame1. */
      FIND CURRENT akt-kont EXCLUSIVE-LOCK. 
      akt-kont.hauptkontakt = NO. 
      FIND CURRENT akt-kont NO-lOCK.
      FIND CURRENT akt-kont1 EXCLUSIVE-LOCK. /*Bernatd B5A35C*/
      akt-kont1.hauptkontakt = YES. 
      FIND CURRENT akt-kont1 NO-LOCK.  
    END. 
    ELSE 
    DO: 
      main-kont = "". 
      /*MTDISP main-kont WITH FRAME frame1. */
    END. 
    maincontact = main-kont.
END. 
FIND CURRENT akt-kont EXCLUSIVE-LOCK. 
delete akt-kont.

/*MTOPEN QUERY q1 FOR EACH akt-kont WHERE akt-kont.gastnr = gastnr 
NO-LOCK BY akt-kont.name. */
