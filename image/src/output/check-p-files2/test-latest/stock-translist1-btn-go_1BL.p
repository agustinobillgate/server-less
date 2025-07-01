
DEFINE TEMP-TABLE t-list 
  FIELD datum       AS DATE 
  FIELD lager-nr    AS INTEGER FORMAT ">>"
  FIELD pos         AS INTEGER FORMAT ">>"
  FIELD op-art      AS INTEGER
  FIELD lscheinnr   AS CHAR FORMAT "x(11)" 
  FIELD f-bezeich   AS CHAR FORMAT "x(16)" 
  FIELD t-bezeich   AS CHAR FORMAT "x(16)" 
  FIELD artnr       AS CHAR FORMAT "x(7)" 
  FIELD bezeich     AS CHAR FORMAT "x(20)" 
  FIELD einheit     AS CHAR FORMAT "x(3)" 
  FIELD content     AS DECIMAL FORMAT ">>>,>>>" 
  FIELD price       AS CHAR FORMAT "x(14)" /* "x(13)"*/
  FIELD qty         AS DECIMAL FORMAT ">>>,>>9.999" 
  FIELD val         AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
  FIELD ID          AS CHAR FORMAT "x(4)"
  FIELD cat-bez     AS CHAR
  FIELD main-bez    AS CHAR
  FIELD subgrp-bez  AS CHAR.

DEF INPUT PARAMETER trans-code  AS CHAR.
DEF INPUT PARAMETER m-grp       AS INT.
DEF INPUT PARAMETER sorttype    AS INT.
DEF INPUT PARAMETER m-str       AS INT.
DEF INPUT PARAMETER mattype     AS INT.
DEF INPUT PARAMETER from-art    AS INT.
DEF INPUT PARAMETER to-art      AS INT.
DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER show-price  AS LOGICAL.
DEF INPUT PARAMETER expense-amt AS LOGICAL.

DEF OUTPUT PARAMETER it-exist AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-list.

IF trans-code NE "" THEN
DO:
    RUN create-list-trans.    /*1*/
END.
ELSE
DO:
    IF m-grp = 0 THEN 
    DO: 
         IF sorttype = 1 THEN RUN create-list.  /*2*/
         ELSE RUN create-listA.     /*3*/
    END. 
    ELSE 
    DO: 
        IF sorttype = 1 THEN RUN create-list1. /*4*/
        ELSE RUN create-list1A. /*5*/
    END. 
END.



PROCEDURE create-list: 
DEFINE VARIABLE lscheinnr AS CHAR. 
DEFINE VARIABLE qty AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0.
DEFINE VARIABLE unit-expense AS DECIMAL NO-UNDO.

DEFINE BUFFER l-store FOR l-lager. 
  
  it-exist = NO. 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  lscheinnr = "". 

  IF m-str NE 0 THEN
  DO:
      FOR EACH l-op WHERE l-op.lager-nr = m-str 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND (l-op.op-art = 2 OR l-op.op-art = 4) 
        AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        NO-LOCK BY l-op.op-art BY l-op.lscheinnr BY l-op.zeit: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
        FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK. 
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        lscheinnr = l-op.lscheinnr. 

        CREATE t-list. 
        RUN add-id.
        ASSIGN
          t-list.lager-nr  = l-op.lager-nr
          t-list.pos       = l-op.pos
          t-list.op-art    = l-op.op-art
          t-list.datum     = l-op.datum
          t-list.lscheinnr = lscheinnr
        . 

        IF l-op.op-art = 4 THEN
        DO:
          t-list.f-bezeich = l-lager.bezeich. 
          IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
        END.
        ELSE
        DO:
          t-list.t-bezeich = l-lager.bezeich. 
          IF AVAILABLE l-store THEN t-list.f-bezeich = l-store.bezeich. 
        END.
        t-list.artnr = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
        t-list.einheit = l-artikel.masseinheit. 
        t-list.content = l-artikel.inhalt. 
        t-list.cat-bez = l-lager.bezeich.
        t-list.main-bez   = l-hauptgrp.bezeich.
        t-list.subgrp-bez = l-untergrup.bezeich.
        IF l-op.anzahl NE 0 AND show-price THEN 
        DO: 
          IF NOT expense-amt THEN
          DO:
            t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = l-op.warenwert
              val        = val + l-op.warenwert 
              t-val      = t-val + l-op.warenwert.
          END.
          ELSE 
          DO:
            unit-expense = 0.
            FOR EACH queasy WHERE queasy.KEY = 121 
              AND queasy.number1 = l-op.artnr 
              AND queasy.date1 LE l-op.datum NO-LOCK
              BY queasy.date1 DESC:
              unit-expense = queasy.deci1.
              LEAVE.
            END.
            t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = unit-expense * l-op.anzahl
              val        = val + t-list.val 
              t-val      = t-val + t-list.val.
          END.
        END. 
        ASSIGN
          qty        = qty + l-op.anzahl
          t-list.qty = l-op.anzahl
          t-qty      = t-qty + l-op.anzahl
        . 
      END. 
  END.
  ELSE
  DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.op-art = 4 AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        NO-LOCK BY l-op.lscheinnr BY l-op.zeit: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
        FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK. 
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        lscheinnr = l-op.lscheinnr. 

        CREATE t-list. 
        RUN add-id.
        ASSIGN
          t-list.lager-nr  = l-op.lager-nr
          t-list.pos       = l-op.pos
          t-list.op-art    = l-op.op-art
          t-list.datum     = l-op.datum
          t-list.lscheinnr = lscheinnr
          t-list.f-bezeich = l-lager.bezeich
          t-list.artnr     = STRING(l-op.artnr, "9999999")
          t-list.bezeich   = l-artikel.bezeich
          t-list.einheit   = l-artikel.masseinheit 
          t-list.content   = l-artikel.inhalt         
          t-list.cat-bez    = l-lager.bezeich
          t-list.main-bez   = l-hauptgrp.bezeich
          t-list.subgrp-bez = l-untergrup.bezeich
        . 
        IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
        IF l-op.anzahl NE 0 AND show-price THEN 
        DO: 
          IF NOT expense-amt THEN
          DO:
            t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = l-op.warenwert
              val        = val + l-op.warenwert 
              t-val      = t-val + l-op.warenwert.
          END.
          ELSE 
          DO:
            unit-expense = 0.
            FOR EACH queasy WHERE queasy.KEY = 121 
              AND queasy.number1 = l-op.artnr 
              AND queasy.date1 LE l-op.datum NO-LOCK
              BY queasy.date1 DESC:
              unit-expense = queasy.deci1.
              LEAVE.
            END.
            t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = unit-expense * l-op.anzahl
              val        = val + t-list.val 
              t-val      = t-val + t-list.val.
          END.
        END. 
        qty = qty + l-op.anzahl. 
        t-list.qty = l-op.anzahl. 
        t-qty = t-qty + l-op.anzahl. 
      END. 
  END.

  IF qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    t-list.price = "Total". 
    t-list.qty = qty. 
    t-list.val = val. 
  END. 
  /*IF m-str = 0 AND t-qty NE 0 THEN*/ 
  IF t-qty NE 0 THEN /* Modify by Michael @ 01/10/2018 for fixing Grand Total */
  DO: 
    CREATE t-list. 
    t-list.price = "Grand Total". 
    t-list.qty = t-qty. 
    t-list.val = t-val. 
  END. 
END. 
 

PROCEDURE create-list-trans: 
DEFINE VARIABLE lscheinnr AS CHAR. 
DEFINE VARIABLE qty AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE unit-expense AS DECIMAL NO-UNDO.

DEFINE BUFFER l-store FOR l-lager. 
  
  it-exist = NO. 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  lscheinnr = "". 
  
  /*FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
    AND l-op.op-art = 4 AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.lscheinnr BY l-op.zeit: */

  IF m-str NE 0 THEN
  DO:
      FOR EACH l-op WHERE l-op.lager-nr = m-str 
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND (l-op.op-art = 2 OR l-op.op-art = 4) 
        AND l-op.herkunftflag = 1  
        AND l-op.lscheinnr = trans-code NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        NO-LOCK BY l-op.op-art BY l-op.lscheinnr BY l-op.zeit: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
        FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK. 
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        lscheinnr = l-op.lscheinnr. 

        CREATE t-list. 
        RUN add-id.
        ASSIGN
          t-list.lager-nr  = l-op.lager-nr
          t-list.pos       = l-op.pos
          t-list.op-art    = l-op.op-art
          t-list.datum     = l-op.datum
          t-list.lscheinnr = lscheinnr
        . 
        
        IF l-op.op-art = 4 THEN
        DO:
          t-list.f-bezeich = l-lager.bezeich. 
          IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
        END.
        ELSE
        DO:
          t-list.t-bezeich = l-lager.bezeich. 
          IF AVAILABLE l-store THEN t-list.f-bezeich = l-store.bezeich. 
        END.
        
        t-list.artnr = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
        t-list.einheit = l-artikel.masseinheit. 
        t-list.content = l-artikel.inhalt.
        t-list.cat-bez    = l-lager.bezeich.     
        t-list.main-bez   = l-hauptgrp.bezeich.  
        t-list.subgrp-bez = l-untergrup.bezeich. 

        IF l-op.anzahl NE 0 AND show-price THEN 
        DO: 
          IF NOT expense-amt THEN
          DO:
            t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = l-op.warenwert
              val        = val + l-op.warenwert 
              t-val      = t-val + l-op.warenwert.
          END.
          ELSE 
          DO:
            unit-expense = 0.
            FOR EACH queasy WHERE queasy.KEY = 121 
              AND queasy.number1 = l-op.artnr 
              AND queasy.date1 LE l-op.datum NO-LOCK
              BY queasy.date1 DESC:
              unit-expense = queasy.deci1.
              LEAVE.
            END.
            t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = unit-expense * l-op.anzahl
              val        = val + t-list.val 
              t-val      = t-val + t-list.val.
          END.
        END. 
        ASSIGN
          qty = qty + l-op.anzahl
          t-list.qty = l-op.anzahl 
          t-qty = t-qty + l-op.anzahl. 
      END. 
  END.
  ELSE
  DO:
      FOR EACH l-op WHERE /*l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND*/ l-op.op-art = 4 AND l-op.herkunftflag = 1
        AND l-op.lscheinnr = trans-code NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        NO-LOCK BY l-op.lscheinnr BY l-op.zeit: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
        FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK. 
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        lscheinnr = l-op.lscheinnr. 

        CREATE t-list. 
        RUN add-id.
        ASSIGN
          t-list.lager-nr  = l-op.lager-nr
          t-list.pos       = l-op.pos
          t-list.op-art    = l-op.op-art
          t-list.datum     = l-op.datum
          t-list.lscheinnr = lscheinnr
          t-list.f-bezeich = l-lager.bezeich
          t-list.artnr     = STRING(l-op.artnr, "9999999")
          t-list.bezeich   = l-artikel.bezeich
          t-list.einheit   = l-artikel.masseinheit 
          t-list.content   = l-artikel.inhalt
          t-list.cat-bez    = l-lager.bezeich     
          t-list.main-bez   = l-hauptgrp.bezeich  
          t-list.subgrp-bez = l-untergrup.bezeich 
        . 
        IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
        
        IF l-op.anzahl NE 0 AND show-price THEN 
        DO: 
          IF NOT expense-amt THEN
          DO:
            t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = l-op.warenwert
              val        = val + l-op.warenwert 
              t-val      = t-val + l-op.warenwert.
          END.
          ELSE 
          DO:
            unit-expense = 0.
            FOR EACH queasy WHERE queasy.KEY = 121 
              AND queasy.number1 = l-op.artnr 
              AND queasy.date1 LE l-op.datum NO-LOCK
              BY queasy.date1 DESC:
              unit-expense = queasy.deci1.
              LEAVE.
            END.
            t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
            IF show-price THEN 
            ASSIGN
              t-list.val = unit-expense * l-op.anzahl
              val        = val + t-list.val 
              t-val      = t-val + t-list.val.
          END.
        END. 
        ASSIGN
          qty = qty + l-op.anzahl
          t-list.qty = l-op.anzahl 
          t-qty = t-qty + l-op.anzahl. 
      END. 
  END.

  IF qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    t-list.price = "Total". 
    t-list.qty = qty. 
    t-list.val = val. 
  END. 
  /*IF t-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    t-list.price = "Grand Total". 
    t-list.qty = t-qty. 
    t-list.val = t-val. 
  END. */
END. 

PROCEDURE create-listA: 
DEFINE VARIABLE curr-artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR. 
DEFINE VARIABLE qty AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it2 AS LOGICAL. 
DEFINE VARIABLE unit-expense AS DECIMAL NO-UNDO.

DEFINE BUFFER l-store FOR l-lager. 
  
  it-exist = NO. 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  curr-artnr = 0. 

  IF m-str NE 0 THEN
  DO:
      /*FOR EACH l-op WHERE l-op.op-art = m-str*/ 
      FOR EACH l-op WHERE l-op.lager-nr = m-str /* Modify by Michael @ 01/10/2018 for fixing Store filter */
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND (l-op.op-art = 2 OR l-op.op-art = 4) 
        AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
        BY l-op.op-art BY l-artikel.bezeich BY l-op.datum BY l-op.lager-nr: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR.         
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF curr-artnr NE l-op.artnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        curr-artnr = l-op.artnr. 

        do-it2 = YES. 
        IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
           (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it2 = NO. 

        IF do-it2 THEN 
        DO: 
          CREATE t-list. 
          RUN add-id.
          ASSIGN
            t-list.lager-nr  = l-op.lager-nr
            t-list.pos       = l-op.pos
            t-list.op-art    = l-op.op-art
            t-list.datum     = l-op.datum
            t-list.lscheinnr = lscheinnr
          . 
          
          IF l-op.op-art = 4 THEN
          DO:
            t-list.f-bezeich = l-lager.bezeich. 
            IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          END.
          ELSE
          DO:
            t-list.t-bezeich = l-lager.bezeich. 
            IF AVAILABLE l-store THEN t-list.f-bezeich = l-store.bezeich. 
          END.
          
          t-list.artnr = STRING(l-op.artnr, "9999999"). 
          t-list.bezeich = l-artikel.bezeich. 
          t-list.einheit = l-artikel.masseinheit. 
          t-list.content = l-artikel.inhalt. 
          t-list.cat-bez    = l-lager.bezeich.     
          t-list.main-bez   = l-hauptgrp.bezeich.  
          t-list.subgrp-bez = l-untergrup.bezeich. 

          IF l-op.anzahl NE 0 AND show-price THEN 
          DO: 
            IF NOT expense-amt THEN
            DO:
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = l-op.warenwert
                val        = val + l-op.warenwert 
                t-val      = t-val + l-op.warenwert.
            END.
            ELSE 
            DO:
              unit-expense = 0.
              FOR EACH queasy WHERE queasy.KEY = 121 
                AND queasy.number1 = l-op.artnr 
                AND queasy.date1 LE l-op.datum NO-LOCK
                BY queasy.date1 DESC:
                unit-expense = queasy.deci1.
                LEAVE.
              END.
              t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = unit-expense * l-op.anzahl
                val        = val + t-list.val 
                t-val      = t-val + t-list.val.
            END.
          END. 

          t-list.qty = l-op.anzahl. 
          qty = qty + l-op.anzahl. 
          t-qty = t-qty + l-op.anzahl. 
        END. 
      END. 
  END.
  ELSE
  DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.op-art = 4 AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
        BY l-artikel.bezeich BY l-op.datum BY l-op.lager-nr: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR.         
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF curr-artnr NE l-op.artnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        curr-artnr = l-op.artnr. 

        do-it2 = YES. 
        IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
           (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it2 = NO. 

        IF do-it2 THEN 
        DO: 
          CREATE t-list. 
          RUN add-id.
          ASSIGN
            t-list.lager-nr  = l-op.lager-nr
            t-list.pos       = l-op.pos
            t-list.op-art    = l-op.op-art
            t-list.datum     = l-op.datum
            t-list.lscheinnr = lscheinnr
            t-list.f-bezeich = l-lager.bezeich
            t-list.artnr     = STRING(l-op.artnr, "9999999")
            t-list.bezeich   = l-artikel.bezeich
            t-list.einheit   = l-artikel.masseinheit 
            t-list.content   = l-artikel.inhalt
            t-list.cat-bez    = l-lager.bezeich     
            t-list.main-bez   = l-hauptgrp.bezeich  
            t-list.subgrp-bez = l-untergrup.bezeich 
          . 
          IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          
          IF l-op.anzahl NE 0 AND show-price THEN 
          DO: 
            IF NOT expense-amt THEN
            DO:
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = l-op.warenwert
                val        = val + l-op.warenwert 
                t-val      = t-val + l-op.warenwert.
            END.
            ELSE 
            DO:
              unit-expense = 0.
              FOR EACH queasy WHERE queasy.KEY = 121 
                AND queasy.number1 = l-op.artnr 
                AND queasy.date1 LE l-op.datum NO-LOCK
                BY queasy.date1 DESC:
                unit-expense = queasy.deci1.
                LEAVE.
              END.
              t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = unit-expense * l-op.anzahl
                val        = val + t-list.val 
                t-val      = t-val + t-list.val.
            END.
          END. 

          t-list.qty = l-op.anzahl. 
          qty = qty + l-op.anzahl. 
          t-qty = t-qty + l-op.anzahl. 
        END. 
      END. 
  END.

  IF qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    t-list.price = "Total". 
    t-list.qty = qty. 
    t-list.val = val. 
  END. 
  /*IF m-str = 0 AND t-qty NE 0 THEN*/ 
  IF t-qty NE 0 THEN /* Modify by Michael @ 01/10/2018 for fixing Grand Total */
  DO: 
    CREATE t-list. 
    t-list.price = "Grand Total". 
    t-list.qty = t-qty. 
    t-list.val = t-val. 
  END. 
END. 
 
PROCEDURE create-list1: 
DEFINE VARIABLE lscheinnr AS CHAR. 
DEFINE VARIABLE qty AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it2 AS LOGICAL. 
DEFINE VARIABLE unit-expense AS DECIMAL NO-UNDO.

DEFINE BUFFER l-store FOR l-lager. 
  
  it-exist = NO. 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  lscheinnr = "". 

  IF m-str NE 0 THEN
  DO:
      /*FOR EACH l-op WHERE l-op.op-art = m-str*/ 
      FOR EACH l-op WHERE l-op.lager-nr = m-str /* Modify by Michael @ 01/10/2018 for fixing Store filter */
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND (l-op.op-art = 2 OR l-op.op-art = 4) 
        AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = m-grp NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
        BY l-op.op-art BY l-op.lscheinnr BY l-op.zeit: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR.         
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        lscheinnr = l-op.lscheinnr. 

        do-it2 = YES. 
        IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
           (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it2 = NO. 

        IF do-it2 THEN 
        DO: 
          CREATE t-list. 
          RUN add-id.
          ASSIGN
            t-list.lager-nr  = l-op.lager-nr
            t-list.pos       = l-op.pos
            t-list.op-art    = l-op.op-art
            t-list.datum     = l-op.datum
            t-list.lscheinnr = lscheinnr
          .
          IF l-op.op-art = 4 THEN
          DO:
            t-list.f-bezeich = l-lager.bezeich. 
            IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          END.
          ELSE
          DO:
            t-list.t-bezeich = l-lager.bezeich. 
            IF AVAILABLE l-store THEN t-list.f-bezeich = l-store.bezeich. 
          END.
          t-list.artnr = STRING(l-op.artnr, "9999999"). 
          t-list.bezeich = l-artikel.bezeich. 
          t-list.einheit = l-artikel.masseinheit. 
          t-list.content = l-artikel.inhalt. 
          t-list.cat-bez    = l-lager.bezeich.     
          t-list.main-bez   = l-hauptgrp.bezeich.  
          t-list.subgrp-bez = l-untergrup.bezeich. 
          
          IF l-op.anzahl NE 0 AND show-price THEN 
          DO: 
            IF NOT expense-amt THEN
            DO:
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = l-op.warenwert
                val        = val + l-op.warenwert 
                t-val      = t-val + l-op.warenwert.
            END.
            ELSE 
            DO:
              unit-expense = 0.
              FOR EACH queasy WHERE queasy.KEY = 121 
                AND queasy.number1 = l-op.artnr 
                AND queasy.date1 LE l-op.datum NO-LOCK
                BY queasy.date1 DESC:
                unit-expense = queasy.deci1.
                LEAVE.
              END.
              t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = unit-expense * l-op.anzahl
                val        = val + t-list.val 
                t-val      = t-val + t-list.val.
            END.
          END. 

          t-list.qty = l-op.anzahl. 
          qty = qty + l-op.anzahl. 
          t-qty = t-qty + l-op.anzahl. 
        END. 
      END. 
  END.
  ELSE
  DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.op-art = 4 AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = m-grp NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
        BY l-op.lscheinnr BY l-op.zeit: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR.         
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        lscheinnr = l-op.lscheinnr. 

        do-it2 = YES. 
        IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
           (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it2 = NO. 

        IF do-it2 THEN 
        DO: 
          CREATE t-list. 
          RUN add-id.
          ASSIGN
            t-list.lager-nr  = l-op.lager-nr
            t-list.pos       = l-op.pos
            t-list.op-art    = l-op.op-art
            t-list.datum     = l-op.datum
            t-list.lscheinnr = lscheinnr
            t-list.f-bezeich = l-lager.bezeich
            t-list.artnr     = STRING(l-op.artnr, "9999999")
            t-list.bezeich   = l-artikel.bezeich
            t-list.einheit   = l-artikel.masseinheit 
            t-list.content   = l-artikel.inhalt 
            t-list.cat-bez    = l-lager.bezeich     
            t-list.main-bez   = l-hauptgrp.bezeich  
            t-list.subgrp-bez = l-untergrup.bezeich 
          . 
          IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          
          IF l-op.anzahl NE 0 AND show-price THEN 
          DO: 
            IF NOT expense-amt THEN
            DO:
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = l-op.warenwert
                val        = val + l-op.warenwert 
                t-val      = t-val + l-op.warenwert.
            END.
            ELSE 
            DO:
              unit-expense = 0.
              FOR EACH queasy WHERE queasy.KEY = 121 
                AND queasy.number1 = l-op.artnr 
                AND queasy.date1 LE l-op.datum NO-LOCK
                BY queasy.date1 DESC:
                unit-expense = queasy.deci1.
                LEAVE.
              END.
              t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = unit-expense * l-op.anzahl
                val        = val + t-list.val 
                t-val      = t-val + t-list.val.
            END.
          END. 

          t-list.qty = l-op.anzahl. 
          qty = qty + l-op.anzahl. 
          t-qty = t-qty + l-op.anzahl. 
        END. 
      END. 
  END.

  IF qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    t-list.price = "Total". 
    t-list.qty = qty. 
    t-list.val = val. 
  END. 
  /*IF m-str = 0 AND t-qty NE 0 THEN*/ 
  IF t-qty NE 0 THEN /* Modify by Michael @ 01/10/2018 for fixing Grand Total */
  DO: 
    CREATE t-list. 
    t-list.price = "Grand Total". 
    t-list.qty = t-qty. 
    t-list.val = t-val. 
  END. 
END. 
 
PROCEDURE create-list1A: 
DEFINE VARIABLE curr-artnr AS INTEGER. 
DEFINE VARIABLE lscheinnr AS CHAR. 
DEFINE VARIABLE qty AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it2 AS LOGICAL. 
DEFINE VARIABLE unit-expense AS DECIMAL NO-UNDO.

DEFINE BUFFER l-store FOR l-lager. 
 
  it-exist = NO. 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  curr-artnr = 0. 

  IF m-str NE 0 THEN
  DO:
      /*FOR EACH l-op WHERE l-op.op-art = m-str*/ 
      FOR EACH l-op WHERE l-op.op-art = m-str /* Modify by Michael @ 01/10/2018 for fixing Store filter */
        AND l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND (l-op.op-art = 2 OR l-op.op-art = 4) 
        AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = m-grp NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
        BY l-op.op-art BY l-artikel.bezeich BY l-op.datum BY l-op.lager-nr: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR.         
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF curr-artnr NE l-op.artnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        curr-artnr = l-op.artnr. 

        do-it2 = YES. 
        IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
           (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it2 = NO. 

        IF do-it2 THEN 
        DO: 
          CREATE t-list. 
          RUN add-id.
          ASSIGN
            t-list.lager-nr  = l-op.lager-nr
            t-list.pos       = l-op.pos
            t-list.op-art    = l-op.op-art
            t-list.datum     = l-op.datum
            t-list.lscheinnr = lscheinnr
          . 
          
          IF l-op.op-art = 4 THEN
          DO:
            t-list.f-bezeich = l-lager.bezeich. 
            IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          END.
          ELSE
          DO:
            t-list.t-bezeich = l-lager.bezeich. 
            IF AVAILABLE l-store THEN t-list.f-bezeich = l-store.bezeich. 
          END.
          
          t-list.artnr = STRING(l-op.artnr, "9999999"). 
          t-list.bezeich = l-artikel.bezeich. 
          t-list.einheit = l-artikel.masseinheit. 
          t-list.content = l-artikel.inhalt. 
          t-list.cat-bez    = l-lager.bezeich.     
          t-list.main-bez   = l-hauptgrp.bezeich.  
          t-list.subgrp-bez = l-untergrup.bezeich. 

          IF l-op.anzahl NE 0 AND show-price THEN 
          DO: 
            IF NOT expense-amt THEN
            DO:
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = l-op.warenwert
                val        = val + l-op.warenwert 
                t-val      = t-val + l-op.warenwert.
            END.
            ELSE 
            DO:
              unit-expense = 0.
              FOR EACH queasy WHERE queasy.KEY = 121 
                AND queasy.number1 = l-op.artnr 
                AND queasy.date1 LE l-op.datum NO-LOCK
                BY queasy.date1 DESC:
                unit-expense = queasy.deci1.
                LEAVE.
              END.
              t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = unit-expense * l-op.anzahl
                val        = val + t-list.val 
                t-val      = t-val + t-list.val.
            END.
          END. 

          t-list.qty = l-op.anzahl. 
          qty = qty + l-op.anzahl. 
          t-qty = t-qty + l-op.anzahl. 
        END. 
      END. 
  END.
  ELSE
  DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
        AND l-op.op-art = 4 AND l-op.herkunftflag = 1 NO-LOCK USE-INDEX artopart_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = m-grp NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
        BY l-artikel.bezeich BY l-op.datum BY l-op.lager-nr: 
        it-exist = YES. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR.         
        FIND FIRST l-hauptgrp  WHERE l-hauptgrp.endkum = l-artikel.endkum NO-LOCK.

        IF curr-artnr NE l-op.artnr AND qty NE 0 THEN 
        DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          qty = 0. 
          val = 0. 
        END. 
        curr-artnr = l-op.artnr. 

        do-it2 = YES. 
        IF (mattype = 1 AND l-untergrup.betriebsnr = 1) OR 
           (mattype = 2 AND l-untergrup.betriebsnr = 0) THEN do-it2 = NO. 

        IF do-it2 THEN 
        DO: 
          CREATE t-list. 
          RUN add-id.
          ASSIGN
            t-list.lager-nr  = l-op.lager-nr
            t-list.pos       = l-op.pos
            t-list.op-art    = l-op.op-art
            t-list.datum     = l-op.datum
            t-list.lscheinnr = lscheinnr
            t-list.f-bezeich = l-lager.bezeich
            t-list.artnr     = STRING(l-op.artnr, "9999999")
            t-list.bezeich   = l-artikel.bezeich
            t-list.einheit   = l-artikel.masseinheit 
            t-list.content   = l-artikel.inhalt 
            t-list.cat-bez    = l-lager.bezeich     
            t-list.main-bez   = l-hauptgrp.bezeich  
            t-list.subgrp-bez = l-untergrup.bezeich 
          . 
          IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
          IF l-op.anzahl NE 0 AND show-price THEN 
          DO: 
            IF NOT expense-amt THEN
            DO:
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = l-op.warenwert
                val        = val + l-op.warenwert 
                t-val      = t-val + l-op.warenwert.
            END.
            ELSE 
            DO:
              unit-expense = 0.
              FOR EACH queasy WHERE queasy.KEY = 121 
                AND queasy.number1 = l-op.artnr 
                AND queasy.date1 LE l-op.datum NO-LOCK
                BY queasy.date1 DESC:
                unit-expense = queasy.deci1.
                LEAVE.
              END.
              t-list.price = STRING(unit-expense, ">>>,>>>,>>9.99"). 
              IF show-price THEN 
              ASSIGN
                t-list.val = unit-expense * l-op.anzahl
                val        = val + t-list.val 
                t-val      = t-val + t-list.val.
            END.
          END. 

          t-list.qty = l-op.anzahl. 
          qty = qty + l-op.anzahl. 
          t-qty = t-qty + l-op.anzahl. 
        END. 
      END. 
  END.

  IF qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    t-list.price = "Total". 
    t-list.qty = qty. 
    t-list.val = val. 
  END. 
  /*IF m-str = 0 AND t-qty NE 0 THEN*/ 
  IF t-qty NE 0 THEN /* Modify by Michael @ 01/10/2018 for fixing Grand Total */
  DO: 
    CREATE t-list. 
    t-list.price = "Grand Total". 
    t-list.qty = t-qty. 
    t-list.val = t-val. 
  END. 
END. 


PROCEDURE add-id:
    DEFINE BUFFER usr FOR bediener.

    FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN
        t-list.id = usr.userinit.
    ELSE t-list.id = "??".
END.
 
