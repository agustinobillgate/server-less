
DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT PARAMETER location AS INT.
DEF INPUT PARAMETER floor AS INT.
DEF OUTPUT PARAMETER f-char AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FIND FIRST htparam WHERE htparam.paramnr = 571 NO-LOCK.
IF htparam.feldtyp = 5 AND htparam.fchar NE "" THEN
    ASSIGN f-char = htparam.fchar.

FOR EACH queasy WHERE queasy.key = 25 AND queasy.number1 = location 
    AND queasy.number2 = floor NO-LOCK BY queasy.char1:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    /*MTcurr-n = curr-n + 1. 
    RUN assign-room(curr-n, queasy.char1, INTEGER(queasy.deci1), 
        INTEGER(queasy.deci2)). 
    RUN disp-room(curr-n). */
END. 
