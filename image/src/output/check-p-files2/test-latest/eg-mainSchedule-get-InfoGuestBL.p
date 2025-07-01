
DEF INPUT PARAMETER h-zinr AS CHAR.
DEF OUTPUT PARAMETER str AS CHAR  FORMAT "x(60)" NO-UNDO.


DEF VAR guestname AS CHAR.
DEF BUFFER resline1 FOR res-line.              
DEF BUFFER guest1 FOR guest.              


FIND FIRST resline1 WHERE resline1.active-flag = 1 AND resline1.zinr = h-zinr /*"415" h-zinr*/ 
    AND resline1.resstatus NE 13 USE-INDEX zinr_index NO-LOCK NO-ERROR.
IF AVAILABLE resline1 THEN
DO:

    FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
        USE-INDEX gastnr_index NO-LOCK NO-ERROR.
    IF AVAILABLE guest1 THEN
    DO:
        guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
            guest1.anrede1 + guest1.anredefirma.
    END.

    str = "InHouse Guest : " + Guestname + CHR(13) + 
          "Expected Departure " +  string(resline1.abreise, "99/99/99")  + " " + STRING(resline1.abreisezeit , "HH:MM").

END.
ELSE
DO:

    FIND FIRST resline1 WHERE resline1.active-flag = 0 AND resline1.zinr = h-zinr /*"415" h-zinr*/ 
        AND resline1.resstatus NE 13 USE-INDEX zinr_index NO-LOCK NO-ERROR.
    IF AVAILABLE resline1 THEN
    DO:
        FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN
        DO:
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
