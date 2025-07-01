DEFINE TEMP-TABLE g-list 
  FIELD jnr             LIKE gl-journal.jnr 
  FIELD fibukonto       LIKE gl-journal.fibukonto
  FIELD acct-fibukonto  LIKE gl-acct.fibukonto
  FIELD debit           LIKE gl-journal.debit 
  FIELD credit          LIKE gl-journal.credit 
  FIELD userinit        LIKE gl-journal.userinit 
  FIELD sysdate         LIKE gl-journal.sysdate INITIAL today 
  FIELD zeit            LIKE gl-journal.zeit 
  FIELD chginit         LIKE gl-journal.chginit 
  FIELD chgdate         LIKE gl-journal.chgdate INITIAL ? 
  FIELD bemerk          LIKE gl-journal.bemerk
  FIELD bezeich         LIKE gl-acct.bezeich
  FIELD duplicate       AS LOGICAL INITIAL YES
  /*gst for penang*/
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS CHAR
  FIELD tot-amt     AS CHAR.

DEF TEMP-TABLE buf-g-list LIKE g-list.

DEF INPUT PARAMETER jnr AS INT.
DEF OUTPUT PARAMETER credits LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER debits LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER remains LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER TABLE FOR buf-g-list.

DEFINE buffer gl-acct1 FOR gl-acct. 

FOR EACH gl-journal WHERE gl-journal.jnr = jnr NO-LOCK: 
    create g-list. 
    g-list.fibukonto = gl-journal.fibukonto. 
    g-list.debit = gl-journal.debit. 
    g-list.credit = gl-journal.credit. 
    g-list.userinit = gl-journal.userinit. 
    g-list.sysdate = gl-journal.sysdate. 
    g-list.zeit = gl-journal.zeit. 
    g-list.chginit = gl-journal.chginit. 
    g-list.chgdate = gl-journal.chgdate. 
    g-list.bemerk = gl-journal.bemerk. 
    credits = credits + gl-journal.credit. 
    debits = debits + gl-journal.debit. 
    remains = debits - credits. 
END.

FOR EACH g-list NO-LOCK, 
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK 
    BY g-list.sysdate descending BY g-list.zeit DESCENDING:
    CREATE buf-g-list.
    BUFFER-COPY g-list TO buf-g-list.
    ASSIGN buf-g-list.acct-fibukonto = gl-acct1.fibukonto
           buf-g-list.bezeich        = gl-acct1.bezeich.

    IF NUM-ENTRIES(gl-acct1.bemerk, ";") GT 1 THEN
        ASSIGN buf-g-list.tax-code = ENTRY(2, gl-acct1.bemerk, ";").
END.
