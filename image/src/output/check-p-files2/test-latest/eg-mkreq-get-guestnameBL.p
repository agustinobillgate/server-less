
DEF INPUT PARAMETER request1-zinr AS CHAR.
DEF INPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER request1-gastnr AS INT.
DEF OUTPUT PARAMETER guestname AS CHAR.
DEF OUTPUT PARAMETER request1-resnr AS INT.
DEF OUTPUT PARAMETER request1-reslinnr AS INT.

RUN get-guestname.

PROCEDURE get-guestname:
    DEF BUFFER resline1 FOR res-line.              
    DEF BUFFER guest1 FOR guest.              

    FIND FIRST resline1 WHERE resline1.active-flag = 1 AND resline1.zinr = 
        request1-zinr AND resline1.resstatus NE 12 AND resline1.ankunft LE ci-date
        AND resline1.abreise GE ci-date NO-LOCK NO-ERROR.
    IF AVAILABLE resline1 THEN
    DO:
        FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN
        DO:
            request1-gastnr = resline1.gastnrmember.
            guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
                guest1.anrede1 + guest1.anredefirma.
            request1-resnr = resline1.resnr.
            request1-reslinnr = resline1.reslinnr.
        END.
    END.
END.
