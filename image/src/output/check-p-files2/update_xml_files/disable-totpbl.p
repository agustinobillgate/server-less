DEFINE TEMP-TABLE value-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD value-str AS CHAR FORMAT "x(20)".

DEFINE TEMP-TABLE signature-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD signature AS CHAR FORMAT "x(40)".

DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER user-init-will-disable AS CHAR.
DEFINE INPUT PARAMETER userOTP AS CHARACTER.
DEFINE INPUT PARAMETER reason AS CHARACTER.
DEFINE OUTPUT PARAMETER result-message AS CHARACTER.
DEFINE OUTPUT PARAMETER totpOK AS LOGICAL INIT FALSE.
DEFINE OUTPUT PARAMETER epoch-signature AS INT64.
DEFINE OUTPUT PARAMETER TABLE FOR signature-list.

/*
DEFINE VARIABLE secretKey AS CHARACTER NO-UNDO INIT "3NQAJIILLKSLAOAO".
DEFINE VARIABLE userOTP AS CHARACTER NO-UNDO INIT "394412".
DEFINE VARIABLE totp AS LOGICAL NO-UNDO INIT FALSE.
*/

DEFINE VARIABLE secretKey     AS CHARACTER NO-UNDO.
DEFINE VARIABLE generatedOTP  AS CHARACTER NO-UNDO.
DEFINE VARIABLE cmd           AS CHARACTER NO-UNDO.
DEFINE VARIABLE result        AS CHARACTER NO-UNDO.
DEFINE VARIABLE returnStatus  AS INTEGER NO-UNDO.
DEFINE VARIABLE foldername    AS CHARACTER NO-UNDO.
DEFINE VARIABLE filename      AS CHARACTER NO-UNDO.

DEFINE BUFFER opr-bediener FOR bediener.
DEFINE BUFFER terminate-totp FOR queasy.

IF (reason EQ "" OR reason EQ ?) THEN
DO:
    result-message = "Reason Is Mandatory!".
    RETURN.
END.

FIND FIRST bediener WHERE bediener.userinit EQ user-init-will-disable NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO:
    IF bediener.username MATCHES "*sindata*" THEN
    DO:
        totpOK = NO.
        CREATE value-list.
        ASSIGN
            value-list.var-name  = "totpOK"
            value-list.value-str = STRING(totpOK).
        
        RUN create-signature(bediener.username, TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
        result-message = "Not Allowed Procedure".
        RETURN.
    END.
END.
RELEASE bediener.

FIND FIRST opr-bediener WHERE opr-bediener.userinit EQ user-init NO-LOCK NO-ERROR.
IF AVAILABLE opr-bediener THEN
DO:
    IF opr-bediener.username MATCHES "*sindata*" THEN
    DO:
        totpOK = YES.
        FIND FIRST bediener WHERE bediener.userinit EQ user-init-will-disable NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ 341 AND queasy.char1 EQ bediener.username NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN 
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                DELETE queasy.

                CREATE res-history.
                ASSIGN 
                  res-history.nr        = opr-bediener.nr
                  res-history.datum     = TODAY
                  res-history.zeit      = TIME
                  res-history.aenderung = "Disable TOTP For User: " + bediener.username + " Reason: " + reason
                  res-history.action    = "User".

                result-message = "TOTP Disable Succesfull".
            END.
            ELSE
            DO:
                result-message = "TOTP Already Disabled".
            END.
            CREATE value-list.
            ASSIGN
                value-list.var-name  = "totpOK"
                value-list.value-str = STRING(totpOK).
                
            RUN create-signature(opr-bediener.username, TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
        END.
    END.
    ELSE
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 341 AND queasy.char1 EQ opr-bediener.username NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN 
        DO:
            totpOK = NO.
            CREATE value-list.
            ASSIGN
                value-list.var-name  = "totpOK"
                value-list.value-str = STRING(totpOK).
            
            RUN create-signature(opr-bediener.username, TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
            result-message = "TOTP Not Configured".
            RETURN.
        END.
        ELSE
        DO:
            secretKey = queasy.char2.
            filename  = "check_totp_" + userOTP + ".txt".
            
            /* Construct the command to generate the expected OTP */
            IF OPSYS EQ "WIN32" THEN
            DO:
                cmd = "wsl oathtool --totp -b " + secretKey + " > " + filename.
                OS-COMMAND SILENT VALUE(cmd).
            END.
            ELSE
            DO:
                foldername = "/usr1/vhp/tmp/totp/".
                UNIX SILENT VALUE("mkdir /usr1/vhp").
                UNIX SILENT VALUE("mkdir /usr1/vhp/tmp").
                UNIX SILENT VALUE("mkdir " + foldername).
            
                filename = foldername + filename.
                cmd = "oathtool --totp -b " + secretKey + " > " + filename.
                /* Run the command and capture the result */
                UNIX SILENT VALUE(cmd).
            
                /* Read the OTP from the file */
                INPUT FROM VALUE(filename).
                IMPORT UNFORMATTED result.
                INPUT CLOSE.
                    
                OS-DELETE VALUE(filename).
                
                /* Trim whitespace from result */
                result = TRIM(result).
                    
                /* Compare user input with generated OTP */
                IF userOTP EQ result THEN 
                DO:
                    totpOK = YES.
                    FIND FIRST bediener WHERE bediener.userinit EQ user-init-will-disable NO-LOCK NO-ERROR.
                    IF AVAILABLE bediener THEN
                    DO:
                        FIND FIRST queasy WHERE queasy.KEY EQ 341 AND queasy.char1 EQ bediener.username NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN 
                        DO:
                            FIND CURRENT queasy EXCLUSIVE-LOCK.
                            DELETE queasy.
    
                            CREATE res-history.
                            ASSIGN 
                              res-history.nr        = opr-bediener.nr
                              res-history.datum     = TODAY
                              res-history.zeit      = TIME
                              res-history.aenderung = "Disable TOTP For User: " + bediener.username + " Reason: " + reason
                              res-history.action    = "User".
    
                            result-message = "TOTP Disable Succesfull".
                        END.
                        ELSE
                        DO:
                            result-message = "TOTP Already Disabled".
                        END.
                    END.
                END.
                ELSE
                DO:
                    result-message = "TOTP Not Match".
                END.
        
                CREATE value-list.
                ASSIGN
                    value-list.var-name  = "totpOK"
                    value-list.value-str = STRING(totpOK).
                
                RUN create-signature(opr-bediener.username, TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
            END.
        END.
    END.
END.
ELSE
DO:
    totpOK = NO.
    result-message = "User Not Found!".
    CREATE value-list.
    ASSIGN
        value-list.var-name  = "totpOK"
        value-list.value-str = STRING(totpOK).
    
    RUN create-signature("", TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
    RETURN.
END.

  
PROCEDURE create-signature:
    DEF INPUT PARAMETER user-name AS CHAR.
    DEF INPUT PARAMETER TABLE FOR value-list.
    DEF OUTPUT PARAMETER epoch AS INT64.
    DEF OUTPUT PARAMETER TABLE FOR signature-list.

    DEF VAR dtz1      AS DATETIME-TZ.
    DEF VAR dtz2      AS DATETIME-TZ.
    DEF VAR lic-nr    AS CHAR.
    DEF VAR data      AS CHAR.
    DEF VAR value-str AS CHAR.

    FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
    RUN decode-string(ptexte, OUTPUT lic-nr). 

    dtz1 = NOW.
    dtz2 = 1970-01-01T00:00:00.000+0:00.

    epoch = INTERVAL(dtz1, dtz2, "milliseconds").

    FOR EACH value-list:
        value-str = LC(value-list.value-str).

        CASE value-str:
            WHEN "yes" THEN value-str = "true".
            WHEN "no" THEN value-str = "false".
        END CASE.

        data = value-str + "-" + STRING(epoch) + "-" + STRING(lic-nr) + "-" + LC(user-name).

        CREATE signature-list.
        signature-list.var-name = value-list.var-name.
        signature-list.signature = HEX-ENCODE(SHA1-DIGEST(data)).
    END.
END.

PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
    s = in-str. 
    j = ASC(SUBSTR(s, 1, 1)) - 70. 
    len = LENGTH(in-str) - 1. 
    s = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END. 
