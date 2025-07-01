DEFINE TEMP-TABLE art-list
    FIELD vhp-artdept  AS INTEGER   FORMAT ">>9"    LABEL "Dept"
    FIELD vhp-artnr    AS INTEGER   FORMAT ">>9"    LABEL "Art No"
    FIELD vhp-arttype  AS CHARACTER FORMAT "x(20)"  LABEL "VHP Art Type"
    FIELD vhp-artname  AS CHARACTER FORMAT "x(20)"  LABEL "VHP Art Description"
    FIELD rms-artname  AS CHARACTER FORMAT "x(20)"  LABEL "RMS Art Description"
    FIELD rms-arttype  AS CHARACTER FORMAT "x(20)"  LABEL "RMS Art Type"
    .

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER dept      AS INT.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR art-list.

IF case-type EQ 1 THEN /*PREPARE*/
DO :
    FOR EACH h-artikel WHERE h-artikel.departemen EQ dept
        AND h-artikel.artart NE 0 NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 98 
            AND queasy.number2 EQ h-artikel.departemen 
            AND queasy.number3 EQ h-artikel.artnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY     = 242
                queasy.number1 = 98
                queasy.number2 = h-artikel.departemen 
                queasy.number3 = h-artikel.artnr
                queasy.char1   = h-artikel.bezeich
                .
        END.
        FIND CURRENT queasy.
        RELEASE queasy.
    END.
END.
ELSE IF case-type EQ 2 THEN /*"UPDATE"*/
DO:
    FOR EACH art-list BY art-list.vhp-artnr:
        FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 98 
            AND queasy.number2 EQ art-list.vhp-artdept 
            AND queasy.number3 EQ art-list.vhp-artnr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN 
                queasy.char2 = art-list.rms-arttype
                queasy.char3 = art-list.rms-artname
                .
        END.
        FIND CURRENT queasy.
        RELEASE queasy.
    END.
END.
EMPTY TEMP-TABLE art-list.
FOR EACH queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 98 
    AND queasy.number2 EQ dept NO-LOCK BY queasy.number2 BY queasy.number3:
    FIND FIRST h-artikel WHERE h-artikel.departement EQ dept AND h-artikel.artnr EQ queasy.number3 NO-LOCK NO-ERROR.
    FIND FIRST wgrpdep WHERE wgrpdep.departement EQ dept AND wgrpdep.zknr EQ h-artikel.zwkum NO-LOCK NO-ERROR.
    CREATE art-list.
    ASSIGN 
        art-list.vhp-artdept = queasy.number2    
        art-list.vhp-artnr   = queasy.number3    
        art-list.vhp-arttype = wgrpdep.bezeich      
        art-list.vhp-artname = queasy.char1  
        art-list.rms-arttype = queasy.char2
        art-list.rms-artname = queasy.char3.
END.
RELEASE queasy.
