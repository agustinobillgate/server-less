DEF TEMP-TABLE t-h-artikel LIKE h-artikel  
    FIELD rec-id AS INT.  
  
DEF INPUT PARAMETER menu-list-artnr AS INT.  
DEF INPUT PARAMETER menu-list-bezeich AS CHAR.  
DEF INPUT PARAMETER menu-list-anzahl AS INT.  
DEF INPUT PARAMETER menu-list-price AS DECIMAL.  
DEF INPUT PARAMETER curr-dept AS INT.  
DEF INPUT PARAMETER cancel-reason AS CHAR.  
DEF INPUT PARAMETER double-currency AS LOGICAL.  
DEF INPUT PARAMETER exchg-rate AS DECIMAL.  
DEF INPUT PARAMETER price-decimal AS INT.  
DEF INPUT PARAMETER transdate AS DATE.  
DEF INPUT PARAMETER cancel-flag AS LOGICAL.  
DEF INPUT PARAMETER foreign-rate AS LOGICAL.  
  
DEF OUTPUT PARAMETER description AS CHAR.  
DEF OUTPUT PARAMETER qty AS INT.  
DEF OUTPUT PARAMETER price AS DECIMAL.  
DEF OUTPUT PARAMETER cancel-str AS CHAR.  
DEF OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.  
DEF OUTPUT PARAMETER amount LIKE vhp.bill-line.betrag.  
DEF OUTPUT PARAMETER fl-code AS INT.  
DEF OUTPUT PARAMETER fl-code1 AS INT.  
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.  
  
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = menu-list-artnr   
    AND vhp.h-artikel.departement = curr-dept NO-LOCK.  
CREATE t-h-artikel.  
BUFFER-COPY h-artikel TO t-h-artikel.  
ASSIGN t-h-artikel.rec-id = RECID(h-artikel).  
  
  
  
ASSIGN  
description = menu-list-bezeich  
qty = menu-list-anzahl  
price = menu-list-price.  
  
IF qty LT 0 THEN cancel-str = cancel-reason.   
RUN ts-restinv-calculate-amountbl.p  
   (RECID(h-artikel), double-currency, INPUT-OUTPUT price, qty,  
    exchg-rate, price-decimal, transdate, cancel-flag,  
    foreign-rate, OUTPUT amount-foreign, OUTPUT amount,  
    OUTPUT fl-code, OUTPUT fl-code1).  
