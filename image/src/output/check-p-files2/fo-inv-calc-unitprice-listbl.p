
DEFINE INPUT PARAMETER autosaldo        AS LOGICAL.
DEFINE INPUT PARAMETER pricetab         AS LOGICAL.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL.
DEFINE INPUT PARAMETER artnr            AS INTEGER.
DEFINE INPUT PARAMETER balance          AS DECIMAL.
DEFINE INPUT PARAMETER balance-foreign  AS DECIMAL.
DEFINE INPUT PARAMETER billart          AS INTEGER.
DEFINE INPUT PARAMETER vat-artList      AS INTEGER EXTENT 4 INITIAL [0,0,0,0].
DEFINE INPUT PARAMETER lvAnzVat         AS INTEGER.
DEFINE INPUT PARAMETER curr-department  AS INTEGER.
DEFINE INPUT PARAMETER bil-recid        AS INTEGER.

DEFINE OUTPUT PARAMETER price           AS DECIMAL.
DEFINE OUTPUT PARAMETER exrate          AS DECIMAL.
DEFINE OUTPUT PARAMETER found           AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER msg             AS INTEGER.

DEFINE VARIABLE amt     AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE ind     AS INTEGER INITIAL 0 NO-UNDO.

/******************************************************************************/
IF autosaldo THEN  /* $$$ */ 
DO: 
    IF pricetab OR double-currency THEN 
    DO: 
        IF double-currency THEN 
        DO:    
            IF pricetab THEN price = - balance-foreign.
            ELSE price = - balance.
        END.
        ELSE 
        DO:
            RUN fo-invoice-return-qtybl.p(artnr, balance,
                    OUTPUT exrate, OUTPUT price, OUTPUT msg).
        END.
    END.
    ELSE
    DO:
        DO ind = 1 TO lvAnzVat:
            IF billArt = vat-artList[ind] THEN found = YES.
        END.
        IF NOT found OR curr-department GT 0 THEN 
        DO:    
            price = - balance.
            RETURN.
        END.
        
        RUN fo-invoice-calculate-unitpricebl.p(billart, bil-recid, OUTPUT amt).
        price = amt.
    END.
END.
