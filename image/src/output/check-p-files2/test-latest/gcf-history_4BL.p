DEFINE TEMP-TABLE ghistory LIKE history
    FIELD hname   AS CHARACTER FORMAT "x(24)" COLUMN-LABEL "Hotel Name"
    FIELD gname   AS CHARACTER
    FIELD address AS CHARACTER
    FIELD s-recid AS INTEGER
    FIELD vcrnr   AS CHARACTER
    FIELD mblnr   AS CHARACTER
    FIELD email   AS CHARACTER.

DEFINE TEMP-TABLE summ-list LIKE history. /*ger 66FA47*/

DEFINE BUFFER hist1 FOR history.

DEFINE INPUT PARAMETER gastnr       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER guest-phone  AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER guest-name   AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER guest-email  AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER fdate        AS DATE NO-UNDO.
DEFINE INPUT PARAMETER tdate        AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR ghistory.
DEFINE OUTPUT PARAMETER TABLE FOR summ-list. /*ger 66FA47*/

DEFINE VARIABLE htl-name    AS CHARACTER.
DEFINE VARIABLE str         AS CHARACTER.
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE gastnr1     AS INTEGER NO-UNDO. /*Hotel*/
DEFINE VARIABLE gastnr2     AS INTEGER NO-UNDO. /*HO*/

/*FDL Jan 20, 2023 - Ticket 890590*/
FIND FIRST paramtext WHERE paramtext.txtnr EQ 200 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext THEN htl-name = paramtext.ptexte.

FIND FIRST guest WHERE guest.mobil-telefon EQ guest-phone 
    AND guest.mobil-telefon NE ? 
    AND guest.mobil-telefon NE " "
    NO-LOCK NO-ERROR. /*CHECK M-PHONE*/
IF AVAILABLE guest THEN
DO:
    ASSIGN gastnr2 = guest.gastnr.
END.
ELSE
DO:
    FIND FIRST guest WHERE guest.email-adr EQ guest-email 
        AND guest.email-adr NE ? 
        AND guest.email-adr NE " "
        NO-LOCK NO-ERROR. /*CHECK EMAIL*/
    IF AVAILABLE guest THEN
    DO:
        ASSIGN gastnr2 = guest.gastnr.
    END.
END.

IF gastnr2 NE 0 THEN
DO:
    RUN create-ghistory.
END.

PROCEDURE create-ghistory:
    FOR EACH history WHERE history.gastnr = gastnr2
        AND history.abreise GE fdate 
        AND history.abreise LE tdate NO-LOCK BY history.abreise DESCENDING:

        CREATE ghistory.
        BUFFER-COPY history EXCEPT gastinfo TO ghistory.
        
        FIND FIRST hist1 WHERE hist1.resnr = history.resnr
            AND hist1.ankunft = history.ankunft 
            AND hist1.abreise = history.abreise 
            AND hist1.segmentcode = history.segmentcode 
            AND hist1.arrangement = history.arrangement NO-LOCK NO-ERROR.  
        IF AVAILABLE hist1 THEN 
        DO:
            ghistory.gastinfo  = hist1.gastinfo.
            ghistory.gname = ENTRY(1, ghistory.gastinfo, "-" ).
            IF NUM-ENTRIES(ghistory.gastinfo, "-") = 2 THEN
                ghistory.address   = ENTRY(2, ghistory.gastinfo, "-").
        END.
        
        FIND FIRST res-line WHERE res-line.zimmer-wunsch MATCHES "*voucher*"
            AND res-line.resnr EQ history.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
        DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str = ENTRY(i, res-line.zimmer-wunsch, ";").
                IF SUBSTR(str,1,7) = "voucher" THEN 
                DO:
                    ghistory.vcrnr = SUBSTR(str,8).
                END.            
            END.
        END.
        
        FIND FIRST guest WHERE guest.gastnr EQ history.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            ghistory.mblnr = guest.mobil-telefon.
            ghistory.email = guest.email-adr.
        END.
        
        FIND FIRST queasy WHERE queasy.KEY EQ 203 
            AND queasy.number1 EQ guest.gastnr 
            AND queasy.number2 EQ history.resnr
            /*AND queasy.char1 NE htl-name*/ /*NEED CHECKING*/
            NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN ghistory.hname = queasy.char1.
        END.
        ELSE
        DO:
            ASSIGN ghistory.hname = htl-name.
        END.
        
        ASSIGN ghistory.s-recid = INTEGER(RECID(history)).
    END.
        
    FOR EACH ghistory:
        FIND FIRST summ-list WHERE summ-list.gastnr = ghistory.gastnr AND summ-list.arrangement = ghistory.arrangement NO-LOCK NO-ERROR.
        IF NOT AVAILABLE summ-list THEN
        DO:
            CREATE summ-list.
            ASSIGN
                summ-list.gastnr         = ghistory.gastnr
                summ-list.zikateg        = "T O T A L"
                summ-list.arrangement    = ghistory.arrangement
                summ-list.zimmeranz      = ghistory.zimmeranz
                summ-list.zipreis        = ghistory.zipreis
                summ-list.gesamtumsatz   = ghistory.gesamtumsatz
                summ-list.argtumsatz     = ghistory.argtumsatz
                summ-list.f-b-umsatz     = ghistory.f-b-umsatz
                summ-list.sonst-umsatz   = ghistory.sonst-umsatz.
        END.
        ELSE
        DO:
            ASSIGN
                summ-list.zimmeranz      = summ-list.zimmeranz + ghistory.zimmeranz
                summ-list.zipreis        = summ-list.zipreis      + ghistory.zipreis
                summ-list.gesamtumsatz   = summ-list.gesamtumsatz + ghistory.gesamtumsatz
                summ-list.argtumsatz     = summ-list.argtumsatz   + ghistory.argtumsatz
                summ-list.f-b-umsatz     = summ-list.f-b-umsatz   + ghistory.f-b-umsatz
                summ-list.sonst-umsatz   = summ-list.sonst-umsatz + ghistory.sonst-umsatz.
        END.
        
        FIND FIRST guest WHERE guest.NAME EQ ENTRY(1,ghistory.gname,",") NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN 
        DO:
            ghistory.mblnr = guest.mobil-telefon.
            ghistory.email = guest.email-adr.
        END.
    END.
END.
