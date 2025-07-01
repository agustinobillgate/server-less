
DEF INPUT PARAMETER h-lagernr AS INT.
DEF INPUT PARAMETER artnr     AS INT.
DEF OUTPUT PARAMETER flag     AS INT INIT 0.

FIND FIRST l-lager WHERE l-lager.lager-nr = h-lagernr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-lager AND artnr NE 0 THEN flag = 1.
