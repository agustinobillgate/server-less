DEFINE TEMP-TABLE program-list
    FIELD prog-number       AS INT
    FIELD prog-hotel-code   AS CHAR
    FIELD prog-name         AS CHAR
    FIELD prog-title        AS CHAR
    FIELD prog-description  AS CHAR
    FIELD prog-type         AS INT
    FIELD prog-flag         AS LOGICAL
    FIELD prog-password     AS CHAR
    FIELD prog-hashpassword AS CHAR
    .

DEFINE INPUT PARAMETER prog-name        AS CHAR.
DEFINE INPUT PARAMETER prog-title       AS CHAR.
DEFINE INPUT PARAMETER prog-description AS CHAR.
DEFINE INPUT PARAMETER prog-type        AS INT.
DEFINE INPUT PARAMETER prog-flag        AS LOGICAL.
DEFINE INPUT PARAMETER case-type        AS INT.
DEFINE INPUT PARAMETER prog-number      AS INT.
DEFINE INPUT PARAMETER prog-hotel-code  AS CHAR.
DEFINE INPUT PARAMETER prog-password    AS CHAR.

DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR program-list.

DEFINE VARIABLE record-number AS INT.

/*prog-type 1=setting, 2=function, 3=report*/

IF case-type EQ 1 THEN /*ADD*/
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 268
        AND queasy.char1 EQ prog-hotel-code
        AND queasy.char2 EQ prog-name NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO:
        mess-result = "Program Already Exist".
    END.
    ELSE
    DO:
        FOR EACH queasy WHERE queasy.KEY EQ 268
            AND queasy.char1 EQ prog-hotel-code
            NO-LOCK BY queasy.number1 DESC:
            record-number = queasy.number1.
            LEAVE.
        END.
        IF record-number EQ 0 THEN record-number = 1.
        ELSE record-number = record-number + 1.

        CREATE queasy.
        ASSIGN
            queasy.KEY      = 268
            queasy.char1    = prog-hotel-code
            queasy.char2    = prog-name
            queasy.char3    = prog-title + "|" + prog-description + "|" + prog-password
            queasy.number1  = record-number
            queasy.number2  = prog-type
            queasy.logi1    = prog-flag
            .
        mess-result = "Add Program Success".
    END.
    RUN load-data.
END.
ELSE IF case-type EQ 2 THEN /*modify*/
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 268
        AND queasy.char1 EQ prog-hotel-code
        AND queasy.number1 EQ prog-number EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN 
    DO:
        mess-result = "Program Not Available".
    END.
    ELSE
    DO:
        ASSIGN
            queasy.char1    = prog-hotel-code
            queasy.char2    = prog-name
            queasy.char3    = prog-title + "|" + prog-description + "|" + prog-password
            queasy.number2  = prog-type
            queasy.logi1    = prog-flag
            .
        mess-result = "Modify Program Success".
    END.
    RUN load-data.
END.
ELSE IF case-type EQ 3 THEN /*delete*/
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 268
        AND queasy.char1 EQ prog-hotel-code
        AND queasy.number1 EQ prog-number EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN 
    DO:
        mess-result = "Program Not Available".
    END.
    ELSE
    DO:
        DELETE queasy.
        mess-result = "Delete Program Success".
    END.
    RUN load-data.
END.
ELSE IF case-type EQ 4 THEN /*load data*/
DO:
    RUN load-data.
    mess-result = "Load Data Success".
END.
ELSE IF case-type EQ 5 THEN /*load data*/
DO:
    RUN load-data-list.
    mess-result = "Load Data Success".
END.

PROCEDURE load-data:
    DEFINE VARIABLE rRawDataSHA AS RAW       NO-UNDO.
    DEFINE VARIABLE cHMACSHA    AS CHARACTER NO-UNDO.
    DEFINE VARIABLE strDate     AS CHARACTER NO-UNDO.
    DEFINE VARIABLE strPass     AS CHARACTER NO-UNDO.
    DEFINE VARIABLE strHtlCode  AS CHARACTER NO-UNDO.

    strDate = STRING(YEAR(TODAY),"9999") + STRING(MONTH(TODAY),"99") + STRING(DAY(TODAY),"99").

    FOR EACH queasy WHERE queasy.KEY EQ 268 AND queasy.char1 EQ prog-hotel-code NO-LOCK:
        
        IF NUM-ENTRIES(queasy.char3,"|") GE 3 THEN
        DO: 
            strHtlCode  = queasy.char1.
            strPass     = ENTRY(3,queasy.char3,"|"). 
            rRawDataSHA = MESSAGE-DIGEST('sha-256',strDate + strPass + strHtlCode,"").
            cHMACSHA    = HEX-ENCODE(rRawDataSHA).
        END.
        ELSE
        DO: 
            strPass     = "".
            cHMACSHA    = "".
        END.

        CREATE program-list.
        ASSIGN 
            program-list.prog-number       = queasy.number1
            program-list.prog-hotel-code   = queasy.char1  
            program-list.prog-name         = queasy.char2  
            program-list.prog-title        = ENTRY(1,queasy.char3,"|")  
            program-list.prog-description  = ENTRY(2,queasy.char3,"|") 
            program-list.prog-type         = queasy.number2
            program-list.prog-flag         = queasy.logi1
            program-list.prog-password     = strPass
            program-list.prog-hashpassword = cHMACSHA.
    END.
END.

PROCEDURE load-data-list:
    DEFINE VARIABLE rRawDataSHA AS RAW       NO-UNDO.
    DEFINE VARIABLE cHMACSHA    AS CHARACTER NO-UNDO.
    DEFINE VARIABLE strDate     AS CHARACTER NO-UNDO.
    DEFINE VARIABLE strPass     AS CHARACTER NO-UNDO.
    DEFINE VARIABLE strHtlCode  AS CHARACTER NO-UNDO.

    strDate = STRING(YEAR(TODAY),"9999") + STRING(MONTH(TODAY),"99") + STRING(DAY(TODAY),"99").

    FOR EACH queasy WHERE queasy.KEY EQ 268 AND queasy.char1 EQ prog-hotel-code NO-LOCK:
        
        IF NUM-ENTRIES(queasy.char3,"|") GE 3 THEN
        DO: 
            strHtlCode  = queasy.char1.
            strPass     = ENTRY(3,queasy.char3,"|"). 
            rRawDataSHA = MESSAGE-DIGEST('sha-256',strDate + strPass + strHtlCode,"").
            cHMACSHA    = HEX-ENCODE(rRawDataSHA).
        END.
        ELSE
        DO: 
            strPass     = "".
            cHMACSHA    = "".
        END.

        CREATE program-list.
        ASSIGN 
            program-list.prog-number       = queasy.number1
            program-list.prog-hotel-code   = queasy.char1  
            program-list.prog-name         = queasy.char2  
            program-list.prog-title        = ENTRY(1,queasy.char3,"|")  
            program-list.prog-description  = ENTRY(2,queasy.char3,"|") 
            program-list.prog-type         = queasy.number2
            program-list.prog-flag         = queasy.logi1
            program-list.prog-password     = ""
            program-list.prog-hashpassword = cHMACSHA.
    END.
END.
