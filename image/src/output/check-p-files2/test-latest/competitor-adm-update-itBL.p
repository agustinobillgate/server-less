DEFINE TEMP-TABLE slist 
    FIELD datum AS DATE    FORMAT "99/99/99" LABEL "Date"
    FIELD hnr   AS INTEGER FORMAT ">>>9"     LABEL "No"
    FIELD hname AS CHAR    FORMAT "x(42)"    LABEL "HotelName"
    FIELD totrm AS INTEGER FORMAT ">>>9"      LABEL "SaleableRm"    /*ger ">>9"*/
    FIELD occrm AS INTEGER FORMAT ">>>9"      LABEL "PayingRm"      /*ger ">>9"*/
    FIELD comrm AS INTEGER FORMAT ">>>9"      LABEL "CompliRm" /*M 010612 -> split occRm into paying and compliment */      /*ger ">>9"*/
    FIELD rmrev AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" LABEL "RoomRevenue"
    .

DEF INPUT PARAMETER TABLE FOR slist.

FOR EACH slist NO-LOCK:
    FIND FIRST zinrstat WHERE zinrstat.zinr = "Competitor"
        AND zinrstat.datum = slist.datum
        AND zinrstat.betriebsnr = slist.hnr
        EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN
    DO:
        ASSIGN zinrstat.zimmeranz = slist.totrm
            zinrstat.personen = slist.occrm
            zinrstat.argtumsatz = DEC(slist.comrm) /*M 010612 -> split occRm into paying and compliment */
            zinrstat.logisumsatz = slist.rmrev.
        FIND CURRENT zinrstat NO-LOCK.
    END.
END.
