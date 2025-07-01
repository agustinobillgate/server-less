DEFINE INPUT PARAMETER rsv-number     AS INT.
DEFINE INPUT PARAMETER rsvline-number AS INT.
DEFINE INPUT PARAMETER case-type      AS INT.
DEFINE OUTPUT PARAMETER res-status    AS CHAR.
DEFINE OUTPUT PARAMETER key-maked     AS INT INIT 0.
DEFINE OUTPUT PARAMETER key-max       AS INT INIT 0.
DEFINE OUTPUT PARAMETER key-avail     AS INT INIT 0.
DEFINE OUTPUT PARAMETER key-qty       AS INT INIT 0.
DEFINE OUTPUT PARAMETER key-string    AS CHAR.
DEFINE OUTPUT PARAMETER payment-flag  AS CHAR.
DEFINE OUTPUT PARAMETER mess-str      AS CHAR.

/*
DEFINE VARIABLE rsv-number     AS INT INIT 6844.
DEFINE VARIABLE rsvline-number AS INT INIT 1.
DEFINE VARIABLE case-type      AS INT INIT 2.
DEFINE VARIABLE res-status     AS CHAR.
DEFINE VARIABLE key-maked      AS INT INIT 0.
DEFINE VARIABLE key-max        AS INT INIT 0.
DEFINE VARIABLE key-avail      AS INT INIT 0.
DEFINE VARIABLE key-qty        AS INT INIT 0.
DEFINE VARIABLE key-string     AS CHAR.
DEFINE VARIABLE payment-flag   AS CHAR.
DEFINE VARIABLE mess-str       AS CHAR FORMAT "x(30)".
*/

DEFINE VARIABLE loop     AS INT.
DEFINE VARIABLE tmp-char AS CHAR.
/*
case-type
1 = check res status
2 = check payment
3 = check keycard
*/

IF rsv-number     EQ ? THEN rsv-number     = 0.  
IF rsvline-number EQ ? THEN rsvline-number = 0.
IF case-type      EQ ? THEN case-type      = 0.

IF (rsv-number EQ 0 OR rsvline-number EQ 0) THEN
DO:
     mess-str = "1 - Wrong value parameters for rsvNumber and revlineNumber!".
     RETURN.
END.

IF (case-type LT 1 OR case-type GT 3) THEN
DO:
     mess-str = "2 - Wrong value parameters for caseType!".
     RETURN.
END.

IF case-type NE 3 THEN
DO:
    FIND FIRST res-line WHERE res-line.resnr EQ rsv-number AND res-line.reslinnr EQ rsvline-number NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        IF case-type EQ 1 THEN /*check res status*/
        DO:
            IF res-line.resstatus EQ 6 AND res-line.active-flag = 1 THEN
                 res-status = "1 - Reservation Already Check-In!".
            ELSE res-status = "0 - Reservation Not Check-In Yet!".  
        END.
        ELSE IF case-type EQ 2 THEN /*check payment status*/
        DO:
            DO loop = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";"):
                tmp-char = ENTRY(loop,res-line.zimmer-wunsch,";").
                IF tmp-char MATCHES "*PREAUTHCC*" THEN 
                DO:
                    payment-flag = "1 - Reservation Already Paid!".
                    LEAVE.
                END.
                ELSE payment-flag = "0 - Reservation Not Paid Yet!".
            END.
        END.
        mess-str = "0 - Checking flag success.".
    END.
    ELSE 
    DO:
        mess-str = "3 - Reservation not found! Please check parameter!".
        RETURN.
    END.
END.
ELSE IF case-type EQ 3 THEN /*check keycard*/
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 8 AND queasy.number2 EQ 3 NO-LOCK NO-ERROR. /*check max keysetup for mci*/
    IF AVAILABLE queasy THEN key-max = queasy.number3.
    IF key-max EQ 0 THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr EQ 927 NO-LOCK NO-ERROR. /*check max key allowed in genparam*/
        IF AVAILABLE htparam THEN key-max = htparam.finteger.
    END.

    DEFINE BUFFER rline      FOR res-line.
    DEFINE BUFFER res-sharer FOR res-line.
    FIND FIRST res-line WHERE res-line.resnr EQ rsv-number AND res-line.reslinnr EQ rsvline-number NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        FIND FIRST res-sharer WHERE res-sharer.resnr EQ res-line.resnr 
        AND res-sharer.reslinnr NE res-line.reslinnr
        AND res-sharer.resstatus EQ 11 
        AND res-sharer.zinr EQ res-line.zinr NO-LOCK NO-ERROR. 
        IF AVAILABLE res-sharer THEN
        DO:
            FOR EACH rline WHERE rline.resnr EQ res-line.resnr AND rline.resstatus EQ 11 
                AND rline.zinr EQ res-line.zinr NO-LOCK:
                key-qty   = key-qty + rline.erwach + rline.kind1 + rline.gratis. /*tanya bapak apakah compliment juga dihitung*/
                key-maked = key-maked + rline.betrieb-gast.
            END.
        END.
        key-maked = key-maked + res-line.betrieb-gast.
        key-qty   = key-qty + res-line.erwach + res-line.kind1 + res-line.gratis.
        key-avail = key-max - key-maked.

        IF key-maked GE key-max THEN
        DO:
            mess-str = "4 - Maximum given key reached, please goto front desk!".
            RETURN.
        END.
        IF key-maked GT 0 THEN key-string = res-line.zinr + "|" + STRING(res-line.resnr) + "|" + STRING(res-line.reslinnr) + "|" + STRING(key-qty) + "|DUPKEY".
        ELSE key-string = res-line.zinr + "|" + STRING(res-line.resnr) + "|" + STRING(res-line.reslinnr) + "|" + STRING(key-qty) + "|MAINKEY".

        mess-str = "0 - Checking flag success.".
    END.
    ELSE
    DO:
        mess-str = "3 - Reservation not found! Please check parameter!".
        RETURN.
    END.
END.

/*
MESSAGE 
    "res-status   : " + STRING(res-status  ) SKIP    
    "key-maked    : " + STRING(key-maked   ) SKIP   
    "key-max      : " + STRING(key-max     ) SKIP   
    "key-avail    : " + STRING(key-avail   ) SKIP   
    "key-qty      : " + STRING(key-qty     ) SKIP   
    "key-string   : " + STRING(key-string  ) SKIP   
    "payment-flag : " + STRING(payment-flag) SKIP   
    "mess-str     : " + STRING(mess-str    ) SKIP   
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
