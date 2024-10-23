
DEFINE TEMP-TABLE bill-list
    FIELD rechnr    AS INTEGER
    FIELD resnr     AS INTEGER
    FIELD reslinnr  AS INTEGER
    FIELD resv-name AS CHAR
    FIELD gname     AS CHAR
    FIELD ci        AS CHAR
    FIELD co        AS CHAR
    FIELD rmno      AS CHAR
    FIELD balanced  AS DECIMAL.

DEFINE OUTPUT PARAMETER TABLE FOR bill-list.

DEFINE VARIABLE bill-date AS DATE NO-UNDO.

RUN htpdate.p(110, OUTPUT bill-date).

FIND FIRST res-line WHERE res-line.resstatus = 8
    AND res-line.abreise = bill-date 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE res-line:

    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.

    FIND FIRST bill WHERE bill.resnr = res-line.resnr 
        AND bill.parent-nr = res-line.reslinnr
        AND bill.saldo NE 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE bill:
        CREATE bill-list.
        ASSIGN 
               bill-list.rechnr     = bill.rechnr
               bill-list.resnr      = bill.resnr
               bill-list.reslinnr   = bill.parent-nr
               bill-list.resv-name  = guest.NAME
               bill-list.gname      = res-line.NAME
               bill-list.ci         = STRING(res-line.ankunft, "99/99/9999")
               bill-list.co         = STRING(res-line.abreise, "99/99/9999")
               bill-list.rmno       = res-line.zinr
               bill-list.balanced   = bill.saldo.

        FIND NEXT bill WHERE bill.resnr = res-line.resnr AND bill.parent-nr = res-line.reslinnr
            AND bill.saldo NE 0 NO-LOCK NO-ERROR.
    END.    
    FIND NEXT res-line WHERE res-line.resstatus = 8
        AND res-line.abreise = bill-date 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
END.


