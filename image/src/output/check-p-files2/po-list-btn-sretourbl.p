
DEF INPUT PARAMETER l-orderhdr-lief-nr AS INT.
DEF INPUT PARAMETER l-orderhdr-docu-nr AS CHAR.

DEF OUTPUT PARAMETER avail-l-kredit AS LOGICAL INIT NO.

FIND FIRST l-kredit WHERE l-kredit.lief-nr = l-orderhdr-lief-nr 
    AND l-kredit.name = l-orderhdr-docu-nr AND l-kredit.zahlkonto GT 0 
    NO-LOCK NO-ERROR.
IF AVAILABLE l-kredit THEN avail-l-kredit = YES.
