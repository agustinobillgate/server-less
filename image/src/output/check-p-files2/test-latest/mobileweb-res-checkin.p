DEFINE INPUT PARAMETER rsv-number      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER rsvline-number  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init       AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER new-roomno      AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER purposeOfStay   AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER email           AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER guest-phnumber  AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER guest-nation    AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER guest-country   AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER guest-region    AS CHAR.
DEFINE INPUT PARAMETER vehicle-number  AS CHAR.
DEFINE INPUT PARAMETER preAuth-string  AS CHAR.
DEFINE INPUT PARAMETER base64image     AS LONGCHAR.

DEFINE OUTPUT PARAMETER checked-in     AS LOGICAL INIT NO  NO-UNDO.
DEFINE OUTPUT PARAMETER new-resstatus  AS INTEGER          NO-UNDO. 
DEFINE OUTPUT PARAMETER result-message AS CHAR             NO-UNDO.

DEFINE VARIABLE self-ci       AS LOGICAL NO-UNDO INIT YES.
DEFINE VARIABLE can-checkin   AS LOGICAL NO-UNDO. 
DEFINE VARIABLE msg-str       AS CHAR    NO-UNDO.
DEFINE VARIABLE msg-str1      AS CHAR    NO-UNDO.
DEFINE VARIABLE msg-str2      AS CHAR    NO-UNDO.
DEFINE VARIABLE msg-str3      AS CHAR    NO-UNDO.
DEFINE VARIABLE msg-str4      AS CHAR    NO-UNDO.
DEFINE VARIABLE msg-answer    AS LOGICAL NO-UNDO.
DEFINE VARIABLE ask-deposit   AS LOGICAL NO-UNDO.
DEFINE VARIABLE keycard-flag  AS LOGICAL NO-UNDO.
DEFINE VARIABLE mcard-flag    AS LOGICAL NO-UNDO.
DEFINE VARIABLE err-number1   AS INT.
DEFINE VARIABLE err-number2   AS INT.
DEFINE VARIABLE err-number3   AS INT.
DEFINE VARIABLE err-number4   AS INT.
DEFINE VARIABLE q-143         AS LOGICAL.
DEFINE VARIABLE fill-gcfemail AS LOGICAL.
DEFINE VARIABLE gast-gastnr   AS INTEGER.
DEFINE VARIABLE flag-report   AS LOGICAL.
DEFINE VARIABLE warn-flag     AS LOGICAL.
DEFINE VARIABLE silenzio      AS LOGICAL INIT NO. 
DEFINE VARIABLE pOfStay       AS INT.
DEFINE VARIABLE pointer       AS MEMPTR NO-UNDO.
DEFINE VARIABLE tmp-zwunsch   AS CHAR    NO-UNDO.

DEFINE STREAM s1.
DEFINE STREAM s2.

IF email          EQ ? THEN email          = "".
IF guest-phnumber EQ ? THEN guest-phnumber = "".
IF guest-nation   EQ ? THEN guest-nation   = "".
IF guest-country  EQ ? THEN guest-country  = "".
IF guest-region   EQ ? THEN guest-region   = "".
IF vehicle-number EQ ? THEN vehicle-number = "".
IF preAuth-string EQ ? THEN preAuth-string = "".
IF new-roomno     EQ ? THEN new-roomno     = "".
IF base64image    EQ ? THEN base64image    = "".
 

DEFINE BUFFER rline         FOR res-line.
DEFINE BUFFER res-sharer    FOR res-line. 
DEFINE BUFFER gbuff         FOR guest.

IF user-init EQ "" OR user-init EQ ? THEN
DO:
    result-message = "5 - User Init Can't Be Null!".
    RETURN.
END.

/*
resultCd=0000&resultMsg=SUCCESS&authNo=035157&tXid=MITTEST00301202010281310035157&referenceNo=Ref20160930061456044141200251&
transDt=20201028&transTm=131003&amount=1000&recurringToken=&preauthToken=ab191d3694ea98ebadaf273fa7a5c0616003c1a24b2ac4e4ec1d2d55d38b75c4&
description=Payment+of+Invoice+No+Ref20160930061456044141200251&cardNo=524325******1567&acquBankCd=BMRI&issuBankCd=BMRI&vat=0&fee=0&notaxAmt=0
*/

DEF VAR bankName   AS CHAR.
DEF VAR noRef      AS CHAR.
DEF VAR resultMsg  AS CHAR.
DEF VAR ccNumber   AS CHAR.
DEF VAR amount     AS CHAR.
DEF VAR transdat   AS CHAR.
DEF VAR transid-merchant   AS CHAR.

DEF VAR mestoken   AS CHAR.
DEF VAR meskeyword AS CHAR.
DEF VAR mesvalue   AS CHAR.
DEF VAR loop-i     AS INT.
DEF VAR payment-string   AS CHAR.
DEF VAR payment-type     AS CHAR.
DEF VAR found-flag AS LOGICAL.
DEF VAR do-it AS LOGICAL.

DEFINE VARIABLE do-payment   AS LOGICAL INIT NO.

DEF VAR DOKU-PAYMENTDATETIME    AS CHAR.
DEF VAR DOKU-PURCHASECURRENCY   AS CHAR.
DEF VAR DOKU-LIABILITY          AS CHAR.
DEF VAR DOKU-PAYMENTCHANNEL     AS CHAR.
DEF VAR DOKU-AMOUNT             AS CHAR.
DEF VAR DOKU-PAYMENTCODE        AS CHAR.
DEF VAR DOKU-MCN                AS CHAR.
DEF VAR DOKU-WORDS              AS CHAR.
DEF VAR DOKU-RESULTMSG          AS CHAR.
DEF VAR DOKU-VERIFYID           AS CHAR.
DEF VAR DOKU-TRANSIDMERCHANT    AS CHAR.
DEF VAR DOKU-BANK               AS CHAR.
DEF VAR DOKU-STATUSTYPE         AS CHAR.
DEF VAR DOKU-APPROVALCODE       AS CHAR.
DEF VAR DOKU-EDUSTATUS          AS CHAR.
DEF VAR DOKU-THREEDSECURESTATUS AS CHAR.
DEF VAR DOKU-VERIFYSCORE        AS CHAR.
DEF VAR DOKU-CURRENCY           AS CHAR.
DEF VAR DOKU-RESPONSECODE       AS CHAR.
DEF VAR DOKU-CHNAME             AS CHAR.
DEF VAR DOKU-BRAND              AS CHAR.
DEF VAR DOKU-VERIFYSTATUS       AS CHAR.
DEF VAR DOKU-SESSIONID          AS CHAR.
DEF VAR DOKU-PAYMENTTYPE        AS CHAR.

DEF VAR QRIS-DPMALLID        AS CHAR.
DEF VAR QRIS-TRANSID         AS CHAR.
DEF VAR QRIS-AMOUNT          AS CHAR.
DEF VAR QRIS-RESULTMSG       AS CHAR.
DEF VAR QRIS-TRANSDATETIME   AS CHAR.
DEF VAR QRIS-CLIENTID        AS CHAR.
DEF VAR QRIS-TRANSIDMERCHANT AS CHAR.
DEF VAR QRIS-RESPONSECODE    AS CHAR.

DEFINE BUFFER receiver  FOR guest. 
DEFINE BUFFER mappingpg FOR queasy.
DEFINE BUFFER wcisetup  FOR queasy.

DEFINE VARIABLE vhp-artno      AS INTEGER.
DEFINE VARIABLE vhp-artdep     AS INTEGER.
DEFINE VARIABLE pg-artstring   AS CHAR.
DEFINE VARIABLE pg-artname     AS CHAR.
DEFINE VARIABLE pg-artno       AS INT.
DEFINE VARIABLE bill-date      AS DATE. 
DEFINE VARIABLE voucher-str    AS CHAR.
DEFINE VARIABLE inv-nr         AS INT.
DEFINE VARIABLE deposit-art    AS INT.
DEFINE VARIABLE errorflag      AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE deposit-pay    AS DECIMAL         NO-UNDO.
DEFINE VARIABLE deposit-exrate AS DECIMAL         NO-UNDO.

DEFINE VARIABLE mail-resno           AS INT.   
DEFINE VARIABLE mail-reslinno        AS INT.
DEFINE VARIABLE mail-transidMerchant AS CHAR.
DEFINE VARIABLE mail-datetimeTrans   AS CHAR.
DEFINE VARIABLE mail-paymentDesc     AS CHAR.
DEFINE VARIABLE mail-totalAmount     AS CHAR.

DEFINE VARIABLE post-amount AS DECIMAL.

/*DOKU
"PAYMENTDATETIME=20210402112945;PURCHASECURRENCY=360;LIABILITY=NA;PAYMENTCHANNEL=15;
AMOUNT=75000.00;PAYMENTCODE=;MCN=411111****1111;WORDS=e1263fb333d284742dcbfee17a68ca928bd84c7a;
RESULTMSG=FAILED;VERIFYID=;TRANSIDMERCHANT=000041502042021112832;BANK=Bank Mandiri;STATUSTYPE=P;
APPROVALCODE=;EDUSTATUS=NA;THREEDSECURESTATUS=TRUE;VERIFYSCORE=-1;CURRENCY=360;RESPONSECODE=00TO;
CHNAME=Arrivaldi Suandhini  MR;BRAND=VISA;VERIFYSTATUS=NA;SESSIONID=ab5e1f5b48a926eb130ba7c7bd4f57677d480dfa",
*/
/*QRIS
QRIS;DPMALLID=3236;TRANSACTIONID=323625bfb9d8919e4abb8de5a6d6eb0ea757;AMOUNT=1000.0;
RESULTMSG=SUCCESS;TRANSACTIONDATETIME=20210506141821;CLIENTID=3236;TRANSIDMERCHANT=000043506052021151710;RESPONSECODE=0000
*/
IF preAuth-string NE "" AND preAuth-string NE "CHECKROOMSTATUS" THEN
DO:
    DEF VAR paymentcode AS INT.
    payment-string = preAuth-string.
    FIND FIRST res-line WHERE res-line.resnr EQ rsv-number AND res-line.reslinnr EQ rsvline-number EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        payment-type   = ENTRY(1,payment-string,";").
        preAuth-string = SUBSTRING(payment-string,6).

        FIND FIRST queasy WHERE queasy.KEY EQ 237
        AND queasy.number1 EQ rsv-number AND queasy.number2 EQ rsvline-number EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
            queasy.char1   = payment-type
            queasy.char3   = preAuth-string               
            .
        END.
        ELSE
        DO:
            CREATE queasy.
            ASSIGN 
            queasy.KEY     = 237
            queasy.number1 = rsv-number
            queasy.number2 = rsvline-number
            queasy.char1   = payment-type
            queasy.char3   = preAuth-string
            queasy.logi1   = NO /*hold flag*/
            queasy.logi2   = NO /*posted flag*/
            .
        END.

        IF payment-type EQ "DOKU" THEN
        DO:
            paymentcode = 1.
            DO loop-i = 1 TO NUM-ENTRIES(preAuth-string,";"):
                mestoken   = ENTRY(loop-i, preAuth-string,";").
                meskeyword = ENTRY(1,mestoken,"=").
                mesvalue   = ENTRY(2,mestoken,"=").

                CASE meskeyword:                                                       /* DOKU;                                              */     
                    WHEN "PAYMENTDATETIME"    THEN DOKU-PAYMENTDATETIME    = mesvalue. /* PAYMENTDATETIME=20210914103249;                    */     
                    WHEN "PAYMENTCHANNEL"     THEN DOKU-PAYMENTCHANNEL     = mesvalue. /* PAYMENTCHANNEL=15;                                 */     
                    WHEN "AMOUNT"             THEN DOKU-AMOUNT             = mesvalue. /* AMOUNT=73810.00;                                   */     
                    WHEN "MCN"                THEN DOKU-MCN                = mesvalue. /* MCN=557338****1101;                                */     
                    WHEN "WORDS"              THEN DOKU-WORDS              = mesvalue. /* WORDS=31d6b1edba4be7805c71347d6e0b3692b2e7e8f2;    */     
                    WHEN "RESULTMSG"          THEN DOKU-RESULTMSG          = mesvalue. /* RESULTMSG=SUCCESS;                                 */     
                    WHEN "TRANSIDMERCHANT"    THEN DOKU-TRANSIDMERCHANT    = mesvalue. /* TRANSIDMERCHANT=000001213092021225115;             */     
                    WHEN "BANK"               THEN DOKU-BANK               = mesvalue. /* BANK=Bank Mandiri;                                 */     
                    WHEN "STATUSTYPE"         THEN DOKU-STATUSTYPE         = mesvalue. /* STATUSTYPE=P;                                      */     
                    WHEN "APPROVALCODE"       THEN DOKU-APPROVALCODE       = mesvalue. /* APPROVALCODE=225904;                               */   
                    WHEN "PAYMENTTYPE"        THEN DOKU-PAYMENTTYPE        = mesvalue. /* PAYMENTTYPE=SALE;                                  */   
                    WHEN "VERIFYSCORE"        THEN DOKU-VERIFYSCORE        = mesvalue. /* VERIFYSCORE=-1;                                    */     
                    WHEN "CHNAME"             THEN DOKU-CHNAME             = mesvalue. /* CHNAME=Marza Dewanta  MR;                          */     
                    WHEN "BRAND"              THEN DOKU-BRAND              = mesvalue. /* BRAND=MASTERCARD;                                  */                                          
                    WHEN "SESSIONID"          THEN DOKU-SESSIONID          = mesvalue. /* SESSIONID=278bf436dd2ed260e0edaf439639bc029d54c7ab */     
                END CASE.
            END.
            
            FIND FIRST queasy WHERE queasy.KEY EQ 223
            AND queasy.number1 EQ rsv-number AND queasy.number2 EQ rsvline-number EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                ASSIGN
                queasy.char1 = DOKU-RESULTMSG
                queasy.char2 = DOKU-TRANSIDMERCHANT + "|" + ENTRY(2,queasy.char2,"|")
                queasy.char3 = preAuth-string
                .
            END.
            ELSE
            DO:
                CREATE queasy.
                ASSIGN 
                queasy.KEY     = 223
                queasy.number1 = rsv-number
                queasy.number2 = rsvline-number
                queasy.number3 = paymentcode
                queasy.char1   = DOKU-RESULTMSG
                queasy.char2   = DOKU-TRANSIDMERCHANT
                queasy.char3   = preAuth-string
                .
            END.

            voucher-str = payment-type + "-" + DOKU-BRAND + "-" + DOKU-BANK.
            do-payment  = NO.
            IF DOKU-RESULTMSG EQ "SUCCESS" THEN do-payment = YES.
            /*IF DOKU-PAYMENTTYPE EQ "SALE"  THEN do-payment = YES.*/

            IF do-payment THEN
            DO:
                mail-transidMerchant = DOKU-TRANSIDMERCHANT. 
                mail-datetimeTrans   = SUBSTRING(DOKU-PAYMENTDATETIME,7,2) + "/" + 
                                       SUBSTRING(DOKU-PAYMENTDATETIME,5,2) + "/" + 
                                       SUBSTRING(DOKU-PAYMENTDATETIME,1,4) + " " + 
                                       SUBSTRING(DOKU-PAYMENTDATETIME,9,2) + ":" + 
                                       SUBSTRING(DOKU-PAYMENTDATETIME,11,2) + ":" + 
                                       SUBSTRING(DOKU-PAYMENTDATETIME,13,2).
                mail-paymentDesc     = CAPS(DOKU-BANK) + " " + CAPS(DOKU-BRAND).
                mail-totalAmount     = STRING(DECIMAL(DOKU-AMOUNT),"->>>,>>>.99").
                post-amount          = DECIMAL(DOKU-AMOUNT).

                FOR EACH mappingpg WHERE mappingpg.KEY EQ 224 
                    AND mappingpg.number1 EQ 1 AND mappingpg.number2 EQ 0 AND mappingpg.logi1 EQ YES NO-LOCK:
    
                    pg-artstring = DOKU-PAYMENTCHANNEL.
                    pg-artname = ENTRY(1,mappingpg.char1,"-").
                    IF pg-artstring EQ pg-artname THEN
                    DO:
                        vhp-artno  = INT(ENTRY(1,mappingpg.char3,"-")).
                        vhp-artdep = mappingpg.number2.
                        LEAVE.
                    END.
                END.
                IF vhp-artno EQ 0 THEN
                DO:
                    result-message = "9-No Mapping Found In VHP, Payment Not Posted".
                    RETURN.
                END.
            END.
        END. /*IF DOKU*/
        ELSE IF payment-type EQ "MIDTRANS" THEN
        DO:

        END.
        ELSE IF payment-type EQ "QRIS" THEN
        DO:
            paymentcode = 3.
            DO loop-i = 1 TO NUM-ENTRIES(preAuth-string,";"):
                mestoken   = ENTRY(loop-i, preAuth-string,";").
                meskeyword = ENTRY(1,mestoken,"=").
                mesvalue   = ENTRY(2,mestoken,"=").

                CASE meskeyword:                                                         
                    WHEN "DPMALLID"        THEN QRIS-DPMALLID        = mesvalue. 
                    WHEN "TRANSID"         THEN QRIS-TRANSID         = mesvalue. 
                    WHEN "AMOUNT"          THEN QRIS-AMOUNT          = mesvalue. 
                    WHEN "RESULTMSG"       THEN QRIS-RESULTMSG       = mesvalue. 
                    WHEN "TRANSDATETIME"   THEN QRIS-TRANSDATETIME   = mesvalue. 
                    WHEN "CLIENTID"        THEN QRIS-CLIENTID        = mesvalue. 
                    WHEN "TRANSIDMERCHANT" THEN QRIS-TRANSIDMERCHANT = mesvalue. 
                    WHEN "RESPONSECODE"    THEN QRIS-RESPONSECODE    = mesvalue.
                END CASE.
            END.
            
            FIND FIRST queasy WHERE queasy.KEY EQ 223
            AND queasy.number1 EQ rsv-number AND queasy.number2 EQ rsvline-number EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                ASSIGN
                queasy.char1 = QRIS-RESULTMSG
                queasy.char2 = QRIS-TRANSIDMERCHANT + "|" + ENTRY(2,queasy.char2,"|")
                queasy.char3 = preAuth-string
                .
            END.
            ELSE
            DO:
                CREATE queasy.
                ASSIGN 
                queasy.KEY     = 223
                queasy.number1 = rsv-number
                queasy.number2 = rsvline-number
                queasy.number3 = paymentcode
                queasy.char1   = QRIS-RESULTMSG
                queasy.char2   = QRIS-TRANSIDMERCHANT
                queasy.char3   = preAuth-string
                .
            END.

            voucher-str = payment-type + "-QRIS".
            do-payment  = NO.
            IF QRIS-RESULTMSG EQ "SUCCESS" THEN do-payment = YES.

            IF do-payment THEN
            DO:
                mail-transidMerchant = QRIS-TRANSIDMERCHANT. 
                mail-datetimeTrans   = SUBSTRING(QRIS-TRANSDATETIME,7,2) + "/" + 
                                       SUBSTRING(QRIS-TRANSDATETIME,5,2) + "/" + 
                                       SUBSTRING(QRIS-TRANSDATETIME,1,4) + " " + 
                                       SUBSTRING(QRIS-TRANSDATETIME,9,2) + ":" + 
                                       SUBSTRING(QRIS-TRANSDATETIME,11,2) + ":" + 
                                       SUBSTRING(QRIS-TRANSDATETIME,13,2).
                mail-paymentDesc     = "QRIS".
                mail-totalAmount     = STRING(DECIMAL(QRIS-AMOUNT),"->>>,>>>.99").
                post-amount          = DECIMAL(QRIS-AMOUNT).

                FOR EACH mappingpg WHERE mappingpg.KEY EQ 224 
                    AND mappingpg.number1 EQ 1 AND mappingpg.number2 EQ 0 AND mappingpg.logi1 EQ YES NO-LOCK:
    
                    pg-artstring = "1".
                    pg-artname = ENTRY(1,mappingpg.char1,"-").
                    IF pg-artstring EQ pg-artname THEN
                    DO:
                        vhp-artno  = INT(ENTRY(1,mappingpg.char3,"-")).
                        vhp-artdep = mappingpg.number2.
                        LEAVE.
                    END.
                END.
                IF vhp-artno EQ 0 THEN
                DO:
                    result-message = "9-No Mapping Found In VHP, Payment Not Posted".
                    RETURN.
                END.
            END.
        END.

        IF do-payment THEN
        DO:
            DEFINE VARIABLE check-payment-exist AS LOGICAL.
            DEFINE VARIABLE check-pay-str AS CHARACTER INITIAL "".
            check-payment-exist = NO.

            /* FD Comment
            FIND FIRST reservation WHERE reservation.resnr EQ rsv-number NO-LOCK.
            IF AVAILABLE reservation THEN
            DO:
                IF reservation.zahlkonto NE 0 THEN check-payment-exist = YES.
                ELSE check-payment-exist = NO.
            END.
            */               

            IF NOT check-payment-exist THEN
            DO:
                FIND FIRST wcisetup WHERE wcisetup.KEY EQ 216 
                    AND wcisetup.number1 EQ 8 
                    AND wcisetup.number2 EQ 34 NO-LOCK NO-ERROR.
                IF AVAILABLE wcisetup THEN deposit-art = INT(wcisetup.char3).

                FIND FIRST artikel WHERE artikel.artnr EQ deposit-art AND artikel.departement = 0 NO-LOCK NO-ERROR. 
                IF artikel.pricetab THEN
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ artikel.betriebsnr NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN 
                    ASSIGN deposit-exrate = waehrung.ankauf / waehrung.einheit.
                END.

                RUN res-checkin-deposit-paybl.p (deposit-art, rsv-number, vhp-artno,
                                                post-amount, - post-amount, 1, voucher-str, user-init, 
                                                OUTPUT msg-str, OUTPUT errorflag, OUTPUT deposit-pay).

                IF NOT errorflag THEN
                DO:
                    RUN sendmail(rsv-number, rsvline-number, mail-transidMerchant, mail-datetimeTrans, mail-paymentDesc, mail-totalAmount).
                END.
            END.
        END.
        result-message = "0 - Update PreAuth Success!".
        RETURN.
    END.
END.
ELSE IF preAuth-string NE "" AND preAuth-string EQ "CHECKROOMSTATUS" THEN
DO:
    can-checkin = NO.
    IF self-ci THEN silenzio = YES.                    
    RUN res-checkin1bl.p (1, rsv-number, rsvline-number, silenzio, OUTPUT can-checkin,
        OUTPUT msg-str, OUTPUT msg-str1, OUTPUT msg-str2, OUTPUT msg-str3,
        OUTPUT msg-str4, OUTPUT err-number1, OUTPUT err-number2,
        OUTPUT err-number3, OUTPUT err-number4,OUTPUT fill-gcfemail,
        OUTPUT gast-gastnr, OUTPUT q-143, OUTPUT flag-report, OUTPUT warn-flag).
    IF msg-str NE "" THEN 
    DO:
        result-message ="99 - " + msg-str. /*err code 99 -> message validation causes can't C/I*/
        RETURN.
    END.
    err-number1 = 0.
    err-number2 = 0.
    IF err-number1 NE 0 OR err-number2 NE 0 OR err-number3 NE 0 OR err-number4 NE 0 THEN 
    DO:
        IF err-number1 = 1 THEN  /*Guest country*/
        DO:
            result-message = "1 - " + msg-str1.
            RETURN.
        END.
        IF err-number2 = 1 THEN /*Guest Nation*/
        DO:
            result-message = "2 - " + msg-str2.
            RETURN.
        END.
        IF err-number3 = 1 THEN /*purpose of stay*/
        DO:
            result-message = "3 - " + msg-str3.
            RETURN.
        END.
        IF err-number4 = 1 THEN /*room number*/
        DO:
            result-message = "4 - " + msg-str4.
            RETURN.
        END.
    END.
    IF err-number1 = 0 AND err-number2 = 0 AND err-number3 = 0 AND err-number4 = 0 THEN can-checkin = YES.  
    checked-in = can-checkin.
    IF checked-in THEN result-message = "0 - Guest Can Checkin".
    ELSE result-message = "1 - Guest Can not Checkin [" + result-message + "]".
END.

IF purposeOfStay NE "" THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.char3 MATCHES "*" + purposeOfStay + "*" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    pOfStay = queasy.number1.
END.

FIND FIRST res-line WHERE res-line.resnr EQ rsv-number AND res-line.reslinnr EQ rsvline-number EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    IF pOfStay NE ? THEN
    DO:
        DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";"):
            mestoken   = ENTRY(loop-i, res-line.zimmer-wunsch,";").
            IF SUBSTR(mestoken,1,8) EQ "SEGM_PUR" THEN 
            DO:
                meskeyword  = SUBSTR(mestoken,1,8).
                mesvalue    = STRING(pOfStay).
                mestoken    = meskeyword + mesvalue.
                tmp-zwunsch = tmp-zwunsch + mestoken + ";".
                found-flag  = YES.
            END.
            ELSE
            DO:
                tmp-zwunsch = tmp-zwunsch + mestoken + ";".
            END.
        END.
        tmp-zwunsch = SUBSTRING(tmp-zwunsch,1,LENGTH(tmp-zwunsch) - 1).
        IF NOT found-flag THEN tmp-zwunsch = tmp-zwunsch + "SEGM_PUR" + STRING(pOfStay) + ";".
        ASSIGN res-line.zimmer-wunsch = tmp-zwunsch.
    END.

    found-flag = NO.
    IF vehicle-number NE "" THEN
    DO:
        DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";"):
            mestoken   = ENTRY(loop-i, res-line.zimmer-wunsch,";").
            IF ENTRY(1,mestoken,"=") EQ "VN" THEN 
            DO:
                meskeyword  = ENTRY(1,mestoken,"=").
                mesvalue    = vehicle-number.
                mestoken    = meskeyword + "=" + mesvalue.
                tmp-zwunsch = tmp-zwunsch + mestoken + ";".
                found-flag  = YES.
            END.
            ELSE
            DO:
                tmp-zwunsch = tmp-zwunsch + mestoken + ";".
            END.
        END.
        tmp-zwunsch = SUBSTRING(tmp-zwunsch,1,LENGTH(tmp-zwunsch) - 1).
        IF NOT found-flag THEN tmp-zwunsch = tmp-zwunsch + "VN=" + vehicle-number + ";".
        ASSIGN res-line.zimmer-wunsch = tmp-zwunsch.

        res-line.bemerk        = res-line.bemerk + CHR(10) + CHR(13) + "Vehicle Number = " + vehicle-number.
    END.

    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        ASSIGN 
            guest.mobil-telefon = guest-phnumber                       
            guest.nation1       = guest-nation
            guest.land          = guest-country    
            guest.geburt-ort2   = guest-region.
    
        IF email NE "" THEN
            guest.email-adr     = email.  
    END.
    
    IF base64image NE "" THEN
    DO:
        FIND FIRST guestbook WHERE guestbook.gastnr = res-line.gastnrmember NO-ERROR.
        IF NOT AVAILABLE guestbook THEN
        DO: 
            CREATE guestbook.
            ASSIGN 
            guestbook.gastnr          = res-line.gastnrmember
            guestbook.zeit            = TIME
            guestbook.userinit        = user-init
            guestbook.reserve-char[1] = STRING(TIME,"99999")
                                        + STRING(YEAR(TODAY))
                                        + STRING(MONTH(TODAY),"99") 
                                        + STRING(DAY(TODAY),"99").
        
            pointer = BASE64-DECODE(base64image).
            COPY-LOB pointer TO guestbook.imagefile.
        END.
        FIND CURRENT guestbook.
        RELEASE guestbook.
    END.

    IF res-line.zinr NE "" THEN
    DO:
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK.
        IF zimmer.zistatus NE 0 THEN 
        DO:
            result-message = "6 - Room not ready yet!".
            /*ASSIGN res-line.zimmer-wunsch = res-line.zimmer-wunsch + "MCI;".*/
            FIND CURRENT res-line NO-LOCK.
            RETURN.
        END.
    END.
    ELSE
    DO:
        result-message = "7 - Room not available yet!".
        RETURN.
    END.
    FIND CURRENT res-line.
    RELEASE res-line.
END.


IF preAuth-string EQ "" THEN
DO:
    IF self-ci THEN silenzio = YES.                    
    RUN res-checkin1bl.p (1, rsv-number, rsvline-number, silenzio, OUTPUT can-checkin,
        OUTPUT msg-str, OUTPUT msg-str1, OUTPUT msg-str2, OUTPUT msg-str3,
        OUTPUT msg-str4, OUTPUT err-number1, OUTPUT err-number2,
        OUTPUT err-number3, OUTPUT err-number4,OUTPUT fill-gcfemail,
        OUTPUT gast-gastnr, OUTPUT q-143, OUTPUT flag-report, OUTPUT warn-flag).
    IF msg-str NE "" THEN 
    DO:
        result-message ="99 - " + msg-str. /*err code 99 -> message validation causes can't C/I*/
        RETURN.
    END.
    IF err-number1 NE 0 OR err-number2 NE 0 OR err-number3 NE 0 OR err-number4 NE 0 THEN 
    DO:
        IF err-number1 = 1 THEN  /*Guest country*/
        DO:
            result-message = "1 - " + msg-str1.
            RETURN.
        END.
        IF err-number2 = 1 THEN /*Guest Nation*/
        DO:
            result-message = "2 - " + msg-str2.
            RETURN.
        END.
        IF err-number3 = 1 THEN /*purpose of stay*/
        DO:
            result-message = "3 - " + msg-str3.
            RETURN.
        END.
        IF err-number4 = 1 THEN /*room number*/
        DO:
            result-message = "4 - " + msg-str4.
            RETURN.
        END.
    END.
    IF err-number1 = 0 AND err-number2 = 0 AND err-number3 = 0 AND 
       err-number4 = 0 THEN can-checkin = YES.        
    
    IF can-checkin THEN
    DO:
        RUN res-checkin2bl.p (1, rsv-number, rsvline-number, 
             user-init, NO, OUTPUT new-resstatus, OUTPUT checked-in,
             OUTPUT ask-deposit, OUTPUT keycard-flag, OUTPUT mcard-flag,
             OUTPUT msg-str).

        FIND FIRST res-line WHERE res-line.resnr EQ rsv-number AND res-line.reslinnr EQ rsvline-number EXCLUSIVE-LOCK NO-ERROR.
        FIND FIRST res-sharer WHERE res-sharer.resnr EQ res-line.resnr 
        AND res-sharer.reslinnr NE res-line.reslinnr
        AND res-sharer.resstatus EQ 11 
        AND res-sharer.zinr EQ res-line.zinr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE res-sharer THEN 
        DO:
            result-message ="00 - " + msg-str. /*err code 00 -> message notification when C/I*/
            res-line.zimmer-wunsch = res-line.zimmer-wunsch + "MCI;".
            FIND CURRENT res-line NO-LOCK.
            RELEASE res-line.
            RETURN.
        END.
        ELSE
        DO:
            FOR EACH rline WHERE rline.resnr EQ res-line.resnr AND rline.resstatus EQ 11 
                AND rline.active-flag EQ 0 AND rline.zinr EQ res-line.zinr EXCLUSIVE-LOCK:

                IF pOfStay NE ? THEN rline.zimmer-wunsch = rline.zimmer-wunsch + "SEGM_PUR" + STRING(pOfStay) + ";".
                
                FIND FIRST guest WHERE guest.gastnr EQ rline.gastnrmember EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                DO:
                    ASSIGN 
                        guest.mobil-telefon = guest-phnumber                       
                        guest.nation1       = guest-nation
                        guest.land          = guest-country    
                        guest.geburt-ort2   = guest-region.
                
                    IF email NE "" THEN guest.email-adr = email.  
                END.

                RUN res-checkin2bl.p (1, rline.resnr, rline.reslinnr, 
                     user-init, NO, OUTPUT new-resstatus, OUTPUT checked-in,
                     OUTPUT ask-deposit, OUTPUT keycard-flag, OUTPUT mcard-flag,
                     OUTPUT msg-str).

                ASSIGN rline.zimmer-wunsch = rline.zimmer-wunsch + "MCI;".
                result-message ="00 - " + msg-str. /*err code 00 -> message notification when C/I*/
                RELEASE res-line.
            END.
        END.
    END.
END.

PROCEDURE sendmail:
    DEFINE INPUT PARAMETER resno           AS INT.
    DEFINE INPUT PARAMETER reslinno        AS INT.
    DEFINE INPUT PARAMETER transidMerchant AS CHAR.
    DEFINE INPUT PARAMETER datetimeTrans   AS CHAR.
    DEFINE INPUT PARAMETER paymentDesc     AS CHAR.
    DEFINE INPUT PARAMETER totalAmount     AS CHAR.

    DEFINE VARIABLE hotelName       AS CHAR.
    DEFINE VARIABLE hotelAddress    AS CHAR.
    DEFINE VARIABLE hotelPhone      AS CHAR.
    DEFINE VARIABLE hotelMail       AS CHAR.
    DEFINE VARIABLE hotelWeb        AS CHAR.
    DEFINE VARIABLE roomNumber      AS CHAR.
    DEFINE VARIABLE ciDate          AS CHAR.
    DEFINE VARIABLE coDate          AS CHAR.
    DEFINE VARIABLE guestName       AS CHAR.
    DEFINE VARIABLE pax             AS CHAR.
    DEFINE VARIABLE bgcolor-code    AS CHAR.

    DEFINE VARIABLE licenseNr       AS CHARACTER.
    DEFINE VARIABLE php-path        AS CHAR NO-UNDO.
    DEFINE VARIABLE temp-htm-path   AS CHAR NO-UNDO.
    DEFINE VARIABLE put-htm-path    AS CHAR NO-UNDO.

    DEFINE VARIABLE php-script      AS LONGCHAR NO-UNDO.
    DEFINE VARIABLE smtp            AS CHAR     NO-UNDO.
    DEFINE VARIABLE username        AS CHAR     NO-UNDO.
    DEFINE VARIABLE password        AS CHAR     NO-UNDO.
    DEFINE VARIABLE security        AS CHAR     NO-UNDO.
    DEFINE VARIABLE port            AS CHAR     NO-UNDO.
    DEFINE VARIABLE email-from      AS CHAR     NO-UNDO.
    DEFINE VARIABLE name-from       AS CHAR     NO-UNDO.
    DEFINE VARIABLE guestEmail      AS CHAR     NO-UNDO.
    DEFINE VARIABLE subject         AS CHAR     NO-UNDO.
    DEFINE VARIABLE body            AS LONGCHAR NO-UNDO.
    DEFINE VARIABLE textbody        AS CHAR     NO-UNDO.
    DEFINE VARIABLE outfile         AS CHAR     NO-UNDO.
    DEFINE VARIABLE outfile-tmp     AS CHAR     NO-UNDO.
    DEFINE VARIABLE strlen          AS CHAR.  
    DEFINE VARIABLE hotel-copybill  AS CHAR    NO-UNDO.

    FIND FIRST paramtext WHERE txtnr EQ 243 NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN RUN decode-string(ptexte, OUTPUT licenseNr). 
    /**/
    php-path      = "/usr1/vhp/tmp/" + licenseNr + "/send-email-selfcheckin.php".
    temp-htm-path = "/usr1/vhp/tmp/" + licenseNr + "/vhpselfcheckin-keyword.html".
    put-htm-path  = "/usr1/vhp/tmp/" + licenseNr + "/vhpselfcheckin.html".

    FOR EACH queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 8 NO-LOCK:
        IF queasy.number2 EQ 19 THEN hotelName      = queasy.char3.
        IF queasy.number2 EQ 20 THEN hotelAddress   = queasy.char3.
        IF queasy.number2 EQ 22 THEN hotelPhone     = queasy.char3.
        IF queasy.number2 EQ 23 THEN hotelMail      = queasy.char3.
        IF queasy.number2 EQ 24 THEN smtp           = queasy.char3.
        IF queasy.number2 EQ 25 THEN port           = queasy.char3.
        IF queasy.number2 EQ 26 THEN username       = queasy.char3.
        IF queasy.number2 EQ 27 THEN password       = queasy.char3.
        IF queasy.number2 EQ 28 THEN security       = queasy.char3.
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 7 AND queasy.number2 EQ 2 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN hotelWeb = queasy.char3.
    FIND FIRST queasy WHERE queasy.KEY EQ 222 
        AND queasy.number1 EQ 1 
        AND queasy.number2 EQ 3
        AND queasy.betriebsnr EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN bgcolor-code = queasy.char2.

    FIND FIRST queasy WHERE queasy.KEY EQ 222 
        AND queasy.number1 EQ 1 
        AND queasy.number2 EQ 20
        AND queasy.betriebsnr EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN hotel-copybill = queasy.char2.


    FIND FIRST res-line WHERE res-line.resnr EQ resno AND res-line.reslinnr EQ reslinno NO-LOCK NO-ERROR.           
    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
    guestEmail = guest.email-adr.
    roomNumber = res-line.zinr.     
    ciDate     = STRING(res-line.ankunft).     
    coDate     = STRING(res-line.abreise).     
    guestName  = res-line.NAME.     
    pax        = STRING(res-line.erwachs).     
    name-from  = "FrontOffice @" + CAPS(hotelName). 
    subject    = "E-Invoice Deposit Payment @" + hotelname + "-" + transidMerchant.

    IF SEARCH(php-path) NE ? THEN OS-DELETE VALUE(php-path).
    outfile-tmp = temp-htm-path.
    outfile     = put-htm-path.
    
    OUTPUT STREAM s1 TO VALUE(outfile).
    INPUT STREAM s2 FROM VALUE(outfile-tmp).

    REPEAT:
        textbody = "".
        strlen   = "".
        IMPORT STREAM s2 UNFORMATTED textbody.
        /*===========HEADER==============*/
        
        IF textbody MATCHES ("*$bgColor*") THEN /*=OK=*/
        DO:
            textbody = ENTRY(1, textbody, "$") + " " + bgcolor-code + ";".
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$totalAmount*") THEN /*=OK=*/
        DO:
            textbody = "Rp " + totalAmount. 
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$hotelName*") THEN /*=OK=*/ 
        DO:
            textbody = hotelname.
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$hotelAddress*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + hoteladdress + " " + SUBSTRING(ENTRY(2, textbody, "$"),13).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*Phone*") THEN /*=OK=*/
        DO:
            textbody = "Phone: " +  hotelPhone + " | Email: " + hotelMail.
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$hotelWeb*") THEN /*=OK=*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelWeb + " " + SUBSTRING(ENTRY(2, textbody, "$"),9).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$transIdMerchant*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + transidMerchant + " " + SUBSTRING(ENTRY(2, textbody, "$"),16).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$dateTimeTrans*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + datetimeTrans + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$resno*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + STRING(resno) + " " + SUBSTRING(ENTRY(2, textbody, "$"),6).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$roomno*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + roomNumber + " " + SUBSTRING(ENTRY(2, textbody, "$"),7).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$cidate*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + ciDate + " " + SUBSTRING(ENTRY(2, textbody, "$"),7).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$codate*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + coDate + " " + SUBSTRING(ENTRY(2, textbody, "$"),7).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$guestName*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + guestName + " " + SUBSTRING(ENTRY(2, textbody, "$"),10).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$adult*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + pax + " " + SUBSTRING(ENTRY(2, textbody, "$"),6).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$depositAMount*") THEN /*=OK=*/
        DO:
            textbody = ENTRY(1, textbody, "$") + totalAmount + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$grandTotalAmount*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + totalAmount + SUBSTRING(ENTRY(2, textbody, "$"),17).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END. 
        ELSE IF textbody MATCHES ("*paymentTotalAmount*") THEN /*=OK=*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + "-" + totalAmount + SUBSTRING(ENTRY(2, textbody, "$"),19).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END. 
        ELSE IF textbody MATCHES ("*$paymentDescription*") THEN /*=OK=*/
        DO:
            textbody = ENTRY(1, textbody, "$") + paymentDesc + " " + SUBSTRING(ENTRY(2, textbody, "$"),19).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$paymentAmount*") THEN /*=OK=*/
        DO:
            textbody = ENTRY(1, textbody, "$") + "-" + totalAmount + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE
        DO:
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
    END.
    OUTPUT STREAM s1 CLOSE.
    INPUT STREAM s2 CLOSE.
    COPY-LOB FILE outfile TO body.
    php-script =
        "<?php"                                                           + CHR(10) +
        "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + CHR(10) +
        "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';"        + CHR(10) +
        "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';"   + CHR(10) +
        "$mail = new PHPMailer;"                                          + CHR(10) +
        "$mail->isSMTP();"                                                + CHR(10) +
        "$mail->Host = '" + smtp + "';"                                   + CHR(10) +
        "$mail->SMTPAuth = true;"                                         + CHR(10) +
        "$mail->Username = '" + username + "';"                           + CHR(10) +
        "$mail->Password = '" + password + "';"                           + CHR(10) +
        "$mail->SMTPSecure = '" + security + "';"                         + CHR(10) +
        "$mail->Port = " + port + ";"                                     + CHR(10) +
        "$mail->setFrom('" + username + "', '" + name-from + "');"        + CHR(10) +
        "$mail->addAddress('" + guestEmail + "');"                        + CHR(10) +
        "$mail->addCC('" + hotel-copybill + "');"                         + CHR(10) +
        "$mail->isHTML(true);"                                            + CHR(10) +
        "$mail->Subject = '" + subject + "';"                             + CHR(10) +
        "$mail->Body = '" + body + "';"                                   + CHR(10) +
        "if(!$mail->send()) " + CHR(123)                                  + CHR(10) +
        "    echo 'Message could not be sent.';"                          + CHR(10) +
        "    echo 'Mailer Error: ' . $mail->ErrorInfo;"                   + CHR(10) +
        CHR(125) + " else " + CHR(123)                                    + CHR(10) +
        "    echo 'Message has been sent';"                               + CHR(10) +
        CHR(125)                                                          + CHR(10) + 
        "?>"                                                              + CHR(10) 
        .
    COPY-LOB php-script TO FILE php-path.
    OS-COMMAND VALUE("php " + php-path).
END.


PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
      s = in-str. 
      j = ASC(SUBSTR(s, 1, 1)) - 70. 
      len = LENGTH(in-str) - 1. 
      s = SUBSTR(in-str, 2, len). 
      DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
      END. 
END.
