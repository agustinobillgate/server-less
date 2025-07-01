
DEF INPUT PARAMETER location-str AS CHAR.
DEF INPUT PARAMETER qty          AS INT.
DEF INPUT PARAMETER user-init    AS CHAR.
DEF INPUT PARAMETER artnr        AS INT.
DEFINE OUTPUT PARAMETER anz1     AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER anz2     AS INTEGER INITIAL 0.

FIND FIRST mathis WHERE mathis.nr = artnr NO-LOCK.
FIND FIRST fa-artikel WHERE fa-artikel.nr = artnr NO-LOCK.

RUN move-it.

PROCEDURE move-it:
DEF BUFFER   fabuff   FOR fa-artikel.
DEF BUFFER   mabuff   FOR mathis.
DEF VARIABLE found    AS LOGICAL INITIAL NO.
DEF VARIABLE billdate AS DATE.

  FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
  billdate = htparam.fdate. 

  FOR EACH mabuff WHERE mabuff.NAME = mathis.NAME
    AND mabuff.location NE mathis.location 
    AND mabuff.asset = mathis.asset 
    AND mabuff.location EQ location-str NO-LOCK:
    FIND FIRST fabuff WHERE fabuff.nr = mabuff.nr NO-LOCK.
    IF fabuff.katnr      = fa-artikel.katnr   AND
       fabuff.gnr        = fa-artikel.gnr     AND
       fabuff.subgrp     = fa-artikel.subgrp  AND
       fabuff.anz-depn   = fa-artikel.anz-dep AND
       fabuff.loeschflag = 0                  AND
       RECID(fabuff) NE RECID(fa-artikel) THEN
    DO:
      found = YES.
      LEAVE.
    END.
  END.
  IF found THEN
  DO:
    CREATE fa-op. 
    ASSIGN
      fa-op.nr            = mathis.nr
      fa-op.opart         = 2 
      fa-op.datum         = billdate 
      fa-op.zeit          = TIME 
      fa-op.anzahl        = qty
      fa-op.einzelpreis   = fa-artikel.book-wert / fa-artikel.anzahl 
      fa-op.warenwert     = fa-op.einzelpreis * qty
      fa-op.id            = user-init
      fa-op.docu-nr       = mathis.NAME + ";;"
                          + mathis.location + ";;"
                          + location-str + ";;" 
                          + "YES" + ";;"
                          + STRING(YEAR(TODAY)) + STRING(MONTH(TODAY),"99")
                          + STRING(DAY(TODAY),"99") + ";;"
    .
    FIND CURRENT fa-op NO-LOCK.
    RELEASE fa-op. 
    
    FIND CURRENT fabuff EXCLUSIVE-LOCK.
    FIND CURRENT fa-artikel EXCLUSIVE-LOCK.
    IF fa-artikel.anzahl = qty THEN
    ASSIGN
        fabuff.warenwert = fabuff.warenwert + fa-artikel.warenwert
        fabuff.book-wert = fabuff.book-wert + fa-artikel.book-wert
        fabuff.depn-wert = fabuff.depn-wert + fa-artikel.depn-wert 
        fabuff.anzahl    = fabuff.anzahl    + qty
        fabuff.anz100    = fabuff.anzahl    + qty
        fabuff.cid       = user-init
        fabuff.changed   = TODAY
        fa-artikel.loeschflag = 1
        fa-artikel.deleted    = TODAY.
    ELSE
    DO:
      ASSIGN
        fabuff.warenwert = fabuff.warenwert 
          + fa-artikel.warenwert * qty / fa-artikel.anzahl
        fabuff.book-wert = fabuff.book-wert 
          + fa-artikel.book-wert * qty / fa-artikel.anzahl
        fabuff.depn-wert = fabuff.depn-wert 
          + fa-artikel.depn-wert * qty / fa-artikel.anzahl
        fabuff.anzahl    = fabuff.anzahl + qty
        fabuff.anz100    = fabuff.anzahl + qty
      .
      ASSIGN
        fa-artikel.warenwert = fa-artikel.warenwert *
          (1 - qty / fa-artikel.anzahl)
        fa-artikel.book-wert = fa-artikel.book-wert *
          (1 - qty / fa-artikel.anzahl)
        fa-artikel.depn-wert = fa-artikel.depn-wert *
          (1 - qty / fa-artikel.anzahl)
        fa-artikel.anzahl    = fa-artikel.anzahl - qty
        fa-artikel.anz100    = fa-artikel.anzahl - qty
      .
      FIND CURRENT fa-artikel NO-LOCK.
    
    END.
    ASSIGN
      anz1 = 11
      anz2 = 22.
  END.
  ELSE
  DO:
    CREATE fa-op. 
    ASSIGN
      fa-op.nr            = mathis.nr
      fa-op.opart         = 2 
      fa-op.datum         = billdate 
      fa-op.zeit          = TIME 
      fa-op.anzahl        = qty 
      fa-op.einzelpreis   = fa-artikel.book-wert / fa-artikel.anzahl 
      fa-op.warenwert     = fa-op.einzelpreis * qty
      fa-op.id            = user-init 
      fa-op.docu-nr       = mathis.NAME + ";;"
                          + mathis.location + ";;"
                          + location-str + ";;" 
                          + "NO" + ";;"
                          + STRING(YEAR(TODAY)) + STRING(MONTH(TODAY),"99")
                          + STRING(DAY(TODAY),"99") + ";;"
    .
    FIND CURRENT fa-op NO-LOCK.
    RELEASE fa-op. 

    IF fa-artikel.anzahl = qty THEN
    DO:
      FIND CURRENT mathis EXCLUSIVE-LOCK.
      ASSIGN mathis.location = location-str.
      FIND CURRENT mathis NO-LOCK.
    END.
    ELSE
    DO:
      FIND FIRST counters WHERE counters.counter-no = 17 EXCLUSIVE-LOCK. 
      ASSIGN counters.counter = counters.counter + 1. 
      FIND CURRENT counters NO-LOCK.
      CREATE mabuff.
      BUFFER-COPY mathis EXCEPT mathis.nr TO mabuff.
      ASSIGN mabuff.nr       = counters.counter
             mabuff.location = location-str
      .
      FIND CURRENT mabuff NO-LOCK.
      CREATE fabuff.
      BUFFER-COPY fa-artikel EXCEPT fa-artikel.nr TO fabuff.
      ASSIGN
          fabuff.nr        = counters.counter
          fabuff.anzahl    = qty
          fabuff.anz100    = qty
          fabuff.warenwert = fa-artikel.warenwert * qty / fa-artikel.anzahl
          fabuff.book-wert = fa-artikel.book-wert * qty / fa-artikel.anzahl
          fabuff.depn-wert = fa-artikel.depn-wert * qty / fa-artikel.anzahl
      .
      FIND CURRENT fabuff NO-LOCK.
      FIND CURRENT fa-artikel EXCLUSIVE-LOCK.
      ASSIGN
          fa-artikel.warenwert = fa-artikel.warenwert *
            (1 - qty / fa-artikel.anzahl)
          fa-artikel.book-wert = fa-artikel.book-wert *
            (1 - qty / fa-artikel.anzahl)
          fa-artikel.depn-wert = fa-artikel.depn-wert *
            (1 - qty / fa-artikel.anzahl)
          fa-artikel.anzahl    = fa-artikel.anzahl - qty
          fa-artikel.anz100    = fa-artikel.anzahl - qty
          fa-artikel.cid       = user-init 
          fa-artikel.changed   = TODAY 
      .
      FIND CURRENT fa-artikel NO-LOCK.
    END.
  END.
END.
