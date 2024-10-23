
DEFINE TEMP-TABLE nation-list
    FIELD nr        AS INTEGER
    FIELD kurzbez   AS CHAR
    FIELD bezeich   AS CHAR FORMAT "x(32)".

DEFINE INPUT PARAMETER gastnr    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER err-flag AS INTEGER NO-UNDO.


DEFINE VARIABLE curr-nat     AS CHAR    NO-UNDO.

FOR EACH nation WHERE nation.natcode = 0 NO-LOCK,
    FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe
        AND queasy.char1 MATCHES "*europe*" NO-LOCK BY nation.kurzbez:
    CREATE nation-list.
    ASSIGN nation-list.nr      = nation.nationnr
           nation-list.kurzbez = nation.kurzbez
           nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
END.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN DO:

    IF guest.land NE " " THEN ASSIGN curr-nat = guest.land.
    ELSE IF guest.nation1 NE " " THEN ASSIGN curr-nat = guest.nation1.

    FIND FIRST nation-list WHERE nation-list.kurzbez = curr-nat NO-LOCK NO-ERROR.
    IF AVAILABLE nation-list THEN ASSIGN err-flag = 1.

    /*gerald gdpr can't active if has membership card 180121*/
    FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN err-flag = 2.

END.
