
DEF INPUT  PARAMETER t-artnr        AS INT.
DEF INPUT  PARAMETER balance        AS DECIMAL.
DEF OUTPUT PARAMETER exrate         AS DECIMAL.
DEF OUTPUT PARAMETER price          AS DECIMAL.
DEF OUTPUT PARAMETER msg            AS INT INIT 0.

DEF BUFFER w1 FOR waehrung.

FIND FIRST artikel WHERE artnr = t-artnr NO-LOCK.
FIND FIRST w1 WHERE w1.waehrungsnr = artikel.betriebsnr NO-LOCK NO-ERROR. 
IF AVAILABLE w1 THEN exrate = w1.ankauf / w1.einheit. 
ELSE 
DO: 
    msg = 1.
    /*MT
    hide MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Currency Number of selected Artikel not defined.",lvCAREA,"") 
    VIEW-AS ALERT-BOX WARNING. 
    exrate = 1. 
    */
END. 
price = - balance / exrate. 
