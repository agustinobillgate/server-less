
DEFINE TEMP-TABLE bill-list
    FIELD billref       LIKE bill.billref
    FIELD rechnr        LIKE bill.rechnr
    FIELD saldo         LIKE bill.saldo 
    FIELD deptNo        LIKE debitor.betriebsnr
    FIELD do-release    AS LOGICAL INIT NO.

DEFINE INPUT PARAMETER guestno   AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER exist    AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR bill-list.

DEFINE VARIABLE guestname AS CHAR NO-UNDO.

FIND FIRST guest WHERE guest.gastnr EQ guestno NO-LOCK NO-ERROR.

IF guest.karteityp EQ 0 THEN
    guestname = guest.NAME + ", " + guest.vorname1.
ELSE guestname = guest.NAME + ", " + guest.anredefirma.

RUN cr-bill-list.

PROCEDURE cr-bill-list:
    FOR EACH bill-list.
        DELETE bill-list.
    END.
    
    FOR EACH debitor WHERE debitor.gastnr = guestNo 
        AND debitor.opart LE 1 AND debitor.saldo NE 0
        AND debitor.zahlkonto = 0 NO-LOCK
        BY debitor.betriebsnr BY debitor.rechnr :
        IF debitor.betriebsnr EQ 0 THEN
        DO:
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr 
                AND bill.billref NE 0 
                AND bill.billref = debitor.debref NO-LOCK NO-ERROR.
            IF AVAILABLE bill AND bill.rechnr NE 0 THEN
            DO:
                FIND FIRST bill-list WHERE bill-list.rechnr = bill.rechnr 
                    AND bill-list.billref = bill.billref NO-LOCK NO-ERROR.
                IF NOT AVAILABLE bill-list THEN
                DO:
                    exist = YES.
                    CREATE bill-list.
                    ASSIGN bill-list.billref       = bill.billref
                           bill-list.rechnr        = bill.rechnr
                           bill-list.saldo         = debitor.saldo 
                           bill-list.deptNo        = debitor.betriebsnr.
                END.                                                 
            END.
            ELSE DO:
                FIND FIRST queasy WHERE queasy.KEY = 192 AND queasy.number1 = debitor.rechnr NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN DO:
                    FIND FIRST bill-list WHERE bill-list.rechnr = queasy.number1 
                        AND bill-list.billref = queasy.number2 NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE bill-list THEN
                    DO:
                        exist = YES.
                        CREATE bill-list.
                        ASSIGN bill-list.billref       = queasy.number2
                               bill-list.rechnr        = queasy.number1
                               bill-list.saldo         = debitor.saldo
                               bill-list.deptNo        = debitor.betriebsnr.
                    END.             
                END.
            END.
        END.
        ELSE 
        DO:
            FIND FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr
                AND h-bill.departement = debitor.betriebsnr
                AND h-bill.service[6] NE 0
                AND h-bill.service[6] = DEC(debitor.debref) 
                NO-LOCK NO-ERROR.
            IF AVAILABLE h-bill AND h-bill.rechnr NE 0 THEN
            DO:
                FIND FIRST bill-list WHERE bill-list.rechnr = bill.rechnr 
                    NO-LOCK NO-ERROR.
                IF NOT AVAILABLE bill-list THEN
                DO:
                    exist = YES.
                    CREATE bill-list.
                    ASSIGN bill-list.billref       = INT(h-bill.service[6])
                           bill-list.rechnr        = h-bill.rechnr
                           bill-list.saldo         = h-bill.saldo 
                           bill-list.deptNo        = debitor.betriebsnr.
                END.
            END.
        END.                                                         
    END.
END.

