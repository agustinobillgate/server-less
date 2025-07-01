
DEF INPUT PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER lager-bezeich AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK NO-ERROR. 
IF AVAILABLE l-lager /*MTAND NOT AVAILABLE op-list*/ THEN 
DO: 
    lager-bezeich = l-lager.bezeich. 
    err-code = 1.
    RETURN NO-APPLY. 
END.
