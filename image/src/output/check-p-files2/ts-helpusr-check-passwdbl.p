
DEF INPUT  PARAMETER passwd AS CHAR. 
DEF INPUT  PARAMETER knr  AS INT.
DEF INPUT  PARAMETER dept AS INT.
DEF OUTPUT PARAMETER anzahl-falsch AS INT.
DEF OUTPUT PARAMETER its-ok AS LOGICAL INITIAL NO. 

RUN check-passwd.

PROCEDURE check-passwd:
DEF VAR passwd1 AS CHAR NO-UNDO. 
DEF BUFFER vhpusr FOR vhp.bediener. 
  FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = knr 
    AND vhp.kellner.departement = dept NO-LOCK. 
  FIND FIRST vhpusr WHERE vhpusr.userinit = 
    TRIM(STRING(vhp.kellner.kellner-nr,">>99")) NO-LOCK. 
  RUN decode-string1(vhpusr.usercode, OUTPUT passwd1). 
  its-ok = (passwd = passwd1). 
  IF NOT its-ok THEN anzahl-falsch = anzahl-falsch + 1. 
END.

PROCEDURE decode-string1: 
DEFINE INPUT  PARAMETER in-str  AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s  AS CHAR. 
DEFINE VARIABLE j  AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 71. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + CHR(ASC(SUBSTR(s,len,1)) - j). 
  END. 
  out-str = SUBSTR(out-str, 5, (LENGTH(out-str) - 4)). 
END. 
