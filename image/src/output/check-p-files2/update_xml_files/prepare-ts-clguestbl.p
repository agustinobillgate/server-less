DEF TEMP-TABLE clguest-list
    FIELD gname       AS CHAR    FORMAT "x(36)" LABEL "Customer Name"
    FIELD zahlungsart AS INTEGER FORMAT ">>>9"  LABEL "C/L No"
    FIELD bezeich     AS CHAR    FORMAT "x(24)" LABEL "Description"
    FIELD address     AS CHAR    FORMAT "x(36)" LABEL "Address"
    FIELD gastnr      AS INTEGER
    FIELD karteityp   AS INTEGER
    FIELD bemerk      AS CHAR
    FIELD kreditlimit AS DECIMAL FORMAT ">>>,>>>,>>9"
.
DEFINE INPUT PARAMETER dept-number AS INT.
DEFINE INPUT PARAMETER bill-number AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR clguest-list.

DEFINE VARIABLE tada-flag AS LOGICAL.
DEFINE VARIABLE tada-guest AS CHAR.

DEFINE BUFFER orderhdr FOR queasy.

FOR EACH guest WHERE guest.karteityp = 0 
    AND guest.gastnr GT 0 AND guest.point-gastnr GT 0 NO-LOCK USE-INDEX point_index, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = guest.zahlungsart 
    AND vhp.artikel.departement = 0 AND vhp.artikel.artart = 2 NO-LOCK BY guest.NAME:
    CREATE clguest-list.
    ASSIGN
        clguest-list.gname       = guest.name + ", " + guest.vorname1 
                                 + " " + guest.anrede1 
                                 + guest.anredefirma
        clguest-list.zahlungsart = guest.zahlungsart
        clguest-list.bezeich     = artikel.bezeich
        clguest-list.address     = TRIM(guest.adresse1
                                 + " " + guest.adresse2 
                                 + " " + guest.wohnort)
        clguest-list.gastnr      = guest.gastnr
        clguest-list.karteityp   = guest.karteityp
        clguest-list.bemerk      = guest.bemerk
        clguest-list.kreditlimit = guest.kreditlimit
    .
END.

FOR EACH guest WHERE guest.karteityp GT 0 
    AND guest.gastnr GT 0 AND guest.zahlungsart GT 0 NO-LOCK USE-INDEX typevorname_ix, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = guest.zahlungsart 
    AND vhp.artikel.departement = 0 AND vhp.artikel.artart = 2 NO-LOCK BY guest.NAME:
    CREATE clguest-list.
    ASSIGN
        clguest-list.gname       = guest.name + ", " + guest.vorname1 
                                 + " " + guest.anrede1 
                                 + guest.anredefirma
        clguest-list.zahlungsart = guest.zahlungsart
        clguest-list.bezeich     = artikel.bezeich
        clguest-list.address     = TRIM(guest.adresse1
                                 + " " + guest.adresse2 
                                 + " " + guest.wohnort)
        clguest-list.gastnr      = guest.gastnr
        clguest-list.karteityp   = guest.karteityp
        clguest-list.bemerk      = guest.bemerk
        clguest-list.kreditlimit = guest.kreditlimit
    .
END.

FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1
    AND queasy.number2 EQ 26 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN tada-flag = YES.
ELSE tada-flag = NO.

FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1
    AND queasy.number2 EQ 4 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN dept-number = INT(queasy.char2).
/*
MESSAGE tada-flag dept-number bill-number
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
IF tada-flag THEN
DO:
    FIND FIRST orderhdr WHERE orderhdr.KEY EQ 271 
    AND orderhdr.betriebsnr EQ 1 
    AND orderhdr.number1 EQ dept-number
    AND orderhdr.number3 EQ bill-number NO-LOCK NO-ERROR.
    IF AVAILABLE orderhdr THEN
    DO:
        tada-guest = ENTRY(3, orderhdr.char2, "|").
    END.

    /*MESSAGE tada-guest
        VIEW-AS ALERT-BOX INFO BUTTONS OK.*/

    FOR EACH clguest-list WHERE NOT clguest-list.gname MATCHES "*" + tada-guest + ",*":
        DELETE clguest-list.
    END.
END.
