DEFINE TEMP-TABLE value-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD value-str AS CHAR FORMAT "x(20)".

DEFINE TEMP-TABLE signature-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD signature AS CHAR FORMAT "x(40)".

DEFINE INPUT PARAMETER username  AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER userOTP AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER checking-flag AS INT NO-UNDO.
DEFINE OUTPUT PARAMETER totpOK AS LOGICAL NO-UNDO INIT FALSE.
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


FIND FIRST bediener WHERE bediener.username EQ username NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 341 AND queasy.char1 EQ bediener.username NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN 
    DO:
        totpOK = NO.
        CREATE value-list.
        ASSIGN
            value-list.var-name  = "totpOK"
            value-list.value-str = STRING(totpOK).
        
        RUN create-signature(bediener.username, TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
        RETURN.
    END.
    ELSE
    DO:
        IF checking-flag EQ 3 THEN
        DO:
            IF queasy.logi1 EQ YES THEN totpOK = YES.
            ELSE totpOK = NO.
        END.
        ELSE
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
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
            END.
            
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
                IF checking-flag EQ 1 THEN
                DO:
                    totpOK = YES.
                    queasy.logi1 = YES.

                    CREATE res-history.
                    ASSIGN 
                      res-history.nr        = bediener.nr
                      res-history.datum     = TODAY
                      res-history.zeit      = TIME
                      res-history.aenderung = "Activate Two-Factor Authentication"
                      res-history.action    = "User".
                END.
                ELSE IF checking-flag EQ 2 THEN
                DO:
                    totpOK = YES.
                    DELETE queasy.

                    CREATE res-history.
                    ASSIGN 
                      res-history.nr        = bediener.nr
                      res-history.datum     = TODAY
                      res-history.zeit      = TIME
                      res-history.aenderung = "Deactivate Two-Factor Authentication"
                      res-history.action    = "User".
                END.
            END.
            /*ELSE
            DO:
                IF checking-flag EQ 2 THEN
                DO:
                    IF userOTP EQ queasy.char3 AND TODAY EQ queasy.date1 AND TIME LE queasy.number1 THEN
                    DO:
                        totp = YES.
                        DELETE queasy.
                    END.
                END.
            END.*/
        END.
        CREATE value-list.
        ASSIGN
            value-list.var-name  = "totpOK"
            value-list.value-str = STRING(totpOK).
        
        RUN create-signature(bediener.username, TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).

    END.
END.
ELSE
DO:
    totpOK = NO.
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
