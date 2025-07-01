DEFINE INPUT PARAMETER uname AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER new-pwd   AS CHAR NO-UNDO.
DEFINE VARIABLE pswd     AS CHAR    NO-UNDO.

RUN encode-string(new-pwd, OUTPUT pswd). 

FIND FIRST bediener WHERE bediener.username = uname NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN DO:
    FIND CURRENT bediener EXCLUSIVE-LOCK.
    ASSIGN
        bediener.usercode   = pswd
        bediener.kassenbest = 0.
    FIND CURRENT bediener NO-LOCK.

    CREATE res-history.
    ASSIGN
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.aenderung   = "Change Password"
        res-history.action      = "User".
    
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.

END.

PROCEDURE encode-string: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR. 
DEFINE VARIABLE s AS CHAR FORMAT "x(50)". 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE ch AS CHAR INITIAL "". 

  j = random(1,9). 
  in-str = STRING(j) + in-str. 
  j = random(1,9). 
  in-str = STRING(j) + in-str. 
  j = random(1,9). 
  in-str = STRING(j) + in-str. 
  j = random(1,9). 
  in-str = STRING(j) + in-str. 
 
  j = random(1,9). 
  ch = CHR(ASC(STRING(j)) + 23). 
  out-str = ch. 
  j = asc(ch) - 71. 
  DO len = 1 TO length(in-str): 
    out-str = out-str + chr(asc(SUBSTR(in-str,len,1)) + j). 
  END. 

END. 
