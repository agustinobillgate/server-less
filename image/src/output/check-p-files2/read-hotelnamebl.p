
DEF INPUT PARAMETER  param-str  AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER hotel-name AS CHAR NO-UNDO INIT "".

DEFINE VARIABLE param-nr AS INTEGER NO-UNDO INIT 0.
ASSIGN 
    param-nr = INTEGER(SUBSTR(param-str, 2))
    param-nr = param-nr * 2 NO-ERROR
.

IF param-nr NE 240 THEN RETURN.

FIND FIRST vhp.paramtext WHERE vhp.paramtext.txtnr = 240 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE paramtext THEN RETURN.

IF AVAILABLE vhp.paramtext AND vhp.paramtext.ptexte NE "" THEN 
  RUN decode-string(vhp.paramtext.ptexte, OUTPUT hotel-name). 

PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = length(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO length(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 
