
DEFINE INPUT  PARAMETER gastNo  AS INT.
DEFINE OUTPUT PARAMETER gname   AS CHAR.
DEFINE OUTPUT PARAMETER telefon AS CHAR.

FIND FIRST guest WHERE guest.gastnr EQ gastNo NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN 
DO:
    gname   = guest.NAME + "," + guest.vorname1.
    telefon = guest.telefon.
END.


