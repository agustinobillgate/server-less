DEFINE TEMP-TABLE age-list 
  FIELD selected        AS LOGICAL INITIAL NO 
  FIELD ar-recid        AS INTEGER 
  FIELD rechnr          AS INTEGER FORMAT ">>>>>>>9" 
  FIELD refno           AS INTEGER FORMAT ">>>>>>>>>" 
  FIELD counter         AS INTEGER 
  FIELD gastnr          AS INTEGER 
  FIELD billname        AS CHAR FORMAT "x(36)" 
  FIELD gastnrmember    AS INTEGER 
  FIELD gastname        AS CHAR FORMAT "x(36)" 
  FIELD zinr            LIKE zimmer.zinr
  FIELD rgdatum         AS DATE 
  FIELD user-init       AS CHAR FORMAT "x(2)" 
  FIELD debt            AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD debt-foreign    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD currency        AS CHAR FORMAT "x(4)" 
  FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0
  FIELD vouc-nr         AS CHAR   FORMAT "x(24)"
  FIELD prevdate        AS DATE 
  FIELD remarks         AS CHAR   FORMAT "x(24)"
  FIELD b-resname       AS CHAR
  FIELD ci-date         AS DATE /*sis 300414 add ci-date*/
  FIELD co-date         AS DATE. /*sis 300414 add co-date*/ 


DEFINE TEMP-TABLE pay-list 
  FIELD artnr       AS INTEGER FORMAT ">>>9" 
  FIELD bezeich     AS CHAR FORMAT "x(22)" 
  FIELD proz        AS DECIMAL FORMAT "->>9.99" 
  FIELD betrag      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD f-amt       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD currency    AS INTEGER INITIAL 0 
  FIELD curr-str    AS CHAR FORMAT "x(4)"
  FIELD bemerk      AS CHAR FORMAT "x(32)" 
  FIELD remain-amt  AS DECIMAL
  FIELD fremain-amt AS DECIMAL
  FIELD balance     AS DECIMAL. /*gerald nyimpan nilai balance 07D19F*/

DEFINE INPUT PARAMETER TABLE FOR age-list.
DEFINE INPUT PARAMETER TABLE FOR pay-list.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER outstand1    AS DECIMAL.
DEFINE INPUT PARAMETER foutstand1   AS DECIMAL.
DEFINE INPUT PARAMETER outstand     AS DECIMAL.
DEFINE INPUT PARAMETER curr-art     AS INTEGER.
DEFINE INPUT PARAMETER rundung      AS INTEGER.
DEFINE INPUT PARAMETER foutstand    AS DECIMAL.
DEFINE INPUT PARAMETER pay-date     AS DATE.
DEFINE INPUT PARAMETER balance      AS DECIMAL.
DEFINE INPUT PARAMETER fbalance     AS DECIMAL.
DEFINE INPUT PARAMETER user-init    AS CHAR.

DEFINE OUTPUT PARAMETER f-flag      AS INTEGER INIT 0.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR INIT "".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ar-debtpay". 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
RUN check-paydate.
IF f-flag = 0 THEN RUN settle-payment.

PROCEDURE check-paydate:
DEF VAR bill-date AS DATE NO-UNDO.
DEF BUFFER debt FOR debitor.
  
  IF pay-date = ? THEN
  DO:
    f-flag = 1.
    RETURN. 
  END.

  RUN htpdate.p(110, OUTPUT bill-date).
  IF pay-date GT bill-date THEN 
  DO: 
    msg-str = translateExtended ("Wrong posting date.",lvCAREA,""). 
    f-flag = 1.
    RETURN. 
  END. 

  FIND FIRST htparam WHERE paramnr = 1014 NO-LOCK. 
  IF htparam.fdate NE ? AND pay-date LE htparam.fdate THEN 
  DO: 
    msg-str = translateExtended ("Wrong posting date: Older than last Transfer Date to G/L",lvCAREA,""). 
    f-flag = 1.
    RETURN. 
  END. 
 
  FOR EACH age-list WHERE age-list.selected = YES 
    AND age-list.tot-debt NE 0 NO-LOCK: 
    FIND FIRST debt WHERE RECID(debt) = age-list.ar-recid NO-LOCK. 
    IF debt.rgdatum GT pay-date THEN 
    DO: 
      msg-str = translateExtended ("Wrong payment date as earlier than A/R billing date.",lvCAREA,""). 
      f-flag = 1.
      RETURN. 
    END. 
  END. 
END.

PROCEDURE settle-payment:
  DEFINE VARIABLE saldo-i       AS DECIMAL. 
  DEFINE VARIABLE fsaldo-i      AS DECIMAL.
  DEFINE VARIABLE pay-amount    AS DECIMAL. 
  DEFINE VARIABLE fpay-amount   AS DECIMAL.
  
/* 10/05/00 created TO avoid rounding ERROR */ 
  DEFINE VARIABLE payment1      AS DECIMAL. 
  DEFINE VARIABLE fpayment1     AS DECIMAL. 
 
  DEF VAR pay-count             AS INTEGER INITIAL 0 NO-UNDO. 
  DEF VAR remain-balance        AS DECIMAL NO-UNDO. 
 
  DEFINE VARIABLE bill-date     AS DATE. 
  DEFINE VARIABLE count         AS INTEGER. 
  DEFINE VARIABLE anzahl        AS INTEGER INITIAL 0. 
  DEFINE VARIABLE billname      AS CHAR. 
  DEFINE VARIABLE ok            AS LOGICAL. 

  DEFINE BUFFER debit FOR debitor. 

  ok = NO. 
  IF outstand = 0 THEN ok = YES. 
  ELSE 
  DO: 
    FOR EACH age-list WHERE age-list.selected = YES 
        AND age-list.tot-debt NE 0 NO-LOCK: 
      anzahl = anzahl + 1. 
    END. 
    IF anzahl = 0 THEN RETURN. 
    IF anzahl = 1 THEN ok = YES. 
    ELSE 
    DO: 
        OK = YES. 
        RUN settle-pay1. 
        RETURN. 
    END. 
  END. 
 
  IF ok THEN 
  DO: 
    IF anzahl NE 1 THEN 
    FOR EACH age-list WHERE age-list.selected = YES 
      AND age-list.tot-debt NE 0 NO-LOCK: 
      anzahl = anzahl + 1. 
    END. 
    FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
    bill-date = htparam.fdate. 
 
    FOR EACH age-list WHERE age-list.selected = YES 
      AND age-list.tot-debt NE 0 NO-LOCK BY age-list.rechnr: 
 
      FIND FIRST debitor WHERE RECID(debitor) = age-list.ar-recid NO-ERROR. 
      IF AVAILABLE debitor THEN billname = debitor.name. 
      ASSIGN
          saldo-i = age-list.tot-debt
          fsaldo-i = age-list.debt-foreign
          payment1 = - saldo-i
          fpayment1 = - fsaldo-i.

      IF outstand GE - 0.01 AND outstand LE 0.01 THEN 
      DO: 
        debitor.opart = 2. 
        /*MTRUN cal-commision.p(RECID(debitor), pay-date). */
      END. 
      count = debitor.counter. 
      IF count = 0 THEN      /* NO pre-payment */ 
      DO: 
        FIND FIRST counters WHERE counters.counter-no = 5 EXCLUSIVE-LOCK 
            NO-ERROR. 
        IF NOT AVAILABLE counters THEN 
        DO: 
            CREATE counters. 
            ASSIGN 
              counters.counter-no = 5 
              counters.counter-bez = "Counter for A/R Payment". 
        END. 
 
        counters.counter = counters.counter + 1. 
        debitor.counter = counters.counter. 
        count = debitor.counter. 
        FIND CURRENT counters NO-LOCK. 
        RELEASE counters. 
      END. 
      ELSE IF count NE 0 AND (outstand GE - 0.01 AND outstand LE 0.01) THEN 
      DO: 
        FOR EACH debit WHERE debit.opart GE 1 
          AND debit.counter = count 
          AND debit.rechnr = age-list.rechnr 
          AND debit.artnr = curr-art 
          /* AND debit.gastnr = age-list.gastnr */ 
          AND debit.zahlkonto GT 0 EXCLUSIVE-LOCK: 
          debit.opart = 2. 
          payment1 = payment1 - debit.saldo. 
          fpayment1 = fpayment1 - debit.vesrdep.
          release debit. 
        END. 
      END. 
 
      IF (pay-count = 0) AND anzahl GT 1 THEN 
      DO: 
        FIND FIRST counters WHERE counters.counter-no = 31 EXCLUSIVE-LOCK 
          NO-ERROR. 
        IF NOT AVAILABLE counters THEN 
        DO: 
          CREATE counters. 
          ASSIGN 
            counters.counter-no = 31 
            counters.counter-bez = "Counter for Total A/R Payment". 
        END. 
        counters.counter = counters.counter + 1. 
        pay-count = counters.counter. 
        FIND CURRENT counters NO-LOCK. 
        RELEASE counters. 
      END. 

      FOR EACH pay-list: 
 
        IF pay-list.proz = 100 THEN 
        DO: 
          ASSIGN
              pay-amount = - saldo-i
              fpay-amount = - fsaldo-i. 
          IF pay-amount = 0 THEN 
              ASSIGN pay-amount = payment1
              fpay-amount = fpayment1. 
        END. 
        ELSE 
        DO: 
          ASSIGN
              pay-amount = saldo-i / outstand1 * pay-list.betrag
              fpay-amount = fsaldo-i / foutstand1 * pay-list.f-amt.
              
          IF outstand = 0 THEN 
          DO: 
            IF ROUND(payment1 - pay-amount, rundung) = 0 THEN 
                pay-amount = payment1. 
          END. 
          ELSE 
          DO: 
            IF (pay-amount - pay-list.remain-amt) LE 0.05 OR 
               (pay-list.remain-amt - pay-amount) LE 0.05 THEN 
              pay-amount = pay-list.remain-amt. 
          END. 

          IF foutstand = 0 THEN
          DO:
              IF ROUND(fpayment1 - fpay-amount, rundung) = 0 THEN
                  fpay-amount = fpayment1.
          END.
          ELSE
          DO:
              IF (fpay-amount - pay-list.fremain-amt) LE 0.05 OR
                  (pay-list.fremain-amt - fpay-amount) LE 0.05 THEN
                  fpay-amount = pay-list.fremain-amt.
          END.
        END. 

        CREATE debit. 
        ASSIGN 
          debit.artnr           = curr-art 
          debit.zinr            = age-list.zinr 
          debit.gastnr          = age-list.gastnr 
          debit.gastnrmember    = age-list.gastnrmember 
          debit.rechnr          = age-list.rechnr 
          debit.saldo           = pay-amount 
/*        debit.vesrdep = age-list.debt-foreign * pay-amount / saldo-i  */ 
          debit.zahlkonto       = pay-list.artnr 
          debit.betrieb-gastmem = pay-list.currency
          debit.counter         = count 
          debit.transzeit       = TIME 
          debit.rgdatum         = pay-date 
          debit.bediener-nr     = bediener.nr 
          debit.name            = billname 
          debit.vesrcod         = pay-list.bemerk 
          debit.betrieb-gastmem = pay-list.currency 
          /*debit.vesrdep         = fpay-amount*/
          debit.betriebsnr      = pay-count
        . 
        
        IF fpay-amount NE ? THEN
            debit.vesrdep = fpay-amount.
        ASSIGN
            pay-list.remain-amt = pay-list.remain-amt - pay-amount
            pay-list.fremain-amt = pay-list.fremain-amt - fpay-amount.

        IF outstand NE 0 THEN debit.opart = 1. 
        ELSE debit.opart = 2. 
        /* %%%%% */
        debit.vesrdep = age-list.debt-foreign * pay-amount / age-list.debt.     

    
/** %%% MAY NOT BE CREATED 
/* August 08, 2000: change bill-date TO pay-date */ 
        FIND FIRST umsatz WHERE umsatz.departement = 0 AND 
          umsatz.artnr = pay-list.artnr AND umsatz.datum 
          = /*bill-date*/ pay-date EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE umsatz THEN create umsatz. 
        umsatz.datum = /*bill-date*/ pay-date. 
        umsatz.artnr = pay-list.artnr. 
        umsatz.anzahl = umsatz.anzahl + 1. 
        umsatz.betrag = umsatz.betrag + debit.saldo. 
        release umsatz. 
** %% **/ 
        
        FIND FIRST artikel WHERE artikel.departement = 0 AND 
          artikel.artnr = pay-list.artnr NO-LOCK. 
 
        IF artikel.artart = 2 OR artikel.artart = 7 THEN 
        RUN inv-ar(pay-list.artnr, age-list.zinr, age-list.gastnr, 
          age-list.gastnrmember, age-list.rechnr, pay-amount, fpay-amount, 
          pay-date, billname, user-init, pay-list.bemerk). 
 
        create billjournal. 
        billjournal.rechnr = debit.rechnr. 
        billjournal.bill-datum = pay-date. 
        billjournal.artnr = pay-list.artnr. 
        billjournal.anzahl = 1. 
        billjournal.betrag = debit.saldo. 
        billjournal.bezeich = artikel.bezeich. 
        billjournal.zinr = debit.zinr. 
        billjournal.zeit = time. 
        billjournal.bediener-nr = bediener.nr. 
        billjournal.userinit = bediener.userinit. 
        IF pay-date NE bill-date THEN billjournal.bezeich = 
          billjournal.bezeich + " - " + STRING(pay-date). 
     END. 
    END. /*each age-list*/
    /*
    FOR EACH pay-list: 
      DELETE pay-list. 
    END.*/
    /*gerald selalu selisih 0.01 or -0.01 Amadea*/
    IF outstand = 0 THEN
    DO:
       RUN check-rounding.
    END.
  END. 
  ELSE 
  DO: 
    msg-str = translateExtended ("Partial Payment for multi-selected A/R records not possible",lvCAREA,""). 
    f-flag = 2.
  END. 
END. 




PROCEDURE settle-pay1: 
  DEFINE VARIABLE remain-payment AS DECIMAL NO-UNDO. 
  DEFINE VARIABLE fremain-payment AS DECIMAL NO-UNDO. 
  DEF VAR pay-count AS INTEGER INITIAL 0 NO-UNDO. 
 
  remain-payment = - balance. 
  fremain-payment = - fbalance.
  
  FOR EACH age-list WHERE age-list.selected = YES 
    AND age-list.tot-debt NE 0 NO-LOCK BY age-list.tot-debt 
    BY age-list.rechnr: 
    
    IF age-list.tot-debt LT remain-payment THEN 
    DO: 
       RUN full-payment (age-list.ar-recid, INPUT-OUTPUT pay-count). 
       ASSIGN
           remain-payment = remain-payment - age-list.tot-debt
           fremain-payment = fremain-payment - age-list.debt-foreign.        
    END. 
    ELSE 
    DO: 
        IF remain-payment NE 0 THEN 
            RUN partial-payment (age-list.ar-recid, - remain-payment, 
                                 - fremain-payment, INPUT-OUTPUT pay-count). 
        RETURN. 
    END. 
  END.  
END. 


PROCEDURE partial-payment: 
  DEFINE INPUT PARAMETER ar-recid AS INTEGER NO-UNDO. 
  DEFINE INPUT PARAMETER payment1 AS DECIMAL NO-UNDO. 
  DEFINE INPUT PARAMETER fpayment1 AS DECIMAL NO-UNDO. 
  DEF INPUT-OUTPUT PARAMETER pay-count AS INTEGER. 
  DEFINE VARIABLE saldo-i AS DECIMAL. 
  DEFINE VARIABLE pay-amount AS DECIMAL. 
  DEFINE VARIABLE fsaldo-i AS DECIMAL. 
  DEFINE VARIABLE fpay-amount AS DECIMAL. 
 
  DEFINE VARIABLE bill-date AS DATE. 
  DEFINE VARIABLE count AS INTEGER. 
  DEFINE VARIABLE anzahl AS INTEGER. 
  DEFINE VARIABLE billname AS CHAR. 
  DEFINE BUFFER debit FOR debitor. 
 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  bill-date = htparam.fdate. 
 
  FIND FIRST debitor WHERE RECID(debitor) = ar-recid NO-ERROR. 
  IF AVAILABLE debitor THEN billname = debitor.name. 
  ASSIGN
      saldo-i = age-list.tot-debt
      fsaldo-i = age-list.debt-foreign. 
 
  count = debitor.counter. 
  IF count = 0 THEN      /* NO pre-payment */ 
  DO: 
      FIND FIRST counters WHERE counters.counter-no = 5 EXCLUSIVE-LOCK 
          NO-ERROR. 
      IF NOT AVAILABLE counters THEN 
      DO: 
          CREATE counters. 
          ASSIGN 
              counters.counter-no = 5 
              counters.counter-bez = "Counter for A/R Payment". 
      END. 
      counters.counter = counters.counter + 1. 
      debitor.counter = counter.counter. 
      count = debitor.counter. 
      FIND CURRENT counters NO-LOCK. 
      release counters. 
  END. 
 
  IF pay-count = 0 THEN 
  DO: 
    FIND FIRST counters WHERE counters.counter-no = 31 EXCLUSIVE-LOCK 
      NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      ASSIGN 
        counters.counter-no = 31 
        counters.counter-bez = "Counter for Total A/R Payment". 
    END. 
    counters.counter = counters.counter + 1. 
    pay-count = counters.counter. 
    FIND CURRENT counters NO-LOCK. 
    RELEASE counters. 
  END. 
 
  FOR EACH pay-list: 
 
    IF pay-list.proz = 100 OR balance EQ pay-list.betrag /* Dzikri 688951 - same decimal value output 0.00xxx even though it has save value */ THEN ASSIGN
        pay-amount = payment1
        fpay-amount = fpayment1. 
    ELSE ASSIGN
        pay-amount = payment1 / balance * pay-list.betrag
        fpay-amount = fpayment1 / fbalance * pay-list.f-amt. 
 
    IF (pay-amount - pay-list.remain-amt) LE 0.05 OR 
       (pay-list.remain-amt - pay-amount) LE 0.05 THEN 
      pay-amount = pay-list.remain-amt. 

    IF (fpay-amount - pay-list.fremain-amt) LE 0.05 OR
        (pay-list.fremain-amt - fpay-amount) LE 0.05 THEN
        fpay-amount = pay-list.fremain-amt.
        
         
    CREATE debit. 
    ASSIGN 
          debit.artnr           = curr-art 
          debit.zinr            = age-list.zinr 
          debit.gastnr          = age-list.gastnr 
          debit.gastnrmember    = age-list.gastnrmember 
          debit.rechnr          = age-list.rechnr 
          debit.saldo           = pay-amount 
          debit.zahlkonto       = pay-list.artnr 
          debit.betrieb-gastmem = pay-list.currency
          debit.counter         = count 
          debit.transzeit       = TIME 
          debit.rgdatum         = pay-date 
          debit.bediener-nr     = bediener.nr 
          debit.name            = billname 
          debit.vesrcod         = pay-list.bemerk 
          debit.betrieb-gastmem = pay-list.currency 
          /*debit.vesrdep         = fpay-amount*/
          debit.opart           = 1 
          debit.betriebsnr      = pay-count
    . 
    IF fpay-amount = ? THEN
        fpay-amount = 0.
    IF fpay-amount NE ? THEN
        debit.vesrdep = fpay-amount.
    pay-list.remain-amt = pay-list.remain-amt - pay-amount. 
    pay-list.fremain-amt = pay-list.fremain-amt - fpay-amount.
 
    FIND FIRST artikel WHERE artikel.departement = 0 AND 
        artikel.artnr = pay-list.artnr NO-LOCK. 
 
    IF artikel.artart = 2 OR artikel.artart = 7 THEN 
    RUN inv-ar(pay-list.artnr, age-list.zinr, age-list.gastnr, 
      age-list.gastnrmember, age-list.rechnr, pay-amount, fpay-amount, 
      pay-date, billname, user-init, pay-list.bemerk). 
 
    create billjournal. 
        billjournal.rechnr = debit.rechnr. 
        billjournal.bill-datum = pay-date. 
        billjournal.artnr = pay-list.artnr. 
        billjournal.anzahl = 1. 
        billjournal.betrag = debit.saldo. 
        billjournal.bezeich = artikel.bezeich. 
        billjournal.zinr = debit.zinr. 
        billjournal.zeit = time. 
        billjournal.bediener-nr = bediener.nr. 
        billjournal.userinit = bediener.userinit. 
        IF pay-date NE bill-date THEN billjournal.bezeich = 
          billjournal.bezeich + " - " + STRING(pay-date). 
  END. 
END.


PROCEDURE full-payment: 
  DEFINE INPUT PARAMETER ar-recid AS INTEGER NO-UNDO. 
  DEF INPUT-OUTPUT PARAMETER pay-count AS INTEGER. 
  DEFINE VARIABLE saldo-i AS DECIMAL. 
  DEFINE VARIABLE fsaldo-i AS DECIMAL.
  DEFINE VARIABLE pay-amount AS DECIMAL. 
  DEFINE VARIABLE fpay-amount AS DECIMAL.
 
/* 10/05/00 created TO avoid rounding ERROR */ 
  DEFINE VARIABLE payment1 AS DECIMAL. 
  DEFINE VARIABLE fpayment1 AS DECIMAL. 
 
  DEFINE VARIABLE bill-date AS DATE. 
  DEFINE VARIABLE count AS INTEGER. 
  DEFINE VARIABLE anzahl AS INTEGER. 
  DEFINE VARIABLE billname AS CHAR. 
  DEFINE BUFFER debit FOR debitor. 
 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  bill-date = htparam.fdate. 
 
  FIND FIRST debitor WHERE RECID(debitor) = ar-recid NO-ERROR. 
  IF AVAILABLE debitor THEN billname = debitor.name. 
  ASSIGN
      saldo-i = age-list.tot-debt
      fsaldo-i = age-list.debt-foreign
      payment1 = - saldo-i
      fpayment1 = - fsaldo-i
      debitor.opart = 2. 
 
  count = debitor.counter. 
  IF count = 0 THEN      /* NO pre-payment */ 
  DO: 
      FIND FIRST counters WHERE counters.counter-no = 5 EXCLUSIVE-LOCK 
          NO-ERROR. 
      IF NOT AVAILABLE counters THEN 
      DO: 
          CREATE counters. 
          ASSIGN 
              counters.counter-no = 5 
              counters.counter-bez = "Counter for A/R Payment". 
      END. 
      counters.counter = counters.counter + 1. 
      debitor.counter = counters.counter. 
      count = debitor.counter. 
      FIND CURRENT counters NO-LOCK. 
      release counters. 
  END. 
  ELSE IF count NE 0 THEN 
  DO: 
      FOR EACH debit WHERE debit.opart GE 1 
          AND debit.counter = count 
          AND debit.rechnr = age-list.rechnr 
          AND debit.artnr = curr-art 
          /* AND debit.gastnr = age-list.gastnr */ 
          AND debit.zahlkonto GT 0 EXCLUSIVE-LOCK: 
          debit.opart = 2. 
          payment1 = payment1 - debit.saldo. 
          fpayment1 = fpayment1 - debit.vesrdep.
          release debit. 
      END. 
  END. 
 
  IF pay-count = 0 THEN 
  DO: 
    FIND FIRST counter WHERE counters.counter-no = 31 EXCLUSIVE-LOCK 
      NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      ASSIGN 
        counters.counter-no = 31 
        counters.counter-bez = "Counter for Total A/R Payment". 
    END. 
    counters.counter = counters.counter + 1. 
    pay-count = counters.counter. 
    FIND CURRENT counters NO-LOCK. 
    RELEASE counters. 
  END. 
 
  FOR EACH pay-list: 
 
    IF pay-list.proz = 100 OR balance EQ pay-list.betrag /* Dzikri 688951 - same decimal value output 0.00xxx even though it has save value */ THEN ASSIGN 
        pay-amount = - saldo-i
        fpay-amount = - fsaldo-i. 
    ELSE ASSIGN
        pay-amount = - saldo-i / balance * pay-list.betrag
        fpay-amount = - fsaldo-i / fbalance * pay-list.f-amt. 
    
    CREATE debit. 
    ASSIGN 
          debit.artnr           = curr-art 
          debit.zinr            = age-list.zinr 
          debit.gastnr          = age-list.gastnr 
          debit.gastnrmember    = age-list.gastnrmember 
          debit.rechnr          = age-list.rechnr 
          debit.saldo           = pay-amount 
          debit.zahlkonto       = pay-list.artnr 
          debit.betrieb-gastmem = pay-list.currency
          debit.counter         = count 
          debit.transzeit       = TIME 
          debit.rgdatum         = pay-date 
          debit.bediener-nr     = bediener.nr 
          debit.name            = billname 
          debit.vesrcod         = pay-list.bemerk 
          debit.betrieb-gastmem = pay-list.currency 
          /*debit.vesrdep         = fpay-amount */
          debit.opart           = 2 
          debit.betriebsnr      = pay-count
    . 
    IF fpay-amount = ? THEN
        fpay-amount = 0.
    IF fpay-amount NE ? THEN
        debit.vesrdep = fpay-amount.
    pay-list.remain-amt = pay-list.remain-amt - pay-amount.
    pay-list.fremain-amt = pay-list.fremain-amt - fpay-amount.
 
    FIND FIRST artikel WHERE artikel.departement = 0 AND 
        artikel.artnr = pay-list.artnr NO-LOCK. 
 
    IF artikel.artart = 2 OR artikel.artart = 7 THEN 
    RUN inv-ar(pay-list.artnr, age-list.zinr, age-list.gastnr, 
        age-list.gastnrmember, age-list.rechnr, pay-amount, fpay-amount, 
        pay-date, billname, user-init, pay-list.bemerk). 
 
    create billjournal. 
        billjournal.rechnr = debit.rechnr. 
        billjournal.bill-datum = pay-date. 
        billjournal.artnr = pay-list.artnr. 
        billjournal.anzahl = 1. 
        billjournal.betrag = debit.saldo. 
        billjournal.bezeich = artikel.bezeich. 
        billjournal.zinr = debit.zinr. 
        billjournal.zeit = time. 
        billjournal.bediener-nr = bediener.nr. 
        billjournal.userinit = bediener.userinit. 
        IF pay-date NE bill-date THEN billjournal.bezeich = 
          billjournal.bezeich + " - " + STRING(pay-date). 
  END. 
END. 

/*gerald selalu selisih 0.01 or -0.01 Amadea*/
PROCEDURE check-rounding:
   DEFINE VAR balance  AS DECIMAL.
   DEFINE VAR balance1 AS DECIMAL.
   DEFINE VAR balance2 AS DECIMAL.
   DEFINE BUFFER debt FOR debitor.

   FOR EACH age-list:
      balance  = 0.
      balance1 = 0.
      balance2 = 0.

      FOR EACH debitor WHERE debitor.zahlkonto GT 0
          AND debitor.rechnr = age-list.rechnr
          AND debitor.gastnr = age-list.gastnr
          AND debitor.gastnrmember = age-list.gastnrmember NO-LOCK:
          ASSIGN balance = balance + debitor.saldo.
      END.

      FIND FIRST debitor WHERE debitor.zahlkonto = 0
          AND debitor.rechnr = age-list.rechnr
          AND debitor.gastnr = age-list.gastnr
          AND debitor.gastnrmember = age-list.gastnrmember NO-LOCK NO-ERROR.
      IF AVAILABLE debitor THEN
      DO:
         ASSIGN balance1 = debitor.saldo.
      END.

      balance2 = balance1 + balance.

      IF balance2 EQ 0.01 THEN
      DO:
         FIND FIRST debt WHERE debt.zahlkonto GT 0
          AND debt.rechnr = age-list.rechnr
          AND debt.gastnr = age-list.gastnr
          AND debt.gastnrmember = age-list.gastnrmember NO-ERROR.
         IF AVAILABLE debt THEN
         DO:
             /*ASSIGN debt.saldo = debt.saldo - balance2.*/   
             ASSIGN debt.saldo = debt.saldo + balance2.     /*MG 475589*/
         END.
      END.
      ELSE IF balance2 EQ -0.01 THEN
      DO:
        FIND FIRST debt WHERE debt.zahlkonto GT 0
          AND debt.rechnr = age-list.rechnr
          AND debt.gastnr = age-list.gastnr
          AND debt.gastnrmember = age-list.gastnrmember NO-ERROR.
         IF AVAILABLE debt THEN
         DO:
             /*ASSIGN debt.saldo = debt.saldo + balance2.*/
             ASSIGN debt.saldo = debt.saldo - balance2. /*MG 475589*/
         END.
      END.
   END.
END.
{ inv-ar.i }



