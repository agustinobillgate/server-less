
DEF INPUT PARAMETER docu-nr         AS CHAR.
DEF INPUT PARAMETER pbuff-returnAmt LIKE gc-PI.returnAmt.
DEF INPUT PARAMETER pbuff-datum2    LIKE gc-PI.datum2.
DEF INPUT PARAMETER ret-acctNo      AS CHAR.

DEF OUTPUT PARAMETER fl-err  AS INT.

DO TRANSACTION:
    FIND FIRST gc-PI WHERE gc-pi.docu-nr = docu-nr EXCLUSIVE-LOCK.
    ASSIGN
      gc-PI.returnAmt = pbuff-returnAmt
      gc-PI.datum2    = pbuff-datum2
    .
    FIND FIRST gc-PIacct WHERE gc-PIacct.fibukonto = ret-acctNo NO-LOCK NO-ERROR.
    IF AVAILABLE gc-PIacct THEN ASSIGN gc-PI.return-fibu = ret-acctNo.
    FIND CURRENT gc-PI NO-LOCK.
END.


IF pbuff-returnAmt NE 0 THEN
DO:
    FIND FIRST gc-PIacct WHERE gc-PIacct.fibukonto = ret-acctNo NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gc-PIacct THEN
    DO:
      fl-err = 1.
      RETURN.
    END.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = ret-acctNo NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
      fl-err = 2.
      RETURN.
    END.
END.
