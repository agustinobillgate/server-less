DEFINE TEMP-TABLE bediener-info
    FIELD user-number   AS INT
    FIELD user-init     AS CHAR
    FIELD user-name     AS CHAR
    FIELD dept-number   AS INT
    FIELD dept-name     AS CHAR
    FIELD email         AS CHAR
    FIELD mobile        AS CHAR
    FIELD pager         AS CHAR
    FIELD totp-flag     AS LOGICAL
    FIELD totp-status   AS CHAR.

DEFINE TEMP-TABLE value-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD value-str AS CHAR FORMAT "x(20)".

DEFINE TEMP-TABLE signature-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD signature AS CHAR FORMAT "x(40)".

DEFINE INPUT PARAMETER user-name AS CHAR.
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE OUTPUT PARAMETER epoch-signature AS INT64.
DEFINE OUTPUT PARAMETER bediener AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR bediener-info.
DEFINE OUTPUT PARAMETER TABLE FOR signature-list.

DEFINE BUFFER buff-user FOR queasy.
DEFINE BUFFER bdept FOR queasy.
DEFINE BUFFER totpdata FOR queasy.

DEF VAR dept-name AS CHAR.

FIND FIRST bediener WHERE bediener.userinit EQ user-init AND bediener.username EQ user-name NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO :
    FIND FIRST buff-user WHERE buff-user.KEY EQ 134 AND buff-user.number1 EQ bediener.nr AND buff-user.betriebsnr EQ 0 AND buff-user.deci1 EQ 0 AND buff-user.logi1 EQ NO USE-INDEX b-num_ix NO-LOCK NO-ERROR.
    FIND FIRST bdept WHERE bdept.KEY EQ 19 AND bdept.number1 EQ bediener.user-group NO-LOCK NO-ERROR.
    IF AVAILABLE bdept THEN dept-name = bdept.char3.
    ELSE dept-name = "".

    CREATE bediener-info.
    ASSIGN
        bediener-info.user-number  = bediener.nr
        bediener-info.user-init    = bediener.userinit
        bediener-info.user-name    = bediener.username
        bediener-info.dept-number  = bediener.user-group
        bediener-info.dept-name    = dept-name
        bediener-info.email        = buff-user.char2
        bediener-info.mobile       = buff-user.char1
        bediener-info.pager        = buff-user.char3.

    /*Masdod 14022025 get totp info*/
    FIND FIRST totpdata WHERE totpdata.KEY EQ 341 AND totpdata.char1 EQ bediener.username NO-LOCK NO-ERROR.
    IF AVAILABLE totpdata THEN 
    DO:
        bediener-info.totp-flag = YES.
        IF totpdata.logi1 EQ YES THEN bediener-info.totp-status = "ACTIVE".
        ELSE bediener-info.totp-status = "INACTIVE".
    END.
    ELSE bediener-info.totp-flag = NO.

    CREATE value-list.
    ASSIGN
        value-list.var-name  = "totp-flag"
        value-list.value-str = STRING(bediener-info.totp-flag).
    
    CREATE value-list.
    ASSIGN
        value-list.var-name  = "totp-status"
        value-list.value-str = bediener-info.totp-status.
    
    RUN create-signature(bediener.username,TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
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

