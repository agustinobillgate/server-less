DEFINE TEMP-TABLE slist 
    FIELD datum AS DATE    FORMAT "99/99/99" LABEL "Date"
    FIELD hnr   AS INTEGER FORMAT ">>>9"     LABEL "No"
    FIELD hname AS CHAR    FORMAT "x(42)"    LABEL "HotelName"
    FIELD totrm AS INTEGER FORMAT ">>>9"      LABEL "SaleableRm"    /*ger ">>9"*/
    FIELD occrm AS INTEGER FORMAT ">>>9"      LABEL "PayingRm"      /*ger ">>9"*/
    FIELD comrm AS INTEGER FORMAT ">>>9"      LABEL "CompliRm" /*M 010612 -> split occRm into paying and compliment */      /*ger ">>9"*/
    FIELD rmrev AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" LABEL "RoomRevenue"
    .

DEFINE TEMP-TABLE tlist    
    FIELD datum AS DATE
    .

DEFINE BUFFER buf-zinrstat FOR zinrstat.

DEF INPUT PARAMETER from-date AS DATE. /*FD*/
DEF INPUT PARAMETER to-date AS DATE. /*FD*/
DEF INPUT PARAMETER TABLE FOR slist.

/* FD Comment: Query Ori
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
*/

/*FD Oct 13, 2021*/
FOR EACH zinrstat WHERE zinrstat.zinr = "Competitor"
    AND zinrstat.datum GE from-date
    AND zinrstat.datum LE to-date:

    DELETE zinrstat.
END.

FOR EACH slist NO-LOCK:
    CREATE zinrstat.
    ASSIGN zinrstat.zinr        = "Competitor"
        zinrstat.datum          = slist.datum
        zinrstat.betriebsnr     = slist.hnr
        zinrstat.zimmeranz      = slist.totrm
        zinrstat.personen       = slist.occrm
        zinrstat.argtumsatz     = DEC(slist.comrm) /*MT 05/09/12 wrong read data DEC(slist.occrm) /*M 010612 -> split occRm into paying and compliment */*/
        zinrstat.logisumsatz    = slist.rmrev.
    FIND CURRENT zinrstat NO-LOCK.
END.
/*End FD*/
