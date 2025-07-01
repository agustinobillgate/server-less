
DEF TEMP-TABLE t-printer LIKE printer.

DEF INPUT  PARAMETER resnr              AS INT.
DEF INPUT  PARAMETER printer-nr         AS INT.
DEF OUTPUT PARAMETER curr-local         AS CHAR.
DEF OUTPUT PARAMETER ch                 AS CHAR FORMAT "x(72)". 
DEF OUTPUT PARAMETER ch1                AS CHAR     INITIAL ""  FORMAT "x(72)".
DEF OUTPUT PARAMETER secondpay          AS CHAR     INITIAL ""  FORMAT "x(72)".
DEF OUTPUT PARAMETER string-guest       AS CHAR     INITIAL ""  FORMAT "x(72)".
DEF OUTPUT PARAMETER string-reslinename AS CHAR     INITIAL ""  FORMAT "x(72)".
DEF OUTPUT PARAMETER string-deposit     AS CHAR     INITIAL "".
DEF OUTPUT PARAMETER balance            AS DECIMAL.
DEF OUTPUT PARAMETER voucher-no         AS CHAR.
/*IF 210219 - Safari Lodge*/
DEFINE OUTPUT PARAMETER ci-date AS DATE         NO-UNDO.
DEFINE OUTPUT PARAMETER co-date AS DATE         NO-UNDO.
DEFINE OUTPUT PARAMETER rmno    AS CHARACTER    NO-UNDO.
/*END IF*/
DEF OUTPUT PARAMETER TABLE FOR t-printer.

DEFINE BUFFER w1    FOR waehrung.

IF printer-nr = 0 THEN printer-nr = 1.

FIND FIRST PRINTER WHERE printer.nr = printer-nr NO-LOCK.
CREATE t-printer.
BUFFER-COPY PRINTER TO t-printer.

FIND FIRST htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = htparam.fchar. 

FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE reservation THEN
DO:
    IF reservation.depositbez GE 1 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr = reservation.zahlkonto
            AND artikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN 
        DO:
            IF NOT artikel.pricetab THEN
            DO:
                ch =  STRING(curr-local, "x(8) ") + STRING(artikel.bezeich, "x(24) ")
                   + STRING(reservation.depositbez,"->>,>>>,>>9.99").
            END.                
            ELSE
            DO:
              FIND FIRST w1 WHERE w1.waehrungsnr = artikel.betriebsnr NO-LOCK.
              ch =  STRING(w1.wabkurz, "x(8) ") + STRING(artikel.bezeich, "x(24) ")
                 + STRING(reservation.depositbez,"->>,>>>,>>9.99").
            END.
        END.
    END.

    IF reservation.depositbez2 GE 1 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr = reservation.zahlkonto2
            AND artikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN 
        DO:
            IF NOT artikel.pricetab THEN
            DO:
                ch1 =  STRING(curr-local, "x(8) ") + STRING(artikel.bezeich, "x(24) ")
                    + STRING(reservation.depositbez2,"->>,>>>,>>9.99").
            END.                
            ELSE
            DO:
              FIND FIRST w1 WHERE w1.waehrungsnr = artikel.betriebsnr NO-LOCK.
              ch1 = STRING(w1.wabkurz, "x(8) ") + STRING(artikel.bezeich, "x(24) ")
                  + STRING(reservation.depositbez2,"->>,>>>,>>9.99").
            END.
        END.

    END.

    IF reservation.depositbez2 NE 0 THEN
        secondpay = "1".

    ASSIGN
        string-guest        = ""
        string-reslineName  = ""
    .

    FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK
        NO-ERROR.
    IF AVAILABLE guest THEN
        string-guest = guest.NAME + " " + guest.vorname1 + ", " + guest.anredefirma + guest.vorname1.

    FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
        AND (res-line.resstatus LE 2 OR res-line.resstatus EQ 5)
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE res-line THEN
    FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
        AND (res-line.resstatus = 6) NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
        string-reslineName = STRING(res-line.name, "x(36)").
    
    ASSIGN
        string-deposit = STRING(reservation.depositgef , "->>,>>>,>>>,>>9")
        balance = reservation.depositgef - reservation.depositbez 
                - reservation.depositbez2
    .
    FIND FIRST debitor WHERE debitor.gastnr = reservation.gastnr
        AND debitor.gastnrmember = reservation.gastnr
        AND debitor.vesrcod MATCHES "Deposit*" 
        AND debitor.vesrcod MATCHES "*" + STRING(reservation.resnr) + "*" NO-LOCK NO-ERROR.
    IF AVAILABLE debitor THEN DO:
        IF NUM-ENTRIES(ENTRY(2, debitor.vesrcod, ":"), ";") GT 1 THEN
            ASSIGN voucher-no = ENTRY(2, ENTRY(2, debitor.vesrcod, ":"), ";").
        ELSE ASSIGN voucher-no = " ".
    END.
    ELSE ASSIGN voucher-no = " ".
END.

/*IF 210219 - Safari Lodge*/
FIND FIRST res-line WHERE res-line.resnr EQ resnr NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN 
DO:
    ASSIGN 
        ci-date     = res-line.ankunft
        co-date     = res-line.abreise
        rmno        = res-line.zinr.
END.
/*END IF*/
    
/*
    FIND FIRST debitor WHERE debitor.gastnr = reservation.gastnr
            AND debitor.gastnrmember = reservation.gastnr
            AND debitor.vesrcod MATCHES "Deposit*" NO-LOCK NO-ERROR.
            IF AVAILABLE debitor THEN DO:
                IF debitor.vesrcod MATCHES("*:*") THEN DO:
                    IF debitor.vesrcod MATCHES("*;*") THEN DO:
                        IF INT(ENTRY(1, ENTRY(2, debitor.vesrcod, ":"), ";")) = reservation.resnr THEN DO:
                            IF NUM-ENTRIES(ENTRY(2, debitor.vesrcod, ":"), ";") GT 1 THEN
                                ASSIGN voucher-no = ENTRY(2, ENTRY(2, debitor.vesrcod, ":"), ";").
                            ELSE ASSIGN voucher-no = " ".
                        END.
                        ELSE ASSIGN voucher-no = " ".
                    END.
                    ELSE ASSIGN voucher-no = " ".
                END.
                ELSE ASSIGN voucher-no = " ".
            END.
        ELSE ASSIGN voucher-no = " ".
    END.
 */
