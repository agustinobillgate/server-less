DEFINE TEMP-TABLE  t-zimmer       LIKE zimmer.  

DEFINE INPUT-OUTPUT PARAMETER zinr AS CHARACTER.
DEFINE OUTPUT PARAMETER msg-str    AS CHARACTER.

RUN read-zimmerbl.p (1, zinr, ?,?, OUTPUT TABLE t-zimmer).  
FIND FIRST t-zimmer NO-ERROR.  
IF NOT AVAILABLE t-zimmer THEN   
DO:   
    msg-str = "No such Room Number.".
    RETURN NO-APPLY.   
END.   
