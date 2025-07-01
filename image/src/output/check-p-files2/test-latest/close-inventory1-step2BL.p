
DEFINE INPUT PARAMETER inv-type  AS INT.
DEFINE INPUT PARAMETER m-endkum  AS INT.
DEFINE INPUT PARAMETER closedate AS DATE.

FOR EACH l-lager NO-LOCK: 
  RUN close-op(l-lager.lager-nr). 
END. 
RUN close-op(0). 


PROCEDURE close-op: 
  DEFINE INPUT PARAMETER lager-nr  AS INT.
  FIND FIRST l-op WHERE l-op.lager-nr = lager-nr 
    AND l-op.datum LE closedate AND l-op.op-art LE 5 NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE l-op: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE l-artikel THEN
    DO:
      FIND CURRENT l-op EXCLUSIVE-LOCK. 
      DELETE l-op. 
    END.
    ELSE IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO: 
      FIND CURRENT l-op EXCLUSIVE-LOCK. 
      IF (l-op.op-art GE 1 AND l-op.op-art LE 4) AND l-op.lager-nr NE 0 
        /*AND l-op.loeschflag NE 2*/ THEN RUN create-ophis. /* Modify by Michael @ 06/09/2018 to preserve cancel inventory history */
      DELETE l-op. 
    END. 
    FIND NEXT l-op WHERE l-op.lager-nr = lager-nr 
      AND l-op.datum LE closedate AND l-op.op-art LE 5 NO-LOCK NO-ERROR. 
  END. 
END. 



PROCEDURE create-ophhis: 

    /*MTIF CONNECTED ("vhparch") THEN
    DO:
        RUN closeinv-arch.p('cr-ophhis', RECID(l-ophdr), datum).
    END.
    ELSE
    DO:*/
        CREATE vhp.l-ophhis. 
        ASSIGN
            vhp.l-ophhis.datum      = l-ophdr.datum
            vhp.l-ophhis.op-typ     = l-ophdr.op-typ 
            vhp.l-ophhis.docu-nr    = l-ophdr.docu-nr 
            vhp.l-ophhis.lscheinnr  = l-ophdr.lscheinnr 
            vhp.l-ophhis.fibukonto  = l-ophdr.fibukonto
            . 
        FIND CURRENT vhp.l-ophhis NO-LOCK. 
    /*MTEND.*/
END. 

PROCEDURE create-ophis: 

    /** IF NOT CONNECTED("vhparch") THEN RUN vhparch-connect.p.

    IF CONNECTED("vhparch") THEN
    DO:
        RUN crophis-arch.p (l-op.lief-nr, l-op.lager-nr, l-op.artnr, l-op.op-art,
            l-op.datum, l-op.docu-nr, l-op.lscheinnr, l-op.anzahl,
            l-op.einzelpreis, l-op.warenwert, l-op.stornogrund, l-op.pos). 
    END.  
    */
    /*MTIF CONNECTED ("vhparch") THEN
    DO:
        RUN closeinv-arch.p('cr-ophis', RECID(l-op)).
    END.
    ELSE
    DO:*/
        CREATE vhp.l-ophis. 
        ASSIGN
            vhp.l-ophis.lief-nr     = l-op.lief-nr
            vhp.l-ophis.lager-nr    = l-op.lager-nr 
            vhp.l-ophis.artnr       = l-op.artnr
            vhp.l-ophis.op-art      = l-op.op-art 
            vhp.l-ophis.datum       = l-op.datum
            vhp.l-ophis.docu-nr     = l-op.docu-nr 
            vhp.l-ophis.lscheinnr   = l-op.lscheinnr 
            vhp.l-ophis.anzahl      = l-op.anzahl
            vhp.l-ophis.einzelpreis = l-op.einzelpreis 
            vhp.l-ophis.warenwert   = l-op.warenwert
            .
        
        IF l-op.op-art = 3 AND l-op.stornogrund NE "" THEN 
            vhp.l-ophis.fibukonto = l-op.stornogrund. 
        IF (l-op.op-art = 2 OR l-op.op-art = 4) THEN vhp.l-ophis.lief-nr = l-op.pos.
        IF l-op.loeschflag EQ 2 THEN ASSIGN l-ophis.fibukonto = l-op.stornogrund + ";CANCELLED". /* Add by Michael @ 06/09/2018 to preserve cancel inventory history */
        FIND CURRENT vhp.l-ophis NO-LOCK. 
    /*MTEND.*/
/**
  CREATE l-ophis. 
  ASSIGN
    l-ophis.lief-nr = l-op.lief-nr
    l-ophis.lager-nr = l-op.lager-nr 
    l-ophis.artnr = l-op.artnr
    l-ophis.op-art = l-op.op-art 
    l-ophis.datum = l-op.datum
    l-ophis.docu-nr = l-op.docu-nr 
    l-ophis.lscheinnr = l-op.lscheinnr 
    l-ophis.anzahl = l-op.anzahl
    l-ophis.einzelpreis = l-op.einzelpreis 
    l-ophis.warenwert = l-op.warenwert
  .
  
  IF l-op.op-art = 3 AND l-op.stornogrund NE "" THEN 
    l-ophis.fibukonto = l-op.stornogrund. 
  IF (l-op.op-art = 2 OR l-op.op-art = 4) THEN l-ophis.lief-nr = l-op.pos. 
  FIND CURRENT l-ophis NO-LOCK. 
*/
END. 
