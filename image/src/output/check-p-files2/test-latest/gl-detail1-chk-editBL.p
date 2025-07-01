

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER jnr            AS INT.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER err-nr         AS INT INIT 0.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-detail1-chk-edit".

FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = jnr NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr THEN DO:
    IF gl-jouhdr.activeflag = 1 THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Closed journals can not be edited",lvCAREA,"").
      RETURN NO-APPLY. 
    END.
    ELSE LEAVE.
END.
ELSE DO:
    msg-str = msg-str + CHR(2)
              + translateExtended ("Archived journals can not be edited",lvCAREA,"").
      RETURN NO-APPLY. 
END.

 
FIND FIRST htparam WHERE paramnr = 983 NO-LOCK. 
IF htparam.flogical THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("G/L closing process is running, journal transaction not possible",lvCAREA,"").
END. 
