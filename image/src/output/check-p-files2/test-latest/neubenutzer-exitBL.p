DEF TEMP-TABLE t-bediener LIKE bediener.

DEF INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER name-str    AS CHAR    NO-UNDO.
DEF INPUT PARAMETER id-str      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER new-id      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER new-id1     AS CHAR    NO-UNDO.

DEF OUTPUT PARAMETER user-init  AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER user-name  AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER msg-str    AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER error-flag AS LOGICAL  NO-UNDO INIT YES.

DEF OUTPUT PARAMETER TABLE FOR t-bediener.

DEFINE VARIABLE nr AS INTEGER. 
  
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "neubenutzer". 

FIND FIRST bediener WHERE bediener.username = name-str 
  AND bediener.flag = 0 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bediener THEN 
DO: 
  msg-str = translateExtended ("Wrong User ID.",lvCAREA,"").
  RETURN.  
END. 
 
FIND FIRST bediener WHERE bediener.username = name-str 
  AND bediener.usercode = id-str AND bediener.betriebsnr = 0 
  AND bediener.flag = 0 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bediener THEN 
DO: 
  RUN decode-usercode(OUTPUT nr). 
  IF nr GT 0 THEN FIND FIRST bediener WHERE bediener.nr = nr NO-LOCK. 
END. 
 
IF NOT AVAILABLE bediener THEN
DO:
  msg-str = translateExtended ("Wrong User ID.",lvCAREA,"").
  RETURN.
END.

ASSIGN
  error-flag = NO
  user-init  = bediener.userinit
  user-name  = bediener.username
. 
  
IF new-id NE new-id1 THEN 
  msg-str = translateExtended ("Passwords do not match and will be ignored.",lvCAREA,""). 
ELSE IF new-id NE "" THEN 
DO: 
  FIND CURRENT bediener EXCLUSIVE-LOCK. 
  RUN encode-string(new-id, OUTPUT new-id1). 
  ASSIGN
    bediener.usercode   = new-id1 
    bediener.betriebsnr = 1
  . 
  FIND CURRENT bediener NO-LOCK. 
  msg-str = translateExtended ("New password accepted.",lvCAREA,"").
END. 

CREATE t-bediener.
BUFFER-COPY bediener TO t-bediener.

PROCEDURE decode-usercode: 
DEFINE OUTPUT PARAMETER nr AS INTEGER INITIAL -1. 
DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
DEFINE VARIABLE passwd AS CHAR. 
DEFINE buffer usr FOR bediener. 
  FIND FIRST usr WHERE usr.username = name-str 
    AND usr.betriebsnr = 1 AND usr.flag = 0 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE usr AND NOT found: 
    RUN decode-string(usr.usercode, OUTPUT passwd). 
    IF passwd = id-str THEN 
    DO: 
      nr = usr.nr. 
      found = YES. 
    END. 
    ELSE FIND NEXT usr WHERE usr.username = name-str 
      AND usr.betriebsnr = 1 AND usr.flag = 0 NO-LOCK NO-ERROR. 
  END. 
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
 
PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = asc(SUBSTR(s, 1, 1)) - 71. 
  len = length(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO length(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
  out-str = SUBSTR(out-str, 5, (length(out-str) - 4)). 
END. 
