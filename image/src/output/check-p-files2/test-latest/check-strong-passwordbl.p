DEFINE TEMP-TABLE tp-bediener LIKE bediener.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER user-name AS CHAR.
DEFINE INPUT PARAMETER user-pswd AS CHAR.

DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER change-password-flag AS LOGICAL.
                         
change-password-flag = NO.

DEFINE BUFFER shabediener FOR bediener.
/*check sha1*/
IF LENGTH(user-pswd) GE 40 THEN
DO:
    DEFINE VARIABLE bediener-pass AS CHAR.
    DEFINE VARIABLE bediener-sha1 AS CHAR.

    FIND FIRST shabediener WHERE shabediener.username EQ user-name NO-LOCK NO-ERROR.
    IF AVAILABLE shabediener THEN
    DO:
        RUN decode-string1(shabediener.usercode,OUTPUT bediener-pass).
        bediener-sha1 = HEX-ENCODE(SHA1-DIGEST(bediener-pass)).
        IF bediener-sha1 NE user-pswd THEN
        DO:
            mess-result = "99 - Incorrect Password!".
            RETURN.
        END.
        ELSE
        DO:
            user-pswd = bediener-pass.
        END.
    END.
END.

FIND FIRST htparam WHERE paramnr EQ 256 NO-LOCK NO-ERROR.
IF htparam.flogical EQ YES THEN
DO:
    IF case-type EQ 1 THEN RUN start-vhp.
    ELSE IF case-type EQ 2 THEN RUN check-password.
    ELSE
    DO:
        mess-result = "Wrong CaseType, please check parameters.".
        RETURN. 
    END.
END.
RELEASE htparam.

PROCEDURE start-vhp: 
    DEFINE VARIABLE nr          AS INTEGER INITIAL -1. 
    DEFINE VARIABLE pswd-str    AS CHAR    NO-UNDO.
    DEFINE VARIABLE pswd-level  AS INTEGER NO-UNDO.
    DEFINE VARIABLE pswd-ok     AS LOGICAL NO-UNDO INITIAL NO.
    DEFINE VARIABLE cancel-it   AS LOGICAL NO-UNDO.

    RUN read-bedienerlist-cldbl.p (1, user-name, OUTPUT TABLE tp-bediener).
    FIND FIRST tp-bediener NO-ERROR. 
    IF NOT AVAILABLE tp-bediener THEN 
    DO: 
        mess-result = "Login incorrect, please try again.".
        RETURN. 
    END. 

    /*expire password*/
    IF tp-bediener.kassenbest = 1 THEN 
    DO:
        mess-result = "Password Expired!".
        change-password-flag = YES.
        RETURN.
    END.
    /*end*/

    RUN pswd-validation-cldbl.p (user-name, user-pswd, OUTPUT pswd-ok, OUTPUT pswd-level).
    IF pswd-ok THEN 
    DO:
        mess-result = "Password OK!".
        change-password-flag = NO.
    END.
    ELSE IF NOT pswd-ok THEN
    DO:
        mess-result = "Your password is not secured enough, It needs to be changed right now!".
        change-password-flag = YES.
        RETURN.
    END.
END.

PROCEDURE check-password: 
    DEFINE VARIABLE nr          AS INTEGER INITIAL -1. 
    DEFINE VARIABLE pswd-str    AS CHAR    NO-UNDO.
    DEFINE VARIABLE pswd-level  AS INTEGER NO-UNDO.
    DEFINE VARIABLE pswd-ok     AS LOGICAL NO-UNDO INITIAL NO.
    DEFINE VARIABLE cancel-it   AS LOGICAL NO-UNDO.

    RUN pswd-validation-cldbl.p (user-name, user-pswd, OUTPUT pswd-ok, OUTPUT pswd-level).
    IF pswd-ok THEN 
    DO:
        mess-result = "Password OK!".
        change-password-flag = NO.
    END.
    ELSE IF NOT pswd-ok THEN
    DO:
        mess-result = "Your password is not secured enough, It needs to be changed right now!".
        change-password-flag = YES.
        RETURN.
    END.
END.

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


