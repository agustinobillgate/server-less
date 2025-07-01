

DEF INPUT  PARAMETER curr-select AS CHAR.
DEF INPUT  PARAMETER int1          AS INTEGER.
DEF INPUT  PARAMETER char1    AS CHAR.
DEF OUTPUT PARAMETER char2  AS CHAR.

DEFINE BUFFER usr       FOR bediener.
DEFINE BUFFER guest0    FOR guest.
IF curr-select = "sales-id" THEN
DO:
    IF int1 GT 0 THEN
    DO:
        FIND FIRST usr WHERE usr.userinit = char1 NO-LOCK.
        char2 = usr.username.
    END.
END.
ELSE IF curr-select = "master" THEN
DO:
    FIND FIRST guest0 WHERE guest0.gastnr = int1 NO-LOCK.
    /*mastername = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma 
               + " " + guest0.anrede1. */
    char2 = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma 
               + " " + guest0.anrede1.
END.
IF curr-select = "payment" THEN 
DO:
    FIND FIRST artikel WHERE artikel.artnr = /*payment*/ int1 AND 
        artikel.departement = 0 NO-LOCK NO-ERROR.
    /*pay-bezeich = artikel.bezeich. */
    char2 = artikel.bezeich.
END.
