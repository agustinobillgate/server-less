DEF INPUT PARAMETER pvILanguage AS INTEGER      NO-UNDO.
DEF INPUT PARAMETER gastno      AS INTEGER      NO-UNDO.
DEF OUTPUT PARAMETER comments   AS CHAR INIT "" NO-UNDO.

DEF BUFFER mguest FOR guest.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gcf-list". 

RUN fill-gcf-comments.

PROCEDURE fill-gcf-comments:
  ASSIGN comments = "".
  FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK.
  FIND FIRST vhp.mc-guest WHERE mc-guest.gastnr = gastno
    AND vhp.mc-guest.activeflag = YES NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.mc-guest THEN
  ASSIGN comments = translateExtended ("Membership No:",lvCAREA,"") 
    + " " + vhp.mc-guest.cardnum + CHR(10).
  comments = comments + guest.bemerk. 
  IF guest.master-gastnr GT 0 THEN 
  DO: 
    FIND FIRST mguest WHERE mguest.gastnr = guest.master-gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE mguest THEN 
    DO: 
      IF comments = "" THEN comments = mguest.name + ", " + mguest.anredefirma. 
      ELSE comments = mguest.name + ", " + mguest.anredefirma 
        + CHR(10) + comments. 
    END. 
  END. 
END.
