
DEF INPUT  PARAMETER pvILanguage   AS INTEGER      NO-UNDO.
DEF OUTPUT PARAMETER msg-str       AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "closemonth".

DEFINE VARIABLE pnl-acct    AS CHAR.
DEFINE VARIABLE balance     AS DECIMAL.
DEFINE VARIABLE curr-date   AS DATE.
DEFINE VARIABLE first-date  AS DATE. 
DEFINE VARIABLE err-acct    AS LOGICAL INIT NO.

/********** Check IF the closing DATE is correct ********/ 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
curr-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 795 no-lock.   /* Last Closing Year Date*/ 
IF (YEAR(htparam.fdate) + 1) LT YEAR(curr-date) THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Closing Year not yet done!",lvCAREA,"").
  RETURN. 
END.

FIND FIRST htparam WHERE paramnr = 558 no-lock. /* LAST Accounting Period */ 
first-date = htparam.fdate + 1.         /* Rulita 211024 | Fixing for serverless */
IF htparam.fdate GE curr-date THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Closing date incorrect (Parameter 558).",lvCAREA,"").
  RETURN. 
END.

FIND FIRST htparam WHERE paramnr = 979 NO-LOCK. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("P&L Account not defined (Parameter 979).",lvCAREA,"").
    RETURN. 
END. 
pnl-acct = gl-acct.fibukonto.


FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
  AND gl-jouhdr.datum GE first-date AND gl-jouhdr.datum LE curr-date 
  NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE gl-jouhdr: 
  balance  = 0.
  err-acct = NO.
  /*MTcurr-bezeich = translateExtended ("Check Journals",lvCAREA,"") + " " 
      + gl-jouhdr.refno. 
  DISP curr-bezeich WITH FRAME frame1. */

  FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK: 
    /*check gl-acct*/
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN DO:
        ASSIGN err-acct = YES.
    END. /*end*/
    balance = balance + gl-journal.debit - gl-journal.credit. 
  END. 

  IF err-acct = YES THEN DO:
      msg-str = translateExtended ("Chart of Account : ",lvCAREA,"") + gl-journal.fibukonto + 
                  translateExtended (" not defined ",lvCAREA,"").
      RETURN.
  END.

  IF balance GT 0 AND balance GT 0.01 OR 
    balance LT 0 AND balance LT (- 0.01) THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Not balanced Journals found; trial not possible.",lvCAREA,"")
            + CHR(10)
            + translateExtended ("Date:",lvCAREA,"") + " " + STRING(gl-jouhdr.datum) + " - "
            + translateExtended ("RefNo:",lvCAREA,"") + " " + gl-jouhdr.refno.
    RETURN. 
  END. 
  FIND NEXT gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
    AND gl-jouhdr.datum GE first-date AND gl-jouhdr.datum LE curr-date 
    NO-LOCK NO-ERROR. 
END. 
