
DEF INPUT  PARAMETER curr-date  AS DATE.
DEF OUTPUT PARAMETER acctNo     AS CHAR.
DEF OUTPUT PARAMETER betrag     AS DECIMAL.

DEF VAR mm-close  AS DATE.
DEF VAR yy-close  AS DATE.
DEF VAR fibukonto AS CHAR.

FIND FIRST gc-piacct WHERE gc-piacct.nr = nr NO-LOCK.
acctNo = gc-piacct.fibukonto.
FIND FIRST gl-acct WHERE gl-acct.fibukonto = acctNo NO-LOCK.

betrag = 0.
FIND FIRST htparam WHERE htparam.paramnr = 558 NO-LOCK.
ASSIGN mm-close = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 795 NO-LOCK.
ASSIGN yy-close = htparam.fdate.

IF YEAR(mm-close) = YEAR(curr-date) THEN
  betrag = gl-acct.actual[MONTH(mm-close)].
ELSE IF YEAR(yy-close) = YEAR(curr-date) - 2 THEN
  betrag = gl-acct.actual[MONTH(mm-close)].
ELSE IF YEAR(yy-close) = YEAR(curr-date) - 1 THEN
  betrag = gl-acct.last-yr[MONTH(mm-close)].
FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GT mm-close NO-LOCK,
  EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
  AND gl-journal.fibukonto = acctNo NO-LOCK:
  betrag = betrag + gl-journal.debit - gl-journal.credit.
END.
