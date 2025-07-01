DEFINE TEMP-TABLE t-printer LIKE printer.

DEFINE TEMP-TABLE output-list  
    FIELD str        AS CHARACTER  
    FIELD pos        AS INT  
    FIELD flag-popup AS LOGICAL INIT NO  
    FIELD npause     AS INT
    FIELD sort-i     AS INT
    .

DEFINE TEMP-TABLE print-list  
    FIELD str        AS CHARACTER  
    FIELD str-pos    AS INTEGER
    FIELD pos        AS INT  
    FIELD flag-popup AS LOGICAL INIT NO  
    FIELD npause     AS INT
    FIELD sort-i     AS INT
    .

DEFINE TEMP-TABLE outlet-split-bill
    FIELD sort-i        AS INTEGER
    FIELD str-date      AS CHARACTER INITIAL ""
    FIELD str-time      AS CHARACTER INITIAL ""
    FIELD bill-no       AS CHARACTER INITIAL ""
    FIELD resto-name    AS CHARACTER INITIAL ""
    FIELD table-usr-id  AS CHARACTER INITIAL ""
    FIELD curr-time     AS CHARACTER INITIAL ""
    FIELD guest-name    AS CHARACTER INITIAL ""
    FIELD guest-member  AS CHARACTER INITIAL "" 
    FIELD od-taker      AS CHARACTER INITIAL ""
    FIELD str-qty       AS CHARACTER INITIAL ""
    FIELD descrip       AS CHARACTER INITIAL ""
    FIELD str-price     AS CHARACTER INITIAL ""
    FIELD foot-note1    AS CHARACTER INITIAL ""
    FIELD foot-note2    AS CHARACTER INITIAL ""
    FIELD foot-note3    AS CHARACTER INITIAL ""
    .

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER print-all    AS LOGICAL.
DEFINE INPUT PARAMETER printnr      AS INTEGER.
DEFINE INPUT PARAMETER hbrecid      AS INTEGER.
DEFINE INPUT PARAMETER use-h-queasy AS LOGICAL INIT YES. /*Always Yes If Check Program e1-main0*/
DEFINE INPUT PARAMETER billnr       AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str     AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER room-no     AS CHARACTER.
DEFINE OUTPUT PARAMETER guest-name  AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR outlet-split-bill.

{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "printsplit-hbill-getsection-web".

DEFINE VARIABLE winprinterFLag      AS LOGICAL NO-UNDO INITIAL NO.
DEFINE VARIABLE session-parameter   AS CHAR NO-UNDO.
DEFINE VARIABLE filename            AS CHAR.
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
DEFINE VARIABLE split-no            AS CHARACTER NO-UNDO.

FIND FIRST printer WHERE printer.nr EQ printnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE printer THEN
DO:
    msg-str = "1-Printer Not Found.".
    RETURN.
END.

RUN pr-sphbill1-cldbl.p  
    (pvILanguage, hbrecid, printnr, use-h-queasy, session:parameter,  
    user-init, billnr, INPUT-OUTPUT print-all, OUTPUT winprinterFlag,  
    OUTPUT filename, OUTPUT msg-str, OUTPUT TABLE print-list,  
    OUTPUT TABLE t-printer). 

IF msg-str NE "" THEN RETURN.

DEFINE BUFFER paylist FOR print-list.
/*
FOR EACH print-list BY print-list.sort-i:
    CREATE output-list.
    BUFFER-COPY print-list TO output-list.
END.
*/
/*
FIND FIRST print-list WHERE print-list.str-pos EQ 1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE print-list THEN
DO:
    msg-str = translateExtended("No Data Available.",lvCAREA,"").
    RETURN.
END.
*/
FOR EACH print-list BY print-list.str-pos:
    CREATE outlet-split-bill.
    outlet-split-bill.sort-i = print-list.sort-i.

    IF print-list.str-pos EQ 1 THEN /*Get Bill Date, Time, BillNo*/
    DO:
        ASSIGN
            outlet-split-bill.str-date   = TRIM(ENTRY(1,print-list.str,"|"))
            outlet-split-bill.str-time   = TRIM(ENTRY(2,print-list.str,"|"))
            outlet-split-bill.bill-no    = TRIM(ENTRY(4,print-list.str,"|"))
            outlet-split-bill.curr-time  = STRING(TIME, "HH:MM:SS")        
            .
    END.
    ELSE IF print-list.str-pos EQ 2 THEN /*Get Resto Name*/
    DO:
        ASSIGN
            outlet-split-bill.resto-name = TRIM(print-list.str).
    END.
    ELSE IF print-list.str-pos EQ 3 THEN /*Get Table No, User ID*/
    DO:
        ASSIGN
            table-no    = TRIM(ENTRY(2,print-list.str,"|"))
            usr-id      = TRIM(ENTRY(3,print-list.str,"|")) + " " + TRIM(ENTRY(5,print-list.str,"|")) 
            split-no    = TRIM(ENTRY(4,print-list.str,"|"))
            .        
            
        outlet-split-bill.table-usr-id = translateExtended("Table",lvCAREA,"") + " " 
            + table-no + "/" + CAPS(usr-id) + split-no.    
    END.
    ELSE IF print-list.str-pos EQ 5 THEN /*Get Guest Name*/
    DO:
        ASSIGN
            outlet-split-bill.guest-name = TRIM(ENTRY(2,print-list.str,"|"))
            GS = outlet-split-bill.guest-name
            guest-name = outlet-split-bill.guest-name
            .
        IF NUM-ENTRIES(print-list.str, "|") GT 2 AND guest-name NE "" THEN
        DO:
            outlet-split-bill.guest-name = outlet-split-bill.guest-name + " | " + TRIM(ENTRY(3,print-list.str,"|")).
        END.

        /* FDL Comment
        FIND FIRST h-bill WHERE RECID(h-bill) EQ hbrecid NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill THEN
        DO:
            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
            DO:
                FIND FIRST res-line WHERE res-line.resnr EQ h-bill.resnr
                    AND res-line.reslinnr EQ h-bill.reslinnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    ASSIGN
                        GS = res-line.NAME
                        guest-name = res-line.NAME
                        outlet-split-bill.guest-name = res-line.NAME
                        .
                END.
            END.
            ELSE IF h-bill.resnr GT 0 THEN
            DO:
                FIND FIRST guest WHERE guest.gastnr EQ h-bill.resnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                DO:
                    ASSIGN
                        GS = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
                        guest-name = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
                        outlet-split-bill.guest-name = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
                        .
                END.
            END.
            ELSE
            DO:
                ASSIGN
                    GS = h-bill.bilname
                    guest-name = h-bill.bilname
                    outlet-split-bill.guest-name = h-bill.bilname
                    .
            END.
        END.
        */
    END.    
    ELSE IF print-list.str-pos EQ 8 THEN /*Get Guest Member*/
    DO:
        ASSIGN
            outlet-split-bill.guest-member = TRIM(print-list.str).
    END.
    ELSE IF print-list.str-pos EQ 10 THEN /*Get QTY, DESC, PRICE*/
    DO:
        ASSIGN
            outlet-split-bill.str-qty    = TRIM(ENTRY(1,print-list.str,"|"))
            outlet-split-bill.descrip    = TRIM(ENTRY(2,print-list.str,"|"))
            outlet-split-bill.str-price  = TRIM(ENTRY(3,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 11 THEN /*Get Subtotal*/
    DO:
        ASSIGN
            outlet-split-bill.descrip    = TRIM(ENTRY(1,print-list.str,"|"))
            outlet-split-bill.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .

        CREATE outlet-split-bill.
        outlet-split-bill.sort-i = -1.
        outlet-split-bill.descrip = FILL("-", 42).
        outlet-split-bill.str-price = FILL("-", 19).
    END.
    ELSE IF print-list.str-pos EQ 12 AND print-list.str MATCHES "*Service*" THEN /*Get Service Charge*/
    DO:
        ASSIGN
            outlet-split-bill.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
            outlet-split-bill.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 12 AND print-list.str MATCHES "*gov*" THEN /*Get Goverment Charge*/
    DO:
        ASSIGN
            outlet-split-bill.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
            outlet-split-bill.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 13 THEN /*Get Total*/
    DO:        
        outlet-split-bill.sort-i = -1.
        outlet-split-bill.descrip = FILL("-", 42).
        outlet-split-bill.str-price = FILL("-", 19).

        CREATE outlet-split-bill.
        ASSIGN
            outlet-split-bill.sort-i     = print-list.sort-i
            outlet-split-bill.descrip    = translateExtended("TOTAL",lvCAREA,"")
            outlet-split-bill.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    /*ELSE IF print-list.str-pos EQ 18 THEN /*Get Guest*/
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
    END.*/
    ELSE IF print-list.str-pos EQ 14 THEN /*Get Payment*/
    DO:
        IF GS NE "" THEN
        DO:
            IF print-list.str MATCHES '*' + GS + '*' THEN
            DO:
                ASSIGN 
                    outlet-split-bill.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
                    outlet-split-bill.descrip    = TRIM(SUBSTR(outlet-split-bill.descrip,LENGTH(GS) + 1))
                .
            END.
            ELSE
            DO:
                 outlet-split-bill.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "").
            END.
        END.
        ELSE
        DO:
             outlet-split-bill.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "").
        END.
        outlet-split-bill.str-price  = TRIM(ENTRY(2,print-list.str,"|")).
    END.
    ELSE IF print-list.str-pos EQ 16 THEN /*Get change*/
    DO:
        ASSIGN        
            outlet-split-bill.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")  
            outlet-split-bill.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 15 THEN /*Get Balance*/
    DO:
        outlet-split-bill.sort-i = -1.
        outlet-split-bill.descrip = FILL("-", 42).
        outlet-split-bill.str-price = FILL("-", 19).

        CREATE outlet-split-bill.
        ASSIGN
            outlet-split-bill.sort-i     = print-list.sort-i
            outlet-split-bill.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
            outlet-split-bill.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 17 THEN /*Get Room*/
    DO:        
        IF NUM-ENTRIES(print-list.str,":") GT 1 THEN room-no = TRIM(ENTRY(2,print-list.str,":")).
        ELSE room-no = "".
    END.
    ELSE IF print-list.str-pos EQ 19 THEN /*Get FootNote 1*/
    DO:
        IF print-list.str EQ ? THEN print-list.str = "".
        outlet-split-bill.foot-note1 = TRIM(print-list.str).
    END.
    ELSE IF print-list.str-pos EQ 20 THEN /*Get FootNote 2*/
    DO:
        IF print-list.str EQ ? THEN print-list.str = "".
        outlet-split-bill.foot-note2 = TRIM(print-list.str).
    END.
    ELSE IF print-list.str-pos EQ 21 THEN /*Get FootNote 3*/
    DO:
        IF print-list.str EQ ? THEN print-list.str = "".
        outlet-split-bill.foot-note3 = TRIM(print-list.str).
    END.
END.

/*Updated Printed*/
FIND FIRST h-bill WHERE RECID(h-bill) = hbrecid.
FIND CURRENT h-bill EXCLUSIVE-LOCK. 
h-bill.rgdruck = 1. 
FIND CURRENT h-bill NO-LOCK.

msg-str = "0-Success".
