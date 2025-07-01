DEF TEMP-TABLE t-artikel LIKE artikel.
DEF TEMP-TABLE artikel-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart.

DEF INPUT  PARAMETER deptNo    AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE     FOR artikel-list.
DEF OUTPUT PARAMETER TABLE     FOR t-artikel.


FOR EACH artikel WHERE artikel.departement = deptno
    AND (artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 
         OR artikel.artart = 9):
    CREATE artikel-list.
    BUFFER-COPY artikel TO artikel-list.
END.
