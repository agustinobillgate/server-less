DEFINE INPUT PARAMETER billdate  AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER err-code AS INTEGER NO-UNDO.


FIND FIRST gl-jouhdr WHERE gl-jouhdr.jtype = 6 /** receiving **/   
    AND gl-jouhdr.datum GE billdate NO-LOCK NO-ERROR.   
IF AVAILABLE gl-jouhdr THEN err-code = 1.  
