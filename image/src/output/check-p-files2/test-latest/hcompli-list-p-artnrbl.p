
DEF INPUT-OUTPUT PARAMETER c-list-p-artnr AS INT.
DEF INPUT-OUTPUT PARAMETER c-list-bezeich AS CHAR.
DEF INPUT PARAMETER artnr AS INT.
DEF INPUT PARAMETER c-list-dept AS INT.
DEF INPUT PARAMETER c-list-datum AS DATE.
DEF INPUT PARAMETER c-list-rechnr AS INT.
DEF OUTPUT PARAMETER avail-h-artikel AS LOGICAL INIT NO.

FIND FIRST h-artikel WHERE h-artikel.artnr = c-list-p-artnr 
  AND h-artikel.departement = c-list-dept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE h-artikel THEN 
DO: 
    avail-h-artikel = NO.
    RETURN NO-APPLY. 
END.

ASSIGN
  c-list-p-artnr  = h-artikel.artnr 
  c-list-bezeich  = h-artikel.bezeich
  avail-h-artikel = YES
. 

FOR EACH h-compli WHERE h-compli.datum = c-list-datum 
    AND c-list-dept = h-compli.departement 
    AND c-list-rechnr = h-compli.rechnr AND h-compli.betriebsnr = 0: 
    h-compli.p-artnr = c-list-p-artnr. 
END.
