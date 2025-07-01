
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT-OUTPUT PARAMETER price AS DECIMAL.
DEF INPUT PARAMETER qty AS INT.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER price-decimal AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER cancel-flag AS LOGICAL.
DEF INPUT PARAMETER foreign-rate AS LOGICAL.

DEF OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.
DEF OUTPUT PARAMETER amount LIKE vhp.bill-line.betrag.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code1 AS INT INIT 0.

FIND FIRST h-artikel WHERE RECID(h-artikel) = rec-id.
RUN calculate-amount.

PROCEDURE calculate-amount: 
DEFINE VARIABLE avrg-kurs       AS DECIMAL INITIAL 1. 
DEFINE VARIABLE rate-defined    AS LOGICAL INITIAL NO.
DEFINE VARIABLE answer          AS LOGICAL INITIAL NO.
DEFINE BUFFER artikel1          FOR vhp.artikel. 
DEFINE BUFFER w1                FOR vhp.waehrung.

  IF double-currency THEN 
  ASSIGN
      amount-foreign = price * qty
      amount = price * exchg-rate * qty 
      amount = ROUND(amount, price-decimal)
  . 
  ELSE 
  DO: 
    IF vhp.h-artikel.artart = 0 THEN 
    DO: 
      FIND FIRST artikel1 WHERE artikel1.artnr = vhp.h-artikel.artnrfront 
        AND artikel1.departement = vhp.h-artikel.departement NO-LOCK NO-ERROR. 
      IF AVAILABLE artikel1 AND artikel1.pricetab AND artikel1.betriebsnr NE 0
      /* price IN foreign currency */ THEN 
      DO: 
        IF transdate NE ? THEN 
        DO: 
          FIND FIRST exrate WHERE exrate.artnr = artikel1.betriebsnr 
            AND exrate.datum = transdate NO-LOCK NO-ERROR. 
          IF AVAILABLE exrate THEN 
          DO: 
            rate-defined = YES. 
            avrg-kurs = exrate.betrag. 
          END. 
        END. 
        IF NOT rate-defined THEN 
        DO: 
          FIND FIRST w1 WHERE w1.waehrungsnr = artikel1.betriebsnr 
            AND w1.ankauf NE 0 NO-LOCK NO-ERROR. 
          IF AVAILABLE w1 THEN avrg-kurs = w1.ankauf / w1.einheit. 
          ELSE avrg-kurs = exchg-rate. 
        END. 
        ELSE avrg-kurs = exchg-rate.
      END.
      ELSE avrg-kurs = exchg-rate.

      IF artikel1.pricetab AND NOT cancel-flag THEN
      DO:
        amount-foreign = price * qty. 
        price = price * avrg-kurs. 
        amount = price * qty. 
        amount = ROUND(amount, price-decimal). 
      END. 
      ELSE 
      DO:        
        /*FDL Feb 22, 2024 => Ticket DC070D*/
        amount = price * qty. 
        IF foreign-rate THEN amount-foreign = ROUND(amount / exchg-rate, 2). 
        /*amount = ROUND(amount, price-decimal).*/
      END. 
    END. 
    ELSE 
    DO:         
      amount = price * qty. 
      amount = ROUND(amount, price-decimal). 
    END. 
  END. 
  IF (amount GT 99999999) OR (amount LT -99999999) THEN
  DO:
    fl-code = 1.
  END.

  IF amount < 0 AND vhp.h-artikel.artart = 0 THEN 
  DO: 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 261 NO-LOCK. 
    IF vhp.htparam.flogical THEN 
    DO: 
      fl-code1 = 1.
    END. 
  END.

END. 
