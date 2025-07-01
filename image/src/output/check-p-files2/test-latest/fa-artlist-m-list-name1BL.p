
DEF INPUT  PARAMETER m-list-name        AS CHAR.
DEF OUTPUT PARAMETER mathis1-model      AS CHAR.
DEF OUTPUT PARAMETER mathis1-supplier   AS CHAR.
DEF OUTPUT PARAMETER do-it              AS LOGICAL INIT NO.

DEF BUFFER mathis1 FOR mathis.

DEF VAR fa-model AS CHARACTER.
DEF VAR fa-name  AS CHARACTER.

FIND FIRST mathis1 WHERE mathis1.name = m-list-name NO-LOCK NO-ERROR. 
IF AVAILABLE mathis1 THEN 
DO: 
    IF mathis1.model EQ ? OR TRIM(mathis1.model) EQ "" THEN
        fa-model = "".
    ELSE
        fa-model = mathis1.model + " - ".

    IF mathis1.name EQ ? THEN
        fa-name = "".
    ELSE
        fa-name = mathis1.name.

    mathis1-model = fa-model + fa-name. /* Oscar (18/12/2024) - 49983A - adding fix asset name */
    mathis1-supplier = mathis1.supplier.

    FIND FIRST fa-artikel WHERE fa-artikel.nr = mathis1.nr NO-LOCK.
    IF AVAILABLE fa-artikel THEN
    DO:
        IF fa-artikel.loeschflag EQ 0 THEN
        DO:
            do-it = YES.
        END.
    END.
END. 
