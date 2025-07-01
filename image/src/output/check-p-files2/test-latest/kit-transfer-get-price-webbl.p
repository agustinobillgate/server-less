
DEF INPUT PARAMETER billart AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER qty AS INTEGER.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER price-decimal AS INTEGER.
DEF INPUT-OUTPUT PARAMETER price AS DECIMAL.
DEF OUTPUT PARAMETER amount AS DECIMAL.
DEF OUTPUT PARAMETER amount-foreign AS DECIMAL.
DEF OUTPUT PARAMETER p-253 AS LOGICAL.

DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE n AS INTEGER.

RUN htplogic.p (253, OUTPUT p-253).


FIND FIRST h-artikel where h-artikel.artnr = billart
  AND h-artikel.departement = curr-dept AND h-artikel.activeflag
  AND h-artikel.artart = 0 NO-LOCK NO-ERROR.
IF AVAILABLE h-artikel AND NOT p-253 THEN
DO:
  IF price = h-artikel.epreis1 THEN
  DO:
    price = h-artikel.epreis1.
    FIND FIRST paramtext WHERE paramtext.txtnr = (10000 + curr-dept)
      NO-LOCK NO-ERROR.
    IF AVAILABLE paramtext THEN 
    DO:
      i = ROUND((TIME / 3600 - 0.5), 0). 
      IF i LE 0 THEN i = 24. 
      n = INTEGER(SUBSTR(paramtext.ptexte, i, 1)). 
      IF n = 2 THEN price = h-artikel.epreis2. 
    END.
  END.
  
  IF price NE 0 AND h-artikel.prozent NE 0 THEN
  DO:
    RUN calculate-amount.
    RUN update-bill(h-artikel.artart, h-artikel.artnrfront). 
  END.
END.

PROCEDURE calculate-amount: 
  IF double-currency THEN 
  DO: 
    amount-foreign = price * qty. 
    amount = price * exchg-rate * qty. 
    amount = round(amount, price-decimal). 
  END. 
  ELSE 
  DO: 
    IF h-artikel.artart = 0 THEN 
    DO: 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR. 
      IF AVAILABLE artikel 
        AND artikel.pricetab THEN 
      DO: 
        amount-foreign = price * qty. 
        price = price * exchg-rate. 
        amount = price * qty. 
        amount = round(amount, price-decimal). 
      END. 
      ELSE 
      DO: 
        amount = price * qty. 
        amount = ROUND(amount, price-decimal). 
      END. 
    END. 
    ELSE 
    DO: 
      amount = price * qty. 
      amount = round(amount, price-decimal). 
    END. 
  END. 
END.

PROCEDURE update-bill: 
  DEFINE INPUT PARAMETER h-artart AS INTEGER. 
  DEFINE INPUT PARAMETER h-artnrfront AS INTEGER. 
  DEFINE buffer fr-art FOR artikel. 
 
  DEFINE VARIABLE h-mwst AS DECIMAL. 
  DEFINE VARIABLE h-service AS DECIMAL. 
  DEFINE VARIABLE h-mwst-foreign AS DECIMAL. 
  DEFINE VARIABLE h-service-foreign AS DECIMAL. 
  DEFINE VARIABLE closed AS LOGICAL. 
  DEFINE VARIABLE p-135 AS LOGICAL.
  DEFINE VARIABLE p-134 AS LOGICAL.
  DEFINE VARIABLE p-479 AS LOGICAL.

  DEFINE VARIABLE unit-price AS DECIMAL. 
 
  DEFINE VARIABLE tax AS DECIMAL. 
  DEFINE VARIABLE serv AS DECIMAL. 
 
  DEFINE VARIABLE sysdate AS DATE. 
  DEFINE VARIABLE zeit AS INTEGER. 
 
  DEF VAR f-dec AS DECIMAL.
  
  ASSIGN
    h-service = 0
    h-mwst = 0
    h-service-foreign = 0
    h-mwst-foreign = 0
    unit-price = price. 
  
  RUN htplogic.p (135, OUTPUT p-135).
  RUN htplogic.p (134, OUTPUT p-134).
  RUN htplogic.p (479, OUTPUT p-479).
  IF NOT p-135 /* service NOT included */ 
    AND h-artart = 0 AND h-artikel.service-code NE 0 THEN 
  DO: 
    RUN htpdec.p (h-artikel.service-code, OUTPUT f-dec).
    IF f-dec NE 0 THEN 
    DO: 
      serv = f-dec / 100. 
      h-service = unit-price * f-dec / 100. 
      h-service-foreign = round(h-service, 2). 
      IF double-currency THEN h-service = round(h-service * exchg-rate, 2). 
      ELSE h-service = round(h-service, 2). 
    END. 
 
    IF NOT p-134 /* mwst NOT included */ 
      AND h-artart = 0 AND h-artikel.mwst-code NE 0 THEN 
    DO: 
      RUN htpdec.p (h-artikel.mwst-code, OUTPUT f-dec).
      IF f-dec NE 0 THEN 
      DO: 
        tax = f-dec / 100. 
        h-mwst = f-dec. 
        IF p-479 /* service taxable */ THEN 
        DO: 
          tax = tax * ( 1 + serv). 
          h-mwst = unit-price * tax. 
/*        h-mwst = h-mwst * (unit-price + h-service-foreign) / 100.  */ 
        END. 
        ELSE h-mwst = h-mwst * unit-price / 100. 
        h-mwst-foreign = round(h-mwst, 2). 
        IF double-currency THEN 
        DO: 
          h-mwst = tax * unit-price * exchg-rate. 
          h-mwst = round(h-mwst, 2). 
        END. 
        ELSE h-mwst = round(h-mwst, 2). 
      END. 
    END. 
  END. 
  amount = amount + (h-service + h-mwst) * qty. 
  amount = round(amount, price-decimal). 
  amount-foreign = amount-foreign + (h-service-foreign + h-mwst-foreign ) * qty. 
END. 



