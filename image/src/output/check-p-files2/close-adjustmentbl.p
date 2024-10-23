

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER closed         AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "close-adjustment".

DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE curr-month      AS INTEGER. 
DEFINE VARIABLE curr-year       AS INTEGER.
DEFINE VARIABLE prev-month      AS INTEGER. 
DEFINE VARIABLE from-month      AS INTEGER. 
DEFINE VARIABLE to-month        AS INTEGER. 
DEFINE VARIABLE pnl-acct        AS CHAR.
DEFINE VARIABLE balance         AS DECIMAL. 
DEFINE VARIABLE profit          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lost            AS DECIMAL INITIAL 0. 
DEFINE VARIABLE i               AS INTEGER. 

/********** Check IF the closing DATE is correct ********/ 
FIND FIRST htparam WHERE paramnr = 795 no-lock.   /* Last Year closing DATE */ 
ASSIGN
  curr-date  = htparam.fdate
  curr-year  = YEAR(curr-date)
  curr-month = 12 
  prev-month = 11
. 

FIND FIRST htparam WHERE paramnr = 597 no-lock. /* CURRENT CLOSE month */ 
from-month = 1. 
to-month = month(htparam.fdate) - 1. 
 
/******* Check IF PnL acct for LY adjustment exists *****/ 
FIND FIRST htparam WHERE paramnr = 980 NO-LOCK. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("P&L Last Year Adjustment Account not defined (Parameter 980).",lvCAREA,"").
  RETURN. 
END. 

IF gl-acct.acc-type NE 4 THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("P&L Last Year Adjustment Account has wrong type (Parameter 980).",lvCAREA,"").
   RETURN. 
END.

pnl-acct = gl-acct.fibukonto. 


FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
  AND gl-jouhdr.datum EQ curr-date NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE gl-jouhdr: 
  balance = 0. 
  
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
  FIND NEXT gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
    AND gl-jouhdr.datum EQ curr-date NO-LOCK NO-ERROR. 
END. 
 
/********** set closing PROCESS active ***/ 
FIND FIRST htparam WHERE paramnr = 983 EXCLUSIVE-LOCK. 
flogical = yes.   /* set running flag */ 
FIND CURRENT htparam NO-LOCK. 
 

FOR EACH gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
  AND gl-jouhdr.datum EQ curr-date NO-LOCK: 
  RUN process-journal(gl-jouhdr.jnr). 
END. 
 
RUN process-jouhdr. 
 
/* !!! */
/*** transfer the profit / lost TO the PnL Adjustment Account ***/ 
FIND FIRST htparam WHERE paramnr = 980 NO-LOCK. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar EXCLUSIVE-LOCK. 
ASSIGN
  gl-acct.last-yr[curr-month] = gl-acct.last-yr[curr-month] 
                              - profit + lost
. 
DO i = from-month TO to-month: 
  gl-acct.actual[i] = gl-acct.actual[i] - profit + lost. 
END. 
FIND CURRENT gl-acct NO-LOCK. 
 
FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = gl-acct.fibukonto
  AND gl-accthis.YEAR = curr-year EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE gl-accthis THEN
DO:
  CREATE gl-accthis.
  BUFFER-COPY gl-acct EXCEPT actual last-yr TO gl-accthis.
  ASSIGN gl-accthis.YEAR = curr-year.
END.
ASSIGN 
  gl-accthis.actual[curr-month] = gl-accthis.actual[curr-month]
                                - profit + lost
.
FIND CURRENT gl-accthis NO-LOCK.


/************ Finish ********/ 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
DO:
  CREATE res-history.
  ASSIGN 
    res-history.nr = bediener.nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME 
    res-history.aenderung = "Close Year Adjustment - " + STRING(curr-date)              
    res-history.action = "G/L". 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history. 
END.

closed = YES. 
FIND FIRST htparam WHERE paramnr = 983 EXCLUSIVE-LOCK. 
flogical = NO.   /* set running flag AS fault */ 
FIND CURRENT htparam NO-LOCK. 


/********************** PROCEDURE ****************/ 
 
PROCEDURE process-journal: 
DEFINE INPUT PARAMETER inp-jnr AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 

  FIND FIRST gl-journal WHERE gl-journal.jnr = inp-jnr 
    AND gl-journal.activeflag = 0 NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE gl-journal: 
    FIND CURRENT gl-journal EXCLUSIVE-LOCK. 
    
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = 
      gl-journal.fibukonto NO-LOCK. 

    FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = gl-journal.fibukonto 
      AND gl-accthis.YEAR = curr-year EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-accthis THEN
    DO:
        CREATE gl-accthis.
        BUFFER-COPY gl-acct TO gl-accthis.
        ASSIGN gl-accthis.YEAR = curr-year.
    END.
    DO:
      gl-accthis.actual[curr-month] = gl-accthis.actual[curr-month] 
        + gl-journal.debit - gl-journal.credit. 
      FIND CURRENT gl-accthis NO-LOCK.
    END.

    FIND CURRENT gl-acct EXCLUSIVE-LOCK.
    gl-acct.last-yr[curr-month] = gl-acct.last-yr[curr-month] 
      + gl-journal.debit - gl-journal.credit. 
    
    IF gl-acct.acc-type = 1 /* sales account */ 
      THEN profit = profit - gl-journal.debit + gl-journal.credit. 
    ELSE IF gl-acct.acc-type = 2 /* cost account */ 
      OR gl-acct.acc-type = 5 /* expense account */ 
    THEN lost = lost + gl-journal.debit - gl-journal.credit. 

    ELSE IF gl-acct.acc-type = 3 /* activa */ THEN 
    DO i = from-month TO to-month: 
      gl-acct.actual[i] = gl-acct.actual[i] 
                        + gl-journal.debit - gl-journal.credit. 
    END. 
    
    ELSE IF gl-acct.acc-type = 4 /* passiva */ THEN 
    DO i = from-month TO to-month: 
      gl-acct.actual[i] = gl-acct.actual[i] 
                        + gl-journal.debit - gl-journal.credit. 
    END. 
    
    FIND CURRENT gl-acct NO-LOCK. 

    gl-journal.activeflag = 1. 
    FIND CURRENT gl-journal NO-LOCK. 
    FIND NEXT gl-journal WHERE gl-journal.jnr = inp-jnr 
      AND gl-journal.activeflag = 0 NO-LOCK NO-ERROR. 
  END. 
END. 
 
PROCEDURE process-jouhdr: 
  FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
    AND gl-jouhdr.datum EQ curr-date NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE gl-jouhdr: 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    gl-jouhdr.activeflag = 1. 
    FIND CURRENT gl-jouhdr NO-LOCK. 
    FIND NEXT gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
      AND gl-jouhdr.datum EQ curr-date NO-LOCK NO-ERROR. 
  END. 
END. 
 

