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

DEFINE TEMP-TABLE outlet-print-list
    FIELD sort-i        AS INTEGER
    FIELD flag-popup    AS LOGICAL INIT NO
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
    .

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER print-all    AS LOGICAL.
DEFINE INPUT PARAMETER printnr      AS INTEGER.
DEFINE INPUT PARAMETER hbrecid      AS INTEGER.
DEFINE INPUT PARAMETER use-h-queasy AS LOGICAL INIT YES. /*Always Yes If Check Program e1-main0*/
DEFINE OUTPUT PARAMETER msg-str     AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER room-no     AS CHARACTER.
DEFINE OUTPUT PARAMETER guest-name  AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR outlet-print-list.

{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "print-hbill-getsection-web".

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

FIND FIRST printer WHERE printer.nr EQ printnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE printer THEN
DO:
    msg-str = "1-Printer Not Found.".
    RETURN.
END.

RUN print-hbill1-cldbl.p
    (pvILanguage, session-parameter, user-init, hbrecid, printnr,
    use-h-queasy, INPUT-OUTPUT print-all, OUTPUT filename,
    OUTPUT msg-str, OUTPUT winprinterFLag,
    OUTPUT TABLE print-list, OUTPUT TABLE t-printer).

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
FOR EACH print-list BY print-list.sort-i:
    CREATE outlet-print-list.
    outlet-print-list.sort-i = print-list.sort-i.
    outlet-print-list.flag-popup = print-list.flag-popup.

    IF print-list.str-pos EQ 1 THEN /*Get Bill Date, Time, BillNo*/
    DO:
        ASSIGN
            outlet-print-list.str-date   = TRIM(ENTRY(1,print-list.str,"|"))
            outlet-print-list.str-time   = TRIM(ENTRY(2,print-list.str,"|"))
            outlet-print-list.bill-no    = TRIM(ENTRY(4,print-list.str,"|"))
            outlet-print-list.curr-time  = STRING(TIME, "HH:MM:SS")        
            .
    END.
    ELSE IF print-list.str-pos EQ 2 THEN /*Get Resto Name*/
    DO:
        ASSIGN
            outlet-print-list.resto-name = TRIM(print-list.str).
    END.
    ELSE IF print-list.str-pos EQ 3 THEN /*Get Table No, User ID*/
    DO:
        ASSIGN
        table-no    = TRIM(ENTRY(2,print-list.str,"|"))
        usr-id      = TRIM(ENTRY(3,print-list.str,"|")) + " " + TRIM(ENTRY(4,print-list.str,"|")) 
        .
        IF TRIM(ENTRY(5,print-list.str,"|")) NE "" THEN
        DO:
            outlet-print-list.od-taker = TRIM(ENTRY(5,print-list.str,"|")).
        END.
            
        outlet-print-list.table-usr-id   = translateExtended("Table",lvCAREA,"") + " " + table-no + " / " + CAPS(usr-id).    
    END.
    ELSE IF print-list.str-pos EQ 5 THEN /*Get Guest Name*/
    DO:
        ASSIGN
            outlet-print-list.guest-name = TRIM(ENTRY(2,print-list.str,"|"))
            GS = outlet-print-list.guest-name
            guest-name = outlet-print-list.guest-name
            .

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
                        outlet-print-list.guest-name = res-line.NAME
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
                        outlet-print-list.guest-name = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
                        .
                END.
            END.
        END.
    END.
    ELSE IF print-list.str-pos EQ 8 THEN /*Get Guest Member*/
    DO:
        ASSIGN
            outlet-print-list.guest-member = TRIM(print-list.str).
    END.
    ELSE IF print-list.str-pos EQ 10 THEN /*Get QTY, DESC, PRICE*/
    DO:
        ASSIGN
            outlet-print-list.str-qty    = TRIM(ENTRY(1,print-list.str,"|"))
            outlet-print-list.descrip    = TRIM(ENTRY(2,print-list.str,"|"))
            outlet-print-list.str-price  = TRIM(ENTRY(3,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 11 THEN /*Get Subtotal*/
    DO:
        ASSIGN
            outlet-print-list.descrip    = TRIM(ENTRY(1,print-list.str,"|"))
            outlet-print-list.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 12 AND print-list.str MATCHES "*Service*" THEN /*Get Service Charge*/
    DO:
        ASSIGN
            outlet-print-list.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
            outlet-print-list.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 12 AND print-list.str MATCHES "*gov*" THEN /*Get Goverment Charge*/
    DO:
        ASSIGN
            outlet-print-list.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
            outlet-print-list.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 13 THEN /*Get Total*/
    DO:
        ASSIGN
            outlet-print-list.descrip    = translateExtended("TOTAL",lvCAREA,"")
            outlet-print-list.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
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
                    outlet-print-list.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
                    outlet-print-list.descrip    = TRIM(SUBSTR(outlet-print-list.descrip,LENGTH(GS) + 1))
                .
            END.
            ELSE
            DO:
                 outlet-print-list.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "").
            END.
        END.
        ELSE
        DO:
             outlet-print-list.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "").
        END.
        outlet-print-list.str-price  = TRIM(ENTRY(2,print-list.str,"|")).
    END.
    ELSE IF print-list.str-pos EQ 16 THEN /*Get change*/
    DO:
        ASSIGN        
            outlet-print-list.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")  
            outlet-print-list.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 15 THEN /*Get Balance*/
    DO:
        ASSIGN
            outlet-print-list.descrip    = translateExtended(TRIM(ENTRY(1,print-list.str,"|")),lvCAREA, "")
            outlet-print-list.str-price  = TRIM(ENTRY(2,print-list.str,"|"))
            .
    END.
    ELSE IF print-list.str-pos EQ 17 THEN /*Get Room*/
    DO:        
        IF NUM-ENTRIES(print-list.str,":") GT 1 THEN room-no = TRIM(ENTRY(2,print-list.str,":")).
        ELSE room-no = "".
    END.
    ELSE IF print-list.str-pos EQ 19 THEN /*Get FootNote 1*/
    DO:
        outlet-print-list.foot-note1 = TRIM(print-list.str).
    END.
    ELSE IF print-list.str-pos EQ 20 THEN /*Get FootNote 1*/
    DO:
        outlet-print-list.foot-note1 = TRIM(print-list.str).
    END.
END.

/*Updated Printed*/
FIND FIRST h-bill WHERE RECID(h-bill) = hbrecid.
FIND CURRENT h-bill EXCLUSIVE-LOCK. 
h-bill.rgdruck = 1. 
FIND CURRENT h-bill NO-LOCK.

msg-str = "0-Success".
