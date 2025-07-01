
DEF INPUT PARAMETER billart AS INT.
DEF INPUT PARAMETER c-list-dept AS INT.
DEF INPUT PARAMETER c-list-datum AS DATE.
DEF INPUT PARAMETER c-list-rechnr AS INT.
DEF OUTPUT PARAMETER t-bezeich AS CHAR.

FIND FIRST h-artikel WHERE h-artikel.artnr = billart 
    AND h-artikel.departement = c-list-dept NO-LOCK. 
t-bezeich = h-artikel.bezeich.
FOR EACH h-compli WHERE h-compli.datum = c-list-datum
    AND c-list-dept = h-compli.departement 
    AND c-list-rechnr = h-compli.rechnr: 
    h-compli.p-artnr = billart. 
END. 
