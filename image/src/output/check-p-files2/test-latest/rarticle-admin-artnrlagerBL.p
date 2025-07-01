
DEF INPUT PARAMETER h-artnrlager AS INT.
DEF OUTPUT PARAMETER flag        AS INT INIT 0.

FIND FIRST l-artikel WHERE l-artikel.artnr = h-artnrlager NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-artikel THEN flag = 1.
