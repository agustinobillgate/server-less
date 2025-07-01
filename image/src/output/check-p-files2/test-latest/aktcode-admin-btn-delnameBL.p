DEF INPUT  PARAMETER akt-code-aktionscode AS INT.
DEF INPUT  PARAMETER recid-akt-code       AS INT.
DEF OUTPUT PARAMETER erase-flag           AS LOGICAL INIT NO.

FIND FIRST akt-line WHERE akt-line.aktionscode EQ akt-code-aktionscode NO-LOCK NO-ERROR. 
IF AVAILABLE akt-line THEN .
ELSE 
DO: 
    FIND FIRST akt-code WHERE RECID(akt-code) EQ recid-akt-code NO-LOCK NO-ERROR.
    IF AVAILABLE akt-code THEN
    DO:
        FIND CURRENT akt-code EXCLUSIVE-LOCK. 
        DELETE akt-code.
        erase-flag = YES.
    END.
END. 
