DEF INPUT PARAMETER deptnr    AS INT.
DEF INPUT PARAMETER mainnr    AS INT.
DEF OUTPUT PARAMETER subtask AS CHAR.

RUN mk-code.

PROCEDURE mk-code:
    DEF VAR tmp AS INTEGER NO-UNDO.
    DEF VAR ctr AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR queasy.

    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.number1 = deptnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
        RETURN.
    
    FIND FIRST qbuff WHERE qbuff.KEY = 133 AND qbuff.number1 = mainnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qbuff THEN
        RETURN.
    
    ctr = 0.
    FOR EACH eg-subtask WHERE /*eg-subtask.reserve-int = "" AND */
        eg-subtask.dept-nr = deptnr AND eg-subtask.main-nr = mainnr NO-LOCK :
        tmp = INTEGER(SUBSTR(eg-subtask.sub-code, 6, 3)) NO-ERROR.
        IF tmp  GT ctr THEN
            ctr = INTEGER(SUBSTR(eg-subtask.sub-code, 6, 3)) NO-ERROR.
    END.
    
    ctr = ctr + 1.
    subtask = STRING(deptnr, "99") + STRING(mainnr, "999") +
        STRING(ctr, "999").
END.
