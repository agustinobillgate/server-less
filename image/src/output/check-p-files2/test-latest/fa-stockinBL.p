
DEFINE TEMP-TABLE q2-list
    FIELD lscheinnr     LIKE fa-op.lscheinnr
    FIELD name          LIKE mathis.name
    FIELD location      LIKE mathis.location
    FIELD einzelpreis   LIKE fa-op.einzelpreis
    FIELD anzahl        LIKE fa-op.anzahl
    FIELD warenwert     LIKE fa-op.warenwert
    FIELD firma         LIKE l-lieferant.firma
    FIELD datum         LIKE fa-op.datum
    FIELD docu-nr       LIKE fa-op.docu-nr
    FIELD lief-nr       LIKE fa-op.lief-nr
    FIELD rec-id        AS INT.

DEFINE INPUT PARAMETER ponum          AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER billdate       AS DATE NO-UNDO.
DEFINE INPUT PARAMETER todate         AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR q2-list.

/* FD Comment
FOR EACH fa-op NO-LOCK WHERE 
    fa-op.opart = 1 AND
    fa-op.docu-nr GE ponum /*AND 
    fa-op.docu-nr = fa-op.lscheinnr*/ AND
    fa-op.datum GE billdate AND fa-op.datum LE todate AND
    fa-op.loeschflag LE 1, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK, 
    FIRST mathis WHERE mathis.nr = fa-op.nr 
    NO-LOCK BY fa-op.datum BY fa-op.docu-nr:
    CREATE q2-list.
    ASSIGN
        q2-list.lscheinnr     = fa-op.lscheinnr
        q2-list.name          = mathis.name
        q2-list.location      = mathis.location
        q2-list.einzelpreis   = fa-op.einzelpreis
        q2-list.anzahl        = fa-op.anzahl
        q2-list.warenwert     = fa-op.warenwert
        q2-list.firma         = l-lieferant.firma
        q2-list.datum         = fa-op.datum
        q2-list.docu-nr       = fa-op.docu-nr
        q2-list.lief-nr       = fa-op.lief-nr
        q2-list.rec-id        = RECID(fa-op).
END.
*/

/*FD Nov 21, 2022 => Ticket A80699*/
IF ponum EQ "" THEN
DO:
    FOR EACH fa-op NO-LOCK WHERE fa-op.opart = 1 
        AND fa-op.lscheinnr GE ponum 
        AND fa-op.datum GE billdate AND fa-op.datum LE todate 
        AND fa-op.loeschflag LE 1, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-op.lief-nr NO-LOCK, 
        FIRST mathis WHERE mathis.nr EQ fa-op.nr 
        NO-LOCK BY fa-op.datum BY fa-op.docu-nr:
    
        CREATE q2-list.
        ASSIGN
        q2-list.lscheinnr     = fa-op.lscheinnr
        q2-list.name          = mathis.name
        q2-list.location      = mathis.location
        q2-list.einzelpreis   = fa-op.einzelpreis
        q2-list.anzahl        = fa-op.anzahl
        q2-list.warenwert     = fa-op.warenwert
        q2-list.firma         = l-lieferant.firma
        q2-list.datum         = fa-op.datum
        q2-list.docu-nr       = fa-op.docu-nr
        q2-list.lief-nr       = fa-op.lief-nr
        q2-list.rec-id        = RECID(fa-op).
    END.
END.
ELSE
DO:
    FOR EACH fa-op NO-LOCK WHERE fa-op.opart = 1 
        AND fa-op.lscheinnr EQ ponum 
        AND fa-op.datum GE billdate AND fa-op.datum LE todate 
        AND fa-op.loeschflag LE 1, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-op.lief-nr NO-LOCK, 
        FIRST mathis WHERE mathis.nr EQ fa-op.nr 
        NO-LOCK BY fa-op.datum BY fa-op.docu-nr:
    
        CREATE q2-list.
        ASSIGN
        q2-list.lscheinnr     = fa-op.lscheinnr
        q2-list.name          = mathis.name
        q2-list.location      = mathis.location
        q2-list.einzelpreis   = fa-op.einzelpreis
        q2-list.anzahl        = fa-op.anzahl
        q2-list.warenwert     = fa-op.warenwert
        q2-list.firma         = l-lieferant.firma
        q2-list.datum         = fa-op.datum
        q2-list.docu-nr       = fa-op.docu-nr
        q2-list.lief-nr       = fa-op.lief-nr
        q2-list.rec-id        = RECID(fa-op).
    END.
END.
