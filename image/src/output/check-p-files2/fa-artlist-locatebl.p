
DEF INPUT  PARAMETER locate         AS CHAR.
DEF OUTPUT PARAMETER avail-fa-lager AS LOGICAL INIT NO.

FIND FIRST fa-lager WHERE fa-lager.bezeich = locate NO-LOCK NO-ERROR. 
IF AVAILABLE fa-lager THEN avail-fa-lager = YES.
