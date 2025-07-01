DEFINE TEMP-TABLE guest-list
    FIELD nr               AS INT
    FIELD guest-nr         AS INT
    FIELD guest-name       AS CHAR FORMAT "x(40)"
    FIELD guest-title      AS CHAR FORMAT "x(5)"
    FIELD address1         AS CHAR FORMAT "x(40)"
    FIELD address2         AS CHAR FORMAT "x(40)"
    FIELD address3         AS CHAR FORMAT "x(40)"
    FIELD city             AS CHAR FORMAT "x(20)"
    FIELD zip              AS CHAR FORMAT "x(10)"
    FIELD country          AS CHAR FORMAT "x(10)" 
    FIELD mastercomp       AS CHAR FORMAT "x(30)"
    FIELD salesid          AS CHAR FORMAT "x(10)"
    FIELD salesid-name     AS CHAR FORMAT "x(40)"
    FIELD refno2           AS CHAR FORMAT "x(10)"
    FIELD refno3           AS CHAR FORMAT "x(10)"
    FIELD phone            AS CHAR FORMAT "x(20)"
    FIELD telefax          AS CHAR FORMAT "x(20)"
    FIELD email            AS CHAR FORMAT "x(40)"
    FIELD maincontact      AS CHAR FORMAT "x(40)"
    FIELD main-fname       AS CHAR FORMAT "x(40)"
    FIELD main-tittle      AS CHAR FORMAT "x(10)"
    FIELD main-bday        AS DATE
    FIELD main-bplace      AS CHAR FORMAT "x(20)"
    FIELD main-telp        AS CHAR FORMAT "x(20)"
    FIELD main-ext         AS CHAR FORMAT "x(20)"
    FIELD main-dept        AS CHAR FORMAT "x(20)"
    FIELD main-function    AS CHAR FORMAT "x(20)"
    FIELD main-email       AS CHAR FORMAT "x(20)"
    FIELD segmentcode      AS CHAR FORMAT "x(20)"
    FIELD tot-room         AS INT
    FIELD tot-revenue      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD tot-room-revenue AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD tot-fb-revenue   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD tot-otherrevenue AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD refno4           AS CHAR FORMAT "x(20)"
    .
    

DEFINE TEMP-TABLE cust-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR     
    FIELD gesamtumsatz      LIKE guest.gesamtumsatz 
    FIELD logiernachte      LIKE guest.logiernachte 
    FIELD argtumsatz        LIKE guest.argtumsatz 
    FIELD f-b-umsatz        LIKE guest.f-b-umsatz 
    FIELD sonst-umsatz      LIKE guest.sonst-umsatz 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS DECIMAL
    FIELD ly-rev            AS DECIMAL
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS INT
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER.

DEF TEMP-TABLE usr LIKE bediener.

DEFINE INPUT PARAMETER cardtype     AS INT.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER recordcount  AS INT.
DEFINE INPUT PARAMETER crm-flag     AS LOGICAL.
DEFINE INPUT PARAMETER his-flag     AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR guest-list.

DEFINE VARIABLE sort-type   AS INTEGER NO-UNDO INITIAL 1.
DEFINE VARIABLE check-ftd   AS LOGICAL NO-UNDO INIT YES.
DEFINE VARIABLE currency    AS CHAR    INIT "Rp".
DEFINE VARIABLE excl-other  AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE curr-sort   AS INTEGER NO-UNDO EXTENT 2.
DEFINE VARIABLE nr          AS INT.

ASSIGN  
curr-sort[1] = 1
curr-sort[2] = 0
check-ftd    = YES.
currency     = "".
excl-other   = NO.
sort-type    = 1.

RUN export-topgcf-getturnoverbl.p (cardtype, sort-type, curr-sort[1], 
                       from-date, to-date,check-ftd, currency, excl-other,
                       INPUT-OUTPUT curr-sort[2], OUTPUT TABLE cust-list).

IF his-flag THEN /*only have production*/
DO:
    FOR EACH cust-list WHERE cust-list.gesamtumsatz NE 0 NO-LOCK BY cust-list.gesamtumsatz DESC:
        /*IF cust-list.cust-name MATCHES "*WALK IN GUEST*" THEN .
        ELSE IF cust-list.cust-name MATCHES "*FIT TELP*" THEN .
        ELSE
        DO:*/
            nr = nr + 1.
            CREATE guest-list.
            ASSIGN 
                guest-list.nr               = nr
                guest-list.guest-nr         = cust-list.gastnr 
                guest-list.salesid          = cust-list.sales-id
                guest-list.tot-room         = cust-list.logiernachte
                guest-list.tot-revenue      = cust-list.gesamtumsatz
                guest-list.tot-room-revenue = cust-list.argtumsatz
                guest-list.tot-fb-revenue   = cust-list.f-b-umsatz + cust-list.ba-umsatz
                guest-list.tot-otherrevenue = cust-list.sonst-umsatz
                .
            
            IF recordcount NE 0 THEN 
            DO:
                IF nr EQ recordcount THEN LEAVE.
            END.
        /*END.*/
    END.
END.
ELSE
DO:
    FOR EACH cust-list NO-LOCK BY cust-list.gesamtumsatz DESC:
        /*IF cust-list.cust-name MATCHES "*WALK IN GUEST*" THEN .
        ELSE IF cust-list.cust-name MATCHES "*FIT TELP*" THEN .
        ELSE
        DO:*/
            nr = nr + 1.
            CREATE guest-list.
            ASSIGN 
                guest-list.nr               = nr
                guest-list.guest-nr         = cust-list.gastnr 
                guest-list.salesid          = cust-list.sales-id
                guest-list.tot-room         = cust-list.logiernachte
                guest-list.tot-revenue      = cust-list.gesamtumsatz
                guest-list.tot-room-revenue = cust-list.argtumsatz
                guest-list.tot-fb-revenue   = cust-list.f-b-umsatz + cust-list.ba-umsatz
                guest-list.tot-otherrevenue = cust-list.sonst-umsatz
                .
            
            IF recordcount NE 0 THEN 
            DO:
                IF nr EQ recordcount THEN LEAVE.
            END.
        /*END.*/
    END.
    FIND FIRST guest WHERE guest.karteityp EQ cardtype NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE guest:
        FIND FIRST guest-list WHERE guest-list.guest-nr EQ guest.gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE guest-list THEN
        DO:
            nr = nr + 1.
            CREATE guest-list.
            ASSIGN 
                guest-list.nr               = nr 
                guest-list.guest-nr         = guest.gastnr 
                guest-list.salesid          = guest.phonetik3.

            IF recordcount NE 0 THEN 
            DO:
                IF nr EQ recordcount THEN LEAVE.
            END.
        END.
        FIND NEXT guest WHERE guest.karteityp EQ cardtype NO-LOCK NO-ERROR.
    END.
END.


DEFINE VARIABLE mastername AS CHAR.
DEFINE VARIABLE sales-name AS CHAR.
DEFINE VARIABLE mainsegm AS CHAR.
DEFINE BUFFER masterguest FOR guest.
FOR EACH guest-list:
    FIND FIRST guest WHERE guest.karteityp EQ cardtype AND guest.gastnr EQ guest-list.guest-nr NO-LOCK NO-ERROR.
    FIND FIRST masterguest WHERE masterguest.gastnr EQ guest.master-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE masterguest THEN mastername = masterguest.NAME + " " + masterguest.vorname1.
    
    EMPTY TEMP-TABLE usr.
    RUN read-bedienerbl.p (0, guest.phonetik3, OUTPUT TABLE usr).
    FIND FIRST usr NO-ERROR.
    IF AVAILABLE usr THEN sales-name = usr.username.

    FIND FIRST guestseg WHERE guestseg.gastnr EQ guest.gastnr AND guestseg.reihenfolge EQ 1 NO-LOCK NO-ERROR.  
    IF AVAILABLE guestseg THEN   
    DO:   
        FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.   
        IF AVAILABLE segment THEN mainsegm = ENTRY(1, segment.bezeich, "$$0").   
    END. 

    FIND FIRST akt-kont WHERE akt-kont.gastnr EQ guest.gastnr AND akt-kont.hauptkontakt EQ YES USE-INDEX kontakt-ix NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN
    DO:
        ASSIGN
            guest-list.maincontact   = akt-kont.NAME
            guest-list.main-fname    = akt-kont.vorname
            guest-list.main-tittle   = akt-kont.anrede 
            guest-list.main-bday     = akt-kont.geburtdatum1 
            guest-list.main-bplace   = akt-kont.geburt-ort1 
            guest-list.main-telp     = akt-kont.telefon 
            guest-list.main-ext      = akt-kont.durchwahl 
            guest-list.main-dept     = akt-kont.abteilung 
            guest-list.main-function = akt-kont.funktion 
            guest-list.main-email    = akt-kont.email-adr 
            .
    END.

    ASSIGN 
        guest-list.guest-name   = guest.NAME + " " + guest.vorname1
        guest-list.guest-title  = guest.anredefirma 
        guest-list.address1     = guest.adresse1 
        guest-list.address2     = guest.adresse2 
        guest-list.address3     = guest.adresse3 
        guest-list.city         = guest.wohnort 
        guest-list.zip          = guest.plz 
        guest-list.country      = guest.land 
        guest-list.mastercomp   = mastername 
        guest-list.salesid      = guest.phonetik3 
        guest-list.salesid-name = sales-name 
        guest-list.refno2       = STRING(guest.point-gastnr) 
        guest-list.refno3       = STRING(guest.steuernr) 
        guest-list.phone        = guest.telefon 
        guest-list.telefax      = guest.fax 
        guest-list.email        = guest.email-adr
        guest-list.segmentcode  = mainsegm. 
        
    mastername = "".
    sales-name = "".
    mainsegm   = "".

    FIND FIRST queasy WHERE queasy.KEY = 231 AND queasy.number1 = guest-list.guest-nr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN guest-list.refno4 = queasy.char1.
END.

IF crm-flag THEN
DO :
    FOR EACH guest-list WHERE guest-list.refno4 EQ "":
        DELETE guest-list.
    END.

    nr = 0.
    FOR EACH guest-list:
        nr = nr + 1.
        guest-list.nr = nr.
    END.
END.

