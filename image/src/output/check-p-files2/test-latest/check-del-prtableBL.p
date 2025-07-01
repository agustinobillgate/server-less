

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER nr AS INT.
DEF INPUT PARAMETER bezeich AS CHAR.
DEF OUTPUT PARAMETER msg-str AS CHAR.

DEF VAR rcode AS CHAR NO-UNDO INIT "".

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "check-del-prtable".

FIND FIRST ratecode WHERE ratecode.marknr = nr 
  NO-LOCK NO-ERROR. 
IF AVAILABLE ratecode THEN rcode = ratecode.CODE.
ELSE
DO:
  FIND FIRST pricecod WHERE pricecod.marknr = nr 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE pricecod THEN rcode = pricecod.CODE.
END.
IF rcode NE "" THEN
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Rates exists, CODE = ",lvCAREA,"") + rcode 
          + "; " + translateExtended ("deleting not possibe",lvCAREA,"").
  RETURN NO-APPLY. 
END.
msg-str = msg-str + CHR(2) + "&Q"
        + translateExtended ("Do you really want to REMOVE the Price Market Table",lvCAREA,"") 
        + CHR(10)
        + STRING(nr) + " - " + bezeich + " ?".
