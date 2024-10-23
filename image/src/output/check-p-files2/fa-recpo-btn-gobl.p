
DEFINE TEMP-TABLE op-list       LIKE fa-op
    FIELD counter AS INTEGER.


DEFINE INPUT PARAMETER TABLE FOR op-list.
DEFINE INPUT PARAMETER docu-nr      AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER billdate     AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER supplier-nr  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER supp-name    AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER del-note     AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER order-nr     AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER allowclose  AS LOGICAL INITIAL YES.

DEFINE VARIABLE art-nr AS INTEGER NO-UNDO.
DEFINE VARIABLE qty    AS INTEGER NO-UNDO.
DEFINE VARIABLE price  AS DECIMAL NO-UNDO.
DEFINE VARIABLE amount AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-amount  AS DECIMAL NO-UNDO.

t-amount = 0. 

FOR EACH op-list : 
    ASSIGN  art-nr      = op-list.nr 
            qty         = op-list.anzahl 
            price       = op-list.einzelpreis 
            amount      = op-list.warenwert 
            t-amount    = t-amount + op-list.warenwert. 
   
    RUN create-fa-op. 
    
    FIND FIRST fa-order WHERE fa-order.order-nr = docu-nr AND fa-order.fa-nr = op-list.nr AND 
        fa-order.fa-pos = op-list.counter NO-LOCK NO-ERROR.
    IF AVAILABLE fa-order THEN
    DO:

        FIND CURRENT fa-order EXCLUSIVE-LOCK.

        fa-order.delivered-qty    = fa-order.delivered-qty + qty.             
        fa-order.delivered-date   = billdate.            
        fa-order.delivered-price  = op-list.einzelpreis.          
        fa-order.delivered-amount = fa-order.delivered-amount + op-list.warenwert.
        fa-order.last-ID          = user-init.

        FIND CURRENT fa-order NO-LOCK.
    END.
END.

RUN close-po.
IF supplier-nr NE 0 AND t-amount NE 0 THEN RUN create-ap. 

PROCEDURE create-fa-op :

    DEFINE VARIABLE next-date AS DATE. 
    DEFINE VARIABLE next-mon AS INTEGER. 
    DEFINE VARIABLE next-yr AS INTEGER.

    DO transaction: 
        FIND FIRST mathis WHERE mathis.nr = art-nr EXCLUSIVE-LOCK. 
        mathis.price = price. 
        mathis.supplier = supp-name  . 
        mathis.datum = billdate. 
        FIND CURRENT mathis NO-LOCK. 
 

        FIND FIRST fa-artikel WHERE fa-artikel.nr = art-nr EXCLUSIVE-LOCK. 
        fa-artikel.lief-nr = supplier-nr. 
        fa-artikel.posted = YES. 
        fa-artikel.anzahl = fa-artikel.anzahl + qty. 
        fa-artikel.warenwert = amount /*fa-artikel.warenwert +*/  . 
        fa-artikel.book-wert = amount /*fa-artikel.book-wert +*/ . 

        /* Malik 
            FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = art-nr NO-LOCK NO-ERROR.

            IF AVAILABLE queasy AND queasy.date1 NE ? THEN
            DO:
                next-mon = month(queasy.date1) + 1. 
                next-yr = year(queasy.date1). 
                IF next-mon = 13 THEN 
                DO: 
                    next-mon = 1. 
                    next-yr = next-yr + 1. 
                END.    

                next-date = DATE(next-mon, 1, next-yr) - 1. 
        
                FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
                IF day(queasy.date1) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
                ELSE 
                DO: 
                    /*
                    next-mon = next-mon + 1. 
                    IF next-mon = 13 THEN 
                    DO: 
                        next-mon = 1. 
                        next-yr = next-yr + 1. 
                    END. 

                    next-date = DATE(next-mon, 1, next-yr) - 1. 
                    fa-artikel.next-depn = next-date. 
                    */
                    fa-artikel.next-depn = next-date. 
                END. 

                IF queasy.date1 LT TODAY THEN 
                DO:
                    next-mon = month(TODAY) + 1. 
                    next-yr = year(TODAY). 
                    IF next-mon = 13 THEN 
                    DO: 
                        next-mon = 1. 
                        next-yr = next-yr + 1. 
                    END.    

                    next-date = DATE(next-mon, 1, next-yr) - 1. 
                    fa-artikel.next-depn = next-date.

                    queasy.date1 = DATE(month(TODAY), day(queasy.date1), year(TODAY)).

                END.

            END.
            ELSE
            DO:
                next-mon = month(billdate) + 1. 
                next-yr = year(billdate). 
                IF next-mon = 13 THEN 
                DO: 
                    next-mon = 1. 
                    next-yr = next-yr + 1. 
                END. 
        
                next-date = DATE(next-mon, 1, next-yr) - 1. 
        
                FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
                IF day(billdate) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
                ELSE 
                DO: 
                    next-mon = next-mon + 1. 
                    IF next-mon = 13 THEN 
                    DO: 
                        next-mon = 1. 
                        next-yr = next-yr + 1. 
                    END. 
        
                    next-date = DATE(next-mon, 1, next-yr) - 1. 
                    fa-artikel.next-depn = next-date. 
                END. 
            END.
        */

        FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = art-nr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.date1 NE ? THEN
        DO:
            next-mon = month(queasy.date1) + 1. 
            next-yr = year(queasy.date1). 
            IF next-mon = 13 THEN 
            DO: 
                next-mon = 1. 
                next-yr = next-yr + 1. 
            END.    

            next-date = DATE(next-mon, 1, next-yr) - 1. 
    
            FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
            IF day(queasy.date1) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
            ELSE 
            DO: 
                fa-artikel.next-depn = next-date. 
            END. 

            IF queasy.date1 LT TODAY THEN 
            DO:
                next-mon = month(TODAY) + 1. 
                next-yr = year(TODAY). 
                IF next-mon = 13 THEN 
                DO: 
                    next-mon = 1. 
                    next-yr = next-yr + 1. 
                END.    

                next-date = DATE(next-mon, 1, next-yr) - 1. 
                fa-artikel.next-depn = next-date.

                queasy.date1 = DATE(month(TODAY), day(queasy.date1), year(TODAY)).

            END.
            /* Fix fa-op not created becuse FIND CURRENT queasy FAILED by Oscar (17 Oktober 2024) - C11EAE */         
            FIND CURRENT queasy NO-LOCK.
        END.
        ELSE
        DO:
            next-mon = month(billdate) + 1. 
            next-yr = year(billdate). 
            IF next-mon = 13 THEN 
            DO: 
                next-mon = 1. 
                next-yr = next-yr + 1. 
            END. 
    
            next-date = DATE(next-mon, 1, next-yr) - 1. 
     
            FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
            IF day(billdate) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
            ELSE 
            DO: 
                next-mon = next-mon + 1. 
                IF next-mon = 13 THEN 
                DO: 
                    next-mon = 1. 
                    next-yr = next-yr + 1. 
                END. 
    
                next-date = DATE(next-mon, 1, next-yr) - 1. 
                fa-artikel.next-depn = next-date. 
            END. 
        END.
        
    /*
        next-mon = month(billdate) + 1. 
        next-yr = year(billdate). 
        IF next-mon = 13 THEN 
        DO: 
            next-mon = 1. 
            next-yr = next-yr + 1. 
        END. 

        next-date = DATE(next-mon, 1, next-yr) - 1. 
 
        FIND FIRST htparam WHERE paramnr = 880 NO-LOCK. 
        IF day(billdate) LE htparam.finteger THEN fa-artikel.next-depn = next-date. 
        ELSE 
        DO: 
            next-mon = next-mon + 1. 
            IF next-mon = 13 THEN 
            DO: 
                next-mon = 1. 
                next-yr = next-yr + 1. 
            END. 

            next-date = DATE(next-mon, 1, next-yr) - 1. 
            fa-artikel.next-depn = next-date. 
        END. 
    */    
    
        /* FIND CURRENT queasy NO-LOCK. */
        FIND CURRENT fa-artikel NO-LOCK. 
        
        create fa-op. 
        ASSIGN  fa-op.nr            = mathis.nr 
                fa-op.opart         = 1 
                fa-op.datum         = billdate
                fa-op.zeit          = TIME 
                fa-op.anzahl        = qty 
                fa-op.einzelpreis   = price 
                fa-op.warenwert     = amount 
                fa-op.id            = user-init 
                fa-op.lscheinnr     = del-note 
                fa-op.docu-nr       = order-nr 
                fa-op.lief-nr       = supplier-nr 
                fa-op.loeschflag    = 0.

    END. 
END.

PROCEDURE close-po :

    FOR EACH fa-order WHERE fa-order.order-nr = order-nr NO-LOCK:
        IF allowclose = YES THEN
        DO:
            IF fa-order.order-qty = fa-order.delivered-qty THEN
            DO:
                allowclose = YES.
            END.
            ELSE
            DO:
                allowclose = NO.
            END.
        END.
        ELSE
        DO:
            allowclose = NO.
        END.
    END.
    
    IF allowclose = YES THEN
    DO:
        FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = order-nr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE fa-ordheader THEN
        DO:
            ASSIGN fa-ordheader.activeflag = 1
                fa-ordheader.close-by = user-init
                fa-ordheader.close-date = billdate
                fa-ordheader.close-time = TIME.
        END.
        
        FIND CURRENT fa-ordheader NO-LOCK.
    
    END.
END.

PROCEDURE create-ap :
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

    create l-kredit. 
    ASSIGN  l-kredit.name       = order-nr
            l-kredit.lief-nr    = supplier-nr
            l-kredit.lscheinnr  = del-note 
            l-kredit.rgdatum    = billdate
            l-kredit.datum      = ? 
            l-kredit.saldo      = t-amount 
            l-kredit.ziel       = 30 
            l-kredit.netto      = t-amount 
            l-kredit.bediener-nr = bediener.nr
            l-kredit.betriebsnr   = 2.  
 
    create ap-journal. 
    ASSIGN  ap-journal.lief-nr      = supplier-nr
            ap-journal.docu-nr      = order-nr
            ap-journal.lscheinnr    = del-note 
            ap-journal.rgdatum      = billdate 
            ap-journal.saldo        = t-amount 
            ap-journal.netto        = t-amount 
            ap-journal.userinit     = bediener.userinit
            ap-journal.zeit         = time. 
END.
