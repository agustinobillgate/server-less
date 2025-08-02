DEFINE TEMP-TABLE tmp-tbl-data
    FIELD fa-nr             AS INTEGER
    FIELD NAME              AS CHARACTER
    FIELD asset             AS CHARACTER
    FIELD order-qty         AS INTEGER
    FIELD order-price       AS DECIMAL
    FIELD order-amount      AS DECIMAL
    FIELD delivered-qty     AS INTEGER
    FIELD delivered-date    AS DATE
    FIELD last-user         AS CHARACTER.

DEFINE INPUT PARAMETER docu-nr AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tmp-tbl-data.

DEFINE TEMP-TABLE disclist 
    FIELD fa-recid AS INTEGER 
    FIELD price0   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999" LABEL "Unit-Price" 
    FIELD brutto   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>>,>>9.999" LABEL "Gross Amount" 
    FIELD disc     AS DECIMAL FORMAT ">9.99" LABEL "Disc" 
    FIELD disc2    AS DECIMAL FORMAT ">9.99" LABEL "Disc2" 
    FIELD vat      AS DECIMAL FORMAT ">9.99" LABEL "VAT". 

DEFINE TEMP-TABLE s-order LIKE fa-order
    FIELD Last-user AS CHAR FORMAT "x(30)".

DEFINE VARIABLE temp-last AS CHAR FORMAT "x(30)".

/******************* Main Logic **************************/

FOR EACH fa-order 
    WHERE fa-order.order-nr = docu-nr 
      AND fa-order.fa-pos GT 0 
      AND fa-order.activeflag = 0 
    NO-LOCK 
    BY fa-order.fa-pos:

    /* Pisahkan FIND FIRST mathis */
    FIND FIRST mathis WHERE mathis.nr = fa-order.fa-nr NO-LOCK NO-ERROR.

    /* Pisahkan FIND FIRST bediener */
    FIND FIRST bediener WHERE bediener.userinit = fa-order.last-id NO-LOCK NO-ERROR.

    IF AVAILABLE bediener THEN
        temp-last = bediener.username.
    ELSE
        temp-last = "".  

    CREATE s-order. 
    ASSIGN 
        s-order.order-nr      = fa-order.order-nr 
        s-order.statflag      = RECID(l-order) 
        s-order.fa-nr         = fa-order.fa-nr 
        s-order.order-qty     = fa-order.order-qty 
        s-order.activeflag    = fa-order.activeflag 
        s-order.order-price   = fa-order.order-price 
        s-order.order-amount  = fa-order.order-amount 
        s-order.activereason  = fa-order.activereason 
        s-order.delivered-qty = fa-order.delivered-qty
        s-order.delivered-date = fa-order.delivered-date
        s-order.fa-pos        = fa-order.fa-pos
        s-order.last-id       = fa-order.last-id
        s-order.last-user     = temp-last.  

    CREATE disclist. 
    ASSIGN 
        disclist.fa-recid = s-order.fa-pos
        disclist.price0   = fa-order.order-price 
                          / (1 - fa-order.discount1 * 0.01) 
                          / (1 - fa-order.discount2 * 0.01) 
                          / (1 + fa-order.vat * 0.01)
        disclist.brutto   = disclist.price0 * fa-order.order-amount
        disclist.disc     = fa-order.discount1
        disclist.disc2    = fa-order.discount2
        disclist.vat      = fa-order.vat.
END.

/* Output Loop */
FOR EACH s-order WHERE s-order.order-nr = docu-nr NO-LOCK:

    /* Pisahkan FIND FIRST disclist */
    FIND FIRST disclist 
        WHERE disclist.fa-recid = s-order.fa-pos 
        NO-LOCK NO-ERROR.

    /* Pisahkan FIND FIRST mathis */
    FIND FIRST mathis 
        WHERE mathis.nr = s-order.fa-nr 
        NO-LOCK NO-ERROR.

    IF AVAILABLE disclist AND AVAILABLE mathis THEN DO:
        CREATE tmp-tbl-data.
        ASSIGN
            tmp-tbl-data.fa-nr          = s-order.fa-nr         
            tmp-tbl-data.NAME           = mathis.NAME           
            tmp-tbl-data.asset          = mathis.asset          
            tmp-tbl-data.order-qty      = s-order.order-qty     
            tmp-tbl-data.order-price    = s-order.order-price   
            tmp-tbl-data.order-amount   = s-order.order-amount  
            tmp-tbl-data.delivered-qty  = s-order.delivered-qty 
            tmp-tbl-data.delivered-date = s-order.delivered-date
            tmp-tbl-data.last-user      = s-order.last-user.
    END.
END.
