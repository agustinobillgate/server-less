
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER vat-artnr      AS INT.
DEF OUTPUT PARAMETER vat-str        AS CHAR.
DEF OUTPUT PARAMETER deptname1      AS CHAR.
DEF OUTPUT PARAMETER serv-artnr     AS INT.
DEF OUTPUT PARAMETER to-dept        AS INT.
DEF OUTPUT PARAMETER deptname2      AS CHAR.
DEF OUTPUT PARAMETER price-decimal  AS INT.


FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
to-date = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 132 NO-LOCK. 
ASSIGN
  vat-artnr = htparam.finteger
  vat-str   = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 133 NO-LOCK. 
ASSIGN serv-artnr = htparam.finteger.

FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK.
deptname1 = hoteldpt.depart.

FOR EACH hoteldpt NO-LOCK: 
  IF to-dept LT hoteldpt.num THEN ASSIGN 
      to-dept = hoteldpt.num
      deptname2 = hoteldpt.depart. 
END. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
