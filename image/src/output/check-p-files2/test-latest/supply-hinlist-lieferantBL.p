
DEF INPUT PARAMETER lief-nr AS INT.
DEF OUTPUT PARAMETER from-supp AS CHAR.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
from-supp = l-lieferant.firma. 
