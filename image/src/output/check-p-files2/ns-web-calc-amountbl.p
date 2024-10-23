DEFINE TEMP-TABLE t-exrate      LIKE exrate.
DEFINE TEMP-TABLE w1            LIKE waehrung.

DEFINE INPUT PARAMETER t-artikel-artart     AS INT.
DEFINE INPUT PARAMETER foreign-rate         AS LOGICAL.
DEFINE INPUT PARAMETER t-artikel-pricetab   AS LOGICAL.
DEFINE INPUT PARAMETER balance-foreign      AS DECIMAL.
DEFINE INPUT PARAMETER transdate            AS DATE.
DEFINE INPUT PARAMETER t-artikel-betriebsnr AS INT.
DEFINE INPUT PARAMETER double-currency      AS LOGICAL.
DEFINE INPUT PARAMETER price-decimal        AS INT.
DEFINE INPUT PARAMETER price                AS DECIMAL.
DEFINE INPUT PARAMETER balance              AS DECIMAL.
DEFINE INPUT PARAMETER exchg-rate           AS DECIMAL. 
DEFINE INPUT PARAMETER qty                  AS INT.
DEFINE INPUT PARAMETER t-artikel-artgrp     AS INT.

DEFINE OUTPUT PARAMETER amount-foreign AS DECIMAL.
DEFINE OUTPUT PARAMETER amount         AS DECIMAL.

DEFINE VARIABLE avrg-kurs       AS DECIMAL INITIAL 1. 
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE n               AS INTEGER. 
DEFINE VARIABLE rate-defined    AS LOGICAL INITIAL NO NO-UNDO. 


IF (t-artikel-artart = 2 OR t-artikel-artart = 4 OR t-artikel-artart = 6 OR t-artikel-artart = 7 ) THEN 
DO: 
    IF (t-artikel-pricetab AND balance-foreign NE 0 AND double-currency) THEN
    DO:
        ASSIGN
            amount-foreign = price
            amount         = ROUND (price * balance / balance-foreign, price-decimal).
        RETURN.
    END.
    ELSE IF (NOT t-artikel-pricetab AND balance NE 0 AND double-currency) THEN
    DO:
        ASSIGN
            amount         = price
            amount-foreign = ROUND (price * balance-foreign / balance, 2).
        RETURN.
    END.
    IF foreign-rate OR t-artikel-pricetab THEN 
    DO: 
        IF double-currency AND balance-foreign NE 0 THEN avrg-kurs = balance / balance-foreign. 
        IF t-artikel-pricetab AND t-artikel-betriebsnr NE 0 THEN 
        DO: 
            IF transdate NE ? THEN 
            DO: 
                RUN read-exratebl.p (1,t-artikel-betriebsnr, transdate, OUTPUT TABLE t-exrate).
                FIND FIRST t-exrate NO-LOCK NO-ERROR. 
                IF AVAILABLE t-exrate THEN 
                DO: 
                    rate-defined = YES. 
                    avrg-kurs = t-exrate.betrag. 
                END. 
            END. 
            IF NOT rate-defined THEN 
            DO: 
                RUN read-waehrungbl.p (7, t-artikel-betriebsnr, ?, OUTPUT TABLE w1).
                FIND FIRST w1 NO-LOCK NO-ERROR. 
                IF AVAILABLE w1 THEN avrg-kurs = w1.ankauf / w1.einheit. 
                ELSE avrg-kurs = exchg-rate. 
            END.
        END. 
        ELSE avrg-kurs = exchg-rate. 
    END. 
    ELSE avrg-kurs = exchg-rate. 
 
    IF t-artikel-pricetab THEN  /* foreign currency */ 
    DO: 
        amount-foreign = price * qty. 
        amount = price * avrg-kurs * qty. 
        amount = ROUND(amount, price-decimal). 
    END. 
    ELSE 
    DO: 
        amount = price * qty. 
        amount = ROUND(amount, price-decimal). 
        amount-foreign = ROUND(amount / avrg-kurs, 6). 
    END. 
END. 
ELSE 
DO: 
    IF double-currency THEN 
    DO: 

        DO: 
            amount-foreign = price * qty. 
            amount = price * exchg-rate * qty. 
            amount = ROUND(amount, price-decimal). 
        END. 
    END. 
    ELSE 
    DO: 
        DO: 
            IF t-artikel-pricetab THEN 
            DO: 
                RUN read-waehrungbl.p (7, t-artikel-betriebsnr, ?,OUTPUT TABLE w1).
                FIND FIRST w1 NO-LOCK NO-ERROR. 
                IF AVAILABLE w1 THEN avrg-kurs = w1.ankauf / w1.einheit. 
                ELSE avrg-kurs = exchg-rate. 
                amount-foreign = price * qty. 
                amount = amount-foreign * avrg-kurs. 
            END. 
            ELSE 
            DO: 
                amount = price * qty. 
                amount-foreign = ROUND(amount / exchg-rate, 6). 
            END. 
            amount = ROUND(amount, price-decimal). 
        END. 
    END. 
END. 
