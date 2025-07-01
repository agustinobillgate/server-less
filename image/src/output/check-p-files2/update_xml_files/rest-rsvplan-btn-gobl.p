DEFINE TEMP-TABLE rsv-table-list
    FIELD rec-id        AS INTEGER
    FIELD dept-no       AS INTEGER
    FIELD dept-name     AS CHARACTER
    FIELD table-no      AS INTEGER
    FIELD guest-name    AS CHARACTER
    FIELD telepon       AS CHARACTER
    FIELD pax           AS INTEGER
    FIELD rsv-date      AS DATE
    FIELD f-time        AS CHARACTER
    FIELD t-time        AS CHARACTER
    FIELD deposit-amt   AS DECIMAL
    FIELD deposit-pay   AS DECIMAL
    FIELD depopay-date  AS DATE
    FIELD depopay-art   AS CHARACTER
    FIELD remark        AS CHARACTER
    FIELD usr-id        AS CHARACTER
    FIELD ns-billno     AS CHARACTER
    FIELD is-refund     AS CHARACTER
    FIELD bill-no       AS CHARACTER
    FIELD rsv-stat      AS CHARACTER
. 

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-time    AS CHARACTER.
DEFINE INPUT PARAMETER to-time      AS CHARACTER.
DEFINE INPUT PARAMETER curr-dept    AS INTEGER.
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR rsv-table-list.

DEFINE VARIABLE tot-pax     AS INTEGER.
DEFINE VARIABLE tot-table   AS INTEGER.
DEFINE VARIABLE ns-billno   AS INTEGER.
DEFINE VARIABLE gastno      AS INTEGER.
DEFINE VARIABLE tot-depoamt AS DECIMAL.
DEFINE VARIABLE tot-depopay AS DECIMAL.
DEFINE VARIABLE depname     AS CHARACTER.
DEFINE VARIABLE depoart     AS INTEGER.

DEFINE BUFFER q251 FOR queasy.

FOR EACH rsv-table-list:
    DELETE rsv-table-list.
END.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart = htparam.finteger.

IF sorttype EQ 0 THEN /*Open*/
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 33 AND queasy.number1 EQ curr-dept
        AND queasy.date1 GE from-date AND queasy.date1 LE to-date 
        AND INTEGER(SUBSTR(queasy.char1,1,4)) LT INTEGER(to-time)
        AND INTEGER(SUBSTR(queasy.char1,5,4)) GT INTEGER(from-time)
        AND queasy.logi3 AND queasy.betriebsnr EQ 0
        NO-LOCK BY queasy.date1 BY queasy.number1: 

        RUN create-rsv-table.
    END.
END.
ELSE IF sorttype EQ 1 THEN /*Close*/
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 33 AND queasy.number1 EQ curr-dept
        AND queasy.date1 GE from-date AND queasy.date1 LE to-date 
        AND INTEGER(SUBSTR(queasy.char1,1,4)) LT INTEGER(to-time)
        AND INTEGER(SUBSTR(queasy.char1,5,4)) GT INTEGER(from-time)
        AND queasy.logi3 AND queasy.betriebsnr EQ 1
        NO-LOCK BY queasy.date1 BY queasy.number1: 

        RUN create-rsv-table.
    END.
END.
ELSE IF sorttype EQ 2 THEN /*Cancel*/
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 33 AND queasy.number1 EQ curr-dept
        AND queasy.date1 GE from-date AND queasy.date1 LE to-date 
        AND INTEGER(SUBSTR(queasy.char1,1,4)) LT INTEGER(to-time)
        AND INTEGER(SUBSTR(queasy.char1,5,4)) GT INTEGER(from-time)
        AND NOT queasy.logi3 AND queasy.betriebsnr EQ 2
        NO-LOCK BY queasy.date1 BY queasy.number1: 

        RUN create-rsv-table.
    END.
END.
ELSE IF sorttype EQ 3 THEN /*Expired*/
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 33 AND queasy.number1 EQ curr-dept
        AND queasy.date1 GE from-date AND queasy.date1 LE to-date 
        AND INTEGER(SUBSTR(queasy.char1,1,4)) LT INTEGER(to-time)
        AND INTEGER(SUBSTR(queasy.char1,5,4)) GT INTEGER(from-time)
        AND NOT queasy.logi3 AND queasy.betriebsnr EQ 3
        NO-LOCK BY queasy.date1 BY queasy.number1: 

        RUN create-rsv-table.
    END.
END.
ELSE IF sorttype EQ 4 THEN /*ALL*/
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 33 AND queasy.number1 EQ curr-dept
        AND queasy.date1 GE from-date AND queasy.date1 LE to-date 
        AND INTEGER(SUBSTR(queasy.char1,1,4)) LT INTEGER(to-time)
        AND INTEGER(SUBSTR(queasy.char1,5,4)) GT INTEGER(from-time)
        NO-LOCK BY queasy.date1 BY queasy.number1: 

        RUN create-rsv-table.
    END.
END.
FIND FIRST rsv-table-list NO-LOCK NO-ERROR.
IF AVAILABLE rsv-table-list THEN
DO:
    CREATE rsv-table-list.
    ASSIGN
        rsv-table-list.dept-name    = "T O T A L"
        rsv-table-list.table-no     = tot-table
        rsv-table-list.pax          = tot-pax
        rsv-table-list.deposit-amt  = tot-depoamt
        rsv-table-list.deposit-pay  = tot-depopay
    .   
END.

PROCEDURE create-rsv-table:
    FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN depname = hoteldpt.depart.

    CREATE rsv-table-list.
    ASSIGN
        rsv-table-list.rec-id       = RECID(queasy)
        rsv-table-list.dept-no      = queasy.number1
        rsv-table-list.dept-name    = depname
        rsv-table-list.table-no     = queasy.number2
        rsv-table-list.guest-name   = ENTRY(1, queasy.char2, "&&")
        rsv-table-list.telepon      = ENTRY(2, queasy.char1, ";")
        rsv-table-list.pax          = queasy.number3
        rsv-table-list.rsv-date     = queasy.date1
        rsv-table-list.f-time       = SUBSTR(queasy.char1,1,4)
        rsv-table-list.t-time       = SUBSTR(queasy.char1,5,4)
        rsv-table-list.deposit-amt  = queasy.deci1
        rsv-table-list.remark       = ENTRY(2, queasy.char3, ";")
        rsv-table-list.usr-id       = ENTRY(1, queasy.char3, ";")
        rsv-table-list.ns-billno    = STRING(queasy.deci2, ">>>>>>>")        
    .

    ns-billno   = INTEGER(queasy.deci2).
    gastno      = INTEGER(ENTRY(3, queasy.char2, "&&")).

    FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ gastno 
        AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
        AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
        FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
            AND bill-line.artnr NE depoart NO-LOCK NO-ERROR.
        IF AVAILABLE bill-line THEN
        DO:
            ASSIGN
                rsv-table-list.deposit-pay = bill-line.betrag
                rsv-table-list.depopay-date = bill-line.bill-datum
                rsv-table-list.depopay-art = bill-line.bezeich
            .
            tot-depopay = tot-depopay + rsv-table-list.deposit-pay.
        END.
    END.

    FIND FIRST q251 WHERE q251.KEY EQ 251 AND q251.number2 EQ INT(RECID(queasy)) NO-LOCK NO-ERROR.
    IF AVAILABLE q251 THEN
    DO:       
        FIND FIRST h-bill WHERE RECID(h-bill) EQ q251.number1 NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill THEN
        DO:
            rsv-table-list.bill-no = STRING(h-bill.rechnr, ">>>>>>>").
        END.        
    END.    

    IF sorttype EQ 0 THEN rsv-table-list.rsv-stat = "Open".
    ELSE IF sorttype EQ 1 THEN rsv-table-list.rsv-stat = "Close".
    ELSE IF sorttype EQ 2 THEN rsv-table-list.rsv-stat = "Cancel".
    ELSE IF sorttype EQ 3 THEN rsv-table-list.rsv-stat = "Expired".
    ELSE IF sorttype EQ 4 THEN
    DO:
        IF queasy.logi3 AND queasy.betriebsnr EQ 0 THEN rsv-table-list.rsv-stat = "Open".
        ELSE IF queasy.logi3 AND queasy.betriebsnr EQ 1 THEN rsv-table-list.rsv-stat = "Close".
        ELSE IF NOT queasy.logi3 AND queasy.betriebsnr EQ 2 THEN rsv-table-list.rsv-stat = "Cancel". 
        ELSE IF NOT queasy.logi3 AND queasy.betriebsnr EQ 3 THEN rsv-table-list.rsv-stat = "Expired".
    END.

    tot-pax     = tot-pax + queasy.number3.
    tot-table   = tot-table + 1.
    tot-depoamt = tot-depoamt + queasy.deci1.
END.
