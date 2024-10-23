
DEF INPUT  PARAMETER to-stock   AS INT.
DEF INPUT  PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER lager-bez1 AS CHAR.
DEF OUTPUT PARAMETER flag       AS INT INIT 0.

FIND FIRST l-lager WHERE l-lager.lager-nr = to-stock NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-lager THEN 
DO: 
    flag = 1.
    RETURN NO-APPLY. 
END. 
IF to-stock = curr-lager THEN 
DO: 
    flag = 2.
    RETURN NO-APPLY. 
END. 

lager-bez1 = l-lager.bezeich. 

