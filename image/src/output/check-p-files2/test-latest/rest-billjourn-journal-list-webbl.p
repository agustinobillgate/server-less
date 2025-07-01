
DEFINE TEMP-TABLE booking-journbill-list
    FIELD datum         AS DATE 
    FIELD tabelno       AS CHAR
    FIELD billno        AS INTEGER
    FIELD artno         AS INTEGER
    FIELD descr         AS CHAR
    FIELD qty           AS INTEGER
    FIELD sales         AS DECIMAL
    FIELD payment       AS DECIMAL
    FIELD depart        AS CHARACTER
    FIELD id            AS CHARACTER
    FIELD zeit          AS CHARACTER    
    FIELD gname         AS CHARACTER
    FIELD rmno          AS CHARACTER
    FIELD st-optable    AS CHARACTER /*FDL Dec 26, 2023*/
    FIELD ct-optable    AS CHARACTER /*FDL Dec 26, 2023*/
.  

DEF INPUT  PARAMETER from-art      AS INT.
DEF INPUT  PARAMETER from-dept     AS INT.
DEF INPUT  PARAMETER to-dept       AS INT.
DEF INPUT  PARAMETER from-date     AS DATE.
DEF INPUT  PARAMETER to-date       AS DATE.
DEF INPUT  PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER TABLE FOR booking-journbill-list.

DEFINE VARIABLE disc-art1 AS INTEGER.
DEFINE VARIABLE disc-art2 AS INTEGER.
DEFINE VARIABLE disc-art3 AS INTEGER.

/*FD July 19, 2021*/
FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
disc-art1 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
disc-art2 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. 
disc-art3 = vhp.htparam.finteger.

RUN journal-list.

PROCEDURE journal-list: 
    DEFINE VARIABLE qty AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE sub-tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE sub-tot1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE curr-date AS DATE. 
    DEFINE VARIABLE last-dept AS INTEGER INITIAL -1. 
    DEFINE VARIABLE it-exist AS LOGICAL. 
    DEFINE VARIABLE curr-guest AS CHARACTER.    /*sis 200814*/
    DEFINE VARIABLE curr-room  AS CHARACTER.    /*DO 231219*/
    DEFINE VARIABLE bill-no AS INTEGER.
    DEFINE VARIABLE dept-no AS INTEGER.
    DEFINE VARIABLE curr-time AS CHARACTER.
    DEFINE VARIABLE art-pay AS INTEGER.

    DEFINE BUFFER buf-hjournal FOR h-journal.
    DEFINE BUFFER buf-hart FOR h-artikel.

    FOR EACH booking-journbill-list: 
        DELETE booking-journbill-list. 
    END. 
 
    IF from-art = 0 THEN 
    FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
        sub-tot = 0. 
        sub-tot1 = 0. 
        it-exist = NO. 
        qty = 0. 
        bill-no = 0.
        dept-no = hoteldpt.num.
        curr-time = "".
        art-pay = 0.

        DO curr-date = from-date TO to-date: 
            FOR EACH h-journal WHERE h-journal.bill-datum = curr-date 
                AND h-journal.departement = hoteldpt.num NO-LOCK BY h-journal.rechnr BY h-journal.sysdate BY h-journal.zeit: 
                FIND FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr AND h-artikel.departement = h-journal.departement NO-LOCK NO-ERROR. 
                it-exist = YES. 
                
                /*sis 200814*/
                curr-guest = "".
                curr-room  = "".
                FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
                    AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                IF AVAILABLE h-bill THEN
                DO:
                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN
                        DO:
                            ASSIGN
                                curr-guest = res-line.NAME
                                curr-room  = res-line.zinr.
                        END.                            
                    END.
                    ELSE IF h-bill.resnr GT 0 THEN
                    DO:
                        FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN
                        ASSIGN
                            curr-guest = guest.NAME + "," + guest.vorname1
                            curr-room  = "".
                    END.
                    ELSE IF h-bill.resnr = 0 THEN /*FD Jan 17, 2020*/
                    DO:
                        ASSIGN
                            curr-guest = h-bill.bilname
                            curr-room  = "".
                    END.
                END. /*end sis*/
                        
                /*FD July 19, 2021*/
                IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
                    OR h-journal.artnr EQ disc-art2) AND h-journal.betrag EQ 0 THEN .
                ELSE
                DO:
                    CREATE booking-journbill-list. 
                    ASSIGN
                        booking-journbill-list.gname    = curr-guest
                        booking-journbill-list.datum    = h-journal.bill-datum
                        booking-journbill-list.tabelno  = STRING(h-journal.tischnr, ">>>9")
                        booking-journbill-list.billno   = h-journal.rechnr
                        booking-journbill-list.artno    = h-journal.artnr
                        booking-journbill-list.descr    = h-journal.bezeich
                        booking-journbill-list.depart   = hoteldpt.depart
                        booking-journbill-list.qty      = h-journal.anzahl
                    .
                                                
                    IF AVAILABLE h-artikel AND h-artikel.artart = 0 THEN 
                    DO: 
                        IF price-decimal = 2 THEN
                        DO:
                            booking-journbill-list.sales = h-journal.betrag.
                            booking-journbill-list.payment = 0.
                        END.                            
                        ELSE 
                        DO:
                            booking-journbill-list.sales = h-journal.betrag.
                            booking-journbill-list.payment = 0.
                        END.

                        /*FDL Dec 26, 2023 => Ticket 597441*/
                        IF bill-no NE h-journal.rechnr
                            AND dept-no EQ h-journal.departement THEN
                        DO:
                            curr-time = STRING(h-journal.zeit, "HH:MM:SS").
                        END.
                        booking-journbill-list.st-optable = curr-time.                                                                                             

                        sub-tot = sub-tot + h-journal.betrag. 
                        tot     = tot + h-journal.betrag. 
                    END. 
                    ELSE IF h-journal.artnr = 0 AND SUBSTR(h-journal.bezeich, 1, 9) = "To Table " THEN 
                    DO: 
                        IF price-decimal = 2 THEN
                        DO:
                            booking-journbill-list.sales = h-journal.betrag.
                            booking-journbill-list.payment = 0.
                        END.                            
                        ELSE 
                        DO:
                            booking-journbill-list.sales = h-journal.betrag.
                            booking-journbill-list.payment = 0.
                        END.

                        sub-tot = sub-tot + h-journal.betrag. 
                        tot     = tot + h-journal.betrag. 
                    END. 
                    ELSE IF h-journal.artnr = 0 AND SUBSTR(h-journal.bezeich, 1, 11) = "From Table " THEN 
                    DO: 
                        IF price-decimal = 2 THEN
                        DO:
                            booking-journbill-list.sales = h-journal.betrag.
                            booking-journbill-list.payment = 0.
                        END.                            
                        ELSE 
                        DO:
                            booking-journbill-list.sales = h-journal.betrag.
                            booking-journbill-list.payment = 0.
                        END.

                        sub-tot = sub-tot + h-journal.betrag. 
                        tot     = tot + h-journal.betrag. 
                    END. 
                    ELSE 
                    DO: 
                        IF price-decimal = 2 THEN
                        DO:
                            booking-journbill-list.sales = 0.
                            booking-journbill-list.payment = h-journal.betrag.
                        END.                            
                        ELSE 
                        DO:
                            booking-journbill-list.sales = 0.
                            booking-journbill-list.payment = h-journal.betrag.
                        END.                        

                        /*FDL Dec 26, 2023 => Ticket 597441*/
                        FIND FIRST buf-hjournal WHERE buf-hjournal.rechnr EQ h-journal.rechnr
                            AND buf-hjournal.departement EQ h-journal.departement
                            AND buf-hjournal.anzahl GT 0
                            AND buf-hjournal.betrag LT 0 NO-LOCK NO-ERROR.
                        IF AVAILABLE buf-hjournal THEN
                        DO:
                            FIND FIRST buf-hart WHERE buf-hart.artnr EQ buf-hjournal.artnr
                                AND buf-hart.departement EQ buf-hjournal.departement
                                AND buf-hart.artart NE 0 NO-LOCK NO-ERROR.
                            IF AVAILABLE buf-hart THEN
                            DO:
                                booking-journbill-list.ct-optable = STRING(buf-hjournal.zeit, "HH:MM:SS").
                            END.                            
                        END.                        
                        
                        sub-tot1 = sub-tot1 + h-journal.betrag. 
                        tot1     = tot1 + h-journal.betrag. 
                    END. 
            
                    booking-journbill-list.id = STRING(h-journal.kellner-nr, "999").
                    booking-journbill-list.zeit = STRING(h-journal.zeit, "HH:MM:SS").
                    booking-journbill-list.rmno = curr-room.

                    qty = qty + h-journal.anzahl.

                    bill-no = h-journal.rechnr.
                END.                                
            END. 
            IF it-exist THEN 
            DO: 
                CREATE booking-journbill-list. 
                IF price-decimal = 2 THEN 
                DO:    
                    ASSIGN
                        booking-journbill-list.descr    = "T O T A L"
                        booking-journbill-list.qty      = qty
                        booking-journbill-list.sales    = sub-tot
                        booking-journbill-list.payment  = sub-tot1
                    .                                            
                END.
                ELSE
                DO:
                    ASSIGN
                        booking-journbill-list.descr    = "T O T A L"
                        booking-journbill-list.qty      = qty
                        booking-journbill-list.sales    = sub-tot
                        booking-journbill-list.payment  = sub-tot1
                    . 
                END.                    
            END.
        END. 
    END. 
END. 
