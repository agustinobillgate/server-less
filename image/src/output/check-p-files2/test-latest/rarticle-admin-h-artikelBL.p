
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER h-artnr     AS INT.
DEF INPUT PARAMETER dept        AS INT.
DEF INPUT PARAMETER h-bezeich   AS CHAR.
DEF OUTPUT PARAMETER flag       AS INT INIT 0.

IF case-type = 1 THEN
FIND FIRST h-artikel WHERE h-artikel.artnr = h-artnr 
    AND h-artikel.departement = dept NO-LOCK NO-ERROR.
ELSE IF case-type = 2 THEN
FIND FIRST h-artikel WHERE h-artikel.bezeich = h-bezeich
    AND h-artikel.departement = dept AND h-artikel.artnr NE h-artnr
    NO-LOCK NO-ERROR. 

IF AVAILABLE h-artikel THEN flag = 1.
