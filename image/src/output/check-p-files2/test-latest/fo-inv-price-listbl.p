
DEFINE TEMP-TABLE t-artikel
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

DEFINE INPUT PARAMETER billart          AS INTEGER.
DEFINE INPUT PARAMETER artdept          AS INTEGER.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL INITIAL NO.
DEFINE INPUT PARAMETER zipreis          AS DECIMAL.
DEFINE INPUT PARAMETER res-exrate       AS DECIMAL.
DEFINE INPUT PARAMETER price-decimal    AS INTEGER.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL.
DEFINE INPUT PARAMETER p-145            AS INTEGER.
DEFINE OUTPUT PARAMETER description     AS CHARACTER.
DEFINE OUTPUT PARAMETER qty             AS INTEGER.
DEFINE OUTPUT PARAMETER price           AS DECIMAL.
DEFINE OUTPUT PARAMETER msg-int         AS INTEGER.

DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE n AS INTEGER.

FOR EACH artikel NO-LOCK WHERE artikel.activeflag = YES:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.

FIND FIRST t-artikel WHERE t-artikel.artnr = billart 
    AND t-artikel.departement = artdept 
    AND t-artikel.activeflag NO-ERROR. 
IF NOT AVAILABLE t-artikel THEN msg-int = 1.

IF AVAILABLE t-artikel AND (t-artikel.artart = 0 OR t-artikel.artart = 2 
    OR t-artikel.artart = 6 OR t-artikel.artart = 7 
    OR t-artikel.artart = 8 OR t-artikel.artart = 9) THEN 
DO: 
    description = t-artikel.bezeich. 
    qty = 1. 
    IF (t-artikel.artart NE 9) OR (t-artikel.artart = 9 
        AND t-artikel.artgrp NE 0) THEN price = t-artikel.epreis. 
    ELSE 
    DO: 
        /*  already correct, DO NOT change anymore *****/ 
        IF NOT double-currency THEN 
        DO: 
            price = round(zipreis * res-exrate, price-decimal). 
            IF foreign-rate AND price-decimal = 0 THEN 
            DO: 
                IF p-145 NE 0 THEN 
                DO: 
                    n = 1. 
                    DO i = 1 TO p-145: 
                        n = n * 10. 
                    END. 
                    price = ROUND(price / n, 0) * n. 
                END.
            END. 
        END. 
        ELSE price = zipreis.
        IF price = 0 THEN msg-int = 2.
    END.
END.
