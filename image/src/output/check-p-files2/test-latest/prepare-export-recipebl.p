
DEF OUTPUT PARAMETER price-type AS INT.
DEF OUTPUT PARAMETER from-artnr AS INTEGER. 
DEF OUTPUT PARAMETER to-artnr   AS INTEGER. 
DEF OUTPUT PARAMETER from-kateg AS INTEGER. 
DEF OUTPUT PARAMETER to-kateg   AS INTEGER. 

FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 
 
RUN cal-nr.

PROCEDURE cal-nr: 
  from-artnr = 999999. 
  to-artnr = 0. 
  from-kateg = 999999. 
  to-kateg = 0. 
  FOR EACH h-rezept NO-LOCK: 
    IF artnrrezept GT to-artnr THEN to-artnr = artnrrezept. 
    IF artnrrezept LT from-artnr THEN from-artnr = artnrrezept. 
    IF kategorie GT to-kateg THEN to-kateg = kategorie. 
    IF kategorie LT from-kateg THEN from-kateg = kategorie. 
  END.
END. 
