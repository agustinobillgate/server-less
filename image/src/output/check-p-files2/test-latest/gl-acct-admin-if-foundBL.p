
DEF INPUT  PARAMETER fibukonto AS CHAR.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

DEF VAR i AS INT.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN
DO:
    DO i = 1 TO 12:
      IF gl-acct.budget[i] GT 0 THEN gl-acct.budget[i] = - gl-acct.budget[i]. 
      IF gl-acct.ly-budget[i] GT 0 THEN gl-acct.ly-budget[i] = - gl-acct.ly-budget[i]. 
      IF gl-acct.debit[i] GT 0 THEN gl-acct.debit[i] = - gl-acct.debit[i].
    END.
    success-flag = YES.
END.
