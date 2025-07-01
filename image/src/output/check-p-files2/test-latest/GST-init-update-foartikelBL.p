
DEF INPUT PARAMETER t-artnr  AS INT.
DEF INPUT PARAMETER dept     AS INT.
DEF INPUT PARAMETER bez      AS CHAR.

FIND FIRST artikel WHERE artikel.artnr = t-artnr AND artikel.departement = dept EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE artikel THEN
DO:
    ASSIGN
        artikel.bezeich2 = bez
        .
END.
