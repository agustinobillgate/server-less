DEF TEMP-TABLE lod-list
    FIELD resnr AS INTEGER
    FIELD reslinnr AS INTEGER
    FIELD zinr LIKE zimmer.zinr                      LABEL "RmNo"
    FIELD rmrate AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "RmRev"
    FIELD lodge  AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "Lodging"
    FIELD bfast  AS DECIMAL FORMAT "->>>,>>9.99"     LABEL "Other"
    FIELD tot    AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "Lodging+Other".

DEF INPUT PARAMETER currdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR lod-list.

RUN show-lodging.

PROCEDURE show-lodging:
    DEF VAR do-it AS LOGICAL INITIAL NO.
    FOR EACH lod-list:
        DELETE lod-list.
    END.
    FOR EACH bill-line WHERE bill-line.bill-datum = currdate 
        AND bill-line.artnr = 99 AND bill-line.departement = 0 NO-LOCK,
        FIRST bill WHERE bill.rechnr = bill-line.rechnr NO-LOCK :
        CREATE lod-list.
        ASSIGN lod-list.zinr = bill-line.zinr
            lod-list.rmrate  = bill-line.betrag
            lod-list.resnr   = bill.resnr.
    END.

    FOR EACH lod-list:
        FIND FIRST billjournal WHERE billjournal.departement = 0 AND 
            billjournal.zinr = lod-list.zinr AND billjournal.bill-datum = 
            currdate AND billjournal.artnr = 100 NO-LOCK NO-ERROR.
        IF AVAILABLE billjournal THEN
            ASSIGN lod-list.lodge = billjournal.betrag
            lod-list.tot = billjournal.betrag.

        FIND FIRST res-line WHERE res-line.zinr = lod-list.zinr 
            AND res-line.resnr = lod-list.resnr NO-LOCK NO-ERROR.
        do-it = AVAILABLE res-line.        

        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement
            NO-LOCK NO-ERROR.
        do-it = AVAILABLE arrangement.
        IF do-it THEN
        DO:
            FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK:
                FIND FIRST billjournal WHERE billjournal.departement NE 0 AND 
                    billjournal.zinr = lod-list.zinr AND billjournal.bill-datum = 
                    currdate AND billjournal.artnr = argt-line.argt-artnr NO-LOCK NO-ERROR.
                IF AVAILABLE billjournal THEN
                    ASSIGN lod-list.bfast = lod-list.bfast + billjournal.betrag
                    lod-list.tot = lod-list.lodge + lod-list.bfast.
            END.
        END.
    END.    /*each lod-list*/
END.
