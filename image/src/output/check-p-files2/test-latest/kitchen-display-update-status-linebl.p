DEFINE INPUT PARAMETER line-recid AS INTEGER.
DEFINE INPUT PARAMETER status-nr  AS INTEGER.
DEFINE OUTPUT PARAMETER ok-flag AS LOGICAL INITIAL NO.

DEFINE BUFFER q-kds-line FOR queasy.
DEFINE VARIABLE save-time1 AS CHAR.
DEFINE VARIABLE save-time2 AS CHAR.
DEFINE VARIABLE save-time3 AS CHAR.
DEFINE VARIABLE orig-char  AS CHAR.

IF status-nr LT 0 THEN
DO:
    ok-flag = NO.
    RETURN.
END.
IF status-nr GT 3 THEN
DO:
    ok-flag = NO.
    RETURN.
END.

FIND FIRST q-kds-line WHERE RECID(q-kds-line) EQ line-recid EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE q-kds-line THEN
DO:
    q-kds-line.char3 = STRING(status-nr).
    ok-flag = YES.

    IF status-nr EQ 1 THEN save-time1 = STRING(NOW,"99/99/9999 HH:MM:SS").
    ELSE IF status-nr EQ 2 THEN save-time2 = STRING(NOW,"99/99/9999 HH:MM:SS").
    ELSE IF status-nr EQ 3 THEN save-time3 = STRING(NOW,"99/99/9999 HH:MM:SS").

    FIND FIRST queasy WHERE queasy.KEY EQ 302 AND queasy.betriebsnr EQ line-recid EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
        queasy.KEY = 302
        queasy.betriebsnr = line-recid
        queasy.char1 = save-time1 + "|" + save-time2 + "|" + save-time3.
    END.
    ELSE
    DO:
        orig-char = queasy.char1.
        IF save-time1 NE "" THEN queasy.char1 = save-time1 + "|" + ENTRY(2,orig-char,"|") + "|" + ENTRY(3,orig-char,"|").
        IF save-time2 NE "" THEN queasy.char1 = ENTRY(1,orig-char,"|") + "|" + save-time2 + "|" + ENTRY(3,orig-char,"|").
        IF save-time3 NE "" THEN queasy.char1 = ENTRY(1,orig-char,"|") + "|" + ENTRY(2,orig-char,"|") + "|" + save-time3.
    END.
END.
ELSE
DO:
    ok-flag = NO.
END.
