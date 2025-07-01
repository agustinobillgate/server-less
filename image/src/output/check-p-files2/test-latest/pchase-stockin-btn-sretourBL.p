
DEF INPUT PARAMETER q2-list-lief-nr AS INT.
DEF INPUT PARAMETER q2-list-docu-nr AS CHAR.
DEF OUTPUT PARAMETER avail-l-kredit AS LOGICAL INIT NO.

FIND FIRST l-kredit WHERE l-kredit.lief-nr = q2-list-lief-nr
  AND l-kredit.name = q2-list-docu-nr AND l-kredit.zahlkonto GT 0 
  NO-LOCK NO-ERROR.
IF AVAILABLE l-kredit THEN avail-l-kredit = YES.
