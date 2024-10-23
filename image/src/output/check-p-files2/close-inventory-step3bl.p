DEF INPUT PARAMETER inv-type    AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER m-endkum    AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER closeDate   AS DATE     NO-UNDO.

DEF VARIABLE startDate          AS DATE     NO-UNDO.
DEF VARIABLE next-fDate         AS DATE     NO-UNDO.
DEF VARIABLE curr-artnr         AS INTEGER  NO-UNDO INIT 0.
DEF BUFFER lbuff                FOR l-besthis.
DEF BUFFER ltrans               FOR l-besthis.
DEF BUFFER l-bestand1           FOR l-bestand.

ASSIGN 
    startDate  = DATE(MONTH(closeDate), 1, YEAR(closeDate))
    next-fdate = closeDate + 1
.

FOR EACH l-ophis WHERE l-ophis.datum GE startDate 
    AND l-ophis.datum LE closeDate 
    AND (l-ophis.op-art GE 1 AND l-ophis.op-art LE 4) NO-LOCK
    BY l-ophis.artnr BY l-ophis.datum BY l-ophis.op-art:    
  IF curr-artnr NE l-ophis.artnr THEN
  DO:
    ASSIGN curr-artnr = l-ophis.artnr.
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK.
  END.
  IF (inv-type = 1 AND l-artikel.endkum LT m-endkum) 
    OR (inv-type = 2 AND l-artikel.endkum GE m-endkum) 
    OR (inv-type = 3) THEN 
  DO TRANSACTION:
    FIND FIRST  l-besthis WHERE l-besthis.anf-best-dat GE startDate 
        AND l-besthis.anf-best-dat LE closeDate 
        AND l-besthis.artnr = l-ophis.artnr
        AND l-besthis.lager-nr = l-ophis.lager-nr NO-ERROR.
    IF NOT AVAILABLE l-besthis THEN
    DO:
        CREATE l-besthis.
        ASSIGN
          l-besthis.artnr = l-ophis.artnr
          l-besthis.anf-best-dat = startDate
          l-besthis.lager-nr = l-ophis.lager-nr
        .
    END.
    FIND FIRST  lbuff WHERE lbuff.anf-best-dat GE startDate 
        AND lbuff.anf-best-dat LE closeDate 
        AND lbuff.artnr = l-ophis.artnr
        AND lbuff.lager-nr = 0 NO-ERROR.
    IF NOT AVAILABLE lbuff THEN
    DO:
        CREATE lbuff.
        ASSIGN
            lbuff.artnr = l-ophis.artnr
            lbuff.anf-best-dat = startDate
            lbuff.lager-nr = 0
          .
    END.
    IF l-ophis.op-art = 1 THEN 
    ASSIGN
        l-besthis.anz-eingang  = l-besthis.anz-eingang + l-ophis.anzahl
        lbuff.anz-eingang  = lbuff.anz-eingang + l-ophis.anzahl
        lbuff.wert-eingang = lbuff.wert-eingang + l-ophis.warenwert
    .
    ELSE IF l-ophis.op-art = 2 THEN
    DO:
        FIND FIRST  ltrans WHERE ltrans.anf-best-dat GE startDate 
          AND ltrans.anf-best-dat LE closeDate 
          AND ltrans.artnr = l-ophis.artnr
          AND ltrans.lager-nr = l-ophis.lief-nr NO-ERROR.
        IF NOT AVAILABLE ltrans THEN
        DO:
          CREATE ltrans.
          ASSIGN
            ltrans.artnr = l-ophis.artnr
            ltrans.anf-best-dat = startDate
            ltrans.lager-nr = l-ophis.lief-nr
          .
        END.
        ASSIGN
            l-besthis.anz-eingang = l-besthis.anz-eingang + l-ophis.anzahl
            ltrans.anz-ausgang = ltrans.anz-ausgang + l-ophis.anzahl            
        .
    END.
    ELSE IF l-ophis.op-art = 3 THEN
    ASSIGN
        l-besthis.anz-ausgang  = l-besthis.anz-ausgang + l-ophis.anzahl
        lbuff.anz-ausgang  = lbuff.anz-ausgang + l-ophis.anzahl
        lbuff.wert-ausgang = lbuff.wert-ausgang + l-ophis.warenwert
    .
    ELSE IF l-ophis.op-art = 4 THEN
        ASSIGN lbuff.anz-ausgang  = lbuff.anz-ausgang + l-ophis.anzahl
    .
  END. /* transaction */
END.

DO TRANSACTION:
    FOR EACH l-besthis WHERE l-besthis.anf-best-dat GE startDate 
        AND l-besthis.anf-best-dat LE closeDate 
        AND l-besthis.lager-nr = 0
        AND l-besthis.anz-anf-best = 0: 
        FOR EACH lbuff WHERE lbuff.artnr = l-besthis.artnr
            AND lbuff.anf-best-dat = l-besthis.anf-best-dat:
            ASSIGN
                lbuff.anz-anf-best = 0
                lbuff.val-anf-best = 0
            .
        END.
    END.
END.

ASSIGN curr-artnr = 0.
FOR EACH l-besthis WHERE l-besthis.anf-best-dat GE startDate 
    AND l-besthis.anf-best-dat LE closeDate NO-LOCK 
    BY l-besthis.artnr BY l-besthis.lager-nr:
  IF curr-artnr NE l-besthis.artnr THEN
  DO:
    ASSIGN curr-artnr = l-besthis.artnr.
    FIND FIRST l-artikel WHERE l-artikel.artnr = curr-artnr NO-LOCK.
  END.
  IF (inv-type = 1 AND l-artikel.endkum LT m-endkum) 
      OR (inv-type = 2 AND l-artikel.endkum GE m-endkum) 
      OR (inv-type = 3) THEN 
  DO TRANSACTION:
    FIND FIRST l-bestand WHERE l-bestand.artnr = l-besthis.artnr
        AND l-bestand.lager-nr = l-besthis.lager-nr
        AND l-bestand.anf-best-dat = next-fdate NO-ERROR.  
    IF NOT AVAILABLE l-bestand THEN CREATE l-bestand.
    ASSIGN
      l-bestand.artnr        = l-besthis.artnr
      l-bestand.anf-best-dat = next-fdate
      l-bestand.lager-nr     = l-besthis.lager-nr
      l-bestand.anz-anf-best = l-besthis.anz-anf-best 
          + l-besthis.anz-eingang - l-besthis.anz-ausgang
      l-bestand.val-anf-best = l-besthis.val-anf-best
          + l-besthis.wert-eingang - l-besthis.wert-ausgang
    .
    IF l-bestand.lager-nr GT 0 
        AND l-bestand.anz-anf-best NE 0 THEN
    DO:
      FIND FIRST l-bestand1 WHERE l-bestand1.artnr = l-bestand.artnr
          AND l-bestand1.anf-best-dat = l-bestand.anf-best-dat
          AND l-bestand1.lager-nr = 0 NO-LOCK.
      IF l-bestand1.anz-anf-best NE 0 THEN
      ASSIGN l-bestand.val-anf-best = l-bestand1.val-anf-best
          * l-bestand.anz-anf-best / l-bestand1.anz-anf-best.
    END.
    FIND CURRENT l-bestand NO-LOCK.
    RELEASE l-bestand.
  END. /* transaction */
END.
