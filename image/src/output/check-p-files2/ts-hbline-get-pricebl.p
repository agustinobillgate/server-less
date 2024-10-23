

DEF INPUT  PARAMETER art-list-artnr AS INT.
DEF INPUT  PARAMETER dept   AS INT.
DEF OUTPUT PARAMETER err    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER err1   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER price  AS DECIMAL INITIAL 0. 
DEF OUTPUT PARAMETER fract  AS DECIMAL INITIAL 1.

RUN get-price. 

PROCEDURE get-price: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE tolerance AS INTEGER. 
DEFINE VARIABLE curr-min  AS INTEGER. 

  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = art-list-artnr 
    AND vhp.h-artikel.departement = dept NO-LOCK.

  price = vhp.h-artikel.epreis1. 
  IF price = 0 THEN 
  DO:
    err = YES.
    /*MT
    RUN TS-getprice.p(OUTPUT price). 
    IF price = -999999999 THEN RETURN.
    */
    RETURN.
  END.
  
  IF vhp.h-artikel.epreis2 NE 0 THEN
  DO:
    FIND FIRST vhp.paramtext WHERE vhp.paramtext.txtnr = (10000 + dept) 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.paramtext THEN 
    DO: 
      tolerance = vhp.paramtext.sprachcode. 
      curr-min = INTEGER(SUBSTR(STRING(time, "HH:MM:SS"),4,2)). 
      i = ROUND((time / 3600 - 0.5), 0). 
      IF i LE 0 THEN i = 24. 
      n = INTEGER(SUBSTR(paramtext.ptexte, i, 1)). 
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

  IF price NE 0 AND vhp.h-artikel.gang = 1 THEN
  DO:
    err1 = YES.
    /*MTRUN TS-getfractUI.p(price, OUTPUT fract). 
    price = price * fract. */
    RETURN.
  END.
END. 
