DEFINE INPUT PARAMETER order-name    AS CHAR. 
DEFINE INPUT PARAMETER order-phone   AS CHAR. 
DEFINE INPUT PARAMETER order-email   AS CHAR. 
DEFINE OUTPUT PARAMETER msg-str      AS CHAR. 

DEFINE VARIABLE payment-param AS INTEGER.
DEFINE VARIABLE curr-gastnr   AS INTEGER.

FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1
    AND queasy.number2 EQ 26 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    payment-param = INT(queasy.char2).
END.
ELSE
DO:
    msg-str = "Artikel Number For Guest Ledger Not Available!". 
    RETURN.
END.

DEFINE BUFFER bguest FOR guest.
FIND FIRST guest WHERE guest.mobil-telefon EQ order-phone AND guest.karteityp EQ 0 EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE guest THEN
DO:
    FIND FIRST guest WHERE guest.telefon EQ order-phone AND guest.karteityp EQ 0 EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE guest THEN 
    DO:
        FOR EACH bguest NO-LOCK BY bguest.gastnr DESC:
            curr-gastnr = bguest.gastnr.
            LEAVE.
        END.
        IF curr-gastnr EQ 0 THEN curr-gastnr = 1.
        ELSE curr-gastnr = curr-gastnr + 1.

        CREATE guest.
        guest.karteityp     = 0.
        guest.NAME          = order-name.
        guest.email-adr     = order-email.
        guest.telefon       = order-phone.
        guest.mobil-telefon = order-phone.
        guest.gastnr        = curr-gastnr.
        guest.zahlungsart   = payment-param.
        guest.point-gastnr  = payment-param.
    END.
    ELSE 
    DO:
        guest.NAME          = order-name.
        guest.email-adr     = order-email.
        guest.telefon       = order-phone.
        guest.mobil-telefon = order-phone.
        guest.zahlungsart   = payment-param.
        guest.point-gastnr  = payment-param.
    END.
END.
ELSE
DO:
    guest.NAME          = order-name.
    guest.email-adr     = order-email.
    guest.telefon       = order-phone.
    guest.mobil-telefon = order-phone.
    guest.zahlungsart   = payment-param.
    guest.point-gastnr  = payment-param.
END.
RELEASE guest.
RELEASE bguest.

