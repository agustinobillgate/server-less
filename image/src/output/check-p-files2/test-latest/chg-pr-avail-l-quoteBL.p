
DEF INPUT  PARAMETER s-list-artnr  AS INT.
DEF OUTPUT PARAMETER avail-l-quote AS LOGICAL INIT NO.

FIND FIRST l-quote WHERE l-quote.artnr = s-list-artnr AND l-quote.lief-nr NE 0
    NO-LOCK NO-ERROR.
IF AVAILABLE l-quote THEN
    avail-l-quote = YES.
