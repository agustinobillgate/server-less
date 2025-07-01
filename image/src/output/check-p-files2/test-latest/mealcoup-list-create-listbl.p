 
DEFINE TEMP-TABLE mlist LIKE mealcoup.

DEF INPUT  PARAMETER from-date   AS DATE.
DEF INPUT  PARAMETER to-date     AS DATE.
DEF OUTPUT PARAMETER TABLE FOR mlist.

RUN create-list.

PROCEDURE create-list:
    DEF VAR rmNo LIKE zimmer.zinr.

    FOR EACH mlist:
        DELETE mlist.
    END.
    
    FOR EACH h-journal WHERE h-journal.bill-datum GE from-date AND
        h-journal.bill-datum LE to-date NO-LOCK,
        FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr AND 
        h-bill.departement = h-journal.departement NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr AND
        h-journal.departement = h-artikel.departement AND 
        h-artikel.artart = 12 NO-LOCK BY h-journal.bill-datum :

        
        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr
            AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
            rmNo = res-line.zinr.
        ELSE rmNo = "".
        FIND FIRST mlist WHERE mlist.resnr = h-bill.resnr AND 
            mlist.zinr = rmNo NO-ERROR.
        IF NOT AVAILABLE mlist THEN
        DO:
            CREATE mlist.
            ASSIGN 
                mlist.resnr = h-bill.resnr
                mlist.zinr  = rmNo
                mlist.NAME  = h-bill.bilname.
            .
            IF AVAILABLE res-line THEN
                ASSIGN
                mlist.ankunft = res-line.ankunft
                mlist.abreise = res-line.abreise.
        END.
        ASSIGN 
            mlist.verbrauch[DAY(h-journal.bill-datum)] = h-journal.anzahl
            mlist.verbrauch[32] = mlist.verbrauch[32] + h-journal.anzahl.
    END.
END.
