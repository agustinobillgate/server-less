
DEF INPUT PARAMETER t-h-rezept-artnrrezept AS INT.

FIND FIRST h-rezept WHERE h-rezept.artnrrezept EQ t-h-rezept-artnrrezept NO-LOCK NO-ERROR.
IF AVAILABLE h-rezept THEN /*Alder - Serverless - Issue 643*/
DO:
    FIND FIRST h-rezlin WHERE h-rezlin.artnrrezept EQ t-h-rezept-artnrrezept NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE h-rezlin: 
        FIND CURRENT h-rezlin EXCLUSIVE-LOCK. 
        DELETE h-rezlin. 
        FIND NEXT h-rezlin WHERE h-rezlin.artnrrezept = t-h-rezept-artnrrezept NO-LOCK NO-ERROR. 
    END. 
    
    /*FDL Dec 26, 2022 => Ticket 66CF3E*/
    FIND FIRST queasy WHERE queasy.KEY EQ 252 AND queasy.number1 EQ t-h-rezept-artnrrezept NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        DELETE queasy.
        RELEASE queasy.
    END.
    
    FIND CURRENT h-rezept EXCLUSIVE-LOCK. 
    DELETE h-rezept.
    RELEASE h-rezept.
END.
