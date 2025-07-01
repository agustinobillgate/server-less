
DEFINE INPUT PARAMETER endkum AS INTEGER. 
DEFINE INPUT PARAMETER zwkum AS INTEGER. 
DEFINE OUTPUT PARAMETER new-artnr AS INTEGER INITIAL 0. 

DEFINE VARIABLE l-end AS INTEGER.
DEFINE VARIABLE l-zw  AS INTEGER.

l-end = LENGTH(STRING(endkum)).
l-zw  = LENGTH(STRING(zwkum)).


FOR EACH fa-artikel WHERE fa-artikel.subgrp = zwkum AND fa-artikel.gnr = endkum NO-LOCK:
    FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK NO-ERROR.
    IF AVAILABLE mathis THEN DO:
        IF INTEGER(SUBSTR(mathis.asset,1,l-end)) = endkum 
        AND INTEGER(SUBSTR(mathis.asset,4,l-zw)) = zwkum  THEN DO:
            new-artnr = INTEGER(mathis.asset) + 1.
            RETURN. 
        END.
    END.
END.
IF l-end = 1 AND l-zw = 1 THEN new-artnr =  endkum * 10000000 + zwkum * 10000 + 1.
ELSE IF l-end = 1 AND l-zw = 2 THEN new-artnr =  endkum * 10000000 + zwkum * 1000 + 1.
ELSE IF l-end = 1 AND l-zw = 3 THEN new-artnr =  endkum * 10000000 + zwkum * 100 + 1. 
ELSE IF l-end = 2 AND l-zw = 1 THEN new-artnr =  endkum * 1000000 + zwkum * 10000 + 1.
ELSE IF l-end = 2 AND l-zw = 2 THEN new-artnr =  endkum * 1000000 + zwkum * 1000 + 1.
ELSE IF l-end = 2 AND l-zw = 3 THEN new-artnr =  endkum * 1000000 + zwkum * 100 + 1.
ELSE IF l-end = 3 AND l-zw = 1 THEN new-artnr =  endkum * 100000 + zwkum * 10000 + 1.
ELSE IF l-end = 3 AND l-zw = 2 THEN new-artnr =  endkum * 100000 + zwkum * 1000 + 1.
ELSE IF l-end = 3 AND l-zw = 3 THEN new-artnr =  endkum * 100000 + zwkum * 100 + 1.

/*
DEFINE buffer fa-art1 FOR fa-artikel. 
DEFINE buffer mhis FOR mathis.


FOR EACH fa-art1 WHERE fa-art1.subgrp = zwkum AND fa-art1.gnr = endkum NO-LOCK BY INTEGER(mhis.asset) descending: 
      FIND FIRST mathis WHERE mathis.nr =   
      IF INTEGER(SUBSTR(mhis.asset,LENGTH(endkum))) = fa-art1.subgrp AND INTEGER(SUBSTR(mhis.asset,4)) = fa-art1.gnr THEN DO :
          new-artnr = INTEGER(mhis.asset) + 1.
      END.
      ELSE new-artnr =  endkum * 10000000 + zwkum * 10000 + 1.
    RETURN. 
END.

new-artnr =  endkum * 1000000 + zwkum * 10000 + 1.*/

/*MG 297CCD
FOR EACH mhis WHERE INTEGER(mhis.asset) = new-artnr NO-LOCK BY INTEGER(mhis.asset) descending: 
    new-artnr = INTEGER(mhis.asset) + 1.
    RETURN. 
END. 

new-artnr =  endkum * 10000\000 + zwkum * 10000 + 1.
*/
