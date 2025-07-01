
DEF TEMP-TABLE t-guest LIKE guest.
DEF TEMP-TABLE t-nation1
    FIELD kurzbez LIKE nation.kurzbez.
DEF TEMP-TABLE t-nation2 LIKE t-nation1.
DEF TEMP-TABLE t-nation3 LIKE t-nation1.

DEFINE INPUT  PARAMETER lastname AS CHARACTER FORMAT "x(30)". 
DEFINE INPUT  PARAMETER firstname AS CHARACTER FORMAT "x(30)". 

DEF OUTPUT PARAMETER read-birthdate AS LOGICAL.
DEF OUTPUT PARAMETER err-nr AS INTEGER.
DEF OUTPUT PARAMETER def-natcode AS CHAR.
DEF OUTPUT PARAMETER curr-gastnr AS INT.
DEF OUTPUT PARAMETER nation1 AS CHAR.
DEF OUTPUT PARAMETER land AS CHAR.
DEF OUTPUT PARAMETER lname AS CHAR.
DEF OUTPUT PARAMETER fname AS CHAR.
DEF OUTPUT PARAMETER f-logical AS LOGICAL.
DEF OUTPUT PARAMETER f-logical1 AS LOGICAL.
DEF OUTPUT PARAMETER htparam-feldtyp AS INT.
DEF OUTPUT PARAMETER htparam-flogical AS LOGICAL.
DEF OUTPUT PARAMETER avail-genlayout AS LOGICAL.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL.
DEF OUTPUT PARAMETER l-param472 AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-nation1.
DEF OUTPUT PARAMETER TABLE FOR t-nation2.
DEF OUTPUT PARAMETER TABLE FOR t-nation3.
DEF OUTPUT PARAMETER TABLE FOR t-guest.


FIND FIRST htparam WHERE htparam.paramnr = 937 NO-LOCK. 
read-birthdate = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 153 NO-LOCK. 
FIND FIRST nation WHERE nation.kurzbez = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE nation THEN 
DO: 
  err-nr = 1.
  RETURN. 
END. 
def-natcode = nation.kurzbez. 

curr-gastnr = 0. 
FIND FIRST guest WHERE guest.gastnr < 0 NO-ERROR. 
IF AVAILABLE guest THEN 
DO: 
  curr-gastnr = - guest.gastnr. 
  DELETE guest. 
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
  err-nr = 2.
  RETURN. 
END. 

FIND FIRST htparam WHERE htparam.paramnr = 472 NO-LOCK. 
IF htparam.paramgr = 99 AND htparam.feldtyp = 4 THEN
ASSIGN l-param472 = htparam.flogical.

CREATE guest. 
ASSIGN 
  guest.karteityp      = 0 
  guest.NAME           = ""
  guest.vornamekind[1] = ""
  guest.gastnr         = curr-gastnr
. 
FIND FIRST htparam WHERE paramnr = 153 NO-LOCK. 
ASSIGN
  nation1 = htparam.fchar 
  land    = htparam.fchar 
  lname   = lastname
  fname   = firstname 
  lname   = CAPS(SUBSTR(lname,1,1)) 
          + SUBSTR(lname, 2, length(lname))
  fname   = CAPS(SUBSTR(fname,1,1)) 
         + SUBSTR(fname, 2, length(fname))
. 

FIND CURRENT guest NO-LOCK. 
CREATE t-guest.
BUFFER-COPY guest TO t-guest.
/*DD here
FIND FIRST t-guest NO-LOCK.
FIND FIRST guestbook WHERE guestbook.gastnr EQ t-guest.gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guestbook THEN 
DO:
    IF SEARCH("c:\e1-vhp\eKTP-img") EQ ? THEN
    DO:
        DOS SILENT "mkdir" + VALUE("c:\e1-vhp\eKTP-img").
        COPY-LOB guestbook.imagefile TO FILE "c:\e1-vhp\eKTP-img".
    END.
    ELSE 
    DO:
        COPY-LOB guestbook.imagefile TO FILE "c:\e1-vhp\eKTP-img".
    END.
END.
*/
FIND FIRST htparam WHERE htparam.paramnr = 223 NO-LOCK.
IF AVAILABLE htparam THEN f-logical = YES.


FIND FIRST htparam WHERE htparam.paramnr = 939 NO-LOCK.
IF AVAILABLE htparam THEN f-logical1 = YES.

FOR EACH nation WHERE nation.natcode = 0:
    CREATE t-nation1.
    ASSIGN t-nation1.kurzbez = nation.kurzbez.
END.
FOR EACH nation WHERE nation.natcode > 0:
    CREATE t-nation2.
    ASSIGN t-nation2.kurzbez = nation.kurzbez.
END.
FOR EACH nation:
    CREATE t-nation3.
    ASSIGN t-nation3.kurzbez = nation.kurzbez.
END.

FIND FIRST htparam WHERE htparam.paramnr = 961 NO-LOCK.
ASSIGN
htparam-feldtyp = htparam.feldtyp
htparam-flogical = htparam.flogical.

FIND FIRST genlayout WHERE genlayout.KEY = "Guest Card" NO-LOCK NO-ERROR.
IF AVAILABLE genlayout THEN avail-genlayout = YES.

FIND FIRST queasy WHERE queasy.KEY = 27 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN avail-queasy = YES.
