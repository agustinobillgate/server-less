/*MESSAGE "stock-transformlist-create-listBL.p - Start"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug*/*/

DEFINE TEMP-TABLE t-list 
  FIELD datum       AS DATE 
  FIELD lscheinnr   AS CHAR FORMAT "x(11)" 
  FIELD f-bezeich   AS CHAR FORMAT "x(24)" 
  FIELD t-bezeich   AS CHAR FORMAT "x(16)" 
  FIELD artnr       AS CHAR FORMAT "x(7)" 
  FIELD bezeich     AS CHAR FORMAT "x(29)" 
  FIELD einheit     AS CHAR FORMAT "x(3)" 
  FIELD content     AS DECIMAL FORMAT "->>>,>>>" /*Alder - Ticket 4CB0F0*/
  FIELD price       AS CHAR FORMAT "x(13)" 
  FIELD qty         AS DECIMAL FORMAT "->>>,>>9.999" /*Alder - Ticket 4CB0F0*/
  FIELD s-qty       AS CHAR FORMAT "x(11)" 
  FIELD op-art      AS INTEGER 
  FIELD val         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99". /*Alder - Ticket 4CB0F0*/

DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER from-art   AS INT.
DEF INPUT  PARAMETER to-art     AS INT.
DEF OUTPUT PARAMETER it-exist   AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

/*MESSAGE "RUN create-list - Start"
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/

RUN create-list.

/*MESSAGE "RUN create-list - End"
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/

PROCEDURE create-list:
DEFINE VARIABLE lscheinnr   AS CHAR. 
DEFINE VARIABLE qty         AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE val         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99". /*Alder - Ticket 4CB0F0*/ 
DEFINE VARIABLE t-qty       AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val       AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0. /*Alder - Ticket 4CB0F0*/ 
DEFINE buffer l-store FOR l-lager. 

  it-exist = NO. 
  FOR EACH t-list: 
    delete t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  lscheinnr = "". 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.artnr GE from-art AND l-op.artnr LE to-art 
    AND l-op.op-art GE 2 AND l-op.op-art LE 4 
    AND l-op.herkunftflag = 3 AND l-op.loeschflag LE 1 
    NO-LOCK USE-INDEX artopart_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.datum BY l-op.lscheinnr BY l-op.op-art /*DESCENDING*/ /*Alder - Ticket 4CB0F0*/ 
    BY l-op.zeit: 
    it-exist = YES. 
    FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
    FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
    
    /*MESSAGE "l-op.lscheinnr : " l-op.lscheinnr SKIP
        "lscheinnr : " lscheinnr SKIP
        VIEW-AS ALERT-BOX INFO BUTTONS OK.  /*Alder Debug*/*/

    IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
    DO: 
      create t-list. 
      t-list.price = "Total". 
      t-list.qty = qty. 
      t-list.val = val. 
      qty = 0. 
      val = 0. 
    END. 
    lscheinnr = l-op.lscheinnr. 

    /*MESSAGE "l-op.lscheinnr : " l-op.lscheinnr SKIP
        "lscheinnr : " lscheinnr SKIP
        VIEW-AS ALERT-BOX INFO BUTTONS OK.  /*Alder Debug*/*/
 
    create t-list. 
    t-list.datum = l-op.datum. 
    t-list.lscheinnr = lscheinnr. 
    t-list.f-bezeich = l-lager.bezeich. 
    IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 
    t-list.artnr = STRING(l-op.artnr, "9999999"). 
    t-list.bezeich = l-artikel.bezeich. 
    t-list.einheit = l-artikel.masseinheit. 
    t-list.content = l-artikel.inhalt. 
    IF l-op.anzahl NE 0 THEN 
    DO: 
      IF NOT long-digit THEN 
        t-list.price = STRING((l-op.warenwert / l-op.anzahl), "->>,>>>,>>9.99"). /*Alder - Ticket 4CB0F0*/
      ELSE 
      t-list.price = STRING((l-op.warenwert / l-op.anzahl), "->,>>>,>>>,>>9"). /*Alder - Ticket 4CB0F0*/
    END. 
    t-list.qty = l-op.anzahl. 
    t-list.val = l-op.warenwert. 
    t-list.s-qty = STRING(t-list.qty, "->>>,>>9.999"). /*Alder - Ticket 4CB0F0*/
    t-list.op-art = l-op.op-art. 
    IF l-op.op-art = 2 THEN 
    DO: 
      val = val + l-op.warenwert. 
      t-val = t-val + l-op.warenwert. 
    END. 
  END.
    
  /* 0AB3B5 Rulita | show item yg sudah di closed inventory */
  FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date
      AND l-ophis.artnr GE from-art AND l-ophis.artnr LE to-art
      AND l-ophis.op-art GE 2 AND l-ophis.op-art LE 4 
      AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") 
      NO-LOCK,
      FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      NO-LOCK BY l-ophis.datum BY l-ophis.lscheinnr BY l-ophis.op-art /*DESCENDING*/ /*Alder - Ticket 4CB0F0*/  :
      FIND FIRST l-lager WHERE l-lager.lager-nr = l-ophis.lager-nr NO-LOCK. 
      
      it-exist = NO.
      IF lscheinnr NE l-ophis.lscheinnr AND qty NE 0 THEN 
      DO: 
        create t-list. 
        t-list.price = "Total". 
        t-list.qty = qty. 
        t-list.val = val. 
        qty = 0. 
        val = 0. 
      END. 
      lscheinnr = l-ophis.lscheinnr. 
      
      create t-list. 
      t-list.datum = l-ophis.datum. 
      t-list.lscheinnr = lscheinnr. 
      t-list.f-bezeich = l-lager.bezeich. 
      t-list.t-bezeich = "". 
      t-list.artnr = STRING(l-ophis.artnr, "9999999"). 
      t-list.bezeich = l-artikel.bezeich. 
      t-list.einheit = l-artikel.masseinheit. 
      t-list.content = l-artikel.inhalt. 
      IF l-ophis.anzahl NE 0 THEN 
      DO: 
        IF NOT long-digit THEN 
          t-list.price = STRING((l-ophis.warenwert / l-ophis.anzahl), "->>,>>>,>>9.99"). /*Alder - Ticket 4CB0F0*/
        ELSE 
        t-list.price = STRING((l-ophis.warenwert / l-ophis.anzahl), "->,>>>,>>>,>>9"). /*Alder - Ticket 4CB0F0*/
      END. 
      t-list.qty = l-ophis.anzahl. 
      t-list.val = l-ophis.warenwert. 
      t-list.s-qty = STRING(t-list.qty, "->>>,>>9.999"). /*Alder - Ticket 4CB0F0*/
      t-list.op-art = l-ophis.op-art. 
      IF l-ophis.op-art = 2 THEN 
      DO: 
        val = val + l-ophis.warenwert. 
        t-val = t-val + l-ophis.warenwert. 
      END. 
  END.

  IF val NE 0 THEN 
  DO: 
    create t-list. 
    t-list.price = "Total". 
    t-list.qty = qty. 
    t-list.val = val. 
  END. 
  IF t-val NE 0 THEN 
  DO: 
    create t-list. 
    t-list.price = "Grand Total". 
    t-list.qty = t-qty. 
    t-list.val = t-val. 
  END. 
END. 

/*MESSAGE "stock-transformlist-create-listBL.p - End"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug*/*/
