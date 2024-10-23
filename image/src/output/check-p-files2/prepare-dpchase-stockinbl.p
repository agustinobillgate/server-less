DEFINE TEMP-TABLE q2-list
    FIELD docu-nr       LIKE l-op.docu-nr
    FIELD lief-nr       LIKE l-op.lief-nr
    FIELD loeschflag    LIKE l-op.loeschflag
    FIELD lscheinnr     LIKE l-op.lscheinnr
    FIELD lager-nr      LIKE l-op.lager-nr
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD einzelpreis   LIKE l-op.einzelpreis
    FIELD anzahl        LIKE l-op.anzahl
    FIELD warenwert     LIKE l-op.warenwert
    FIELD firma         LIKE l-lieferant.firma
    FIELD datum         LIKE l-op.datum.

DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER heute AS DATE.
DEF OUTPUT PARAMETER beg-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
heute = billdate. 

FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
beg-date = DATE(month(fdate), 1, year(fdate)). 

FOR EACH l-op WHERE /*MTl-op.docu-nr GE ponum 
    AND*/ l-op.docu-nr = l-op.lscheinnr AND l-op.datum = billdate 
    /*MTAND l-op.loeschflag = 0*/ AND NOT l-op.flag 
    AND l-op.op-art = 1 AND l-op.pos GE 1 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.docu-nr:
    CREATE q2-list.
    ASSIGN
      q2-list.docu-nr       = l-op.docu-nr
      q2-list.lief-nr       = l-op.lief-nr
      q2-list.loeschflag    = l-op.loeschflag
      q2-list.lscheinnr     = l-op.lscheinnr
      q2-list.lager-nr      = l-op.lager-nr
      q2-list.artnr         = l-artikel.artnr
      q2-list.bezeich       = l-artikel.bezeich
      q2-list.einzelpreis   = l-op.einzelpreis
      q2-list.anzahl        = l-op.anzahl
      q2-list.warenwert     = l-op.warenwert
      q2-list.firma         = l-lieferant.firma
      q2-list.datum         = l-op.datum.
END.
