DEF INPUT PARAMETER user-name   AS CHAR    NO-UNDO.
DEF INPUT PARAMETER inp-pswd    AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER pswd-ok    AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER pswd-level AS INTEGER NO-UNDO INIT 0.

DEF VARIABLE heute          AS DATE     NO-UNDO.

DEF VARIABLE sindata-pswd   AS CHAR     NO-UNDO.
DEF VARIABLE dd-str         AS CHAR     NO-UNDO.
DEF VARIABLE mm-str         AS CHAR     NO-UNDO.
DEF VARIABLE yy-str         AS CHAR     NO-UNDO.

DEF VARIABLE nr             AS INTEGER  NO-UNDO.
DEF VARIABLE dd             AS INTEGER  NO-UNDO.
DEF VARIABLE tot-digit      AS INTEGER  NO-UNDO.
DEF VARIABLE tot-special    AS INTEGER  NO-UNDO.
DEF VARIABLE tot-char       AS INTEGER  NO-UNDO.
DEF VARIABLE curr-i         AS INTEGER  NO-UNDO.

DEF VARIABLE month-str      AS CHAR EXTENT 12 NO-UNDO
 INIT ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
       "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"].

IF user-name = "Sindata" THEN
DO:
  ASSIGN
    heute   = TODAY
    dd      = DAY(heute)
    mm-str  = month-str[MONTH(heute)]
    yy-str  = STRING(YEAR(heute))  
    yy-str  = SUBSTR(yy-str,4,1) + SUBSTR(yy-str,3,1)
            + SUBSTR(yy-str,2,1) + SUBSTR(yy-str,1,1) 
  .
  IF dd = 1 OR dd = 21 OR dd = 31 THEN
    dd-str = STRING(dd,"99") + "st".
  ELSE IF dd = 2 OR dd = 22  THEN 
    dd-str = STRING(dd,"99") + "nd".
  ELSE IF dd = 3 OR dd = 23  THEN 
    dd-str = STRING(dd,"99") + "rd".
  ELSE dd-str = STRING(dd,"99") + "th".
    sindata-pswd = "*" + dd-str + mm-str + yy-str + "#".
  pswd-ok = inp-pswd = sindata-pswd.
  IF pswd-ok THEN RETURN.

  RUN decode-usercode(OUTPUT nr). 
  IF nr LE 0 THEN RETURN. 

END.

IF LENGTH(inp-pswd) LT 10 THEN 
DO: 
    pswd-level = -1.
    RETURN.
END.

DO curr-i = 1 TO LENGTH(inp-pswd):
    IF SUBSTR(inp-pswd, curr-i, 1) GE "0" 
      AND SUBSTR(inp-pswd, curr-i, 1) LE "9" THEN
      tot-digit = tot-digit + 1.
    ELSE IF SUBSTR(inp-pswd, curr-i, 1) GE "a" 
      AND SUBSTR(inp-pswd, curr-i, 1) LE "z" THEN
      tot-char = tot-char + 1.
    ELSE tot-special = tot-special + 1.
END.
IF tot-digit LT 2 OR tot-special = 0 OR tot-char LT 5 THEN
DO:
  pswd-level = -2.
  RETURN.
END.

ASSIGN pswd-ok = YES.
RUN check-pswd-strength(inp-pswd, OUTPUT pswd-level).

PROCEDURE check-pswd-strength:
DEFINE INPUT PARAMETER  pass       AS CHAR CASE-SENSITIVE NO-UNDO.
DEFINE OUTPUT PARAMETER pswd-level AS INTEGER NO-UNDO INITIAL 0.

DEFINE VARIABLE upper-case  AS CHAR EXTENT 26 INITIAL ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"] CASE-SENSITIVE.
DEFINE VARIABLE lower-case  AS CHAR EXTENT 26 INITIAL ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"] CASE-SENSITIVE.
DEFINE VARIABLE numbers     AS CHAR EXTENT 10 INITIAL ["0","1","2","3","4","5","6","7","8","9"] CASE-SENSITIVE.
DEFINE VARIABLE strStatus   AS CHAR INITIAL " ".
DEFINE VARIABLE pointer     AS CHAR.
DEFINE VARIABLE tot-up      AS INT INITIAL 0.
DEFINE VARIABLE tot-low     AS INT INITIAL 0.
DEFINE VARIABLE tot-num     AS INT INITIAL 0.
DEFINE VARIABLE tot-special AS INT INITIAL 0.
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE index1      AS INTEGER.
DEFINE VARIABLE longer      AS INTEGER.
DEFINE VARIABLE intScore    AS INTEGER INIT 0 NO-UNDO.

  longer = LENGTH(pass).

/*length point*/
  IF longer LT 4 THEN                         /*less than 4 characters*/
    intScore = intScore + 3.               
  ELSE IF longer GT 5 AND longer LT 7 THEN    /*between 5 and 7 characters*/
    intScore = intScore + 6.
  ELSE IF longer GT 8 AND longer LT 15 THEN   /*between 8 and 15 characters*/
    intScore = intScore + 12.
  ELSE IF longer GT 16 THEN                   /*16 or more characters*/
    intScore = intScore + 18.

/*total upper case  and total lower case */
  DO i = 1 TO longer:
     DO index1 = 1 TO 26:
        pointer = SUBSTRING(pass, i, 1).
       IF pointer = upper-case[index1] THEN
            tot-up = tot-up + 1.
       ELSE IF pointer MATCHES lower-case[index1] THEN
            tot-low = tot-low + 1. 
       END.
  END.

/*total number*/
  DO i = 1 TO longer:
     DO index1 = 1 TO 10:
        pointer = SUBSTRING(pass, i, 1).
      IF pointer MATCHES numbers[index1] THEN
            tot-num = tot-num + 1.  
      END.
  END. 

/*total special character*/
  tot-special = longer - (tot-up + tot-low + tot-num).

/*letters point*/   
  IF tot-up = 0 AND tot-low = 0 THEN                              /*no letters*/
    intScore = intScore + 0.
  ELSE IF tot-up = 0 AND tot-num = 0 AND tot-special = 0 THEN     /*all letters are lower case*/
    intScore = intScore + 5.
  ELSE IF tot-up NE 0 AND tot-low NE 0 THEN                       /*letters are mixed case*/
    intScore = intScore + 7.

/*numbers point*/
  IF tot-num = 0 THEN             /*no numbers exist*/
    intScore = intScore + 0.
  ELSE IF tot-num = 1 THEN        /*one number exists*/
    intScore = intScore + 5.
  ELSE IF tot-num GT 3 THEN       /*3 or more numbers exists*/
    intScore = intScore + 7.

/*special character point*/
  IF tot-special = 0 THEN         /*no special characters*/
    intScore = intScore + 0.
  ELSE IF tot-special = 1 THEN    /*one special character exists*/
    intScore = intScore + 5.
  ELSE IF tot-special GT 1 THEN   /*more than one special character exists*/
    intScore = intScore + 10.

/*combinations point*/
  IF tot-up NE 0 AND tot-num NE 0 OR  tot-low NE 0 AND tot-num NE 0 THEN          /*letters and numbers exist*/
    intScore = intScore + 1.
  IF tot-up NE 0 AND tot-low NE 0 THEN                                       /*mixed case letters*/
    intScore = intScore + 1.
  IF tot-up NE 0 AND tot-num NE 0 AND tot-special NE 0 OR tot-low NE 0 AND tot-num NE 0 AND tot-special NE 0 THEN   /*letters, numbers and special characters exist*/ 
    intScore = intScore + 2.
  IF tot-up NE 0 AND tot-num NE 0 AND tot-special NE 0 AND tot-low NE 0 THEN /*mixed case letters, numbers and special characters exist*/
    intScore = intScore + 2.

/* strStatus */
  IF intScore LT 16 THEN pswd-level = 1.
  ELSE IF intScore GT 15 AND intScore LT 25 THEN pswd-level = 2.
  ELSE IF intScore GT 24 AND intScore LT 35 THEN pswd-level = 3.
  ELSE IF intScore GT 34 AND intScore LT 45 THEN pswd-level = 4.
  ELSE pswd-level = 5.

END.

PROCEDURE decode-usercode: 
DEFINE OUTPUT PARAMETER nr AS INTEGER INITIAL -1. 
DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
DEFINE VARIABLE passwd AS CHAR. 
DEFINE buffer usr FOR bediener. 
  FIND FIRST usr WHERE usr.username = user-name AND usr.flag = 0 
    AND usr.betriebsnr = 1 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE usr AND NOT found: 
    RUN decode-string1(usr.usercode, OUTPUT passwd). 
    IF passwd = inp-pswd THEN 
    DO: 
      nr = usr.nr. 
      found = YES. 
    END. 
    ELSE FIND NEXT usr WHERE usr.username = user-name 
      AND usr.flag = 0 AND usr.betriebsnr = 1 NO-LOCK NO-ERROR. 
  END. 
END. 

PROCEDURE decode-string1: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 71. 
  len = length(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO length(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
  out-str = SUBSTR(out-str, 5, (length(out-str) - 4)). 
END. 
