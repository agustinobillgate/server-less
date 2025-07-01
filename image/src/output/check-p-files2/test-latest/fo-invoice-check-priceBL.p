
DEF INPUT-OUTPUT PARAMETER l-price AS DECIMAL.
DEF INPUT PARAMETER t-artnr AS INT.
DEF INPUT PARAMETER t-departement AS INT.

DEFINE BUFFER w1 FOR waehrung. 

FIND FIRST artikel WHERE artikel.artnr = t-artnr
    AND artikel.departement = t-departement NO-LOCK.
FIND FIRST w1 WHERE w1.waehrungsnr = artikel.betriebsnr NO-LOCK NO-ERROR. 
IF AVAILABLE w1 THEN l-price = l-price * w1.ankauf / w1.einheit.
