DEFINE buffer gl-acc1    FOR gl-acct.
DEFINE buffer gl-acct1   FOR gl-acct.
DEFINE buffer gl-jouhdr1 FOR gl-jouhdr.

DEFINE TEMP-TABLE g-list 
  FIELD  nr         AS INTEGER 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  bemerk     AS CHAR FORMAT "x(32)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES
    
  FIELD  acct-fibukonto LIKE gl-acct1.fibukonto
  FIELD  acct-bezeich   LIKE gl-acct1.bezeich.

DEF INPUT PARAMETER TABLE FOR g-list.
DEF INPUT PARAMETER amt         AS DECIMAL.
DEF INPUT PARAMETER nr          AS INT.
DEF INPUT PARAMETER datum       AS DATE.
DEF INPUT PARAMETER refno       AS CHAR.
DEF INPUT PARAMETER bezeich     AS CHAR.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER remains     AS DECIMAL.
DEF INPUT PARAMETER debits      AS DECIMAL.
DEF INPUT PARAMETER credits     AS DECIMAL.
DEF INPUT PARAMETER qty         AS INT.
DEF INPUT PARAMETER fa-wert     AS DECIMAL. 
DEF INPUT PARAMETER depn-wert   AS DECIMAL. 
DEF INPUT PARAMETER book-wert   AS DECIMAL. 
DEF OUTPUT PARAMETER sold-out   AS LOGICAL INITIAL NO.

DEFINE VARIABLE new-hdr         AS LOGICAL INITIAL YES.

FIND FIRST fa-artikel WHERE fa-artikel.nr = nr NO-LOCK.
RUN create-header. 
RUN create-journals. 
RUN update-fix-asset.

PROCEDURE create-header: 
  create gl-jouhdr. 
  FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE counters THEN 
  DO: 
    create counters. 
    counters.counter-no = 25. 
    counters.counter-bez = "G/L Transaction Journal". 
  END. 
  counters.counter = counters.counter + 1. 
  FIND CURRENT counters NO-LOCK.
  gl-jouhdr.jnr = counters.counter. 
  gl-jouhdr.refno = refno.
  gl-jouhdr.datum = datum. 
  gl-jouhdr.bezeich = bezeich. 
  gl-jouhdr.batch = YES. 
  gl-jouhdr.jtype = 7. 
  new-hdr = YES. 
END. 
 
PROCEDURE create-journals: 
  FOR EACH g-list  NO-LOCK: 
    create gl-journal. 
    gl-journal.jnr = counters.counter. 
    gl-journal.fibukonto = g-list.fibukonto. 
    gl-journal.debit = g-list.debit. 
    gl-journal.credit = g-list.credit. 
    gl-journal.bemerk = g-list.bemerk. 
    gl-journal.userinit = g-list.userinit. 
    gl-journal.zeit = g-list.zeit. 
  END. 
  DO transaction: 
    IF remains = 0.01 OR remains = - 0.01 THEN remains = 0. 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    gl-jouhdr.credit = credits. 
    gl-jouhdr.debit = debits. 
    gl-jouhdr.remain = remains. 
    FIND CURRENT gl-jouhdr NO-LOCK. 
  END. 
  release gl-jouhdr. 
END. 
 
PROCEDURE update-fix-asset: 
DEFINE VARIABLE orig-bookval AS DECIMAL. 
  sold-out = (fa-artikel.anzahl = qty). 
  orig-bookval = fa-artikel.book-wert. 
  FIND CURRENT fa-artikel EXCLUSIVE-LOCK. 
  fa-artikel.posted = YES. 
  IF sold-out THEN 
  DO: 
    fa-artikel.loeschflag = 1. 
    fa-artikel.deleted = TODAY. 
  END. 
  ELSE 
  DO: 
    fa-artikel.anzahl = fa-artikel.anzahl - qty. 
    fa-artikel.warenwert = fa-artikel.warenwert - fa-wert. 
    fa-artikel.depn-wert = fa-artikel.depn-wert - depn-wert. 
    fa-artikel.book-wert = fa-artikel.book-wert - book-wert. 
  END. 
  fa-artikel.did = user-init. 
  FIND CURRENT fa-artikel NO-LOCK. 
 
  create mhis-line. 
  mhis-line.nr = nr. 
  mhis-line.datum = datum. 
  mhis-line.remark = "Sold Out: Qty = " + STRING(qty) 
    + "; Amount = " + TRIM(STRING(amt,">>>,>>>,>>>,>>9.99")). /*wen tambah digit 23/02/17*/
  FIND CURRENT mhis-line NO-LOCK. 
 
  create fa-op. 
  fa-op.nr = nr. 
  fa-op.opart = 3. 
  fa-op.datum = datum. 
  fa-op.zeit = TIME. 
  fa-op.anzahl = qty. 
  fa-op.einzelpreis = orig-bookval. 
  fa-op.warenwert = book-wert. 
  fa-op.id = user-init. 
  fa-op.lscheinnr = refno. 
  fa-op.docu-nr = bezeich. 
  fa-op.lief-nr = fa-artikel.lief-nr. 
  release fa-op. 
END. 
