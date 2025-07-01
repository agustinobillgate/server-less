
DEF TEMP-TABLE t-budget      LIKE budget.
DEF TEMP-TABLE t-artikel  LIKE artikel.

DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-budget.

FOR EACH artikel WHERE artikel.departement = dept 
    AND (artikel.artart = 0 OR artart = 8) NO-LOCK BY artikel.bezeich:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.

FIND FIRST t-artikel NO-ERROR.
IF AVAILABLE t-artikel THEN 
    RUN article-budget-disp-itbl.p
        (t-artikel.departement, t-artikel.artnr, from-date, to-date,
         OUTPUT TABLE t-budget).
