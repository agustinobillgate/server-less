DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gastNo         AS INT.
DEF OUTPUT PARAMETER resnr1         AS INT.
DEF OUTPUT PARAMETER gname          AS CHAR.
DEF OUTPUT PARAMETER remark         AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-tbplan".

FIND FIRST guest WHERE guest.gastnr = gastNo NO-LOCK.
ASSIGN 
    resnr1        = guest.gastnr 
    gname         = guest.NAME + "," + guest.vorname1.

FIND FIRST vhp.mc-guest WHERE mc-guest.gastnr = vhp.guest.gastnr
    AND vhp.mc-guest.activeflag = YES NO-LOCK NO-ERROR.
IF AVAILABLE vhp.mc-guest THEN
DO:
  ASSIGN remark = translateExtended ("Membership No:",lvCAREA,"") 
      + " " + vhp.mc-guest.cardnum + CHR(10).
END.

