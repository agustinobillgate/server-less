DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.  
  
DEF INPUT-OUTPUT PARAMETER from-dept AS INT.  
DEF INPUT-OUTPUT PARAMETER to-dept AS INT.  
  
DEF OUTPUT PARAMETER to-date AS DATE.  
DEF OUTPUT PARAMETER from-date AS DATE.  
DEF OUTPUT PARAMETER depname1 AS CHAR.  
DEF OUTPUT PARAMETER depname2 AS CHAR.  
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
  
DEF VAR t-htpchar AS CHAR.  
RUN htpdate.p (110, OUTPUT to-date).  
from-date = DATE(month(to-date), 1, year(to-date)).   
  
RUN select-deptbl.p  
    (INPUT-OUTPUT from-dept, INPUT-OUTPUT to-dept, OUTPUT depname1, OUTPUT depname2).  
  
FOR EACH hoteldpt:  
    CREATE t-hoteldpt.  
    BUFFER-COPY hoteldpt TO t-hoteldpt.  
END.  
