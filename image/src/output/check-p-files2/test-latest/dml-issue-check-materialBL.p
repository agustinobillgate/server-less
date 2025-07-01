
DEFINE TEMP-TABLE op-list       LIKE l-op. 

DEFINE INPUT  PARAMETER TABLE FOR op-list.
DEFINE INPUT  PARAMETER mat-grp AS INT.
DEFINE OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES. 

DEFINE VARIABLE param89 AS LOGICAL INITIAL NO.

/* FDL Comment 78BC52
FIND FIRST htparam WHERE htparam.paramnr EQ 89
    AND htparam.bezeich NE "not used" NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND NOT htparam.flogical THEN 
DO:
    its-ok = NO.
    RETURN.
END.
*/
its-ok = NO.
FOR EACH op-list NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr EQ op-list.artnr 
    /*AND l-artikel.endkum GE mat-grp*/ NO-LOCK:

    /* FDL Comment 78BC52
    /*FDL Ticket F3344B*/
    IF NOT l-artikel.bestellt THEN
    DO:
        its-ok = NO.
        RETURN.
    END.
    */
    its-ok = YES.
    RETURN.
END. 
