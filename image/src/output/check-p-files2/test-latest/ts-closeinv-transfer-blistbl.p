

DEF INPUT PARAMETER b-list-rechnr   AS INT.
DEF INPUT PARAMETER curr-dept       AS INT.
DEF INPUT PARAMETER b-list-artnr    AS INT.
DEF INPUT PARAMETER b-list-sysdate  AS DATE.
DEF INPUT PARAMETER b-list-zeit     AS INT.
DEF OUTPUT PARAMETER avail-h-bill-line AS LOGICAL INIT NO.

FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = b-list-rechnr 
  AND vhp.h-bill-line.departement = curr-dept 
  AND vhp.h-bill-line.artnr = b-list-artnr 
  AND vhp.h-bill-line.sysdate = b-list-sysdate 
  AND vhp.h-bill-line.zeit = b-list-zeit NO-LOCK NO-ERROR.
IF AVAILABLE h-bill-line THEN avail-h-bill-line = YES.
