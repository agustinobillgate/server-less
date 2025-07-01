DEFINE TEMP-TABLE akt-code-list LIKE akt-code. 

DEF INPUT PARAMETER TABLE FOR akt-code-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER recid-akt-code AS INT.

FIND FIRST akt-code-list.
IF case-type = 1 THEN
DO :
    CREATE akt-code. 
    akt-code.aktiongrup  = 1.
    akt-code.aktionscode = akt-code-list.aktionscode. 
    akt-code.bezeich     = akt-code-list.bezeich. 
    akt-code.bemerkung   = akt-code-list.bemerkung.  
END.
ELSE
DO:
    FIND FIRST akt-code WHERE RECID(akt-code) EQ recid-akt-code NO-LOCK NO-ERROR.
    IF NOT AVAILABLE akt-code THEN RETURN.
    ELSE
    DO:
        FIND CURRENT akt-code EXCLUSIVE-LOCK. 
        akt-code.aktiongrup  = 1.
        akt-code.aktionscode = akt-code-list.aktionscode. 
        akt-code.bezeich     = akt-code-list.bezeich. 
        akt-code.bemerkung   = akt-code-list.bemerkung. 
        FIND CURRENT akt-code NO-LOCK.
        RELEASE akt-code.
    END.
END.

PROCEDURE fill-akt-code: 
    akt-code.aktiongrup = 1.
    akt-code.aktionscode = akt-code-list.aktionscode. 
    akt-code.bezeich = akt-code-list.bezeich. 
    akt-code.bemerkung = akt-code-list.bemerkung. 
END. 
