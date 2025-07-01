
DEF INPUT PARAMETER property-nr AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egmain FOR eg-maintain.
DEF BUFFER egReq FOR eg-request.


FIND FIRST egReq WHERE egReq.propertynr = property-nr AND egReq.reqstatus NE 5 NO-LOCK NO-ERROR.
FIND FIRST egmain WHERE egmain.propertynr = property-nr AND egmain.TYPE NE 3 NO-LOCK NO-ERROR.

IF AVAILABLE egReq OR AVAILABLE egmain THEN
DO:
    IF egReq.reqstatus NE 5 OR egmain.TYPE NE 3 THEN
    DO:
        fl-code = 1.
        RETURN NO-APPLY. 
    END.
    ELSE
    DO:
        fl-code = 2.
        RETURN NO-APPLY.
    END.
END.
ELSE
DO:  
    fl-code = 3.
    RETURN NO-APPLY.
END. 
