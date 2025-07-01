/*FD August 24, 2021 => BL EG Repair Item - View Detail For WEB*/
DEFINE TEMP-TABLE t-artikel-cost
    FIELD reqno AS CHAR FORMAT "x(10)"
    FIELD art-no AS CHAR FORMAT "x(10)"
    FIELD art-desc AS CHAR FORMAT "x(64)"
    FIELD art-qty AS CHAR FORMAT "x(11)"
    FIELD art-price AS CHAR FORMAT "x(19)"
    FIELD art-total AS CHAR FORMAT "x(19)"    
    FIELD tFlag AS CHAR 
.

DEFINE TEMP-TABLE t-vendor-cost
    FIELD reqno AS CHAR FORMAT "x(10)"
    FIELD vend-no AS CHAR FORMAT "x(10)"
    FIELD vend-desc AS CHAR FORMAT "x(64)"
    FIELD vend-start AS CHAR FORMAT "x(10)"
    FIELD vend-finish AS CHAR FORMAT "x(10)"
    FIELD vend-price AS CHAR FORMAT "x(19)"    
    FIELD tFlag AS CHAR 
.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER reqno AS INT.
DEFINE OUTPUT PARAMETER tot-artcost AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER tot-vendcost AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel-cost.
DEFINE OUTPUT PARAMETER TABLE FOR t-vendor-cost.

/* Testing
DEFINE VARIABLE case-type AS INT.
DEFINE VARIABLE reqno   AS INT.
DEFINE VARIABLE fdate   AS DATE.
DEFINE VARIABLE tdate   AS DATE.
DEFINE VARIABLE tot-artcost AS CHAR FORMAT "x(19)".
DEFINE VARIABLE tot-vendcost AS CHAR FORMAT "x(19)".

case-type = 1.
reqno = 47.
*/
DEFINE VARIABLE atotal  AS INTEGER.
DEFINE VARIABLE btotal  AS INTEGER.
DEFINE VARIABLE tot     AS DECIMAL.

DEFINE BUFFER tbuff FOR l-artikel.

IF case-type EQ 1 THEN RUN create-artikel-cost.
ELSE RUN create-vendor-cost.

PROCEDURE create-artikel-cost:
    DEFINE VARIABLE itotal  AS DECIMAL. 

    FOR EACH t-artikel-cost:
        DELETE t-artikel-cost.
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

                CREATE t-artikel-cost.
                ASSIGN
                    t-artikel-cost.reqno        = STRING(reqno, "->>>>>>>>9")
                    t-artikel-cost.art-no       = STRING(eg-queasy.stock-nr, "9999999")
                    t-artikel-cost.art-desc     = tbuff.bezeich
                    t-artikel-cost.art-qty      = STRING(eg-queasy.deci1 ,"->>>,>>9.99")
                    t-artikel-cost.art-price    = STRING(eg-queasy.price, "->>>,>>>,>>>,>>9.99")
                    t-artikel-cost.art-total    = STRING(itotal, "->>>,>>>,>>>,>>9.99")
                    t-artikel-cost.tFlag        = "1"
                .
            END.
            tot = tot + itotal.
        END.
    END.

    IF tot NE 0 THEN
    DO:
        tot-artcost = STRING(tot, "->>>,>>>,>>>,>>9.99").   
        tot = 0.
    END.
END PROCEDURE.

PROCEDURE create-vendor-cost:
    DEFINE VARIABLE vendo-nm    AS CHAR.
    DEFINE VARIABLE start-date  AS CHAR.
    DEFINE VARIABLE finish-date AS CHAR.
    DEFINE VARIABLE itotal      AS DECIMAL. 

    FOR EACH t-vendor-cost:
        DELETE t-vendor-cost.
    END.    
    
    FIND FIRST eg-vperform WHERE eg-vperform.reqnr EQ reqno NO-LOCK NO-ERROR.
    IF AVAILABLE eg-vperform THEN
    DO:
        FOR EACH eg-vperform WHERE eg-vperform.reqnr EQ reqno NO-LOCK BY eg-vperform.perform-nr:

            FIND FIRST eg-vendor WHERE eg-vendor.vendor-nr = eg-vperform.vendor-nr NO-LOCK NO-ERROR.
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

            CREATE t-vendor-cost.
            ASSIGN
                t-vendor-cost.reqno         = STRING(reqno, "->>>>>>>>9")
                t-vendor-cost.vend-no       = STRING(eg-vperform.perform-nr, "9999999")
                t-vendor-cost.vend-desc     = vendo-nm
                t-vendor-cost.vend-start    = start-date
                t-vendor-cost.vend-finish   = finish-date
                t-vendor-cost.vend-price    = STRING(eg-vperform.price, "->>>,>>>,>>>,>>9.99")
                t-vendor-cost.tFlag         = "2"
            .

            tot = tot + eg-vperform.price.
        END.
    END.

    IF tot NE 0 THEN
    DO:
        tot-vendcost = STRING(tot, "->>>,>>>,>>>,>>9.99").   
        tot = 0.
    END.
END PROCEDURE.
