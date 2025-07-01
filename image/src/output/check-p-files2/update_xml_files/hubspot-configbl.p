DEFINE TEMP-TABLE hubspot-param
    FIELD nr          AS INTEGER   FORMAT ">>9"   LABEL "No"
    FIELD param-name  AS CHARACTER FORMAT "x(50)" LABEL "Param Name"
    FIELD param-value AS CHARACTER FORMAT "x(50)" LABEL "Param Value".

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR hubspot-param.

RUN create-queasy.
IF case-type EQ 1 THEN
DO:
    FOR EACH hubspot-param:
        FIND FIRST queasy WHERE queasy.KEY EQ 319 AND queasy.number1 EQ hubspot-param.nr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN 
                queasy.char2 = hubspot-param.param-value.
        END.
    END.
END.
FOR EACH queasy WHERE queasy.KEY EQ 319 NO-LOCK:
    CREATE hubspot-param.
    ASSIGN 
        hubspot-param.nr          = queasy.number1 
        hubspot-param.param-name  = queasy.char1   
        hubspot-param.param-value = queasy.char2 .  
END.

PROCEDURE create-queasy:
    DEF VAR paramnr AS INT.

    paramnr = 1.
    FIND FIRST queasy WHERE queasy.KEY EQ 319 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "Hubspot URL"
            queasy.char2    = "" 
            .  
    END.
    paramnr = 2.
    FIND FIRST queasy WHERE queasy.KEY EQ 319 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "Hubspot Secret Key"
            queasy.char2    = "" 
            .  
    END.
END.

