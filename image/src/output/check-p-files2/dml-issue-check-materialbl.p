
DEFINE TEMP-TABLE op-list       LIKE l-op. 

DEFINE INPUT  PARAMETER TABLE FOR op-list.
DEFINE INPUT  PARAMETER mat-grp AS INT.
DEFINE OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES. 


FOR EACH op-list NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr 
    AND l-artikel.endkum GE mat-grp NO-LOCK:
    its-ok = NO.
    RETURN. 
END. 
