
DEF INPUT PARAMETER request1-zinr AS CHAR.
DEF INPUT PARAMETER ci-date AS DATE.

DEF OUTPUT PARAMETER request1-gastnr AS INT.
DEF OUTPUT PARAMETER guestname AS CHAR.
DEF OUTPUT PARAMETER str AS CHAR FORMAT "x(60)" NO-UNDO.

DEF BUFFER resline1 FOR res-line.              
DEF BUFFER guest1 FOR guest.              
/*MTDEF VAR str AS CHAR  FORMAT "x(60)" NO-UNDO.*/

FIND FIRST resline1 WHERE resline1.active-flag = 1 AND resline1.zinr = request1-zinr
    AND resline1.resstatus NE 13 AND resline1.ankunft LE ci-date 
    AND resline1.abreise GE ci-date USE-INDEX zinr_index NO-LOCK NO-ERROR.
IF AVAILABLE resline1 THEN
DO:
    FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
        USE-INDEX gastnr_index NO-LOCK NO-ERROR.
    IF AVAILABLE guest1 THEN
    DO:
        request1-gastnr = resline1.gastnrmember.
        guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
            guest1.anrede1 + guest1.anredefirma.
    END.

    str = "InHouse Guest : " + Guestname + CHR(13) + 
          "Expected Departure " +  string(resline1.abreise, "99/99/99")  + " " + STRING(resline1.abreisezeit , "HH:MM").
END.
ELSE
DO:

    FIND FIRST resline1 WHERE resline1.active-flag = 0 AND resline1.zinr = request1-zinr
        AND resline1.resstatus NE 13 AND resline1.ankunft LE ci-date 
    AND resline1.abreise GE ci-date USE-INDEX zinr_index NO-LOCK NO-ERROR.
    IF AVAILABLE resline1 THEN
    DO:
        FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN
        DO:
            request1-gastnr = resline1.gastnrmember.
            guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
                guest1.anrede1 + guest1.anredefirma.
        END.

        str = "Reservation Guest : " + Guestname + CHR(13) + 
              "Expected Arrival " +  string(resline1.ankunft, "99/99/99")  + " " + STRING(resline1.ankzeit , "HH:MM").
    END.
    ELSE
    DO:
        str = "Reservation or Inhouse record not found".
    END.
END.

/*MT
VIEW FRAME frame6.

ASSIGN Zinr-info = str.

DISP Zinr-info btn-exit6 WITH FRAME frame6.
ENABLE Zinr-info btn-exit6 WITH FRAME frame6. 
ASSIGN zinr-info:READ-ONLY IN FRAME frame6 = TRUE
       zinr-info:BGCOL IN FRAME frame6 = 15.
APPLY "entry" TO btn-exit6 .
WAIT-FOR CHOOSE OF btn-exit6.  
HIDE FRAME frame6 NO-PAUSE.
/*APPLY "entry" TO stat-combo IN FRAME frame1.*/
*/
