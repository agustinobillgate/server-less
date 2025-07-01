
DEF INPUT PARAMETER nonr AS INT.
DEF OUTPUT PARAMETER sloc AS CHAR.

FIND FIRST eg-property WHERE eg-property.nr = nonr NO-LOCK NO-ERROR.
IF AVAILABLE eg-property THEN
DO:
    FIND FIRST eg-location WHERE eg-location.nr = eg-property.location NO-LOCK NO-ERROR.  
    IF AVAILABLE eg-location THEN
    DO:
        ASSIGN sloc = eg-location.bezeich.
    END.
    ELSE
    DO:
        ASSIGN sloc = "".
    END.
END.
