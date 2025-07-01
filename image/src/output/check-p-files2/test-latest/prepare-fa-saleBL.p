
DEF INPUT  PARAMETER nr             AS INT.
DEF OUTPUT PARAMETER last-close     AS DATE.
DEF OUTPUT PARAMETER datum          AS DATE.
DEF OUTPUT PARAMETER qty            AS INT.
DEF OUTPUT PARAMETER amt            AS DECIMAL.
DEF OUTPUT PARAMETER mathis-name    AS CHAR.
DEF OUTPUT PARAMETER mathis-asset      LIKE mathis.asset.
DEF OUTPUT PARAMETER fa-artikel-anzahl AS INT.

FIND FIRST htparam WHERE paramnr = 558 no-lock. /* LAST Accounting Period */ 
/* last-close = fdate. */       /* Rulita 211024 | Fixing for serverless */
last-close = htparam.fdate.               
FIND FIRST htparam WHERE paramnr = 372 no-lock.   /* journal posting DATE */ 
datum = htparam.fdate. 

FIND FIRST fa-artikel WHERE fa-artikel.nr = nr NO-LOCK. 
  qty = fa-artikel.anzahl. 
  amt = fa-artikel.book-wert. 
  fa-artikel-anzahl = fa-artikel.anzahl.

FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK. 
mathis-name       = mathis.name.
mathis-asset      = mathis.asset.

