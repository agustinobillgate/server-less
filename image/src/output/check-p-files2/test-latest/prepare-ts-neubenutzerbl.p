DEF TEMP-TABLE kellner-list
    FIELD nr        AS INTEGER
    FIELD userinit  AS CHAR FORMAT "x(4)"
    FIELD username  AS CHAR FORMAT "x(24)"
    FIELD password  AS CHAR
    FIELD mc-number AS CHAR
.

DEF INPUT PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR kellner-list.

RUN create-list.

PROCEDURE create-list:
  FOR EACH bediener WHERE bediener.flag = 0 AND (SUBSTR(bediener.perm, 19, 1) GE "1" 
    OR SUBSTR(bediener.perm, 20, 1) GE "1") NO-LOCK, 
    FIRST kellner WHERE kellner.kellnername = bediener.username 
    AND kellner.departement = curr-dept NO-LOCK BY bediener.username:
      CREATE kellner-list.
      ASSIGN
          kellner-list.nr        = bediener.nr
          kellner-list.userinit  = bediener.userinit
          kellner-list.username  = bediener.username
          kellner-list.mc-number = STRING(kellner.sprachcode)
      .
      RUN decode-string1 (bediener.usercode, 
          OUTPUT kellner-list.password). 
  END.
END.

PROCEDURE decode-string1: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = asc(SUBSTR(s, 1, 1)) - 71. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + CHR(ASC(SUBSTR(s,len,1)) - j). 
  END. 
  out-str = SUBSTR(out-str, 5, (LENGTH(out-str) - 4)). 
END. 
