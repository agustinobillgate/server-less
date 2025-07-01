
DEF TEMP-TABLE q1-list
    FIELD lscheinnr     LIKE fa-op.lscheinnr
    FIELD name          LIKE mathis.name
    FIELD location      LIKE mathis.location
    FIELD einzelpreis   LIKE fa-op.einzelpreis
    FIELD anzahl        LIKE fa-op.anzahl
    FIELD warenwert     LIKE fa-op.warenwert
    FIELD firma         LIKE l-lieferant.firma
    FIELD datum         LIKE fa-op.datum.

DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH fa-op WHERE 
    fa-op.datum GE from-date AND fa-op.datum LE to-date
    AND fa-op.loeschflag = 2 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK, 
    FIRST mathis WHERE mathis.nr = fa-op.nr 
    NO-LOCK BY fa-op.docu-nr:
    CREATE q1-list.
    ASSIGN
    q1-list.lscheinnr     = fa-op.lscheinnr
    q1-list.name          = mathis.name
    q1-list.location      = mathis.location
    q1-list.einzelpreis   = fa-op.einzelpreis
    q1-list.anzahl        = fa-op.anzahl
    q1-list.warenwert     = fa-op.warenwert
    q1-list.firma         = l-lieferant.firma
    q1-list.datum         = fa-op.datum.
END.
