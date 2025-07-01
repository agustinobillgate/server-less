
DEF INPUT  PARAMETER lief-nr AS INTEGER.
DEF OUTPUT PARAMETER firma   AS CHAR.
DEF OUTPUT PARAMETER fdate   AS DATE.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK.
firma = l-lieferant.firma.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
fdate = htparam.fdate.
