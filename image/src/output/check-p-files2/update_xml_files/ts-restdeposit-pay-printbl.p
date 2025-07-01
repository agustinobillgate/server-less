
DEFINE INPUT PARAMETER curr-dept    AS INTEGER.
DEFINE INPUT PARAMETER deposit-amt  AS DECIMAL.
DEFINE INPUT PARAMETER deposit-pay  AS DECIMAL.
DEFINE INPUT PARAMETER ns-billno    AS INTEGER.
DEFINE INPUT PARAMETER gastno       AS INTEGER.
DEFINE OUTPUT PARAMETER str-line    AS CHARACTER.
DEFINE OUTPUT PARAMETER str-line2   AS CHARACTER.
DEFINE OUTPUT PARAMETER str-line3   AS CHARACTER.
DEFINE OUTPUT PARAMETER dept-name   AS CHARACTER.

DEFINE VARIABLE art-name AS CHARACTER.
DEFINE VARIABLE depopay-art AS CHARACTER.
DEFINE VARIABLE str-saldo AS CHARACTER.
DEFINE VARIABLE depoart AS INTEGER.


FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN dept-name = hoteldpt.depart.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart = htparam.finteger.

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
str-line = STRING(art-name, "x(15)") + " " + STRING(deposit-amt, "->>,>>>,>>9.99").

FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ gastno 
    AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
    AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:
    FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
        AND bill-line.artnr NE depoart NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN
    DO:
        depopay-art = bill-line.bezeich.
    END.
END.
str-line2 = STRING(depopay-art, "x(15)") + " " + STRING(deposit-pay, "->>,>>>,>>9.99").
str-saldo = "Balance".
str-line3 = STRING(str-saldo, "x(15)") + " " + STRING(0, "->>,>>>,>>9.99").
