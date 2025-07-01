DEF INPUT PARAMETER dept        AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER billno      AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER inp-resnr   AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER inp-line    AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER billnr      AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER transdate   AS DATE             NO-UNDO.


DEFINE VARIABLE billdate        AS DATE             NO-UNDO.
DEFINE VARIABLE do-it           AS LOGICAL          NO-UNDO.
DEFINE VARIABLE pax             AS INTEGER          NO-UNDO.

FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = dept
    AND vhp.h-bill.rechnr = billno NO-LOCK NO-ERROR.
IF NOT AVAILABLE vhp.h-bill THEN RETURN.

FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = inp-resnr
    AND vhp.res-line.reslinnr = inp-line NO-LOCK NO-ERROR.

IF AVAILABLE vhp.res-line THEN 
    FIND FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.res-line.gastnrmember NO-LOCK NO-ERROR.
ELSE IF inp-resnr GT 0 THEN 
    FIND FIRST vhp.guest WHERE vhp.guest.gastnr = inp-resnr NO-LOCK NO-ERROR.

IF NOT AVAILABLE vhp.guest THEN RETURN.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK.
IF transdate NE ? THEN billdate = transdate.
ELSE billdate = vhp.htparam.fdate.

DO TRANSACTION:
    /*
    FIND FIRST vhp.guest-queasy WHERE vhp.guest-queasy.KEY = "gast-info"
        AND vhp.guest-queasy.gastnr  = vhp.guest.gastnr
        AND vhp.guest-queasy.number1 = dept
        AND vhp.guest-queasy.number2 = inp-resnr
        AND vhp.guest-queasy.number3 = inp-line
        AND vhp.guest-queasy.date1   = billdate NO-LOCK NO-ERROR.
    IF NOT AVAILABLE vhp.guest-queasy THEN
    */
    DO:
        CREATE vhp.guest-queasy.
        ASSIGN
            vhp.guest-queasy.KEY     = "gast-info"
            vhp.guest-queasy.gastnr  = guest.gastnr
            vhp.guest-queasy.number1 = dept 
            vhp.guest-queasy.number2 = inp-resnr
            vhp.guest-queasy.number3 = inp-line 
            vhp.guest-queasy.date1   = billdate
            vhp.guest-queasy.date2   = billdate
        .
    END.
    
    FIND CURRENT vhp.guest-queasy EXCLUSIVE-LOCK.
    ASSIGN 
        vhp.guest-queasy.char3 = STRING(INTEGER(vhp.guest-queasy.char3) + vhp.h-bill.belegung)
        vhp.guest-queasy.char1 = STRING(vhp.h-bill.rechnr)
    . 
    
    IF vhp.guest-queasy.date2 LT billdate THEN ASSIGN vhp.guest-queasy.date2 = billdate.
    
    FOR EACH vhp.h-journal WHERE vhp.h-journal.bill-datum = billdate
        AND vhp.h-journal.departement = dept
        AND vhp.h-journal.rechnr = billno
        AND vhp.h-journal.artnr NE 0 NO-LOCK:

        IF billnr = 0 THEN do-it = YES.
        ELSE do-it = vhp.h-journal.waehrungcode = billnr.
        IF do-it THEN
        DO:
            FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-journal.artnr 
                AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR.
            IF AVAILABLE vhp.h-artikel AND vhp.h-artikel.artart = 0 THEN
            DO:
                FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront 
                    AND vhp.artikel.departement = dept NO-LOCK NO-ERROR.
                IF AVAILABLE vhp.artikel THEN
                DO:
                    IF vhp.artikel.umsatzart = 3 OR vhp.artikel.umsatzart = 5 THEN
                        ASSIGN vhp.guest-queasy.deci1 = vhp.guest-queasy.deci1 + vhp.h-journal.betrag.
                    ELSE IF vhp.artikel.umsatzart = 6 THEN
                        ASSIGN vhp.guest-queasy.deci2 = vhp.guest-queasy.deci2 + vhp.h-journal.betrag.
                    ELSE
                        ASSIGN vhp.guest-queasy.deci3 = vhp.guest-queasy.deci3 + vhp.h-journal.betrag.
                END.
            END.
        END.
    END.
    
    FIND CURRENT vhp.guest-queasy NO-LOCK.
    RELEASE vhp.guest-queasy.
END.
