
DEFINE INPUT PARAMETER curr-dept    AS INTEGER.
DEFINE INPUT PARAMETER s-recid      AS INTEGER.
DEFINE OUTPUT PARAMETER pax         AS INTEGER.
DEFINE OUTPUT PARAMETER guest-name  AS CHARACTER.
DEFINE OUTPUT PARAMETER telefon     AS CHARACTER.
DEFINE OUTPUT PARAMETER voucher-str AS CHARACTER.
DEFINE OUTPUT PARAMETER str-line    AS CHARACTER.
DEFINE OUTPUT PARAMETER str-line2   AS CHARACTER.
DEFINE OUTPUT PARAMETER str-line3   AS CHARACTER.
DEFINE OUTPUT PARAMETER dept-name   AS CHARACTER.
DEFINE OUTPUT PARAMETER time-rsv    AS CHARACTER.
DEFINE OUTPUT PARAMETER depo-flag   AS LOGICAL INITIAL NO.

DEFINE VARIABLE art-name        AS CHARACTER.
DEFINE VARIABLE depopay-art     AS CHARACTER.
DEFINE VARIABLE str-saldo       AS CHARACTER.
DEFINE VARIABLE str1            AS CHARACTER.
DEFINE VARIABLE depoart         AS INTEGER.
DEFINE VARIABLE ns-billno       AS INTEGER.
DEFINE VARIABLE guest-no        AS INTEGER.
DEFINE VARIABLE depo-amount     AS DECIMAL.
DEFINE VARIABLE depo-payment    AS DECIMAL.
DEFINE VARIABLE date-depopay    AS DATE.

DEFINE BUFFER buf-bline FOR bill-line.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN dept-name = hoteldpt.depart.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart = htparam.finteger.

FIND FIRST queasy WHERE RECID(queasy) EQ s-recid NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    ASSIGN
        pax         = queasy.number3
        guest-name  = ENTRY(1, queasy.char2, "&&")
        telefon     = TRIM(SUBSTR(queasy.char1,10))
        time-rsv    = SUBSTR(queasy.char1,1,2) + ":" + SUBSTR(queasy.char1,3,2) + " - " + SUBSTR(queasy.char1,5,2) + ":" + SUBSTR(queasy.char1,7,2)
        guest-no    = INTEGER(ENTRY(3, queasy.char2, "&&"))
        depo-amount = queasy.deci1
        ns-billno   = INTEGER(queasy.deci2)
        .   

    FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ guest-no 
        AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
        AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
        FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
            AND bill-line.artnr NE depoart NO-LOCK NO-ERROR.
        IF AVAILABLE bill-line THEN
        DO:
            ASSIGN
                depo-payment = bill-line.betrag
                date-depopay = bill-line.bill-datum
                depopay-art  = bill-line.bezeich
                .
            depo-flag = YES.
        END.

        FIND FIRST buf-bline WHERE buf-bline.rechnr EQ bill.rechnr
            AND buf-bline.artnr EQ depoart NO-LOCK NO-ERROR.
        IF AVAILABLE buf-bline THEN
        DO:
            str1 = ENTRY(1, bill-line.bezeich, "[").
            voucher-str = TRIM(ENTRY(2, str1, "/")).
        END.
    END.    

    /*Get Artikel Deposit Resto*/
    FIND FIRST wgrpgen WHERE wgrpgen.bezeich MATCHES "*deposit*" NO-LOCK NO-ERROR.
    IF AVAILABLE wgrpgen THEN
    DO:
        FIND FIRST h-artikel WHERE h-artikel.endkum EQ wgrpgen.eknr
            AND h-artikel.activeflag NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN
        DO:
            art-name = h-artikel.bezeich.
        END.        
    END.

    str-line = STRING(art-name, "x(15)") + " " + STRING(depo-amount, "->>,>>>,>>9.99").
    str-line2 = STRING(depopay-art, "x(15)") + " " + STRING(depo-payment, "->>,>>>,>>9.99").
    str-saldo = "Balance".
    str-line3 = STRING(str-saldo, "x(15)") + " " + STRING(0, "->>,>>>,>>9.99").
END.
