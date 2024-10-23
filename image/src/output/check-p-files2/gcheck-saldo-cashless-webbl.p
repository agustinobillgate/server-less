/*FDL => API for check saldo cashless from guest mobile phone browse*/

DEFINE INPUT PARAMETER guest-name       AS CHARACTER.
DEFINE INPUT PARAMETER cashless-code    AS CHARACTER.
DEFINE OUTPUT PARAMETER cashless-saldo  AS DECIMAL.
/*
DEFINE VARIABLE guest-name       AS CHARACTER INIT "Dummy, Guest".
DEFINE VARIABLE cashless-code    AS CHARACTER INIT "2216038154201".
DEFINE VARIABLE  cashless-saldo  AS DECIMAL.
*/
DEFINE VARIABLE str-code AS CHARACTER NO-UNDO.

str-code = TRIM(cashless-code).

IF str-code EQ ? THEN str-code = "".
ELSE IF guest-name EQ ? THEN guest-name = "".

IF str-code NE "" THEN
DO:
    FIND FIRST bill WHERE bill.flag EQ 0 AND bill.rechnr GT 0    
        AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
        AND bill.vesrdepot2 EQ str-code
        AND bill.NAME MATCHES("*" + guest-name + "*") NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
        cashless-saldo = bill.saldo.
    END.
END.

