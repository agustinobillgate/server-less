USING PROGRESS.Json.ObjectModel.JsonArray.
USING PROGRESS.Json.ObjectModel.JsonObject.

DEFINE INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER user-code    AS CHAR NO-UNDO. /*encoded pswd */
DEFINE INPUT PARAMETER license-nr   AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER master-key   AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER user-token  AS CHAR NO-UNDO INIT "".

DEFINE VARIABLE oJsonArray         AS JsonArray  NO-UNDO.
DEFINE VARIABLE oJsonObjectHeader  AS JsonObject NO-UNDO.
DEFINE VARIABLE oJsonObjectPayload AS JsonObject NO-UNDO.
DEFINE VARIABLE tokenSignature     AS CHAR       NO-UNDO.

DEFINE VARIABLE secret AS CHARACTER NO-UNDO.
DEFINE VARIABLE token  AS CHARACTER NO-UNDO.

DEFINE VARIABLE headerString  AS CHARACTER.
DEFINE VARIABLE payloadString AS CHARACTER.

DEFINE VARIABLE rawHeader  AS RAW.
DEFINE VARIABLE rawPayload AS RAW.

DEFINE VARIABLE user-pswd AS CHAR NO-UNDO.
DEFINE VARIABLE username  AS CHAR NO-UNDO.
    
DEFINE VARIABLE i AS INT.

FUNCTION BinaryXOR RETURNS INTEGER
    (INPUT intOperand1 AS INTEGER,
    INPUT intOperand2 AS INTEGER):

    DEFINE VARIABLE iByteLoop  AS INTEGER NO-UNDO.
    DEFINE VARIABLE iXOResult  AS INTEGER NO-UNDO.
    DEFINE VARIABLE lFirstBit  AS LOGICAL NO-UNDO.
    DEFINE VARIABLE lSecondBit AS LOGICAL NO-UNDO.

    iXOResult = 0.

    /*spin through each byte of each char*/
    DO iByteLoop = 0 TO 7: /* as processing a single byte character */

        /*find state (true / false) of each integer's byte*/
        ASSIGN
            lFirstBit  = GET-BITS(intOperand1,iByteLoop + 1,1) = 1
            lSecondBit = GET-BITS(intOperand2,iByteLoop + 1,1) = 1.

        /* XOR each bit*/
        IF (lFirstBit AND NOT lSecondBit) OR
            (lSecondBit AND NOT lFirstBit) THEN
            iXOResult = iXOResult + EXP(2, iByteLoop).
    END.

    RETURN iXOResult.
END FUNCTION. /*End function of BinaryXOR */
    
FUNCTION HMAC-BASE64 RETURN CHARACTER 
        (INPUT pcSHA AS CHARACTER,
        INPUT pcKey AS CHARACTER, 
        INPUT pcData AS CHARACTER):
    
        DEFINE VARIABLE mKeyOpad       AS MEMPTR    NO-UNDO.
        DEFINE VARIABLE mKeyIpad       AS MEMPTR    NO-UNDO.
        DEFINE VARIABLE mData          AS MEMPTR    NO-UNDO.
        DEFINE VARIABLE mKey           AS MEMPTR    NO-UNDO.
        DEFINE VARIABLE mInnerCombined AS MEMPTR    NO-UNDO.
        DEFINE VARIABLE mOuterCombined AS MEMPTR    NO-UNDO.
        DEFINE VARIABLE iBytePos       AS INTEGER   NO-UNDO.
        DEFINE VARIABLE iOpad          AS INTEGER   NO-UNDO.
        DEFINE VARIABLE iIpad          AS INTEGER   NO-UNDO.
        DEFINE VARIABLE iKey           AS INTEGER   NO-UNDO.
        DEFINE VARIABLE iTimeTaken     AS INTEGER   NO-UNDO.
        DEFINE VARIABLE rRawDataSHA    AS RAW       NO-UNDO.
        DEFINE VARIABLE cHMACSHA       AS CHARACTER NO-UNDO.
    
        &SCOPED-DEFINE xiBlockSize  64
    
        SET-SIZE(mKey)     = 0.
        SET-SIZE(mKeyOpad) = 0.
        SET-SIZE(mKeyIpad) = 0.
        SET-SIZE(mKey)     = {&xiBlockSize}.
        SET-SIZE(mKeyOpad) = {&xiBlockSize}.
        SET-SIZE(mKeyIpad) = {&xiBlockSize}.
    
        DO iBytePos = 1 TO {&xiBlockSize}:
            PUT-BYTES(mKey,     iBytePos) = HEX-DECODE("00":U).  /* 64 bytes of zeros 0x00*/
            PUT-BYTES(mKeyOpad, iBytePos) = HEX-DECODE("5C":U).  /* 64 bytes of 0x5C (92 dec,  "/" ascii) */
            PUT-BYTES(mKeyIpad, iBytePos) = HEX-DECODE("36":U).  /* 64 bytes of 0x36 (54 dec, "6" ascii)*/
        END.
    
        /* correction by Valery A.Eliseev */
        IF LENGTH(pcKey) > {&xiBlockSize} THEN 
        DO:
            set-size(mData) = LENGTH(pcKey).
            put-string(mData, 1, LENGTH(pcKey)) = pcKey.
            rRawDataSHA = SHA1-DIGEST(mData).
            PUT-BYTES(mKey, 1) = rRawDataSHA.
        END.
        ELSE
            /* end of correction */
    
            PUT-STRING(mKey, 1, LENGTH(pckey))  = pcKey. 
    
        DO iBytePos = 1 TO {&xiBlockSize}:
    
            ASSIGN
                iKey  = GET-BYTE(mKey,     iBytePos)
                iOpad = GET-BYTE(mKeyOpad, iBytePos)
                iIpad = GET-BYTE(mKeyIpad, iBytePos).
    
            /* The inner key, mKeyIpad is formed from mKey by XORing each byte with 0x36.. */
            PUT-BYTE(mKeyIpad, iBytePos) = BinaryXOR(INPUT iKey, 
                INPUT iIpad).
    
            /* The inner key, mKeyOpad is formed from mKey by XORing each byte with 0x5C. */
            PUT-BYTE(mKeyOpad, iBytePos) = BinaryXOR(INPUT iKey, 
                INPUT iOpad).
    
        END.
    
        SET-SIZE(mKey)  = 0.
        SET-SIZE(mData) = 0.
        SET-SIZE(mData) = LENGTH(pcData).
        PUT-STRING(mData,1,LENGTH(pcData)) = pcData.
    
    
        /* Inner Loop*/
        SET-SIZE(mInnerCombined)      = GET-SIZE(mKeyIpad) + GET-SIZE(mData).
    
        PUT-BYTES(mInnerCombined, 1)  = mKeyIpad.
        SET-SIZE(mKeyIpad) = 0.
    
        /*Append the data the end of the block size.*/
        PUT-BYTES(mInnerCombined, {&xiBlockSize} + 1) = mData.
    
        /* Deallocates any memory. */
        SET-SIZE(mData) = 0.
    
        /* Get the results of the SHA Digest.*/
        CASE pcSHA:
            WHEN 'SHA1' THEN
                    ASSIGN
                        rRawDataSHA = SHA1-DIGEST(mInnerCombined).
            WHEN 'SHA-256' THEN
                ASSIGN
                    rRawDataSHA = MESSAGE-DIGEST('SHA-256', mInnerCombined).
            OTHERWISE 
            ASSIGN
                rRawDataSHA = SHA1-DIGEST(mInnerCombined).
        END CASE.
                                     
    /* Deallocates any memory. */
    SET-SIZE(mInnerCombined) = 0.
    
    /* Outer Loop calculation for SHA*/
    SET-SIZE(mOuterCombined)                      = 0.
    SET-SIZE(mOuterCombined)                      = GET-SIZE(mKeyOpad) + LENGTH(rRawDataSHA,'RAW':U).
    PUT-BYTES(mOuterCombined, 1)                  = mKeyOpad.
    PUT-BYTES(mOuterCombined, {&xiBlockSize} + 1) = rRawDataSHA.
    
    /* SHA*/
    CASE pcSHA:
        WHEN 'SHA1' THEN
            ASSIGN
                rRawDataSHA = SHA1-DIGEST(mOuterCombined).
        WHEN 'SHA-256' THEN
            ASSIGN
                rRawDataSHA = MESSAGE-DIGEST('SHA-256', mOuterCombined).
        OTHERWISE 
        ASSIGN
            rRawDataSHA = SHA1-DIGEST(mOuterCombined).
    END CASE.
    
    /* Deallocates any memory. */
    SET-SIZE(mKeyOpad)       = 0.
    SET-SIZE(mOuterCombined) = 0.
    
    /* Convert the raw binary results into a human readable BASE-64 value.*/
    cHMACSHA = BASE64-ENCODE(rRawDataSHA).
    /*cHMACSHA = HEX-ENCODE(rRawDataSHA).*/
    
    
    &UNDEFINE xiBlockSize
    RETURN cHMACSHA.
END FUNCTION. /** End Of Function HMACSHA1-BASE64 */

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
username = bediener.username.

IF master-key = "" THEN
DO:
    FOR EACH guest-queasy WHERE guest-queasy.KEY = "userToken" AND guest-queasy.char1 EQ user-init NO-LOCK BY guest-queasy.number3 DESCENDING:
        ASSIGN master-key = ENTRY(1, guest-queasy.char3, "|").
        LEAVE.
    END.
END.

IF license-nr = "" THEN
DO:
    FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN RUN decode-string(paramtext.ptexte, OUTPUT license-nr). 
END.

/*secret = username + license-nr + master-key.*/
secret = master-key.

/* create token ... */
/******** Generate Token ********/
oJsonObjectHeader = NEW JsonObject().
oJsonObjectHeader:ADD("alg", "HS256").
oJsonObjectHeader:ADD("type", "JWT").

headerString = STRING(oJsonObjectHeader:GetJsonText()).
PUT-STRING(rawHeader,1) = headerString. 
headerString = STRING(BASE64-ENCODE(rawHeader)).
headerString = REPLACE(headerString,"/","_").
headerString = REPLACE(headerString,"+","-").
headerString = REPLACE(headerString,"=","").
headerString = RIGHT-TRIM(headerString,"A").

oJsonObjectPayload = NEW JsonObject().
oJsonObjectPayload:Add("loggedInAs","admin").
oJsonObjectPayload:Add("generated",NOW).
oJsonObjectPayload:Add("expired",NOW + 3600 * 1000).

payloadString = STRING(oJsonObjectPayload:GetJsonText()).
PUT-STRING(rawPayload,1) = payloadString. 
payloadString = STRING(BASE64-ENCODE(rawPayload)).
payloadString = REPLACE(payloadString,"/","_").
payloadString = REPLACE(payloadString,"+","-").
payloadString = REPLACE(payloadString,"=","").
payloadString = RIGHT-TRIM(payloadString,"A").
/*
tokenSignature = hmac-base64('SHA-256', secret, headerString + "." + payloadString).
tokenSignature = REPLACE(tokenSignature,"/","_").
tokenSignature = REPLACE(tokenSignature,"+","-").
tokenSignature = REPLACE(tokenSignature,"=","").
*/
DO i = 1 TO LENGTH(secret):
    tokenSignature = tokenSignature + "#" + SUBSTRING(secret,i,1).
END.
tokenSignature = tokenSignature + "#".
tokenSignature = HEX-ENCODE(SHA1-DIGEST(tokenSignature)).
tokenSignature = CAPS(tokenSignature).
token = headerString + payloadString + STRING(tokenSignature).
CLIPBOARD:VALUE = token.
user-token = CAPS(token).

/*
errCode    = "0 - Success".
CURRENT-WINDOW:WIDTH = 300.
DISP user-token FORMAT "x(295)" WITH WIDTH 299.
UPDATE user-token.
*/
/*===============================PROCEDURES================================*/

PROCEDURE decode-string1: 
    DEFINE INPUT PARAMETER in-str   AS CHAR     NO-UNDO. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR     NO-UNDO INITIAL "". 
    DEFINE VARIABLE s               AS CHAR     NO-UNDO. 
    DEFINE VARIABLE j               AS INTEGER  NO-UNDO. 
    DEFINE VARIABLE len             AS INTEGER  NO-UNDO. 
    ASSIGN
        s   = in-str 
        j   = ASC(SUBSTR(s, 1, 1)) - 71 
        len = LENGTH(in-str) - 1 
        s   = SUBSTR(in-str, 2, len)
    .
    DO len = 1 TO LENGTH(s): 
      out-str = out-str + chr(ASC(SUBSTR(s,len,1)) - j). 
    END. 
    out-str = SUBSTR(out-str, 5, (LENGTH(out-str) - 4)). 
END. 

PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
    s   = in-str. 
    j   = ASC(SUBSTR(s, 1, 1)) - 70. 
    len = LENGTH(in-str) - 1. 
    s   = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END. 

