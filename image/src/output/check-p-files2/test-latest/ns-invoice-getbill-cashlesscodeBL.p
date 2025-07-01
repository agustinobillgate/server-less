
DEFINE INPUT PARAMETER mode-type AS INTEGER.
DEFINE INPUT PARAMETER qr-code AS CHARACTER.
DEFINE INPUT PARAMETER curr-dept AS INTEGER.
DEFINE OUTPUT PARAMETER bill-recid AS INTEGER.
DEFINE OUTPUT PARAMETER gname AS CHARACTER.

DEFINE VARIABLE str-qrcode AS CHARACTER NO-UNDO.

str-qrcode = TRIM(qr-code).

FIND FIRST bill WHERE bill.flag EQ 0 AND bill.rechnr GT 0
    AND bill.billtyp EQ curr-dept AND bill.vesrdepot2 EQ str-qrcode
    AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:
    bill-recid = RECID(bill).

    FIND FIRST guest WHERE guest.gastnr EQ bill.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        gname = guest.NAME.
    END.
END.
