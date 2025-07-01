DEFINE TEMP-TABLE guest-list
    FIELD guest-nr      AS INT
    FIELD guest-nr2     AS INT
    FIELD guest-name    AS CHAR /*FORMAT "x(40)"*/
    FIELD guest-title   AS CHAR /*FORMAT "x(5)" */
    FIELD address1      AS CHAR /*FORMAT "x(40)"*/
    FIELD address2      AS CHAR /*FORMAT "x(40)"*/
    FIELD address3      AS CHAR /*FORMAT "x(40)"*/
    FIELD city          AS CHAR /*FORMAT "x(20)"*/
    FIELD zip           AS CHAR
    FIELD country       AS CHAR /*FORMAT "x(10)"*/ 
    FIELD mastercomp    AS CHAR /*FORMAT "x(30)"*/
    FIELD salesid       AS CHAR /*FORMAT "x(10)"*/
    FIELD salesid-name  AS CHAR /*FORMAT "x(40)"*/
    FIELD refno2        AS CHAR /*FORMAT "x(10)"*/
    FIELD refno3        AS CHAR /*FORMAT "x(10)"*/
    FIELD phone         AS CHAR
    FIELD telefax       AS CHAR
    FIELD email         AS CHAR /*FORMAT "x(40)"*/
    FIELD maincontact   AS CHAR /*FORMAT "x(40)"*/
    FIELD main-fname    AS CHAR /*FORMAT "x(40)"*/
    FIELD main-tittle   AS CHAR /*FORMAT "x(10)"*/
    FIELD main-bday     AS DATE
    FIELD main-bplace   AS CHAR /*FORMAT "x(20)"*/
    FIELD main-telp     AS CHAR /*FORMAT "x(20)"*/
    FIELD main-ext      AS CHAR /*FORMAT "x(20)"*/
    FIELD main-dept     AS CHAR /*FORMAT "x(20)"*/
    FIELD main-function AS CHAR /*FORMAT "x(20)"*/
    FIELD main-email    AS CHAR /*FORMAT "x(20)"*/
    FIELD segmentcode   AS CHAR /*FORMAT "x(20)"*/
    FIELD refno4        AS CHAR /*FORMAT "x(20)"*/
    FIELD keyaccount    AS CHAR /*FORMAT "x(30)"*/
    FIELD delflag       AS LOGICAL
    FIELD karteityp     AS INT
    .

DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER TABLE FOR guest-list.

DEFINE BUFFER t-queasy FOR queasy.
DEFINE BUFFER b-queasy FOR queasy.
DEFINE BUFFER b-akt    FOR akt-kont.
DEFINE VARIABLE curr-gastnr AS INT.
DEFINE VARIABLE nr          AS INT.
DEFINE VARIABLE kont-nr     AS INT.

RUN gcf-create.

PROCEDURE gcf-create:
    curr-gastnr = 0.
    IF curr-gastnr EQ 0 THEN
    DO:
        FIND LAST guest WHERE guest.gastnr NE ? NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN 
            curr-gastnr = guest.gastnr + 1.
        ELSE 
            curr-gastnr = 1.
    END.
    
    FOR EACH guest-list WHERE guest-list.guest-nr EQ 0 NO-LOCK:
        CREATE guest.
        ASSIGN
            guest.gastnr        = curr-gastnr
            guest.karteityp     = guest-list.karteityp
            guest.name          = guest-list.guest-name
            guest.anredefirma   = guest-list.guest-title
            guest.adresse1      = guest-list.address1    
            guest.adresse2      = guest-list.address2
            guest.adresse3      = guest-list.address3
            guest.wohnort       = guest-list.city
            guest.plz           = ENTRY(1,guest-list.zip,".")
            guest.land          = guest-list.country
            guest.phonetik3     = ENTRY(1,guest-list.salesid,".")
            guest.point-gastnr  = INTEGER(guest-list.refno2)
            guest.steuernr      = guest-list.refno3
            guest.telefon       = ENTRY(1,guest-list.phone,".")  
            guest.fax           = ENTRY(1,guest-list.telefax,".")
            guest.email-adr     = guest-list.email  
            .

        IF guest-list.maincontact NE "" THEN
        DO:
            kont-nr = 0.
            FOR EACH b-akt WHERE b-akt.gastnr EQ curr-gastnr NO-LOCK:
                IF b-akt.kontakt-nr GT kont-nr THEN kont-nr = b-akt.kontakt-nr.
            END.
            FIND FIRST akt-kont WHERE akt-kont.gastnr EQ curr-gastnr AND akt-kont.hauptkontakt EQ YES USE-INDEX kontakt-ix NO-LOCK NO-ERROR.
            IF NOT AVAILABLE akt-kont THEN
            DO:
                kont-nr = kont-nr + 1.
                CREATE akt-kont.
                ASSIGN
                    akt-kont.gastnr         = curr-gastnr
                    akt-kont.NAME           = guest-list.maincontact  
                    akt-kont.vorname        = guest-list.main-fname   
                    akt-kont.anrede         = guest-list.main-tittle  
                    akt-kont.geburtdatum1   = guest-list.main-bday    
                    akt-kont.geburt-ort1    = guest-list.main-bplace  
                    akt-kont.telefon        = ENTRY(1,guest-list.main-telp,".")    
                    akt-kont.durchwahl      = guest-list.main-ext     
                    akt-kont.abteilung      = guest-list.main-dept    
                    akt-kont.funktion       = guest-list.main-function
                    akt-kont.email-adr      = guest-list.main-email
                    akt-kont.hauptkontakt   = YES
                    akt-kont.kontakt-nr     = kont-nr
                    akt-kont.kategorie      = 1.
            END.
            ELSE
            DO:
                kont-nr = kont-nr + 1.
                CREATE akt-kont.
                ASSIGN
                    akt-kont.gastnr         = curr-gastnr
                    akt-kont.NAME           = guest-list.maincontact  
                    akt-kont.vorname        = guest-list.main-fname   
                    akt-kont.anrede         = guest-list.main-tittle  
                    akt-kont.geburtdatum1   = guest-list.main-bday    
                    akt-kont.geburt-ort1    = guest-list.main-bplace  
                    akt-kont.telefon        = ENTRY(1,guest-list.main-telp,".")    
                    akt-kont.durchwahl      = guest-list.main-ext     
                    akt-kont.abteilung      = guest-list.main-dept    
                    akt-kont.funktion       = guest-list.main-function
                    akt-kont.email-adr      = guest-list.main-email
                    akt-kont.hauptkontakt   = YES
                    akt-kont.kontakt-nr     = kont-nr
                    akt-kont.kategorie      = 1.
            END.
        END.

        IF guest-list.segmentcode NE "" THEN
        DO:
            FIND FIRST segment WHERE ENTRY(1, segment.bezeich, "$$0") EQ guest-list.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN
            DO:
                FIND FIRST guestseg WHERE guestseg.gastnr EQ curr-gastnr 
                    AND guestseg.reihenfolge EQ 1 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE guestseg THEN
                DO:
                    CREATE guestseg.
                    ASSIGN
                        guestseg.gastnr       = curr-gastnr
                        guestseg.reihenfolge  = 1
                        guestseg.segmentcode  = segment.segmentcode.
                END.
            END.
        END.

        IF guest-list.salesid NE "" THEN 
        DO: 
            FIND FIRST htparam WHERE paramnr = 1002 NO-LOCK. 
            IF htparam.flogical THEN 
            DO: 
                FIND FIRST akt-cust WHERE akt-cust.gastnr = curr-gastnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE akt-cust THEN
                DO:
                    CREATE akt-cust. 
                    ASSIGN 
                        akt-cust.gastnr   = curr-gastnr
                        akt-cust.c-init   = user-init 
                        akt-cust.userinit = guest-list.salesid
                    .
                END.
                ELSE
                DO:
                    IF akt-cust.userinit = guest-list.salesid THEN .
                    ELSE
                    DO:
                        FIND CURRENT akt-cust EXCLUSIVE-LOCK.
                        ASSIGN
                            akt-cust.c-init   = user-init 
                            akt-cust.userinit = guest-list.salesid
                        .
                        FIND CURRENT akt-cust NO-LOCK.
                    END.
                END.
            END.
        END.
        ELSE 
        DO: 
            FIND FIRST akt-cust WHERE akt-cust.gastnr = curr-gastnr 
                AND akt-cust.userinit = guest-list.salesid EXCLUSIVE-LOCK NO-ERROR. 
            IF AVAILABLE akt-cust THEN 
            DO: 
                DELETE akt-cust. 
                RELEASE akt-cust. 
            END. 
        END.

        IF guest-list.refno4 NE "" THEN DO:
            FIND FIRST queasy WHERE queasy.KEY = 231
                AND queasy.number1 = curr-gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN DO:
                ASSIGN queasy.char1 = guest-list.refno4.
            END.
            ELSE DO:
                CREATE queasy.
                ASSIGN queasy.KEY     = 231
                       queasy.number1 = curr-gastnr
                       queasy.char1   = guest-list.refno4.
            END.
        END.

        IF guest-list.keyaccount NE "" THEN 
        DO:
            FIND FIRST b-queasy WHERE b-queasy.KEY EQ 211 AND b-queasy.char1 EQ guest-list.keyaccount NO-LOCK NO-ERROR.
            IF AVAILABLE b-queasy THEN
            DO:
                FOR EACH t-queasy WHERE t-queasy.KEY EQ 212 AND t-queasy.number1 EQ b-queasy.number1 BY t-queasy.number2 DESC:
                    nr = t-queasy.number2 + 1.
                    LEAVE.
                END.

                FIND FIRST t-queasy WHERE t-queasy.KEY EQ 212 AND t-queasy.number3 EQ curr-gastnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE t-queasy THEN
                DO:
                    CREATE t-queasy.
                    ASSIGN
                        t-queasy.KEY        = 212
                        t-queasy.number1    = b-queasy.number1
                        t-queasy.number2    = nr
                        t-queasy.char1      = guest-list.guest-name
                        t-queasy.number3    = curr-gastnr
                        .
                END.
            END.
        END.

        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
        CREATE res-history. 
        ASSIGN 
            res-history.nr = bediener.nr 
            res-history.datum = TODAY 
            res-history.zeit = TIME 
            res-history.aenderung = "Create GuestCard: GastNo " + STRING(curr-gastnr) 
              + " " + guest-list.guest-name
            res-history.action = "GuestFile". 
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history.

        curr-gastnr = curr-gastnr + 1.
    END.
END. 
