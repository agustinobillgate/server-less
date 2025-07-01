DEFINE TEMP-TABLE stockin-list 
    FIELD dDate     AS DATE                         COLUMN-LABEL "Date" 
    FIELD iSt       AS INTEGER FORMAT "99"          COLUMN-LABEL "St" 
    FIELD sDocument AS CHARACTER FORMAT "X(12)"     COLUMN-LABEL "Document No" 
    FIELD iArticle  AS INTEGER FORMAT "9999999"     COLUMN-LABEL "Article" 
    FIELD sDesc     AS CHARACTER FORMAT "X(36)"     COLUMN-LABEL "Description" 
    FIELD dQuantity AS DECIMAL FORMAT "->>>,>>9.99" COLUMN-LABEL "Quantity" 
    FIELD sAmount   AS CHARACTER FORMAT "X(19)"     COLUMN-LABEL "Amount" 
    FIELD sSupplier AS CHARACTER FORMAT "X(20)"     COLUMN-LABEL "Supplier" 
    FIELD sDelNote  AS CHARACTER FORMAT "X(16)"     COLUMN-LABEL "Delivery Note" 
    FIELD sNote     AS CHARACTER FORMAT "X(8)" 
    FIELD iMark      AS INTEGER 
    FIELD ID        AS CHARACTER FORMAT "x(4)"      COLUMN-LABEL "ID"
    INDEX idx1 iMark iArticle dDate 
    INDEX idx2 iMark sDesc dDate 
    INDEX idx3 iMark sDocument dDate. 


DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-lager   AS INTEGER.
DEFINE INPUT PARAMETER to-lager     AS INTEGER.
DEFINE INPUT PARAMETER from-art     AS INTEGER.
DEFINE INPUT PARAMETER to-art       AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE       FOR stockin-list.
    

DEFINE VARIABLE note-str AS CHARACTER EXTENT 2 
    INITIAL ["        ", "Transfer"]                    NO-UNDO. 

DEFINE VARIABLE tot-anz     AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE tot-amount  AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE beg-date    AS DATE     NO-UNDO. 
DEFINE VARIABLE end-date    AS DATE     NO-UNDO. 

DEFINE VARIABLE show-price  AS LOGICAL  NO-UNDO. 
DEFINE VARIABLE long-digit  AS LOGICAL  NO-UNDO. 
DEFINE VARIABLE fdate       AS DATE     NO-UNDO.

/****************************************************************************/
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK NO-ERROR.
fdate = DATE(MONTH(htparam.fdate), 1, YEAR(htparam.fdate)).
beg-date = fdate - 1. 

ASSIGN  tot-anz     = 0 
        tot-amount  = 0 
        end-date    = beg-date. 

IF to-date LT beg-date THEN end-date = to-date. 

FOR EACH l-lager NO-LOCK WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager: 
    
    /*  calculate the incoming stocks within the given periods */ 
    IF from-date LE beg-date THEN 
    DO:
        FOR EACH l-ophis NO-LOCK WHERE l-ophis.lager-nr = l-lager.lager-nr AND 
        l-ophis.datum GE from-date AND l-ophis.datum LE end-date AND 
        l-ophis.artnr GE from-art AND l-ophis.artnr LE to-art AND l-ophis.op-art = 1, 
        FIRST l-artikel NO-LOCK WHERE l-artikel.artnr = l-ophis.artnr 
        BY l-ophis.artnr BY l-ophis.datum: 
        
            CREATE stockin-list. 
            ASSIGN  tot-anz                 = tot-anz + l-ophis.anzahl 
                    tot-amount              = tot-amount + l-ophis.warenwert 
                    stockin-list.dDate      = l-ophis.datum 
                    stockin-list.iSt        = l-ophis.lager-nr 
                    stockin-list.iArticle   = l-artikel.artnr 
                    stockin-list.sDocument  = l-ophis.docu-nr 
                    stockin-list.sDesc      = l-artikel.bezeich 
                    stockin-list.dQuantity  = l-ophis.anzahl 
                    stockin-list.sNote      = note-str[l-ophis.op-art] 
                    stockin-list.sDelNote   = SUBSTRING(l-ophis.lscheinnr,MAX(1, LENGTH(l-ophis.lscheinnr) - 15), 16). 
    
            IF show-price THEN ASSIGN stockin-list.sAmount = 
                IF long-digit THEN 
                    STRING(l-ophis.warenwert, "   ->>>,>>>,>>>,>>9") 
                ELSE 
                    STRING(l-ophis.warenwert, "->>>,>>>,>>>,>>9.99"). 
        
            IF l-ophis.lief-nr NE 0 THEN 
            DO: 
                FIND FIRST l-lieferant NO-LOCK WHERE l-lieferant.lief-nr = l-ophis.lief-nr. 
                IF AVAILABLE l-lieferant THEN ASSIGN stockin-list.sSupplier = l-lieferant.firma. 
            END. 
        END.    
    END. 
    
    FOR EACH l-op NO-LOCK WHERE l-op.lager-nr = l-lager.lager-nr AND 
        l-op.datum GE from-date AND l-op.datum LE to-date AND l-op.artnr GE from-art AND 
        l-op.artnr LE to-art AND l-op.loeschflag LT 2 AND l-op.op-art = 1, 
        /* AND l-op.herkunftflag NE 2  this is  direct issue USE-INDEX artopart_ix  */ 
        FIRST l-artikel NO-LOCK WHERE l-artikel.artnr = l-op.artnr 
        BY l-op.artnr BY l-op.datum: 
        
            CREATE stockin-list. 
            ASSIGN  tot-anz                 = tot-anz + l-op.anzahl 
                    tot-amount              = tot-amount + l-op.warenwert 
                    stockin-list.dDate      = l-op.datum 
                    stockin-list.iSt        = l-op.lager-nr 
                    stockin-list.iArticle   = l-artikel.artnr 
                    stockin-list.sDocument  = l-op.docu-nr 
                    stockin-list.sDesc      = l-artikel.bezeich 
                    stockin-list.dQuantity  = l-op.anzahl 
                    stockin-list.sNote      = note-str[l-op.op-art] 
                    stockin-list.sDelNote   = SUBSTRING(l-op.lscheinnr,MAX(1, LENGTH(l-op.lscheinnr) - 15), 16) 
                    stockin-list.iMark      = 0. 
        
            RUN add-id.
            IF show-price THEN ASSIGN stockin-list.sAmount = 
                IF long-digit THEN STRING(l-op.warenwert, "   ->>>,>>>,>>>,>>9") 
                ELSE STRING(l-op.warenwert, "->>>,>>>,>>>,>>9.99"). 
            IF l-op.lief-nr NE 0 THEN 
            DO: 
                FIND FIRST l-lieferant NO-LOCK WHERE l-lieferant.lief-nr = l-op.lief-nr. 
                IF AVAILABLE l-lieferant THEN ASSIGN stockin-list.sSupplier = l-lieferant.firma. 
            END. 
    END. 
END. 

/* Create TOTAL line */ 
CREATE stockin-list. 
ASSIGN  stockin-list.sDesc       = "T O T A L" 
        stockin-list.dQuantity   = tot-anz 
        stockin-list.iMark       = 1. 

IF show-price THEN ASSIGN stockin-list.sAmount = 
    IF long-digit THEN STRING(tot-amount, "   ->>>,>>>,>>>,>>9") 
    ELSE STRING(tot-amount, "->>>,>>>,>>>,>>9.99"). 

/*********************************************************************************/
PROCEDURE add-id:
    DEFINE BUFFER usr FOR bediener.

    FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN stockin-list.ID = usr.userinit.
    ELSE stockin-list.ID = "??".
END.
