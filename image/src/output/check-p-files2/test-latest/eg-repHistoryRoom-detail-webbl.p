/*FD Dec 17, 2020 => BL for vhpweb Based convert STR to Temp-Table*/

DEFINE TEMP-TABLE t-hisroom-line-cost    
    FIELD reqno     AS CHAR FORMAT "x(8)"
    FIELD flag      AS CHAR 
    FIELD artno     AS CHAR FORMAT "x(8)"
    FIELD bezeich   AS CHAR FORMAT "x(48)"
    FIELD qty       AS CHAR FORMAT "x(8)"
    FIELD price     AS CHAR FORMAT "x(19)"
    FIELD tot-price AS CHAR FORMAT "x(19)"
.

DEFINE TEMP-TABLE t-hisroom-line-vendor    
    FIELD reqno         AS CHAR FORMAT "x(8)"
    FIELD flag          AS CHAR 
    FIELD outsource     AS CHAR FORMAT "x(8)"
    FIELD vendor-nm     AS CHAR FORMAT "x(48)"
    FIELD startdate     AS CHAR FORMAT "x(10)"
    FIELD finishdate    AS CHAR FORMAT "x(10)"        
    FIELD price         AS CHAR FORMAT "x(19)"    
.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER reqno AS INT.

DEFINE OUTPUT PARAMETER tot-cost AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER tot-vend AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER TABLE FOR t-hisroom-line-cost.
DEFINE OUTPUT PARAMETER TABLE FOR t-hisroom-line-vendor.

DEFINE BUFFER tbuff FOR l-artikel.

DEFINE VARIABLE tot AS DECIMAL.
DEFINE VARIABLE curr-tot AS DECIMAL.

IF case-type EQ 1 THEN RUN create-artikel-cost.
ELSE RUN create-vendor-cost.

/*****************************************************************************************/
PROCEDURE create-artikel-cost:
    DEFINE VARIABLE itotal      AS DECIMAL.   

    FOR EACH t-hisroom-line-cost:
        DELETE t-hisroom-line-cost.
    END.         
               
    FIND FIRST eg-queasy WHERE eg-queasy.KEY EQ 1 AND eg-queasy.reqnr EQ reqno NO-LOCK NO-ERROR.
    IF AVAILABLE eg-queasy THEN
    DO:  
        FOR EACH eg-queasy WHERE eg-queasy.KEY EQ 1 AND eg-queasy.reqnr EQ reqno 
            NO-LOCK BY eg-queasy.stock-nr:

            FIND FIRST tbuff WHERE tbuff.artnr EQ eg-queasy.stock-nr NO-LOCK NO-ERROR.
            IF AVAILABLE tbuff THEN
            DO:
                itotal  = eg-queasy.deci1 * eg-queasy.price.                   

                CREATE t-hisroom-line-cost.
                ASSIGN                     
                    t-hisroom-line-cost.reqno       = STRING(reqno, "->>>>>>9")
                    t-hisroom-line-cost.flag        = "1"
                    t-hisroom-line-cost.artno       = STRING(eg-queasy.stock-nr, "9999999")
                    t-hisroom-line-cost.bezeich     = tbuff.bezeich
                    t-hisroom-line-cost.qty         = STRING(eg-queasy.deci1 ,"->>>>>>9")
                    t-hisroom-line-cost.price       = STRING(eg-queasy.price, "->>>,>>>,>>>,>>9.99")
                    t-hisroom-line-cost.tot-price   = STRING(itotal , "->>>,>>>,>>>,>>9.99")
                .
            END. 
            tot = tot + itotal.            
        END.        
    END.

    IF tot NE 0 THEN
    DO:
        tot-cost = STRING(tot, "->>>,>>>,>>>,>>9.99").   
        tot = 0.
    END.
END PROCEDURE.

PROCEDURE create-vendor-cost:
    DEFINE VARIABLE vendo-nm    AS CHAR.
    DEFINE VARIABLE start-date  AS CHAR.
    DEFINE VARIABLE finish-date AS CHAR.
    DEFINE VARIABLE itotal      AS DECIMAL.

    FOR EACH t-hisroom-line-vendor:
        DELETE t-hisroom-line-vendor.
    END.

    FIND FIRST eg-vperform WHERE eg-vperform.reqnr EQ reqno NO-LOCK NO-ERROR.
    IF AVAILABLE eg-vperform THEN
    DO:            
        FOR EACH eg-vperform WHERE eg-vperform.reqnr EQ reqno NO-LOCK BY eg-vperform.perform-nr:
            FIND FIRST eg-vendor WHERE eg-vendor.vendor-nr EQ eg-vperform.vendor-nr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-vendor THEN
            DO:
                vendo-nm = eg-vendor.bezeich.
            END.
            ELSE
            DO:
                vendo-nm = "Undefine".
            END.
            
            IF eg-vperform.startdate = ? THEN start-date = "-".
            ELSE start-date = STRING(eg-vperform.startdate, "99/99/99").

            IF eg-vperform.finishdate = ? THEN finish-date = "-".
            ELSE finish-date = STRING(eg-vperform.finishdate, "99/99/99").                

            CREATE t-hisroom-line-vendor.
            ASSIGN                                                                                 
                t-hisroom-line-vendor.reqno         = STRING(reqno, "->>>>>>9")    
                t-hisroom-line-vendor.flag          = "2"                    
                t-hisroom-line-vendor.outsource     = STRING(eg-vperform.perform-nr, "9999999")
                t-hisroom-line-vendor.vendor-nm     = vendo-nm
                t-hisroom-line-vendor.startdate     = start-date
                t-hisroom-line-vendor.finishdate    = finish-date   
                t-hisroom-line-vendor.price         = STRING(eg-vperform.price , "->>>,>>>,>>>,>>9.99")                
            .       

            tot = tot + eg-vperform.price.             
        END.                 
    END.

    IF tot NE 0 THEN
    DO:            
        tot-vend = STRING(tot, "->>>,>>>,>>>,>>9.99").
        tot = 0.
    END.     
END PROCEDURE.

