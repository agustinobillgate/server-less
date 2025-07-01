DEFINE TEMP-TABLE menu-list   
  FIELD nr              AS INTEGER  
  FIELD rec-id          AS INTEGER  
  FIELD art-number      AS INTEGER 
  FIELD art-description AS CHARACTER    
  FIELD art-qty         AS INT   
  FIELD art-price       AS DECIMAL   
  FIELD special-request AS CHARACTER.  

DEFINE TEMP-TABLE post-menu-list  
  FIELD rec-id          AS INTEGER
  FIELD DESCRIPTION     AS CHARACTER
  FIELD qty             AS INTEGER
  FIELD price           AS DECIMAL
  FIELD special-request AS CHARACTER.

/**/
DEFINE INPUT PARAMETER outlet-number     AS INTEGER.
DEFINE INPUT PARAMETER table-nr          AS INTEGER.
DEFINE INPUT PARAMETER room-number       AS CHARACTER.
DEFINE INPUT PARAMETER guest-name        AS CHARACTER.
DEFINE INPUT PARAMETER pax               AS INTEGER.
DEFINE INPUT PARAMETER guest-number      AS INTEGER.
DEFINE INPUT PARAMETER res-number        AS INTEGER.     
DEFINE INPUT PARAMETER resline-number    AS INTEGER.     
DEFINE INPUT PARAMETER order-datetime    AS DATETIME.
DEFINE INPUT PARAMETER active-order      AS LOGICAL.
DEFINE INPUT PARAMETER session-parameter AS CHARACTER.

DEFINE INPUT PARAMETER TABLE FOR menu-list.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.

/*
DEFINE VARIABLE outlet-number  AS INTEGER   INIT 1.
DEFINE VARIABLE table-nr       AS INTEGER   INIT 16.
DEFINE VARIABLE room-number    AS CHARACTER INIT "".
DEFINE VARIABLE guest-name     AS CHARACTER INIT "arys".
DEFINE VARIABLE order-datetime AS DATETIME  INIT NOW.
DEFINE VARIABLE active-order   AS LOGICAL INIT YES. 
DEFINE VARIABLE mess-result    AS CHAR.
DEFINE VARIABLE session-parameter AS CHARACTER INIT "vhptest12".
DEFINE VARIABLE pax            AS INTEGER INIT 1.
DEFINE VARIABLE guest-number      AS INTEGER.
DEFINE VARIABLE res-number        AS INTEGER.     
DEFINE VARIABLE resline-number    AS INTEGER.  
*/

DEFINE VARIABLE orderbill-number AS INT.
DEFINE VARIABLE orderbill-line-number AS INT.
DEFINE VARIABLE direct-post AS LOGICAL.
DEFINE VARIABLE count-i     AS INT.
DEFINE VARIABLE alpha-flag  AS LOGICAL.
DEFINE VARIABLE room-no     AS CHARACTER.
DEFINE VARIABLE rm-no       AS CHARACTER.
DEFINE VARIABLE str1        AS CHARACTER.
DEFINE VARIABLE dynamic-qr  AS LOGICAL.
DEFINE VARIABLE room-serviceflag  AS LOGICAL.
DEFINE VARIABLE pay-flag    AS LOGICAL.
DEFINE VARIABLE found-menu  AS LOGICAL INITIAL NO.

DEFINE VARIABLE sclose-time AS INTEGER.
DEFINE VARIABLE eclose-time AS INTEGER.
DEFINE VARIABLE scurr-time  AS INTEGER.
DEFINE VARIABLE ecurr-time  AS INTEGER.
DEFINE VARIABLE curr-time   AS INTEGER.
DEFINE VARIABLE time-str    AS CHAR.
DEFINE VARIABLE shour       AS INTEGER.
DEFINE VARIABLE sminute     AS INTEGER.
DEFINE VARIABLE ehour       AS INTEGER.
DEFINE VARIABLE eminute     AS INTEGER.

DEFINE BUFFER new-order FOR queasy.

DEFINE VARIABLE recid-hbill AS INTEGER.
DEFINE BUFFER buff-hbill FOR h-bill.
DEFINE BUFFER q-orderbill FOR queasy.
DEFINE BUFFER q-takentable FOR queasy.
DEFINE BUFFER sosqsy FOR queasy.
DEFINE BUFFER h-order FOR queasy.

/* RUN create-bill. */

/*search for order number*/

IF outlet-number EQ ? OR outlet-number EQ 0 THEN
DO:
    mess-result = "1-Outlet number can't be null!".
    RETURN.
END.
IF table-nr EQ ? OR table-nr EQ 0 THEN
DO:
    mess-result = "2-Table number can't be null!".
    RETURN.
END.
IF guest-name EQ ? OR guest-name EQ "" THEN
DO:
    mess-result = "3-Guest Name can't be null!".
    RETURN.
END.
IF pax EQ ? OR pax EQ 0 THEN
DO:
    mess-result = "4-Number of Pax can't be null!".
    RETURN.
END.
IF order-datetime EQ ? THEN
DO:
    mess-result = "5-Order Date and Time can't be null!".
    RETURN.
END.

/*FDL July 17, 2024 - Check Menu List Exist or Not*/
FIND FIRST menu-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE menu-list THEN
DO:
    mess-result = "7-Request is not complete. Menu List not available.".
    RETURN.
END.

/*FDL Nov 11, 2023 => Ticket FEF6F0*/
FIND FIRST queasy WHERE queasy.KEY EQ 222 AND queasy.number1 EQ 1
    AND queasy.number2 EQ 25 AND queasy.number3 EQ 5
    AND queasy.betriebsnr EQ outlet-number
    AND queasy.char2 NE "" NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    shour = INT(SUBSTR(TRIM(ENTRY(1,queasy.char2,"|")),1,2)).
    sminute = INT(SUBSTR(TRIM(ENTRY(1,queasy.char2,"|")),4,2)).
    ehour = INT(SUBSTR(TRIM(ENTRY(2,queasy.char2,"|")),1,2)).
    eminute = INT(SUBSTR(TRIM(ENTRY(2,queasy.char2,"|")),4,2)).

    sclose-time = shour * 3600 + sminute * 60.
    eclose-time = ehour * 3600 + eminute * 60.

    curr-time = TIME.
    time-str = STRING(TIME, "HH:MM").
    scurr-time = INT(ENTRY(1,time-str,":")).
    ecurr-time = INT(ENTRY(2,time-str,":")).                      

    IF ehour - shour < 0 THEN /*Start Time before 00.00 and Closed Time Passed 00.00*/
    DO:
        IF scurr-time GE shour THEN
        DO:
            IF curr-time GE sclose-time AND eclose-time LE curr-time THEN
            DO:
                mess-result = "4-Closing Time periode! Order not possible.".
                RETURN.
            END.
        END.
        ELSE IF scurr-time LE ehour THEN
        DO:
            IF curr-time LE eclose-time THEN
            DO:
                mess-result = "4-Closing Time periode! Order not possible.".
                RETURN.
            END.
        END. 
    END.
    ELSE /*Start Time before 00.00 and Closed Time before 00.00*/
    DO:
        IF curr-time GE sclose-time AND curr-time LE eclose-time THEN
        DO:
            mess-result = "4-Closing Time periode! Order not possible.".
            RETURN.
        END.
    END.
END.

active-order = YES.
direct-post = NO.
FIND FIRST queasy WHERE queasy.KEY EQ 222 AND queasy.number1 = 1 
    AND queasy.number2 = 15 AND queasy.betriebsnr EQ outlet-number NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN direct-post = queasy.logi1.

IF direct-post THEN
DO:
    /*FDL Oct 26, 2023 => Ticket 3BCBFA*/
    FIND FIRST h-bill WHERE h-bill.tischnr EQ table-nr
        AND h-bill.departement EQ outlet-number
        AND h-bill.flag EQ 0 
        AND h-bill.saldo EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr
            AND h-bill-line.departement EQ h-bill.departement NO-LOCK,
            FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr
            AND h-artikel.departement EQ h-bill-line.departement
            AND h-artikel.artart NE 0 NO-LOCK:
            
            pay-flag = YES.
            LEAVE.
        END.
        IF pay-flag THEN
        DO:
            mess-result = "91-Bill on this table has been paid and balance is zero. Please come back at the moment or contact the cashier.".
            RETURN.
        END.
    END.
END.

IF room-number EQ ? THEN room-number = "".
IF guest-number EQ ? THEN guest-number = 0.
IF res-number EQ ? THEN res-number = 0.
IF resline-number EQ ? THEN resline-number = 0.

/*Check Sold Out Item*/
DEF VAR found-soldout AS LOGICAL.
FOR EACH menu-list:
    FIND FIRST queasy WHERE queasy.key EQ 222 AND queasy.number1 EQ 2
    AND queasy.number2 EQ menu-list.art-number
    AND queasy.number3 EQ outlet-number NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        IF queasy.logi2 EQ YES THEN 
        DO:
            found-soldout = YES.
            LEAVE.
        END.
    END.
END.
IF found-soldout THEN
DO:
    mess-result = "6-One of Item Has SoldOut!".
    RETURN.
END.

FOR EACH sosqsy WHERE sosqsy.KEY EQ 222 AND sosqsy.number1 EQ 1 
    AND sosqsy.betriebsnr EQ outlet-number NO-LOCK:
    IF sosqsy.number2 EQ 14 THEN dynamic-qr = sosqsy.logi1.
    IF sosqsy.number2 EQ 21 THEN room-serviceflag = sosqsy.logi1.
END.

/*FD Sept 29, 2022 => Validation for posting from SelfOrder get in to the Close Bill*/
recid-hbill = 0.
FOR EACH buff-hbill WHERE buff-hbill.tischnr EQ table-nr
    AND buff-hbill.departement EQ outlet-number
    AND buff-hbill.flag EQ 1 NO-LOCK BY buff-hbill.rechnr DESC:

    recid-hbill = RECID(buff-hbill).
    IF recid-hbill NE 0 THEN
    DO:
        LEAVE.
    END.    
END.

FIND FIRST q-orderbill WHERE q-orderbill.KEY EQ 225
    AND q-orderbill.char1 EQ "orderbill"
    AND q-orderbill.number1 EQ outlet-number
    AND q-orderbill.number2 EQ table-nr     
    AND q-orderbill.number3 EQ 0
    AND q-orderbill.char3 EQ session-parameter
    AND q-orderbill.betriebsnr EQ recid-hbill NO-LOCK NO-ERROR.
IF AVAILABLE q-orderbill THEN
DO:
    FIND CURRENT q-orderbill EXCLUSIVE-LOCK.
    DELETE q-orderbill.
    RELEASE q-orderbill.
END.
/*End FD*/

/*FDL March 16, 2023 => Ticket 490301 - validate for room no numeric + alphabet*/
IF room-serviceflag THEN
DO:
    FIND FIRST q-takentable WHERE q-takentable.KEY EQ 225
        AND q-takentable.char1 EQ "taken-table"
        AND q-takentable.number2 EQ table-nr
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
END.

IF alpha-flag THEN
DO:
    FIND FIRST tisch WHERE tisch.departement EQ outlet-number
        AND tisch.tischnr EQ table-nr NO-LOCK NO-ERROR.
    IF AVAILABLE tisch THEN 
    DO:        
        room-no = SUBSTRING(tisch.bezeich,6).
    END.
    
    FIND FIRST res-line WHERE res-line.resstatus EQ 6 AND res-line.zinr EQ room-no NO-LOCK NO-ERROR.
END.
ELSE
DO:
    FIND FIRST res-line WHERE res-line.resstatus EQ 6 AND res-line.zinr EQ STRING(table-nr) NO-LOCK NO-ERROR.
END.
/*End FDL*/
/*search for reservation*/
/*FIND FIRST res-line WHERE res-line.resstatus EQ 6 AND res-line.zinr EQ STRING(table-nr) NO-LOCK NO-ERROR.*/
IF AVAILABLE res-line THEN
DO:
    res-number     = res-line.resnr.
    resline-number = res-line.reslinnr.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 225 
        AND queasy.number1 EQ outlet-number 
        AND queasy.char1 EQ "orderbill" 
        AND queasy.number2 EQ table-nr
        AND queasy.logi1 EQ active-order NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 225 
        AND queasy.number1 EQ outlet-number 
        AND queasy.char1 EQ "orderbill" 
        AND queasy.number2 EQ table-nr
        AND queasy.logi1 EQ active-order NO-LOCK BY queasy.number3 DESC.
        orderbill-number = queasy.number3 + 1.
        LEAVE.
    END.
END.
ELSE orderbill-number = 1.

/*create new queasy as new record or add line in each record*/
FIND FIRST queasy WHERE queasy.KEY EQ 225 
        AND queasy.number1 EQ outlet-number 
        AND queasy.char1 EQ "orderbill" 
        AND queasy.number2 EQ table-nr
        AND queasy.number3 EQ orderbill-number 
        AND queasy.date1 EQ DATE(order-datetime) 
        AND queasy.logi1 EQ active-order NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:    
    CREATE queasy.
    ASSIGN 
        queasy.KEY     = 225
        queasy.number1 = outlet-number
        queasy.number2 = table-nr
        queasy.number3 = orderbill-number
        queasy.char1   = "orderbill"
        queasy.char2   = "RN=" + room-number +
                        "|NM=" + guest-name + 
                        "|DT=" + STRING(order-datetime) + 
                        "|PX=" + STRING(pax) + 
                        "|GN=" + STRING(guest-number) + 
                        "|RS=" + STRING(res-number) + 
                        "|RL=" + STRING(resline-number)         
        queasy.date1   = DATE(order-datetime)                                              
        queasy.logi1   = active-order    
        queasy.logi3   = NO 
        queasy.char3   = session-parameter
        /*queasy.betriebsnr = 0*/
        .              

    /*MESSAGE "Header SelfOrder => " queasy.date1 "|" queasy.number1 "|" queasy.number2 "|"  
        queasy.number3 "|" queasy.char3        
        VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    /*
    /*FD April 21, 2022*/
    FIND FIRST h-bill WHERE h-bill.flag EQ 0
        AND h-bill.tischnr EQ table-nr 
        AND h-bill.departement EQ outlet-number NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN /*If have a bill from POS dekstop, get the recid h-bill*/
    DO:        
        queasy.betriebsnr = RECID(h-bill).
    END.
    ELSE*/
    DO: 
        queasy.betriebsnr = 0.
    END.    

    FOR EACH menu-list:
        CREATE queasy.
        ASSIGN 
        queasy.KEY     = 225
        queasy.number1 = orderbill-number
        queasy.number2 = table-nr
        queasy.number3 = menu-list.nr
        queasy.char1   = "orderbill-line"
        queasy.char2   = STRING(outlet-number) + "|" + STRING(table-nr) + "|" + STRING(order-datetime) + "|" + session-parameter
        queasy.char3   = STRING(menu-list.nr             ) + "|" + 
                         STRING(menu-list.art-number     ) + "|" + 
                         STRING(menu-list.art-description) + "|" + 
                         STRING(menu-list.art-qty        ) + "|" + 
                         STRING(menu-list.art-price      ) + "|" + 
                         STRING(menu-list.special-request) 
        queasy.date1   = DATE(order-datetime)
        queasy.logi2   = NO
        queasy.logi3   = NO
        .       

        /*MESSAGE "Body SelfOrder => " queasy.date1 "|" queasy.number1 "|" queasy.number2 "|"  
            queasy.number3 "|" queasy.char3 "|" queasy.char2    
            VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    END.
    /*
    IF  THEN
    DO:
        FIND FIRST h-order WHERE h-order.KEY EQ 225
            AND h-order.char1 EQ "orderbill"
            AND h-order.char3 EQ session-parameter
            AND h-order.number1 EQ outlet-number
            AND h-order.number2 EQ table-nr
            AND h-order.number3 EQ orderbill-number
            AND h-order.date1 EQ DATE(order-datetime)
            AND h-order.logi1 EQ active-order 
            AND h-order.logi3 EQ NO
            AND queasy.betriebsnr EQ 0 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE h-order THEN
        DO:
            DELETE h-order.
            RELEASE h-order.
        END.
        RETURN.
    END.
    */
    IF direct-post THEN RUN post-to-outlet.
    ELSE mess-result = "0-Posting Item Success".
END.
ELSE
DO:
    FOR EACH menu-list:
        CREATE queasy.
        ASSIGN 
        queasy.KEY     = 225
        queasy.number1 = orderbill-number
        queasy.number2 = table-nr
        queasy.number3 = menu-list.nr
        queasy.char1   = "orderbill-line"
        queasy.char2   = STRING(outlet-number) + "|" + STRING(table-nr) + "|" + STRING(order-datetime) + "|" + session-parameter
        queasy.char3   = STRING(menu-list.nr             ) + "|" + 
                         STRING(menu-list.art-number     ) + "|" + 
                         STRING(menu-list.art-description) + "|" + 
                         STRING(menu-list.art-qty        ) + "|" + 
                         STRING(menu-list.art-price      ) + "|" + 
                         STRING(menu-list.special-request)
        queasy.date1   = DATE(order-datetime)
        queasy.logi2   = NO
        queasy.logi3   = NO
        .
    END.

    IF direct-post THEN RUN post-to-outlet.
    ELSE mess-result = "0-RePosting Item Success".
END.

PROCEDURE post-to-outlet:
    DEFINE VARIABLE post-language-code AS INTEGER INIT 0.
    DEFINE VARIABLE post-rec-id        AS INTEGER INIT 0.   
    DEFINE VARIABLE post-tischnr       AS INTEGER.   
    DEFINE VARIABLE post-curr-dept     AS INTEGER.   
    DEFINE VARIABLE post-gname         AS CHARACTER. 
    DEFINE VARIABLE post-pax           AS INTEGER.   
    DEFINE VARIABLE post-guestnr       AS INTEGER.   
    DEFINE VARIABLE post-curr-room     AS CHARACTER. 
    DEFINE VARIABLE post-resnr         AS INTEGER.   
    DEFINE VARIABLE post-reslinnr      AS INTEGER. 
    DEFINE VARIABLE post-table-no      AS INTEGER.   
    DEFINE VARIABLE post-order-no      AS INTEGER. 
    DEFINE VARIABLE post-bill-number   AS INTEGER. 
    DEFINE VARIABLE post-session-param AS CHARACTER. 
    DEFINE VARIABLE post-bill-recid    AS INTEGER.
    DEFINE VARIABLE post-mess-str      AS CHARACTER.
    DEFINE VARIABLE user-init          AS CHARACTER.       

    FIND FIRST queasy WHERE queasy.KEY EQ 222
        AND queasy.number1 EQ 1
        AND queasy.number2 EQ 9 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN user-init = queasy.char2.

    DEFINE BUFFER mergequeasy FOR queasy.
    FIND FIRST mergequeasy WHERE mergequeasy.KEY EQ 225 
        AND mergequeasy.char1 EQ "orderbill"
        AND mergequeasy.char3 EQ session-parameter 
        AND mergequeasy.betriebsnr NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE mergequeasy THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY EQ 225 
            AND queasy.char1 EQ "orderbill" 
            AND queasy.char3 EQ mergequeasy.char3 EXCLUSIVE-LOCK:
            queasy.betriebsnr = mergequeasy.betriebsnr.
        END.
        RELEASE queasy. /*FDL Stack Trace Yello Manggarai*/
    END.

    DEFINE BUFFER getrec-id FOR queasy.
    FIND FIRST getrec-id WHERE getrec-id.KEY EQ 225 
        AND getrec-id.char1 EQ "orderbill"
        AND getrec-id.char3 EQ session-parameter NO-LOCK NO-ERROR.
    IF AVAILABLE getrec-id THEN post-bill-recid = getrec-id.betriebsnr.
    ELSE post-bill-recid = 0.

    EMPTY TEMP-TABLE post-menu-list.
    FOR EACH menu-list:
        CREATE post-menu-list.
        ASSIGN 
            post-menu-list.rec-id          = menu-list.art-number          
            post-menu-list.DESCRIPTION     = menu-list.art-description        
            post-menu-list.qty             = menu-list.art-qty           
            post-menu-list.price           = menu-list.art-price         
            post-menu-list.special-request = menu-list.special-request                  
            .
    END.

    ASSIGN 
        post-table-no      = table-nr
        post-order-no      = orderbill-number
        post-tischnr       = table-nr 
        post-curr-dept     = outlet-number       
        post-gname         = guest-name  
        post-pax           = pax
        post-guestnr       = guest-number  
        post-curr-room     = room-number
        post-resnr         = res-number    
        post-reslinnr      = resline-number
        post-session-param = session-parameter
        
        .


    RUN pos-dashboard-post-menubl.p (1, post-bill-recid, post-tischnr,      
            post-curr-dept, user-init, post-gname,        
            post-pax,post-guestnr,post-curr-room,post-resnr,        
            post-reslinnr, post-session-param, post-order-no, INPUT TABLE post-menu-list,
            OUTPUT post-bill-number, OUTPUT post-mess-str).

    IF post-mess-str EQ "Order Posted Success" THEN mess-result = "0-Posting Item Success".
    ELSE mess-result = "9-" + post-mess-str.
END.
