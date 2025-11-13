DEFINE TEMP-TABLE res-info
    FIELD res-time      AS CHARACTER
    FIELD res-id        AS CHARACTER
    FIELD ota-code      AS CHARACTER
    FIELD commission    AS CHARACTER
    FIELD curr          AS CHARACTER
    FIELD adult         AS CHARACTER
    FIELD child1        AS CHARACTER
    FIELD child2        AS CHARACTER
    FIELD remark        AS CHARACTER
    FIELD eta           AS CHARACTER
    FIELD given-name    AS CHARACTER
    FIELD sure-name     AS CHARACTER
    FIELD phone         AS CHARACTER
    FIELD email         AS CHARACTER
    FIELD address1      AS CHARACTER
    FIELD address2      AS CHARACTER
    FIELD city          AS CHARACTER
    FIELD zip           AS CHARACTER
    FIELD state         AS CHARACTER
    FIELD country       AS CHARACTER
    FIELD uniq-id       AS CHARACTER
    FIELD res-status    AS CHARACTER /*Jason 29/07/16*/
    FIELD deposit       AS DECIMAL
    FIELD membership    AS CHARACTER /* membershipProgramName-membershipID */
    FIELD card-info     AS CHARACTER
    FIELD gastnrmember  AS INTEGER
    .

DEFINE TEMP-TABLE room-avail-list 
    FIELD zikatnr     AS INTEGER 
    FIELD i-typ       AS INTEGER
    FIELD sleeping    AS LOGICAL INITIAL YES 
    FIELD allotment   AS INTEGER
    FIELD bezeich     AS CHAR FORMAT "x(19)" FONT 1 
    FIELD room        AS INTEGER
    FIELD troom       AS INTEGER
    FIELD datum       AS DATE
. 

DEFINE TEMP-TABLE service-list
    FIELD ci-date           AS CHARACTER
    FIELD co-date           AS CHARACTER
    FIELD res-id            AS CHARACTER
    FIELD amountaftertax    AS DECIMAL
    FIELD amountbeforetax   AS DECIMAL
    FIELD tamountaftertax   AS DECIMAL
    FIELD tamountbeforetax  AS DECIMAL
    FIELD bezeich           AS CHARACTER
    FIELD rph               AS CHARACTER
    FIELD id                AS CHARACTER
    FIELD curr              AS CHARACTER
    FIELD qty               AS INTEGER.
    
DEFINE TEMP-TABLE room-list
    FIELD reslinnr  AS INTEGER
    FIELD res-id    AS CHARACTER
    FIELD ci-date   AS CHARACTER
    FIELD co-date   AS CHARACTER
    FIELD amount    AS CHARACTER
    FIELD room-type AS CHARACTER
    FIELD rate-code AS CHARACTER
    FIELD number    AS INTEGER
    FIELD adult     AS INTEGER
    FIELD child1    AS INTEGER
    FIELD child2    AS INTEGER
    FIELD service   AS CHARACTER
    FIELD gastnr    AS CHARACTER
    FIELD comment   AS CHARACTER
    FIELD argtnr    AS CHARACTER
    FIELD ankunft   AS DATE
    FIELD abreise   AS DATE
    FIELD zikatnr   AS INTEGER.

DEFINE TEMP-TABLE guest-list
    FIELD res-id        AS CHARACTER
    FIELD given-name    AS CHARACTER
    FIELD sure-name     AS CHARACTER
    FIELD phone         AS CHARACTER
    FIELD email         AS CHARACTER
    FIELD address1      AS CHARACTER
    FIELD address2      AS CHARACTER
    FIELD city          AS CHARACTER
    FIELD zip           AS CHARACTER
    FIELD state         AS CHARACTER
    FIELD country       AS CHARACTER
    FIELD gastnr        AS CHARACTER
    FIELD gastnrmember  AS INTEGER.


DEFINE TEMP-TABLE nation-list
    FIELD nat-nr        AS INT
    FIELD nat-abbr      AS CHAR
    FIELD nat-desc      AS CHAR
.

DEFINE INPUT  PARAMETER TABLE FOR res-info.
DEFINE INPUT  PARAMETER TABLE FOR room-list.    
DEFINE INPUT  PARAMETER TABLE FOR service-list.
DEFINE INPUT  PARAMETER TABLE FOR guest-list.
DEFINE INPUT  PARAMETER res-mode        AS CHAR     NO-UNDO. /* "New" or "Insert" */
DEFINE INPUT  PARAMETER dyna-code       AS CHARACT  NO-UNDO.
DEFINE INPUT  PARAMETER beCode          AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER new-resno       AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter     AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter1    AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter2    AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter3    AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER t-guest-nat     AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER t-curr-name     AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER error-str       AS CHARACTER    INITIAL "".
DEFINE OUTPUT PARAMETER done            AS LOGICAL      INITIAL NO.

/* BLY - Adding Variable Room-OCC */
DEFINE VARIABLE room-occ AS INT INITIAL 0.

/*M dummy information for testing
DEFINE VARIABLE hWebService             AS HANDLE NO-UNDO.
DEFINE VARIABLE hServiceType            AS HANDLE NO-UNDO.

DEFINE VARIABLE hXdoc                   AS HANDLE.
DEFINE VARIABLE hXnoderef1              AS HANDLE.
DEFINE VARIABLE hXnoderef2              AS HANDLE.
DEFINE VARIABLE hXnoderef3              AS HANDLE.
DEFINE VARIABLE hXtext                  AS HANDLE.
DEFINE VARIABLE g_header                AS HANDLE.

DEFINE VARIABLE get-value               AS LOGICAL  INITIAL NO NO-UNDO.
DEFINE NEW SHARED VARIABLE curr-map     AS CHARACTER NO-UNDO.
DEFINE NEW SHARED VARIABLE cou-map      AS CHARACTER NO-UNDO.
DEFINE NEW SHARED VARIABLE chDelimeter1 AS CHAR NO-UNDO.
DEFINE NEW SHARED VARIABLE chDelimeter2 AS CHAR NO-UNDO.
DEFINE NEW SHARED VARIABLE chDelimeter3 AS CHAR NO-UNDO.

DEFINE VARIABLE error-str   AS CHARACTER    INITIAL "".
DEFINE VARIABLE done        AS LOGICAL      INITIAL NO.
DEF VAR err AS LOGICAL.

FOR EACH res-info :
    DELETE res-info.
END.
CREATE res-info.
ASSIGN  res-time = "2011-12-06T18:33:31"
     res-id   = "BDN-731290141"
     ota-code = "BDC"
     commission = "0"
     no-room  =  1
     rate-code = "DR11"
     room-type = "HR"
     ci-date   = 12/23/11
     co-date   = 12/24/11
     night     = 1
     amount    = "55.27;"
     curr      = "USD"
     adult     = "2"
     child1    = ""
     child2    = ""
     remark    = "Smoking: NO, Floor: High, Customer Request: EXTENSION OF STAY ROOM 350. I already stay at the hotel right now"
     eta       = "18:00:00"
     given-name = "Margareta"
     sure-name  = "Dwiyanti"
     phone      = "+628999957961"
     email      = "margareta@sindata.net"
     address1   = "jalan jalan"
     address2   = ""
     city       = "Jakarta"
     zip        = "10610"
     state      = ""
     country    = "Indonesia".
*/

/******************* DEFINE WIDGETS ****************************/
DEFINE VARIABLE curr-date       AS DATE     NO-UNDO INITIAL ?.
DEFINE VARIABLE exist           AS LOGICAL  NO-UNDO INITIAL NO.
DEFINE VARIABLE curr-error-str  AS CHARACTER.

DEFINE VARIABLE cm-gastno       AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE cm-name         AS CHAR     NO-UNDO.
DEFINE VARIABLE inp-resno       AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE ota-gastnr      AS INTEGER  NO-UNDO.
DEFINE VARIABLE rsegcode        AS INTEGER  NO-UNDO.
DEFINE VARIABLE resart          AS INTEGER  NO-UNDO.
DEFINE VARIABLE gastnrmember    AS INTEGER  NO-UNDO INITIAL 1.
DEFINE VARIABLE rsegm           AS INTEGER  NO-UNDO.
DEFINE VARIABLE resstatus       AS INTEGER  NO-UNDO INITIAL 1.
DEFINE VARIABLE i               AS INTEGER  NO-UNDO INITIAL 1.

DEFINE VARIABLE markno          AS INTEGER  NO-UNDO.
DEFINE VARIABLE argtno          AS INTEGER  NO-UNDO.
DEFINE VARIABLE zikatno         AS INTEGER  NO-UNDO.
DEFINE VARIABLE currno          AS INTEGER  NO-UNDO.
DEFINE VARIABLE rm-qty          AS INTEGER  NO-UNDO.

DEFINE VARIABLE rmtype          AS CHAR     NO-UNDO.
DEFINE VARIABLE card-name       AS CHAR     NO-UNDO.
DEFINE VARIABLE card-no         AS CHAR     NO-UNDO.
DEFINE VARIABLE argt            AS CHAR     NO-UNDO.
DEFINE VARIABLE ratecode1       AS CHAR     NO-UNDO INITIAL "".
DEFINE VARIABLE guest-nat       AS CHAR     NO-UNDO INITIAL "".
DEFINE VARIABLE eta-char        AS CHAR     NO-UNDO.
DEFINE VARIABLE hh              AS CHAR     NO-UNDO.
DEFINE VARIABLE mm              AS CHAR     NO-UNDO.

DEFINE VARIABLE bookingID       AS CHAR     NO-UNDO INIT "".
DEFINE VARIABLE avail-gdpr      AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE curr-nat        AS CHAR     NO-UNDO INIT "".
DEFINE VARIABLE do-it           AS LOGICAL  NO-UNDO INIT NO.

DEFINE VARIABLE card-exist      AS LOGICAL  NO-UNDO INITIAL NO.
DEFINE VARIABLE new-contrate    AS LOGICAL  NO-UNDO.
DEFINE VARIABLE restricted-disc AS LOGICAL  NO-UNDO INITIAL NO.
DEFINE VARIABLE use-it          AS LOGICAL  NO-UNDO INITIAL NO.

DEFINE VARIABLE ci-rate         AS DECIMAL  NO-UNDO INITIAL 0.
DEFINE VARIABLE ci-rate1        AS DECIMAL  NO-UNDO INITIAL 0.
DEFINE VARIABLE room-price      AS DECIMAL  NO-UNDO.

DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE city-str        AS CHARACTER.
DEFINE VARIABLE loop-i          AS INTEGER. 
DEFINE VARIABLE curr-j          AS INTEGER.

DEFINE VARIABLE c-number AS CHARACTER.
DEFINE VARIABLE c-code   AS CHARACTER.
DEFINE VARIABLE c-exp    AS CHARACTER.
DEFINE VARIABLE c-info   AS CHARACTER.

DEFINE VARIABLE globekey-rsv        AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE globekey-tot-amount AS DECIMAL.
DEFINE VARIABLE tot-rmrate-VHP      AS DECIMAL.
DEFINE VARIABLE asc-str             AS CHAR.

DEFINE BUFFER rgast     FOR guest.
DEFINE BUFFER bguest    FOR guest.
DEFINE BUFFER bratecode FOR ratecode.     
DEFINE BUFFER nationbuf FOR nation.
DEFINE BUFFER qsy6      FOR queasy.
DEFINE BUFFER qsy       FOR queasy.
DEFINE BUFFER rqueasy   FOR queasy.
DEFINE BUFFER bqueasy   FOR queasy.
DEFINE BUFFER gseg      FOR guestseg.
DEFINE BUFFER bres      FOR reservation. /* NC-#43398F 22/11/24 */
DEFINE BUFFER bres-line FOR res-line. /* NC-#43398F 22/11/24 */

DEFINE VARIABLE str-date AS CHAR.
DEFINE VARIABLE m        AS INT.
DEFINE VARIABLE yy       AS INT.
DEFINE VARIABLE dd       AS INT.
DEFINE VARIABLE n        AS INT INIT 0.

DEFINE VARIABLE tmp-given-name AS CHAR.
DEFINE VARIABLE tmp-email AS CHAR.
DEFINE VARIABLE tmp-sure-name AS CHAR.
DEFINE VARIABLE tmp-adress1 AS CHAR.
DEFINE VARIABLE tmp-adress2 AS CHAR.
DEFINE VARIABLE tmp-country AS CHAR.
DEFINE VARIABLE tmp-phone AS CHAR.
DEFINE VARIABLE tmp-city AS CHAR.
DEFINE VARIABLE tmp-zip AS CHAR.

DEFINE VARIABLE tgastnrmember AS INT.
DEFINE VARIABLE tot-guest AS INT INIT 1.
DEFINE VARIABLE curri AS INT.
DEFINE VARIABLE ota-name AS CHAR. /*NC - 15/12/24 */
DEFINE VARIABLE ota-seg AS INT. /*NC - 15/12/24 */

DEFINE VARIABLE avalue      AS CHARACTER INIT "" NO-UNDO.
DEFINE VARIABLE p           AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE tahun       AS DATE FORMAT "99/99/9999" INITIAL TODAY NO-UNDO.
DEFINE VARIABLE service-dept  AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE service-artnr AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE tax-included  AS LOGICAL INITIAL NO NO-UNDO.
DEFINE VARIABLE double-currency AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE foreign-rate    AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE ratecode-frate  AS DECIMAL INIT 1 NO-UNDO.
DEFINE VARIABLE sm-frate        AS DECIMAL INIT 1 NO-UNDO.
/*NC - 21/06/22*/
DEFINE VARIABLE bill-date       AS DATE         NO-UNDO.
DEFINE VARIABLE upto-date       AS DATE         NO-UNDO.
DEFINE VARIABLE zikatnr AS INTEGER.

/*NC - 21/09/22 */
DEF VAR commission-str AS CHAR      NO-UNDO INIT "".    
DEF VAR commission-dec AS DECIMAL   NO-UNDO INIT 0.
DEF VAR dcommission    AS LOGICAL  NO-UNDO INITIAL NO. /*price OTA included commission or not*/
DEF VAR markup-str AS CHAR      NO-UNDO INIT "".    
DEF VAR markup-dec AS DECIMAL   NO-UNDO INIT 0.
DEF VAR artnr-comm	AS INTEGER   NO-UNDO INIT 0. /*artnr commission*/

/*RVN - 30-10-2024 - 0783E2*/
DEF VAR default-country AS CHAR NO-UNDO INIT "".
/**************************************************************************/
FIND FIRST queasy WHERE queasy.KEY = 159 AND queasy.number1 = beCode NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
    ASSIGN
        cm-gastno = queasy.number2
        cm-name   = queasy.char1.
    
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
curr-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 67 NO-LOCK.
rsegcode = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 69 NO-LOCK.
resart   = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 30 NO-LOCK NO-ERROR.
service-artnr = htparam.finteger.
service-dept = 0.

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK.
tax-included = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 953 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN 
DO:
    IF htparam.flogical = YES AND NOT htparam.bezeichnung = "Not Used" THEN 
        resstatus = 5.
    ELSE
        resstatus = 1.
END.

/* CHIRAG 20DEC2018 FOR GDPR */
FIND FIRST htparam WHERE paramnr = 346 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN avail-gdpr = htparam.flogical.

IF avail-gdpr THEN
DO:
    FOR EACH nationbuf WHERE nationbuf.natcode = 0 NO-LOCK,
        FIRST qsy6 WHERE qsy6.KEY = 6 AND qsy6.number1 = nationbuf.untergruppe
            AND qsy6.char1 MATCHES "*europe*" NO-LOCK BY nationbuf.kurzbez:
        CREATE nation-list.
        ASSIGN 
            nation-list.nat-nr              = nationbuf.nationnr
            nation-list.nat-abbr            = nationbuf.kurzbez
            nation-list.nat-desc            = ENTRY(1, nationbuf.bezeich, ";").
    END.
END.

FIND FIRST res-info /*EXCLUSIVE-LOCK*/ NO-ERROR.
IF AVAILABLE res-info THEN
DO:
/*     FIND FIRST guest WHERE TRIM(ENTRY(1, guest.steuernr, "-")) 
        MATCHES TRIM(res-info.ota-code) NO-LOCK NO-ERROR.
    IF AVAILABLE guest AND NUM-ENTRIES(guest.steuernr, "-") EQ 2 THEN
        res-info.commission = ENTRY(2, guest.steuernr, "-").
    ELSE res-info.commission = "0". */

    RUN chk-ascii(res-info.sure-name, OUTPUT asc-str).
    res-info.sure-name = asc-str.
    asc-str = "".

    RUN chk-ascii(res-info.city, OUTPUT asc-str).
    res-info.city = asc-str.
    asc-str = "".

    RUN chk-ascii(res-info.given-name, OUTPUT asc-str).
    res-info.given-name = asc-str.
    asc-str = "".

    RUN chk-ascii(res-info.address1, OUTPUT asc-str).
    res-info.address1 = asc-str.
    asc-str = "".

    RUN chk-ascii(res-info.address2, OUTPUT asc-str).
    res-info.address2 = asc-str.
    asc-str = "".

    RUN chk-ascii(res-info.city, OUTPUT asc-str).
    res-info.city = asc-str.
    asc-str = "".
    
    RUN chk-ascii(res-info.remark, OUTPUT asc-str).
    res-info.remark = asc-str.
    asc-str = "".

    RUN chk-ascii(res-info.email, OUTPUT asc-str).
    res-info.email = asc-str.
    asc-str = "".
    
    FIND CURRENT res-info NO-LOCK.
END.

FOR EACH guest-list:
    RUN chk-ascii(guest-list.sure-name, OUTPUT asc-str).
    guest-list.sure-name = asc-str.
    asc-str = "".

    RUN chk-ascii(guest-list.city, OUTPUT asc-str).
    res-info.city = asc-str.
    asc-str = "".

    RUN chk-ascii(guest-list.given-name, OUTPUT asc-str).
    guest-list.given-name = asc-str.
    asc-str = "".

    RUN chk-ascii(guest-list.address1, OUTPUT asc-str).
    guest-list.address1 = asc-str.
    asc-str = "".

    RUN chk-ascii(guest-list.address2, OUTPUT asc-str).
    guest-list.address2 = asc-str.
    asc-str = "".

    RUN chk-ascii(guest-list.city, OUTPUT asc-str).
    guest-list.city = asc-str.
    asc-str = "".
    
    RUN chk-ascii(guest-list.email, OUTPUT asc-str).
    guest-list.email = asc-str.
    asc-str = "".
END.

FIND FIRST res-info NO-LOCK NO-ERROR.
IF AVAILABLE res-info THEN
DO: 
    FIND FIRST rgast WHERE TRIM(ENTRY(1, rgast.steuernr, "|")) EQ TRIM(res-info.ota-code) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE rgast THEN 
    DO:                                               
        error-str = error-str + "Reservation TA File not found for : " + TRIM(res-info.ota-code) + ". ".
        FIND FIRST rgast WHERE rgast.gastnr = cm-gastno NO-LOCK NO-ERROR.
        IF AVAILABLE rgast THEN ota-gastnr = rgast.gastnr.
    END.
    ELSE ota-gastnr = rgast.gastnr. 
	ASSIGN
		bookingID = res-info.res-id
		ota-name = rgast.name /*NC- 15/12/24*/
		ota-seg = rgast.segment3 /*NC- 15/12/24*/
	.
	IF TRIM(res-info.ota-code) EQ "SERVR" THEN resstatus = 5. /**/
	FIND FIRST guest WHERE guest.gastnr = ota-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
	/*NC - 21/09/22 added for OTA commission stored in VHP as arrangement - ticket req no DDD8E4*/
      IF NUM-ENTRIES(guest.steuernr, "|") GT 5 THEN /*if ABI exist*/
      DO:
			IF ENTRY(2, guest.steuernr, "|") NE "" OR ENTRY(2, guest.steuernr, "|") NE ? THEN
			ASSIGN
			commission-str = ENTRY(2, guest.steuernr, "|")
			commission-str = REPLACE(commission-str, "-", "")
			commission-str = REPLACE(commission-str, "%", "")
			commission-str = REPLACE(commission-str, ",", ".")
			commission-dec = DECIMAL(commission-str)
			.
			IF ENTRY(7, guest.steuernr, "|") NE "" OR ENTRY(7, guest.steuernr, "|") NE ? THEN
			ASSIGN
			markup-str = ENTRY(7, guest.steuernr, "|")
			markup-str = REPLACE(commission-str, "-", "")
			markup-str = REPLACE(commission-str, "%", "")
			markup-str = REPLACE(commission-str, ",", ".")
			markup-dec = DECIMAL(commission-str)
			.
			IF ENTRY(8, guest.steuernr, "|") NE "" OR ENTRY(8, guest.steuernr, "|") NE ? THEN
			dcommission = LOGICAL(ENTRY(8, guest.steuernr, "|")).
			IF ENTRY(9, guest.steuernr, "|") NE "" OR ENTRY(9, guest.steuernr, "|") NE ? THEN 
			artnr-comm = INTEGER(ENTRY(9, guest.steuernr, "|")).
			
	  END.
	  ELSE IF NUM-ENTRIES(guest.steuernr, "|") EQ 5 THEN
	  DO:
			IF ENTRY(2, guest.steuernr, "|") NE "" OR ENTRY(2, guest.steuernr, "|") NE ? THEN
			ASSIGN
			commission-str = ENTRY(2, guest.steuernr, "|")
			commission-str = REPLACE(commission-str, "-", "")
			commission-str = REPLACE(commission-str, "%", "")
			commission-str = REPLACE(commission-str, ",", ".")
			commission-dec = DECIMAL(commission-str).
			
			IF ENTRY(3, guest.steuernr, "|") NE "" OR ENTRY(3, guest.steuernr, "|") NE ? THEN
			ASSIGN
			markup-str = ENTRY(3, guest.steuernr, "|")
			markup-str = REPLACE(commission-str, "-", "")
			markup-str = REPLACE(commission-str, "%", "")
			markup-str = REPLACE(commission-str, ",", ".")
			markup-dec = DECIMAL(commission-str).
			
			IF ENTRY(4, guest.steuernr, "|") NE "" OR ENTRY(4, guest.steuernr, "|") NE ? THEN
			dcommission = LOGICAL(ENTRY(4, guest.steuernr, "|")).
			IF ENTRY(5, guest.steuernr, "|") NE "" OR ENTRY(5, guest.steuernr, "|") NE ? THEN 
				artnr-comm = INTEGER(ENTRY(5, guest.steuernr, "|")).
	  END.

   END.
/*DO TRANSACTION:*/ /*NC - sometime make reservation double 144F81*/     
    IF res-mode = "new" THEN
    DO:
        FOR EACH room-list:
			/*NC-21/06/22*/
			FIND FIRST rqueasy WHERE rqueasy.KEY = 2 AND rqueasy.char1 = room-list.rate-code 
            NO-LOCK NO-ERROR.
			IF NOT AVAILABLE rqueasy THEN room-list.rate-code = dyna-code.
			
            FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.char1 = room-list.room-type NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                FIND FIRST zimkateg WHERE zimkateg.kurzbez = room-list.room-type NO-LOCK NO-ERROR.
                IF NOT AVAILABLE zimkateg THEN
                DO: 
                    error-str = error-str + CHR(10) + room-list.room-type  + "No such Room Category".
                    RETURN.
                END.
            END.
        END.

        /*FIND FIRST reservation WHERE reservation.vesrdepot = bookingID AND reservation.gastnr = ota-gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
            FIND FIRST res-line WHERE res-line.gastnr = ota-gastnr AND
                res-line.zimmer-wunsch MATCHES "*voucher" + bookingID + "*" NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN
            DO:
                ASSIGN error-str = error-str + CHR(10) + "Reservation " + res-info.res-id + " already exist.".
                ASSIGN
                    exist = YES
                    done = YES.
                RETURN.
            END.
        END.
        IF exist THEN RETURN. */
		 /* hotel fourteen roses, akomodir kasus setelah cancel ada modify yang harus masuk sebagai new reservation (CRG 21/09/2023) */
        FIND FIRST reservation WHERE reservation.vesrdepot = bookingID 
            AND reservation.gastnr = ota-gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE reservation THEN
        DO:
            FIND FIRST res-line WHERE res-line.gastnr = ota-gastnr AND
                /* res-line.ankunft = res-info.ci-date AND  */
                res-line.zimmer-wunsch MATCHES "*voucher" + bookingID + "*"
                AND NOT res-line.resstatus = 9
                NO-LOCK NO-ERROR.
        END.
        IF AVAILABLE res-line OR AVAILABLE reservation THEN
        DO:        
            ASSIGN error-str = error-str + CHR(10) + "Reservation " + res-info.uniq-id + " already exist.".
            ASSIGN
                exist = YES
                done = YES.
            FIND FIRST room-list WHERE room-list.res-id EQ bookingID NO-LOCK NO-ERROR.
			IF room-list.ankunft = room-list.abreise THEN upto-date = room-list.abreise.
			ELSE upto-date = room-list.abreise - 1.
			DO bill-date = room-list.ankunft TO upto-date :
				FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.char1 = room-list.room-type NO-LOCK NO-ERROR.
				IF AVAILABLE queasy THEN
				DO:
					zikatnr = queasy.number1.
				END.
				ELSE
				DO:
					FIND FIRST zimkateg WHERE zimkateg.kurzbez = room-list.room-type NO-LOCK NO-ERROR.
					IF AVAILABLE zimkateg THEN 
						ASSIGN
							zikatnr = zimkateg.zikatnr.
				END.
				
				FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
				  AND qsy.number1 = zikatnr AND qsy.char1 = room-list.rate-code NO-LOCK NO-ERROR.
				IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
				DO:
					FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) NO-LOCK NO-ERROR.
					IF AVAILABLE bqueasy THEN
					DO:
						FIND CURRENT bqueasy EXCLUSIVE-LOCK.
						bqueasy.logi2 = YES.
						FIND CURRENT bqueasy NO-LOCK.
						RELEASE bqueasy.
					END.
				END.
				FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
				  AND qsy.number1 = zikatnr AND qsy.char1 = "" NO-LOCK NO-ERROR.
				IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
				DO:
					FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) NO-LOCK NO-ERROR.
					IF AVAILABLE bqueasy THEN
					DO:
						FIND CURRENT bqueasy EXCLUSIVE-LOCK.
						bqueasy.logi2 = YES.
						FIND CURRENT bqueasy NO-LOCK.
						RELEASE bqueasy.
					END.
				END.
			END.
			IF exist THEN RETURN.
        END.
    END.
/*END.*/

    RELEASE guest.
    /*DO TRANSACTION: */ /*NC - sometime make reservation double 144F81*/      
        IF res-info.card-info NE "" THEN
        DO:            
            DO i = 1 TO NUM-ENTRIES(res-info.card-info,";"):
                c-info = ENTRY(i,res-info.card-info,";").
                IF c-info NE "" AND NUM-ENTRIES(c-info,":") GT 1 THEN
                DO:
                    IF ENTRY(1,c-info,":") = "number" THEN
                        c-number = ENTRY(2,c-info,":").
                    ELSE IF ENTRY(1,c-info,":") = "exp" THEN
                        c-exp = ENTRY(2,c-info,":").
                    ELSE IF ENTRY(1,c-info,":") = "code" THEN
                        c-code = ENTRY(2,c-info,":").
                END.
            END.
            IF c-number NE "" THEN
            DO:                
                IF c-code = "VI" THEN
                    FIND FIRST artikel WHERE artikel.artart = 7 AND artikel.bezeich MATCHES "*visa*" NO-LOCK NO-ERROR.
                ELSE IF c-code = "MC" THEN
                    FIND FIRST artikel WHERE artikel.artart = 7 AND artikel.bezeich MATCHES "*master*" NO-LOCK NO-ERROR. 
                ELSE IF c-code = "AX" THEN
                    FIND FIRST artikel WHERE artikel.artart = 7 AND artikel.bezeich MATCHES "*american*" NO-LOCK NO-ERROR. 
                ELSE IF c-code = "JC" THEN
                    FIND FIRST artikel WHERE artikel.artart = 7 AND artikel.bezeich MATCHES "*japanese*" NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE artikel THEN
                    FIND FIRST artikel WHERE artikel.artart = 7 NO-LOCK NO-ERROR.
                
                IF c-exp NE "" THEN
                    c-exp = SUBSTR(c-exp,1,2) + "20" + SUBSTR(c-exp,3,2).                  
            END.
        END.

        /*guest reserve*/
        DO: 
            IF NOT NUM-ENTRIES(res-info.email,"@") = 2 THEN            
                res-info.email = "".
            ELSE
                IF NOT LENGTH(ENTRY(1,res-info.email,"@")) GE 2
                    AND NOT LENGTH(ENTRY(2,res-info.email,"@")) GE 2 THEN
                    res-info.email = "".      
			/* NC - 10/01/23 request Pak Stephen */
			res-info.phone = REPLACE(res-info.phone, " ", "").
			res-info.phone = REPLACE(res-info.phone, "-", "").
			IF SUBSTR(res-info.phone,1,3) EQ "+62" THEN
				res-info.phone = REPLACE(res-info.phone, "+62","0").
			ELSE IF SUBSTR(res-info.phone,1,2) EQ "62" THEN
				res-info.phone = REPLACE(res-info.phone, SUBSTR(res-info.phone,1,2),"0").
			
			IF res-info.phone NE "" AND res-info.phone NE "N/A" THEN
				FIND FIRST guest WHERE (guest.telefon MATCHES '*' + SUBSTR(res-info.phone,2) OR guest.mobil-telefon MATCHES '*' + SUBSTR(res-info.phone,2)) AND guest.NAME = res-info.sure-name AND guest.vorname1 = res-info.given-name NO-LOCK NO-ERROR.
			ELSE
			DO:	
				IF res-info.email NE "" AND res-info.email NE "N/A" THEN
				/*FIND FIRST guest WHERE (guest.vorname1 = res-info.given-name AND guest.email-adr = res-info.email)
					OR (guest.NAME = res-info.sure-name AND guest.vorname1 = res-info.given-name 
						AND guest.adresse1 = res-info.address1) NO-LOCK NO-ERROR.*/
					FIND FIRST guest WHERE (guest.email-adr = res-info.email OR guest.email-adr = "N/A" OR guest.email-adr = "") AND guest.NAME = res-info.sure-name AND
                    guest.vorname1 = res-info.given-name NO-LOCK NO-ERROR.
                ELSE
				    FIND FIRST guest WHERE (guest.NAME = res-info.sure-name AND guest.vorname1 = res-info.given-name 
					AND guest.adresse1 = res-info.address1) NO-LOCK NO-ERROR.
			END.
			IF NOT AVAILABLE guest THEN 
            DO:

                /*ENHANCE Validation if ""Unknown not found" still create Guest Card for reservation RVN 29/02/2024*/  
				IF res-info.country NE "" THEN 
				DO:
					t-guest-nat = "".
					FIND FIRST nation WHERE nation.bezeich = res-info.country NO-LOCK NO-ERROR.
					IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
					ELSE 
					DO:
						RUN if-siteminder-read-mappingbl.p (2, res-info.country, OUTPUT t-guest-nat).
						IF t-guest-nat NE "" THEN
						DO:
							FIND FIRST nation WHERE nation.kurzbez = t-guest-nat NO-LOCK NO-ERROR.
							IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
						END.
						ELSE
						DO:
							FIND FIRST nation WHERE nation.bezeich MATCHES "*Unknown*" NO-LOCK NO-ERROR.
							IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
							ELSE t-guest-nat = "".
						END.    
					END.
				END.
				ELSE DO:

                    /*Enhance Validasi kalau nationality kosong, ambil default county code - RVN - 30-10-2024 - 0783E2*/
                    FIND FIRST htparam WHERE htparam.paramnr = 153 NO-LOCK.
                    default-country = htparam.fchar.

                    IF default-country NE "" OR default-country NE ? THEN
                    DO:
                        ASSIGN
                            t-guest-nat = default-country.
                    END.
                    ELSE 
                    DO:
                        FIND FIRST nation WHERE nation.bezeich MATCHES "*Unknown*" NO-LOCK NO-ERROR.
					    IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
					    ELSE t-guest-nat = "".
                    END.

				END.
				exist = NO.
				gastnrmember = 0.
                FOR EACH guest USE-INDEX gastnr_index NO-LOCK BY guest.gastnr DESC:
					ASSIGN gastnrmember = guest.gastnr + 1.
					LEAVE.
				END.
                
				FIND FIRST rgast WHERE rgast.gastnr = gastnrmember NO-LOCK NO-ERROR.
				exist = AVAILABLE rgast.
					
				REPEAT WHILE exist :
					gastnrmember = gastnrmember + 1.
					FIND FIRST rgast WHERE rgast.gastnr = gastnrmember NO-LOCK NO-ERROR.
					exist = AVAILABLE rgast.
				END.
				IF NOT exist THEN DO:
					FIND FIRST bguest WHERE bguest.gastnr = gastnrmember NO-LOCK NO-ERROR.
					IF NOT AVAILABLE bguest THEN DO:
						CREATE bguest.
						ASSIGN 
							bguest.gastnr    = gastnrmember
							bguest.NAME      = res-info.sure-name
							bguest.vorname1  = res-info.given-name
							bguest.adresse1  = res-info.address1
							/*bguest.adresse2  = res-info.address2*/
							bguest.wohnort   = res-info.city
							bguest.land      = t-guest-nat
							bguest.plz       = res-info.zip
							bguest.email-adr = res-info.email
							bguest.telefon   = res-info.phone
							bguest.nation1   = t-guest-nat                    
							.
						IF c-number NE "" THEN
							bguest.ausweis-nr2 = artikel.bezeich + "\" + c-number + "\" + c-exp + "|".

						FIND FIRST guestseg WHERE guestseg.gastnr = ota-gastnr 
							AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR.
						IF AVAILABLE guestseg THEN
						DO:
							rsegm = guestseg.segmentcode.

							FIND FIRST gseg WHERE gseg.gastnr = gastnrmember AND gseg.segmentcode = rsegm AND gseg.reihenfolge = 1 NO-LOCK NO-ERROR.
							IF NOT AVAILABLE gseg THEN
							DO:
								CREATE gseg.
								ASSIGN
									gseg.gastnr      = gastnrmember
									gseg.reihenfolge = 1
									gseg.segmentcode = rsegm
								.    
							END.
						END.
					END.
				END.
			END.
            ELSE
            DO:
                gastnrmember = guest.gastnr.
                FIND FIRST bguest WHERE RECID(bguest) = RECID(guest) NO-LOCK NO-ERROR.
                IF AVAILABLE bguest AND bguest.ausweis-nr2 EQ "" AND c-number NE "" THEN DO:
					FIND CURRENT bguest EXCLUSIVE-LOCK.
                    bguest.ausweis-nr2 = artikel.bezeich + "\" + c-number + "\" + c-exp + "|".
					FIND CURRENT bguest NO-LOCK.
					RELEASE bguest.
				END.					
            END.
			ASSIGN
            res-info.gastnrmember = gastnrmember.

            IF res-info.membership NE "" THEN
            DO:   
                FIND FIRST mc-guest WHERE mc-guest.gastnr = gastnrmember NO-LOCK NO-ERROR.
                IF NOT AVAILABLE mc-guest THEN
                DO:            
                    CREATE mc-guest.
                    ASSIGN
                        mc-guest.gastnr        = gastnrmember
                        mc-guest.created-date  = TODAY
                        mc-guest.activeflag    = NO
                        mc-guest.fdate         = TODAY
                        mc-guest.tdate         = tahun + 32850
                        .
                    DO p = 1 TO NUM-ENTRIES(res-info.membership, "-"):
                        avalue = ENTRY(p, res-info.membership, "-").
                        IF avalue MATCHES "*membershipid*" THEN
                            mc-guest.cardnum = ENTRY(2, avalue, ":").
                        IF avalue MATCHES "*membershipprogram*" THEN
                            mc-guest.bemerk = ENTRY(2, avalue, ":").
                    END.
                END.
            END.
        END.

        FOR EACH guest-list:
            IF NOT NUM-ENTRIES(guest-list.email,"@") = 2 THEN            
                guest-list.email = "".
            ELSE
                IF NOT LENGTH(ENTRY(1,guest-list.email,"@")) GE 2
                    AND NOT LENGTH(ENTRY(2,guest-list.email,"@")) GE 2 THEN
                    guest-list.email = "".
			/* NC - 10/01/23 request Pak Stephen */	
			guest-list.phone = REPLACE(guest-list.phone, " ", "").
			guest-list.phone = REPLACE(guest-list.phone, "-", "").
			IF SUBSTR(guest-list.phone,1,3) EQ "+62" THEN
				guest-list.phone = REPLACE(guest-list.phone, "+62","0").
			ELSE IF SUBSTR(guest-list.phone,1,2) EQ "62" THEN
				guest-list.phone = REPLACE(guest-list.phone, SUBSTR(guest-list.phone,1,2),"0").	
				
			IF guest-list.phone NE "" AND guest-list.phone NE "N/A" THEN
				FIND FIRST guest WHERE (guest.telefon MATCHES '*' + SUBSTR(guest-list.phone,2) OR guest.mobil-telefon MATCHES '*' + SUBSTR(guest-list.phone,2)) AND guest.NAME = guest-list.sure-name AND guest.vorname1 = guest-list.given-name NO-LOCK NO-ERROR.
			ELSE
			DO:
				IF guest-list.email NE "" AND guest-list.email NE "N/A" THEN
					/*
				FIND FIRST guest WHERE (guest.vorname1 = guest-list.given-name AND guest.email-adr = guest-list.email)
					OR (guest.NAME = guest-list.sure-name AND guest.vorname1 = guest-list.given-name 
						AND guest.adresse1 = guest-list.address1) NO-LOCK NO-ERROR.*/
                    FIND FIRST guest WHERE (guest.email-adr = guest-list.email OR guest.email-adr = "N/A" OR
                    guest.email-adr = "") AND guest.NAME = guest-list.sure-name AND
                    guest.vorname1 = guest-list.given-name NO-LOCK NO-ERROR.
                ELSE
				    FIND FIRST guest WHERE (guest.NAME = guest-list.sure-name AND guest.vorname1 = guest-list.given-name 
                    AND guest.adresse1 = guest-list.address1) NO-LOCK NO-ERROR.
			END.
            IF NOT AVAILABLE guest THEN 
            DO:

                /*ENHANCE Validation if ""Unknown not found" still create Guest Card for reservation RVN 29/02/2024*/ 
                IF guest-list.country NE "" THEN
                DO:
					t-guest-nat = "".
                    FIND FIRST nation WHERE nation.bezeich = guest-list.country NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
                    ELSE 
                    DO:
                        RUN if-siteminder-read-mappingbl.p (2, guest-list.country, OUTPUT t-guest-nat).
                        IF t-guest-nat NE "" THEN
                        DO:
                            FIND FIRST nation WHERE nation.kurzbez = t-guest-nat NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
                        END.
                        ELSE ASSIGN  
								error-str = error-str + CHR(10) + "Guest country not mapping yet = " + guest-list.country
								t-guest-nat = "".

                    END.
                END.
				ELSE ASSIGN  
						error-str = error-str + CHR(10) + "Guest country not defined." 
						t-guest-nat = "".
				exist = NO.
				gastnrmember = 0.
                FOR EACH guest USE-INDEX gastnr_index NO-LOCK BY guest.gastnr DESC:
					ASSIGN gastnrmember = guest.gastnr + 1.
					LEAVE.
				END.
					
				FIND FIRST rgast WHERE rgast.gastnr = gastnrmember NO-LOCK NO-ERROR.
				exist = AVAILABLE rgast.
					
				REPEAT WHILE exist :
					gastnrmember = gastnrmember + 1.
					FIND FIRST rgast WHERE rgast.gastnr = gastnrmember NO-LOCK NO-ERROR.
					exist = AVAILABLE rgast.
				END.
				IF NOT exist THEN DO:
					FIND FIRST bguest WHERE bguest.gastnr = gastnrmember NO-LOCK NO-ERROR.
					IF NOT AVAILABLE bguest THEN DO:
						CREATE bguest.
						ASSIGN 
							bguest.gastnr    = gastnrmember
							bguest.NAME      = guest-list.sure-name
							bguest.vorname1  = guest-list.given-name
							bguest.adresse1  = guest-list.address1
							/*bguest.adresse2  = guest-list.address2*/
							bguest.wohnort   = guest-list.city
							bguest.land      = t-guest-nat
							bguest.plz       = guest-list.zip
							bguest.email-adr = guest-list.email
							bguest.telefon   = guest-list.phone
							bguest.nation1   = t-guest-nat                    
							.
						FIND FIRST guestseg WHERE guestseg.gastnr = ota-gastnr 
							AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR.
						IF AVAILABLE guestseg THEN
						DO:
							rsegm = guestseg.segmentcode.

							FIND FIRST gseg WHERE gseg.gastnr = gastnrmember AND gseg.segmentcode = rsegm AND gseg.reihenfolge = 1 NO-LOCK NO-ERROR.
							IF NOT AVAILABLE gseg THEN
							DO:
								CREATE gseg.
								ASSIGN
									gseg.gastnr      = gastnrmember
									gseg.reihenfolge = 1
									gseg.segmentcode = rsegm
								.    
							END.
						END.
					END.
				END.
            END.
            ELSE
            DO:
                gastnrmember = guest.gastnr.
            END.
			ASSIGN
            guest-list.gastnrmember = gastnrmember.
        END.
        
        bookingID = res-info.res-id.
        RELEASE reservation.
        
        IF res-mode = "new" THEN
        DO:
            FIND FIRST guestseg WHERE guestseg.gastnr = ota-gastnr
              AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guestseg THEN
            FIND FIRST guestseg WHERE guestseg.gastnr = ota-gastnr NO-LOCK NO-ERROR.
			
			exist = NO.
			new-resno = 0.
			/* NC-#561809 27/08/25 */  
			FOR EACH reservation USE-INDEX resnr_index NO-LOCK BY reservation.resnr DESC:
				ASSIGN new-resno = reservation.resnr + 1.
				LEAVE.
			END.

			FIND FIRST bres WHERE bres.resnr = new-resno NO-LOCK NO-ERROR.
			FIND FIRST bres-line WHERE bres-line.resnr = new-resno NO-LOCK NO-ERROR.
			exist = AVAILABLE bres OR AVAILABLE bres-line.

			 /* NC-#43398F 22/11/24 */
			REPEAT WHILE exist:
				new-resno = new-resno + 1.
				FIND FIRST bres WHERE bres.resnr = new-resno NO-LOCK NO-ERROR.
				FIND FIRST bres-line WHERE bres-line.resnr = new-resno NO-LOCK NO-ERROR.
				exist = AVAILABLE bres OR AVAILABLE bres-line.
				
			END.
			IF NOT exist THEN DO:
				FIND FIRST reservation WHERE reservation.resnr = new-resno NO-LOCK NO-ERROR.
				IF NOT AVAILABLE reservation THEN DO:
					CREATE reservation.
					ASSIGN
						reservation.resnr                 = new-resno
						reservation.gastnr                = ota-gastnr
						reservation.gastnrherk            = ota-gastnr
						reservation.herkunft              = ota-name /*NC - 15/12/24*/
						reservation.NAME                  = ota-name /*NC - 15/12/24*/
						reservation.useridanlage          = "**"
						reservation.vesrdepot             = bookingID /*---update to avoid double reservation --*/
						reservation.bemerk                = res-info.remark
						reservation.ankzeit               = 0
						reservation.point-resnr           = 0
					   /*  reservation.depositgef            = res-info.deposit NC - deposit related to backend and needs to filled manual in VHP*/
						. 
					IF AVAILABLE guestseg THEN 
					  reservation.segmentcode = guestseg.segmentcode.
					ELSE reservation.segmentcode = rsegcode.
			
					IF ota-seg NE 0 THEN 
					  reservation.resart = ota-seg.
					ELSE reservation.resart = resart.
				END.
				ELSE error-str = error-str + CHR(10) + "Reservation already exist with resnr: " +  STRING(reservation.resnr) + "; VN: " + STRING(reservation.vesrdepot) .
			END.
        END.
        ELSE IF res-mode = "Insert" THEN    
            FIND FIRST reservation WHERE reservation.resnr = new-resno NO-LOCK. 
			
		RELEASE res-line.
		loop-i = 0.
        FOR EACH room-list:
            loop-i = loop-i + 1.
            IF res-mode = "new" THEN 
                room-list.reslinnr = loop-i.
            RUN add-resline(room-list.reslinnr). /* NC-#43398F 22/11/24 */
        END.
            
        ASSIGN  done = YES 
        /*curr-error-str = "OC"  + chDelimeter1 + res-info.ota-code                               + chDelimeter2 + 
                         "RC"  + chDelimeter1 + res-info.rate-code                              + chDelimeter2 + 
                         "RT"  + chDelimeter1 + res-info.room-type                              + chDelimeter2 + 
                         "CI"  + chDelimeter1 + STRING(res-info.ci-date, "99/99/9999")          + chDelimeter2 + 
                         "CO"  + chDelimeter1 + STRING(res-info.co-date, "99/99/9999")          + chDelimeter2 + 
                         "AM"  + chDelimeter1 + res-info.amount                                 + chDelimeter2 + 
                         "NR"  + chDelimeter1 + STRING(res-info.no-room)                        + chDelimeter2 + 
                         "AD"  + chDelimeter1 + STRING(res-info.adult)                          + chDelimeter2 + 
                         "CH1" + chDelimeter1 + STRING(res-info.child1)                         + chDelimeter2 + 
                         "CH2" + chDelimeter1 + STRING(res-info.child2)                         + chDelimeter2 + 
                         "GN"  + chDelimeter1 + res-info.sure-name + "," + res-info.given-name  + chDelimeter2 + 
                         error-str.*/
        error-str = error-str + curr-error-str.
		
		IF error-str MATCHES "*resnr*" THEN done = NO.

        i = i + 1.
    /*END.*/
END.

/****************************** PROCEDURES **********************************/
PROCEDURE add-resline:    
    DEFINE INPUT PARAMETER new-reslinno    AS INTEGER .
    DEFINE VARIABLE allotnr         AS INTEGER INITIAL 0.
    DEFINE VARIABLE statCode        AS CHAR.    
    DEFINE VARIABLE res-statCode    AS CHAR.
    DEFINE VARIABLE start-date      AS DATE.
    DEFINE VARIABLE end-date        AS DATE.
    DEFINE BUFFER bufguest FOR guest.
    DEFINE BUFFER guestbuff FOR guest.
    DEFINE BUFFER mcguestbuf FOR mc-guest.

    IF new-contrate THEN RUN create-new-fixrate(new-resno, room-list.reslinnr,
                                                OUTPUT statCode, OUTPUT res-statCode).
    ELSE RUN create-fixed-rate(new-resno, room-list.reslinnr).

    IF res-info.eta NE "" THEN
    DO:
        hh = ENTRY(1, res-info.eta, ":").
        mm = ENTRY(2, res-info.eta, ":").
        eta-char = hh + mm.
    END.
    ELSE eta-char = "0000".
    
    /*MT 19/11/12 */
    RUN global-allotment-number.p(cm-gastno, ota-gastnr, room-list.ankunft,
                                  room-list.abreise, rmtype,OUTPUT allotnr).

	FIND FIRST res-line WHERE res-line.resnr EQ new-resno AND res-line.reslinnr EQ new-reslinno NO-LOCK NO-ERROR.
	IF NOT AVAILABLE res-line THEN DO :

		CREATE res-line.
		ASSIGN
			res-line.resnr                        = new-resno
			res-line.reslinnr                     = new-reslinno
			res-line.gastnr                       = ota-gastnr
			res-line.gastnrpay                    = ota-gastnr
			res-line.ankunft                      = room-list.ankunft
			res-line.abreise                      = room-list.abreise
			res-line.flight-nr                    = "      " + STRING(eta-char, "x(5)") +
													"           "
			res-line.arrangement                  = argt
			res-line.resstatus                    = resstatus
			res-line.erwachs                      = room-list.adult
			res-line.kind1                        = room-list.child1
			res-line.kind2                        = room-list.child2
			res-line.betriebsnr                   = currno
			res-line.bemerk                       = room-list.comment + chDelimeter1 
			res-line.zimmeranz                    = 1 /*M always one because qty of the room will be broke down */
			res-line.zikatnr                      = zikatNo
			res-line.zipreis                      = ci-rate1
			res-line.was-status                   = 1      /* fixed rate */
			res-line.reserve-char                 = STRING(YEAR(TODAY) - 2000, "99") + "/" 
													+ STRING(MONTH(TODAY), "99") + "/" 
													+ STRING(DAY(TODAY), "99") 
													+ STRING(TIME,"HH:MM") 
													+ "**"
			res-line.reserve-int                  = markno
			.

		FIND FIRST guest-list WHERE guest-list.gastnr = room-list.gastnr NO-LOCK NO-ERROR.
		IF AVAILABLE guest-list THEN
		DO:
			FIND FIRST bufguest WHERE bufguest.gastnr = guest-list.gastnrmember NO-LOCK NO-ERROR.
			IF AVAILABLE bufguest THEN DO:
			ASSIGN
				res-line.gastnrmember = bufguest.gastnr
                res-line.NAME = bufguest.NAME + ", " + bufguest.vorname1 + ", " + bufguest.anrede1.

				error-str = error-str + CHR(10) + " Assign Guest Room: " + bufguest.name + "(" + STRING(bufguest.gastnr) + ")".
			END.
		END.
        ELSE
        DO:
            FIND FIRST bufguest WHERE bufguest.gastnr = res-info.gastnrmember NO-LOCK NO-ERROR.
			IF AVAILABLE bufguest THEN DO:
			ASSIGN
				res-line.gastnrmember = bufguest.gastnr
                res-line.NAME = bufguest.NAME + ", " + bufguest.vorname1 + ", " + bufguest.anrede1.

				error-str = error-str + CHR(10) + "Assign Guest Room: " + bufguest.name + "(" + STRING(bufguest.gastnr) + ")".
			END.
        END.
        
		
		/*NC - 07/08/24 #E78F56*/
		IF room-list.comment EQ "" THEN res-line.bemerk = "".
		
		IF room-list.ankunft = room-list.abreise THEN
			res-line.anztage = 1.
		ELSE res-line.anztage = room-list.abreise - room-list.ankunft.

		IF res-line.resstatus = 1 THEN
		   res-line.kontignr                     = allotnr.

		IF new-contrate THEN
		DO:
			res-line.zimmer-wunsch = "ebdisc;restricted;date,"
									+ STRING(YEAR(curr-date)) + STRING(MONTH(curr-date),"99")
									+ STRING(DAY(curr-date),"99") + ";" 
									+ "voucher" + bookingID + ";" 
									+ "$CODE$" + res-statCode + ";"
									+ "$OrigCode$" + room-list.rate-code + ";".
		END.

		/* CHIRAG 20DEC2018 FOR GDPR */
		IF avail-gdpr THEN
		DO:
			FIND FIRST guestbuff WHERE guestbuff.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
			IF AVAILABLE guestbuff THEN
			DO: /*kalo guestnya dari negara EU*/
				FIND FIRST mcguestbuf WHERE mcguestbuf.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
				IF AVAILABLE mcguestbuf THEN ASSIGN do-it = NO.
			
				IF guestbuff.land NE " " THEN ASSIGN curr-nat = guestbuff.land.
				ELSE IF guestbuff.nation1 NE " " THEN ASSIGN curr-nat = guestbuff.nation1.
			
				FIND FIRST nation-list WHERE nation-list.nat-abbr = curr-nat NO-LOCK NO-ERROR.
				IF AVAILABLE nation-list THEN do-it = YES.
				ELSE do-it = NO.

				IF do-it THEN
				DO:
					IF NOT res-line.zimmer-wunsch MATCHES "*GDPR*" THEN
					DO:
						res-line.zimmer-wunsch = res-line.zimmer-wunsch + "GDPRyes;".
					END.                
				END.
			END.
		END.

		res-info.remark = REPLACE(res-info.remark, ";", ",").
		/*Storing Booking Engine Comment*/
		res-line.zimmer-wunsch = res-line.zimmer-wunsch + "$OTACOM$" + res-info.remark + chDelimeter1 + "SM-TIME," + res-info.res-time + ";" + "$PAID$" + res-info.commission + ";" + "$PRCODE$" + res-info.address2 + ";".

		IF NUM-ENTRIES(room-list.service,"-") NE 0 THEN
		DO: /*NC - 12/09/19 service room level*/
			DO i = 1 TO NUM-ENTRIES(room-list.service,"-") - 1:
				FIND FIRST service-list WHERE service-list.rph = ENTRY(i,room-list.service,"-") NO-LOCK NO-ERROR.
				IF AVAILABLE service-list THEN
				DO:
					IF service-list.ci-date NE "" THEN
						start-date = DATE(INT(ENTRY(2,service-list.ci-date,"-")),INT(ENTRY(3,service-list.ci-date,"-")),INT(ENTRY(1,service-list.ci-date,"-"))).

					IF service-list.co-date NE "" THEN
						end-date = DATE(INT(ENTRY(2,service-list.co-date,"-")),INT(ENTRY(3,service-list.co-date,"-")),INT(ENTRY(1,service-list.co-date,"-"))).


					CREATE fixleist.
					ASSIGN
						fixleist.bezeich = service-list.bezeich
						fixleist.number = service-list.qty
						fixleist.sequenz = 6
						fixleist.betrag = service-list.amountaftertax
						fixleist.artnr = service-artnr
						fixleist.departement = service-dept
						fixleist.resnr = new-resno
						fixleist.reslinnr = room-list.reslinnr
					.
					IF foreign-rate OR double-currency THEN
							fixleist.betrag = fixleist.betrag * (sm-frate / ratecode-frate).
					IF start-date EQ ? THEN
						ASSIGN
							fixleist.lfakt = room-list.ankunft
							fixleist.dekade = room-list.abreise - room-list.ankunft
						.
					ELSE IF start-date NE ? THEN
						ASSIGN
							fixleist.lfakt = start-date
							fixleist.dekade = end-date - start-date
						.
					IF fixleist.dekade = 0 THEN
						fixleist.dekade = 1.
				END.
			END.
		END.
		/*
		ELSE
		DO: /*NC - 12/09/19 service reservation level*/
			FOR EACH service-list WHERE service-list.res-id = bookingID NO-LOCK:
				IF service-list.ci-date NE "" THEN
					start-date = DATE(INT(ENTRY(2,service-list.ci-date,"-")),INT(ENTRY(3,service-list.ci-date,"-")),INT(ENTRY(1,service-list.ci-date,"-"))).

				IF service-list.co-date NE "" THEN
					end-date = DATE(INT(ENTRY(2,service-list.co-date,"-")),INT(ENTRY(3,service-list.co-date,"-")),INT(ENTRY(1,service-list.co-date,"-"))).


				FIND FIRST fixleist WHERE fixleist.resnr EQ res-line.resnr 
				AND fixleist.reslinnr EQ 1 /*applied to first room stay*/
				AND fixleist.departement EQ service-dept 
				AND fixleist.artnr EQ service-artnr
				AND fixleist.sequenz EQ 6
				AND fixleist.bezeich EQ service-list.bezeich NO-ERROR.
				IF NOT AVAILABLE fixleist THEN CREATE fixleist.
				ASSIGN
					fixleist.bezeich = service-list.bezeich
					fixleist.number = service-list.qty
					fixleist.sequenz = 6
					fixleist.betrag = service-list.amountaftertax
					fixleist.artnr = service-artnr
					fixleist.departement = service-dept
					fixleist.resnr = new-resno
					fixleist.reslinnr = 1
				.
				IF foreign-rate OR double-currency THEN
						fixleist.betrag = fixleist.betrag * (sm-frate / ratecode-frate).
				IF start-date EQ ? THEN
					ASSIGN
						fixleist.lfakt = room-list.ankunft
						fixleist.dekade = room-list.abreise - room-list.ankunft
					.
				ELSE IF start-date NE ? THEN
					ASSIGN
						fixleist.lfakt = start-date
						fixleist.dekade = end-date - start-date
					.
				IF fixleist.dekade = 0 THEN
					fixleist.dekade = 1.
			END.
		END.*/
	

		rm-qty = res-line.zimmeranz.
		FIND CURRENT res-line NO-LOCK.

		/* CRG 17/07/2023 add new data trigger for crm */
		IF res-mode = "new" THEN
			RUN intevent-1.p(12, "", "Priscilla", res-line.resnr, res-line.reslinnr).
		ELSE IF res-mode = "insert" THEN
			RUN intevent-1.p(11, "", "Priscilla", res-line.resnr, res-line.reslinnr).

		RUN create-resplan.
		RUN create-reslog.
		error-str = error-str + "CUR" + chDelimeter1 + STRING(res-line.betriebsnr).
		RELEASE res-line.
    END.
	ELSE error-str = error-str + CHR(10) + "Resline already exist with resnr: " +  STRING(res-line.resnr) + ";reslinnr: " + STRING(res-line.reslinnr) + ";loop: " + STRING(loop-i) .
END PROCEDURE.

PROCEDURE create-new-fixrate:
    DEFINE INPUT PARAMETER resno         AS INTEGER.
    DEFINE INPUT PARAMETER reslinno      AS INTEGER.
    DEFINE OUTPUT PARAMETER StatCode     AS CHAR.
    DEFINE OUTPUT PARAMETER res-StatCode AS CHAR.
	/* NC - Move up as global variable 21/06/22
    DEFINE VARIABLE bill-date       AS DATE         NO-UNDO.
    DEFINE VARIABLE upto-date       AS DATE         NO-UNDO.
	*/
    DEFINE VARIABLE rate-found      AS LOGICAL      NO-UNDO.
    DEFINE VARIABLE rmrate          AS DECIMAL      NO-UNDO.
    DEFINE VARIABLE kback-flag      AS LOGICAL      NO-UNDO.
    DEFINE VARIABLE n               AS INTEGER      NO-UNDO INITIAL 0.
    DEFINE VARIABLE ratecode-curr   AS CHAR.
    DEFINE VARIABLE serv            AS DECIMAL.
    DEFINE VARIABLE vat             AS DECIMAL.

    DEFINE VARIABLE currno-SM       AS INT.
    DEFINE VARIABLE check-arg       AS LOGICAL INIT NO.
/* NC - Move up as global variable 21/06/22
    DEFINE BUFFER bres      FOR reservation.
    DEFINE BUFFER bres-line FOR res-line.
	
    DEFINE BUFFER rqueasy   FOR queasy.
    DEFINE BUFFER qsy       FOR queasy.
    DEFINE BUFFER bqueasy   FOR queasy.
    DEFINE VARIABLE zikatnr AS INTEGER.
	*/
    DEFINE VARIABLE avail-room AS INTEGER.
    DEFINE VARIABLE avail-rmtype AS INTEGER.
    
    DEFINE VARIABLE i AS INT.

    IF room-list.ankunft = room-list.abreise THEN upto-date = room-list.abreise.
    ELSE upto-date = room-list.abreise - 1.

    FIND FIRST arrangement WHERE arrangement.arrangement = room-list.argtnr NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement THEN argtno = arrangement.argtnr.
    DO bill-date = room-list.ankunft TO upto-date :
        n = n + 1.
        currno = 0.
        markno = 0.

        FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr
            AND artikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
            RUN calc-servvat.p (artikel.departement, artikel.artnr, bill-date,
                artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
        
        IF tax-included THEN
        DO:
            IF NUM-ENTRIES(room-list.amount, "-") - 1 GT 1 THEN
                room-price = DECIMAL(ENTRY(n, room-list.amount, "-")).
            ELSE room-price = DECIMAL(ENTRY(1, room-list.amount, "-")).
        END.
        ELSE
        DO:
            IF NUM-ENTRIES(room-list.amount, "-") - 1 GT 1 THEN
                room-price = ROUND(DECIMAL(ENTRY(n, room-list.amount, "-")) / (1 + serv + vat),0).                             
            ELSE room-price = ROUND(DECIMAL(ENTRY(1, room-list.amount, "-")) / (1 + serv + vat),0).               
        END.

        ci-rate = room-price.  /*MT 9/11/12 */

        FIND FIRST waehrung WHERE waehrung.wabkurz = res-info.curr
            AND waehrung.betriebsnr = 0 NO-LOCK NO-ERROR.           /* perbaikan Chirag 05OCT18 */
        IF NOT AVAILABLE waehrung THEN
        DO:
            RUN if-siteminder-read-mappingbl.p (1, res-info.curr, OUTPUT t-curr-name).
            IF t-curr-name NE "" THEN
                FIND FIRST waehrung WHERE waehrung.wabkurz = t-curr-name AND waehrung.betriebsnr = 0 NO-LOCK NO-ERROR.
        END.    
        IF AVAILABLE waehrung THEN currno-SM = waehrung.waehrungsnr.
		/*NC - Move up 21/06/22
        FIND FIRST rqueasy WHERE rqueasy.KEY = 2 AND rqueasy.char1 = room-list.rate-code 
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE rqueasy THEN room-list.rate-code = dyna-code.
		*/
        FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.char1 = room-list.room-type NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            zikatnr = queasy.number1.
            RUN count-availability.p (bill-date,OUTPUT TABLE room-avail-list).
            avail-room = 0.
            avail-rmtype = 0.
            FOR EACH room-avail-list WHERE room-avail-list.i-typ = queasy.number1 BY room-avail-list.room :
                IF room-avail-list.room GE avail-room THEN
                    ASSIGN
                        avail-room   = room-avail-list.room
                        avail-rmtype = room-avail-list.zikatnr.
            END.
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = avail-rmtype NO-LOCK NO-ERROR.
            IF NOT AVAILABLE zimkateg THEN 
                FIND FIRST zimkateg WHERE zimkateg.typ = queasy.number1 NO-LOCK NO-ERROR.
            rmtype = zimkateg.kurzbez.
        END.
        ELSE
        DO:
            FIND FIRST zimkateg WHERE zimkateg.kurzbez = room-list.room-type NO-LOCK NO-ERROR.
            IF AVAILABLE zimkateg THEN 
                ASSIGN
                    rmtype = room-list.room-type 
                    zikatnr = zimkateg.zikatnr.
        END.

        FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmtype NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN zikatno = zimkateg.zikatnr.

        FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
          AND qsy.number1 = zikatnr AND qsy.char1 = room-list.rate-code NO-LOCK NO-ERROR.
        IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
        DO:
            FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) NO-LOCK NO-ERROR.
            IF AVAILABLE bqueasy THEN
            DO:
				FIND CURRENT bqueasy EXCLUSIVE-LOCK.
                bqueasy.logi2 = YES.
                FIND CURRENT bqueasy NO-LOCK.
                RELEASE bqueasy.
            END.
        END.
        
        FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
          AND qsy.number1 = zikatnr AND qsy.char1 = "" NO-LOCK NO-ERROR.
        IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
        DO:
            FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) NO-LOCK NO-ERROR.
            IF AVAILABLE bqueasy THEN
            DO:
				FIND CURRENT bqueasy EXCLUSIVE-LOCK.
                bqueasy.logi2 = YES.
                FIND CURRENT bqueasy NO-LOCK.
                RELEASE bqueasy.
            END.
        END.

        /* BLY - Adding Output Room-OCC */
        RUN find-dyna-ratecodesm_1bl.p(ota-gastnr, bill-date, rmtype,
                                   room-list.adult, room-list.child1, room-price,
                                   room-list.rate-code, OUTPUT StatCode,
                                   INPUT-OUTPUT argtno, OUTPUT markno,
                                   OUTPUT currno, OUTPUT room-occ).

        IF n = 1 THEN res-statcode = statCode.
        
        FIND FIRST queasy WHERE queasy.KEY = 18 AND queasy.number1 = markNo
            NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.char3 NE "" THEN 
        DO:    
            FIND FIRST waehrung WHERE waehrung.wabkurz = queasy.char3 NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN currNo = waehrung.waehrungsnr.
        END.

        IF currno-SM NE 0 AND currno NE 0 AND currno-SM NE currno THEN
        DO:
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = currno
                AND waehrung.betriebsnr = 0
                NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN ratecode-frate = waehrung.ankauf / waehrung.einheit.

            FIND FIRST waehrung WHERE waehrung.wabkurz = res-info.curr
                AND waehrung.betriebsnr = 0
                NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN sm-frate = waehrung.ankauf / waehrung.einheit.

            ci-rate = ci-rate * (sm-frate / ratecode-frate).
            ci-rate = ROUND(ci-rate, price-decimal).

            FIND FIRST rqueasy WHERE rqueasy.KEY = 2 AND rqueasy.char1 = room-list.rate-code 
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rqueasy THEN room-list.rate-code = dyna-code.

            /* BLY - Adding Output Room-OCC */
            RUN find-dyna-ratecodesm_1bl.p(ota-gastnr, bill-date, rmtype,
                                       room-list.adult, room-list.child1, ci-rate,
                                       room-list.rate-code, OUTPUT StatCode,
                                       INPUT-OUTPUT argtno, OUTPUT markno,
                                       OUTPUT currno, OUTPUT room-occ).

            IF n = 1 THEN res-statcode = statCode.
        END. /*masih bingung*/
        
        IF argtno = 0 THEN
        DO: 
            FIND FIRST ratecode WHERE ratecode.CODE = room-list.rate-code 
                AND ratecode.zikatNr = zikatNo NO-LOCK NO-ERROR.
            IF NOT AVAILABLE ratecode THEN
            DO:
                error-str = error-str + "Arrangement Not Found " + room-list.rate-code
                            + " " + STRING(zikatno).

                /*MT check arrangement */
                FIND FIRST htparam WHERE paramnr = 151 NO-LOCK. 
                IF htparam.fchar NE "" THEN
                DO:
                    FIND FIRST arrangement WHERE arrangement.arrangement = htparam.fchar NO-LOCK NO-ERROR. 
                    IF AVAILABLE arrangement THEN 
						ASSIGN 
							argt = arrangement.arrangement
							argtno = arrangement.argtnr. /*NC 21/09/22 */
                    ELSE check-arg = YES.
                END.
                ELSE check-arg = YES.

                IF check-arg THEN
                DO:
                    FIND FIRST arrangement WHERE arrangement.segmentcode = 0 NO-LOCK.
					IF AVAILABLE arrangement THEN 
						ASSIGN 
							argt = arrangement.arrangement
							argtno = arrangement.argtnr. /*NC 21/09/22 */
                END.
            END.
        END.
		ELSE 
		DO:
			FIND FIRST arrangement WHERE arrangement.argtnr = argtno NO-LOCK NO-ERROR.
            IF AVAILABLE arrangement THEN argt = arrangement.arrangement.
		END.
        IF markno = 0 THEN
        DO:
            error-str = error-str + "Market Segment Not Found.".
        END.
        IF currno = 0 THEN
        DO:
            FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK NO-ERROR.
            IF AVAILABLE htparam THEN
            DO:
                FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
                IF NOT AVAILABLE waehrung THEN
                    FIND FIRST waehrung NO-LOCK NO-ERROR.
                currNo = waehrung.waehrungsnr.

            END.
        END.
        
        /* IF argtno NE 0 THEN
        DO:
            FIND FIRST arrangement WHERE arrangement.argtnr = argtno NO-LOCK NO-ERROR.
            IF AVAILABLE arrangement THEN argt = arrangement.arrangement.
        END. */ /*NC - Move to up => ELSE*/
        
        RUN ratecode-rate.p(YES, YES, resno, reslinno, /*( "!" + ratecode1 )*/ ( "!" + StatCode ),
                            curr-date, bill-date, room-list.ankunft, room-list.abreise, 
                            markno, argtno, zikatno, room-list.adult, 
                            room-list.child1, room-list.child2, 0, currno, 
                            OUTPUT rate-found, OUTPUT rmrate, 
                            OUTPUT restricted-disc, OUTPUT kback-flag).

        /*MTRUN calc-commisions (INPUT-OUTPUT room-price).*/
		IF artnr-comm NE 0 THEN
		DO:
			IF dcommission THEN RUN calc-commissions (bill-date, resno, reslinno, argtno, room-price). /*NC - 21/09/22 added for OTA commission stored in VHP as arrangement */.
		END.
		
        CREATE reslin-queasy.
        ASSIGN
            reslin-queasy.key       = "arrangement" 
            reslin-queasy.resnr     = resno
            reslin-queasy.reslinnr  = reslinno 
            reslin-queasy.date1     = bill-date 
            reslin-queasy.date2     = bill-date 
            reslin-queasy.deci1     = /*room-price*/ ci-rate
            reslin-queasy.char1     = argt
            reslin-queasy.char2     = /*MTratecode1*/ StatCode
            .

        CREATE reslin-queasy.
        ASSIGN
            reslin-queasy.key       = "occ-room" 
            reslin-queasy.resnr     = resno
            reslin-queasy.reslinnr  = reslinno 
            reslin-queasy.date1     = bill-date 
            reslin-queasy.date2     = bill-date 
            reslin-queasy.deci1     = ci-rate /*room-price*/ 
            reslin-queasy.char1     = argt
            reslin-queasy.char2     = StatCode /*MTratecode1*/
            reslin-queasy.number1   = room-occ
            .
        FIND CURRENT reslin-queasy NO-LOCK.
        IF bill-date = room-list.ankunft THEN ci-rate1 = ci-rate.
    END.
END.

PROCEDURE create-fixed-rate:
    DEFINE INPUT PARAMETER resno       AS INTEGER.
    DEFINE INPUT PARAMETER reslinno    AS INTEGER.
    DEFINE VARIABLE bill-date          AS DATE      NO-UNDO.

    FIND FIRST guest-pr WHERE guest-pr.gastnr = ota-gastnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE guest-pr THEN
    DO:
        error-str = error-str + "Guest PR not available for gastnr" 
                  + STRING(ota-gastnr) + ".".
        RETURN.
    END.
        
    FIND FIRST ratecode WHERE ratecode.CODE = guest-pr.CODE NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN 
        ASSIGN  markno  = ratecode.marknr
                argtno  = ratecode.argtnr.
    
    IF argtno = 0 THEN
    DO:
        error-str = error-str + "Arrangement not available".
        RETURN.
    END.
    ELSE 
    DO:
        FIND FIRST arrangement WHERE arrangement.argtnr = argtno NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN argt = arrangement.arrangement.
    END.
    IF room-list.ankunft = room-list.abreise THEN upto-date = room-list.abreise.
    ELSE upto-date = room-list.abreise - 1. /* NC - #074913*/
    DO bill-date = room-list.ankunft TO upto-date:
        FIND FIRST pricecod WHERE pricecod.code = guest-pr.code 
            AND pricecod.marknr = markno 
            AND pricecod.argtnr = arrangement.argtnr 
            AND pricecod.zikatnr = zikatNo
            AND pricecod.startperiode LE bill-date
            AND pricecod.endperiode GE bill-date NO-LOCK NO-ERROR. 
        IF AVAILABLE pricecod THEN
        DO:
            CREATE reslin-queasy.
            ASSIGN
                reslin-queasy.key = "arrangement" 
                reslin-queasy.resnr = resno
                reslin-queasy.reslinnr = reslinno 
                reslin-queasy.date1 = bill-date 
                reslin-queasy.date2 = bill-date 
                reslin-queasy.deci1 = pricecod.perspreis[room-list.adult] 
                                    + pricecod.kindpreis[1] * room-list.child1 
                reslin-queasy.char1 = argt
            . 
            FIND CURRENT reslin-queasy NO-LOCK. 
            IF bill-date = room-list.ankunft THEN ci-rate = reslin-queasy.deci1.
			/* NC - NOT SURE used in grup reservation
			IF artnr-comm NE 0 THEN
			DO:
				IF dcommission THEN RUN calc-commissions (bill-date, resno, reslinno, argtno, reslin-queasy.deci1). /*NC - 21/09/22 added for OTA commission stored in VHP as arrangement */.
			END.
			*/
        END.
    END.
END.  

PROCEDURE create-reslog:
    DEFINE BUFFER guest1 FOR guest.
    DEFINE VARIABLE cid   AS CHAR FORMAT "x(2)" INITIAL "  ".
    DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        ".
    
    CREATE reslin-queasy.
    ASSIGN
            reslin-queasy.key      = "ResChanges"
            reslin-queasy.resnr    = res-line.resnr
            reslin-queasy.reslinnr = res-line.reslinnr
            reslin-queasy.date2    = TODAY
            reslin-queasy.number2  = TIME
            reslin-queasy.char3    = STRING(res-line.ankunft)                   + ";"
                                    + STRING(res-line.ankunft)                  + ";"
                                    + STRING(res-line.abreise)                  + ";"
                                    + STRING(res-line.abreise)                  + ";"
                                    + STRING(res-line.zimmeranz, ">>9")         + ";"
                                    + STRING(res-line.zimmeranz, ">>9")         + ";"
                                    + STRING(res-line.erwachs, ">9")            + ";"
                                    + STRING(res-line.erwachs, ">9")            + ";"
                                    + STRING(res-line.kind1, ">9")              + ";"
                                    + STRING(res-line.kind1, ">9")              + ";"
                                    + STRING(res-line.gratis, ">9")             + ";"
                                    + STRING(res-line.gratis, ">9")             + ";"
                                    + STRING(res-line.zikatnr, ">>9")           + ";"
                                    + STRING(res-line.zikatnr, ">>9")           + ";"
                                    + STRING(res-line.zinr, "x(4)")             + ";"
                                    + STRING(res-line.zinr, "x(4)")             + ";"
                                    + STRING(res-line.arrangement, "x(5)")      + ";"
                                    + STRING(res-line.arrangement, "x(5)")      + ";"
                                    + STRING(res-line.zipreis, ">,>>>,>>9.99")  + ";"
                                    + STRING(res-line.zipreis, ">,>>>,>>9.99")  + ";"
                                    + STRING("**", "x(2)")                      + ";"
                                    + STRING("**", "x(2)")                      + ";"
                                    + STRING(TODAY)                             + ";"
                                    + STRING(TODAY)                             + ";"
                                    + STRING(res-line.name, "x(16)")            + ";"
                                    + STRING("New Reservation", "x(16)")        + ";"
                                    + STRING("YES", "x(3)")  /* fixed rate */   + ";"
                                    + STRING("YES", "x(3)")                     
                                    .
    
    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy.
END PROCEDURE.

PROCEDURE create-resplan:
    DEFINE VARIABLE curr-date AS DATE NO-UNDO.
	IF res-line.ankunft = res-line.abreise THEN upto-date = res-line.abreise.
    ELSE upto-date = res-line.abreise - 1. /* NC - #074913*/
    DO curr-date = res-line.ankunft TO upto-date:
        FIND FIRST resplan WHERE resplan.zikatnr = res-line.zikatnr
            AND resplan.datum = curr-date NO-LOCK NO-ERROR. /* NC - #C4E865*/
        IF AVAILABLE resplan THEN
        DO:
			FIND CURRENT resplan EXCLUSIVE-LOCK.
			resplan.anzzim[res-line.resstatus] = resplan.anzzim[res-line.resstatus] + res-line.zimmeranz.
			FIND CURRENT resplan NO-LOCK.
			RELEASE resplan.
           
        END.
		ELSE DO: /* NC - #C4E865*/
			CREATE resplan.
			ASSIGN  resplan.datum = curr-date
                    resplan.zikatnr = res-line.zikatnr
					resplan.anzzim[res-line.resstatus] = resplan.anzzim[res-line.resstatus] + res-line.zimmeranz.
		END.
    END.
END PROCEDURE.
/*
PROCEDURE calc-commisions :
    DEFINE INPUT-OUTPUT PARAMETER room-price    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ccommission     AS CHAR NO-UNDO INITIAL "0".
    DEFINE VARIABLE dcommission     AS DEC  NO-UNDO INITIAL 0 FORMAT "->9.999".
    DEFINE VARIABLE decs            AS DEC  NO-UNDO INITIAL 0 FORMAT "->9.999".
    DEFINE VARIABLE points          AS CHAR NO-UNDO.

    ccommission = res-info.commission.

    IF ccommission MATCHES "*%*" THEN
        ccommission = TRIM(REPLACE(ccommission, "%", "")).
    
    IF ccommission MATCHES "*,*" THEN
    DO:
        ASSIGN  decs    = DEC(ENTRY(1, ccommission, ","))
                points  = ENTRY(2, ccommission, ",").
    END.
    ELSE IF ccommission MATCHES "*.*" 
        AND NUM-ENTRIES(ccommission, ".") GE 2 THEN
    DO:
        ASSIGN  decs    = DEC(ENTRY(1, ccommission, "."))
                points  = ENTRY(2, ccommission, ".").
    END.
    ELSE ASSIGN decs    = DEC(ccommission)
                points  = "0".
    
    dcommission = decs + 
                (DEC(SUBSTRING(points, 1, 1)) / 10) +
                (DEC(SUBSTRING(points, 2, 1)) / 100) +
                (DEC(SUBSTRING(points, 3, 1)) / 1000)
        .

    room-price = ROUND(room-price * ( 1 + (dcommission / 100)), 2).
END.
*/
/*
PROCEDURE check-vhp-rsv:
    DEFINE VARIABLE bill-date   AS DATE.
    DEFINE VARIABLE statCode    AS CHAR.
 
    DO bill-date = detRes.ci-date TO detRes.co-date:
        RUN find-dyna-ratecodesm.p(ota-gastnr, bill-date, detRes.room-type,
                                   1, 1, globekey-tot-amount,
                                   detRes.rate-code, OUTPUT StatCode,
                                   INPUT-OUTPUT argtno, OUTPUT markno,
                                   OUTPUT currno).
        RUN calc-dynaratessm.p(bill-date, bill-date, SM-gastno,
                               detRes.rate-code, zikatNo, argtNo, 1,
                               1, OUTPUT TABLE rate-list2).
        FOR EACH rate-list2: /*M to store rates from all roomtype and argt */
            CREATE rate-list.
            BUFFER-COPY rate-list2 TO rate-list.
        END.
    END.


    FOR EACH rate-list WHERE rate-list.room-type = detRes.room-type
        AND rate-list.datum GE detRes.ci-date
        AND rate-list.datum LT detRes.co-date
        NO-LOCK:
        tot-rmrate-VHP = tot-rmrate-VHP + rate-list.rmRate.
    END.
END.*/

/*RVN 5D4197 Update Validasi Special Character*/
PROCEDURE chk-ascii:
    DEF INPUT  PARAMETER str1 AS CHAR NO-UNDO.
    DEF OUTPUT PARAMETER str2 AS CHAR NO-UNDO INIT "".
    
    DEF VAR curr-i AS INT NO-UNDO.

    str2 = "".
    DO curr-i = 1 TO LENGTH(str1):
       IF ASC(SUBSTR(str1, curr-i, 1)) EQ 10 THEN
           str2 = str2 + "-".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) LT 32 THEN
           str2 = str2 + "-".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 192 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 193
            OR ASC(SUBSTR(str1, curr-i, 1)) = 194
            OR ASC(SUBSTR(str1, curr-i, 1)) = 195
            OR ASC(SUBSTR(str1, curr-i, 1)) = 196
            OR ASC(SUBSTR(str1, curr-i, 1)) = 197 THEN 
           str2 = str2 + "A".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 224 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 225
            OR ASC(SUBSTR(str1, curr-i, 1)) = 226
            OR ASC(SUBSTR(str1, curr-i, 1)) = 227
            OR ASC(SUBSTR(str1, curr-i, 1)) = 228
            OR ASC(SUBSTR(str1, curr-i, 1)) = 229 THEN 
           str2 = str2 + "a".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 200 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 201
            OR ASC(SUBSTR(str1, curr-i, 1)) = 202
            OR ASC(SUBSTR(str1, curr-i, 1)) = 203 THEN 
           str2 = str2 + "E".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 232 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 233
            OR ASC(SUBSTR(str1, curr-i, 1)) = 234
            OR ASC(SUBSTR(str1, curr-i, 1)) = 235 THEN 
           str2 = str2 + "e".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 204 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 205
            OR ASC(SUBSTR(str1, curr-i, 1)) = 206
            OR ASC(SUBSTR(str1, curr-i, 1)) = 207 THEN 
           str2 = str2 + "I".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 236 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 237
            OR ASC(SUBSTR(str1, curr-i, 1)) = 238
            OR ASC(SUBSTR(str1, curr-i, 1)) = 239 THEN 
           str2 = str2 + "i".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 210
            OR ASC(SUBSTR(str1, curr-i, 1)) = 211
            OR ASC(SUBSTR(str1, curr-i, 1)) = 212
            OR ASC(SUBSTR(str1, curr-i, 1)) = 213
            OR ASC(SUBSTR(str1, curr-i, 1)) = 214 THEN 
           str2 = str2 + "O".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 242
            OR ASC(SUBSTR(str1, curr-i, 1)) = 243
            OR ASC(SUBSTR(str1, curr-i, 1)) = 244
            OR ASC(SUBSTR(str1, curr-i, 1)) = 245
            OR ASC(SUBSTR(str1, curr-i, 1)) = 246 THEN 
           str2 = str2 + "o".
        ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 217 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 218
            OR ASC(SUBSTR(str1, curr-i, 1)) = 219
            OR ASC(SUBSTR(str1, curr-i, 1)) = 220 THEN 
           str2 = str2 + "U".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 249 
            OR ASC(SUBSTR(str1, curr-i, 1)) = 250
            OR ASC(SUBSTR(str1, curr-i, 1)) = 251
            OR ASC(SUBSTR(str1, curr-i, 1)) = 252 THEN 
           str2 = str2 + "u".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 209 THEN 
           str2 = str2 + "N".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 241 THEN 
           str2 = str2 + "n".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) = 160 THEN 
           str2 = str2 + " ".
       ELSE IF ASC(SUBSTR(str1, curr-i, 1)) GT 127 
           OR ASC(SUBSTR(str1,curr-i,1)) LT 32 THEN 
           str2 = str2 + "-".
       ELSE str2 = str2 + SUBSTR(str1, curr-i, 1).
    END.
END.
PROCEDURE calc-commissions :
DEFINE INPUT PARAMETER stay-date         AS DATE NO-UNDO.
DEFINE INPUT PARAMETER rsv-resno         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER rsv-reslinno      AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER rsv-argtNo 		 AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER rsv-rate 		 AS DECIMAL NO-UNDO.
DEFINE VARIABLE commission-amount        AS DECIMAL NO-UNDO.
	commission-amount = ROUND(((commission-dec / 100) * rsv-rate), 0).
	FIND FIRST argt-line WHERE argt-line.argtnr = rsv-argtNo 
		AND argt-line.argt-artnr = artnr-comm NO-LOCK NO-ERROR.
	IF AVAILABLE argt-line THEN DO:
      CREATE reslin-queasy.
	  ASSIGN
		reslin-queasy.KEY       = "fargt-line"
		reslin-queasy.number1   = argt-line.departement
		reslin-queasy.number2   = rsv-argtNo
		reslin-queasy.number3   = argt-line.argt-artnr
		reslin-queasy.resnr     = rsv-resno
		reslin-queasy.reslinnr  = rsv-reslinno
		reslin-queasy.deci1     = commission-amount
		reslin-queasy.deci2     = 0
		reslin-queasy.deci3     = 0
		reslin-queasy.date1     = stay-date
		reslin-queasy.date2     = stay-date
		.
	  FIND CURRENT reslin-queasy NO-LOCK.

	END.

END PROCEDURE.

