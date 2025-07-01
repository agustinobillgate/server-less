
DEF INPUT PARAMETER subtask-dept-nr AS INT.
DEF INPUT PARAMETER subtask-main-nr AS INT.

DEF OUTPUT PARAMETER t-sub-code AS CHAR.

RUN mk-code.

PROCEDURE mk-code:
    DEF VAR tmp AS INTEGER NO-UNDO.
    DEF VAR ctr AS INTEGER NO-UNDO.
    DEF BUFFER ebuff FOR eg-subtask.
    DEF BUFFER qbuff FOR queasy.

    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.number1 = subtask-dept-nr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
        RETURN.
    
    FIND FIRST qbuff WHERE qbuff.KEY = 133 AND qbuff.number1 = subtask-main-nr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qbuff THEN
        RETURN.
    
    ctr = 0.
    FOR EACH ebuff WHERE /* ebuff.reserve-int = "" AND */
        ebuff.dept-nr = subtask-dept-nr AND ebuff.main-nr = subtask-main-nr NO-LOCK :
        tmp = INTEGER(SUBSTR(ebuff.sub-code, 6, 3)) NO-ERROR.
        IF tmp  GT ctr THEN
            ctr = INTEGER(SUBSTR(ebuff.sub-code, 6, 3)) NO-ERROR.
    END.
    
    ctr = ctr + 1.
    t-sub-code = STRING(subtask-dept-nr, "99") + STRING(subtask-main-nr, "999") +
        STRING(ctr, "999").
END.


