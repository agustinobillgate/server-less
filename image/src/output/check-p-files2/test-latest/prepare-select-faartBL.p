
DEF TEMP-TABLE q1-list
    FIELD name      LIKE mathis.name
    FIELD nr        LIKE mathis.nr
    FIELD asset     LIKE mathis.asset
    FIELD warenwert LIKE fa-artikel.warenwert
    FIELD anzahl    LIKE fa-artikel.anzahl.

DEF INPUT PARAMETER name AS CHAR.
DEF INPUT PARAMETER nr   AS INT.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH mathis WHERE mathis.name GE name 
    AND mathis.flag = 2 AND mathis.nr NE nr NO-LOCK, 
    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
    AND fa-artikel.loeschflag = 0 AND fa-artikel.warenwert GT 0 
    AND fa-artikel.depn-wert = 0 NO-LOCK BY mathis.name 
    BY mathis.asset:
    CREATE q1-list.
    ASSIGN
    q1-list.name      = mathis.name
    q1-list.nr        = mathis.nr
    q1-list.asset     = mathis.asset
    q1-list.warenwert = fa-artikel.warenwert
    q1-list.anzahl    = fa-artikel.anzahl.
END.
