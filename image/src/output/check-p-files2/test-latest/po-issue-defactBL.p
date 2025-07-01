
DEF INPUT PARAMETER stornogrund AS CHAR.
DEF INPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER avail-gl AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER cost-acct LIKE gl-acct.fibukonto.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = TRIM(stornogrund) 
  NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
DO: 
      cost-acct = gl-acct.fibukonto. 
      avail-gl = YES.
END. 
ELSE 
DO: 
  FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR. 
  IF AVAILABLE l-artikel THEN 
  DO: 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto 
          NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct AND 
          (gl-acct.acc-type = 2 OR gl-acct.acc-type = 5) THEN 
      DO: 
          cost-acct = gl-acct.fibukonto. 
          avail-gl = YES.
      END. 
  END. 
END. 
