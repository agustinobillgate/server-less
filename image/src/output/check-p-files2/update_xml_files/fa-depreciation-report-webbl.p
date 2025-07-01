DEFINE TEMP-TABLE depreciation-asset
    FIELD COA            LIKE fa-grup.fibukonto
    FIELD order-date     LIKE fa-ordheader.Order-Date
    FIELD order-number   LIKE fa-ordheader.Order-Nr 
    FIELD desc1      LIKE mathis.name
    FIELD qty        AS CHAR /* LIKE fa-order.order-qty */
    FIELD price      AS CHAR /* LIKE fa-order.order-price */
    FIELD amount     AS CHAR /* LIKE fa-order.order-amount */
    FIELD depn-value AS CHAR /* LIKE fa-artikel.depn-wert */
    FIELD book-value AS CHAR /* LIKE fa-artikel.book-wert */
    FIELD acc-depn   AS CHAR /* LIKE fa-artikel.anz-depn */
    FIELD date-rcv   LIKE fa-ordheader.close-date
    FIELD first-depn LIKE fa-artikel.first-depn.


DEFINE TEMP-TABLE payload-list     
    FIELD from-date   AS DATE
    FIELD to-date     AS DATE.

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR depreciation-asset.

DEFINE VARIABLE tot-amount AS DECIMAL. 
DEFINE VARIABLE tot-depn-value AS DECIMAL. 
DEFINE VARIABLE tot-book-value AS DECIMAL. 
DEFINE VARIABLE tot-acc-depn AS INTEGER. 

FIND FIRST payload-list.

FOR EACH fa-ordheader WHERE fa-ordheader.order-date GE payload-list.from-date 
    AND fa-ordheader.order-date LE payload-list.to-date 
    AND fa-ordheader.activeflag EQ 1 
    NO-LOCK USE-INDEX datumactive:

    FOR EACH fa-order WHERE fa-order.order-nr EQ fa-ordheader.order-nr NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-order.fa-nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr NO-LOCK:
        
        CREATE depreciation-asset.
        ASSIGN
          depreciation-asset.COA          = fa-artikel.fibukonto
          depreciation-asset.order-date   = fa-ordheader.Order-Date
          depreciation-asset.order-number = fa-ordheader.Order-Nr
          depreciation-asset.desc1        = mathis.name
          depreciation-asset.qty          = STRING(fa-order.order-qty, "->,>>>,>>9") /* fa-order.order-qty */
          depreciation-asset.price        = STRING(fa-order.order-price, "->>,>>>,>>>,>>>,>>9.99")
          depreciation-asset.amount       = STRING(fa-order.order-amount, "->>,>>>,>>>,>>>,>>9.99")
          depreciation-asset.depn-value   = STRING(fa-artikel.depn-wert, ">>,>>>,>>>,>>9.99")
          depreciation-asset.book-value   = STRING(fa-artikel.book-wert, ">>,>>>,>>>,>>9.99")
          depreciation-asset.acc-depn     = STRING(fa-artikel.anz-depn, ">>9")
          depreciation-asset.date-rcv     = fa-ordheader.close-date
          depreciation-asset.first-depn   = fa-artikel.first-depn.
    
        tot-amount = tot-amount + fa-order.order-amount.
        tot-depn-value = tot-depn-value + fa-artikel.depn-wert.
        tot-book-value = tot-book-value + fa-artikel.book-wert. /**/
        tot-acc-depn = tot-acc-depn + fa-artikel.anz-depn.
    END.
END.
FIND FIRST depreciation-asset NO-ERROR.
IF AVAILABLE depreciation-asset THEN
DO:
    CREATE depreciation-asset.
    ASSIGN
        depreciation-asset.desc1        = "T O T A L"
        depreciation-asset.amount       = STRING(tot-amount, "->>,>>>,>>>,>>>,>>9.99")
        depreciation-asset.depn-value   = STRING(tot-depn-value, ">>,>>>,>>>,>>9.99")
        depreciation-asset.book-value   = STRING(tot-book-value, ">>,>>>,>>>,>>9.99")
        depreciation-asset.acc-depn     = STRING(tot-acc-depn, ">>9").
END.
