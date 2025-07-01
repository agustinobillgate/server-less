DEF INPUT PARAMETER recid-queasy AS INT.
/* Rd, if available, recid, #370, 12-Des-24 */
FIND FIRST queasy WHERE RECID(queasy) = recid-queasy NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    DELETE queasy.
END.
