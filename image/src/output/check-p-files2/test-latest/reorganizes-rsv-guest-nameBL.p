
DEFINE OUTPUT PARAMETER v-success AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER counter AS INTEGER.

DEFINE VARIABLE gname AS CHARACTER.

FIND FIRST res-line WHERE res-line.resstatus NE 8
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
    AND res-line.resstatus NE 12 AND res-line.resstatus NE 99
    AND res-line.gastnrmember GT 0 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE res-line:

    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
        IF res-line.name NE gname THEN
        DO:
            FIND CURRENT res-line EXCLUSIVE-LOCK.
            res-line.name = gname.
            FIND CURRENT res-line NO-LOCK.            
            counter = counter + 1.
        END.            
    END.
    FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN
    DO:
        IF reservation.gastnr NE res-line.gastnr THEN
        DO:
            FIND CURRENT res-line EXCLUSIVE-LOCK.
            res-line.gastnr = reservation.gastnr.
            FIND CURRENT res-line NO-LOCK.            
            counter = counter + 1.
        END.        
    END.

    FIND NEXT res-line WHERE res-line.resstatus NE 8
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
        AND res-line.resstatus NE 12 AND res-line.resstatus NE 99
        AND res-line.gastnrmember GT 0 NO-LOCK NO-ERROR.
END.
RELEASE res-line.
v-success = YES.

