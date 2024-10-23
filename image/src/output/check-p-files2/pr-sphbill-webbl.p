{tb-printer.i}

DEFINE TEMP-TABLE t-print-head
    FIELD str-date      AS CHARACTER INITIAL ""
    FIELD str-time      AS CHARACTER INITIAL ""
    FIELD bill-no       AS CHARACTER INITIAL ""
    FIELD resto-name    AS CHARACTER INITIAL ""
    FIELD table-usr-id  AS CHARACTER INITIAL ""
    FIELD curr-time     AS CHARACTER INITIAL ""
.

DEFINE TEMP-TABLE t-print-line
    FIELD str-qty       AS CHARACTER INITIAL ""
    FIELD descrip       AS CHARACTER INITIAL ""
    FIELD str-price     AS CHARACTER INITIAL ""
    FIELD foot-note1    AS CHARACTER INITIAL ""
    FIELD foot-note2    AS CHARACTER INITIAL ""
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
DEFINE INPUT PARAMETER bill-nr      AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str     AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER room-no     AS CHARACTER.
DEFINE OUTPUT PARAMETER guest-name  AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-print-head.
DEFINE OUTPUT PARAMETER TABLE FOR t-print-line.

/* For Testing 
DEFINE VARIABLE pvILanguage  AS INTEGER.  
DEFINE VARIABLE user-init    AS CHARACTER.
DEFINE VARIABLE print-all    AS LOGICAL.
DEFINE VARIABLE printnr      AS INTEGER.
DEFINE VARIABLE hbrecid      AS INTEGER.
DEFINE VARIABLE use-h-queasy AS LOGICAL INITIAL YES.
DEFINE VARIABLE msg-str      AS CHARACTER INITIAL "".
DEFINE VARIABLE room-no      AS CHARACTER.
DEFINE VARIABLE guest-name   AS CHARACTER. 
DEFINE VARIABLE bill-nr      AS INTEGER.

ASSIGN
    pvILanguage     = 1
    user-init       = "01"
    print-all       = YES
    printnr         = 99
    hbrecid         = 4710297
    use-h-queasy    = YES
    msg-str         = ""
    bill-nr         = 6
.
*/

{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "print-hbill1".

DEFINE VARIABLE session-parameter   AS CHARACTER.
DEFINE VARIABLE winprinterFLag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE filename            AS CHARACTER. 
DEFINE VARIABLE table-no            AS CHARACTER.
DEFINE VARIABLE usr-id              AS CHARACTER.
DEFINE VARIABLE pax                 AS CHARACTER.
DEFINE VARIABLE counter             AS INTEGER.

DEFINE VARIABLE GS                  AS CHARACTER.
DEFINE VARIABLE pay-str             AS CHARACTER.
DEFINE VARIABLE pay-amount          AS CHARACTER.
DEFINE VARIABLE curr-amount         AS CHARACTER.
DEFINE VARIABLE curr-pay            AS CHARACTER.
DEFINE VARIABLE rechnr-str          AS CHARACTER.
DEFINE VARIABLE flag-change         AS LOGICAL INITIAL NO.
DEFINE VARIABLE flag-pay            AS LOGICAL INITIAL NO.
DEFINE VARIABLE flag-vat            AS LOGICAL INITIAL NO.
DEFINE VARIABLE foot-note           AS CHARACTER INITIAL "".
DEFINE VARIABLE guest-addr          AS CHARACTER.
DEFINE VARIABLE guest-addr1         AS CHARACTER.
DEFINE VARIABLE count-i             AS INTEGER.
DEFINE VARIABLE GS-1                AS CHARACTER.

RUN pr-sphbill1-lnlbl.p (pvILanguage, hbrecid, printnr, use-h-queasy, session-parameter,  
                user-init, bill-nr, INPUT-OUTPUT print-all, OUTPUT winprinterFlag,  
                OUTPUT filename, OUTPUT msg-str, OUTPUT TABLE output-list2,  
                OUTPUT TABLE t-printer).

IF msg-str NE "" THEN RETURN.

DEFINE BUFFER print-list FOR output-list2.
DEFINE BUFFER paylist FOR output-list2.

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
    ASSIGN
        t-print-head.str-date   = TRIM(SUBSTRING(print-list.str,6,8))
        t-print-head.str-time   = TRIM(SUBSTRING(print-list.str,15,5))
        t-print-head.bill-no    = TRIM(SUBSTRING(print-list.str,28,10))
        t-print-head.curr-time  = STRING(TIME, "HH:MM:SS")
        rechnr-str              = t-print-head.bill-no
    .
END.

/*Get Resto Name*/
FIND FIRST print-list WHERE print-list.str-pos EQ 2 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:    
    ASSIGN
        t-print-head.resto-name = TRIM(print-list.str).
END.

/*Get Table No, User ID*/
FIND FIRST print-list WHERE print-list.str-pos EQ 3 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    ASSIGN
        table-no                    = TRIM(SUBSTRING(print-list.str,11,5))
        pax                         = TRIM(SUBSTRING(print-list.str,17,13))
        usr-id                      = TRIM(SUBSTRING(print-list.str,30,32))
        t-print-head.table-usr-id   = translateExtended("Table",lvCAREA,"") + " " + table-no + " / " + pax + " " + CAPS(usr-id)
    .
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
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = TRIM(SUBSTRING(print-list.str,1,20))
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
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
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended(TRIM(SUBSTRING(print-list.str,6,25)),lvCAREA, "")
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
    .
END.

/*Get Goverment Charge*/
FIND FIRST print-list WHERE print-list.str-pos EQ 12 AND print-list.str MATCHES "*gov*" NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:
    flag-vat = YES.
    CREATE t-print-line.
    ASSIGN
        t-print-line.descrip    = translateExtended(TRIM(SUBSTRING(print-list.str,6,25)),lvCAREA, "")
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
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
        t-print-line.str-price  = TRIM(SUBSTRING(print-list.str,31,19))
    .
END.

/*Get Guest*/
FIND FIRST print-list WHERE print-list.str-pos EQ 18 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:    
    ASSIGN
        GS = TRIM(SUBSTRING(print-list.str,2,30))
        GS-1 = SUBSTRING(print-list.str,2,30)
        guest-addr = TRIM(SUBSTRING(print-list.str,33,48))
        guest-addr1 = SUBSTRING(print-list.str,33,48)
        guest-name = GS
    .

    IF guest-name EQ ? THEN guest-name = "".
END.

/*Get Payment*/
FIND FIRST print-list WHERE print-list.str-pos EQ 14 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN
DO:    
    flag-pay = YES.
    FOR EACH paylist WHERE paylist.str-pos EQ 14 NO-LOCK:     
        IF GS NE "" THEN
        DO:       
            IF guest-addr EQ "" THEN
            DO:                
                IF paylist.str MATCHES '*' + GS + '*' THEN 
                DO:
                    pay-str     = TRIM(SUBSTRING(paylist.str,LENGTH(GS) + 3,36)).
                    curr-pay    = pay-str.
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
END.

/*Get change*/
FIND FIRST print-list WHERE print-list.str-pos EQ 16 NO-LOCK NO-ERROR.
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
END.
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
END.

/*Get Room*/
/*IF curr-pay MATCHES("*RmNo*") THEN room-no = TRIM(ENTRY(2,curr-pay," ")).*/
FIND FIRST print-list WHERE print-list.str-pos EQ 17 NO-LOCK NO-ERROR.
IF AVAILABLE print-list THEN 
DO:
    IF NUM-ENTRIES(print-list.str,":") GT 1 THEN room-no = TRIM(ENTRY(2,SUBSTRING(print-list.str,6,25),":")).
    ELSE room-no = "".
END.    


FOR EACH print-list WHERE print-list.str-pos EQ 19 NO-LOCK:
    foot-note = foot-note + TRIM(print-list.str) + ";".
END.

IF foot-note NE "" THEN
DO:
    CREATE t-print-line.
    ASSIGN
        t-print-line.foot-note1 = ENTRY(1,foot-note,";")
        t-print-line.foot-note2 = ENTRY(2,foot-note,";")
    .
END.
