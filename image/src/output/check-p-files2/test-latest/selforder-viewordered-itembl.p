/*CURRENT-WINDOW:WIDTH = 199.*/
DEFINE TEMP-TABLE ordered-item    
    FIELD table-nr      AS INTEGER  
    FIELD order-nr      AS INTEGER  
    FIELD nr            AS INTEGER FORMAT ">>>" LABEL "No"
    FIELD bezeich       AS CHARACTER FORMAT "x(35)"
    FIELD qty           AS INTEGER FORMAT "->>>" 
    FIELD sp-req        AS CHARACTER FORMAT "x(40)"
    FIELD confirm       AS LOGICAL
    FIELD remarks       AS CHAR FORMAT "x(20)" LABEL "Remarks"
    FIELD order-date    AS CHAR 
    FIELD price         AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD subtotal      AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD subtotalprice AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD artnr         AS INT
    FIELD service       AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD tax           AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD bill-date     AS DATE
    FIELD order-status  AS CHAR
    FIELD count-amount  AS LOGICAL
    FIELD posted        AS LOGICAL
    FIELD article-type  AS CHAR /*SALES,PAYMENT,DISCOUNT FOOD,BEV,OTHER,VOUCHER,VOID,DEPOSIT*/
    FIELD priceTaxServ  AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD webpost-flag  AS LOGICAL
    FIELD hbline-recid  AS INT
    FIELD hbline-time   AS INT
    FIELD item-str      AS CHAR
    FIELD bline-str     AS CHAR
    FIELD amount        AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD cancel-str    AS CHARACTER
    .
/**/
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER dept AS INT.
DEFINE INPUT PARAMETER table-no AS INT.
DEFINE INPUT PARAMETER session-parameter AS CHAR.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER user-name AS CHAR.
DEFINE OUTPUT PARAMETER dept-name AS CHAR.
DEFINE OUTPUT PARAMETER guest-name AS CHAR.
DEFINE OUTPUT PARAMETER pax AS INT.
DEFINE OUTPUT PARAMETER room AS CHAR.
DEFINE OUTPUT PARAMETER total-tax AS DECIMAL FORMAT "->>>,>>>,>>>,>>>".
DEFINE OUTPUT PARAMETER total-service AS DECIMAL FORMAT "->>>,>>>,>>>,>>>".
DEFINE OUTPUT PARAMETER total-price AS DECIMAL FORMAT "->>>,>>>,>>>,>>>".
DEFINE OUTPUT PARAMETER total-payment AS DECIMAL FORMAT "->>>,>>>,>>>,>>>".
DEFINE OUTPUT PARAMETER grand-total AS DECIMAL FORMAT "->>>,>>>,>>>,>>>".
DEFINE OUTPUT PARAMETER sessionExpired AS LOGICAL.
DEFINE OUTPUT PARAMETER hold-payment AS LOGICAL.
DEFINE OUTPUT PARAMETER bill-number AS INT.
DEFINE OUTPUT PARAMETER payment-method AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR ordered-item.
/**/
/*
DEFINE VAR user-init AS CHAR.
DEFINE VAR dept AS INT.
DEFINE VAR table-no AS INT.
DEFINE VAR session-parameter AS CHAR.

DEFINE VAR mess-result    AS CHAR.
DEFINE VAR user-name      AS CHAR.
DEFINE VAR dept-name      AS CHAR.
DEFINE VAR guest-name     AS CHAR.
DEFINE VAR pax            AS INT.
DEFINE VAR room           AS CHAR.
DEFINE VAR total-tax      AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>>".
DEFINE VAR total-service  AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>>".
DEFINE VAR total-price    AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>>".
DEFINE VAR total-payment  AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>>".
DEFINE VAR grand-total    AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>>".
DEFINE VAR sessionExpired AS LOGICAL.
DEFINE VAR hold-payment   AS LOGICAL.
DEFINE VAR bill-number    AS INT.
DEFINE VAR payment-method AS CHAR.

user-init = "01".
dept = 1.
table-no = 50.
session-parameter = "541".
*/
/*=====================*/

IF session-parameter EQ ? OR session-parameter EQ "" THEN
DO:
    mess-result = "1-Session Parameter can't be null value!".
    RETURN.
END.
IF dept EQ ? OR dept EQ 0 THEN
DO:
    mess-result = "1-Department can't be null value!".
    RETURN.
END.
IF user-init EQ ? OR user-init EQ "" THEN
DO:
    mess-result = "1-User Initials can't be null value!".
    RETURN.
END.

DEFINE VARIABLE mess-str AS CHAR.
DEFINE VARIABLE i-str AS INT.
DEFINE VARIABLE mess-token AS CHAR.
DEFINE VARIABLE mess-keyword AS CHAR.
DEFINE VARIABLE mess-value AS CHAR.

DEFINE VARIABLE orderdatetime AS CHAR.
DEFINE VARIABLE gname AS CHAR.

DEFINE VARIABLE order-i AS INT.

DEFINE VARIABLE serv%        AS DECIMAL INITIAL 0.  
DEFINE VARIABLE mwst%        AS DECIMAL INITIAL 0.  
DEFINE VARIABLE fact         AS DECIMAL INITIAL 1.   
DEFINE VARIABLE mmwst1       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE mwst         AS DECIMAL INITIAL 0. 
DEFINE VARIABLE h-service    AS DECIMAL.  
DEFINE VARIABLE h-mwst       AS DECIMAL.  
DEFINE VARIABLE incl-service AS LOGICAL.  
DEFINE VARIABLE incl-mwst    AS LOGICAL.
DEFINE VARIABLE gst-logic    AS LOGICAL INITIAL NO.
DEFINE VARIABLE serv-disc    AS LOGICAL INITIAL YES.
DEFINE VARIABLE vat-disc     AS LOGICAL INITIAL YES.
DEFINE VARIABLE f-discArt    AS INTEGER INITIAL -1 NO-UNDO. 
DEFINE VARIABLE amount       AS DECIMAL. 
/* DEFINE VARIABLE bill-number  AS INTEGER NO-UNDO. */
DEFINE VARIABLE price-decimal AS INTEGER.   

DEFINE VARIABLE tax         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE serv        AS DECIMAL NO-UNDO.
DEFINE VARIABLE service     AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat         AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE vat2        AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE fact-scvat  AS DECIMAL NO-UNDO INIT 1.
DEFINE VARIABLE serv-vat    AS LOGICAL NO-UNDO. 
DEFINE VARIABLE tax-vat     AS LOGICAL NO-UNDO.
DEFINE VARIABLE ct          AS CHARACTER NO-UNDO.
DEFINE VARIABLE l-deci      AS INTEGER NO-UNDO INIT 2.
DEFINE VARIABLE tot-amount  AS DECIMAL NO-UNDO.   

DEFINE VARIABLE bill-date110 AS DATE.  
DEFINE VARIABLE bill-date    AS DATE. 

DEFINE VARIABLE service-taxable AS LOGICAL NO-UNDO.
DEFINE VARIABLE sesion-id AS CHAR.
DEFINE VARIABLE servtax-use-foart AS LOGICAL.
DEFINE VARIABLE dynamic-qr  AS LOGICAL.
DEFINE VARIABLE room-serviceflag  AS LOGICAL.
DEFINE VARIABLE rm-no AS CHARACTER.
DEFINE VARIABLE str1 AS CHARACTER.
DEFINE VARIABLE count-i AS INT.
DEFINE VARIABLE alpha-flag AS LOGICAL.

DEFINE BUFFER bqsy FOR queasy.
DEFINE BUFFER bposted FOR queasy.
DEFINE BUFFER qrqsy FOR queasy.
DEFINE BUFFER queasyorderbill FOR queasy.
DEFINE BUFFER orderbill FOR queasy.
DEFINE BUFFER orderbill-line FOR queasy.
DEFINE BUFFER orderbill-posted FOR queasy.
DEFINE BUFFER bufforder FOR ordered-item.
DEFINE BUFFER sosqsy FOR queasy.
DEFINE BUFFER q-takentable FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr = 468 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN serv-disc = htparam.flogic.
FIND FIRST htparam WHERE htparam.paramnr = 469 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN vat-disc = htparam.flogic.
FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. /*rest food disc artNo */   
IF vhp.htparam.finteger NE 0 THEN f-discArt = vhp.htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr = 376 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    IF NOT htparam.flogic AND ENTRY(1,htparam.fchar,";") = "GST(MA)" THEN
    gst-logic = YES.
END.
FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
incl-service = vhp.htparam.flogical. 
FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
incl-mwst = vhp.htparam.flogical. 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
service-taxable = vhp.htparam.flogical. 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK.   
price-decimal = vhp.htparam.finteger.

FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN user-name = CAPS(bediener.username).

FIND FIRST hoteldpt WHERE hoteldpt.num EQ dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN
DO:
    dept-name = CAPS(hoteldpt.depart).
    servtax-use-foart = hoteldpt.defult. /*FD July 14, 2022*/
END.    

FIND FIRST qrqsy WHERE qrqsy.KEY EQ 230 AND qrqsy.char1 = session-parameter NO-LOCK NO-ERROR.
IF AVAILABLE qrqsy THEN sessionExpired = qrqsy.logi1.

/*FDL March 16, 2023 => Ticket 490301 - validate for room no numeric + alphabet*/
FOR EACH sosqsy WHERE sosqsy.KEY EQ 222 AND sosqsy.number1 EQ 1 
    AND sosqsy.betriebsnr EQ dept NO-LOCK:
    IF sosqsy.number2 EQ 14 THEN dynamic-qr = sosqsy.logi1.
    IF sosqsy.number2 EQ 21 THEN room-serviceflag = sosqsy.logi1.
END.

IF room-serviceflag THEN
DO:
    FIND FIRST q-takentable WHERE q-takentable.KEY EQ 225
        AND q-takentable.char1 EQ "taken-table"
        AND q-takentable.number2 EQ table-no
        AND ENTRY(1, q-takentable.char3, "|") EQ session-parameter
        AND NUM-ENTRIES(q-takentable.char3, "|") EQ 3 NO-LOCK NO-ERROR.
    IF AVAILABLE q-takentable THEN 
    DO:
        str1 = ENTRY(3, q-takentable.char3, "|").
        rm-no = ENTRY(1, str1, "$").
    END.

    IF rm-no NE "" THEN
    DO:
        DO count-i = 65 TO 90:
            IF rm-no MATCHES ("*" + CHR(count-i) + "*") THEN alpha-flag = YES.
        END.
        IF NOT alpha-flag THEN 
        DO:
            count-i = 0.
            DO count-i = 97 TO 122:
                IF rm-no MATCHES ("*" + CHR(count-i) + "*") THEN alpha-flag = YES.
            END.
        END.
    END.

    IF alpha-flag THEN
    DO:
        FIND FIRST tisch WHERE tisch.departement EQ dept
            AND tisch.tischnr EQ table-no NO-LOCK NO-ERROR.
        IF AVAILABLE tisch THEN 
        DO:        
            room = SUBSTRING(tisch.bezeich,6).
        END.
    END.
    ELSE
    DO:
        room = STRING(table-no).
    END.
END.
/*End FDL*/

RUN query-order.
IF mess-result EQ "1-No order found!" THEN
DO:
    DEF VAR found-bill AS INT.
    DEF VAR billno     AS INT.
    DEF VAR do-it      AS LOGICAL INITIAL NO. /*FD*/

    billno = INT(session-parameter) NO-ERROR.

    IF billno NE 0 AND billno NE ? THEN
    DO:
        do-it = YES. 
    END.

    IF do-it THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY EQ 225 
            AND queasy.number1 EQ dept 
            AND queasy.char1 EQ "orderbill" NO-LOCK:
    
            mess-str = queasy.char2.
            DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
                mess-token = ENTRY(i-str,mess-str,"|").
                mess-keyword = ENTRY(1,mess-token,"=").
                mess-value = ENTRY(2,mess-token,"=").
                IF mess-keyword EQ "BL" THEN
                DO: 
                    found-bill = INT(mess-value).
                    LEAVE.
                END.
            END.
            IF found-bill EQ billno THEN
            DO: 
                session-parameter = queasy.char3.
                LEAVE.
            END.
            ELSE
            DO:
                mess-result = "1-No order found!".
            END.
        END.
        RUN query-order. 
    END.    
END.
FOR EACH ordered-item BY ordered-item.order-nr:
    IF order-i NE ordered-item.order-nr THEN order-i = ordered-item.order-nr.
    FOR EACH bufforder WHERE bufforder.order-nr EQ order-i /*EXCLUSIVE-LOCK*/ NO-LOCK:
        ordered-item.subtotalprice = ordered-item.subtotalprice + bufforder.subtotal.
    END.    
END.

/*CALCULATE TAX N SERVICE*/
FOR EACH ordered-item WHERE ordered-item.count-amount = YES BY ordered-item.order-nr:
    FIND FIRST h-artikel WHERE h-artikel.departement EQ dept AND h-artikel.artnr EQ ordered-item.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
        mmwst1    = 0.
        h-service = 0.
        h-mwst    = 0.
        service   = 0.
        mwst      = 0.

        RUN cal-servat (h-artikel.departement, h-artikel.artnr,  
                        h-artikel.service-code, h-artikel.mwst-code, ordered-item.bill-date, 
                        OUTPUT serv%, OUTPUT mwst%, OUTPUT fact). 

        /*amount = ordered-item.subtotal * (1 + serv% + mwst% + service).*/
        amount = ordered-item.price * (1 + serv% + mwst% + service).
        
        IF NOT serv-disc AND h-artikel.artnr EQ f-discArt THEN.
        ELSE
        ASSIGN
            h-service = amount / fact * serv%
            h-service = ROUND(h-service,2).

        IF NOT vat-disc AND h-artikel.artnr EQ f-discArt THEN.
        ELSE 
        ASSIGN
            h-mwst = amount / fact * mwst%
            h-mwst = ROUND(h-mwst,2).

        IF NOT incl-service THEN   
        ASSIGN  
            amount  = amount - h-service 
            service = service + h-service  
        .  
        IF NOT incl-mwst THEN   
        ASSIGN  
            amount = amount - h-mwst 
            mwst   = mwst   + h-mwst  
            mmwst1  = mmwst1  + h-mwst  
        .  
        ordered-item.service = service. 
        ordered-item.tax     = mmwst1.

        IF ordered-item.service EQ ? THEN ordered-item.service = 0.
        IF ordered-item.tax EQ ? THEN ordered-item.tax = 0.

        ordered-item.service = ordered-item.service * ordered-item.qty.
        ordered-item.tax = ordered-item.tax * ordered-item.qty.

        IF ordered-item.article-type EQ "VOID" THEN
        DO:
            ordered-item.price    = ordered-item.price / ordered-item.qty.
            ordered-item.service  = ordered-item.service / ordered-item.qty.
            ordered-item.tax      = ordered-item.tax / ordered-item.qty.
            ordered-item.subtotal = ordered-item.price * ordered-item.qty.

            ordered-item.price    = ordered-item.price.
            ordered-item.subtotal = ordered-item.subtotal.
            ordered-item.service  = ordered-item.service.
            ordered-item.tax      = ordered-item.tax    .
        END.
        IF (ordered-item.article-type EQ "SALES" OR ordered-item.article-type EQ "VOID") THEN
            ordered-item.priceTaxServ = (ordered-item.price * ordered-item.qty) + ordered-item.service + ordered-item.tax.
        ELSE 
            ordered-item.priceTaxServ = ordered-item.subtotal.
    END.
    IF (ordered-item.article-type MATCHES "*PAYMENT*" 
        OR ordered-item.article-type MATCHES "*VOUCHER*"
        OR ordered-item.article-type MATCHES "*DEPOSIT*") THEN /*FDL Dec 29, 2022 - Deposit Resto*/
    DO:
        ordered-item.tax = 0.
        ordered-item.service = 0.
    END.
    total-price   = total-price + ordered-item.subtotal.
    total-tax     = total-tax + ordered-item.tax.   
    total-service = total-service + ordered-item.service.

END.
total-price   = INT(ROUND(total-price,2)).  
total-tax     = total-tax - 0.01.
total-tax     = INT(ROUND(total-tax,2)). 
total-service = INT(ROUND(total-service,2)).
/*grand-total   = INT(ROUND(total-price + total-tax + total-service,2)).*/
grand-total   = INT(ROUND(tot-amount, 2)).
/*
IF price-decimal EQ 2 THEN
DO:
    total-price   = DEC(ROUND(total-price,2)).  
    /*total-tax     = total-tax - 0.01.*/
    total-tax     = DEC(ROUND(total-tax,2)). 
    total-service = DEC(ROUND(total-service,2)).
    /*grand-total   = INT(ROUND(total-price + total-tax + total-service,2)).*/
    grand-total   = INT(ROUND(tot-amount, 2)).
END.
ELSE
DO:
    total-price   = INT(ROUND(total-price,2)).  
    /*total-tax     = total-tax - 0.01.*/
    total-tax     = INT(ROUND(total-tax,2)). 
    total-service = INT(ROUND(total-service,2)).
    /*grand-total   = INT(ROUND(total-price + total-tax + total-service,2)).*/
    grand-total   = INT(ROUND(tot-amount, 2)).
END.
*/
/*==============================================================*/
PROCEDURE query-order:
    DEFINE VARIABLE posted-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE itemposted-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE bill-nr AS INT.

    DEFINE BUFFER searchbill FOR queasy.
    DEFINE BUFFER mergebill FOR queasy.

    /*
    FIND FIRST searchbill WHERE searchbill.KEY EQ 225 
            AND searchbill.number1 EQ dept 
            AND searchbill.char1 EQ "orderbill" 
            AND searchbill.char3 EQ session-parameter 
            AND searchbill.betriebsnr NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE searchbill THEN
    DO:
        DEF VAR get-bill AS INT.
        DEF VAR get-betrieb AS INT.
        mess-str = searchbill.char2.
        DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
            mess-token = ENTRY(i-str,mess-str,"|").
            mess-keyword = ENTRY(1,mess-token,"=").
            mess-value = ENTRY(2,mess-token,"=").
            IF mess-keyword EQ "BL" THEN get-bill = INT(mess-value).
        END.
        get-betrieb = searchbill.betriebsnr.

        FOR EACH mergebill WHERE mergebill.KEY EQ 225
            AND mergebill.number1 EQ dept 
            AND mergebill.char1 EQ "orderbill" 
            AND mergebill.char3 EQ session-parameter 
            AND mergebill.betriebsnr EQ 0 EXCLUSIVE-LOCK:
            ASSIGN 
                mergebill.char2 = mergebill.char2 + "|BL=" + STRING(get-bill)
                mergebill.betriebsnr = get-betrieb.
        END.
    END.*/

    FIND FIRST searchbill WHERE searchbill.KEY EQ 225 
        AND searchbill.number1 EQ dept 
        AND searchbill.char1 EQ "orderbill" 
        AND searchbill.char3 EQ session-parameter
        AND searchbill.number3 NE 0 NO-LOCK NO-ERROR.   /*FD validation if posting from dekstop first*/         
    IF AVAILABLE searchbill THEN
    DO:        
        mess-str = searchbill.char2.
        DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
            mess-token = ENTRY(i-str,mess-str,"|").
            mess-keyword = ENTRY(1,mess-token,"=").
            mess-value = ENTRY(2,mess-token,"=").
            IF mess-keyword EQ "RN" THEN room = mess-value.
            ELSE IF mess-keyword EQ "PX" THEN pax = INT(mess-value).
            ELSE IF mess-keyword EQ "NM" THEN gname = mess-value.
            ELSE IF mess-keyword EQ "DT" THEN orderdatetime = mess-value.
            ELSE IF mess-keyword EQ "BL" THEN bill-number = INT(mess-value).
        END.        

        FOR EACH orderbill WHERE orderbill.KEY EQ 225 
            AND orderbill.number1 EQ dept 
            AND orderbill.char1 EQ "orderbill" 
            AND orderbill.char3 EQ session-parameter 
            AND orderbill.logi1 EQ YES NO-LOCK BY orderbill.number2:

            mess-str = orderbill.char2.
            DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
                mess-token = ENTRY(i-str,mess-str,"|").
                mess-keyword = ENTRY(1,mess-token,"=").
                mess-value = ENTRY(2,mess-token,"=").
                IF mess-keyword EQ "BL" THEN bill-nr = INT(mess-value).
            END.
            IF bill-nr NE 0 THEN 
            DO:
                bill-number = bill-nr.
                posted-flag = YES.                
                LEAVE.
            END.
        END.
       
        FOR EACH orderbill WHERE orderbill.KEY EQ 225 
            AND orderbill.number1 EQ dept 
            AND orderbill.char1 EQ "orderbill" 
            AND orderbill.char3 EQ session-parameter 
            AND orderbill.logi1 EQ YES NO-LOCK BY orderbill.number2 BY orderbill.number3:
    
            mess-str = orderbill.char2.
            DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
                mess-token = ENTRY(i-str,mess-str,"|").
                mess-keyword = ENTRY(1,mess-token,"=").
                mess-value = ENTRY(2,mess-token,"=").
                IF mess-keyword EQ "DT" THEN orderdatetime = mess-value.
            END. 

            FOR EACH orderbill-line WHERE orderbill-line.KEY EQ 225 
                AND orderbill-line.char1 EQ "orderbill-line"
                AND orderbill-line.number2 EQ orderbill.number2 
                AND orderbill-line.number1 EQ orderbill.number3
                AND orderbill-line.date1 EQ orderbill.date1
                AND ENTRY(3, orderbill-line.char2, "|") EQ orderdatetime
                NO-LOCK BY orderbill-line.number1:     

                total-payment = orderbill.deci1.
                guest-name = CAPS(gname).
                itemposted-flag = orderbill.logi3.

                IF NUM-ENTRIES (orderbill-line.char2,"|") GE 4 THEN sesion-id = ENTRY(4,orderbill-line.char2,"|").

                IF sesion-id EQ session-parameter THEN
                DO:   
                    mess-str = orderbill-line.char3.

                    FIND FIRST ordered-item WHERE ordered-item.item-str EQ orderbill-line.char3 
                        AND ordered-item.bline-str EQ orderbill-line.char2 NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE ordered-item THEN
                    DO:
                        /* DISP sesion-id FORMAT "x(30)"
                         session-parameter FORMAT "x(30)"
                         orderbill-line.number1
                         ENTRY(3,mess-str,"|")
                         orderbill-line.logi3
                         orderbill-line.char3 FORMAT "x(50)" WITH WIDTH 180.*/

                        CREATE ordered-item.
                        ASSIGN ordered-item.table-nr     = orderbill.number2   
                               ordered-item.order-nr     = orderbill-line.number1
                               ordered-item.bezeich      = ENTRY(3,mess-str,"|")
                               ordered-item.qty          = INT(ENTRY(4,mess-str,"|"))
                               ordered-item.sp-req       = ENTRY(6,mess-str,"|")
                               ordered-item.confirm      = orderbill-line.logi2 /*old logi3*/
                               ordered-item.remarks      = ""
                               ordered-item.order-date   = ENTRY(3,orderbill-line.char2,"|")
                               ordered-item.nr           = orderbill-line.number3
                               ordered-item.price        = DEC(ENTRY(5,mess-str,"|"))  
                               ordered-item.subtotal     = ordered-item.price * ordered-item.qty
                               ordered-item.artnr        = INT(ENTRY(2,mess-str,"|"))
                               ordered-item.bill-date    = orderbill.date1
                               ordered-item.posted       = /*posted-flag*/ orderbill-line.logi3
                               ordered-item.article-type = "SALES"
                               ordered-item.item-str     = orderbill-line.char3
                               ordered-item.bline-str    = orderbill-line.char2
                               ordered-item.webpost-flag = YES.
        
                        IF NUM-ENTRIES (orderbill-line.char3,"|") GE 7 THEN
                        DO:
                            ASSIGN
                                ordered-item.hbline-recid = INT(ENTRY(7,orderbill-line.char3,"|"))
                                ordered-item.hbline-time  = INT(ENTRY(8,orderbill-line.char3,"|"))                               
                                /*ordered-item.posted       = YES
                                ordered-item.confirm      = YES*/
                                .

                            /*FD May 18, 2022*/
                            IF NUM-ENTRIES (orderbill-line.char3,"|") GE 9 THEN
                            DO:
                                ordered-item.cancel-str = ENTRY(9,orderbill-line.char3,"|").
                            END.
                        END.
                            
        
                        /*IF ordered-item.posted EQ NO THEN
                        DO:
                            ASSIGN 
                                ordered-item.order-status = "WAIT FOR WAITER CONFIRM"
                                ordered-item.sp-req       = "WAIT FOR WAITER CONFIRM" + " - " + ordered-item.sp-req
                                ordered-item.count-amount = NO.
                        END.
                        ELSE IF ordered-item.posted EQ YES THEN
                        DO:
                            
                            IF ordered-item.confirm EQ NO THEN 
                            DO:
                                ordered-item.price        = 0.  
                                ordered-item.subtotal     = 0.
                                ordered-item.order-status = "ORDER CANCELED".
                                ordered-item.sp-req       = "ORDER CANCELED" + " - " + ordered-item.sp-req.
                                ordered-item.count-amount = NO.
                            END.
                            ELSE 
                                ASSIGN 
                                    ordered-item.order-status = "ORDER POSTED"
                                    ordered-item.sp-req       = "ORDER POSTED" + " - " + ordered-item.sp-req
                                    ordered-item.count-amount = YES.
                            */
                        IF itemposted-flag EQ NO THEN
                        DO:
                            ASSIGN 
                                ordered-item.order-status = "WAIT FOR WAITER CONFIRM"
                                ordered-item.sp-req       = "WAIT FOR WAITER CONFIRM" + " - " + ordered-item.sp-req
                                ordered-item.count-amount = NO.
                        END.
                        ELSE IF itemposted-flag EQ YES THEN
                        DO:
                            IF ordered-item.confirm EQ NO THEN 
                            DO:
                                ordered-item.price        = 0.  
                                ordered-item.subtotal     = 0.
                                ordered-item.order-status = "ORDER CANCELED".
                                ordered-item.sp-req       = "ORDER CANCELED" + " - " + ordered-item.sp-req.
                                ordered-item.count-amount = NO.
                            END.
                            ELSE 
                                ASSIGN 
                                    ordered-item.order-status = "ORDER POSTED"
                                    ordered-item.sp-req       = "ORDER POSTED" + " - " + ordered-item.sp-req
                                    ordered-item.count-amount = YES.
                        END.
                    END.
                END.
            END.
        END.

        IF bill-number NE 0 THEN
        DO:            
            DEFINE VARIABLE art-type      AS CHAR.
            DEFINE VARIABLE art-discfood  AS INT.
            DEFINE VARIABLE art-discbev   AS INT.
            DEFINE VARIABLE art-discother AS INT.
            DEFINE VARIABLE art-voucher   AS INT.
            DEFINE VARIABLE art-paycash   AS INT.
            DEFINE VARIABLE art-cc        AS CHAR.
            DEFINE VARIABLE loop-cc       AS INT.
            DEFINE VARIABLE art-cl        AS CHAR.
            DEFINE VARIABLE loop-cl       AS INT.
            DEFINE VARIABLE art-paycc     AS INT.
            DEFINE VARIABLE art-paycl     AS INT.
            DEFINE VARIABLE art-reczeit   AS CHAR.
            DEFINE VARIABLE do-it         AS LOGICAL.
        
            FIND FIRST htparam WHERE paramnr EQ 557 NO-LOCK NO-ERROR.
            art-discfood = htparam.finteger.
            FIND FIRST htparam WHERE paramnr EQ 596 NO-LOCK NO-ERROR.
            art-discbev = htparam.finteger.
            FIND FIRST htparam WHERE paramnr EQ 556 NO-LOCK NO-ERROR.
            art-discother = htparam.finteger.
            FIND FIRST htparam WHERE paramnr EQ 1001 NO-LOCK NO-ERROR.
            art-voucher = htparam.finteger. 
            FIND FIRST htparam WHERE paramnr EQ 855 NO-LOCK NO-ERROR.
            art-paycash = htparam.finteger. 
            FOR EACH h-artikel WHERE h-artikel.departement = dept 
                AND h-artikel.artart = 7 
                AND h-artikel.activeflag NO-LOCK:
                art-cc = art-cc + STRING(h-artikel.artnr) + ":" .
            END.
            /*FD*/
            FOR EACH h-artikel WHERE h-artikel.departement = dept 
                AND h-artikel.artart = 2 
                AND h-artikel.activeflag NO-LOCK:
                art-cl = art-cl + STRING(h-artikel.artnr) + ";" .
            END.
            FIND FIRST h-bill WHERE h-bill.departement EQ dept AND h-bill.rechnr EQ bill-number NO-LOCK NO-ERROR.
            IF AVAILABLE h-bill THEN
            DO:
                IF h-bill.flag EQ 0 THEN do-it = YES.
                ELSE do-it = NO.
            END.

            do-it = YES.
            IF do-it THEN
            DO:
                FOR EACH h-bill-line WHERE h-bill-line.departement EQ dept AND h-bill-line.rechnr EQ bill-number NO-LOCK:
                    FIND FIRST h-artikel WHERE h-artikel.departement EQ dept AND h-artikel.artnr EQ h-bill-line.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE h-artikel THEN
                    DO:
                        IF h-artikel.artart NE 0 AND h-artikel.artart NE 5 THEN
                        DO:
                            payment-method = CAPS(h-artikel.bezeich).
                            LEAVE.
                        END.
                        ELSE IF h-artikel.artart NE 0 AND h-artikel.artart EQ 5 THEN
                        DO:
                            payment-method = CAPS(h-artikel.bezeich).
                            LEAVE.
                        END.
                    END.
                END.
    
                FOR EACH h-bill-line WHERE h-bill-line.departement EQ dept
                    AND h-bill-line.rechnr EQ bill-number 
                    NO-LOCK BY h-bill-line.bill-datum DESC BY h-bill-line.zeit DESC:
                    
                    FIND FIRST ordered-item WHERE ordered-item.hbline-recid EQ INT(RECID(h-bill-line)) 
                        AND ordered-item.hbline-time EQ h-bill-line.zeit NO-LOCK NO-ERROR.
                    IF AVAILABLE ordered-item THEN .
                    ELSE
                    DO:
                        FIND FIRST h-artikel WHERE h-artikel.departement EQ dept AND h-artikel.artnr EQ h-bill-line.artnr NO-LOCK NO-ERROR.
                        IF AVAILABLE h-artikel THEN
                        DO:
                            IF h-artikel.artart EQ 0 THEN art-type = "SALES".
                            ELSE IF h-artikel.artart EQ 5 THEN art-type = "DEPOSIT". /*FDL Dec 29, 2022*/
                        END.                            
            
                        IF h-bill-line.anzahl LT 0 THEN art-type = "VOID".
                        ELSE
                        DO:
                            IF h-bill-line.artnr EQ art-discfood       THEN art-type = "DISCOUNT FOOD".
                            ELSE IF h-bill-line.artnr EQ art-discbev   THEN art-type = "DISCOUNT BEV".
                            ELSE IF h-bill-line.artnr EQ art-discother THEN art-type = "DISCOUNT OTHER".
                            ELSE IF h-bill-line.artnr EQ art-voucher   THEN art-type = "VOUCHER".
                            ELSE IF h-bill-line.artnr EQ art-paycash   THEN art-type = "PAYMENT CASH".
                            ELSE
                            DO:
                                DO loop-cc = 1 TO NUM-ENTRIES(art-cc,":"):
                                    art-paycc = INT(ENTRY(loop-cc,art-cc,":")).
                                    IF h-bill-line.artnr EQ art-paycc THEN art-type = "PAYMENT CCARD".                                    
                                END.

                                DO loop-cl = 1 TO NUM-ENTRIES(art-cl,";"):
                                    art-paycl = INT(ENTRY(loop-cl,art-cl,";")).
                                    IF h-bill-line.artnr EQ art-paycl THEN art-type = "PAYMENT CLEDGER".                                    
                                END.
                            END.
                        END.
                        CREATE ordered-item.
                        ASSIGN ordered-item.table-nr   = h-bill-line.tischnr   
                               ordered-item.order-nr   = 0
                               ordered-item.bezeich    = h-bill-line.bezeich
                               ordered-item.qty        = h-bill-line.anzahl
                               ordered-item.sp-req     = ""
                               ordered-item.confirm    = YES
                               ordered-item.remarks    = ""
                               ordered-item.order-date = STRING(h-bill-line.bill-datum)
                               ordered-item.nr         = 0
                               ordered-item.price      = h-bill-line.nettobetrag
                               ordered-item.price      = ROUND(ordered-item.price,2)
                               ordered-item.subtotal   = h-bill-line.nettobetrag * h-bill-line.anzahl                               
                               ordered-item.artnr      = h-bill-line.artnr
                               ordered-item.bill-date  = h-bill-line.bill-datum
                               ordered-item.posted     = YES
                               ordered-item.article-type = art-type
                               ordered-item.count-amount = YES.
                               
                        IF ordered-item.qty GT 1 THEN
                        DO:
                            ordered-item.price    = ordered-item.price / ordered-item.qty.
                            ordered-item.subtotal = h-bill-line.nettobetrag.
                        END.
    
                        IF ordered-item.posted EQ NO THEN
                        DO:
                            ASSIGN 
                                ordered-item.order-status = "WAIT FOR WAITER CONFIRM"
                                ordered-item.sp-req       = "WAIT FOR WAITER CONFIRM" + " - " + ordered-item.sp-req
                                ordered-item.count-amount = NO.
                        END.
                        ELSE IF ordered-item.posted EQ YES THEN
                        DO:
                            IF ordered-item.confirm EQ NO THEN 
                            DO:
                                ordered-item.price        = 0.  
                                ordered-item.subtotal     = 0.
                                ordered-item.order-status = "ORDER CANCELED".
                                ordered-item.sp-req       = "ORDER CANCELED" + " - " + ordered-item.sp-req.
                                ordered-item.count-amount = NO.
                            END.
                            ELSE 
                                ASSIGN 
                                    ordered-item.order-status = "ORDER POSTED"
                                    ordered-item.sp-req       = "ORDER POSTED" + " - " + ordered-item.sp-req
                                    ordered-item.count-amount = YES.
                        END.      
                    END.
                END.

                /*Get Grand Total*/
                FIND FIRST h-bill WHERE h-bill.rechnr EQ bill-number
                    AND h-bill.departement EQ dept NO-LOCK NO-ERROR.
                IF AVAILABLE h-bill THEN
                DO:
                    IF h-bill.flag EQ 0 THEN
                    DO:
                        FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ bill-number
                            AND h-bill-line.departement EQ dept NO-LOCK,  
                            FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr  
                            AND h-artikel.departement EQ h-bill-line.departement NO-LOCK:  
        
                            tot-amount = tot-amount + vhp.h-bill-line.betrag.  
                        END.
                    END.
                    ELSE
                    DO:
                        tot-amount = 0.
                    END.                                       
                END.                
            END.
        END.
        mess-result = "0-Order found success!".
    END.
    ELSE
    DO:
        mess-result = "1-No order found!".
        RETURN.
    END.
END.

PROCEDURE cal-servat:  
    DEF INPUT PARAMETER depart          AS INT.  
    DEF INPUT PARAMETER h-artnr         AS INT.  
    DEF INPUT PARAMETER service-code    AS INT.  
    DEF INPUT PARAMETER mwst-code       AS INT.
    DEF INPUT PARAMETER inpDate         AS DATE.
    DEF OUTPUT PARAMETER serv%          AS DECIMAL INITIAL 0.  
    DEF OUTPUT PARAMETER mwst%          AS DECIMAL INITIAL 0.  
    DEF OUTPUT PARAMETER servat         AS DECIMAL INITIAL 0. 
      
    DEF VAR serv-htp AS DECIMAL            NO-UNDO.  
    DEF VAR vat-htp  AS DECIMAL            NO-UNDO.  
    DEF VAR vat2     AS DECIMAL INITIAL 0.  
      
    DEF BUFFER hbuff FOR vhp.h-artikel.  
    DEF BUFFER aBuff FOR vhp.artikel.  
      
    IF servtax-use-foart THEN
    DO:
        FIND FIRST hbuff WHERE hbuff.artnr = h-artnr AND hbuff.departement = depart NO-LOCK.    
        FIND FIRST abuff WHERE abuff.artnr = hbuff.artnrfront AND abuff.departement = depart NO-LOCK.  
    
        /* SY AUG 13 2017 */
        RUN calc-servtaxesbl.p(1, abuff.artnr, abuff.departement, inpDate, OUTPUT serv%, OUTPUT mwst%, OUTPUT vat2, OUTPUT servat).
        ASSIGN mwst% = mwst% + vat2.
    END.
    ELSE /*FD July 14, 2022*/
    DO:
        IF service-code NE 0 THEN   
        DO:   
            FIND FIRST htparam WHERE htparam.paramnr EQ service-code NO-LOCK.   
            serv-htp = htparam.fdecimal / 100.   
        END.   

        IF mwst-code NE 0 THEN   
        DO:   
            FIND FIRST htparam WHERE htparam.paramnr EQ mwst-code NO-LOCK.   
            vat-htp = htparam.fdecimal / 100.  
        END.  

        IF service-taxable THEN
        DO:
            ASSIGN  
                serv%  = serv-htp  
                mwst%  = (1 + serv-htp) * vat-htp  
                servat = 1 + serv% + mwst%  
            . 
        END.          
        ELSE 
        DO:
            ASSIGN  
                serv%  = serv-htp  
                mwst%  = vat-htp  
                servat = 1 + serv% + mwst%  
            . 
        END.        
    END.    
END.
/**/
/*CURRENT-WINDOW:WIDTH = 199.
DEF VAR subtot AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99".
FOR EACH ordered-item BY ordered-item.artnr: 

    subtot = (ordered-item.price * ordered-item.qty) + ordered-item.service + ordered-item.tax.
    DISP ordered-item.order-nr
         ordered-item.nr
         ordered-item.qty
         ordered-item.bezeich
         ordered-item.price  
         ordered-item.article-type
         ordered-item.confirm
         ordered-item.posted
         ordered-item.order-status
         ordered-item.hbline-recid
         ordered-item.hbline-time

         /*ordered-item.service(sum)      
         ordered-item.tax(sum)  
         ordered-item.subtotal(SUM)
         ordered-item.priceTaxServ(SUM)*/
         /*subtot(sum)
         total-price
         total-tax
         total-service 
         grand-total*/
        WITH WIDTH 190.
END.  */


