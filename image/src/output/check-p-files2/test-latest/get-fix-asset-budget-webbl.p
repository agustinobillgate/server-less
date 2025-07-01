DEFINE TEMP-TABLE fix-asset-list
    FIELD nr-budget          AS INTEGER
    FIELD desc-budget        AS CHARACTER
    FIELD date-budget        AS DATE
    FIELD amount-budget      AS DECIMAL
    FIELD is-active-budget   AS LOGICAL
    FIELD safe-to-del-or-mod AS LOGICAL
    FIELD remain-budget      AS DECIMAL
    .

DEFINE INPUT PARAMETER search-by-desc AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER retrieve-for   AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR fix-asset-list.

IF retrieve-for EQ "setting" THEN
DO:
    IF search-by-desc EQ " " THEN
        RUN retrieve-it1a.
    ELSE
        RUN retrieve-it1b.
        
END.
ELSE IF retrieve-for EQ "purchase-order" THEN
DO:
    IF search-by-desc EQ " " THEN
        RUN retrieve-it2a.
    ELSE
        RUN retrieve-it2b.
END.

PROCEDURE retrieve-it1a:
    DEFINE VARIABLE t-warenwert AS DECIMAL INITIAL 0.0.

    FOR EACH queasy WHERE queasy.key EQ 324 NO-LOCK:

        t-warenwert = 0.0.

        CREATE fix-asset-list.
        
        ASSIGN 
            fix-asset-list.nr-budget          = queasy.number1
            fix-asset-list.desc-budget        = queasy.char1
            fix-asset-list.date-budget        = queasy.date1
            fix-asset-list.amount-budget      = queasy.deci1
            fix-asset-list.is-active-budget   = queasy.logi1
        .

        FIND FIRST fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE fa-order THEN
        DO:
            fix-asset-list.safe-to-del-or-mod = YES.
        END.

        FOR EACH fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK:
            FIND FIRST fa-op WHERE fa-op.loeschflag LE 1 
            AND fa-op.opart EQ 1 
            AND fa-op.anzahl GT 0
            AND fa-op.docu-nr EQ fa-order.Order-Nr NO-LOCK NO-ERROR.
            IF AVAILABLE fa-op THEN
            DO:
                t-warenwert = t-warenwert + fa-op.warenwert.
            END.
        END.

        fix-asset-list.remain-budget = queasy.deci1 - t-warenwert.
    END.
END.

PROCEDURE retrieve-it1b:
    DEFINE VARIABLE t-warenwert AS DECIMAL INITIAL 0.0.

    FOR EACH queasy WHERE queasy.key EQ 324 
    AND queasy.char1 MATCHES "*" + search-by-desc + "*" NO-LOCK:

        t-warenwert = 0.0.

        CREATE fix-asset-list.
        
        ASSIGN 
            fix-asset-list.nr-budget          = queasy.number1
            fix-asset-list.desc-budget        = queasy.char1
            fix-asset-list.date-budget        = queasy.date1
            fix-asset-list.amount-budget      = queasy.deci1
            fix-asset-list.is-active-budget   = queasy.logi1
        .

        FIND FIRST fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE fa-order THEN
        DO:
            fix-asset-list.safe-to-del-or-mod = YES.
        END.

        FOR EACH fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK:
            FIND FIRST fa-op WHERE fa-op.loeschflag LE 1 
            AND fa-op.opart EQ 1 
            AND fa-op.anzahl GT 0
            AND fa-op.docu-nr EQ fa-order.Order-Nr NO-LOCK NO-ERROR.
            IF AVAILABLE fa-op THEN
            DO:
                t-warenwert = t-warenwert + fa-op.warenwert.
            END.
        END.

        fix-asset-list.remain-budget = queasy.deci1 - t-warenwert.
    END.
END.


PROCEDURE retrieve-it2a:
    DEFINE VARIABLE t-warenwert AS DECIMAL INITIAL 0.0.

    FOR EACH queasy WHERE queasy.key EQ 324 
    AND queasy.logi1 EQ YES NO-LOCK:

        t-warenwert = 0.0.

        CREATE fix-asset-list.
        
        ASSIGN 
            fix-asset-list.nr-budget          = queasy.number1
            fix-asset-list.desc-budget        = STRING(queasy.number1) + " - " + queasy.char1
            fix-asset-list.date-budget        = queasy.date1
            fix-asset-list.amount-budget      = queasy.deci1
            fix-asset-list.is-active-budget   = queasy.logi1
        .

        FIND FIRST fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE fa-order THEN
        DO:
            fix-asset-list.safe-to-del-or-mod = YES.
        END.

        FOR EACH fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK:
            FIND FIRST fa-op WHERE fa-op.loeschflag LE 1 
            AND fa-op.opart EQ 1 
            AND fa-op.anzahl GT 0
            AND fa-op.docu-nr EQ fa-order.Order-Nr NO-LOCK NO-ERROR.
            IF AVAILABLE fa-op THEN
            DO:
                t-warenwert = t-warenwert + fa-op.warenwert.
            END.
        END.

        fix-asset-list.remain-budget = queasy.deci1 - t-warenwert.
    END.
END.


PROCEDURE retrieve-it2b:
    DEFINE VARIABLE t-warenwert AS DECIMAL INITIAL 0.0.

    FOR EACH queasy WHERE queasy.key EQ 324 
    AND queasy.logi1 EQ YES
    AND queasy.char1 MATCHES "*" + search-by-desc + "*"  NO-LOCK:

        t-warenwert = 0.0.
        
        CREATE fix-asset-list.
        
        ASSIGN 
            fix-asset-list.nr-budget          = queasy.number1
            fix-asset-list.desc-budget        = STRING(queasy.number1) + " - " + queasy.char1
            fix-asset-list.date-budget        = queasy.date1
            fix-asset-list.amount-budget      = queasy.deci1
            fix-asset-list.is-active-budget   = queasy.logi1
        .

        FIND FIRST fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE fa-order THEN
        DO:
            fix-asset-list.safe-to-del-or-mod = YES.
        END.

        FOR EACH fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK:
            FIND FIRST fa-op WHERE fa-op.loeschflag LE 1 
            AND fa-op.opart EQ 1 
            AND fa-op.anzahl GT 0 
            AND fa-op.docu-nr EQ fa-order.Order-Nr NO-LOCK NO-ERROR.
            IF AVAILABLE fa-op THEN
            DO:
                t-warenwert = t-warenwert + fa-op.warenwert.
            END.
        END.

        fix-asset-list.remain-budget = queasy.deci1 - t-warenwert.
    END.
END.
