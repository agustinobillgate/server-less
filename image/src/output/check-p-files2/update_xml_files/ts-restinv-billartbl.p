
DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT PARAMETER billart AS INT.
DEF INPUT PARAMETER curr-dept AS INT.

DEF OUTPUT PARAMETER price AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = billart 
    AND vhp.h-artikel.departement = curr-dept AND vhp.h-artikel.activeflag 
    AND vhp.h-artikel.artart = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.h-artikel THEN 
    DO:
        CREATE t-h-artikel.
        BUFFER-COPY h-artikel TO t-h-artikel.
        ASSIGN t-h-artikel.rec-id = RECID(h-artikel).
        RUN get-price.
    END.

PROCEDURE get-price: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE tolerance AS INTEGER. 
DEFINE VARIABLE curr-min AS INTEGER. 
  price = vhp.h-artikel.epreis1. 
  IF vhp.h-artikel.epreis2 = 0 THEN RETURN. 
  FIND FIRST vhp.paramtext WHERE vhp.paramtext.txtnr = (10000 + curr-dept) 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.paramtext THEN 
  DO: 
    tolerance = vhp.paramtext.sprachcode. 
    curr-min = INTEGER(SUBSTR(STRING(time, "HH:MM:SS"),4,2)). 
    i = ROUND((time / 3600 - 0.5), 0). 
    IF i LE 0 THEN i = 24. 
    n = INTEGER(SUBSTR(vhp.paramtext.ptexte, i, 1)). 
    IF n = 2 THEN price = vhp.h-artikel.epreis2. 
    ELSE IF tolerance GT 0 THEN 
    DO: 
      IF i = 1 THEN j = 24. 
      ELSE j = i - 1. 
      IF INTEGER(SUBSTR(vhp.paramtext.ptexte, j, 1)) = 2 
        AND curr-min LE tolerance THEN price = vhp.h-artikel.epreis2. 
    END. 
  END. 
END. 

