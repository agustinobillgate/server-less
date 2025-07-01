DEFINE TEMP-TABLE value-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD value-str AS CHAR FORMAT "x(20)".

DEFINE TEMP-TABLE signature-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD signature AS CHAR FORMAT "x(40)".

DEFINE INPUT PARAMETER user-name AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER hotel-code AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER totpURI AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER recoveryCode AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER epoch-signature AS INT64.
DEFINE OUTPUT PARAMETER TABLE FOR signature-list.

/*
DEFINE VARIABLE accountName AS CHARACTER NO-UNDO.
DEFINE VARIABLE totpSecret AS CHARACTER NO-UNDO.
DEFINE VARIABLE totpURI AS CHARACTER NO-UNDO.
DEFINE VARIABLE recoveryCode AS CHARACTER NO-UNDO.
*/

DEFINE VARIABLE base32Chars AS CHARACTER NO-UNDO.
DEFINE VARIABLE randomByte  AS INTEGER NO-UNDO.
DEFINE VARIABLE i           AS INTEGER NO-UNDO.
DEFINE VARIABLE issuer      AS CHARACTER NO-UNDO INIT "VHP".
DEFINE VARIABLE algorithm   AS CHARACTER NO-UNDO.
DEFINE VARIABLE digits      AS INTEGER NO-UNDO.
DEFINE VARIABLE period      AS INTEGER NO-UNDO.
DEFINE VARIABLE totpSecret  AS CHARACTER NO-UNDO.

/* Base32 character set */
base32Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567".

/* Initialize the secret */
totpSecret = "".

/* Generate a 16-character TOTP secret */
DO i = 1 TO 16:
    /* Generate a random number between 0 and 31 (Base32 index) */
    randomByte = RANDOM(0, 31).
    
    /* Append the corresponding Base32 character */
    totpSecret = totpSecret + SUBSTRING(base32Chars, randomByte + 1, 1).
END.

/* Generate a 16-character Recovery Code */
DO i = 1 TO 16:
    /* Generate a random number between 0 and 31 (Base32 index) */
    randomByte = RANDOM(0, 31).
    
    /* Append the corresponding Base32 character */
    recoveryCode = recoveryCode + SUBSTRING(base32Chars, randomByte + 1, 1).
END.


/* Define TOTP parameters */
algorithm = "SHA1". /* Standard TOTP algorithm */
digits = 6. /* Default is 6-digit OTP */
period = 30. /* OTP refreshes every 30 seconds */

/* Construct the TOTP URI manually */
totpURI = "otpauth://totp/" + user-name + "@" + hotel-code
          + "?secret=" + totpSecret
          + "&issuer=" + issuer
          + "&algorithm=" + algorithm
          + "&digits=" + STRING(digits)
          + "&period=" + STRING(period).


FIND FIRST bediener WHERE bediener.username EQ user-name NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 341 AND queasy.char1 EQ bediener.username NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY     = 341 
            queasy.char1   = bediener.username
            queasy.char2   = totpSecret
            queasy.char3   = ""
            queasy.logi1   = NO
            queasy.number2 = TIME
            queasy.date2   = TODAY.

        CREATE res-history.
        ASSIGN 
          res-history.nr        = bediener.nr
          res-history.datum     = TODAY
          res-history.zeit      = TIME
          res-history.aenderung = "Create Two-Factor Authentication"
          res-history.action    = "User".
    END.
    ELSE
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        queasy.char2 = totpSecret.
        queasy.logi1 = NO.
        FIND CURRENT queasy NO-LOCK.
    END.
    RELEASE queasy.

    CREATE value-list.
    ASSIGN
        value-list.var-name  = "totpURI"
        value-list.value-str = totpURI.
    
    RUN create-signature(bediener.username,TABLE value-list, OUTPUT epoch-signature,OUTPUT TABLE signature-list).
END.
/* Display the generated TOTP secret and URI */
/*
MESSAGE "Generated TOTP Secret: " totpSecret SKIP
        "TOTP URI: " totpURI SKIP
        "Recovery Code:"  recoveryCode VIEW-AS ALERT-BOX.
*/

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
