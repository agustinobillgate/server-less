DEFINE INPUT  PARAMETER gnr             AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER avail-fibukonto AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER avail-credit    AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER avail-debit     AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER fibukonto       AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER credit-fibu     AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER debit-fibu      AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER sgrp-bez        AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER err-nr          AS INTEGER NO-UNDO.

FIND FIRST fa-grup WHERE fa-grup.gnr = gnr AND fa-grup.flag = 1 NO-LOCK.
IF NOT AVAILABLE fa-grup THEN DO:
    ASSIGN err-nr = 1.
    RETURN NO-APPLY.
END.
ASSIGN sgrp-bez = fa-grup.bezeich.


FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto
  NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN 
DO:
  ASSIGN
      fibukonto       = gl-acct.fibukonto
      avail-fibukonto = YES.
END.
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.credit-fibu
  NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN 
DO:
  ASSIGN 
      credit-fibu  = gl-acct.fibukonto
      avail-credit = YES.
END.
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.debit-fibu
  NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN 
DO:
  ASSIGN
      debit-fibu   = gl-acct.fibukonto
      avail-debit  = YES.
END.
