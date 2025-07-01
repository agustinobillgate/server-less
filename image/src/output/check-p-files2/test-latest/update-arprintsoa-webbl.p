
DEFINE TEMP-TABLE bill-list
    FIELD billref       LIKE bill.billref
    FIELD rechnr        LIKE bill.rechnr
    FIELD saldo         LIKE bill.saldo 
    FIELD deptNo        LIKE debitor.betriebsnr
    FIELD do-release    AS LOGICAL INIT NO.

DEFINE TEMP-TABLE t-payload-list
    FIELD user-init AS CHARACTER. /* Naufal Afthar - 94078C*/

DEFINE INPUT PARAMETER guestno AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR bill-list.
DEFINE INPUT PARAMETER TABLE FOR t-payload-list.

FIND FIRST t-payload-list NO-LOCK NO-ERROR. /* Naufal Afthar - 94078C -> add system log when release SOA*/

RUN update-bill-list.
PROCEDURE update-bill-list:
    DEFINE VARIABLE do-it        AS LOGICAL  NO-UNDO INIT NO.
    DEFINE VARIABLE curr-billref AS INTEGER  NO-UNDO INIT "".
    DEFINE VARIABLE rechnr-list  AS CHARACTER INIT "".

    FIND FIRST bill-list WHERE bill-list.do-release = NO NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bill-list THEN do-it = YES.

    /* Naufal Afthar - 94078C -> add system log when release SOA*/
    FIND FIRST bediener WHERE bediener.userinit EQ t-payload-list.user-init NO-LOCK NO-ERROR.

    FOR EACH bill-list WHERE bill-list.do-release = YES 
        NO-LOCK BY bill-list.billref:

        /* Naufal Afthar - 94078C -> add system log when release SOA*/
        IF curr-billref EQ 0 THEN ASSIGN curr-billref = bill-list.billref.

        IF AVAILABLE bediener AND curr-billref NE bill-list.billref THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr = bediener.nr
                res-history.datum = TODAY
                res-history.zeit = TIME
                res-history.action = "Statement Of Account"
                res-history.aenderung = "Transaction Bill Number " + 
                                         SUBSTRING(rechnr-list, 1, LENGTH(rechnr-list) - 2) + " has been released from Invoice No : " +
                                         STRING(curr-billref, "9999999").
            
            curr-billref = bill-list.billref.
            rechnr-list = "".
        END.

        rechnr-list = rechnr-list + STRING(bill-list.rechnr) + ", ".

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

    /* Naufal Afthar - 94078C -> add system log when release SOA (last)*/
    CREATE res-history.
    ASSIGN
        res-history.nr = bediener.nr
        res-history.datum = TODAY
        res-history.zeit = TIME
        res-history.action = "Statement Of Account"
        res-history.aenderung = "Transaction Bill Number " + 
                                 SUBSTRING(rechnr-list, 1, LENGTH(rechnr-list) - 2) + " has been released from Invoice No : " +
                                 STRING(curr-billref, "9999999").
    
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
