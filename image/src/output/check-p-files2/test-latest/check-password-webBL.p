DEFINE TEMP-TABLE payload-list
    FIELD hashed-pass AS CHARACTER
    FIELD int-input   AS INTEGER
    FIELD vmode       AS CHARACTER.

DEFINE TEMP-TABLE response-list
    FIELD success-status AS LOGICAL
    FIELD msg-str        AS CHARACTER
    FIELD err-no         AS INTEGER.

DEFINE TEMP-TABLE value-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD value-str AS CHAR FORMAT "x(20)".

DEFINE TEMP-TABLE signature-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD signature AS CHAR FORMAT "x(40)".

DEFINE INPUT PARAMETER user-name AS CHARACTER.
DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR response-list.
DEFINE OUTPUT PARAMETER epoch-signature AS INT64.
DEFINE OUTPUT PARAMETER TABLE FOR signature-list.

DEFINE VARIABLE hashed-pass    AS CHARACTER.
DEFINE VARIABLE int-input      AS INTEGER.
DEFINE VARIABLE vmode          AS CHARACTER.
DEFINE VARIABLE success-status AS LOGICAL.
DEFINE VARIABLE msg-str        AS CHARACTER.
DEFINE VARIABLE err-no         AS INTEGER.

DEFINE VARIABLE hashed-from-be AS CHARACTER.

DEFINE VARIABLE licenseNr AS CHARACTER.
FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr). 

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        hashed-pass = payload-list.hashed-pass
        int-input   = payload-list.int-input
        vmode       = payload-list.vmode
    .

    RUN checker-hash.
    
    CREATE response-list.
    ASSIGN
        response-list.success-status = success-status
        response-list.msg-str        = msg-str
        response-list.err-no         = err-no
    .
END.

PROCEDURE checker-hash:
    IF vmode EQ "genparam" THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr EQ int-input NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO:
            IF htparam.fchar NE "" AND htparam.fchar NE ? THEN
            DO: 
                IF NUM-ENTRIES(htparam.fchar, ";") GE 4 THEN
                DO:
                    hashed-from-be = HEX-ENCODE(SHA1-DIGEST(ENTRY(4, htparam.fchar, ";"))).

                    IF hashed-pass EQ hashed-from-be THEN
                    DO:
                        success-status = TRUE.
                        RUN gen-signature.
                        msg-str = "".
                        err-no = 0.
                    END.
                    ELSE
                    DO:
                        success-status = FALSE.
                        RUN gen-signature.
                        msg-str = "Password is incorrect.".
                        err-no = 1.
                    END.
                END.
                ELSE
                DO:
                    success-status = FALSE.
                    RUN gen-signature.
                    msg-str = "Improper parameter configuration.".
                    err-no = 2.
                END.
            END.
            ELSE
            DO:
                success-status = TRUE.
                RUN gen-signature.
                msg-str = "".
                err-no = 0.
            END.
        END.
        ELSE
        DO:
            success-status = FALSE.
            RUN gen-signature.
            msg-str = "Parameter is not found.".
            err-no = 3.
        END.
    END.
    /* Dzikri F3BC84 - Validate password */
    ELSE IF vmode EQ "genparamplain" THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr EQ int-input NO-LOCK NO-ERROR.
        IF AVAILABLE htparam AND htparam.bezeich NE "not used" THEN
        DO:
            IF htparam.fchar NE "" AND htparam.fchar NE ? THEN
            DO: 
                hashed-from-be = HEX-ENCODE(SHA1-DIGEST(htparam.fchar)).

                IF hashed-pass EQ hashed-from-be THEN
                DO:
                    success-status = TRUE.
                    RUN gen-signature.
                    msg-str = "".
                    err-no = 0.
                END.
                ELSE
                DO:
                    success-status = FALSE.
                    RUN gen-signature.
                    msg-str = "Password is incorrect.".
                    err-no = 1.
                END.
            END.
            ELSE
            DO:
                success-status = TRUE.
                RUN gen-signature.
                msg-str = "".
                err-no = 0.
            END.
        END.
        ELSE
        DO:
            success-status = FALSE.
            RUN gen-signature.
            msg-str = "Parameter is not found.".
            err-no = 3.
        END.
    END.
    ELSE IF vmode EQ "cekpassword" THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr EQ int-input NO-LOCK NO-ERROR.
        IF AVAILABLE htparam AND htparam.bezeich NE "not used" THEN
        DO:
            IF htparam.fchar NE "" AND htparam.fchar NE ? THEN
            DO: 
                success-status = TRUE.
                msg-str = "Password Exist".
                err-no = 1.
            END.
            ELSE
            DO:
                success-status = TRUE.
                msg-str = "No Password".
                err-no = 0.
            END.
        END.
        ELSE
        DO:
            success-status = FALSE.
            msg-str = "Parameter is not found.".
            err-no = 3.
        END.
    END.
    /* Dzikri F3BC84 - END */
END.

PROCEDURE gen-signature:
    CREATE value-list.
    ASSIGN
        value-list.var-name  = "success-status"
        value-list.value-str = STRING(success-status).
    
    RUN create-signature(user-name,TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
END.

PROCEDURE create-signature:
    DEF INPUT PARAMETER user-name AS CHAR.
    DEF INPUT PARAMETER TABLE FOR value-list.
    DEF OUTPUT PARAMETER epoch AS INT64.
    DEF OUTPUT PARAMETER TABLE FOR signature-list.

    DEF VAR dtz1      AS DATETIME-TZ.
    DEF VAR dtz2      AS DATETIME-TZ.
    DEF VAR data      AS CHAR.
    DEF VAR value-str AS CHAR.

    dtz1 = NOW.
    dtz2 = 1970-01-01T00:00:00.000+0:00.

    epoch = INTERVAL(dtz1, dtz2, "milliseconds").

    FOR EACH value-list:
        value-str = LC(value-list.value-str).

        CASE value-str:
            WHEN "yes" THEN value-str = "true".
            WHEN "no" THEN value-str = "false".
        END CASE.

        data = value-str + "-" + STRING(epoch) + "-" + STRING(licenseNr) + "-" + LC(user-name).

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
    s   = in-str. 
    j   = ASC(SUBSTR(s, 1, 1)) - 70. 
    len = LENGTH(in-str) - 1. 
    s   = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END.

