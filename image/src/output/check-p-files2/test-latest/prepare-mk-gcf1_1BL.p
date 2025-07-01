
DEF TEMP-TABLE t-nation1
    FIELD kurzbez LIKE nation.kurzbez.
DEF TEMP-TABLE t-guest LIKE guest.
DEF TEMP-TABLE t-sourccod1
    FIELD source-code LIKE sourccod.source-code
    FIELD bezeich LIKE sourccod.bezeich.


DEFINE INPUT  PARAMETER lastname AS CHARACTER FORMAT "x(30)". 
DEFINE INPUT  PARAMETER firstname AS CHARACTER FORMAT "x(30)". 

DEF OUTPUT PARAMETER err-nr AS INT INIT 0.
DEF OUTPUT PARAMETER curr-gastnr AS INT.
DEF OUTPUT PARAMETER lname AS CHAR.
DEF OUTPUT PARAMETER f-logical AS LOGICAL.
DEF OUTPUT PARAMETER avail-genlayout AS LOGICAL.
DEF OUTPUT PARAMETER refno-label        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-nation1.
DEF OUTPUT PARAMETER TABLE FOR t-sourccod1.
DEF OUTPUT PARAMETER TABLE FOR t-guest.

curr-gastnr = 0.
FIND FIRST guest WHERE guest.gastnr < 0 NO-ERROR. 
IF AVAILABLE guest THEN 
DO: 
  curr-gastnr = - guest.gastnr. 
  delete guest. 
  FIND FIRST guest WHERE guest.gastnr = curr-gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE guest THEN curr-gastnr = 0. 
END.

IF curr-gastnr = 0 THEN
DO: 
  FIND LAST guest WHERE guest.gastnr NE ? NO-LOCK NO-ERROR. 
  IF AVAILABLE guest THEN curr-gastnr = guest.gastnr + 1. 
  ELSE curr-gastnr = 1. 
END. 

FIND FIRST htparam WHERE paramnr = 999 NO-LOCK. 
IF htparam.flogical = YES AND curr-gastnr GT 300 THEN 
DO: 
  err-nr = 1.
  RETURN. 
END.

/*MTDO TRANSACTION:*/
    CREATE guest. 
    ASSIGN
      guest.karteityp = 1
      guest.gastnr = curr-gastnr
    . 
    lname = lastname. 
    guest.anredefirma = firstname. 
    lname = CAPS(SUBSTR(lname,1,1)) + SUBSTR(lname, 2, length(lname)). 
    FIND CURRENT guest NO-LOCK. 
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
/*END.*/

FIND FIRST htparam WHERE htparam.paramnr = 223 NO-LOCK. 
f-logical = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 1356 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN refno-label = htparam.fchar.

FOR EACH sourccod WHERE sourccod.betriebsnr = 0
    AND sourccod.source-code NE guest.segment3
    NO-LOCK BY sourccod.source-cod:
    CREATE t-sourccod1.
    ASSIGN 
      t-sourccod1.source-code = sourccod.source-code
      t-sourccod1.bezeich = sourccod.bezeich.
END.

FIND FIRST genlayout WHERE genlayout.KEY = "Guest Card" NO-LOCK NO-ERROR.
IF AVAILABLE genlayout THEN avail-genlayout = YES.

FOR EACH nation:
    CREATE t-nation1.
    ASSIGN t-nation1.kurzbez = nation.kurzbez.
END.
