
DEFINE TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEFINE OUTPUT PARAMETER cidate         AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER from-dept      AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER to-dept        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER depname1       AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER depname2       AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-hoteldpt.


DEFINE VARIABLE min-dept       AS INT INITIAL 99.
DEFINE VARIABLE max-dept       AS INT INITIAL 0.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN cidate = htparam.fdate.

FOR EACH hoteldpt WHERE hoteldpt.num GE 0 NO-LOCK BY hoteldpt.num: 
  IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num.
  IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
END.

ASSIGN
    from-dept = min-dept
    to-dept   = max-dept. 

FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK. 
depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK. 
depname2 = hoteldpt.depart. 

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
