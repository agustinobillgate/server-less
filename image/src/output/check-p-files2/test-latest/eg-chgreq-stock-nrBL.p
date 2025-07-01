
DEF INPUT PARAMETER stock-stock-nr AS INT.
DEF OUTPUT PARAMETER bez AS CHAR.
DEF OUTPUT PARAMETER t-ek-aktuell AS DECIMAL.
DEF OUTPUT PARAMETER avail-inv AS LOGICAL.

DEF BUFFER inventory FOR l-artikel.
FIND FIRST inventory WHERE 
    inventory.artnr = stock-stock-nr USE-INDEX artnr_ix NO-LOCK NO-ERROR.
IF AVAILABLE inventory THEN
DO:
    bez = inventory.bezeich.
    t-ek-aktuell = inventory.ek-aktuell.
    avail-inv = YES.
END.
    
