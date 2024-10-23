DEFINE INPUT PARAMETER bill-no       AS INTEGER.
DEFINE INPUT PARAMETER datum         AS DATE.
                                     
DEFINE OUTPUT PARAMETER datum1       AS DATE.
DEFINE OUTPUT PARAMETER saldo        AS DECIMAL.
DEFINE OUTPUT PARAMETER avail-kredit AS LOGICAL.
DEFINE OUTPUT PARAMETER msg-str      AS CHAR.

IF datum EQ ? THEN
DO:
    RUN release-ap-return-billnobl.p (1, bill-no, ?, OUTPUT datum1, OUTPUT saldo, 
                                      OUTPUT avail-kredit).  
END.
ELSE 
DO:
    RUN release-ap-return-billnobl.p (2, bill-no, datum, OUTPUT datum1, OUTPUT saldo,  
                                      OUTPUT avail-kredit).  
    IF NOT avail-kredit THEN   
    DO:    
        msg-str = "No such A/P record found!".
        RETURN. 
    END.
END.
