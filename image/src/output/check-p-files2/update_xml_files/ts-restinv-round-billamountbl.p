
DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER rec-id         AS INT.
DEF INPUT  PARAMETER rest-amount    AS DECIMAL.

DEF INPUT  PARAMETER double-currency AS LOGICAL.
DEF INPUT  PARAMETER exchg-rate     AS DECIMAL.
DEF INPUT  PARAMETER transdate      AS DATE.
DEF INPUT  PARAMETER cancel-flag    AS LOGICAL.
DEF INPUT  PARAMETER foreign-rate   AS LOGICAL.

DEF OUTPUT PARAMETER printed        AS CHAR.
DEF OUTPUT PARAMETER billart        AS INT.
DEF OUTPUT PARAMETER qty            AS INT.
DEF OUTPUT PARAMETER DESCRIPTION    AS CHAR.
DEF OUTPUT PARAMETER price          AS DECIMAL.
DEF OUTPUT PARAMETER fl-code        AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code1       AS INT INIT 0.

DEF OUTPUT PARAMETER amount-foreign AS DECIMAL INIT 0.
DEF OUTPUT PARAMETER amount         AS DECIMAL.
/*MT

DEF OUTPUT PARAMETER succed         AS LOGICAL.
*/
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

/*FT*/
DEFINE VARIABLE gst-logic       AS LOGICAL INITIAL NO.

FIND FIRST htparam WHERE htparam.paramnr = 376 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    IF NOT htparam.flogic AND ENTRY(1,htparam.fchar,";") = "GST(MA)" THEN
        gst-logic = YES.
END.

RUN Round-Billamount.

PROCEDURE Round-Billamount:
DEF VAR rest-amount  AS DECIMAL NO-UNDO.
  
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 738 NO-LOCK.
  IF vhp.htparam.finteger = 0 THEN RETURN.
  
  FIND FIRST vhp.h-bill WHERE RECID(vhp.h-bill) = rec-id NO-LOCK.
  IF vhp.h-bill.flag = 1 THEN RETURN.
  IF gst-logic THEN 
  DO:
      rest-amount = 0.
      RUN calc-round(vhp.h-bill.saldo,OUTPUT rest-amount).
      rest-amount = rest-amount - vhp.h-bill.saldo.
  END.
  ELSE rest-amount = vhp.h-bill.saldo - TRUNCATE(vhp.h-bill.saldo, 0).

  IF rest-amount = 0 THEN RETURN.

  FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.htparam.finteger
      AND vhp.artikel.departement = curr-dept NO-LOCK NO-ERROR.
  IF NOT AVAILABLE vhp.artikel THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("F/O Article not found (Param 738):",lvCAREA,"")
            + " " + STRING(vhp.htparam.finteger).
    RETURN.
  END.
  
  IF vhp.artikel.artart NE 0 THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Rouding F/O Article type must be Revenue: ",lvCAREA,"")
            + " " + STRING(vhp.htparam.finteger) + "-" + vhp.artikel.bezeich.
    RETURN.
  END.

  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnrfront = vhp.artikel.artnr
    AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
  IF NOT AVAILABLE vhp.h-artikel THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("POS rounding Article not found.",lvCAREA,"").
    RETURN.
  END.
  
  CREATE t-h-artikel.
  BUFFER-COPY h-artikel TO t-h-artikel.
  t-h-artikel.rec-id = RECID(h-artikel).
  IF vhp.h-artikel.artart NE 0 THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("POS Rouding Article's type must be Revenue: ",lvCAREA,"")
            + " " + STRING(vhp.htparam.finteger) + "-" + vhp.h-artikel.bezeich.
    RETURN.
  END.
  
  ASSIGN 
      printed = ""
      billart = vhp.h-artikel.artnr
      qty = 1
      DESCRIPTION = vhp.h-artikel.bezeich.

  IF gst-logic THEN
  DO:
      /*IF rest-amount GT 0 THEN
      DO:
        IF rest-amount LT 0.05 THEN price = - rest-amount.
        ELSE price = 0.1 - rest-amount.
      END.
      ELSE
      DO:
        IF (- rest-amount) LT 0.05 THEN price = - rest-amount.
        ELSE price = - (0.1 + rest-amount).
      END.*/
      price = rest-amount.
  END.
  ELSE
  DO:
      IF rest-amount GT 0 THEN
      DO:
        IF rest-amount LT 0.5 THEN price = - rest-amount.
        ELSE price = 1 - rest-amount.
      END.
      ELSE
      DO:
        IF (- rest-amount) LT 0.5 THEN price = - rest-amount.
        ELSE price = - (1 + rest-amount).
      END.
  END.
  
  fl-code = 1.
  RUN calculate-amount.
  /*MT
  IF price NE 0 AND amount = 0 THEN .
  ELSE RUN update-bill(vhp.h-artikel.artart, vhp.h-artikel.artnrfront).
  DISP balance WITH FRAME frame1. 
  IF double-currency THEN DISP balance-foreign WITH FRAME frame1. */
END.


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
        amount = price * qty. 
        IF foreign-rate THEN amount-foreign = ROUND(amount / exchg-rate, 2). 
        amount = ROUND(amount, price-decimal). 
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
    /*MTHIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("The amount = ",lvCAREA,"") 
      + TRIM(STRING(amount, "->>,>>>,>>>,>>9.99")) 
      SKIP 
      translateExtended ("Is this correct?",lvCAREA,"") 
      VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
    IF NOT answer THEN amount = 0.*/
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

PROCEDURE calc-round:
    DEFINE INPUT PARAMETER amount1 AS DECIMAL.
    DEFINE OUTPUT PARAMETER amount2 AS DECIMAL.

    IF amount1 - TRUNCATE(amount1,1) LE 0.02 THEN amount2 = ROUND(amount1,1).
    ELSE IF (amount1 - TRUNCATE(amount1,1) GE 0.02 AND amount1 - TRUNCATE(amount1,1) LE 0.05)
        OR (amount1 - TRUNCATE(amount1,1) = 0.06 OR amount1 - TRUNCATE(amount1,1) = 0.07) THEN 
        amount2 = TRUNCATE(amount1,1) + 0.05.
    ELSE amount2 = ROUND(amount1,1).

END.
