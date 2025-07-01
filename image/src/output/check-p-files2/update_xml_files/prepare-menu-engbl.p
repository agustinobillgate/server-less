  
DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.  
DEF TEMP-TABLE t-wgrpdep LIKE wgrpdep.
  
DEF INPUT-OUTPUT PARAMETER from-dept AS INT.  
DEF INPUT-OUTPUT PARAMETER to-dept AS INT.  
  
DEF OUTPUT PARAMETER to-date AS DATE.  
DEF OUTPUT PARAMETER from-date AS DATE.  
DEF OUTPUT PARAMETER vat-included AS LOGICAL.  
DEF OUTPUT PARAMETER depname1 AS CHAR.  
DEF OUTPUT PARAMETER depname2 AS CHAR.  
DEF OUTPUT PARAMETER ldry-dept AS INT.  
DEF OUTPUT PARAMETER double-currency AS LOGICAL.  
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL INIT 1.  
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR t-wgrpdep.
  
DEF VAR t-htpchar AS CHAR.  
RUN htpdate.p (110, OUTPUT to-date).  
from-date = DATE(month(to-date), 1, year(to-date)).   
   
RUN htplogic.p (134, OUTPUT vat-included).  
  
RUN select-deptbl.p  
    (INPUT-OUTPUT from-dept, INPUT-OUTPUT to-dept, OUTPUT depname1, OUTPUT depname2).  
  
RUN htpint.p (1081, OUTPUT ldry-dept).  
RUN htplogic.p (240, OUTPUT double-currency).  
  
IF double-currency THEN   
DO:  
  RUN htpchar.p(144, OUTPUT t-htpchar).  
  FIND FIRST waehrung WHERE waehrung.wabkurz = t-htpchar NO-LOCK NO-ERROR.   
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.   
END.  
  
FOR EACH hoteldpt:  
    CREATE t-hoteldpt.  
    BUFFER-COPY hoteldpt TO t-hoteldpt.  
END.  

FOR EACH wgrpdep:  
    CREATE t-wgrpdep.  
    BUFFER-COPY wgrpdep TO t-wgrpdep.  
END.  
