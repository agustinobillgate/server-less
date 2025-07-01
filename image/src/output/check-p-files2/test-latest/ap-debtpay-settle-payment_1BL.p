DEFINE TEMP-TABLE pay-list 
  FIELD dummy AS CHAR FORMAT "x(30)" 
  FIELD artnr    AS INTEGER FORMAT ">>>9" 
  FIELD bezeich  AS CHAR FORMAT "x(32)" 
  FIELD proz     AS DECIMAL FORMAT "->>9.99" 
  FIELD betrag   AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
  .

DEFINE TEMP-TABLE age-list 
  FIELD selected        AS LOGICAL INITIAL NO 
  FIELD ap-recid        AS INTEGER 
  FIELD counter         AS INTEGER 
  FIELD docu-nr         AS CHAR FORMAT "x(10)" 
  FIELD rechnr          AS INTEGER 
  FIELD lief-nr         AS INTEGER 
  FIELD lscheinnr       AS CHAR FORMAT "x(23)" 
  FIELD supplier        AS CHAR FORMAT "x(24)" 
  FIELD rgdatum         AS DATE 
  FIELD rabatt          AS DECIMAL FORMAT ">9.99" 
  FIELD rabattbetrag    AS DECIMAL FORMAT "->,>>>,>>9.99" 
  FIELD ziel            AS DATE 
  FIELD netto           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD user-init       AS CHAR FORMAT "x(2)" 
  FIELD debt            AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD credit          AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD bemerk          AS CHAR 
  FIELD tot-debt        AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
  FIELD rec-id          AS INT
  FIELD resname         AS CHAR
  FIELD comments        AS CHAR
  /*gerald 210920 Tauzia LnL*/   
  FIELD fibukonto       LIKE gl-journal.fibukonto     
  FIELD t-bezeich       LIKE gl-acct.bezeich          
  FIELD debt2            AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0  
  FIELD recv-date       AS DATE
  /*Rulita*/
  FIELD DESCRIPTION   AS CHAR
  .

DEFINE TEMP-TABLE t-l-lieferant 
    FIELD telefon   LIKE l-lieferant.telefon
    FIELD fax       LIKE l-lieferant.fax
    FIELD adresse1  LIKE l-lieferant.adresse1
    FIELD notizen-1 AS CHAR
    FIELD lief-nr   LIKE l-lieferant.lief-nr.

DEF INPUT-OUTPUT PARAMETER TABLE FOR pay-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR age-list.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER outstand  AS DECIMAL.
DEF INPUT PARAMETER outstand1 AS DECIMAL.
DEF INPUT PARAMETER rundung   AS INTEGER.
DEF INPUT PARAMETER pay-date  AS DATE.
DEF INPUT PARAMETER remark    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-l-lieferant.

RUN settle-payment.

FOR EACH age-list NO-LOCK:
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = age-list.lief-nr 
        NO-LOCK NO-ERROR.
    IF AVAILABLE l-lieferant THEN
    DO: 
        FIND FIRST t-l-lieferant WHERE t-l-lieferant.lief-nr = l-lieferant.lief-nr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-l-lieferant THEN
        DO:
            CREATE t-l-lieferant.
            ASSIGN
                t-l-lieferant.telefon   = l-lieferant.telefon
                t-l-lieferant.fax       = l-lieferant.fax
                t-l-lieferant.adresse1  = l-lieferant.adresse1
                t-l-lieferant.notizen-1 = l-lieferant.notizen[1]
                t-l-lieferant.lief-nr   = l-lieferant.lief-nr.
        END.
    END.
END.

PROCEDURE settle-payment: 
  DEFINE VARIABLE saldo-i   AS DECIMAL. 
  DEFINE VARIABLE bill-date AS DATE. 
  DEFINE VARIABLE count     AS INTEGER. 
  DEFINE VARIABLE anzahl    AS INTEGER. 
  DEFINE VARIABLE supplier  AS CHAR. 
  DEFINE VARIABLE pay-amount AS DECIMAL. 
 
/* 10/05/00 created TO avoid rounding ERROR */ 
  DEFINE VARIABLE payment1 AS DECIMAL. 
 
  DEFINE buffer l-kredit1 FOR l-kredit. 
 
/*  FIND FIRST htparam WHERE paramnr = 349 no-lock. */ 
    FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
    bill-date = htparam.fdate. 
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
 
    FOR EACH age-list WHERE age-list.selected = YES 
        /* AND age-list.tot-debt NE 0 */ NO-LOCK: 
      FIND FIRST l-kredit1 WHERE l-kredit1.opart = 0     /* l-kredit record */ 
        AND l-kredit1.lief-nr = age-list.lief-nr 
        AND l-kredit1.name = age-list.docu-nr 
        AND l-kredit1.lscheinnr = age-list.lscheinnr 
        AND l-kredit1.rgdatum = age-list.rgdatum 
        AND l-kredit1.saldo = age-list.debt. 
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit1.lief-nr 
        NO-LOCK. 
      supplier = l-lieferant.firma. 
      saldo-i = age-list.tot-debt. 
      payment1 = - saldo-i. 
 
      IF outstand EQ 0 THEN 
      DO: 
        l-kredit1.opart = 2. 
        RUN del-po(RECID(l-kredit1), l-kredit1.lscheinnr). 
      END. 
      l-kredit1.datum = pay-date. 
        
      /*ITA 170117*/
      IF NUM-ENTRIES(l-kredit1.bemerk, ";") GT 1 THEN DO:
          ENTRY(1, l-kredit1.bemerk, ";") = remark.
      END.
      ELSE l-kredit1.bemerk = remark. 
 
      count = l-kredit1.counter. 
      IF count = 0 THEN      /* NO pre-payment */ 
      DO: 
         FIND FIRST counters WHERE counters.counter-no = 24 
            EXCLUSIVE-LOCK NO-ERROR. 
         IF NOT AVAILABLE counters THEN 
         DO: 
           create counters. 
           counters.counter-no = 24. 
           counters.counter-bez = "Accounts Payable". 
         END. 
         counters.counter = counters.counter + 1. 
         l-kredit1.counter = counter.counter. 
         count = l-kredit1.counter. 
         release counter. 
      END. 
      ELSE IF count NE 0 AND outstand = 0 THEN 
      DO: 
        FOR EACH l-kredit WHERE l-kredit.opart GE 1 
          AND l-kredit.counter = count 
          AND l-kredit.name = age-list.docu-nr 
          AND l-kredit.zahlkonto GT 0 
          AND l-kredit.lief-nr = age-list.lief-nr EXCLUSIVE-LOCK: 
          l-kredit.opart = 2. 
          payment1 = payment1 - l-kredit.saldo. 
          release l-kredit. 
        END. 
      END. 
 
      FOR EACH pay-list: 
 
        IF pay-list.proz = 100 THEN pay-amount = - saldo-i. 
        ELSE 
        DO: 
          pay-amount = saldo-i / outstand1 * pay-list.betrag. 
          IF outstand = 0 THEN 
          DO: 
            IF round(payment1 - pay-amount, rundung) = 0 THEN 
             pay-amount = payment1. 
          END. 
        END. 
 
        IF age-list.tot-debt NE 0 THEN
        DO:
          create l-kredit. 
          l-kredit.lief-nr = age-list.lief-nr. 
          IF outstand NE 0 THEN l-kredit.opart = 1. 
          ELSE l-kredit.opart = 2. 
          l-kredit.name = age-list.docu-nr. 
          l-kredit.rechnr = age-list.rechnr. 
          l-kredit.lief-nr = age-list.lief-nr. 
          l-kredit.lscheinnr = age-list.lscheinnr. 
          l-kredit.saldo = pay-amount. 
          l-kredit.rabatt = age-list.rabatt. 
          l-kredit.rabattbetrag = age-list.rabattbetrag. 
          l-kredit.netto = age-list.netto. 
          l-kredit.zahlkonto = pay-list.artnr. 
          l-kredit.counter = count. 
          l-kredit.rgdatum = pay-date. 
          /*l-kredit.bemerk = remark. */
          l-kredit.bediener-nr = bediener.nr. 
            
          /*ITA 170117*/
          IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN DO:
              ENTRY(1, l-kredit.bemerk, ";") = remark.
          END.
          ELSE l-kredit.bemerk = remark. 
 
          l-kredit1.skontobetrag = l-kredit1.skontobetrag + l-kredit.saldo. 
 
          FIND FIRST umsatz WHERE umsatz.departement = 0 AND 
            umsatz.artnr = pay-list.artnr AND umsatz.datum = pay-date 
            EXCLUSIVE-LOCK NO-ERROR. 
          IF NOT AVAILABLE umsatz THEN create umsatz. 
          umsatz.datum = pay-date. 
          umsatz.artnr = pay-list.artnr. 
          umsatz.anzahl = umsatz.anzahl + 1. 
          umsatz.betrag = umsatz.betrag + l-kredit.saldo. 
          RELEASE umsatz. 
 
          CREATE ap-journal. 
          ap-journal.lief-nr = age-list.lief-nr. 
          ap-journal.docu-nr = age-list.docu-nr. 
          ap-journal.lscheinnr = age-list.lscheinnr. 
          ap-journal.rgdatum = pay-date. 
          ap-journal.saldo = l-kredit.saldo. 
          ap-journal.netto = l-kredit.netto. 
          ap-journal.zahlkonto = l-kredit.zahlkonto. 
          ap-journal.userinit = bediener.userinit. 
          ap-journal.zeit = time. 
       END.
      END.
    END. 
   /* FOR EACH pay-list: 
      delete pay-list. 
    END. */
END. 


PROCEDURE del-po: 
DEFINE INPUT PARAMETER ap-recid AS INTEGER. 
DEFINE INPUT PARAMETER docu-nr AS CHAR. 
DEFINE buffer l-od FOR l-order. 
DEFINE buffer l-ap FOR l-kredit. 
 
  FIND FIRST l-od WHERE l-od.docu-nr = docu-nr AND l-od.pos EQ 0 
    EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-od THEN RETURN. 
  /* manual created A/P, order record does NOT exists */ 
  IF l-od.loeschflag = 0 THEN return.  /* PO NOT fully delivered */ 
 
  FIND FIRST l-ap WHERE l-ap.lscheinnr = docu-nr AND l-ap.opart = 0 
    AND RECID(l-ap) NE ap-recid NO-LOCK NO-ERROR. 
  IF AVAILABLE l-ap THEN RETURN. 
/* other unpaid A/P record WITH the same docu-nr exists */ 
 
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
  l-od.loeschflag = 2. 
  l-od.lieferdatum-eff = pay-date. 
  l-od.lief-fax[3] = bediener.username. 
  FIND CURRENT l-od NO-LOCK. 
 
  FOR EACH l-od WHERE l-od.docu-nr = docu-nr AND 
     l-od.pos GT 0 AND l-od.loeschflag = 0 EXCLUSIVE-LOCK: 
    l-od.loeschflag = 2. 
    l-od.lieferdatum = pay-date. 
    l-od.lief-fax[2] = bediener.username. 
    release l-od. 
  END. 
END. 
