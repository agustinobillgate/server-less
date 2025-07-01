DEFINE TEMP-TABLE t-param
    FIELD dept      AS INTEGER   FORMAT ">>9"
    FIELD grup      AS INTEGER   FORMAT ">>9"
    FIELD number    AS INTEGER   FORMAT ">>9"   LABEL "No"
    FIELD bezeich   AS CHARACTER FORMAT "x(50)" LABEL "Description"
    FIELD typ       AS INTEGER 
    FIELD logv      AS LOGICAL 
    FIELD val       AS CHARACTER FORMAT "x(30)" LABEL "Value".

DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD dept  AS CHARACTER FORMAT "x(30)".

DEFINE OUTPUT PARAMETER TABLE FOR t-param.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.
DEFINE OUTPUT PARAMETER licenseNr AS INT.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr). 

FOR EACH hoteldpt /*WHERE hoteldpt.num GT 0*/ NO-LOCK:
    CREATE t-dept.
    ASSIGN
        t-dept.nr   = hoteldpt.num
        t-dept.dept = CAPS(hoteldpt.depart).
END.


FOR EACH t-param:
    DELETE t-param.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1 
    AND queasy.number2 EQ 1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 1
        queasy.char1    = "Username"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = 1
        .  
END.
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1 
    AND queasy.number2 EQ 2 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 2
        queasy.char1    = "Password"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = 1
        .  
END.
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1 
    AND queasy.number2 EQ 3 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 3
        queasy.char1    = "Interval Refresh Time"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = 1
        .  
END.

FOR EACH queasy WHERE queasy.KEY EQ 270 AND queasy.number1 EQ 1 AND queasy.betriebsnr EQ 1 NO-LOCK BY queasy.number2:
    CREATE t-param.
    ASSIGN
        t-param.dept    = queasy.betriebsnr 
        t-param.grup    = queasy.number1
        t-param.number  = queasy.number2
        t-param.bezeich = queasy.char1
        t-param.typ     = queasy.number3.
    IF queasy.number3 EQ 1 THEN t-param.val = STRING(queasy.char2).
    ELSE IF queasy.number3 EQ 2 THEN t-param.val = STRING(queasy.deci1).
    ELSE IF queasy.number3 EQ 3 THEN t-param.val = STRING(queasy.date1).
    ELSE IF queasy.number3 EQ 4 THEN
    DO:
        t-param.val  = STRING(queasy.logi1).
        t-param.logv = queasy.logi1.
    END.
    ELSE IF queasy.number3 EQ 5 THEN t-param.val = STRING(queasy.char2).
END.

PROCEDURE decode-string1: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
    s = in-str. 
    j = ASC(SUBSTR(s, 1, 1)) - 71. 
    len = LENGTH(in-str) - 1. 
    s = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(ASC(SUBSTR(s,len,1)) - j). 
    END. 
        out-str = SUBSTR(out-str, 5, (LENGTH(out-str) - 4)). 
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
