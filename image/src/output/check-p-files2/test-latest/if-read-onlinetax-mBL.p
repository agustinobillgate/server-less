DEFINE INPUT PARAMETER datum-rech AS DATE.

DEFINE VARIABLE reihenfolge AS INTEGER.

FIND FIRST nightaudit WHERE nightaudit.programm = "nt-onlinetax.p" 
   NO-LOCK NO-ERROR.
ASSIGN reihenfolge = nightaudit.reihenfolge.

FIND LAST nitehist WHERE nitehist.datum EQ datum-rech 
    AND nitehist.reihenfolge = reihenfolge
    AND nitehis.LINE = "END-OF-RECORD" NO-ERROR.
    IF NOT AVAILABLE nitehist THEN
    DO:
        RETURN.                                    
    END.
    ELSE
    DO:
        nitehis.line-nr = 99999998.
END.        
