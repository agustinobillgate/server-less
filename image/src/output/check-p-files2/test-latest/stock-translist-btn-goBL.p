DEFINE TEMP-TABLE t-list 
  FIELD nr          AS INTEGER
  FIELD f-lager     AS INTEGER 
  FIELD t-lager     AS INTEGER 
  FIELD f-bezeich   AS CHAR FORMAT "x(20)" 
  FIELD t-bezeich   AS CHAR FORMAT "x(20)" 
  FIELD artnr       AS CHAR FORMAT "x(7)" 
  FIELD subgr       AS INTEGER FORMAT ">>9"
  FIELD sub-bezeich AS CHAR FORMAT "x(20)"
  FIELD bezeich     AS CHAR FORMAT "x(20)" 
  FIELD qty         AS DECIMAL FORMAT ">>>,>>9.999" 
  FIELD val         AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" 
  FIELD t-qty       AS DECIMAL FORMAT ">,>>>,>>9.999" 
  FIELD t-val       AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99". 


DEFINE INPUT PARAMETER main-grp     AS INT  NO-UNDO.
DEFINE INPUT PARAMETER sorttype     AS INT  NO-UNDO.
DEFINE INPUT PARAMETER mattype      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER from-lager   AS INT  NO-UNDO.
DEFINE INPUT PARAMETER to-lager     AS INT  NO-UNDO.
DEFINE INPUT PARAMETER from-art     AS INT  NO-UNDO.
DEFINE INPUT PARAMETER to-art       AS INT  NO-UNDO.
DEFINE INPUT PARAMETER from-date    AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE curr-nr     AS INTEGER  NO-UNDO INIT 0. 
IF main-grp = 0 THEN
DO:
    IF sorttype = 0 THEN RUN create-list. 
    ELSE RUN list-subgroup.
END.                  
ELSE
DO:
    IF sorttype = 0 THEN RUN create-list1. 
    ELSE RUN list-subgroup1.
END.                  

/******************************** PROCEDURE ***********************************/ 
PROCEDURE create-list: 
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE t-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE buffer l-store FOR l-lager.

  IF from-lager = to-lager THEN
  DO:
    RUN create-listA.
    RETURN.
  END.

  FOR EACH t-list: 
    DELETE t-list. 
  END. 
 
  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    t-lager = 0. 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.op-art = 4 AND l-op.herkunftflag = 1 
      NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      NO-LOCK BY l-op.pos BY l-artikel.bezeich: 
 
      IF (f-lager NE l-lager.lager-nr OR t-lager NE l-op.pos) 
        AND t-qty NE 0 THEN 
      DO: 
        create t-list.
        ASSIGN
          curr-nr        = curr-nr + 1
          t-list.nr      = curr-nr
          t-list.bezeich = "Total"
          t-list.qty     = qty
          t-list.val     = val 
          t-list.t-qty   = t-qty 
          t-list.t-val   = t-val 
          qty            = 0
          val            = 0 
          t-qty          = 0 
          t-val          = 0
        . 
      END. 
 
      FIND FIRST t-list WHERE t-list.f-lager = l-lager.lager-nr 
        AND t-list.t-lager = l-op.pos 
        AND INTEGER(t-list.artnr) = l-artikel.artnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
        CREATE t-list.
        ASSIGN
          curr-nr        = curr-nr + 1
          t-list.nr      = curr-nr
          t-list.f-lager = l-lager.lager-nr
          t-list.t-lager = l-op.pos
        . 
        
        IF f-lager NE l-lager.lager-nr OR t-lager NE l-op.pos THEN 
        DO: 
          t-list.f-bezeich = l-lager.bezeich. 
          IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          f-lager = l-lager.lager-nr. 
          t-lager = l-op.pos. 
        END. 
        t-list.artnr = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
      END. 
      IF l-op.datum = to-date THEN 
      DO: 
        t-list.qty = t-list.qty + l-op.anzahl. 
        t-list.val = t-list.val + l-op.warenwert. 
        qty = qty + l-op.anzahl. 
        val = val + l-op.warenwert. 
        d-qty = d-qty + l-op.anzahl. 
        d-val = d-val + l-op.warenwert. 
      END. 
      t-list.t-qty = t-list.t-qty + l-op.anzahl. 
      t-list.t-val = t-list.t-val + l-op.warenwert. 
      t-qty = t-qty + l-op.anzahl. 
      t-val = t-val + l-op.warenwert. 
      m-qty = m-qty + l-op.anzahl. 
      m-val = m-val + l-op.warenwert. 
    END. 
    IF t-qty NE 0 THEN 
    DO: 
      CREATE t-list. 
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.bezeich = "Total"
        t-list.qty     = qty
        t-list.val     = val 
        t-list.t-qty   = t-qty 
        t-list.t-val   = t-val
      . 
    END. 
  END. 
  IF m-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "GRAND TOTAL"
      t-list.qty     = d-qty
      t-list.val     = d-val
      t-list.t-qty   = m-qty 
      t-list.t-val   = m-val
    . 
  END. 
END. 

PROCEDURE create-listA: 
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE t-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE buffer l-store FOR l-lager. 

  FOR EACH t-list: 
    DELETE t-list. 
  END. 
  FIND FIRST l-lager WHERE l-lager.lager-nr = from-lager NO-LOCK.

  ASSIGN
    t-lager = 0 
    qty     = 0
    val     = 0 
    t-qty   = 0 
    t-val   = 0 
    d-qty   = 0
    d-val   = 0
    m-qty   = 0
    m-val   = 0
  .
  FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
    AND l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
    AND l-op.op-art = 4 AND l-op.herkunftflag = 1 
    AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.pos BY l-artikel.bezeich: 
 
    IF t-lager = 0 THEN t-lager = l-op.pos.
    IF t-lager NE l-op.pos AND t-qty NE 0 THEN 
    DO: 
      CREATE t-list.
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.bezeich = "Total" 
        t-list.qty     = qty
        t-list.val     = val 
        t-list.t-qty   = t-qty 
        t-list.t-val   = t-val 
        qty            = 0 
        val            = 0 
        t-qty          = 0 
        t-val          = 0 
        t-lager        = l-op.pos
      .
    END. 
 
    FIND FIRST t-list WHERE t-list.f-lager = l-lager.lager-nr 
      AND t-list.t-lager = l-op.pos 
      AND INTEGER(t-list.artnr) = l-artikel.artnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE t-list THEN 
    DO: 
      FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK. 
      CREATE t-list. 
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.f-lager = l-lager.lager-nr 
        t-list.t-lager = l-op.pos
        t-list.artnr   = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
      . 
      IF t-qty = 0 THEN 
      ASSIGN
        t-list.f-bezeich = l-lager.bezeich
        t-list.t-bezeich = l-store.bezeich
      . 
    END. 
      
    IF l-op.datum = to-date THEN 
    ASSIGN 
        t-list.qty = t-list.qty + l-op.anzahl
        t-list.val = t-list.val + l-op.warenwert 
        qty        = qty + l-op.anzahl
        val        = val + l-op.warenwert 
        d-qty      = d-qty + l-op.anzahl 
        d-val      = d-val + l-op.warenwert 
    .
    ASSIGN
      t-list.t-qty = t-list.t-qty + l-op.anzahl
      t-list.t-val = t-list.t-val + l-op.warenwert 
      t-qty        = t-qty + l-op.anzahl
      t-val        = t-val + l-op.warenwert 
      m-qty        = m-qty + l-op.anzahl
      m-val        = m-val + l-op.warenwert
    . 
  END. 
    
  IF t-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "Total" 
      t-list.qty     = qty
      t-list.val     = val 
      t-list.t-qty   = t-qty 
      t-list.t-val   = t-val
    . 
  END. 
  IF m-qty NE 0 THEN 
  DO: 
    CREATE t-list.
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "GRAND TOTAL"
      t-list.qty     = d-qty
      t-list.val     = d-val 
      t-list.t-qty   = m-qty 
      t-list.t-val   = m-val
    . 
  END. 

  ASSIGN
    t-lager = 0 
    qty     = 0
    val     = 0 
    t-qty   = 0 
    t-val   = 0 
    d-qty   = 0
    d-val   = 0
    m-qty   = 0
    m-val   = 0
  .
  FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
    AND l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
    AND l-op.op-art = 2 AND l-op.herkunftflag = 1 
    AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.pos BY l-artikel.bezeich: 
 
    IF t-lager = 0 THEN t-lager = l-op.pos.
    IF t-lager NE l-op.pos AND t-qty NE 0 THEN 
    DO: 
      CREATE t-list.
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.bezeich = "Total" 
        t-list.qty     = qty
        t-list.val     = val 
        t-list.t-qty   = t-qty 
        t-list.t-val   = t-val 
        qty            = 0 
        val            = 0 
        t-qty          = 0 
        t-val          = 0 
        t-lager        = l-op.pos
      .
    END. 
 
    FIND FIRST t-list WHERE t-list.t-lager = l-lager.lager-nr 
      AND t-list.f-lager = l-op.pos 
      AND INTEGER(t-list.artnr) = l-artikel.artnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE t-list THEN 
    DO: 
      FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK. 
      CREATE t-list. 
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.t-lager = l-lager.lager-nr 
        t-list.f-lager = l-op.pos
        t-list.artnr   = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
      . 
      IF t-qty = 0 THEN 
      ASSIGN
        t-list.t-bezeich = l-lager.bezeich
        t-list.f-bezeich = l-store.bezeich
      . 
    END. 
      
    IF l-op.datum = to-date THEN 
    ASSIGN 
        t-list.qty = t-list.qty + l-op.anzahl
        t-list.val = t-list.val + l-op.warenwert 
        qty        = qty + l-op.anzahl
        val        = val + l-op.warenwert 
        d-qty      = d-qty + l-op.anzahl 
        d-val      = d-val + l-op.warenwert 
    .
    ASSIGN
      t-list.t-qty = t-list.t-qty + l-op.anzahl
      t-list.t-val = t-list.t-val + l-op.warenwert 
      t-qty        = t-qty + l-op.anzahl
      t-val        = t-val + l-op.warenwert 
      m-qty        = m-qty + l-op.anzahl
      m-val        = m-val + l-op.warenwert
    . 
  END. 
    
  IF t-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "Total" 
      t-list.qty     = qty
      t-list.val     = val 
      t-list.t-qty   = t-qty 
      t-list.t-val   = t-val
    . 
  END. 
  IF m-qty NE 0 THEN 
  DO: 
    CREATE t-list.
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "GRAND TOTAL"
      t-list.qty     = d-qty
      t-list.val     = d-val 
      t-list.t-qty   = m-qty 
      t-list.t-val   = m-val
    . 
  END. 

END.

PROCEDURE list-subgroup:
    DEFINE VARIABLE last-sub AS CHAR.
    DEFINE VARIABLE to-store AS INTEGER.
    DEFINE VARIABLE f-lager AS INTEGER. 
    DEFINE VARIABLE t-lager AS INTEGER. 
    DEFINE VARIABLE t-subgr AS INTEGER.
    DEFINE VARIABLE qty AS DECIMAL. 
    DEFINE VARIABLE val AS DECIMAL. 
    DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
    DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE d-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
    DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE m-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
    DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 

    DEFINE VARIABLE subd-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
    DEFINE VARIABLE subd-val AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE subm-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
    DEFINE VARIABLE subm-val AS DECIMAL INITIAL 0. 

    DEFINE buffer l-store FOR l-lager. 
    FOR EACH t-list: 
      delete t-list. 
    END. 

  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    t-lager = 0. 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.op-art = 4 AND l-op.herkunftflag = 1 
      NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK
      BY l-artikel.zwkum BY l-op.pos BY l-artikel.bezeich: 
 
      IF to-store NE l-op.pos AND subm-qty NE 0 OR
          (t-subgr NE 0 AND t-subgr NE l-artikel.zwkum) THEN
      DO:
          CREATE t-list.
          ASSIGN
              curr-nr        = curr-nr + 1
              t-list.nr      = curr-nr  
              t-list.bezeich = "SubTotal"
              t-list.qty     = subd-qty
              t-list.val     = subd-val
              t-list.t-qty   = subm-qty
              t-list.t-val   = subm-val
              subd-qty = 0
              subd-val = 0
              subm-qty = 0
              subm-val = 0.
          
      END.
      to-store = l-op.pos.

      IF t-subgr NE l-artikel.zwkum AND t-qty NE 0 THEN
      DO: 
        CREATE t-list. 
        ASSIGN
          curr-nr        = curr-nr + 1
          t-list.nr      = curr-nr  
          t-list.bezeich = "Total " + last-sub 
          t-list.qty     = qty
          t-list.val     = val 
          t-list.t-qty   = t-qty 
          t-list.t-val   = t-val 
          qty            = 0 
          val            = 0 
          t-qty          = 0 
          t-val          = 0
        . 
      END. 

      FIND FIRST t-list WHERE t-list.subgr = l-artikel.zwkum AND
          t-list.f-lager = l-lager.lager-nr AND t-list.t-lager = l-op.pos 
          AND INTEGER(t-list.artnr) = l-artikel.artnr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE t-list THEN 
      DO: 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
        
        CREATE t-list. 
        ASSIGN
          curr-nr        = curr-nr + 1
          t-list.nr      = curr-nr  
          t-list.f-lager = l-lager.lager-nr
          t-list.t-lager = l-op.pos
        . 
        IF f-lager NE l-lager.lager-nr OR t-lager NE l-op.pos 
            OR t-subgr NE l-artikel.zwkum THEN 
        DO: 
          t-list.f-bezeich = l-lager.bezeich. 
          IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          f-lager = l-lager.lager-nr. 
          t-lager = l-op.pos. 
          IF t-subgr NE l-artikel.zwkum THEN
          DO:
            t-list.sub-bezeich = l-untergrup.bezeich.
            /*t-subgr        = l-artikel.zwkum.*/
          END.
        END. 
        t-list.artnr = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
        t-list.subgr   = l-artikel.zwkum.    
        t-subgr = l-artikel.zwkum.
        last-sub = l-untergrup.bezeich.
      END. 
      IF l-op.datum = to-date THEN 
      DO: 
        t-list.qty = t-list.qty + l-op.anzahl. 
        t-list.val = t-list.val + l-op.warenwert. 
        qty = qty + l-op.anzahl. 
        val = val + l-op.warenwert. 
        d-qty = d-qty + l-op.anzahl. 
        d-val = d-val + l-op.warenwert. 
        subd-qty = subd-qty + l-op.anzahl.
        subd-val = subd-val + l-op.warenwert.
      END. 
      t-list.t-qty = t-list.t-qty + l-op.anzahl. 
      t-list.t-val = t-list.t-val + l-op.warenwert. 
      t-qty = t-qty + l-op.anzahl. 
      t-val = t-val + l-op.warenwert. 
      m-qty = m-qty + l-op.anzahl. 
      m-val = m-val + l-op.warenwert. 
      subm-qty = subm-qty + l-op.anzahl.
      subm-val = subm-val + l-op.warenwert.
    END. 
    IF subm-qty NE 0 THEN
    DO:
        CREATE t-list.
        ASSIGN
          curr-nr        = curr-nr + 1
          t-list.nr      = curr-nr  
          t-list.bezeich = "SubTotal"
          t-list.qty     = subd-qty
          t-list.val     = subd-val
          t-list.t-qty   = subm-qty
          t-list.t-val   = subm-val
          subd-qty = 0
          subd-val = 0
          subm-qty = 0
          subm-val = 0.
        
    END.
    IF t-qty NE 0 THEN 
    DO: 
      CREATE t-list. 
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.bezeich = "Total " + last-sub
        t-list.qty     = qty
        t-list.val     = val 
        t-list.t-qty   = t-qty 
        t-list.t-val   = t-val
      . 
    END. 
  END. 
  IF m-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "GRAND TOTAL"
      t-list.qty     = d-qty
      t-list.val     = d-val 
      t-list.t-qty   = m-qty 
      t-list.t-val   = m-val
    . 
  END. 
END.
 
PROCEDURE create-list1: 
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE t-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE buffer l-store FOR l-lager. 
DEFINE VARIABLE do-it AS LOGICAL. 
 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    t-lager = 0. 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.op-art = 4 AND l-op.herkunftflag = 1 
      NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum EQ main-grp NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
      BY l-op.pos BY l-artikel.bezeich: 
      do-it = YES. 
      IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
         (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it = NO. 
      IF (f-lager NE l-lager.lager-nr OR t-lager NE l-op.pos) 
        AND t-qty NE 0 THEN 
      DO: 
        CREATE t-list. 
        ASSIGN
          curr-nr        = curr-nr + 1
          t-list.nr      = curr-nr  
          t-list.bezeich = "Total"
          t-list.qty     = qty
          t-list.val     = val 
          t-list.t-qty   = t-qty 
          t-list.t-val   = t-val 
          qty            = 0    
          val            = 0 
          t-qty          = 0 
          t-val          = 0
        . 
      END. 
      IF do-it THEN 
      DO: 
        FIND FIRST t-list WHERE t-list.f-lager = l-lager.lager-nr 
          AND t-list.t-lager = l-op.pos 
          AND INTEGER(t-list.artnr) = l-artikel.artnr 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE t-list THEN 
        DO: 
          FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR.           
          CREATE t-list. 
          ASSIGN
            curr-nr        = curr-nr + 1
            t-list.nr      = curr-nr  
            t-list.f-lager = l-lager.lager-nr
            t-list.t-lager = l-op.pos
          . 
          IF f-lager NE l-lager.lager-nr OR t-lager NE l-op.pos THEN 
          DO: 
            t-list.f-bezeich = l-lager.bezeich. 
            IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
            f-lager = l-lager.lager-nr. 
            t-lager = l-op.pos. 
          END. 
          t-list.artnr = STRING(l-op.artnr, "9999999"). 
          t-list.bezeich = l-artikel.bezeich. 
        END. 
        IF l-op.datum = to-date THEN 
        DO: 
          t-list.qty = t-list.qty + l-op.anzahl. 
          t-list.val = t-list.val + l-op.warenwert. 
          qty = qty + l-op.anzahl. 
          val = val + l-op.warenwert. 
          d-qty = d-qty + l-op.anzahl. 
          d-val = d-val + l-op.warenwert. 
        END. 
        t-list.t-qty = t-list.t-qty + l-op.anzahl. 
        t-list.t-val = t-list.t-val + l-op.warenwert. 
        t-qty = t-qty + l-op.anzahl. 
        t-val = t-val + l-op.warenwert. 
        m-qty = m-qty + l-op.anzahl. 
        m-val = m-val + l-op.warenwert. 
      END. 
    END. 
    IF t-qty NE 0 THEN 
    DO: 
      CREATE t-list. 
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.bezeich = "Total"
        t-list.qty     = qty
        t-list.val     = val 
        t-list.t-qty   = t-qty 
        t-list.t-val   = t-val
      . 
    END. 
  END. 
  IF m-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "GRAND TOTAL"
      t-list.qty     = d-qty
      t-list.val     = d-val 
      t-list.t-qty   = m-qty 
      t-list.t-val   = m-val
    . 
  END. 
END. 
 
PROCEDURE list-subgroup1: 
DEFINE VARIABLE t-subgr AS INTEGER.
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE t-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE buffer l-store FOR l-lager. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE to-store AS INTEGER.
DEFINE VARIABLE subd-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE subd-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE subm-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE subm-val AS DECIMAL INITIAL 0.
DEFINE VARIABLE last-sub AS CHAR.
 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
    t-lager = 0. 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.op-art = 4 AND l-op.herkunftflag = 1 
      NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum EQ main-grp NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
      BY l-artikel.zwkum BY l-op.pos BY l-artikel.bezeich: 
      do-it = YES. 
      IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
         (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it = NO. 
      IF do-it THEN 
      DO: 
          IF to-store NE l-op.pos AND subm-qty NE 0 OR 
              (t-subgr NE 0 AND t-subgr NE l-artikel.zwkum) THEN
          DO:
              CREATE t-list.
              ASSIGN
                  curr-nr        = curr-nr + 1
                  t-list.nr      = curr-nr  
                  t-list.bezeich = "SubTotal"
                  t-list.qty     = subd-qty
                  t-list.val     = subd-val
                  t-list.t-qty   = subm-qty
                  t-list.t-val   = subm-val
                  subd-qty = 0
                  subd-val = 0
                  subm-qty = 0
                  subm-val = 0.
              
          END.
          to-store = l-op.pos.
    
          IF (t-subgr NE l-artikel.zwkum) AND t-qty NE 0 THEN 
          DO: 
            CREATE t-list. 
            ASSIGN
              curr-nr        = curr-nr + 1
              t-list.nr      = curr-nr  
              t-list.bezeich = "Total " + last-sub
              t-list.qty     = qty
              t-list.val     = val 
              t-list.t-qty   = t-qty 
              t-list.t-val   = t-val 
              qty            = 0
              val            = 0 
              t-qty          = 0 
              t-val          = 0
            . 
          END. 
      
        FIND FIRST t-list WHERE t-list.subgr = l-artikel.zwkum AND
            t-list.f-lager = l-lager.lager-nr AND t-list.t-lager = l-op.pos 
            AND INTEGER(t-list.artnr) = l-artikel.artnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-list THEN 
        DO: 
          FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
          
          CREATE t-list. 
          ASSIGN
            curr-nr        = curr-nr + 1
            t-list.nr      = curr-nr  
            t-list.f-lager = l-lager.lager-nr
            t-list.t-lager = l-op.pos
          . 
          
          IF f-lager NE l-lager.lager-nr OR t-lager NE l-op.pos 
              OR t-subgr NE l-artikel.zwkum THEN
          DO:                                 
              t-list.f-bezeich = l-lager.bezeich. 
              IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
              f-lager = l-lager.lager-nr. 
              t-lager = l-op.pos. 
              IF t-subgr NE l-artikel.zwkum THEN
              DO: 
                  t-list.sub-bezeich = l-untergrup.bezeich.
              END.
          END.
          t-list.artnr = STRING(l-op.artnr, "9999999"). 
          t-list.subgr  = l-artikel.zwkum.
          t-list.bezeich = l-artikel.bezeich. 
          last-sub = l-untergrup.bezeich.
          t-subgr = l-artikel.zwkum.
        END.                              
        IF l-op.datum = to-date THEN 
        DO: 
          t-list.qty = t-list.qty + l-op.anzahl. 
          t-list.val = t-list.val + l-op.warenwert. 
          qty = qty + l-op.anzahl. 
          val = val + l-op.warenwert. 
          d-qty = d-qty + l-op.anzahl. 
          d-val = d-val + l-op.warenwert. 
          subd-qty = subd-qty + l-op.anzahl.
          subd-val = subd-val + l-op.warenwert.
        END. 
        t-list.t-qty = t-list.t-qty + l-op.anzahl. 
        t-list.t-val = t-list.t-val + l-op.warenwert. 
        t-qty = t-qty + l-op.anzahl. 
        t-val = t-val + l-op.warenwert. 
        m-qty = m-qty + l-op.anzahl. 
        m-val = m-val + l-op.warenwert. 
        subm-qty = subm-qty + l-op.anzahl.
        subm-val = subm-val + l-op.warenwert.
      END. 
    END. 
    
    IF subm-qty NE 0 THEN
    DO:
        CREATE t-list.
        ASSIGN
          curr-nr        = curr-nr + 1
          t-list.nr      = curr-nr  
          t-list.bezeich = "SubTotal"
          t-list.qty     = subd-qty
          t-list.val     = subd-val
          t-list.t-qty   = subm-qty
          t-list.t-val   = subm-val
          subd-qty = 0
          subd-val = 0
          subm-qty = 0
          subm-val = 0.
        
    END.
    IF t-qty NE 0 THEN 
    DO: 
      CREATE t-list. 
      ASSIGN
        curr-nr        = curr-nr + 1
        t-list.nr      = curr-nr  
        t-list.bezeich = "Total " + last-sub
        t-list.qty     = qty
        t-list.val     = val 
        t-list.t-qty   = t-qty 
        t-list.t-val   = t-val
      .
    END. 
  END. 
  IF m-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      curr-nr        = curr-nr + 1
      t-list.nr      = curr-nr  
      t-list.bezeich = "GRAND TOTAL"
      t-list.qty     = d-qty
      t-list.val     = d-val 
      t-list.t-qty   = m-qty 
      t-list.t-val   = m-val
    . 
  END. 
END. 
