
DEF TEMP-TABLE tbuff 
    FIELD tischnr LIKE vhp.tisch.tischnr.

DEF TEMP-TABLE zbuff 
    FIELD zinr LIKE vhp.zimmer.zinr.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER curr-printer   AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.

DEF OUTPUT PARAMETER b-title        AS CHAR.
DEF OUTPUT PARAMETER mc-flag        AS LOGICAL.
DEF OUTPUT PARAMETER mc-pos1        AS INT.
DEF OUTPUT PARAMETER mc-pos2        AS INT.
DEF OUTPUT PARAMETER curr-waiter    AS INTEGER INIT 1.
DEF OUTPUT PARAMETER vpos-flag      AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR tbuff.
DEF OUTPUT PARAMETER TABLE FOR zbuff.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-table".

FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = dept NO-LOCK. 
b-title = translateExtended ("Select Table",lvCAREA,""). 

/*MT not supported
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1007 NO-LOCK. 
IF vhp.htparam.flogical THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 200 NO-LOCK. 
  IF vhp.htparam.finteger = dept THEN 
  DO: 
    tablestr = translateExtended ("Cabin:",lvCAREA,""). 
    b-title = translateExtended ("Select Cabin",lvCAREA,""). 
  END. 
END.

FIND FIRST vhp.htparam WHERE paramnr = 300 NO-LOCK. 
hogatex-flag = vhp.htparam.flogical. 
IF hogatex-flag THEN 
DO: 
  FIND FIRST vhp.htparam WHERE paramnr = 301 NO-LOCK. 
  pf-dir = vhp.htparam.fchar. 
  FIND FIRST vhp.htparam WHERE paramnr = 326 NO-LOCK. 
  pf-filename = pf-dir + vhp.htparam.fchar. 
  FIND FIRST vhp.htparam WHERE paramnr = 305 NO-LOCK. 
  IF vhp.htparam.fchar NE "" THEN pf-filename2 = pf-dir + vhp.htparam.fchar. 
END. 
*/

DO: 
  FIND FIRST vhp.htparam WHERE paramnr = 336 NO-LOCK. 
  IF vhp.htparam.feldtyp = 4 THEN 
  DO: 
    mc-flag = vhp.htparam.flogical. 
    FIND FIRST vhp.htparam WHERE paramnr = 337 NO-LOCK. 
    mc-pos1 = vhp.htparam.finteger. 
    FIND FIRST vhp.htparam WHERE paramnr = 338 NO-LOCK. 
    mc-pos2 = vhp.htparam.finteger. 
  END. 
END.

FOR EACH tisch WHERE tisch.departement = dept:
    CREATE tbuff.
    ASSIGN tbuff.tischnr = vhp.tisch.tischnr.
END.

FOR EACH zimmer:
    CREATE zbuff.
    ASSIGN zbuff.zinr = vhp.zimmer.zinr.
END.

curr-waiter = INTEGER(user-init) NO-ERROR. 
FIND FIRST vhp.kellner WHERE kellner.kellner-nr = curr-waiter 
  AND kellner.departement = dept NO-LOCK NO-ERROR. 

FIND FIRST vhp.htparam WHERE paramnr = 975 no-lock.   /* VHP Front multi user */ 
vpos-flag = (vhp.htparam.finteger EQ 1).
