
DEFINE TEMP-TABLE tt-list 
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD subgroup    AS INTEGER 
  FIELD subbez      AS CHAR FORMAT "x(24)"
  FIELD f-lager     AS INTEGER 
  FIELD f-bezeich   AS CHAR FORMAT "x(20)" 
  FIELD artnr       AS CHAR FORMAT "x(7)" 
  FIELD bezeich     AS CHAR FORMAT "x(23)" 
  FIELD einheit     AS CHAR FORMAT "x(3)" 
  FIELD qty         AS DECIMAL FORMAT "->>,>>9.99" 
  FIELD val         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" 
  FIELD t-qty       AS DECIMAL FORMAT " ->>>,>>9.99" 
  FIELD t-val       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
  FIELD grand-flag AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE t-list 
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD subgroup    AS INTEGER 
  FIELD subbez      AS CHAR FORMAT "x(24)"
  FIELD f-lager     AS INTEGER 
  FIELD f-bezeich   AS CHAR FORMAT "x(20)" 
  FIELD artnr       AS CHAR FORMAT "x(7)" 
  FIELD bezeich     AS CHAR FORMAT "x(23)" 
  FIELD einheit     AS CHAR FORMAT "x(3)" 
  FIELD qty         AS DECIMAL FORMAT "->>,>>9.99" 
  FIELD val         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" 
  FIELD t-qty       AS DECIMAL FORMAT " ->>>,>>9.99" 
  FIELD t-val       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
  FIELD grand-flag AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE big-total 
  FIELD total AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
  FIELD lager-nr     AS INTEGER
  FIELD f-bezeich    AS CHAR.
  
DEFINE TEMP-TABLE temp-list LIKE tt-list.

DEF INPUT PARAMETER sorttype AS INT.
DEF INPUT PARAMETER from-lager AS INT.
DEF INPUT PARAMETER to-lager AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER from-art AS INT.
DEF INPUT PARAMETER to-art AS INT.
DEF INPUT PARAMETER from-grp AS INT.
DEF INPUT PARAMETER to-grp AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-list.


IF sorttype = 1 THEN
DO:
    RUN create-list1. 
END.  
ELSE IF sorttype = 2 THEN
DO:
    RUN create-list2.
END.
ELSE IF sorttype = 3 THEN
DO: 
    RUN create-list3.
END.
/*add by bernatd B7230C 2025*/
ELSE IF sorttype = 4 THEN
DO:
  RUN create-list4.
  RUN create-output.
END. 

PROCEDURE create-list1: 
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE buffer l-store FOR l-lager. 

  FOR EACH t-list: 
    delete t-list. 
  END. 

  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK BY l-lager.lager-nr: 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
      AND l-op.anzahl NE 0 
      AND l-op.op-art = 1 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.zwkum GE from-grp AND l-artikel.zwkum LE to-grp NO-LOCK BY l-artikel.artnr: 

      IF f-lager NE l-lager.lager-nr AND t-qty NE 0 THEN 
      DO: 
        create t-list. 
        t-list.flag = 1. 
        t-list.f-lager = f-lager. 
        t-list.bezeich = "TOTAL". 
        t-list.qty = qty. 
        t-list.val = val. 
        t-list.t-qty = t-qty. 
        t-list.t-val = t-val. 
        qty = 0. 
        val = 0. 
        t-qty = 0. 
        t-val = 0. 
        f-lager = l-lager.lager-nr. 
      END. 

      FIND FIRST t-list WHERE t-list.f-lager = l-lager.lager-nr 
        AND INTEGER(t-list.artnr) = l-artikel.artnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        t-list.f-lager = l-lager.lager-nr. 
        IF f-lager NE l-lager.lager-nr THEN 
        DO: 
          t-list.f-bezeich = l-lager.bezeich. 
          f-lager = l-lager.lager-nr. 
        END. 
        t-list.artnr = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
        t-list.einheit = l-artikel.masseinheit. 
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
      create t-list. 
      t-list.flag = 1. 
      t-list.f-lager = f-lager. 
      t-list.bezeich = "TOTAL". 
      t-list.qty = qty. 
      t-list.val = val. 
      t-list.t-qty = t-qty. 
      t-list.t-val = t-val. 
    END. 
  END. 
  DO: 
    create t-list. 
    t-list.flag = 1. 
    t-list.f-lager = 9999. 
    t-list.bezeich = "GRAND TOTAL". 
    t-list.qty = d-qty. 
    t-list.val = d-val. 
    t-list.t-qty = m-qty. 
    t-list.t-val = m-val.
    t-list.grand-flag = YES. 
  END. 

END. /*end procedure*/

PROCEDURE create-list3: 
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE st-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE st-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE sm-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE sm-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE subgr AS CHAR NO-UNDO.

DEFINE buffer l-store FOR l-lager. 
 
  status default "Processing...". 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK BY l-lager.lager-nr: 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
      AND l-op.anzahl NE 0 
      AND l-op.op-art = 1 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.zwkum GE from-grp AND l-artikel.zwkum LE to-grp 
      NO-LOCK, FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
        NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 
        IF subgr NE l-untergrup.bezeich AND subgr NE "" AND sm-qty NE 0 THEN
        DO:
            CREATE t-list.
            ASSIGN
                t-list.flag = 1
                t-list.bezeich = subgr
                t-list.qty = st-qty
                t-list.val = st-val
                t-list.t-qty = sm-qty
                t-list.t-val = sm-val
                st-qty = 0
                st-val = 0
                sm-qty = 0
                sm-val = 0.
        END.
        
      IF f-lager NE l-lager.lager-nr AND t-qty NE 0 THEN 
      DO: 
        create t-list. 
        t-list.flag = 1. 
        t-list.f-lager = f-lager. 
        t-list.bezeich = "TOTAL". 
        t-list.qty = qty. 
        t-list.val = val. 
        t-list.t-qty = t-qty. 
        t-list.t-val = t-val. 
        qty = 0. 
        val = 0. 
        t-qty = 0. 
        t-val = 0. 
        f-lager = l-lager.lager-nr. 
      END. 

      FIND FIRST t-list WHERE t-list.f-lager = l-lager.lager-nr 
        AND INTEGER(t-list.artnr) = l-artikel.artnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        t-list.f-lager = l-lager.lager-nr. 
        IF f-lager NE l-lager.lager-nr THEN 
        DO: 
          t-list.f-bezeich = l-lager.bezeich. 
          f-lager = l-lager.lager-nr. 
        END. 
        t-list.artnr = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
        t-list.einheit = l-artikel.masseinheit. 
        t-list.subgroup = l-artikel.zwkum.
        t-list.subbez = l-untergrup.bezeich.
      END. 
      IF l-op.datum = to-date THEN 
      DO: 
        t-list.qty = t-list.qty + l-op.anzahl. 
        t-list.val = t-list.val + l-op.warenwert. 
        qty = qty + l-op.anzahl. 
        val = val + l-op.warenwert. 
        st-qty = st-qty + l-op.anzahl. 
        st-val = st-val + l-op.warenwert. 
        d-qty = d-qty + l-op.anzahl. 
        d-val = d-val + l-op.warenwert. 
      END. 
      t-list.t-qty = t-list.t-qty + l-op.anzahl. 
      t-list.t-val = t-list.t-val + l-op.warenwert. 
      t-qty = t-qty + l-op.anzahl. 
      t-val = t-val + l-op.warenwert. 
      m-qty = m-qty + l-op.anzahl. 
      m-val = m-val + l-op.warenwert. 
      sm-qty = sm-qty + l-op.anzahl. 
      sm-val = sm-val + l-op.warenwert. 
      subgr = l-untergrup.bezeich.
    END.
    IF sm-qty NE 0 THEN
    DO:
        CREATE t-list.
        ASSIGN
            t-list.flag = 1
            t-list.bezeich = subgr
            t-list.qty = st-qty
            t-list.val = st-val
            t-list.t-qty = sm-qty
            t-list.t-val = sm-val
            st-qty = 0
            st-val = 0
            sm-qty = 0
            sm-val = 0.
    END.
    IF t-qty NE 0 THEN 
    DO: 
      create t-list. 
      t-list.flag = 1. 
      t-list.f-lager = f-lager. 
      t-list.bezeich = "TOTAL". 
      t-list.qty = qty. 
      t-list.val = val. 
      t-list.t-qty = t-qty. 
      t-list.t-val = t-val. 
    END. 
  END. 
  DO: 
    create t-list. 
    t-list.flag = 1. 
    t-list.f-lager = 9999. 
    t-list.bezeich = "GRAND TOTAL". 
    t-list.qty = d-qty. 
    t-list.val = d-val. 
    t-list.t-qty = m-qty. 
    t-list.t-val = m-val. 
    END. 
END. 
 
PROCEDURE create-list2: 
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE buffer l-store FOR l-lager. 
 
  status default "Processing...". 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK BY l-lager.lager-nr: 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
      AND l-op.anzahl NE 0 
      AND l-op.op-art = 1 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.zwkum GE from-grp AND l-artikel.zwkum LE to-grp 
      NO-LOCK BY l-artikel.bezeich: 
 
      IF f-lager NE l-lager.lager-nr AND t-qty NE 0 THEN 
      DO: 
        create t-list. 
        t-list.flag = 1. 
        t-list.f-lager = f-lager. 
        t-list.bezeich = "TOTAL". 
        t-list.qty = qty. 
        t-list.val = val. 
        t-list.t-qty = t-qty. 
        t-list.t-val = t-val. 
        qty = 0. 
        val = 0. 
        t-qty = 0. 
        t-val = 0. 
        f-lager = l-lager.lager-nr. 
      END. 
 
      FIND FIRST t-list WHERE t-list.f-lager = l-lager.lager-nr 
        AND INTEGER(t-list.artnr) = l-artikel.artnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        t-list.f-lager = l-lager.lager-nr. 
        IF f-lager NE l-lager.lager-nr THEN 
        DO: 
          t-list.f-bezeich = l-lager.bezeich. 
          f-lager = l-lager.lager-nr. 
        END. 
        t-list.artnr = STRING(l-op.artnr, "9999999"). 
        t-list.bezeich = l-artikel.bezeich. 
        t-list.einheit = l-artikel.masseinheit. 
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
      create t-list. 
      t-list.flag = 1. 
      t-list.f-lager = f-lager. 
      t-list.bezeich = "TOTAL". 
      t-list.qty = qty. 
      t-list.val = val. 
      t-list.t-qty = t-qty. 
      t-list.t-val = t-val. 
    END. 
  END. 
  DO: 
    create t-list. 
    t-list.flag = 1. 
    t-list.f-lager = 9999. 
    t-list.bezeich = "GRAND TOTAL". 
    t-list.qty = d-qty. 
    t-list.val = d-val. 
    t-list.t-qty = m-qty. 
    t-list.t-val = m-val. 
    END. 
END. 


PROCEDURE create-list4: 
DEFINE VARIABLE f-lager AS INTEGER. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE VARIABLE t-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-val AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-qty AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-val AS DECIMAL INITIAL 0. 
DEFINE buffer l-store FOR l-lager. 
 
  status default "Processing...". 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  f-lager = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK BY l-lager.lager-nr: 
    qty = 0. 
    val= 0. 
    t-qty = 0. 
    t-val = 0. 
    FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
      AND l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
      AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
      AND l-op.anzahl NE 0 
      AND l-op.op-art = 1 NO-LOCK USE-INDEX artopart_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.zwkum GE from-grp AND l-artikel.zwkum LE to-grp 
      NO-LOCK BY l-artikel.bezeich: 
 
      IF f-lager NE l-lager.lager-nr AND t-qty NE 0 THEN 
      DO: 
        create tt-list. 
        tt-list.flag = 1. 
        tt-list.f-lager = f-lager. 
        tt-list.bezeich = "TOTAL". 
        tt-list.qty = qty. 
        tt-list.val = val. 
        tt-list.t-qty = t-qty. 
        tt-list.t-val = t-val. 
        qty = 0. 
        val = 0. 
        t-qty = 0. 
        t-val = 0. 
        f-lager = l-lager.lager-nr. 
      END. 
      
      FIND FIRST tt-list WHERE tt-list.f-lager = l-lager.lager-nr 
        AND INTEGER(tt-list.artnr) = l-artikel.artnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE tt-list THEN 
      DO: 
        create tt-list. 
        tt-list.f-lager = l-lager.lager-nr. 
        IF f-lager NE l-lager.lager-nr THEN 
        DO: 
          tt-list.f-bezeich = l-lager.bezeich. 
          f-lager = l-lager.lager-nr. 
        END. 
        tt-list.artnr = STRING(l-op.artnr, "9999999"). 
        tt-list.bezeich = l-artikel.bezeich. 
        tt-list.einheit = l-artikel.masseinheit. 
      END. 

      IF tt-list.f-bezeich NE "" THEN  /*bernatd*/
      DO:
        create tt-list. 
        tt-list.f-lager = l-lager.lager-nr. 
        IF f-lager NE l-lager.lager-nr THEN 
        DO: 
          tt-list.f-bezeich = l-lager.bezeich. 
          f-lager = l-lager.lager-nr. 
        END. 
        tt-list.artnr = STRING(l-op.artnr, "9999999"). 
        tt-list.bezeich = l-artikel.bezeich. 
        tt-list.einheit = l-artikel.masseinheit. 
      END.
   
  
      IF l-op.datum = to-date THEN 
      DO: 
        tt-list.qty = tt-list.qty + l-op.anzahl. 
        tt-list.val = tt-list.val + l-op.warenwert. 
        qty = qty + l-op.anzahl. 
        val = val + l-op.warenwert. 
        d-qty = d-qty + l-op.anzahl. 
        d-val = d-val + l-op.warenwert. 
      END. 
      tt-list.t-qty = tt-list.t-qty + l-op.anzahl. 
      tt-list.t-val = tt-list.t-val + l-op.warenwert. 
      t-qty = t-qty + l-op.anzahl. 
      t-val = t-val + l-op.warenwert. 
      m-qty = m-qty + l-op.anzahl. 
      m-val = m-val + l-op.warenwert. 
    END. 
    IF t-qty NE 0 THEN 
    DO: 
      create tt-list. 
      tt-list.flag = 1. 
      tt-list.f-lager = f-lager. 
      tt-list.bezeich = "TOTAL". 
      tt-list.qty = qty. 
      tt-list.val = val. 
      tt-list.t-qty = t-qty. 
      tt-list.t-val = t-val. 
    END. 
  END. 
  DO: 
    create tt-list. 
    tt-list.flag = 1. 
    tt-list.f-lager = 9999. 
    tt-list.bezeich = "GRAND TOTAL". 
    tt-list.qty = d-qty. 
    tt-list.val = d-val. 
    tt-list.t-qty = m-qty. 
    tt-list.t-val = m-val. 
    END. 
END. 



PROCEDURE create-output:

    FOR EACH tt-list NO-LOCK:
        CREATE temp-list.
        BUFFER-COPY tt-list TO temp-list.  
    END.
    
    FOR EACH tt-list WHERE tt-list.bezeich EQ "TOTAL" AND tt-list.f-lager NE 9999 NO-LOCK BY tt-list.t-val DESCENDING:
        FIND FIRST temp-list WHERE temp-list.f-lager EQ tt-list.f-lager AND temp-list.f-bezeich NE "" NO-LOCK NO-ERROR.
        IF AVAILABLE temp-list THEN 
        DO:
            CREATE t-list.
            ASSIGN
                t-list.artnr       = temp-list.artnr
                t-list.bezeich     = temp-list.bezeich
                t-list.einheit     = temp-list.einheit
                t-list.f-bezeich   = temp-list.f-bezeich
                t-list.f-lager     = temp-list.f-lager
                t-list.flag        = temp-list.flag
                t-list.qty         = temp-list.qty
                t-list.subbez      = temp-list.subbez
                t-list.subgroup    = temp-list.subgroup
                t-list.t-qty       = temp-list.t-qty
                t-list.t-val       = temp-list.t-val
                t-list.val         = temp-list.val. 
        END.
            
        FOR EACH temp-list WHERE temp-list.f-lager EQ tt-list.f-lager AND temp-list.bezeich NE "TOTAL" NO-LOCK BY temp-list.t-val DESCENDING:
            CREATE t-list.
            ASSIGN
                t-list.artnr       = temp-list.artnr
                t-list.bezeich     = temp-list.bezeich
                t-list.einheit     = temp-list.einheit
                t-list.f-bezeich   = temp-list.f-bezeich
                t-list.f-lager     = temp-list.f-lager
                t-list.flag        = temp-list.flag
                t-list.qty         = temp-list.qty
                t-list.subbez      = temp-list.subbez
                t-list.subgroup    = temp-list.subgroup
                t-list.t-qty       = temp-list.t-qty
                t-list.t-val       = temp-list.t-val
                t-list.val         = temp-list.val.
        END. 

        FIND FIRST temp-list WHERE temp-list.f-lager EQ t-list.f-lager AND temp-list.bezeich EQ "TOTAL" NO-LOCK NO-ERROR.
        IF AVAILABLE temp-list THEN 
        DO:
            CREATE t-list.
            ASSIGN
                t-list.artnr       = temp-list.artnr
                t-list.bezeich     = temp-list.bezeich
                t-list.einheit     = temp-list.einheit
                t-list.f-bezeich   = temp-list.f-bezeich
                t-list.f-lager     = temp-list.f-lager
                t-list.flag        = temp-list.flag
                t-list.qty         = temp-list.qty
                t-list.subbez      = temp-list.subbez
                t-list.subgroup    = temp-list.subgroup
                t-list.t-qty       = temp-list.t-qty
                t-list.t-val       = temp-list.t-val
                t-list.val         = temp-list.val. 
        END. 
    END. 

    FIND FIRST temp-list WHERE temp-list.f-lager EQ 9999 NO-LOCK NO-ERROR.
    IF AVAILABLE temp-list THEN 
    DO:
        CREATE t-list.
        ASSIGN
            t-list.flag        = temp-list.flag
            t-list.f-lager     = temp-list.f-lager
            t-list.bezeich   = temp-list.bezeich
            t-list.qty         = temp-list.qty
            t-list.t-qty       = temp-list.t-qty
            t-list.t-val       = temp-list.t-val
            t-list.val         = temp-list.val.
    END.
END.














