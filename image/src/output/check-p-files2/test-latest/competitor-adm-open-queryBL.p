DEFINE TEMP-TABLE slist 
    FIELD datum AS DATE    FORMAT "99/99/99" LABEL "Date"
    FIELD hnr   AS INTEGER FORMAT ">>>9"     LABEL "No"
    FIELD hname AS CHAR    FORMAT "x(42)"    LABEL "HotelName"
    FIELD totrm AS INTEGER FORMAT ">>>9"      LABEL "SaleableRm" /*ger ">>9"*/
    FIELD occrm AS INTEGER FORMAT ">>>9"      LABEL "PayingRm"   /*ger ">>9"*/
    FIELD comrm AS INTEGER FORMAT ">>>9"      LABEL "CompliRm" /*M 010612 -> split occRm into paying and compliment */ /*ger ">>9"*/
    FIELD rmrev AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" LABEL "RoomRevenue"
    .

DEF INPUT  PARAMETER from-date   AS DATE.
DEF INPUT  PARAMETER to-date     AS DATE.
DEF OUTPUT PARAMETER TABLE FOR slist.

FOR EACH slist:
    DELETE slist.
END.
FOR EACH zinrstat WHERE zinrstat.zinr = "Competitor"
    AND zinrstat.datum GE from-date
    AND zinrstat.datum LE to-date NO-LOCK :
    CREATE slist.
    ASSIGN slist.datum = zinrstat.datum
        slist.hnr      = zinrstat.betriebsnr
        slist.totrm    = zinrstat.zimmeranz
        slist.occrm    = zinrstat.personen
        slist.comrm    = INT(zinrstat.argtumsatz) /*M 010612 -> split occRm into paying and compliment */
        slist.rmrev    = zinrstat.logisumsatz.
    /*FIND FIRST queasy WHERE queasy.KEY = 136 AND queasy.number1 = 
        zinrstat.betriebsnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
        slist.hname    = queasy.char3.*/
    FIND FIRST akt-code WHERE akt-code.aktionscode = zinrstat.betriebsnr
        AND akt-code.aktiongrup = 4 NO-LOCK NO-ERROR.
    IF AVAILABLE akt-code THEN slist.hname = akt-code.bezeich.
END.
