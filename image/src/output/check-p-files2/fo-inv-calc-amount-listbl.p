
DEF TEMP-TABLE t-artikel
    FIELD artnr         LIKE artikel.artnr
    FIELD bezeich       LIKE artikel.bezeich
    FIELD epreis        LIKE artikel.epreis
    FIELD departement   LIKE artikel.departement
    FIELD artart        LIKE artikel.artart
    FIELD activeflag    LIKE artikel.activeflag
    FIELD artgrp        LIKE artikel.artgrp
    FIELD bezaendern    LIKE artikel.bezaendern
    FIELD autosaldo     LIKE artikel.autosaldo
    FIELD pricetab      LIKE artikel.pricetab
    FIELD betriebsnr    LIKE artikel.betriebsnr
    FIELD resart        LIKE artikel.resart
    FIELD zwkum         LIKE artikel.zwkum.

DEFINE TEMP-TABLE t-exrate LIKE exrate.
DEFINE TEMP-TABLE t-waehrung LIKE waehrung.

DEFINE INPUT PARAMETER transdate        AS DATE.
DEFINE INPUT PARAMETER betriebsnr       AS INTEGER.
DEFINE INPUT PARAMETER artart           AS INTEGER.
DEFINE INPUT PARAMETER pricetab         AS LOGICAL.
DEFINE INPUT PARAMETER balance-foreign  AS DECIMAL.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL.
DEFINE INPUT PARAMETER balance          AS DECIMAL.
DEFINE INPUT PARAMETER price            AS DECIMAL.
DEFINE INPUT PARAMETER price-decimal    AS INTEGER.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL.
DEFINE INPUT PARAMETER p-145            AS INTEGER.
DEFINE INPUT PARAMETER epreis           AS DECIMAL.
DEFINE INPUT PARAMETER adrflag          AS LOGICAL.
DEFINE INPUT PARAMETER artgrp           AS INTEGER.
DEFINE INPUT PARAMETER qty              AS INTEGER.
DEFINE INPUT PARAMETER res-exrate       AS DECIMAL.
DEFINE INPUT PARAMETER exchg-rate       AS DECIMAL INITIAL 1.
DEFINE INPUT PARAMETER zipreis          AS DECIMAL.

DEFINE OUTPUT PARAMETER amount-foreign  AS DECIMAL.
DEFINE OUTPUT PARAMETER amount          AS DECIMAL.
DEFINE OUTPUT PARAMETER avrg-kurs       AS DECIMAL INITIAL 1.
DEFINE OUTPUT PARAMETER rate-defined    AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER msg-int         AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER.

DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE n AS INTEGER.
/*
FOR EACH artikel NO-LOCK WHERE artikel.activeflag = YES:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.
*/
RUN fo-invoice-calculate-amountbl.p(transdate, betriebsnr, 
                                    OUTPUT TABLE t-exrate, OUTPUT TABLE t-waehrung).

IF (artart = 2 OR artart = 4 OR 
    artart = 6 OR artart = 7 ) THEN 
DO: 
  IF (pricetab AND balance-foreign NE 0 AND double-currency) THEN
  DO: 
    ASSIGN
      amount-foreign = price
      amount         = ROUND (price * balance / balance-foreign, price-decimal).
    RETURN.
  END.
  ELSE IF (NOT pricetab AND balance NE 0 AND double-currency) THEN
  DO: 
    ASSIGN
      amount         = price
      amount-foreign = ROUND (price * balance-foreign / balance, 2).
    RETURN.
  END.
  IF foreign-rate OR pricetab THEN 
  DO: 
    IF double-currency AND balance-foreign NE 0 THEN avrg-kurs = balance / balance-foreign. 
    IF pricetab AND betriebsnr NE 0 THEN 
    DO: 
      IF transdate NE ? THEN 
      DO: 
        FIND FIRST t-exrate NO-ERROR. 
        IF AVAILABLE t-exrate THEN 
        DO: 
          rate-defined = YES. 
          avrg-kurs = t-exrate.betrag. 
        END.
      END. 
      IF NOT rate-defined THEN 
      DO: 
        FIND FIRST t-waehrung WHERE t-waehrung.waehrungsnr = betriebsnr 
          AND t-waehrung.ankauf NE 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE t-waehrung THEN avrg-kurs = t-waehrung.ankauf / t-waehrung.einheit. 
        ELSE avrg-kurs = exchg-rate.
      END. 
    END. 
    ELSE avrg-kurs = exchg-rate. 
  END. 
  ELSE avrg-kurs = exchg-rate. 
  
  IF pricetab THEN  /* foreign currency */ 
  DO: 
    amount-foreign = price * qty. 
    amount = price * avrg-kurs * qty. 
    amount = ROUND(amount, price-decimal). 
  END. 
  ELSE 
  DO:     
    amount = price * qty. 
    amount = ROUND(amount, price-decimal). 
  /*  old  */ 
  /*    amount-foreign = ROUND(amount / avrg-kurs, 2).   */ 
  /* %%% NEW 13/03/03 */ 
    IF balance NE 0 THEN 
      amount-foreign = ROUND(balance-foreign / balance * amount, 6). 
  /*      ELSE amount-foreign = ROUND(amount / avrg-kurs, 6). */
  /* 12 Aug 2007 Tashkent */
    ELSE amount-foreign = ROUND(amount / exchg-rate, 6). 
  END. 
END.
ELSE 
DO: 
  IF double-currency THEN 
  DO: 
    IF artart = 9 AND artgrp = 0 AND adrflag THEN 
    DO: 
      amount-foreign = price * qty / exchg-rate. 
      amount = price * qty. 
      amount = ROUND(amount, price-decimal). 
    END. 
    ELSE 
    DO: 
      amount-foreign = price * qty. 
      amount = price * exchg-rate * qty. 
      amount = ROUND(amount, price-decimal). 
    END. 
  END.
  ELSE 
  DO: 
    IF artart = 9 AND artgrp NE 0 THEN 
    DO:
      IF pricetab THEN 
      DO: 
        FIND FIRST t-waehrung WHERE t-waehrung.waehrungsnr = betriebsnr 
            AND t-waehrung.ankauf NE 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE t-waehrung THEN avrg-kurs = t-waehrung.ankauf / t-waehrung.einheit. 
        ELSE avrg-kurs = exchg-rate. 
        amount-foreign = price * qty. 
        amount = amount-foreign * avrg-kurs.
      END. 
      ELSE 
      DO: 
        amount = price * qty. 
        amount-foreign = ROUND(amount / res-exrate, 6). 
      END. 
      amount = ROUND(amount, price-decimal). 
    END. 
    ELSE IF artart = 9 AND NOT adrflag AND foreign-rate THEN 
    DO: 
      amount = price * qty. 
      amount-foreign = zipreis * qty. 
    END. 
    ELSE 
    DO: 
      IF pricetab THEN 
      DO: 
        FIND FIRST t-waehrung WHERE t-waehrung.waehrungsnr = betriebsnr 
          AND t-waehrung.ankauf NE 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE t-waehrung THEN avrg-kurs = t-waehrung.ankauf / t-waehrung.einheit. 
        ELSE avrg-kurs = exchg-rate. 
        amount-foreign = price * qty. 
        amount = amount-foreign * avrg-kurs.
      END. 
      ELSE 
      DO: 
        amount = price * qty. 
        amount-foreign = ROUND(amount / res-exrate, 6). 
      END. 
      amount = ROUND(amount, price-decimal). 
    END. 
  END.
END.

IF (artart = 0 OR artart = 8) AND epreis = 0 
    AND double-currency THEN msg-int = 1. 
ELSE IF (artart = 2 OR artart = 7 OR artart = 6) 
    AND double-currency THEN msg-int = 2.

IF artart = 9 AND artgrp = 0 
  AND foreign-rate AND price-decimal = 0 THEN 
DO: 
  IF p-145 NE 0 THEN 
  DO: 
    n = 1. 
    DO i = 1 TO p-145:
      n = n * 10. 
    END. 
    amount = ROUND(amount / n, 0) * n. 
  END.
END.

IF qty LT 0 AND artart = 9 AND artgrp = 0 THEN msg-str = "1".
ELSE IF qty GT 1 AND artart = 9 AND artgrp = 0 THEN msg-str = "2".

