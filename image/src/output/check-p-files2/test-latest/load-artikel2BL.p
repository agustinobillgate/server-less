DEF TEMP-TABLE t-artikel LIKE artikel.

DEF INPUT  PARAMETER case-type AS INTEGER   NO-UNDO.
DEF INPUT  PARAMETER int1      AS INTEGER   NO-UNDO.
DEF INPUT  PARAMETER int2      AS INTEGER   NO-UNDO.
DEF INPUT  PARAMETER int3      AS INTEGER   NO-UNDO.
DEF INPUT  PARAMETER int4      AS INTEGER   NO-UNDO.
DEF INPUT  PARAMETER int5      AS INTEGER   NO-UNDO.
DEF INPUT  PARAMETER char1     AS CHARACTER NO-UNDO.

DEF OUTPUT PARAMETER TABLE     FOR t-artikel.


CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH artikel WHERE (artikel.artart = int1 OR artikel.artart = int2)
            AND artikel.artnr GE int3 AND artikel.artnr LE int4
            AND artikel.departement = int5
            NO-LOCK BY (STRING(artikel.artart) + STRING(artikel.artnr,"9999")):
            CREATE t-artikel.
            BUFFER-COPY artikel TO t-artikel.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = int1 
            AND artikel.artart = int2 AND artikel.activeflag NO-LOCK:
            CREATE t-artikel.
            BUFFER-COPY artikel TO t-artikel.
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = int1 
            AND artikel.artart = int2
            AND artikel.artnr GE int3
            AND artikel.activeflag NO-LOCK:
            CREATE t-artikel.
            BUFFER-COPY artikel TO t-artikel.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = int1 
            AND artikel.artart = int2
            AND artikel.bezeich GE char1
            AND artikel.activeflag NO-LOCK:
            CREATE t-artikel.
            BUFFER-COPY artikel TO t-artikel.
        END.
    END.
END CASE.
