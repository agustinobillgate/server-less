
DEF INPUT-OUTPUT PARAMETER guest-gastnr AS INT.
DEF INPUT-OUTPUT PARAMETER lname        AS CHAR.
DEF INPUT  PARAMETER akt-line1-gastnr   AS INT.
DEF OUTPUT PARAMETER guest1-gastnr      AS INT.
DEF OUTPUT PARAMETER guest-name         AS CHAR.
DEF OUTPUT PARAMETER avail-guest1       AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-guest        AS LOGICAL INIT NO.

DEFINE buffer guest1 FOR guest. 

FIND FIRST guest1 WHERE guest1.name = lname OR 
    (guest1.NAME + ", " + guest1.anredefirma) = lname NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest1 THEN .
ELSE 
DO:
    avail-guest1 = YES.
    guest1-gastnr = guest1.gastnr.
    FIND FIRST guest WHERE guest.gastnr = guest1.gastnr NO-LOCK. 
    IF AVAILABLE guest AND guest.NAME NE "" THEN
    DO:
        lname = guest.NAME + ", " + guest.anredefirma. 
        guest-gastnr = guest.gastnr.
        avail-guest = YES.
        guest-name = "".
    END.
END.

