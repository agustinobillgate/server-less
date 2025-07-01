/*FDL Fixed Asset Budget List F9131B 12/07/24*/ 
DEFINE TEMP-TABLE fa-budget-ytd                      
    FIELD asset             AS CHAR    
    FIELD descrip-str       AS CHAR
    FIELD account-no        AS CHAR    
    FIELD anzahl-str        AS CHAR        
    FIELD amount-str        AS CHAR    
    FIELD mtd-budget-str    AS CHAR    
    FIELD mtd-variance-str  AS CHAR
    FIELD anzahlytd-str     AS CHAR
    FIELD amountytd-str     AS CHAR
    FIELD ytd-budget-str    AS CHAR    
    FIELD ytd-variance-str  AS CHAR
    . 

DEFINE TEMP-TABLE fa-budget-period                      
    FIELD asset             AS CHAR
    FIELD asset-date        AS DATE
    FIELD descrip-str       AS CHAR
    FIELD account-no        AS CHAR    
    FIELD price-str         AS CHAR
    FIELD anzahl-str        AS CHAR    
    FIELD amount-str        AS CHAR 
    FIELD budget-str        AS CHAR    
    FIELD variance-str      AS CHAR
    FIELD budget-date       AS DATE     /* Dzikri 01B1DB */
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

DEFINE INPUT PARAMETER ytd-flag  AS LOGICAL.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER ytd-date  AS DATE.
DEFINE INPUT PARAMETER detailed  AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR fa-budget-ytd.
DEFINE OUTPUT PARAMETER TABLE FOR fa-budget-period.

DEFINE VARIABLE curr-fibu            AS CHARACTER NO-UNDO.
DEFINE VARIABLE fibu-formated        AS CHARACTER NO-UNDO.
DEFINE VARIABLE count-i              AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE t-mtd-qty            AS INTEGER NO-UNDO.
DEFINE VARIABLE t-ytd-qty            AS INTEGER NO-UNDO.
DEFINE VARIABLE period-qty           AS INTEGER NO-UNDO.
DEFINE VARIABLE start-jan            AS DATE NO-UNDO.
DEFINE VARIABLE mtd-budget           AS DECIMAL NO-UNDO.
DEFINE VARIABLE mtd-variance         AS DECIMAL NO-UNDO.
DEFINE VARIABLE ytd-budget           AS DECIMAL NO-UNDO.
DEFINE VARIABLE ytd-variance         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-mtd-amount         AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-ytd-amount         AS DECIMAL NO-UNDO.
DEFINE VARIABLE period-amount        AS DECIMAL NO-UNDO.
DEFINE VARIABLE period-budget        AS DECIMAL NO-UNDO.
DEFINE VARIABLE period-variance      AS DECIMAL NO-UNDO.
DEFINE VARIABLE it-exist             AS LOGICAL NO-UNDO.
DEFINE VARIABLE nr-budget            AS CHARACTER NO-UNDO.
DEFINE VARIABLE fa-artnr             AS INTEGER NO-UNDO.
    
DEFINE VARIABLE grand-total-qty      AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE grand-total-amount   AS DECIMAL NO-UNDO INITIAL 0.
DEFINE VARIABLE grand-total-budget   AS DECIMAL NO-UNDO INITIAL 0.
DEFINE VARIABLE grand-total-variance AS DECIMAL NO-UNDO INITIAL 0.

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

/* retrieve first fa-op.nr for looping */
FOR EACH fa-order WHERE fa-order.ActiveReason NE "0" 
AND fa-order.ActiveReason NE ""
AND fa-order.ActiveReason NE ? NO-LOCK,
EACH fa-op WHERE fa-op.loeschflag LE 1 
AND fa-op.opart EQ 1 
AND fa-op.anzahl GT 0
AND fa-op.docu-nr EQ fa-order.Order-Nr
AND fa-op.datum GE start-jan 
AND fa-op.datum LE ytd-date NO-LOCK,
FIRST fix-asset-list WHERE STRING(fix-asset-list.nr-budget) EQ fa-order.ActiveReason NO-LOCK,
FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK 
BY fa-order.ActiveReason BY fa-op.nr BY fa-op.datum:

    fa-artnr = fa-op.nr.
    LEAVE.
END.

IF ytd-flag THEN RUN create-budget-ytd.
ELSE RUN create-budget-period.

/*********************************************************************************************
                                          PROCEDURES
*********************************************************************************************/
PROCEDURE create-budget-ytd:
    DEFINE VARIABLE budget-date-last AS DATE.
    DEFINE VARIABLE budget-nr-last AS INTEGER.
    DEFINE VARIABLE budget-desc-last AS CHARACTER.
    
    start-jan = DATE(1,1,YEAR(ytd-date)).

    /* not used */
    /* 
    FOR EACH fa-op WHERE fa-op.loeschflag LE 1
        AND fa-op.datum GE start-jan AND fa-op.datum LE ytd-date NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
        FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp AND fa-grup.flag GT 0 NO-LOCK,
        FIRST gl-acct WHERE gl-acct.fibukonto EQ fa-artikel.fibukonto NO-LOCK 
        BY fa-artikel.fibukonto BY fa-op.datum:
        
        IF curr-fibu NE fa-artikel.fibukonto THEN
        DO:
            mtd-budget      = 0.
            ytd-budget      = 0.
            t-mtd-qty       = 0.
            t-mtd-amount    = 0.
            mtd-variance    = 0.
            t-ytd-qty       = 0. 
            t-ytd-amount    = 0.
            ytd-variance    = 0.

            RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu-formated).
            
            mtd-budget = gl-acct.budget[MONTH(ytd-date)].
            DO count-i = 1 TO MONTH(ytd-date):  
                ytd-budget = ytd-budget + gl-acct.budget[count-i]. 
            END.

            CREATE fa-budget-ytd.
            ASSIGN 
                fa-budget-ytd.descrip-str       = fa-grup.bezeich + " - " + fibu-formated
                fa-budget-ytd.account-no        = fa-artikel.fibukonto
                fa-budget-ytd.mtd-budget-str    = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-ytd.ytd-budget-str    = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                .
        END.

        IF MONTH(fa-op.datum) EQ MONTH(ytd-date) THEN
        DO:
            ASSIGN
                t-mtd-qty = t-mtd-qty + fa-op.anzahl
                t-mtd-amount = t-mtd-amount + fa-op.warenwert
                mtd-variance = (mtd-budget - t-mtd-amount)
                .
        END.
        t-ytd-qty = t-ytd-qty + fa-op.anzahl.
        t-ytd-amount = t-ytd-amount + fa-op.warenwert.
        ytd-variance = (ytd-budget - t-ytd-amount).

        ASSIGN
            fa-budget-ytd.anzahl-str        = STRING(t-mtd-qty, "->>,>>>,>>9")
            fa-budget-ytd.amount-str        = STRING(t-mtd-amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.mtd-variance-str  = STRING(mtd-variance, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.anzahlytd-str     = STRING(t-ytd-qty, "->>,>>>,>>9")
            fa-budget-ytd.amountytd-str     = STRING(t-ytd-amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.ytd-variance-str  = STRING(ytd-variance, "->>>,>>>,>>>,>>>,>>9.99")
            .

        curr-fibu = fa-artikel.fibukonto.
    END. */


    FOR EACH fa-order WHERE fa-order.ActiveReason NE "0" 
    AND fa-order.ActiveReason NE ""
    AND fa-order.ActiveReason NE ? NO-LOCK,
    EACH fa-op WHERE fa-op.loeschflag LE 1 
    AND fa-op.opart EQ 1 
    AND fa-op.anzahl GT 0
    AND fa-op.docu-nr EQ fa-order.Order-Nr
    AND fa-op.datum GE start-jan 
    AND fa-op.datum LE ytd-date NO-LOCK,
    FIRST fix-asset-list WHERE STRING(fix-asset-list.nr-budget) EQ fa-order.ActiveReason NO-LOCK,
    FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
    FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK 
    BY fa-order.ActiveReason BY fa-op.nr BY fa-op.datum:

        IF fa-order.ActiveReason NE nr-budget THEN
        DO:
            IF nr-budget NE "" THEN
            DO:
                CREATE fa-budget-ytd.

                ASSIGN
                    fa-budget-ytd.anzahl-str        = STRING(t-mtd-qty, "->>,>>>,>>9")
                    fa-budget-ytd.amount-str        = STRING(t-mtd-amount, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-ytd.mtd-variance-str  = STRING(mtd-variance, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-ytd.anzahlytd-str     = STRING(t-ytd-qty, "->>,>>>,>>9")
                    fa-budget-ytd.amountytd-str     = STRING(t-ytd-amount, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-ytd.ytd-variance-str  = STRING(ytd-variance, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-ytd.descrip-str       = STRING(nr-budget) + " - " + budget-desc-last
                    fa-budget-ytd.account-no        = STRING(nr-budget, ">,>>9")
                    fa-budget-ytd.mtd-budget-str    = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-ytd.ytd-budget-str    = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                .

                mtd-budget      = 0.
                ytd-budget      = 0.
                t-mtd-qty       = 0.
                t-mtd-amount    = 0.
                mtd-variance    = 0.
                t-ytd-qty       = 0. 
                t-ytd-amount    = 0.
                ytd-variance    = 0.
            END.

            mtd-budget = fix-asset-list.amount-budget.
            ytd-budget = fix-asset-list.amount-budget.

            nr-budget          = fa-order.ActiveReason.
            budget-date-last   = fix-asset-list.date-budget.
            budget-nr-last     = fix-asset-list.nr-budget.
            budget-desc-last   = fix-asset-list.desc-budget.
        END.

        count-i = count-i + 1.
        IF fa-artnr NE fa-op.nr THEN
        DO:
            IF MONTH(fa-op.datum) EQ MONTH(ytd-date) THEN
            DO:
                ASSIGN
                    t-mtd-qty = t-mtd-qty + fa-op.anzahl
                    t-mtd-amount = t-mtd-amount + fa-op.warenwert
                    mtd-variance = (mtd-budget - t-mtd-amount)
                .
            END.

            t-ytd-qty = t-ytd-qty + fa-op.anzahl.
            t-ytd-amount = t-ytd-amount + fa-op.warenwert.
            ytd-variance = (ytd-budget - t-ytd-amount).

            fa-artnr = fa-op.nr.
        END.
    END.

    IF count-i GT 0 THEN
    DO:
        CREATE fa-budget-ytd.

        ASSIGN
            fa-budget-ytd.anzahl-str        = STRING(t-mtd-qty, "->>,>>>,>>9")
            fa-budget-ytd.amount-str        = STRING(t-mtd-amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.mtd-variance-str  = STRING(mtd-variance, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.anzahlytd-str     = STRING(t-ytd-qty, "->>,>>>,>>9")
            fa-budget-ytd.amountytd-str     = STRING(t-ytd-amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.ytd-variance-str  = STRING(ytd-variance, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.descrip-str       = STRING(nr-budget) + " - " + budget-desc-last
            fa-budget-ytd.account-no        = STRING(nr-budget, ">,>>9")
            fa-budget-ytd.mtd-budget-str    = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
            fa-budget-ytd.ytd-budget-str    = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99")
        .
    END.

END PROCEDURE.

PROCEDURE create-budget-period:
    DEFINE VARIABLE budget-date-last AS DATE.
    DEFINE VARIABLE budget-nr-last AS INTEGER.
    DEFINE VARIABLE budget-desc-last AS CHARACTER.
    
    IF detailed THEN
    DO:
        /* not used */
        /* FOR EACH fa-op WHERE fa-op.loeschflag LE 1
            AND fa-op.datum GE from-date AND fa-op.datum LE to-date NO-LOCK,
            FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK,
            FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
            FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp AND fa-grup.flag GT 0 NO-LOCK
            /*FIRST gl-acct WHERE gl-acct.fibukonto EQ fa-artikel.fibukonto NO-LOCK*/ 
            BY fa-artikel.fibukonto BY fa-op.datum:                       

            IF curr-fibu NE fa-artikel.fibukonto THEN
            DO:                      
                IF curr-fibu NE "" THEN
                DO:                 
                    FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ curr-fibu NO-LOCK NO-ERROR.
                    IF AVAILABLE gl-acct THEN
                    DO:
                        period-budget = 0.
                        DO count-i = MONTH(from-date) TO MONTH(to-date):  
                            period-budget = period-budget + gl-acct.budget[count-i]. 
                        END.
                    END.                    
                END.                                                                   
    
                IF period-qty NE 0 AND period-amount NE 0 THEN
                DO:
                    period-variance = (period-budget - period-amount).
                    CREATE fa-budget-period. 
                    ASSIGN
                        fa-budget-period.descrip-str    = "T O T A L"
                        fa-budget-period.anzahl-str     = STRING(period-qty, "->>,>>>,>>9")
                        fa-budget-period.amount-str     = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                        fa-budget-period.budget-str     = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
                        fa-budget-period.variance-str   = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
                        .
                END.
                
                RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu-formated).
                CREATE fa-budget-period.
                ASSIGN 
                    fa-budget-period.descrip-str    = fa-grup.bezeich + " - " + fibu-formated
                    fa-budget-period.account-no     = fa-artikel.fibukonto                   
                    .
                
                period-qty      = 0. 
                period-amount   = 0.
                period-variance = 0.
            END.
            
            CREATE fa-budget-period.
            ASSIGN 
                fa-budget-period.descrip-str    = mathis.NAME 
                fa-budget-period.asset          = mathis.asset 
                fa-budget-period.account-no     = fa-artikel.fibukonto
                fa-budget-period.asset-date     = fa-op.datum
                fa-budget-period.price-str      = STRING(fa-op.einzelpreis, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.anzahl-str     = STRING(fa-op.anzahl, "->>,>>>,>>9")
                fa-budget-period.amount-str     = STRING(fa-op.warenwert, "->>>,>>>,>>>,>>>,>>9.99")
                .
            /* Dzikri 01B1DB */
            FIND FIRST queasy WHERE queasy.key EQ 315 AND queasy.number1 EQ mathis.nr AND queasy.char1 EQ fa-op.docu-nr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            ASSIGN
                fa-budget-period.budget-date    = queasy.date1 
            .
            /* Dzikri 01B1DB - END */

            ASSIGN
                period-qty = period-qty + fa-op.anzahl
                period-amount = period-amount + fa-op.warenwert                
                .            
                        
            curr-fibu = fa-artikel.fibukonto.
            it-exist = YES.
        END.
        IF it-exist THEN
        DO:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ curr-fibu NO-LOCK NO-ERROR.
            IF AVAILABLE gl-acct THEN
            DO:
                period-budget = 0.
                DO count-i = MONTH(from-date) TO MONTH(to-date):  
                    period-budget = period-budget + gl-acct.budget[count-i]. 
                END.
            END.
            IF period-qty NE 0 AND period-amount NE 0 THEN
            DO:
                period-variance = (period-budget - period-amount).
                CREATE fa-budget-period.
                ASSIGN
                    fa-budget-period.descrip-str    = "T O T A L"
                    fa-budget-period.anzahl-str     = STRING(period-qty, "->>,>>>,>>9")
                    fa-budget-period.amount-str     = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-period.budget-str     = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-period.variance-str   = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
                    .
            END.
        END. */

        FOR EACH fa-order WHERE fa-order.ActiveReason NE "0" 
        AND fa-order.ActiveReason NE ""
        AND fa-order.ActiveReason NE ? NO-LOCK,
        EACH fa-op WHERE fa-op.loeschflag LE 1 
        AND fa-op.opart EQ 1 
        AND fa-op.anzahl GT 0
        AND fa-op.docu-nr EQ fa-order.Order-Nr
        AND fa-op.datum GE from-date 
        AND fa-op.datum LE to-date NO-LOCK,
        FIRST fix-asset-list WHERE STRING(fix-asset-list.nr-budget) EQ fa-order.ActiveReason NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK 
        BY fa-order.ActiveReason BY fa-op.nr BY fa-op.datum:

            count-i = count-i + 1.

            IF fa-order.ActiveReason NE nr-budget THEN
            DO:
                IF nr-budget NE "" THEN
                DO:
                    CREATE fa-budget-period.

                    ASSIGN
                        fa-budget-period.anzahl-str        = STRING(period-qty, "->>,>>>,>>9")
                        fa-budget-period.amount-str        = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                        fa-budget-period.variance-str      = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
                        fa-budget-period.budget-str        = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
                        fa-budget-period.budget-date       = fix-asset-list.date-budget
                        fa-budget-period.descrip-str       = "T O T A L"
                        fa-budget-period.account-no        = STRING(fix-asset-list.nr-budget, ">,>>9")
                    .

                    grand-total-qty      = grand-total-qty      + period-qty.
                    grand-total-amount   = grand-total-amount   + period-amount.
                    grand-total-budget   = grand-total-budget   + period-budget.
                    grand-total-variance = grand-total-variance + period-variance.

                    CREATE fa-budget-period.

                    period-budget   = 0.
                    period-qty      = 0. 
                    period-amount   = 0.
                    period-variance = 0.
                END.

                period-budget = fix-asset-list.amount-budget.

                CREATE fa-budget-period.
                ASSIGN 
                    fa-budget-period.descrip-str       = STRING(fix-asset-list.nr-budget) + " - " + fix-asset-list.desc-budget
                    fa-budget-period.account-no        = STRING(fix-asset-list.nr-budget, ">,>>9")
                .

                nr-budget        = fa-order.ActiveReason.
                budget-date-last = fix-asset-list.date-budget.
                budget-nr-last   = fix-asset-list.nr-budget.
            END.


            IF fa-artnr NE fa-op.nr THEN
            DO:
                CREATE fa-budget-period.
                ASSIGN 
                    fa-budget-period.descrip-str    = mathis.NAME 
                    fa-budget-period.asset          = mathis.asset 
                    fa-budget-period.account-no     = fa-artikel.fibukonto
                    fa-budget-period.asset-date     = fa-op.datum
                    fa-budget-period.price-str      = STRING(fa-op.einzelpreis, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget-period.anzahl-str     = STRING(fa-op.anzahl, "->>,>>>,>>9")
                    fa-budget-period.amount-str     = STRING(fa-op.warenwert, "->>>,>>>,>>>,>>>,>>9.99")
                .

                period-qty = period-qty + fa-op.anzahl.
                period-amount = period-amount + fa-op.warenwert.
                period-variance = (period-budget - period-amount).

                fa-artnr = fa-op.nr.
            END.
        END.

        IF count-i GT 0 THEN
        DO:

            CREATE fa-budget-period.

            ASSIGN
                fa-budget-period.anzahl-str        = STRING(period-qty, "->>,>>>,>>9")
                fa-budget-period.amount-str        = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.variance-str      = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.budget-str        = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.budget-date       = budget-date-last
                fa-budget-period.descrip-str       = "T O T A L"
            .

            CREATE fa-budget-period.

            grand-total-qty      = grand-total-qty      + period-qty.
            grand-total-amount   = grand-total-amount   + period-amount.
            grand-total-budget   = grand-total-budget   + period-budget.
            grand-total-variance = grand-total-variance + period-variance.

            CREATE fa-budget-period.

            ASSIGN
                fa-budget-period.anzahl-str        = STRING(grand-total-qty, "->>,>>>,>>9")
                fa-budget-period.amount-str        = STRING(grand-total-amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.variance-str      = STRING(grand-total-variance, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.budget-str        = STRING(grand-total-budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.descrip-str       = "GRAND TOTAL"
            .
        END.
    END.
    ELSE
    DO:
        /* not used */
        /* FOR EACH fa-op WHERE fa-op.loeschflag LE 1
            AND fa-op.datum GE from-date AND fa-op.datum LE to-date NO-LOCK,
            FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK,
            FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
            FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp AND fa-grup.flag GT 0 NO-LOCK,
            FIRST gl-acct WHERE gl-acct.fibukonto EQ fa-artikel.fibukonto NO-LOCK 
            BY fa-artikel.fibukonto BY fa-op.datum:

            IF curr-fibu NE fa-artikel.fibukonto THEN
            DO:                
                period-budget   = 0.
                period-qty      = 0. 
                period-amount   = 0.
                period-variance = 0. 

                RUN convert-fibu(fa-artikel.fibukonto, OUTPUT fibu-formated).
                                
                DO count-i = MONTH(from-date) TO MONTH(to-date):  
                    period-budget = period-budget + gl-acct.budget[count-i]. 
                END.
    
                CREATE fa-budget-period.
                ASSIGN 
                    fa-budget-period.descrip-str    = fa-grup.bezeich + " - " + fibu-formated
                    fa-budget-period.account-no     = fa-artikel.fibukonto                    
                    fa-budget-period.budget-str     = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
                    .
            END.
                
            ASSIGN
                period-qty = period-qty + fa-op.anzahl
                period-amount = period-amount + fa-op.warenwert
                period-variance = (period-budget - period-amount)
                .                       
    
            ASSIGN
                fa-budget-period.anzahl-str         = STRING(period-qty, "->>,>>>,>>9")
                fa-budget-period.amount-str         = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.variance-str       = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")                
                .
    
            curr-fibu = fa-artikel.fibukonto.
        END. */

        FOR EACH fa-order WHERE fa-order.ActiveReason NE "0" 
            AND fa-order.ActiveReason NE ""
            AND fa-order.ActiveReason NE ? NO-LOCK,
            EACH fa-op WHERE fa-op.loeschflag LE 1 
            AND fa-op.opart EQ 1 
            AND fa-op.anzahl GT 0
            AND fa-op.docu-nr EQ fa-order.Order-Nr
            AND fa-op.datum GE from-date 
            AND fa-op.datum LE to-date NO-LOCK,
            FIRST fix-asset-list WHERE STRING(fix-asset-list.nr-budget) EQ fa-order.ActiveReason NO-LOCK,
            FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
            FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK 
            BY fa-order.ActiveReason BY fa-op.nr BY fa-op.datum:

            count-i = count-i + 1.

            IF fa-order.ActiveReason NE nr-budget THEN
            DO:

                IF nr-budget NE "" THEN
                DO:

                    CREATE fa-budget-period.

                    ASSIGN 
                        fa-budget-period.budget-str        = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
                        fa-budget-period.budget-date       = budget-date-last
                        fa-budget-period.descrip-str       = STRING(budget-nr-last) + " - " + budget-desc-last
                        fa-budget-period.account-no        = STRING(budget-nr-last, ">,>>9")
                        fa-budget-period.anzahl-str        = STRING(period-qty, "->>,>>>,>>9")
                        fa-budget-period.amount-str        = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                        fa-budget-period.variance-str      = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
                    .

                    grand-total-qty      = grand-total-qty      + period-qty.
                    grand-total-amount   = grand-total-amount   + period-amount.
                    grand-total-budget   = grand-total-budget   + period-budget.
                    grand-total-variance = grand-total-variance + period-variance.

                    period-budget   = 0.
                    period-qty      = 0. 
                    period-amount   = 0.
                    period-variance = 0.
                END.

                period-budget = fix-asset-list.amount-budget.

                nr-budget = fa-order.ActiveReason.
                budget-date-last = fix-asset-list.date-budget.
                budget-nr-last   = fix-asset-list.nr-budget.
                budget-desc-last = fix-asset-list.desc-budget.
            END.
            
            IF fa-artnr NE fa-op.nr THEN
            DO:
                period-qty = period-qty + fa-op.anzahl.
                period-amount = period-amount + fa-op.warenwert.
                period-variance = (period-budget - period-amount).

                fa-artnr = fa-op.nr.
            END.
        END.

        IF count-i GT 0 THEN
        DO:
            CREATE fa-budget-period.

            ASSIGN 
                fa-budget-period.budget-str        = STRING(period-budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.budget-date       = budget-date-last
                fa-budget-period.descrip-str       = STRING(budget-nr-last) + " - " + budget-desc-last
                fa-budget-period.account-no        = STRING(budget-nr-last, ">,>>9")
                fa-budget-period.anzahl-str        = STRING(period-qty, "->>,>>>,>>9")
                fa-budget-period.amount-str        = STRING(period-amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.variance-str      = STRING(period-variance, "->>>,>>>,>>>,>>>,>>9.99")
            .

            CREATE fa-budget-period.

            grand-total-qty      = grand-total-qty      + period-qty.
            grand-total-amount   = grand-total-amount   + period-amount.
            grand-total-budget   = grand-total-budget   + period-budget.
            grand-total-variance = grand-total-variance + period-variance.

            CREATE fa-budget-period.

            ASSIGN
                fa-budget-period.anzahl-str        = STRING(grand-total-qty, "->>,>>>,>>9")
                fa-budget-period.amount-str        = STRING(grand-total-amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.variance-str      = STRING(grand-total-variance, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.budget-str        = STRING(grand-total-budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa-budget-period.descrip-str       = "T O T A L"
            .
        END.
    END.
END PROCEDURE. 

/* 
PROCEDURE convert-fibu: 
    DEFINE INPUT  PARAMETER konto   AS CHAR. 
    DEFINE OUTPUT PARAMETER s       AS CHAR INITIAL "". 
    DEFINE VARIABLE ch AS CHAR. 
    DEFINE VARIABLE i AS INTEGER. 
    DEFINE VARIABLE j AS INTEGER. 
    FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
    ch = htparam.fchar. 
    j = 0. 
    DO i = 1 TO length(ch): 
        IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
        DO: 
            j = j + 1. 
            s = s + SUBSTR(konto, j, 1). 
        END. 
        ELSE s = s + SUBSTR(ch, i, 1). 
    END. 
END. 
 */
