DEFINE TEMP-TABLE fa-budget-realization                      
    FIELD asset             AS CHAR
    FIELD asset-date        AS DATE
    FIELD descrip-str       AS CHAR
    FIELD account-no        AS CHAR    
    FIELD price-str         AS CHAR
    FIELD anzahl-str        AS CHAR    
    FIELD amount-str        AS CHAR 
    FIELD budget-str        AS CHAR    
    FIELD variance-str      AS CHAR
    FIELD budget-date       AS DATE    
    FIELD order-number      LIKE fa-op.docu-nr
    FIELD budget-number     AS CHAR
    FIELD tot-budget-item   AS CHAR
    FIELD COA               LIKE fa-artikel.fibukonto
    FIELD budget-amount     AS CHAR 
    FIELD asset-loc         AS CHAR 
    FIELD asset-name        AS CHAR 
    FIELD asset-qty         AS CHAR 
    FIELD asset-price       AS CHAR 
    FIELD asset-amount      AS CHAR 
    FIELD payment-date      LIKE fa-ordheader.paymentdate
    . 

DEFINE TEMP-TABLE fix-asset-list
    FIELD nr-budget          AS INTEGER
    FIELD desc-budget        AS CHARACTER
    FIELD date-budget        AS DATE
    FIELD amount-budget      AS DECIMAL
    FIELD is-active-budget   AS LOGICAL
    FIELD safe-to-del-or-mod AS LOGICAL
    FIELD remain-budget      AS DECIMAL
.


DEFINE TEMP-TABLE payload-list
    FIELD from-date AS DATE
    FIELD to-date AS DATE.

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR fa-budget-realization.

DEFINE VARIABLE count-i              AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE period-qty           AS INTEGER NO-UNDO.
DEFINE VARIABLE start-jan            AS DATE NO-UNDO.
DEFINE VARIABLE period-amount        AS DECIMAL NO-UNDO.
DEFINE VARIABLE period-budget        AS DECIMAL NO-UNDO.
DEFINE VARIABLE period-variance      AS DECIMAL NO-UNDO.
DEFINE VARIABLE nr-budget            AS CHARACTER NO-UNDO.
DEFINE VARIABLE fa-artnr             AS INTEGER NO-UNDO.
    
DEFINE VARIABLE grand-total-qty      AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE grand-total-amount   AS DECIMAL NO-UNDO INITIAL 0.
DEFINE VARIABLE grand-total-budget   AS DECIMAL NO-UNDO INITIAL 0.
DEFINE VARIABLE grand-total-variance AS DECIMAL NO-UNDO INITIAL 0.

DEFINE VARIABLE tot-qty-item AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-price-item AS DECIMAL NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-amount-item AS DECIMAL NO-UNDO INITIAL 0.


FOR EACH queasy WHERE queasy.key EQ 324 NO-LOCK:
    CREATE fix-asset-list.
    
    ASSIGN 
        fix-asset-list.nr-budget          = queasy.number1
        fix-asset-list.desc-budget        = queasy.char1
        fix-asset-list.date-budget        = queasy.date1
        fix-asset-list.amount-budget      = queasy.deci1
        fix-asset-list.is-active-budget   = queasy.logi1
    .
END.


FIND FIRST payload-list.
RUN create-budget-realization.

/*********************************************************************************************
                                          PROCEDURES
*********************************************************************************************/

PROCEDURE create-budget-realization:
    DEFINE VARIABLE budget-date-last AS DATE.
    DEFINE VARIABLE budget-nr-last AS INTEGER.
    DEFINE VARIABLE budget-desc-last AS CHARACTER.
    DEFINE VARIABLE tmp-budget-number AS CHARACTER.

    DEFINE VARIABLE tot-qty AS INTEGER.
    DEFINE VARIABLE tot-price AS DECIMAL.
    DEFINE VARIABLE tot-amount AS DECIMAL.

    FOR EACH fa-order WHERE fa-order.ActiveReason NE "0" 
        AND fa-order.ActiveReason NE ""
        AND fa-order.ActiveReason NE ? NO-LOCK,
        EACH fa-op WHERE fa-op.loeschflag LE 1 
        AND fa-op.opart EQ 1 
        AND fa-op.anzahl GT 0
        AND fa-op.docu-nr EQ fa-order.Order-Nr
        AND fa-op.datum GE payload-list.from-date 
        AND fa-op.datum LE payload-list.to-date NO-LOCK,
        FIRST fix-asset-list WHERE STRING(fix-asset-list.nr-budget) EQ fa-order.ActiveReason NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK,
        FIRST fa-ordheader WHERE fa-ordheader.order-nr EQ fa-op.docu-nr NO-LOCK
        BY fa-order.ActiveReason BY fa-op.nr BY fa-op.datum:
        
        count-i = count-i + 1.
        IF fa-order.ActiveReason NE nr-budget THEN
        DO:
            IF nr-budget NE "" THEN
            DO:
                CREATE fa-budget-realization.
                ASSIGN
                    fa-budget-realization.anzahl-str        = STRING(period-qty, "->>,>>>,>>9")
                    fa-budget-realization.amount-str        = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-realization.variance-str      = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
                    /* fa-budget-realization.budget-str        = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99") */
                    /* fa-budget-realization.budget-date       = fix-asset-list.date-budget */
                    fa-budget-realization.descrip-str       = "T O T A L"
                    fa-budget-realization.account-no        = ""
                    /* fa-budget-realization.budget-number     = STRING(fix-asset-list.nr-budget, ">,>>9") */
                    /* additional */
                    fa-budget-realization.asset-qty         = STRING(tot-qty-item)
                    fa-budget-realization.asset-price       = STRING(tot-price-item, "->>,>>>,>>>,>>>,>>9.99")
                    fa-budget-realization.asset-amount      = STRING(tot-amount-item, "->>,>>>,>>>,>>>,>>9.99")
                .
                grand-total-qty      = grand-total-qty      + period-qty.
                grand-total-amount   = grand-total-amount   + period-amount.
                grand-total-budget   = grand-total-budget   + period-budget.
                grand-total-variance = grand-total-variance + period-variance.
                CREATE fa-budget-realization.
                period-budget   = 0.
                period-qty      = 0. 
                period-amount   = 0.
                period-variance = 0.
                tot-qty-item = 0.
                tot-price-item = 0.
                tot-amount-item = 0.
            END.
            period-budget = fix-asset-list.amount-budget.
            CREATE fa-budget-realization.
            ASSIGN 
                fa-budget-realization.descrip-str       = STRING(fix-asset-list.nr-budget) + " - " + fix-asset-list.desc-budget
                fa-budget-realization.account-no        = ""
                fa-budget-realization.budget-number     = STRING(fix-asset-list.nr-budget, ">,>>9")
                fa-budget-realization.budget-date       = fix-asset-list.date-budget
                fa-budget-realization.budget-str        = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
            .
            nr-budget        = fa-order.ActiveReason.
            budget-date-last = fix-asset-list.date-budget.
            budget-nr-last   = fix-asset-list.nr-budget.
        END.
        IF fa-artnr NE fa-op.nr THEN
        DO:
            CREATE fa-budget-realization.
            ASSIGN 
                /* fa-budget-realization.descrip-str    = mathis.NAME */ 
                fa-budget-realization.asset          = mathis.asset 
                fa-budget-realization.account-no     = fa-artikel.fibukonto
                fa-budget-realization.asset-date     = fa-op.datum
                fa-budget-realization.price-str      = STRING(fa-op.einzelpreis, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-realization.anzahl-str     = STRING(fa-op.anzahl, "->>,>>>,>>9")
                fa-budget-realization.amount-str     = STRING(fa-op.warenwert, "->>>,>>>,>>>,>>>,>>9.99")
                /* fa-budget-realization.order-number   = fa-op.docu-nr */
                /* DETAIL */
                fa-budget-realization.COA = fa-artikel.fibukonto             
                /* fa-budget-realization.budget-number = STRING(fix-asset-list.nr-budget, ">,>>9") */
                /* fa-budget-realization.budget-decs    = mathis.NAME */
                fa-budget-realization.budget-amount  = STRING(fix-asset-list.amount-budget)
                fa-budget-realization.order-number   = fa-op.docu-nr
                fa-budget-realization.asset-loc      = mathis.location
                fa-budget-realization.asset-name     = mathis.NAME
                fa-budget-realization.asset-qty      = STRING(fa-order.order-qty)
                fa-budget-realization.asset-price    = STRING(fa-order.order-price, "->>,>>>,>>>,>>>,>>9.99")
                fa-budget-realization.asset-amount   = STRING(fa-order.order-amount, "->>,>>>,>>>,>>>,>>9.99")
                fa-budget-realization.payment-date   = fa-ordheader.paymentdate
            .
            period-qty = period-qty + fa-op.anzahl.
            period-amount = period-amount + fa-op.warenwert.
            period-variance = (period-budget - period-amount).
            tot-qty-item = tot-qty-item + fa-order.order-qty.
            tot-price-item = tot-price-item + fa-order.order-price.
            tot-amount-item = tot-amount-item + fa-order.order-amount.
            fa-artnr = fa-op.nr.
        END.
    END.

    IF count-i GT 0 THEN
    DO:

        CREATE fa-budget-realization.
        ASSIGN
            fa-budget-realization.anzahl-str        = STRING(period-qty, "->>,>>>,>>9")
            fa-budget-realization.amount-str        = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-realization.variance-str      = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
            /* fa-budget-realization.budget-str        = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99") */
            /* fa-budget-realization.budget-date       = budget-date-last */
            fa-budget-realization.descrip-str       = "T O T A L"
            /* fa-budget-realization.asset             = "T O T A L"
            fa-budget-realization.order-number      = "T O T A L" */
            /* Additional */
            fa-budget-realization.asset-qty         = STRING(tot-qty-item)
            fa-budget-realization.asset-price       = STRING(tot-price-item, "->>,>>>,>>>,>>>,>>9.99")
            fa-budget-realization.asset-amount      = STRING(tot-amount-item, "->>,>>>,>>>,>>>,>>9.99")
        .
        CREATE fa-budget-realization.
            grand-total-qty      = grand-total-qty      + period-qty.
            grand-total-amount   = grand-total-amount   + period-amount.
            grand-total-budget   = grand-total-budget   + period-budget.
            grand-total-variance = grand-total-variance + period-variance.

            CREATE fa-budget-realization.

            ASSIGN
                fa-budget-realization.anzahl-str        = STRING(grand-total-qty, "->>,>>>,>>9")
                /* fa-budget-realization.amount-str        = STRING(grand-total-amount, "->>>,>>>,>>>,>>>,>>9.99") */
                fa-budget-realization.asset-amount        = STRING(grand-total-amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-realization.variance-str      = STRING(grand-total-variance, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-realization.budget-str        = STRING(grand-total-budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-realization.descrip-str       = "GRAND TOTAL"
            .
    END.
END PROCEDURE. 
