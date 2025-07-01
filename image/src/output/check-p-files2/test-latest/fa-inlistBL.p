
DEFINE TEMP-TABLE output-list
    FIELD datum         LIKE fa-op.datum
    FIELD nr            LIKE mathis.nr
    FIELD NAME          LIKE mathis.NAME
    FIELD anzahl        LIKE fa-op.anzahl
    FIELD einzelpreis   LIKE fa-op.einzelpreis
    FIELD warenwert     LIKE fa-op.warenwert
    FIELD lscheinnr     LIKE fa-op.lscheinnr.

DEF INPUT  PARAMETER lief-nr   AS INT.
DEF INPUT  PARAMETER docu-nr   AS CHAR.
DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER t-firma   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR output-list.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
t-firma = l-lieferant.firma.
 
FOR EACH fa-op WHERE fa-op.datum GE from-date AND fa-op.datum LE to-date 
    AND fa-op.loeschflag = 0 AND fa-op.lief-nr = lief-nr 
    AND fa-op.docu-nr = docu-nr NO-LOCK,
    FIRST mathis WHERE mathis.nr = fa-op.nr NO-LOCK 
    BY fa-op.datum BY fa-op.nr: 

    CREATE output-list.
    ASSIGN
    output-list.datum         = fa-op.datum
    output-list.nr            = mathis.nr
    output-list.NAME          = mathis.NAME
    output-list.anzahl        = fa-op.anzahl
    output-list.einzelpreis   = fa-op.einzelpreis
    output-list.warenwert     = fa-op.warenwert
    output-list.lscheinnr     = fa-op.lscheinnr.

END. 
