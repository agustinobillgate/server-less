DEFINE TEMP-TABLE tb3 LIKE ratecode
    FIELD s-recid     AS INTEGER. /*M real ratecode */

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER prcode       AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER market       AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER market-nr    AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER zikatnr      AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER argtnr       AS INTEGER  NO-UNDO. 

DEFINE OUTPUT PARAMETER comments    AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tb3.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ratecode-admin". 

RUN open-query.

PROCEDURE open-query: 
  ASSIGN comments = "". 
  FIND FIRST arrangement WHERE arrangement.argtnr = argtnr NO-LOCK. 
  IF arrangement.zuordnung NE "" THEN 
    comments = TRIM(STRING(arrangement.arrangement,"x(5)")) 
      + translateExtended (" - Comments:",lvCAREA,"") 
      + CHR(10) + arrangement.zuordnung + CHR(10). 
  
  FOR EACH guest-pr WHERE guest-pr.code = prcode NO-LOCK,
    FIRST guest WHERE guest.gastnr = guest-pr.gastnr NO-LOCK BY guest.NAME:
    IF guest.bemerk NE "" 
        AND (LENGTH(comments) + LENGTH(guest.bemerk) + LENGTH(guest.NAME)) LE 30000
        THEN 
        comments = comments + guest.name 
      + translateExtended (" - Comment:",lvCAREA,"") 
      + " " + guest.bemerk + CHR(10). 
  END.
 
  FIND FIRST prmarket WHERE prmarket.nr = market-nr NO-LOCK NO-ERROR.
  IF AVAILABLE prmarket THEN DO:
    FOR EACH ratecode WHERE ratecode.marknr = prmarket.nr 
        AND ratecode.code = prcode 
        AND ratecode.argtnr = argtnr AND ratecode.zikatnr = zikatnr NO-LOCK 
        BY ratecode.startperiode BY ratecode.wday
        BY ratecode.erwachs BY ratecode.kind1 BY ratecode.kind2:
        CREATE tb3.
        BUFFER-COPY ratecode TO tb3.
        ASSIGN tb3.s-recid = INTEGER(RECID(ratecode)).
     END.
  END.
END. 

