
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

DEFINE INPUT PARAMETER fromdate   AS DATE.
DEFINE INPUT PARAMETER todate     AS DATE.
DEFINE INPUT PARAMETER searchby   AS INTEGER.
DEFINE INPUT PARAMETER devnote-no AS CHARACTER.
DEFINE INPUT PARAMETER po-no      AS CHARACTER.
DEFINE INPUT PARAMETER supp-no    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR q2-list.

IF (devnote-no = "" AND po-no = "" AND supp-no = 0) OR searchby = ? OR 
   (searchby = 1 AND devnote-no = "") OR
   (searchby = 2 AND po-no = "") OR 
   (searchby = 3 AND supp-no = 0) THEN
    FOR EACH fa-op NO-LOCK WHERE 
        fa-op.opart = 1 AND
        fa-op.datum GE fromdate AND fa-op.datum LE todate AND
        fa-op.loeschflag LE 1, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK, 
        FIRST mathis WHERE mathis.nr = fa-op.nr 
        NO-LOCK BY fa-op.datum BY fa-op.docu-nr:
        RUN create-q2-list.                     
    END.
ELSE IF searchby = 1 AND devnote-no NE "" THEN
    FOR EACH fa-op NO-LOCK WHERE 
        fa-op.opart = 1 AND
        fa-op.datum GE fromdate AND fa-op.datum LE todate AND
        fa-op.loeschflag LE 1 AND
        fa-op.lscheinnr = devnote-no, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK, 
        FIRST mathis WHERE mathis.nr = fa-op.nr 
        NO-LOCK BY fa-op.datum BY fa-op.docu-nr:
        RUN create-q2-list.                     
    END.
ELSE IF searchby = 2 AND po-no NE "" THEN
    FOR EACH fa-op NO-LOCK WHERE 
        fa-op.opart = 1 AND
        fa-op.datum GE fromdate AND fa-op.datum LE todate AND
        fa-op.loeschflag LE 1 AND
        fa-op.docu-nr = po-no, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK, 
        FIRST mathis WHERE mathis.nr = fa-op.nr 
        NO-LOCK BY fa-op.datum BY fa-op.docu-nr:
        RUN create-q2-list.                     
    END.
ELSE IF searchby = 3 AND supp-no NE 0 THEN
    FOR EACH fa-op NO-LOCK WHERE 
        fa-op.opart = 1 AND
        fa-op.datum GE fromdate AND fa-op.datum LE todate AND
        fa-op.loeschflag LE 1 AND
        fa-op.lief-nr = supp-no, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK, 
        FIRST mathis WHERE mathis.nr = fa-op.nr 
        NO-LOCK BY fa-op.datum BY fa-op.docu-nr:
        RUN create-q2-list.                     
    END.

PROCEDURE create-q2-list:
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
