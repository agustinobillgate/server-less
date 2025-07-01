DEFINE TEMP-TABLE t-maingrp LIKE queasy.
DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD dept  AS CHARACTER FORMAT "x(30)".

DEFINE OUTPUT PARAMETER TABLE FOR t-maingrp.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.
DEFINE OUTPUT PARAMETER licenseNr AS INT.

FOR EACH queasy WHERE queasy.KEY = 228:
    CREATE t-maingrp.
    BUFFER-COPY queasy TO t-maingrp.
END.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr). 

FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
    CREATE t-dept.
    ASSIGN
        t-dept.nr   = hoteldpt.num
        t-dept.dept = CAPS(hoteldpt.depart).
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
