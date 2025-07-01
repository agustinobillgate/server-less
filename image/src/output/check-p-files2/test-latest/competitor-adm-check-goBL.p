DEFINE TEMP-TABLE slist 
    FIELD datum AS DATE    FORMAT "99/99/99" LABEL "Date"
    FIELD hnr   AS INTEGER FORMAT ">>>9"     LABEL "No"
    FIELD hname AS CHAR    FORMAT "x(42)"    LABEL "HotelName"
    FIELD totrm AS INTEGER FORMAT ">>>9"      LABEL "SaleableRm" /*ger ">>9"*/
    FIELD occrm AS INTEGER FORMAT ">>>9"      LABEL "PayingRm"   /*ger ">>9"*/
    FIELD comrm AS INTEGER FORMAT ">>>9"      LABEL "CompliRm" /*M 010612 -> split occRm into paying and compliment */ /*ger ">>9"*/
    FIELD rmrev AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" LABEL "RoomRevenue"
    .

DEF INPUT  PARAMETER TABLE FOR slist.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER curr-mode      AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "competitor-adm". 

DEF BUFFER sbuff FOR slist.

IF curr-mode = "new" THEN
DO:
    FOR EACH slist NO-LOCK:
        FIND FIRST zinrstat WHERE zinrstat.datum = slist.datum 
            AND zinrstat.zinr = "Competitor" AND zinrstat.betriebsnr = 
            slist.hnr NO-LOCK NO-ERROR.
        IF AVAILABLE zinrstat THEN
        DO:
            msg-str = "&W" + translateExtended("Statistic record found for date", lvCAREA, "") 
                    + " " + STRING(slist.datum) + " " 
                    + translateExtended("hotel number",lvCAREA, "") 
                    + STRING(slist.hnr) + "!".
            RETURN NO-APPLY.
        END.
    END.
END.
FOR EACH sbuff NO-LOCK:
    FIND FIRST slist WHERE slist.datum = sbuff.datum 
        AND slist.hnr = sbuff.hnr AND RECID(slist) NE RECID(sbuff)
        NO-LOCK NO-ERROR.
    IF AVAILABLE slist THEN
    DO:
        msg-str = "&W" + translateExtended("Duplicate Records found for date ", lvCAREA, "")
                + " " + STRING(slist.datum) + " " 
                + translateExtended("Hotel", lvCAREA, "") + " " 
                + STRING(slist.hnr) + "!".
        RETURN NO-APPLY.
    END.
END.
