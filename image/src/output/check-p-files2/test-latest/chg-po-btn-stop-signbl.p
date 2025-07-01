DEFINE TEMP-TABLE q245
    FIELD KEY       AS INTEGER
    FIELD docu-nr   AS CHARACTER
    FIELD user-init AS CHARACTER
    FIELD app-id    AS CHARACTER
    FIELD app-no    AS INTEGER
    FIELD sign-id   AS INTEGER.

DEFINE INPUT PARAMETER docu-nr AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR q245.

FOR EACH queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ docu-nr EXCLUSIVE-LOCK:
    DELETE queasy.
END.
FOR EACH q245 NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY EQ q245.KEY AND queasy.char1 EQ q245.docu-nr AND queasy.number1 EQ q245.app-no EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = q245.KEY
            queasy.char1    = q245.docu-nr 
            queasy.char2    = q245.user-init
            queasy.char3    = q245.app-id
            queasy.number1  = q245.app-no
            queasy.number2  = q245.sign-id.
    END.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN  
            queasy.char2    = q245.user-init
            queasy.char3    = q245.app-id
            queasy.number1  = q245.app-no
            queasy.number2  = q245.sign-id.
    END.
END.
