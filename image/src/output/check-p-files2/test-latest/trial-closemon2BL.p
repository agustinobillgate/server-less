
DEFINE VARIABLE lost            AS DECIMAL INITIAL 0.
DEFINE VARIABLE profit          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE revLocal        AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE revfremd        AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE beg-month       AS INTEGER. 
DEFINE VARIABLE end-month       AS INTEGER. 
DEFINE VARIABLE foreign-rate    AS LOGICAL. 
DEFINE VARIABLE curr-month      AS INTEGER. 
DEFINE VARIABLE prev-month      AS INTEGER. 
DEFINE VARIABLE first-date      AS DATE. 
DEFINE VARIABLE double-currency AS LOGICAL INITIAL NO. 
DEFINE VARIABLE wahrNo          AS INTEGER INITIAL 0 NO-UNDO.

FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
curr-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 993 no-lock. /* month OF closing year */ 
end-month = htparam.finteger. 
beg-month = htparam.finteger + 1. 
IF beg-month GT 12 THEN beg-month = 1.

FIND FIRST htparam WHERE paramnr = 558 no-lock. /* LAST Accounting Period */ 
first-date = htparam.fdate + 1.        /* Rulita 211024 | Fixing for serverless */

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


DO transaction: 
    FIND FIRST htparam WHERE paramnr = 983 EXCLUSIVE-LOCK. 
    flogical = yes.   /* set running flag */ 
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


DO TRANSACTION:
    FIND FIRST exrate WHERE exrate.artnr = 99999
        AND exrate.datum = curr-date EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE exrate THEN
    DO:
        CREATE exrate.
        ASSIGN
            exrate.artnr = 99999
            exrate.datum = curr-date.
    END.
    IF revFremd NE 0 THEN ASSIGN exrate.betrag = ROUND(revLocal / revFremd, 2).
    ELSE exrate.betrag = 1.
    FIND CURRENT exrate NO-LOCK.


    /*** transfer the profit / lost TO the account ***/ 
    FIND FIRST htparam WHERE paramnr = 979 NO-LOCK. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar EXCLUSIVE-LOCK. 
    gl-acct.actual[curr-month] = gl-acct.actual[curr-month] - profit + lost. 
    FIND CURRENT gl-acct NO-LOCK.

    FIND FIRST htparam WHERE paramnr = 983 EXCLUSIVE-LOCK. 
    flogical = NO. 
    FIND CURRENT htparam NO-LOCK. 
END.


PROCEDURE update-glacct: 
  /*MTcurr-anz = 0. */
  FOR EACH gl-acct /* WHERE gl-acct.activeflag = YES */ EXCLUSIVE-LOCK: 
    gl-acct.actual[curr-month] = 0. 
    IF gl-acct.acc-type = 3 OR gl-acct.acc-type = 4 THEN 
    DO: 
      /*MTcurr-anz = curr-anz + 1. 
      curr-bezeich = gl-acct.bezeich. 
      DISP curr-bezeich curr-anz WITH FRAME frame1. */
      IF curr-month NE beg-month THEN 
        gl-acct.actual[curr-month] = gl-acct.actual[prev-month]. 
      ELSE gl-acct.actual[curr-month] = gl-acct.last-yr[end-month]. 
    END. 
  END. 
END. 



PROCEDURE process-journal: 
DEFINE INPUT PARAMETER jnr   AS INTEGER. 
DEFINE INPUT PARAMETER datum AS DATE.

  FIND FIRST gl-journal WHERE  gl-journal.jnr = jnr 
      AND gl-journal.activeflag = 0 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE gl-journal: 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = 
        gl-journal.fibukonto NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO TRANSACTION:
        FIND CURRENT gl-acct EXCLUSIVE-LOCK.
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
    END.
    FIND NEXT gl-journal WHERE  gl-journal.jnr = jnr 
        AND gl-journal.activeflag = 0 NO-LOCK NO-ERROR. 
  END. 
END. 

PROCEDURE closing-month: 
DEFINE OUTPUT PARAMETER acct-date AS INTEGER FORMAT "99". 
  FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
  acct-date = month(htparam.fdate). 
  IF day(htparam.fdate) LT 15 THEN acct-date = acct-date - 1. 
  IF acct-date = 0 THEN acct-date = 12. 
END. 
