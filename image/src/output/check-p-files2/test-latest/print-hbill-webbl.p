{tb-printer.i}

DEFINE TEMP-TABLE t-print-head
    FIELD str-date      AS CHARACTER INITIAL ""
    FIELD str-time      AS CHARACTER INITIAL ""
    FIELD bill-no       AS CHARACTER INITIAL ""
    FIELD resto-name    AS CHARACTER INITIAL ""
    FIELD table-usr-id  AS CHARACTER INITIAL ""
    FIELD curr-time     AS CHARACTER INITIAL ""
    FIELD guest-member  AS CHARACTER INITIAL "" 
    FIELD od-taker      AS CHARACTER INITIAL ""
    FIELD table-desc    AS CHARACTER INITIAL ""
.

DEFINE TEMP-TABLE t-print-line
    FIELD str-qty       AS CHARACTER INITIAL ""
    FIELD descrip       AS CHARACTER INITIAL ""
    FIELD str-price     AS CHARACTER INITIAL ""
    FIELD foot-note1    AS CHARACTER INITIAL ""
    FIELD foot-note2    AS CHARACTER INITIAL ""
    FIELD foot-note3    AS CHARACTER INITIAL ""
.

DEFINE TEMP-TABLE output-list2  
    FIELD str        AS CHARACTER
    FIELD str-pos    AS INTEGER
    FIELD pos        AS INTEGER
    FIELD flag-popup AS LOGICAL INITIAL NO  
    FIELD npause     AS INTEGER
    FIELD sort-i     AS INTEGER
.

DEFINE TEMP-TABLE t-printer LIKE printer.
/**/
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER.  
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER print-all    AS LOGICAL.
DEFINE INPUT PARAMETER printnr      AS INTEGER.
DEFINE INPUT PARAMETER hbrecid      AS INTEGER.
DEFINE INPUT PARAMETER use-h-queasy AS LOGICAL INITIAL YES.
DEFINE OUTPUT PARAMETER msg-str     AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER room-no     AS CHARACTER.
DEFINE OUTPUT PARAMETER guest-name  AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-print-head.
DEFINE OUTPUT PARAMETER TABLE FOR t-print-line.

/* For Testing Local
DEFINE VARIABLE pvILanguage  AS INTEGER.  
DEFINE VARIABLE user-init    AS CHARACTER.
DEFINE VARIABLE print-all    AS LOGICAL.
DEFINE VARIABLE printnr      AS INTEGER.
DEFINE VARIABLE hbrecid      AS INTEGER.
DEFINE VARIABLE use-h-queasy AS LOGICAL INITIAL YES.
DEFINE VARIABLE msg-str      AS CHARACTER INITIAL "".
DEFINE VARIABLE room-no      AS CHARACTER.
DEFINE VARIABLE guest-name   AS CHARACTER. 

ASSIGN
    pvILanguage     = 1
    user-init       = "01"
    print-all       = YES
    printnr         = 99
    hbrecid         = 4737964
    use-h-queasy    = YES
    msg-str         = ""
.
*/

{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "print-hbill1".

DEFINE VARIABLE session-parameter   AS CHARACTER.
DEFINE VARIABLE winprinterFLag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE filename            AS CHARACTER. 
DEFINE VARIABLE table-no            AS CHARACTER.
DEFINE VARIABLE usr-id              AS CHARACTER.
DEFINE VARIABLE counter             AS INTEGER.

DEFINE VARIABLE GS                  AS CHARACTER.
DEFINE VARIABLE pay-str             AS CHARACTER.
DEFINE VARIABLE depopay-str         AS CHARACTER.
DEFINE VARIABLE pay-amount          AS CHARACTER.
DEFINE VARIABLE curr-amount         AS CHARACTER.
DEFINE VARIABLE curr-pay            AS CHARACTER.
DEFINE VARIABLE rechnr-str          AS CHARACTER.
DEFINE VARIABLE flag-change         AS LOGICAL INITIAL NO.
DEFINE VARIABLE flag-pay            AS LOGICAL INITIAL NO.
DEFINE VARIABLE flag-vat            AS LOGICAL INITIAL NO.
DEFINE VARIABLE foot-note           AS CHARACTER INITIAL "".
DEFINE VARIABLE curr-footnote       AS CHARACTER INITIAL "".
DEFINE VARIABLE guest-addr          AS CHARACTER.
DEFINE VARIABLE guest-addr1         AS CHARACTER.
DEFINE VARIABLE count-i             AS INTEGER.
DEFINE VARIABLE GS-1                AS CHARACTER.
DEFINE VARIABLE fo-depoart          AS INTEGER NO-UNDO.
DEFINE VARIABLE fo-depobez          AS CHARACTER NO-UNDO.
DEFINE VARIABLE fb-depoart          AS INTEGER NO-UNDO.
DEFINE VARIABLE fb-depobez          AS CHARACTER NO-UNDO.
DEFINE VARIABLE voucher-depo        AS CHARACTER.
DEFINE VARIABLE gastno              AS INTEGER NO-UNDO.
DEFINE VARIABLE ns-billno           AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-dept           AS INTEGER NO-UNDO.
DEFINE VARIABLE str1                AS CHARACTER NO-UNDO.


RUN print-hbilllnl-cldbl.p (pvILanguage, session-parameter, user-init, hbrecid, printnr,
               use-h-queasy, INPUT-OUTPUT print-all, OUTPUT filename,
               OUTPUT msg-str, OUTPUT winprinterFLag,
               OUTPUT TABLE output-list2, OUTPUT TABLE t-printer).

IF msg-str NE "" THEN RETURN.

DEFINE BUFFER print-list FOR output-list2.
DEFINE BUFFER paylist FOR output-list2.
DEFINE BUFFER q-33 FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN
    DO:
        ASSIGN 
            fo-depoart = artikel.artnr
            fo-depobez = artikel.bezeich
            .
    END.    
END.

FIND FIRST wgrpgen WHERE wgrpgen.bezeich MATCHES "*deposit*" NO-LOCK NO-ERROR.
IF AVAILABLE wgrpgen THEN
DO:
    FIND FIRST h-artikel WHERE h-artikel.endkum EQ wgrpgen.eknr
        AND h-artikel.activeflag NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
        ASSIGN
            fb-depoart  = h-artikel.artnr
            fb-depobez  = h-artikel.bezeich
        .
    END.        
END.

FIND FIRST queasy WHERE queasy.KEY EQ 251 AND queasy.number1 EQ hbrecid NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND FIRST q-33 WHERE RECID(q-33) EQ queasy.number2 NO-LOCK NO-ERROR.
    IF AVAILABLE q-33 THEN
    DO:
        ASSIGN
            ns-billno   = INTEGER(q-33.deci2)
            gastno      = INTEGER(ENTRY(3, q-33.char2, "&&"))
            curr-dept   = q-33.number1
            .

        /*Get Voucher Deposit*/
        FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ gastno 
            AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
            AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
        IF AVAILABLE bill THEN
        DO:
            FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
                AND bill-line.artnr EQ fo-depoart NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
                str1 = ENTRY(1, bill-line.bezeich, "[").
                voucher-depo = TRIM(ENTRY(2, str1, "/")).
            END.
        END.
    END.
END.

CREATE t-print-head.

FIND FIRST print-list WHERE print-list.str-pos EQ 1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE print-list THEN
DO:
    msg-str = translateExtended("No Data Available.",lvCAREA,"").
    RETURN.
END.
ELSE
DO:
    /*Get Bill Date, Time, BillNo*/
    /*ASSIGN
        t-print-head.str-date   = TRIM(SUBSTRING(print-list.str,6,8))
        t-print-head.str-time   = TRIM(SUBSTRING(print-list.str,15,5))
        t-print-head.bill-no    = TRIM(SUBSTRING(print-list.str,28,10))
        t-print-head.curr-time  = STRING(TIME, "HH:MM:SS")
        rechnr-str              = t-print-head.bill-no
    .
    */
    ASSIGN
        t-print-head.str-date   = TRIM(ENTRY(1,print-list.str,"|"))
        t-print-head.str-time   = TRIM(ENTRY(2,print-list.str,"|"))
        t-print-head.bill-no    = TRIM(ENTRY(4,print-list.str,"|"))
        t-print-head.curr-time  = STRING(TIME, "HH:MM:SS")
        rechnr-str              = t-print-head.bill-no
        .
END.

/*Get Resto Name*/
FIND FIRST print-list WHERE print-list.str-pos EQ 2 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:    
    ASSIGN
        t-print-head.resto-name = print-list.str.
END.

/*Get Table No, User ID*/
FIND FIRST print-list WHERE print-list.str-pos EQ 3 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    /*ASSIGN
        table-no                    = TRIM(SUBSTRING(print-list.str,11,5))
        usr-id                      = TRIM(SUBSTRING(print-list.str,17,56))
        t-print-head.table-usr-id   = translateExtended("Table",lvCAREA,"") + " " + table-no + " / " + CAPS(usr-id)
    .
    */
    ASSIGN
        table-no    = TRIM(ENTRY(2,print-list.str,"|"))
        usr-id      = TRIM(ENTRY(3,print-list.str,"|")) + " " + TRIM(ENTRY(4,print-list.str,"|")) 
    .
    IF TRIM(ENTRY(5,print-list.str,"|")) NE "" THEN
    DO:
        t-print-head.od-taker = TRIM(ENTRY(5,print-list.str,"|")).
    END.
    IF TRIM(ENTRY(6,print-list.str,"|")) NE "" THEN
    DO:
        t-print-head.table-desc = TRIM(ENTRY(6,print-list.str,"|")).
    END.
        
    /*t-print-head.table-usr-id   = translateExtended("Table",lvCAREA,"") + " " + table-no + " / " + CAPS(usr-id).*/
    t-print-head.table-usr-id   = translateExtended(t-print-head.table-desc,lvCAREA,"") + " / " + CAPS(usr-id).
END.

/*Get Guest Member*/
FIND FIRST print-list WHERE print-list.str-pos EQ 8 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:    
    ASSIGN
        t-print-head.guest-member = TRIM(print-list.str).
END.

/*Get QTY, DESC, PRICE*/
FOR EACH print-list WHERE print-list.str-pos EQ 10 NO-LOCK:     
    CREATE t-print-line.
    ASSIGN
        t-print-line.str-qty    = TRIM(ENTRY(1,print-list.str,"|"))
        t-print-line.descrip    = TRIM(ENTRY(2,print-list.str,"|"))
        t-print-line.str-price  = TRIM(ENTRY(3,print-list.str,"|"))
    .
END.

/*Get Subtotal*/
FIND FIRST print-list WHERE print-list.str-pos EQ 11 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    /*
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = TRIM(SUBSTRING(print-list.str,1,20))
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
    .   
    */   
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = TRIM(ENTRY(1,print-list.str,"|"))
        t-print-line.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
    .   
END.

CREATE t-print-line.
t-print-line.descrip    = FILL("-",42).
t-print-line.str-price  = FILL("-",19).

/*Get Service Charge*/
FIND FIRST print-list WHERE print-list.str-pos EQ 12 AND print-list.str MATCHES "*Service*" NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    flag-vat = YES.
    /*
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended(TRIM(SUBSTRING(print-list.str,6,25)),lvCAREA, "")
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
    .
    */
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
        t-print-line.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
    .
END.

/*Get Goverment Charge*/
FIND FIRST print-list WHERE print-list.str-pos EQ 12 AND print-list.str MATCHES "*gov*" NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    flag-vat = YES.
    /*
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended(TRIM(SUBSTRING(print-list.str,6,25)),lvCAREA, "")
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
    .
    */
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
        t-print-line.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
    .
END.

IF flag-vat THEN
DO:
    CREATE t-print-line.
    t-print-line.descrip    = FILL("-",42).
    t-print-line.str-price  = FILL("-",19).
END.


/*Get Total*/
FIND FIRST print-list WHERE print-list.str-pos EQ 13 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended("TOTAL",lvCAREA,"").
        /*t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))*/
        t-print-line.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
    .
END.

/*Get Guest*/
FIND FIRST print-list WHERE print-list.str-pos EQ 18 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:    
    ASSIGN
        GS = TRIM(SUBSTRING(print-list.str,2,64))
        GS-1 = SUBSTRING(print-list.str,2,64)
        guest-addr = TRIM(SUBSTRING(print-list.str,67,48))
        guest-addr1 = SUBSTRING(print-list.str,67,48)
        guest-name = GS
    .

    IF GS EQ ? THEN GS = "".
    IF guest-name EQ ? THEN guest-name = "".
END.

/*Get Payment*/
FIND FIRST print-list WHERE print-list.str-pos EQ 14 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:    
    flag-pay = YES.
    FOR EACH paylist WHERE paylist.str-pos EQ 14 NO-LOCK:
        CREATE t-print-line.        

        IF GS NE "" THEN
        DO:
            IF paylist.str MATCHES '*' + GS + '*' THEN
            DO:
                IF (GS EQ "Compl" OR GS EQ "Compliment" OR GS EQ "A&G" 
                    OR GS EQ "Eng" OR GS EQ "FB" OR GS EQ "FO" OR GS EQ "HK" 
                    OR GS EQ "HRD" OR GS EQ "Owner" OR GS EQ "Sales")
                    AND (paylist.str MATCHES("*Compliment*") OR paylist.str MATCHES("*Compl*")
                    OR paylist.str MATCHES("*Entertaint*") OR paylist.str MATCHES("*Officer Check*")) THEN /*FDL May 30, 2025: F0C3BE*/
                DO:
                    t-print-line.descrip    = TRIM(SUBSTR(translateExtended(ENTRY(1,paylist.str,"|"),lvCAREA, ""),LENGTH(GS))).
                END.
                ELSE
                DO:
                    ASSIGN                     
                        t-print-line.descrip    = translateExtended(TRIM(ENTRY(1,paylist.str,"|")),lvCAREA, "")
                        t-print-line.descrip    = TRIM(SUBSTR(t-print-line.descrip,LENGTH(GS) + 1)).
                END.
            END.
            ELSE
            DO:
                 t-print-line.descrip    = translateExtended(TRIM(ENTRY(1,paylist.str,"|")),lvCAREA, "").
            END.
        END.
        ELSE
        DO:
             t-print-line.descrip    = translateExtended(TRIM(ENTRY(1,paylist.str,"|")),lvCAREA, "").
        END.
        t-print-line.str-price  = TRIM(ENTRY(2,paylist.str,"|")).
    END.
    /*
    FOR EACH paylist WHERE paylist.str-pos EQ 14 NO-LOCK:     
        IF GS NE "" THEN
        DO:       
            IF guest-addr EQ "" THEN
            DO:                
                IF paylist.str MATCHES '*' + GS + '*' THEN 
                DO:
                    IF paylist.str MATCHES "*deposit*" THEN
                    DO:
                        depopay-str = TRIM(SUBSTRING(paylist.str,LENGTH(GS) + 3)).
                        depopay-str = TRIM(SUBSTRING(depopay-str,1,LENGTH(fb-depobez))) + voucher-depo.

                        curr-pay    = pay-str.
                        curr-amount = TRIM(SUBSTRING(paylist.str,LENGTH(GS) + 2,LENGTH(paylist.str))).
                        count-i     = NUM-ENTRIES(curr-amount, "-").  
                        pay-amount  = "-" + TRIM(ENTRY(count-i,curr-amount,"-")).
                        pay-str     = REPLACE(depopay-str,"-","").
                    END.
                    ELSE
                    DO:
                        pay-str = TRIM(SUBSTRING(paylist.str,LENGTH(GS) + 3,36)).
                        curr-pay    = pay-str.
                        curr-amount = TRIM(SUBSTRING(paylist.str,LENGTH(GS) + 2,LENGTH(paylist.str))).
                        count-i     = NUM-ENTRIES(curr-amount, "-").  
                        pay-amount  = "-" + TRIM(ENTRY(count-i,curr-amount,"-")).
                        pay-str     = REPLACE(pay-str,"-","").
                    END.                                       
    
                    CREATE t-print-line.
                    ASSIGN 
                        t-print-line.descrip    = translateExtended(TRIM(pay-str),lvCAREA, "")
                        t-print-line.str-price  = TRIM(pay-amount)
                    .                    
                END.
                ELSE
                DO:
                    pay-str    = TRIM(SUBSTRING(paylist.str,6,24)).
                    curr-pay   = pay-str.
                    pay-amount = TRIM(SUBSTRING(paylist.str,31,19)).
                    pay-str    = REPLACE(pay-str,"-","").
    
                    CREATE t-print-line.
                    ASSIGN 
                        t-print-line.descrip    = translateExtended(TRIM(pay-str),lvCAREA, "")
                        t-print-line.str-price  = TRIM(pay-amount)
                    .
                END.
            END.
            ELSE
            DO:                      
                IF paylist.str MATCHES '*' + GS + '*' THEN 
                DO:      
                    /*paylist.str = REPLACE(paylist.str,guest-addr,";").*/
                    pay-str     = TRIM(SUBSTRING(paylist.str,LENGTH(GS-1) + LENGTH(guest-addr1) + 3,30)).
                    curr-amount = TRIM(SUBSTRING(paylist.str,LENGTH(GS) + 2,LENGTH(paylist.str))).
                    count-i     = NUM-ENTRIES(curr-amount, "-").  
                    pay-amount  = "-" + TRIM(ENTRY(count-i,curr-amount,"-")).
                    pay-str     = REPLACE(pay-str,"-","").
    
                    CREATE t-print-line.
                    ASSIGN 
                        t-print-line.descrip    = translateExtended(TRIM(pay-str),lvCAREA, "")
                        t-print-line.str-price  = TRIM(pay-amount)
                    .
                END.
                ELSE
                DO:
                    pay-str    = TRIM(SUBSTRING(paylist.str,6,24)).
                    curr-pay   = pay-str.
                    pay-amount = TRIM(SUBSTRING(paylist.str,31,19)).
                    pay-str    = REPLACE(pay-str,"-","").
    
                    CREATE t-print-line.
                    ASSIGN 
                        t-print-line.descrip    = translateExtended(TRIM(pay-str),lvCAREA, "")
                        t-print-line.str-price  = TRIM(pay-amount)
                    .
                END.            
            END.
            
            /*ELSE
            DO:
                pay-str    = pay-str + TRIM(SUBSTRING(paylist.str,6,24)).
                pay-amount = pay-amount + TRIM(SUBSTRING(paylist.str,31,12)).
            END.*/
        END.
        ELSE
        DO:                        
            IF NOT paylist.str MATCHES "*Cash Rp(Change)*" THEN
            DO:
                pay-str    = TRIM(SUBSTRING(paylist.str,6,24)).
                curr-pay   = pay-str.
                pay-amount = TRIM(SUBSTRING(paylist.str,31,19)).
                pay-str    = REPLACE(pay-str,"-","").

                CREATE t-print-line.
                ASSIGN 
                    t-print-line.descrip    = translateExtended(TRIM(pay-str),lvCAREA, "")
                    t-print-line.str-price  = TRIM(pay-amount)
                .
            END.         
        END.                           
    END.   
    */        
END.

/*Get change*/
FIND FIRST print-list WHERE print-list.str-pos EQ 16 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    CREATE t-print-line.
    ASSIGN        
        t-print-line.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")  
        t-print-line.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
    .  
END.
/*FIND FIRST print-list WHERE print-list.str-pos EQ 16 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    flag-change = YES.

    CREATE t-print-line.
    t-print-line.descrip    = FILL("-",42).
    t-print-line.str-price  = FILL("-",19).

    CREATE t-print-line.
    ASSIGN        
        t-print-line.descrip    = translateExtended(TRIM(SUBSTRING(print-list.str,6,25)),lvCAREA, "")  
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
    .               
END.
ELSE
DO:
    FOR EACH paylist WHERE paylist.str-pos EQ 14 NO-LOCK:
        IF GS NE "" THEN
        DO:                   
            IF NOT paylist.str MATCHES '*' + GS + '*' THEN 
            DO:
                pay-str    = TRIM(SUBSTRING(paylist.str,6,24)).
                pay-amount = TRIM(SUBSTRING(paylist.str,31,19)).
            END.
        END.
        ELSE
        DO:
            IF paylist.str MATCHES "*Cash Rp(Change)*" THEN
            DO:
                pay-str    = TRIM(SUBSTRING(paylist.str,6,24)).
                pay-amount = TRIM(SUBSTRING(paylist.str,31,19)).
            END.             
        END.
        pay-str    = REPLACE(pay-str,"-","").        
    END.

    IF pay-str MATCHES "*Cash Rp(Change)*" THEN
    DO:
        CREATE t-print-line.
        ASSIGN 
            t-print-line.descrip    = translateExtended(TRIM(pay-str),lvCAREA, "")
            t-print-line.str-price  = TRIM(pay-amount)
        .
    END.    
END.*/
GS         = "".
pay-str    = "".
pay-amount = "".

IF NOT flag-change AND flag-pay THEN
DO:
    CREATE t-print-line.
    t-print-line.descrip    = FILL("-",42).
    t-print-line.str-price  = FILL("-",19).
END.

/*Get Balance*/
FIND FIRST print-list WHERE print-list.str-pos EQ 15 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
        t-print-line.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
    .
END.
/*FIND FIRST print-list WHERE print-list.str-pos EQ 15 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    CREATE t-print-line.

    IF flag-change OR NOT flag-pay THEN
    DO:
        ASSIGN
            t-print-line.descrip    = ""
            t-print-line.str-price  = ""
        .
    END.
    ELSE
    DO:
        ASSIGN
            t-print-line.descrip    = translateExtended(TRIM(SUBSTRING(print-list.str,6,25)),lvCAREA, "")
            t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
        .
    END.        
END.
ELSE
DO:
    CREATE t-print-line.

    IF flag-change OR NOT flag-pay THEN
    DO:
        ASSIGN
            t-print-line.descrip    = ""
            t-print-line.str-price  = ""
        .
    END.
    ELSE
    DO:
        ASSIGN
        t-print-line.descrip    = translateExtended("BALANCE",lvCAREA, "").

        FIND FIRST print-list WHERE print-list.str-pos EQ 13 NO-LOCK NO-ERROR.
        IF AVAILABLE print-list THEN t-print-line.str-price = TRIM(SUBSTRING(print-list.str,31,19)).
    END.    
END.*/

/*Get Room*/
/*IF curr-pay MATCHES("*RmNo*") THEN room-no = TRIM(ENTRY(2,curr-pay," ")).*/
FIND FIRST print-list WHERE print-list.str-pos EQ 17 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN 
DO:
    IF NUM-ENTRIES(print-list.str,":") GT 1 THEN room-no = TRIM(ENTRY(2,SUBSTRING(print-list.str,6,25),":")).
    ELSE room-no = "".
END.    


FOR EACH print-list WHERE print-list.str-pos EQ 19 NO-LOCK:
    IF print-list.str EQ ? THEN print-list.str = "".
    print-list.str = REPLACE(print-list.str,";"," ").    
    foot-note = foot-note + TRIM(print-list.str) + ";".
END.
foot-note = SUBSTR(foot-note, 1, LENGTH(foot-note) - 1).

IF foot-note NE "" THEN
DO:
    CREATE t-print-line.
    IF NUM-ENTRIES(foot-note,";") LE 1 THEN
    DO:
        t-print-line.foot-note1 = ENTRY(1,foot-note,";").
    END.
    ELSE IF NUM-ENTRIES(foot-note,";") LE 2 THEN
    DO:
        ASSIGN
            t-print-line.foot-note1 = ENTRY(1,foot-note,";")
            t-print-line.foot-note2 = ENTRY(2,foot-note,";").
    END.
    ELSE IF NUM-ENTRIES(foot-note,";") LE 3 THEN
    DO:
        ASSIGN
            t-print-line.foot-note1 = ENTRY(1,foot-note,";")
            t-print-line.foot-note2 = ENTRY(2,foot-note,";")
            t-print-line.foot-note3 = ENTRY(3,foot-note,";")
            .
    END.
END.

/*Updated Printed*/
FIND FIRST h-bill WHERE RECID(h-bill) = hbrecid.
FIND CURRENT h-bill EXCLUSIVE-LOCK. 
h-bill.rgdruck = 1. 
FIND CURRENT h-bill NO-LOCK.
RELEASE h-bill.
