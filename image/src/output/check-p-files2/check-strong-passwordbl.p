DEFINE TEMP-TABLE tp-bediener LIKE bediener.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER user-name AS CHAR.
DEFINE INPUT PARAMETER user-pswd AS CHAR.

DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER change-password-flag AS LOGICAL.
                         
change-password-flag = NO.

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



