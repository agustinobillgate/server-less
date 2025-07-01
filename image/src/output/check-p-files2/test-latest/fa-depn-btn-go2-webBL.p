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
    
  FIELD gl-acct1-fibukonto AS CHARACTER
  FIELD gl-acct1-bezeich AS CHARACTER.

DEF INPUT-OUTPUT PARAMETER TABLE FOR g-list.
DEF INPUT PARAMETER datum   AS DATE.
DEF INPUT PARAMETER refno   AS CHAR.
DEF INPUT PARAMETER bezeich AS CHAR.
DEF INPUT PARAMETER debits  AS DECIMAL.
DEF INPUT PARAMETER credits AS DECIMAL.
DEF INPUT PARAMETER remains AS DECIMAL.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEFINE VARIABLE new-hdr     AS LOGICAL INITIAL YES.
RUN create-header. 
RUN create-journals. 
RUN update-fix-asset. 
FIND FIRST htparam WHERE paramnr = 881 EXCLUSIVE-LOCK. 
htparam.fdate = datum.
FIND CURRENT htparam NO-LOCK.

success-flag = YES.

/*******************************************************************************************/
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
  DEFINE VARIABLE next-date AS DATE. 

  /* Malik add history FA */
  DEFINE VARIABLE depn-wert-hist AS DECIMAL. 
  DEFINE VARIABLE anz-depn-hist AS INTEGER. 
  DEFINE VARIABLE book-wert-hist AS DECIMAL. 
  DEFINE BUFFER fa-artikel-buff FOR fa-artikel. 

  next-date = datum + 35. 
  next-date = DATE(month(next-date), 1, year(next-date)) - 1. 
  FOR EACH g-list: 
    IF g-list.credit NE 0 THEN 
    DO: 
      /* Malik 4E136B -> add history FA  */
      FIND FIRST queasy WHERE queasy.key = 348 AND queasy.number1 = g-list.nr 
        AND queasy.date1 = datum NO-LOCK NO-ERROR.
      IF NOT AVAILABLE queasy THEN
      DO:
          FIND FIRST fa-artikel-buff WHERE fa-artikel-buff.nr = g-list.nr NO-LOCK NO-ERROR.

          depn-wert-hist = fa-artikel-buff.depn-wert + g-list.credit.
          anz-depn-hist = fa-artikel-buff.anz-depn + 1.
          book-wert-hist = fa-artikel-buff.book-wert - g-list.credit.

          CREATE queasy.
          ASSIGN
            queasy.key = 348
            queasy.number1  = g-list.nr
            queasy.number2  = fa-artikel-buff.anzahl /* Quantity */
            queasy.date1    = datum
            queasy.deci1    = depn-wert-hist  /* depreciation value */
            queasy.number3  = anz-depn-hist   /* total depreciation */
            queasy.deci2    = book-wert-hist.  /* Booking Value */
      END.
      /* END malik */

      FIND FIRST fa-artikel WHERE fa-artikel.nr = g-list.nr NO-LOCK NO-ERROR. 
      IF AVAILABLE fa-artikel THEN
      DO:
        FIND CURRENT fa-artikel EXCLUSIVE-LOCK.
        fa-artikel.posted = YES. 
        IF fa-artikel.first-depn = ? THEN fa-artikel.first-depn = datum. 
        fa-artikel.last-depn = datum. 
        fa-artikel.depn-wert = fa-artikel.depn-wert + g-list.credit. 
        fa-artikel.book-wert = fa-artikel.book-wert - g-list.credit. 
        fa-artikel.anz-depn = fa-artikel.anz-depn + 1. 
        IF fa-artikel.book-wert GT 0 THEN fa-artikel.next-depn = next-date. 
        FIND CURRENT fa-artikel NO-LOCK. 
      END.
    END. 
    delete g-list. 
  END. 
END. 
