
DEFINE VARIABLE profit          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE revLocal        AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE revfremd        AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE lost            AS DECIMAL INITIAL 0.
DEFINE VARIABLE prev-month      AS INTEGER. 
DEFINE VARIABLE curr-month      AS INTEGER. 

DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE beg-month       AS INTEGER. 
DEFINE VARIABLE end-month       AS INTEGER. 

FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
curr-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 993 no-lock. /* month OF closing year */ 
end-month = htparam.finteger. 
beg-month = htparam.finteger + 1. 
IF beg-month GT 12 THEN beg-month = 1.

DEFINE VARIABLE first-date      AS DATE. 
FIND FIRST htparam WHERE paramnr = 558 no-lock. /* LAST Accounting Period */ 
first-date = htparam.fdate + 1.        /* Rulita 211024 | Fixing for serverless */

DEFINE VARIABLE wahrNo          AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE foreign-rate    AS LOGICAL. 
DEFINE VARIABLE double-currency AS LOGICAL INITIAL NO. 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN double-currency = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical.
IF foreign-rate OR double-currency THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN wahrNo = waehrung.waehrungsnr. 
END.

RUN closing-month(OUTPUT curr-month).

prev-month = curr-month - 1. 
IF prev-month = 0 THEN prev-month = 12.

PROCEDURE closing-month: 
DEFINE OUTPUT PARAMETER acct-date AS INTEGER FORMAT "99". 
  FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
  acct-date = month(htparam.fdate). 
  IF day(htparam.fdate) LT 15 THEN acct-date = acct-date - 1. 
  IF acct-date = 0 THEN acct-date = 12. 
END. 



DO transaction: 
  FIND FIRST htparam WHERE paramnr = 983 NO-LOCK NO-ERROR.
  IF AVAILABLE htparam THEN DO:
      FIND CURRENT htparam EXCLUSIVE-LOCK.
      ASSIGN htparam.flogical = yes.   /* set running flag */ 
      FIND CURRENT htparam NO-LOCK.
      RELEASE htparam.
  END.
END.

RUN update-glacct.


FOR EACH gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
  AND gl-jouhdr.datum GE first-date 
  AND gl-jouhdr.datum LE curr-date NO-LOCK: 
  /*MTcurr-anz = curr-anz + 1. 
  curr-bezeich = "STEP II: " + gl-jouhdr.refno. 
  DISP curr-anz curr-bezeich WITH FRAME frame1. */
  RUN process-journal(gl-jouhdr.jnr, gl-jouhdr.datum). 
END.

RUN process-jouhdr.


/*** transfer the profit / lost TO the account ***/ 
FIND FIRST htparam WHERE paramnr = 979 NO-LOCK. 
DO TRANSACTION: 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar EXCLUSIVE-LOCK. 
/* 
  IF curr-month = beg-month THEN 
    gl-acct.actual[curr-month] = gl-acct.last-yr[end-month] - profit + lost. 
  ELSE gl-acct.actual[curr-month] = gl-acct.actual[prev-month] - profit + lost. 
*/ 
  gl-acct.actual[curr-month] = gl-acct.actual[curr-month] - profit + lost. 
  FIND CURRENT gl-acct NO-LOCK. 
END.

DO transaction: 
  FIND FIRST htparam WHERE paramnr = 983 NO-LOCK NO-ERROR.
  IF AVAILABLE htparam THEN DO:
      FIND CURRENT htparam EXCLUSIVE-LOCK.
      ASSIGN htparam.flogical = NO. 
      FIND CURRENT htparam NO-LOCK.
      RELEASE htparam.
  END.
 
  FIND FIRST htparam WHERE paramnr = 558 NO-LOCK NO-ERROR. /* LAST Acct Period */ 
  IF AVAILABLE htparam THEN DO:
      FIND CURRENT htparam EXCLUSIVE-LOCK.
      htparam.fdate    = curr-date. 
      htparam.lupdate  = TODAY.
      FIND CURRENT htparam NO-LOCK. 
      RELEASE htparam.
  END.
END.

RUN set-acct-modflag.

DO TRANSACTION:
    FIND FIRST exrate WHERE exrate.artnr = 99999
        AND exrate.datum = curr-date NO-LOCK NO-ERROR.
    IF NOT AVAILABLE exrate THEN
    DO:
        CREATE exrate.
        ASSIGN
            exrate.artnr = 99999
            exrate.datum = curr-date.
        IF revFremd NE 0 THEN ASSIGN exrate.betrag = ROUND(revLocal / revFremd, 2).
        ELSE exrate.betrag = 1.
    END.
    ELSE DO:
        FIND CURRENT exrate EXCLUSIVE-LOCK.
        IF revFremd NE 0 THEN ASSIGN exrate.betrag = ROUND(revLocal / revFremd, 2).
        ELSE exrate.betrag = 1.
        FIND CURRENT exrate NO-LOCK.
        RELEASE exrate.
    END.
END.

/*********************************************************************/
PROCEDURE update-glacct: 
DEFINE buffer gl-acc FOR gl-acct. 
  /*MTcurr-anz = 0. */
  FOR EACH gl-acc /* WHERE gl-acc.activeflag = YES */ NO-LOCK: 
    FIND FIRST gl-acct WHERE RECID(gl-acct) = RECID(gl-acc) EXCLUSIVE-LOCK. 
    gl-acct.actual[curr-month] = 0. 
    IF gl-acct.acc-type = 3 OR gl-acct.acc-type = 4 THEN 
    DO: 
      /*MTcurr-anz = curr-anz + 1. 
      curr-bezeich = gl-acct.bezeich. 
      DISP curr-bezeich curr-anz WITH FRAME frame1. */
      IF curr-month NE beg-month THEN 
        gl-acct.actual[curr-month] = gl-acct.actual[prev-month]. 
      ELSE gl-acct.actual[curr-month] = gl-acct.last-yr[end-month]. 

      IF gl-acct.fibukonto = "10001006" THEN
          DISP gl-acct.actual[curr-month] curr-month beg-month prev-month
               gl-acct.actual[prev-month] gl-acct.last-yr[end-month].
    END. 
  END. 
END. 


PROCEDURE process-journal: 
DEFINE INPUT PARAMETER jnr   AS INTEGER. 
DEFINE INPUT PARAMETER datum AS DATE.

DEFINE BUFFER bacct FOR gl-acct.
DEFINE BUFFER bjournal FOR gl-journal.

  FOR EACH gl-journal WHERE  gl-journal.jnr = jnr 
    AND gl-journal.activeflag = 0 NO-LOCK,
    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK
    BY gl-journal.fibukonto:
        
        IF gl-acct.fibukonto = "10001006" THEN DO:
            DISP gl-journal.jnr gl-acct.actual[curr-month] FORMAT "->>>,>>>,>>>,>>9.99"
                 gl-journal.debit gl-journal.credit
                (gl-acct.actual[curr-month] 
                + gl-journal.debit - gl-journal.credit) FORMAT "->>>,>>>,>>>,>>9.99".
        END.

        FIND FIRST bacct WHERE RECID(bacct) = RECID(gl-acct) EXCLUSIVE-LOCK.
        ASSIGN bacct.actual[curr-month] = bacct.actual[curr-month] 
                            + gl-journal.debit - gl-journal.credit. 
        FIND CURRENT bacct NO-LOCK.

        IF gl-acct.acc-type = 1 /* sales account */ THEN
        DO:
          profit = profit - gl-journal.debit + gl-journal.credit. 
          IF wahrNo NE 0 THEN 
          DO:    
            FIND FIRST exrate WHERE exrate.artnr = wahrNo
                AND exrate.datum = datum NO-LOCK NO-ERROR.
            IF AVAILABLE exrate AND exrate.betrag NE 0 THEN
            ASSIGN
              revLocal = revLocal + gl-journal.credit - gl-journal.debit
              revFremd = revFremd + (gl-journal.credit - gl-journal.debit) / exrate.betrag
            .
          END.
        END.    
        ELSE IF gl-acct.acc-type = 2 /* cost account */ 
          OR gl-acct.acc-type = 5 /* expense account */ 
        THEN lost = lost + gl-journal.debit - gl-journal.credit. 
        
        FIND FIRST bjournal WHERE RECID(bjournal) = RECID(gl-journal) EXCLUSIVE-LOCK.
        bjournal.activeflag = 1. 
        FIND CURRENT bjournal NO-LOCK.
        RELEASE bjournal.
        RELEASE bacct.
  END.
    
  /*
  FIND FIRST gl-journal WHERE  gl-journal.jnr = jnr 
    AND gl-journal.activeflag = 0 NO-LOCK NO-ERROR. 
  DO transaction WHILE AVAILABLE gl-journal: 
    FIND CURRENT gl-journal EXCLUSIVE-LOCK. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = 
      gl-journal.fibukonto EXCLUSIVE-LOCK. 

      IF gl-acct.fibukonto = "10001006" THEN DO:
        DISP gl-acct.actual[curr-month] FORMAT "->>>,>>>,>>>,>>9.99"
             gl-journal.debit gl-journal.credit
            (gl-acct.actual[curr-month] 
            + gl-journal.debit - gl-journal.credit) FORMAT "->>>,>>>,>>>,>>9.99".
      END.
   
      gl-acct.actual[curr-month] = gl-acct.actual[curr-month] 
          + gl-journal.debit - gl-journal.credit. 

    
    FIND CURRENT gl-acct NO-LOCK. 

    IF gl-acct.acc-type = 1 /* sales account */ THEN
    DO:
      profit = profit - gl-journal.debit + gl-journal.credit. 
      IF wahrNo NE 0 THEN 
      DO:    
        FIND FIRST exrate WHERE exrate.artnr = wahrNo
            AND exrate.datum = datum NO-LOCK NO-ERROR.
        IF AVAILABLE exrate AND exrate.betrag NE 0 THEN
        ASSIGN
          revLocal = revLocal + gl-journal.credit - gl-journal.debit
          revFremd = revFremd + (gl-journal.credit - gl-journal.debit) / exrate.betrag
        .
      END.
    END.
    
    ELSE IF gl-acct.acc-type = 2 /* cost account */ 
      OR gl-acct.acc-type = 5 /* expense account */ 
    THEN lost = lost + gl-journal.debit - gl-journal.credit. 
    gl-journal.activeflag = 1. 
    FIND CURRENT gl-journal NO-LOCK. 
    FIND NEXT gl-journal WHERE  gl-journal.jnr = jnr 
      AND gl-journal.activeflag = 0 NO-LOCK NO-ERROR. 
  END. */
END. 


PROCEDURE process-jouhdr: 
  FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
    AND gl-jouhdr.datum GE first-date 
    AND gl-jouhdr.datum LE curr-date NO-LOCK NO-ERROR. 
  DO transaction WHILE AVAILABLE gl-jouhdr: 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    gl-jouhdr.activeflag = 1. 
    FIND CURRENT gl-jouhdr NO-LOCK. 
    FIND NEXT gl-jouhdr WHERE gl-jouhdr.activeflag = 0 
      AND gl-jouhdr.datum GE first-date 
      AND gl-jouhdr.datum LE curr-date NO-LOCK NO-ERROR. 
  END. 
END. 

PROCEDURE set-acct-modflag: 
DEFINE buffer gl-acc FOR gl-acct. 
  FOR EACH gl-acc /* WHERE gl-acc.activeflag = YES */ NO-LOCK: 
    FIND FIRST gl-acct WHERE RECID(gl-acct) = RECID(gl-acc) EXCLUSIVE-LOCK. 
    gl-acct.modifiable = NO. 
    FIND CURRENT gl-acct NO-LOCK. 
  END. 
END. 
