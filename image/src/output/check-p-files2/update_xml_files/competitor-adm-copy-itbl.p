DEFINE TEMP-TABLE slist 
    FIELD datum AS DATE    FORMAT "99/99/99" LABEL "Date"
    FIELD hnr   AS INTEGER FORMAT ">>>9"     LABEL "No"
    FIELD hname AS CHAR    FORMAT "x(42)"    LABEL "HotelName"
    FIELD totrm AS INTEGER FORMAT ">>>9"      LABEL "SaleableRm" /*ger ">>9"*/
    FIELD occrm AS INTEGER FORMAT ">>>9"      LABEL "PayingRm"   /*ger ">>9"*/
    FIELD comrm AS INTEGER FORMAT ">>>9"      LABEL "CompliRm" /*M 010612 -> split occRm into paying and compliment */ /*ger ">>9"*/
    FIELD rmrev AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" LABEL "RoomRevenue"
    .

DEFINE OUTPUT PARAMETER TABLE FOR slist.

DEFINE VARIABLE curr-date AS DATE NO-UNDO.

FOR EACH slist:
    DELETE slist.
END.

FOR EACH zinrstat WHERE zinrstat.zinr = "Competitor" NO-LOCK BY zinrstat.datum DESC:

    IF curr-date NE ? AND curr-date NE zinrstat.datum THEN LEAVE.

    CREATE slist.
    ASSIGN 
        slist.datum    = zinrstat.datum + 1
        slist.hnr      = zinrstat.betriebsnr
        slist.totrm    = zinrstat.zimmeranz
        curr-date      = zinrstat.datum
        .        

    FIND FIRST akt-code WHERE akt-code.aktionscode = zinrstat.betriebsnr
        AND akt-code.aktiongrup = 4 NO-LOCK NO-ERROR.
    IF AVAILABLE akt-code THEN slist.hname = akt-code.bezeich.
END.

