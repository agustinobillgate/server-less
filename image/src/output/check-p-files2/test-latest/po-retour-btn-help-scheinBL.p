
DEF INPUT PARAMETER l-orderhdr-docu-nr AS CHAR.
DEF INPUT PARAMETER l-orderhdr-lief-nr AS INT.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF OUTPUT PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER lager-bezeich AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST l-kredit WHERE l-kredit.name = l-orderhdr-docu-nr 
    AND l-kredit.lief-nr = l-orderhdr-lief-nr 
    AND l-kredit.zahlkonto GT 0 NO-LOCK NO-ERROR. 
IF AVAILABLE l-kredit THEN 
DO: 
    err-code = 1.
    RETURN NO-APPLY. 
END. 
FIND FIRST l-ophdr WHERE l-ophdr.docu-nr = docu-nr 
    AND l-ophdr.lscheinnr = lscheinnr NO-LOCK. 
curr-lager = l-ophdr.lager-nr. 
FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK. 
lager-bezeich = l-lager.bezeich.
