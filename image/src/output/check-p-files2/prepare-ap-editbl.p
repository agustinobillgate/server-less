
DEF TEMP-TABLE t-l-kredit LIKE l-kredit.

DEF INPUT  PARAMETER recid-ap AS INT.
DEF OUTPUT PARAMETER firma LIKE l-lieferant.firma.
DEF OUTPUT PARAMETER lief-nr LIKE l-lieferant.lief-nr.
DEF OUTPUT PARAMETER TABLE FOR t-l-kredit.

FIND FIRST l-kredit WHERE RECID(l-kredit) = recid-ap NO-LOCK. 
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK.

CREATE t-l-kredit.
BUFFER-COPY l-kredit TO t-l-kredit.

firma = l-lieferant.firma.
lief-nr = l-lieferant.lief-nr.
