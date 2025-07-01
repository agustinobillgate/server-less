
DEF INPUT PARAMETER artnr AS INT.
DEF INPUT PARAMETER departement AS INT.
DEF OUTPUT PARAMETER avail-h-art AS LOGICAL.

DEFINE buffer h-art FOR vhp.h-artikel.

FIND FIRST h-art WHERE h-art.artnr = /*vhp.h-bill-line.*/ artnr
  AND h-art.departement = /*vhp.h-bill-line.*/ departement
  AND h-art.artart = 0 NO-LOCK NO-ERROR.
IF AVAILABLE h-art THEN avail-h-art = YES.
