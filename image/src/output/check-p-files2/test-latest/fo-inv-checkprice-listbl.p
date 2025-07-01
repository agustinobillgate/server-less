
DEFINE INPUT PARAMETER pvILanguage          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER double-currency      AS LOGICAL.
DEFINE INPUT PARAMETER price                AS DECIMAL.
DEFINE INPUT PARAMETER p-1086               AS DECIMAL.
DEFINE INPUT PARAMETER billart              AS INTEGER.
DEFINE INPUT PARAMETER curr-department      AS INTEGER.
DEFINE INPUT PARAMETER balance              AS DECIMAL.
DEFINE INPUT PARAMETER balance-foreign      AS DECIMAL.
DEFINE INPUT PARAMETER price-decimal        AS INTEGER.
DEFINE INPUT PARAMETER exchg-rate           AS DECIMAL.

{SupertransBL.i}
DEFINE OUTPUT PARAMETER do-it               AS LOGICAL INITIAL YES.
DEFINE OUTPUT PARAMETER msgInt              AS INTEGER.
DEFINE OUTPUT PARAMETER l-price             AS DECIMAL FORMAT "->>>,>>>,>>9.99".

DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "fo-inv-check-price".
DEFINE VARIABLE answer AS LOGICAL INITIAL NO. 
DEFINE VARIABLE max-price AS DECIMAL NO-UNDO.

DEFINE BUFFER t-artikel FOR artikel.
/******************************************************************************/

FIND FIRST t-artikel WHERE t-artikel.artnr = billart
    AND t-artikel.departement = curr-department NO-LOCK NO-ERROR.
IF AVAILABLE t-artikel THEN
DO:
    max-price = p-1086.
    IF price = 0 THEN 
    DO: 
        do-it = NO. 
        RETURN. 
    END.
 
    IF double-currency AND ((price GE 100) OR (price LE - 100)) 
        AND t-artikel.pricetab THEN 
    DO:
      IF (t-artikel.artart = 2 OR t-artikel.artart = 6 OR t-artikel.artart = 7) 
          AND balance-foreign NE 0 THEN
      DO:
          ASSIGN l-price = ROUND(price * balance / balance-foreign, price-decimal).
      END.          
      ELSE ASSIGN l-price = ROUND(price * exchg-rate, price-decimal).
        
      msgInt = 1.
    END. 

    IF NOT double-currency AND max-price NE 0 THEN 
    DO: 
        IF price GT 0 THEN l-price = price. 
        ELSE l-price = - price. 
        IF t-artikel.pricetab THEN 
        DO:
            RUN fo-invoice-check-pricebl.p
                (INPUT-OUTPUT l-price, t-artikel.artnr, t-artikel.departement).
        END. 
        IF l-price GE max-price THEN 
        DO: 
            msgInt = 2.
            do-it = NO. 
        END. 
    END.  
END.

