
DEFINE TEMP-TABLE t-artikel LIKE artikel.

DEFINE INPUT PARAMETER dept AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.

FOR EACH artikel WHERE artikel.departement = dept 
  AND artikel.artart = 0 AND artikel.activeflag = YES NO-LOCK 
  BY artikel.artnr:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.
