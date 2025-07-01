/***************** Check User Access Right OF given Array **********************/   
DEFINE INPUT PARAMETER user-init   AS CHAR FORMAT "x(2)".   
DEFINE INPUT PARAMETER array-nr    AS INTEGER.   
DEFINE INPUT PARAMETER expected-nr AS INTEGER.   
DEFINE OUTPUT PARAMETER zugriff    AS LOGICAL INITIAL YES.   
DEFINE OUTPUT PARAMETER mess-str   AS CHARACTER.

DEFINE TEMP-TABLE tp-bediener  LIKE bediener.  
DEFINE TEMP-TABLE t-messages   LIKE messages.  
  
DEFINE VARIABLE mail-exist      AS LOGICAL NO-UNDO.  
DEFINE VARIABLE logical-flag    AS LOGICAL NO-UNDO.  
DEFINE VARIABLE n               AS INTEGER.   
DEFINE VARIABLE perm            AS INTEGER EXTENT 99 FORMAT "9".   
DEFINE VARIABLE s1              AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE s2              AS CHAR FORMAT "x(1)".   
DEFINE VARIABLE mn-date         AS DATE.   
DEFINE VARIABLE anz             AS INTEGER.   
DEFINE VARIABLE hAsync          AS HANDLE               NO-UNDO.  

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
        s1 = STRING(array-nr, "99").   
        s2 = STRING(expected-nr). 
        mess-str = "Sorry, No Access Right, Access Code = " + s1 + s2. 
    END.   
END.   
  
