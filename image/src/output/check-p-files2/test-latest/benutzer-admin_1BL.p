
DEF TEMP-TABLE t-bediener LIKE bediener.
DEF TEMP-TABLE t-queasy   LIKE queasy.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER mphone    AS CHAR.
DEF INPUT PARAMETER email     AS CHAR.
DEF INPUT PARAMETER pager     AS CHAR.
/*IF - 160719 [67222F - Iqbal]*/
DEFINE INPUT PARAMETER userInit AS CHARACTER.
/*END IF*/
DEF INPUT PARAMETER TABLE FOR t-bediener.
DEF INPUT PARAMETER TABLE FOR t-queasy.

IF case-type = 1 THEN
DO:
    FIND FIRST t-bediener NO-ERROR.
    IF AVAILABLE t-bediener THEN
    DO:
        CREATE bediener.
        BUFFER-COPY t-bediener TO bediener.
    END.

    FIND FIRST t-queasy NO-ERROR.
    IF AVAILABLE t-queasy THEN
    DO:
        CREATE queasy.
        BUFFER-COPY t-queasy TO queasy.
    END.

/*IF - 160719 [67222F - Iqbal]*/    
    FIND FIRST bediener WHERE bediener.userinit EQ userInit NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN 
    DO:
    CREATE res-history.
    ASSIGN
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "User"
        res-history.aenderung   = "Create New User For " + t-bediener.username.
    END.
/*END IF*/    
END.
ELSE
DO:
    FIND FIRST t-bediener NO-ERROR.
    IF AVAILABLE t-bediener THEN
    DO:
        FIND FIRST bediener WHERE bediener.nr = t-bediener.nr 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            BUFFER-COPY t-bediener TO bediener.
            RELEASE bediener.
        END.
    END.

    FIND FIRST queasy WHERE queasy.KEY = 134 AND queasy.number1 = 
        t-bediener.nr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN 
    DO:
        CREATE queasy.
        ASSIGN queasy.KEY = 134.
    END.
    ELSE
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
    END.
    ASSIGN
        queasy.number1 = t-bediener.nr
        queasy.char1   = mphone
        queasy.char2   = email
        queasy.char3   = pager.
    FIND CURRENT queasy NO-LOCK.
    
/*IF - 160719 [67222F - Iqbal]*/    
    FIND FIRST bediener WHERE bediener.userinit EQ userInit NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN 
    DO:
    CREATE res-history.
    ASSIGN
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "User"
        res-history.aenderung   = "Update User Data For " + t-bediener.username.
    END.
/*END IF*/        
END.
