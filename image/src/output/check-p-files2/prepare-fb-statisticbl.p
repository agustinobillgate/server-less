DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF INPUT  PARAMETER fdept          AS INT.
DEF INPUT  PARAMETER tdept          AS INT.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER fdpt-str       AS CHAR.
DEF OUTPUT PARAMETER tdpt-str       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 AND hoteldpt.num = fdept  
    NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN fdpt-str = hoteldpt.depart.
FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 AND hoteldpt.num = tdept  
    NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN tdpt-str = hoteldpt.depart.

FOR EACH hoteldpt WHERE hoteldpt.num GT 0:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
