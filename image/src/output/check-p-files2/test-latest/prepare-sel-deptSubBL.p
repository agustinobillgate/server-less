
DEFINE TEMP-TABLE DeptSub
    FIELD deptsub-nr AS INTEGER
    FIELD deptsub-nm AS CHAR.

DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER msg-flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR DeptSub.

RUN define-engineering.
RUN create-related-dept.


PROCEDURE Define-engineering:
    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        ASSIGN EngID = 0
               msg-flag = YES.
    END.
END.

PROCEDURE create-Related-dept:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF VAR c AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR queasy.
        
/*
    FOR EACH dept-link:
        DELETE dept-link.
    END.
*/
    FOR EACH deptsub :
        DELETE deptsub.
    END.

    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.number1 = EngId
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO: 
/*
        CREATE dept-link.
        ASSIGN dept-link.dept-nr   = 
            dept-link.dept-nm   = .
*/
        CREATE deptsub.
        ASSIGN deptsub.deptsub-nr = EngId
               deptsub.deptsub-nm = queasy.char3.

        DO i = 1 TO NUM-ENTRIES(queasy.char2, ";"):
            c = INTEGER(ENTRY(i, queasy.char2, ";")).
            FIND FIRST qbuff WHERE qbuff.KEY = 19 AND qbuff.number1 = 
                INTEGER(ENTRY(i, queasy.char2, ";")) NO-LOCK NO-ERROR.
            IF AVAILABLE qbuff THEN
            DO:
/*
                CREATE dept-link.
                ASSIGN 
                    dept-link.dept-nr   = c
                    dept-link.dept-nm   = qbuff.char3.
*/
                CREATE deptsub.
                ASSIGN deptsub.deptsub-nr = c
                       deptsub.deptsub-nm = qbuff.char3.
            END.                
        END.
    END.
END.

PROCEDURE create-deptsub:
    DEFINE BUFFER qbuff FOR eg-subtask.
    DEFINE BUFFER qbuff1 FOR queasy.

    FOR EACH deptsub :
        DELETE deptsub.
    END.

    FOR EACH qbuff NO-LOCK:
        FIND FIRST deptsub WHERE deptsub.deptsub-nr = qbuff.dept-nr NO-LOCK NO-ERROR.
        IF AVAILABLE deptsub THEN
        DO:
        END.
        ELSE
        DO:
            FIND FIRST qbuff1 WHERE qbuff1.KEY = 19 AND qbuff1.number1 = qbuff.dept-nr NO-LOCK NO-ERROR.
            IF AVAILABLE qbuff1 THEN
            DO:
                CREATE deptsub.
                ASSIGN deptsub.deptsub-nr = qbuff.dept-nr
                       deptsub.deptsub-nm = qbuff1.char3.
            END.
            ELSE
            DO:
            END.
        END.
    END.
END.

