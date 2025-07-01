/*MCH Oct 20, 2024 => Ticket 52E28C - Add case-type 2 for Load Settings*/

DEFINE TEMP-TABLE kds-param
    FIELD nr          AS INTEGER   FORMAT ">>9"   LABEL "No"
    FIELD param-name  AS CHARACTER FORMAT "x(50)" LABEL "Param Name"
    FIELD param-value AS CHARACTER FORMAT "x(50)" LABEL "Param Value".

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR kds-param.

RUN create-queasy.
IF case-type EQ 1 THEN
DO:
    FOR EACH kds-param:
        FIND FIRST queasy WHERE queasy.KEY EQ 320 AND queasy.number1 EQ kds-param.nr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN 
                queasy.char2 = kds-param.param-value.
            FIND CURRENT queasy NO-LOCK.
        END.
    END.
END.
IF case-type EQ 2 THEN
DO:
	FIND FIRST queasy WHERE queasy.KEY EQ 320  AND queasy.number1 EQ 1 NO-LOCK NO-ERROR.
	IF queasy.char2 EQ "" THEN
	DO:
        CREATE kds-param.
		ASSIGN 
			kds-param.nr          = 0 
			kds-param.param-name  = "error"   
			kds-param.param-value = "KDS not configured yet, please setting up first.".
		RETURN.
	END.
END.

FOR EACH queasy WHERE queasy.KEY EQ 320 NO-LOCK:
    CREATE kds-param.
    ASSIGN 
        kds-param.nr          = queasy.number1 
        kds-param.param-name  = queasy.char1   
        kds-param.param-value = queasy.char2 .  
END.

PROCEDURE create-queasy:
    DEF VAR paramnr AS INT.

    paramnr = 1.
    FIND FIRST queasy WHERE queasy.KEY EQ 320 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "KDS Refresh Interval (In Second)"
            queasy.char2    = "" 
            .  
    END.
    paramnr = 2.
    FIND FIRST queasy WHERE queasy.KEY EQ 320 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "KDS Timeout Refresh Interval (In Second)"
            queasy.char2    = "" 
            .  
    END.
    paramnr = 3.
    FIND FIRST queasy WHERE queasy.KEY EQ 320 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "Interval Cooking Time 1 [Green](In Minute)"
            queasy.char2    = "" 
            .  
    END.
    paramnr = 4.
    FIND FIRST queasy WHERE queasy.KEY EQ 320 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "Interval Cooking Time 2 [Yellow](In Minute)"
            queasy.char2    = "" 
            .  
    END.
    paramnr = 5.
    FIND FIRST queasy WHERE queasy.KEY EQ 320 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "Interval Cooking Time 3 [Red](In Minute)"
            queasy.char2    = "" 
            .  
    END.
    paramnr = 6.
    FIND FIRST queasy WHERE queasy.KEY EQ 320 AND queasy.number1 EQ paramnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 320
            queasy.number1  = paramnr
            queasy.char1    = "Sound Notification (Max 200kb)"
            queasy.char2    = "" 
            .  
    END.
END.
