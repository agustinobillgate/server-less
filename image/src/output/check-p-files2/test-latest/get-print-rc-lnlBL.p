
DEFINE TEMP-TABLE print-rc-list
    FIELD gastno          AS CHARACTER
    FIELD cr-usr          AS CHARACTER
    FIELD last-name       AS CHARACTER
    FIELD first-name      AS CHARACTER
    FIELD guest-title     AS CHARACTER
    FIELD room            AS CHARACTER
    FIELD room-no         AS CHARACTER
    FIELD room-price      AS CHARACTER
    FIELD arrival         AS CHARACTER
    FIELD departure       AS CHARACTER
    FIELD eta-flight      AS CHARACTER
    FIELD eta-time        AS CHARACTER
    FIELD etd-flight      AS CHARACTER
    FIELD etd-time        AS CHARACTER
    FIELD no-guest        AS CHARACTER
    FIELD purpose-stay    AS CHARACTER
    FIELD guest-address1  AS CHARACTER
    FIELD guest-address2  AS CHARACTER
    FIELD guest-address3  AS CHARACTER
    FIELD guest-country   AS CHARACTER
    FIELD guest-zip       AS CHARACTER
    FIELD guest-city      AS CHARACTER
    FIELD guest-nation    AS CHARACTER
    FIELD guest-id        AS CHARACTER
    FIELD guest-email     AS CHARACTER
    FIELD birth-date      AS CHARACTER   
    FIELD company-name    AS CHARACTER
    FIELD rsv-addr1       AS CHARACTER
    FIELD rsv-addr2       AS CHARACTER
    FIELD rsv-addr3       AS CHARACTER
    FIELD rsv-country     AS CHARACTER
    FIELD rsv-city        AS CHARACTER
    FIELD rsv-zip         AS CHARACTER
    FIELD ccard           AS CHARACTER
    FIELD mobile-no       AS CHARACTER
    FIELD bill-instruct   AS CHARACTER
    FIELD birth-place     AS CHARACTER
    FIELD expired-id      AS CHARACTER
    FIELD resnr           AS CHARACTER
    /*sis 180714*/
    FIELD province        AS CHARACTER
    FIELD phone           AS CHARACTER
    FIELD telefax         AS CHARACTER
    FIELD occupation      AS CHARACTER

    FIELD child1          AS CHARACTER
    FIELD child2          AS CHARACTER
    FIELD main-comment    AS CHARACTER
    FIELD member-comment  AS CHARACTER
    /*end sis*/

    /*wen 051216*/
    FIELD depositgef      AS CHARACTER
    FIELD depositbez      AS CHARACTER
    /*end wen*/
     /*wen 311019*/
    FIELD segment         AS CHARACTER    
.

DEFINE INPUT PARAMETER resno            AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER reslino          AS INTEGER      NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR print-rc-list.

DEFINE VARIABLE temp-zimmerwusch    AS CHAR     NO-UNDO.
DEFINE VARIABLE anz                 AS INTEGER  NO-UNDO.
DEFINE VARIABLE WI-gastnr           AS INTEGER  NO-UNDO.
DEFINE VARIABLE IND-gastnr          AS INTEGER  NO-UNDO.
DEFINE VARIABLE cc-str              AS CHAR     NO-UNDO.
DEFINE VARIABLE cc-nr               AS CHAR     INITIAL ""  NO-UNDO.
DEFINE VARIABLE ccard               AS CHAR     INITIAL ""  NO-UNDO.
DEFINE VARIABLE mm                  AS INTEGER  INITIAL 0   NO-UNDO.
DEFINE VARIABLE yy                  AS INTEGER  INITIAL 0   NO-UNDO.
DEFINE VARIABLE cc-valid            AS LOGICAL  INITIAL YES NO-UNDO.

DEFINE BUFFER rsvguest     FOR guest.

FIND FIRST res-line WHERE res-line.resnr = resno 
    AND res-line.reslinnr = reslino NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    CREATE print-rc-list.
    ASSIGN  print-rc-list.room-no        = STRING(res-line.zinr)
            print-rc-list.arrival        = STRING(res-line.ankunft, "99/99/9999") /* Malik : serverless ankunft -> res-line.ankunft */
            print-rc-list.departure      = STRING(res-line.abreise, "99/99/9999") + " " + STRING(res-line.abreisezeit,"HH:MM") /* Malik : serverless abreise -> res-line.abreise */
            print-rc-list.eta-flight     = SUBSTR(res-line.flight-nr, 1, 6)
            print-rc-list.eta-time       = SUBSTR(res-line.flight-nr,7,2) + ":" + SUBSTR(res-line.flight-nr,9,2)
            print-rc-list.etd-flight     = SUBSTR(res-line.flight-nr, 12, 6)
            print-rc-list.etd-time       = SUBSTR(res-line.flight-nr,18,2) + ":" + SUBSTR(res-line.flight-nr,20,2)
            print-rc-list.no-guest       = STRING(res-line.erwachs + res-line.gratis)
            print-rc-list.gastno         = STRING(res-line.gastnrmember)
        /*sis 180714*/
            print-rc-list.child1         = STRING(res-line.kind1)
            print-rc-list.child2         = STRING(res-line.kind2)
            print-rc-list.member-comment = STRING(res-line.bemerk).
        /*end sis*/

    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
        NO-LOCK NO-ERROR.
    IF AVAILABLE reservation AND reservation.useridanlage NE "" THEN
        cr-usr = reservation.useridanlage.

    ASSIGN
        print-rc-list.resnr         = STRING(res-line.resnr)
        print-rc-list.main-comment  = STRING(reservation.bemerk) /*sis 180714*/
        /*wen 051216*/
        print-rc-list.depositgef         = STRING(reservation.depositgef).
        print-rc-list.depositbez         = STRING(reservation.depositbez).

    /*FDL - Ticket 30467A*/
    FIND FIRST bill WHERE bill.resnr EQ resno AND bill.reslinnr EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN print-rc-list.depositgef = "0.00".
    /* FDL Comment 2BD812
    ELSE
    DO:
        FIND FIRST master WHERE master.resnr EQ resno 
            AND master.active EQ YES 
            AND master.flag EQ 0 NO-LOCK NO-ERROR.
        IF AVAILABLE master THEN print-rc-list.depositgef = "0.00".
    END.*/

    DO anz = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        temp-zimmerwusch = ENTRY(anz, res-line.zimmer-wunsch, ";").
        IF SUBSTR(temp-zimmerwusch,1,8) = "segm_pur" THEN 
        DO:
            print-rc-list.purpose-stay = SUBSTR(temp-zimmerwusch,9).
            FIND FIRST queasy WHERE queasy.KEY = 143 
                AND queasy.number1 = INTEGER(print-rc-list.purpose-stay) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy AND queasy.char3 NE "" THEN 
                print-rc-list.purpose-stay = queasy.char3.
            LEAVE.
        END.
    END.
    
    FIND FIRST queasy WHERE queasy.key = 9 AND 
        queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.char1 NE "" THEN 
        print-rc-list.bill-instruct = queasy.char1.  

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR. 
    IF AVAILABLE zimkateg THEN
        print-rc-list.room = zimkateg.kurzbez + " / " + STRING(vhp.res-line.zimmeranz). 

    /* guest detail */
    /*Dody 27/06/16 Add Keyword membership number to Print RC*/
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        ASSIGN /* print-rc-list.last-name         = guest.NAME */
                print-rc-list.first-name        = guest.vorname1 
                print-rc-list.guest-title       = guest.anrede1
                print-rc-list.guest-address1    = TRIM(guest.adresse1)
                print-rc-list.guest-address2    = TRIM(guest.adresse2)
                print-rc-list.guest-address3    = TRIM(guest.adresse3)
                print-rc-list.guest-country     = TRIM(guest.land)
                print-rc-list.guest-zip         = STRING(guest.plz)
                print-rc-list.guest-city        = TRIM(guest.wohnort)
                print-rc-list.guest-nation      = TRIM(guest.nation1)
                print-rc-list.guest-id          = TRIM(guest.ausweis-nr1)
                print-rc-list.guest-email       = TRIM(guest.email-adr)
                print-rc-list.mobile-no         = STRING(guest.mobil-telefon,"x(16)")
                print-rc-list.birth-place       = STRING(guest.telex,"x(24)")
            /*sis 180714*/
                print-rc-list.province          = STRING(guest.geburt-ort2)
                print-rc-list.phone             = STRING(guest.telefon) 
                print-rc-list.occupation        = STRING(guest.beruf).
            /*end sis*/ 

        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE reservation AND reservation.resart NE 0 THEN
        DO:
            FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart NO-LOCK NO-ERROR.
            IF AVAILABLE sourccod THEN
                print-rc-list.mobile-no = print-rc-list.mobile-no + ";" + sourccod.bezeich.
        END.
        
        /*Dody 27/06/16*/
        /* Malik Serverless */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN 
        DO:
            print-rc-list.telefax           = STRING(guest.fax) + ";" + STRING(mc-guest.cardnum).
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
            DO:
                print-rc-list.last-name         = STRING(guest.NAME) + "-" + STRING(mc-types.bezeich).
            END.
            ELSE 
            DO:
                print-rc-list.last-name         = STRING(guest.NAME).
            END. 
        END.
        ELSE 
        DO:
            print-rc-list.telefax           = STRING(guest.fax).
        END.
        /* END Malik */

        /* Uncomment for serverless
        FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN 
                print-rc-list.telefax           = STRING(guest.fax) + ";" + STRING(mc-guest.cardnum).
        ELSE    print-rc-list.telefax           = STRING(guest.fax).

        FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-types THEN 
                print-rc-list.last-name         = STRING(guest.NAME) + "-" + STRING(mc-types.bezeich).
        ELSE    print-rc-list.last-name         = STRING(guest.NAME).
        */
           
        IF guest.geburtdatum1 NE ? THEN 
            print-rc-list.birth-date            = STRING(guest.geburtdatum1,"99/99/9999").
        IF guest.geburtdatum2 NE ? THEN 
            print-rc-list.expired-id            = STRING(guest.geburtdatum2,"99/99/9999").
            
        ASSIGN  cc-str = ENTRY(1, guest.ausweis-nr2, "|")
                ccard  = ENTRY(2, cc-str, "\")
                mm     = INTEGER(SUBSTR(ENTRY(3, cc-str, "\"),1,2)) 
                yy     = INTEGER(SUBSTR(ENTRY(3, cc-str, "\"),3)) 
                cc-nr  = ccard  NO-ERROR.

        IF cc-nr = "" THEN cc-valid = NO.
        IF cc-valid THEN 
            IF yy LT YEAR(TODAY) THEN cc-valid = NO.
        IF cc-valid THEN 
            IF (yy = YEAR(TODAY) AND mm LT MONTH(TODAY)) THEN cc-valid = NO.
        IF cc-valid THEN 
        ASSIGN
        ccard = SUBSTR(ccard,1,1) 
            + FILL("X", LENGTH(ccard) - 5) 
            + SUBSTR(ccard, LENGTH(ccard) - 3)
        print-rc-list.ccard = ccard
        print-rc-list.ccard = print-rc-list.ccard
                            + ", " 
                            + SUBSTR(ENTRY(3, cc-str, "\"),1,2) 
                            + "/"
                            + SUBSTR(ENTRY(3, cc-str, "\"),3) NO-ERROR
        .
    END.

    /* reserve detail */
    FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK.
    WI-gastnr = htparam.finteger.
    FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK.
    IND-gastnr = htparam.finteger.
    FIND FIRST rsvguest WHERE rsvguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE rsvguest THEN
    DO:
        ASSIGN  print-rc-list.company-name      = STRING((rsvguest.NAME + ", " + rsvguest.anredefirma),"x(50)") /*modified by gerald 171219 BUGS 8F83FF*/
                print-rc-list.rsv-addr1         = TRIM(rsvguest.adresse1)
                print-rc-list.rsv-addr2         = TRIM(rsvguest.adresse2)
                print-rc-list.rsv-addr3         = TRIM(rsvguest.adresse3)
                print-rc-list.rsv-city          = TRIM(rsvguest.wohnort)
                print-rc-list.rsv-zip           = TRIM(rsvguest.plz)
                print-rc-list.rsv-country       = TRIM(rsvguest.land)
            .

        /*MT 181012 */
        IF (AVAILABLE rsvguest AND rsvguest.karteityp > 1) 
            AND (rsvguest.gastnr NE WI-gastnr AND rsvguest.gastnr NE IND-gastnr) THEN 
        DO:
            /*M 290512 -> from company or travel agent should not be showed
            room-price = TRIM(STRING(res-line.zipreis, ">>>,>>>,>>9.99")). */
            print-rc-list.room-price = "0.00".
        END.
        ELSE IF res-line.gastnrmember = res-line.gastnrpay
            OR rsvguest.gastnr = WI-gastnr OR rsvguest.gastnr = IND-gastnr THEN
            print-rc-list.room-price = TRIM(STRING(res-line.zipreis, ">>>,>>>,>>9.99")).
        ELSE IF rsvguest.karteityp LE 1 THEN print-rc-list.room-price = TRIM(STRING(res-line.zipreis, ">>>,>>>,>>9.99")) .
        /*MT 181012 */

        /*MT
        IF rsvguest.karteityp = 0 OR rsvguest.gastnr = WI-gastnr OR rsvguest.gastnr = IND-gastnr THEN 
            print-rc-list.room-price = TRIM(STRING(res-line.zipreis, ">>>,>>>,>>9.99")). 
        ELSE IF res-line.gastnrmember = res-line.gastnrpay THEN
            print-rc-list.room-price = TRIM(STRING(res-line.zipreis, ">>>,>>>,>>9.99")). 
        */
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN
        DO:
            print-rc-list.segment = segment.bezeich.
        END.
    END.
END.                                                     



