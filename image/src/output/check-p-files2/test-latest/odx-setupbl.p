DEFINE TEMP-TABLE t-param
    FIELD number    AS INTEGER   FORMAT ">>9"    LABEL "No"
    FIELD bezeich   AS CHARACTER FORMAT "x(40)"  LABEL "Description"
    FIELD val       AS CHARACTER FORMAT "x(200)" LABEL "Value".

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-param.

IF case-type EQ 1 THEN /*PREPARE*/
DO :
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 1
            queasy.char1    = "Main Url"
            queasy.char3    = ""
            .
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 2 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 2
            queasy.char1    = "Client ID"
            queasy.char3    = ""
            .
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 3 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 3
            queasy.char1    = "Client Secret"
            queasy.char3    = ""
            .
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 4 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 4
            queasy.char1    = "Cookie"
            queasy.char3    = ""
            .
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 5 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 5
            queasy.char1    = "Property Code"
            queasy.char3    = ""
            .
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 6 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 6
            queasy.char1    = "Terminal ID"
            queasy.char3    = ""
            .
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 7 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 7
            queasy.char1    = "PMS ID"
            queasy.char3    = ""
            .
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 8 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 242
            queasy.number1  = 8
            queasy.char1    = "Logfile Path"
            queasy.char3    = ""
            .
    END.
END.
ELSE IF case-type EQ 2 THEN /*"UPDATE"*/
DO:
    DEF VAR before AS CHAR.
    FOR EACH t-param BY t-param.number:
        FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ t-param.number EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            IF queasy.char3 NE t-param.val THEN
            DO:
                before = queasy.char3.
                ASSIGN queasy.char3 = t-param.val.

                FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
                CREATE res-history. 
                ASSIGN 
                    res-history.nr        = bediener.nr  
                    res-history.action    = "ODX Setup"
                    res-history.datum     = TODAY 
                    res-history.zeit      = TIME 
                    res-history.aenderung = "Changes From: " + before + " To: " + t-param.val.
            END.
        END.
    END.
END.
EMPTY TEMP-TABLE t-param.
FOR EACH queasy WHERE queasy.KEY EQ 242 AND queasy.number1 NE 99 NO-LOCK BY number1:
    CREATE t-param.
    ASSIGN 
        t-param.number  = queasy.number1 
        t-param.bezeich = queasy.char1 
        t-param.val     = queasy.char3. 
END.
