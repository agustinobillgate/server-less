

DEF INPUT  PARAMETER pvILanguage   AS INTEGER      NO-UNDO.
DEF OUTPUT PARAMETER curr-date     AS DATE.
DEF OUTPUT PARAMETER msg-str       AS CHAR.

DEFINE VARIABLE curr-closeyr    AS INTEGER.
DEFINE VARIABLE balance         AS DECIMAL.
DEFINE VARIABLE pnl-acct        AS CHAR.
DEFINE VARIABLE first-date      AS DATE. 

/*FDL Jan 20, 2023 => Ticket 267932*/
DEFINE VARIABLE bom-597         AS DATE.
DEFINE VARIABLE end-of-month    AS DATE.
DEFINE VARIABLE param269        AS DATE.
DEFINE VARIABLE param1003       AS DATE.
DEFINE VARIABLE param1014       AS DATE.
DEFINE VARIABLE param1035       AS DATE.
DEFINE VARIABLE param1118       AS DATE.
DEFINE VARIABLE param1123       AS DATE.
/*FDL Feb 16, 2024 => Ticket B73034*/
DEFINE VARIABLE param221        AS DATE.
DEFINE VARIABLE param224        AS DATE.
DEFINE VARIABLE param988        AS LOGICAL.
DEFINE VARIABLE param996        AS LOGICAL.
DEFINE VARIABLE param1016       AS LOGICAL.
DEFINE VARIABLE param997        AS LOGICAL.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "closemonth".

/********** Check IF the closing DATE is correct ********/ 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
curr-date = htparam.fdate. 
 
/*FDL Jan 20, 2023 => Ticket 267932*/
FIND FIRST htparam WHERE paramnr = 269 no-lock.   /* Last receiving Transfer Date to GL */ 
param269 = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 1003 no-lock.   /* Last F/O Transfer Date to GL */ 
param1003 = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 1014 no-lock.   /* Last A/R Transfer Date to GL */ 
param1014 = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 1035 no-lock.   /* Last Inventory Transfer Date to GL */ 
param1035 = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 1118 no-lock.   /* Last A/P Transfer Date to GL */ 
param1118 = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 1123 no-lock.   /* Last FB Compli Transfer Date to GL */ 
param1123 = htparam.fdate. 
/*FDL Feb 16, 2024 => Ticket B73034*/
FIND FIRST htparam WHERE paramnr = 221 no-lock.   /* Current Inv Closing Material */ 
param221 = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 no-lock.   /* Current Inv Closing FB */ 
param224 = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 988 no-lock.   /* License Inventory */ 
param988 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 996 no-lock.   /* License FO */ 
param996 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 1016 no-lock.   /* License AP */ 
param1016 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 997 no-lock.   /* License AR */ 
param997 = htparam.flogical.
/*
bom-597 = DATE(MONTH(curr-date),1,YEAR(curr-date)).
end-of-month = bom-597 - 1.
*/
/*FDL Feb 16, 2024 => Ticket B73034*/
IF param996 THEN
DO:
    IF param1003 LT curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, please check Parameter 1003.",lvCAREA,"").
        RETURN. 
    END.
END.
IF param1016 THEN
DO:
    IF param1118 LT curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, please check Parameter 1118.",lvCAREA,"").
        RETURN. 
    END.
END.
IF param997 THEN
DO:
    IF param1014 LT curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, please check Parameter 1014.",lvCAREA,"").
        RETURN. 
    END.
END.
IF param988 THEN
DO:
    IF param269 LT curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, please check Parameter 269.",lvCAREA,"").
        RETURN. 
    END.
    ELSE IF param1035 LT curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, please check Parameter 1035.",lvCAREA,"").
        RETURN. 
    END.
    ELSE IF param1123 LT curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, please check Parameter 1123.",lvCAREA,"").
        RETURN. 
    END.

    IF param221 LE curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, inventory has not yet closed.",lvCAREA,"")
            + CHR(10) + translateExtended ("Please check Parameter 221.",lvCAREA,"").
        RETURN.
    END.
    ELSE IF param224 LE curr-date THEN
    DO:
        msg-str = msg-str + CHR(2)
            + translateExtended ("Closing month not possible, inventory has not yet closed.",lvCAREA,"")
            + CHR(10) + translateExtended ("Please check Parameter 224.",lvCAREA,"").
        RETURN.
    END.
END.
/*End FDL*/

FIND FIRST htparam WHERE paramnr = 558 no-lock. /* LAST Accounting Period */ 
first-date = fdate + 1. 
IF htparam.fdate GE curr-date THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Closing date incorrect (Parameter 558).",lvCAREA,"").
  RETURN. 
END. 
 
FIND FIRST htparam WHERE paramnr = 795 no-lock. /* LAST YEAR Accounting Date */ 
curr-closeyr = YEAR(htparam.fdate) + 1.
IF YEAR(curr-date) GT curr-closeyr THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Closing Year has not been done yet.",lvCAREA,"").
  RETURN. 
END.

/******* Check IF batch file(s) still exists ******/ 
FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
  AND gl-jouhdr.batch AND gl-jouhdr.datum LE curr-date NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Batch journal(s) still exists, closing not possible.",lvCAREA,"")
          + CHR(10)
          + STRING(gl-jouhdr.datum) + " - " + gl-jouhdr.refno.
  RETURN. 
END.

/******* Check IF profit-lost account was set *****/ 
FIND FIRST htparam WHERE paramnr = 979 NO-LOCK. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("P&L Account not defined (Parameter 979).",lvCAREA,"").
    RETURN. 
END. 
pnl-acct = gl-acct.fibukonto.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 1
  AND gl-jouhdr.datum GE first-date AND gl-jouhdr.datum LE curr-date 
  NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Closed Journal found! Re-check it.",lvCAREA,"").
  RETURN. 
END.


FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
  AND gl-jouhdr.datum GE first-date AND gl-jouhdr.datum LE curr-date 
  NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE gl-jouhdr: 
  balance = 0. 
  /*MTcurr-bezeich = "Check Journals " + gl-jouhdr.refno. 
  DISP curr-bezeich WITH FRAME frame1. */
 
  FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK: 
    balance = balance + gl-journal.debit - gl-journal.credit. 
  END. 
  IF balance GT 0 AND balance GT 0.01 OR 
    balance LT 0 AND balance LT (- 0.01) THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Not balanced Journals found (closing not possible).",lvCAREA,"")
            + CHR(10)
            + translateExtended ("Date : ",lvCAREA,"") + STRING(gl-jouhdr.datum) + " - "
            + translateExtended ("RefNo : ",lvCAREA,"") + gl-jouhdr.refno.
    RETURN. 
  END. 
  FIND NEXT gl-jouhdr WHERE gl-jouhdr.activeflag = 0 AND 
    gl-jouhdr.datum GE first-date AND gl-jouhdr.datum LE curr-date 
    NO-LOCK NO-ERROR. 
END.
