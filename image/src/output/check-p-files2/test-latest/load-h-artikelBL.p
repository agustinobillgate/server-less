DEF TEMP-TABLE t-h-artikel LIKE h-artikel.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER dept      AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER artType   AS INTEGER NO-UNDO. 
DEF OUTPUT PARAMETER TABLE     FOR t-h-artikel.

IF case-type = 1 THEN
FOR EACH h-artikel WHERE h-artikel.departement = dept 
    AND h-artikel.artart = artType 
    AND h-artikel.activeflag NO-LOCK:
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
END.

ELSE IF case-type = 2 THEN
FOR EACH h-artikel WHERE h-artikel.departement = dept 
    AND (h-artikel.artart = 2 OR h-artikel.artart = 7) 
    AND h-artikel.activeflag NO-LOCK:
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
END.

ELSE IF case-type = 3 THEN
FOR EACH h-artikel WHERE h-artikel.departement = dept NO-LOCK:
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
END.
