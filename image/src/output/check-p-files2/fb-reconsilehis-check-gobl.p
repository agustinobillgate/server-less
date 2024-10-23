
DEF INPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER avail-l-besthis AS LOGICAL INIT NO.

FIND FIRST l-besthis WHERE l-besthis.anf-best-dat = from-date NO-LOCK NO-ERROR.
IF AVAILABLE l-besthis THEN avail-l-besthis = YES.
