DEFINE INPUT PARAMETER qhead-recid AS INTEGER.
DEFINE INPUT PARAMETER status-nr AS INTEGER.
DEFINE OUTPUT PARAMETER ok-flag AS LOGICAL INITIAL NO.

DEFINE BUFFER q-kds-head FOR queasy.
DEFINE BUFFER q-kds-line FOR queasy.

FIND FIRST q-kds-head WHERE RECID(q-kds-head) EQ qhead-recid NO-LOCK NO-ERROR.
IF AVAILABLE q-kds-head THEN
DO:
    FIND CURRENT q-kds-head EXCLUSIVE-LOCK.
    q-kds-head.deci2 = status-nr.
    FIND CURRENT q-kds-head NO-LOCK.
    RELEASE q-kds-head.

    FOR EACH q-kds-line WHERE q-kds-line.KEY EQ 255 AND q-kds-line.deci2 EQ qhead-recid EXCLUSIVE-LOCK:
        q-kds-line.char3 = "1".
    END.
    ok-flag = YES.
END.
ELSE
DO:
    ok-flag = NO.
END.
 
