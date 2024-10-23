DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER 
    FIELD dept  AS CHARACTER
    .

DEFINE OUTPUT PARAMETER licenseNr AS INTEGER.
DEFINE OUTPUT PARAMETER license-cashless AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.

FOR EACH hoteldpt NO-LOCK:
    CREATE t-dept.
    ASSIGN
        t-dept.nr   = hoteldpt.num
        t-dept.dept = CAPS(hoteldpt.depart).
END.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr).

FIND FIRST htparam WHERE htparam.paramnr EQ 1022
    AND htparam.bezeich NE "not used"
    AND htparam.flogical NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN license-cashless = YES.

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
