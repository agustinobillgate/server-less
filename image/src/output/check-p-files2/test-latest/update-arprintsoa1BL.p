
DEFINE TEMP-TABLE bill-list
    FIELD billref       LIKE bill.billref
    FIELD rechnr        LIKE bill.rechnr
    FIELD saldo         LIKE bill.saldo 
    FIELD deptNo        LIKE debitor.betriebsnr
    FIELD do-release    AS LOGICAL INIT NO.

DEFINE INPUT PARAMETER guestno AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR bill-list.

RUN update-bill-list.
PROCEDURE update-bill-list:
    DEFINE VARIABLE do-it        AS LOGICAL  NO-UNDO INIT NO.
    DEFINE VARIABLE curr-billref AS INTEGER  NO-UNDO.

    FIND FIRST bill-list WHERE bill-list.do-release = NO NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bill-list THEN do-it = YES.
    
    FOR EACH bill-list WHERE bill-list.do-release = YES NO-LOCK:
        IF bill-list.deptNo EQ 0 THEN 
        DO:
            FIND FIRST bill WHERE bill.billref = bill-list.billref
                AND bill.rechnr = bill-list.rechnr NO-LOCK NO-ERROR.
            IF AVAILABLE bill THEN DO:
                FIND CURRENT bill EXCLUSIVE-LOCK.
                IF bill.billref NE 0 THEN ASSIGN bill.billref = 0.                
                FIND CURRENT bill NO-LOCK.
                RELEASE bill.
            END.
            ELSE DO:
                    FIND FIRST queasy WHERE queasy.KEY = 192 AND queasy.number1 = bill-list.rechnr
                        AND queasy.number2 = bill-list.billref NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN DO:
                        FIND CURRENT queasy EXCLUSIVE-LOCK.
                        DELETE queasy.
                        RELEASE queasy.
                    END.
            END.
        END.
        ELSE
        DO:
            FIND FIRST h-bill WHERE h-bill.service[6] = DEC(bill-list.billref)
                AND h-bill.departement = bill-list.deptNo
                AND h-bill.rechnr = bill-list.rechnr EXCLUSIVE-LOCK.
            IF AVAILABLE h-bill THEN
                ASSIGN h-bill.service[6] = 0.
            FIND CURRENT h-bill NO-LOCK.
            RELEASE h-bill.
        END.
    END.
    
    IF do-it THEN
    FOR EACH bill-list WHERE bill-list.do-release = YES NO-LOCK:
        FIND FIRST debitor WHERE debitor.gastnr = guestno
            AND debitor.opart LE 1 AND debitor.saldo NE 0
            AND debitor.zahlkonto = 0 
            AND debitor.debref = bill-list.billref EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE debitor THEN debitor.debref = 0.
        FIND CURRENT debitor NO-LOCK.
    END.
END.
