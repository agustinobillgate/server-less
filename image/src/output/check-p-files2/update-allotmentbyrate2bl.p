DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER allotment AS INT.
DEFINE INPUT PARAMETER inp-str   AS CHAR.
DEFINE INPUT PARAMETER rmtype    AS CHAR.

DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE cat-flag AS LOGICAL INIT NO.
DEFINE VARIABLE i-typ AS INT.
DEFINE VARIABLE currcode AS CHAR.
DEFINE VARIABLE user-init AS CHAR.
DEFINE VARIABLE created AS LOGICAL INIT NO.
DEFINE VARIABLE avail-qsy AS LOGICAL INIT NO.

IF NUM-ENTRIES(inp-str,";") GT 1 THEN
    ASSIGN
        currcode = ENTRY(1,inp-str,";")
        user-init = ENTRY(2,inp-str,";").
ELSE currcode = inp-str.

FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.char1 = rmtype NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN i-typ = queasy.number1.
ELSE IF NOT AVAILABLE queasy THEN
DO:
    FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmtype NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN i-typ = zimkateg.zikatnr.
END.



DO datum = from-date TO to-date:
    avail-qsy = NO.
    IF user-init NE "" THEN
    DO:
        created = YES.
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        CREATE res-history. 
        ASSIGN 
            res-history.nr     = bediener.nr 
            res-history.datum  = TODAY 
            res-history.zeit   = TIME 
            res-history.action = "AllotmentByRateCode"
        . 
    END.

    IF allotment NE 0 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 = currcode
            AND queasy.date1 = datum AND queasy.number1 = i-typ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.number3 NE allotment THEN
        DO:
            IF user-init NE "" THEN
                res-history.aenderung = "RCode:" + currcode + ",Rmtype:" + rmtype + 
                    "Date: " + STRING(YEAR(datum),"9999") + STRING(MONTH(datum),"99") +
                    STRING(DAY(datum),"99") + "," + STRING(queasy.number3) + "ChangeTo" + STRING(allotment).
        
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN
                queasy.number3 = allotment
                queasy.logi3 = YES.
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
        END.
        ELSE IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY = 171
                queasy.char1 = currcode
                queasy.number1 = i-typ
                queasy.number3 = allotment
                queasy.date1 = datum
                queasy.logi1 = YES
                queasy.logi3 = YES.
    
            IF user-init NE "" THEN
                res-history.aenderung = "RCode:" + currcode + ",Rmtype:" + rmtype + 
                    "Date: " + STRING(YEAR(datum),"9999") + STRING(MONTH(datum),"99") +
                    STRING(DAY(datum),"99") + ",All ChangeTo" + STRING(allotment).
        END.
    END.
    ELSE IF allotment = 0 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 = currcode
            AND queasy.date1 = datum AND queasy.number1 = i-typ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.number3 NE allotment THEN
        DO:
            avail-qsy = YES.
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            DELETE queasy.
            RELEASE queasy.
        END.


        IF avail-qsy THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 = ""
                AND queasy.date1 = datum AND queasy.number1 = i-typ NO-LOCK NO-ERROR.
            IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO 
                AND queasy.logi3 = NO THEN
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN
                    queasy.logi3 = YES.
                FIND CURRENT queasy NO-LOCK.
                RELEASE queasy.
            END.  
        END.      
    END.                   
END.
