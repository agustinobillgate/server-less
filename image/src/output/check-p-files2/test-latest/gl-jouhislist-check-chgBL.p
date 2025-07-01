
DEF INPUT  PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER jnr AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-jouhislist". 

FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = jnr NO-LOCK. 
IF gl-jhdrhis.activeflag = 1 THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Closed journals can not be edited",lvCAREA,"").
  err-code = 1.
  RETURN NO-APPLY.
END. 
FIND FIRST htparam WHERE paramnr = 983 NO-LOCK. 
IF htparam.flogical THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("G/L closing process is running, journal transaction not possible",lvCAREA,"").
END. 
