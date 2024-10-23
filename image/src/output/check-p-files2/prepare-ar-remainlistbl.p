
DEF OUTPUT PARAMETER from-art       AS INT.
DEF OUTPUT PARAMETER to-art         AS INT.
DEF OUTPUT PARAMETER from-bez       AS CHAR.
DEF OUTPUT PARAMETER to-bez         AS CHAR.
DEF OUTPUT PARAMETER day1           AS INTEGER. 
DEF OUTPUT PARAMETER day2           AS INTEGER. 
DEF OUTPUT PARAMETER day3           AS INTEGER. 
DEF OUTPUT PARAMETER letter1        AS INTEGER. 
DEF OUTPUT PARAMETER letter2        AS INTEGER. 
DEF OUTPUT PARAMETER letter3        AS INTEGER. 
DEF OUTPUT PARAMETER price-decimal  AS INTEGER.

FOR EACH artikel WHERE artikel.departement = 0 
    AND artikel.artart = 2 AND artikel.activeflag = YES NO-LOCK: 
    IF from-art GT artikel.artnr THEN 
    DO: 
        from-art = artikel.artnr. 
        from-bez = artikel.bezeich. 
    END. 
    IF to-art LT artikel.artnr THEN 
    DO: 
        to-art = artikel.artnr. 
        to-bez = artikel.bezeich. 
    END. 
END. 

FIND FIRST htparam WHERE paramnr = 330 NO-LOCK. 
day1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 331 NO-LOCK. 
day2 = htparam.finteger + day1. 
FIND FIRST htparam WHERE paramnr = 332 NO-LOCK. 
day3 = htparam.finteger + day2. 
 
FIND FIRST htparam WHERE paramnr = 670 NO-LOCK. 
letter1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 671 NO-LOCK. 
letter2 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 388 NO-LOCK. 
letter3 = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
