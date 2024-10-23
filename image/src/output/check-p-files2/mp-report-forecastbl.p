DEFINE TEMP-TABLE t-raum
    FIELD nr        AS INTEGER
    FIELD raum      AS CHARACTER
    FIELD bezeich   AS CHARACTER
    FIELD forecast  AS DECIMAL.

DEFINE INPUT PARAMETER reportType       AS INTEGER.
/*DEFINE INPUT PARAMETER searchBy         AS INTEGER.
DEFINE INPUT PARAMETER searchValue      AS CHARACTER.
DEFINE INPUT PARAMETER searchDate1      AS DATE.
DEFINE INPUT PARAMETER searchDate2      AS DATE.*/
DEFINE OUTPUT PARAMETER TABLE FOR t-raum.

DEFINE VARIABLE forecast    AS DECIMAL      NO-UNDO.
DEFINE VARIABLE dayCount    AS INTEGER      NO-UNDO.

IF reportType EQ 3 THEN
DO:
    /*searchValue = "*" + searchValue + "*".*/
    
    FOR EACH bk-raum:
        CREATE t-raum.
        ASSIGN
            t-raum.raum     = bk-raum.raum
            t-raum.bezeich  = bk-raum.bezeich.    
    END.
    
    FOR EACH bk-event-detail /*WHERE bk-event-detail.start-date GE searchDate1 
        AND bk-event-detail.start-date LE searchDate2*/:
        
        dayCount = bk-event-detail.end-date - bk-event-detail.start-date + 1.
        
        FIND FIRST t-raum WHERE t-raum.bezeich EQ bk-event-detail.venue EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE t-raum THEN
        DO:
            forecast = bk-event-detail.atendees * bk-event-detail.amount.
            ASSIGN 
                t-raum.forecast = (t-raum.forecast + forecast) * dayCount.
        END.    
    END.        
END.
ELSE IF reportType EQ 4 THEN
DO:
    /*searchValue = "*" + searchValue + "*".*/
    
    FOR EACH bk-queasy WHERE bk-queasy.key EQ 5 NO-LOCK:
        CREATE t-raum.
        ASSIGN
            t-raum.nr       = bk-queasy.number1
            t-raum.raum     = bk-queasy.char1
            t-raum.bezeich  = bk-queasy.char2
            t-raum.forecast = 0.
    END.
    
    FOR EACH t-raum:
        FIND FIRST bk-master WHERE bk-master.restype EQ t-raum.nr NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE bk-master:
            FIND FIRST bk-event-detail WHERE bk-event-detail.block-id EQ bk-master.block-id
                /*AND bk-event-detail.start-date GE searchDate1
                AND bk-event-detail.start-date LE searchDate2*/ NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE bk-event-detail:
                forecast = bk-event-detail.atendees * bk-event-detail.amount.
                
                ASSIGN  
                    t-raum.forecast = t-raum.forecast + forecast.
                
                FIND NEXT bk-event-detail WHERE bk-event-detail.block-id EQ bk-master.block-id NO-LOCK NO-ERROR.
            END.
            
            FIND NEXT bk-master WHERE bk-master.restype EQ t-raum.nr NO-LOCK NO-ERROR.        
        END.
    END.        
END.
/*
IF searchBy EQ 1 THEN
DO:
    FOR EACH t-raum WHERE NOT t-raum.raum MATCHES searchValue:
        DELETE t-raum.
    END.        
END.
ELSE IF searchBy EQ 2 THEN
DO:
    FOR EACH t-raum WHERE NOT t-raum.bezeich MATCHES searchValue:
        DELETE t-raum.
    END.    
END.
ELSE IF searchBy EQ 3 THEN
DO:
    FOR EACH t-raum WHERE NOT STRING(t-raum.forecast) MATCHES searchValue:
        DELETE t-raum.
    END.        
END.
*/
