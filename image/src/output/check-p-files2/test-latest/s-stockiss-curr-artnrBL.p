
DEF INPUT PARAMETER fibu AS CHAR.
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER avail-gl AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER stock-oh AS DECIMAL.
DEF OUTPUT PARAMETER cost-acct AS CHAR.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct AND (gl-acct.acc-type = 2 OR gl-acct.acc-type = 5) THEN 
DO: 
  cost-acct = gl-acct.fibukonto. 
  avail-gl = YES.
END. 

FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
IF AVAILABLE l-bestand THEN 
stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
  - l-bestand.anz-ausgang. 
ELSE stock-oh = 0. 
