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

DEF TEMP-TABLE t-foinv
    FIELD vipnr1            AS INT
    FIELD vipnr2            AS INT
    FIELD vipnr3            AS INT
    FIELD vipnr4            AS INT
    FIELD vipnr5            AS INT
    FIELD vipnr6            AS INT
    FIELD vipnr7            AS INT
    FIELD vipnr8            AS INT
    FIELD vipnr9            AS INT
    FIELD ext-char          AS CHAR
    FIELD price-decimal     AS INT
    FIELD double-currency   AS LOGICAL
    FIELD change-date       AS LOGICAL
    FIELD foreign-rate      AS LOGICAL
    FIELD exchg-rate        AS DECIMAL INIT 1
    FIELD curr-local        AS CHAR
    FIELD curr-foreign      AS CHAR
    FIELD lvAnzVat          AS INT
    FIELD b-title           AS CHAR
    FIELD artikel-str       AS CHAR
    FIELD p-219             AS LOGICAL
    FIELD p-199             AS LOGICAL
    FIELD p-145             AS INT
    FIELD p-242             AS INT
    FIELD p-60              AS INT
    FIELD p-251             AS LOGICAL
    FIELD p-2313            AS INT
    FIELD p-1116            AS INT
    FIELD p-685             AS INT
    FIELD avail-brief685    AS LOGICAL INIT NO
    FIELD p-173             AS CHAR
    FIELD p-2314            AS INT
    FIELD p-83              AS LOGICAL
    FIELD p-497             AS INT
    FIELD p-120             AS INT
    FIELD avail-brief497    AS LOGICAL INIT NO
    FIELD p-1086            AS DECIMAL.

DEFINE INPUT PARAMETER bil-flag           AS INTEGER.
DEFINE OUTPUT PARAMETER vipnr1            AS INT.            
DEFINE OUTPUT PARAMETER vipnr2            AS INT.           
DEFINE OUTPUT PARAMETER vipnr3            AS INT.          
DEFINE OUTPUT PARAMETER vipnr4            AS INT.         
DEFINE OUTPUT PARAMETER vipnr5            AS INT.            
DEFINE OUTPUT PARAMETER vipnr6            AS INT.           
DEFINE OUTPUT PARAMETER vipnr7            AS INT.           
DEFINE OUTPUT PARAMETER vipnr8            AS INT.           
DEFINE OUTPUT PARAMETER vipnr9            AS INT.            
DEFINE OUTPUT PARAMETER ext-char          AS CHAR.           
DEFINE OUTPUT PARAMETER price-decimal     AS INT.            
DEFINE OUTPUT PARAMETER double-currency   AS LOGICAL.        
DEFINE OUTPUT PARAMETER change-date       AS LOGICAL.        
DEFINE OUTPUT PARAMETER foreign-rate      AS LOGICAL.        
DEFINE OUTPUT PARAMETER exchg-rate        AS DECIMAL INIT 1. 
DEFINE OUTPUT PARAMETER curr-local        AS CHAR.           
DEFINE OUTPUT PARAMETER curr-foreign      AS CHAR.           
DEFINE OUTPUT PARAMETER lvAnzVat          AS INT .           
DEFINE OUTPUT PARAMETER b-title           AS CHAR.           
DEFINE OUTPUT PARAMETER artikel-str       AS CHAR.           
DEFINE OUTPUT PARAMETER p-219             AS LOGICAL.        
DEFINE OUTPUT PARAMETER p-199             AS LOGICAL.        
DEFINE OUTPUT PARAMETER p-145             AS INT.            
DEFINE OUTPUT PARAMETER p-242             AS INT.             
DEFINE OUTPUT PARAMETER p-60              AS INT.             
DEFINE OUTPUT PARAMETER p-251             AS LOGICAL.         
DEFINE OUTPUT PARAMETER p-2313            AS INT.             
DEFINE OUTPUT PARAMETER p-1116            AS INT.             
DEFINE OUTPUT PARAMETER p-685             AS INT.             
DEFINE OUTPUT PARAMETER avail-brief685    AS LOGICAL INIT NO. 
DEFINE OUTPUT PARAMETER p-173             AS CHAR.            
DEFINE OUTPUT PARAMETER p-2314            AS INT .            
DEFINE OUTPUT PARAMETER p-83              AS LOGICAL.        
DEFINE OUTPUT PARAMETER p-497             AS INT.            
DEFINE OUTPUT PARAMETER p-120             AS INT.            
DEFINE OUTPUT PARAMETER avail-brief497    AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER p-1086            AS DECIMAL.    
DEFINE OUTPUT PARAMETER cash-refund-str   AS CHAR.
DEFINE OUTPUT PARAMETER rebate-str        AS CHAR.        
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.

RUN prepare-fo-invoicebl.p (bil-flag, OUTPUT TABLE t-artikel, OUTPUT TABLE t-foinv).
RUN init-var.

PROCEDURE init-var:
    FIND FIRST t-foinv NO-LOCK.
    ASSIGN 
        vipnr1          = t-foinv.vipnr1
        vipnr2          = t-foinv.vipnr2
        vipnr3          = t-foinv.vipnr3
        vipnr4          = t-foinv.vipnr4
        vipnr5          = t-foinv.vipnr5
        vipnr6          = t-foinv.vipnr6
        vipnr7          = t-foinv.vipnr7
        vipnr8          = t-foinv.vipnr8
        vipnr9          = t-foinv.vipnr9
        ext-char        = ENTRY(1, t-foinv.ext-char, ";")
        price-decimal   = t-foinv.price-decimal
        double-currency = t-foinv.double-currency
        change-date     = t-foinv.change-date
        foreign-rate    = t-foinv.foreign-rate
        exchg-rate      = t-foinv.exchg-rate
        curr-local      = t-foinv.curr-local
        curr-foreign    = t-foinv.curr-foreign
        lvAnzVat        = t-foinv.lvAnzVat
        b-title         = t-foinv.b-title
        artikel-str     = t-foinv.artikel-str
        p-219           = t-foinv.p-219
        p-199           = t-foinv.p-199
        p-145           = t-foinv.p-145
        p-242           = t-foinv.p-242
        p-60            = t-foinv.p-60
        p-251           = t-foinv.p-251
        p-2313          = t-foinv.p-2313
        p-1116          = t-foinv.p-1116
        p-685           = t-foinv.p-685
        avail-brief685  = t-foinv.avail-brief685
        p-173           = t-foinv.p-173
        p-2314          = t-foinv.p-2314
        p-83            = t-foinv.p-83
        p-497           = t-foinv.p-497
        p-120           = t-foinv.p-120
        avail-brief497  = t-foinv.avail-brief497
        p-1086          = t-foinv.p-1086
    .
    IF NUM-ENTRIES(t-foinv.ext-char, ";") GT 1  THEN
    ASSIGN
        cash-refund-str = "," + ENTRY(2, t-foinv.ext-char, ";") + ","
        rebate-str      = "," + ENTRY(3, t-foinv.ext-char, ";") + "," 
        cash-refund-str = REPLACE(cash-refund-str," ","")
        rebate-str      = REPLACE(rebate-str," ", "")
        rebate-str      = REPLACE(rebate-str,";", "") NO-ERROR
    .
END.
