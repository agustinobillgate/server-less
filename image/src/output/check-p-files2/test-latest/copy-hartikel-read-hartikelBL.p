
DEF INPUT PARAMETER art1 AS INT.
DEF INPUT PARAMETER dept1 AS INT.
DEF OUTPUT PARAMETER t-bez AS CHAR.
DEF OUTPUT PARAMETER avail-hartikel AS LOGICAL INIT NO.

FIND FIRST h-artikel WHERE h-artikel.artnr = art1
    AND h-artikel.departement = dept1
/*IF 270619 - Because in copy-hartikel-btn-gobl.p this validation exist*/
    AND h-artikel.activeflag
/*END IF*/
    NO-LOCK NO-ERROR.
IF AVAILABLE h-artikel THEN 
DO:
    t-bez = h-artikel.bezeich. 
    avail-hartikel = YES.
END.
