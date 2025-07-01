DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD guestname AS CHARACTER.

DEFINE INPUT  PARAMETER qNo         AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE VARIABLE guest-name AS CHARACTER NO-UNDO.

/* special for HK preference !!!! - from load-queasybl by MNAufal*/
FOR EACH queasy WHERE queasy.KEY = qNo NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.number3 = INTEGER(RECID(queasy)).
    /*frome read-res-linebl casetype 7 by MNAufal*/
    FIND FIRST res-line WHERE res-line.zinr = queasy.char1
        AND res-line.active-flag = 1 AND res-line.resnr NE 0
        NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        guest-name = res-line.NAME.
    END.
END.
