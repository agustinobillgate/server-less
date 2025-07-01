DEFINE TEMP-TABLE t-queasy
    FIELD instruct-no   AS INTEGER
    FIELD dept-no       AS INTEGER
    FIELD department    AS CHARACTER
    FIELD instruction   AS CHARACTER
.
    
DEFINE INPUT PARAMETER dept-nr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.    

DEFINE BUFFER buffQueasy FOR queasy.

FOR EACH bk-queasy WHERE bk-queasy.key EQ 13 NO-LOCK:
    FIND FIRST buffQueasy WHERE buffQueasy.key EQ 148
        AND buffQueasy.number1 = bk-queasy.number2
        AND buffQueasy.number1 = dept-nr NO-LOCK NO-ERROR.
    IF AVAILABLE buffQueasy THEN 
    DO:
        CREATE t-queasy.
        ASSIGN 
            t-queasy.instruct-no    = bk-queasy.number1
            t-queasy.dept-no        = buffQueasy.number1
            t-queasy.department     = buffQueasy.char3
            t-queasy.instruction    = bk-queasy.char1
        .
    END.
END.
