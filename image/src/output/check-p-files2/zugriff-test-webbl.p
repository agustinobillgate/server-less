DEFINE TEMP-TABLE value-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD value-str AS CHAR FORMAT "x(20)".

DEFINE TEMP-TABLE signature-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD signature AS CHAR FORMAT "x(40)".

DEFINE TEMP-TABLE tp-bediener  LIKE bediener.  
DEFINE TEMP-TABLE t-messages   LIKE messages. 

/***************** Check User Access Right OF given Array **********************/  

DEFINE INPUT PARAMETER user-init   AS CHAR FORMAT "x(2)".   
DEFINE INPUT PARAMETER array-nr    AS INTEGER.   
DEFINE INPUT PARAMETER expected-nr AS INTEGER.   
DEFINE OUTPUT PARAMETER zugriff    AS LOGICAL INITIAL YES.
DEFINE OUTPUT PARAMETER epoch-signature AS INT64.
DEFINE OUTPUT PARAMETER mess-str   AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR signature-list.

/*
DEFINE VARIABLE user-init       AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE array-nr        AS INTEGER.   
DEFINE VARIABLE expected-nr     AS INTEGER.   
DEFINE VARIABLE zugriff         AS LOGICAL INITIAL YES.
DEFINE VARIABLE epoch-signature AS INT64.
DEFINE VARIABLE mess-str        AS CHARACTER.
*/

DEFINE VARIABLE mail-exist   AS LOGICAL NO-UNDO.  
DEFINE VARIABLE logical-flag AS LOGICAL NO-UNDO.  
DEFINE VARIABLE n            AS INTEGER.   
DEFINE VARIABLE perm         AS INTEGER EXTENT 120 FORMAT "9". /* Malik 4CD2E2 */  
DEFINE VARIABLE s1           AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE s2           AS CHAR FORMAT "x(1)".   
DEFINE VARIABLE mn-date      AS DATE.   
DEFINE VARIABLE anz          AS INTEGER.   
DEFINE VARIABLE hAsync       AS HANDLE NO-UNDO.  

DEFINE VARIABLE username AS CHAR.

IF user-init = "" THEN  
DO:   
    zugriff = NO.   
    mess-str = "User not defined.".
    RETURN.
END.   
ELSE   
DO:  
    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE tp-bediener.
        BUFFER-COPY bediener TO tp-bediener.
        username = bediener.username.
    END.
    ELSE
    DO:
        zugriff = NO.  
        mess-str = "User not found.".
        RETURN.
    END.

    DO  n = 1 TO LENGTH(tp-bediener.permissions):   
        perm[n] = INTEGER(SUBSTR(tp-bediener.permissions, n, 1)).   
    END.   
    IF perm[array-nr] LT expected-nr THEN   
    DO:   
        zugriff = NO. 
        s1 = STRING(array-nr, "999").   
        s2 = STRING(expected-nr).
        mess-str = "Sorry, No Access Right, Access Code = " + s1 + s2. 
    END.   

    CREATE value-list.
    ASSIGN
        value-list.var-name  = "zugriff"
        value-list.value-str = STRING(zugriff).
    
    RUN create-signature(username,TABLE value-list, OUTPUT epoch-signature, 
                         OUTPUT TABLE signature-list).

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
