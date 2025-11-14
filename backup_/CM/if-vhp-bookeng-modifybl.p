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

DEFINE TEMP-TABLE detRes
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
    FIELD zikatnr   AS INTEGER
    FIELD firstname AS CHAR
    FIELD lastname  AS CHAR
    FIELD SELECTED  AS LOGICAL INIT NO.

DEFINE TEMP-TABLE tb-detRes LIKE detRes.

DEFINE TEMP-TABLE room-list1 LIKE room-list.

DEFINE INPUT PARAMETER TABLE FOR res-info.
DEFINE INPUT PARAMETER TABLE FOR room-list.
DEFINE INPUT PARAMETER TABLE FOR service-list.
DEFINE INPUT PARAMETER TABLE FOR guest-list.
DEFINE INPUT  PARAMETER BEcode          AS INT      NO-UNDO.
DEFINE INPUT  PARAMETER t-guest-nat     AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER t-curr-name     AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER dyna-code       AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter     AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter1    AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter2    AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER chDelimeter3    AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER error-str       AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER done            AS LOGICAL  NO-UNDO INIT NO.

DEFINE TEMP-TABLE t-resline LIKE res-line
    FIELD firstname AS CHAR
    FIELD lastname  AS CHAR
    FIELD uniq-id   AS CHAR
    FIELD typ       AS INT
    FIELD flag      AS LOGICAL INIT NO
    FIELD SELECTED  AS LOGICAL INIT NO.



DEFINE VARIABLE cm-gastno       AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE ota-gastnr      AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE check-integer   AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE asc-str         AS CHAR                 NO-UNDO.
DEFINE VARIABLE j               AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE i               AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE k               AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE cat-flag        AS LOGICAL INIT NO      NO-UNDO.
DEFINE VARIABLE counter         AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE gastnrmember    AS INTEGER INIT 1       NO-UNDO.
DEFINE VARIABLE rsegm           AS INTEGER              NO-UNDO.
DEFINE VARIABLE avalue          AS CHARACTER            NO-UNDO.
DEFINE VARIABLE del-mainres     AS LOGICAL              NO-UNDO.
DEFINE VARIABLE cancel-msg      AS CHARACTER            NO-UNDO.

DEFINE VARIABLE curr-resnr AS INTEGER       NO-UNDO INIT 0.
DEFINE VARIABLE curr-reslinnr AS INTEGER    NO-UNDO INIT 0.

DEFINE VARIABLE m AS INT.
DEFINE VARIABLE yy AS INT.
DEFINE VARIABLE dd AS INT.
DEFINE VARIABLE date-str AS CHAR INIT "".

/*NC - 21/06/22*/
DEFINE VARIABLE bill-date       AS DATE         NO-UNDO.
DEFINE VARIABLE upto-date       AS DATE         NO-UNDO.
DEFINE VARIABLE zikatnr 		AS INTEGER NO-UNDO.
DEFINE VARIABLE ifTask      	AS CHAR    NO-UNDO.
DEFINE VARIABLE rline-origcode  AS CHAR    NO-UNDO.

/*NC - 21/09/22 */
DEF VAR commission-str AS CHAR      NO-UNDO INIT "".    
DEF VAR commission-dec AS DECIMAL   NO-UNDO INIT 0.
DEF VAR dcommission    AS LOGICAL  NO-UNDO INITIAL NO. /*price OTA included commission or not*/
DEF VAR markup-str AS CHAR      NO-UNDO INIT "".    
DEF VAR markup-dec AS DECIMAL   NO-UNDO INIT 0.
DEF VAR artnr-comm	AS INTEGER   NO-UNDO INIT 0. /*artnr commission*/

DEFINE BUFFER qsy       FOR queasy.
DEFINE BUFFER rqueasy   FOR queasy.
DEFINE BUFFER bqueasy   FOR queasy.

DEFINE BUFFER rgast     FOR guest.
DEFINE BUFFER bres      FOR reservation.
/****************************************************************/
EMPTY TEMP-TABLE t-resline.
EMPTY TEMP-TABLE detRes.
EMPTY TEMP-TABLE tb-detRes.

FIND FIRST res-info NO-ERROR.

FIND FIRST queasy WHERE queasy.KEY = 159 AND queasy.number1 = beCode
    NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
    ASSIGN cm-gastno = queasy.number2.

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.

IF res-info.ota-code NE "" THEN
DO:
    FIND FIRST rgast WHERE rgast.karteityp GT 0
        AND TRIM(ENTRY(1, rgast.steuernr, "|")) MATCHES 
        TRIM(res-info.ota-code) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE rgast THEN     /*tidak ketemu guest dengan OTA code*/
    DO:
        FIND FIRST rgast WHERE rgast.gastnr = cm-gastno NO-LOCK NO-ERROR.
        IF AVAILABLE rgast THEN
            ota-gastnr = rgast.gastnr. /*Dialihkan ke GuestCard Booking Engine*/
        ELSE
        DO:        
            error-str = "GuestNo " + STRING(cm-gastno) + " not found".
            RETURN.
        END.
    END.
    ELSE ota-gastnr = rgast.gastnr. /*ketemu guest dengan OTA code*/
END.
ELSE
    ota-gastnr = cm-gastno.
	
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

FIND FIRST reservation WHERE reservation.gastnr = ota-gastnr 
    AND reservation.vesrdepot EQ res-info.res-id 
    AND reservation.activeflag = 0 NO-LOCK NO-ERROR. /*NC - 04/04/25*/
IF NOT AVAILABLE reservation THEN
	FIND FIRST reservation WHERE reservation.vesrdepot EQ  res-info.res-id 
    AND reservation.activeflag = 0 NO-LOCK NO-ERROR. /*NC - 04/04/25*/
IF NOT AVAILABLE reservation THEN
DO:
    error-str = "Reservation " + res-info.res-id + " not found".
	/*NC - 21/06/22 trigger to push availability*/
	FIND FIRST reservation WHERE reservation.vesrdepot = res-info.res-id NO-LOCK NO-ERROR.
	IF AVAILABLE reservation THEN
	DO:
		FOR EACH res-line WHERE res-line.resnr = reservation.resnr NO-LOCK :
			IF res-line.ankunft EQ res-line.abreise THEN upto-date = res-line.abreise.
			ELSE upto-date = res-line.abreise - 1.
			DO bill-date = res-line.ankunft TO upto-date :
				FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
				IF AVAILABLE zimkateg THEN
				DO:
					IF cat-flag THEN
						zikatnr = zimkateg.typ.
					ELSE
						zikatnr = zimkateg.zikatnr.
				END.
				
				rline-origcode = "".
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                    DO:
                        rline-origcode  = SUBSTR(iftask,11).
                        LEAVE.
                    END.
                END.

				FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
				  AND qsy.number1 = zikatnr AND qsy.char1 = rline-origcode NO-LOCK NO-ERROR.
				IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
				DO:
					FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
					IF AVAILABLE bqueasy THEN
					DO:
						bqueasy.logi2 = YES.
						FIND CURRENT bqueasy NO-LOCK.
						RELEASE bqueasy.
					END.
				END.
				
				FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
				  AND qsy.number1 = zikatnr AND qsy.char1 = "" NO-LOCK NO-ERROR.
				IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
				DO:
					FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
					IF AVAILABLE bqueasy THEN
					DO:
						bqueasy.logi2 = YES.
						FIND CURRENT bqueasy NO-LOCK.
						RELEASE bqueasy.
					END.
				END.
			END.
		END.
	END.
    RETURN.
END.

FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
        AND res-line.l-zuordnung[3] = 0 
        AND res-line.active-flag = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN
DO:
    error-str = "Reservation " + res-info.res-id + " not found. Expired Modify Date".
    RETURN.
END.

/*NC- 09/08/19*/
FIND FIRST bres WHERE bres.resnr = reservation.resnr EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE bres THEN
DO:
    bres.bemerk = res-info.remark.
    FIND CURRENT bres NO-LOCK.
    RELEASE bres.
END.  
ASSIGN
curr-resnr = reservation.resnr
.
FOR EACH res-line WHERE res-line.resnr = reservation.resnr 
    AND res-line.l-zuordnung[3] = 0 
    AND res-line.active-flag = 0 NO-LOCK:
    CREATE t-resline.
    BUFFER-COPY res-line TO t-resline NO-ERROR.
    ASSIGN
        t-resline.firstname = TRIM(ENTRY(2, t-resline.NAME, ","))
        t-resline.lastname  = TRIM(ENTRY(1, t-resline.NAME, ","))
        t-resline.uniq-id   = res-info.res-id
    .
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN
        t-resline.typ = zimkateg.typ.
END.


DO:
/*     ASSIGN 
        res-info.commission = "0"
        res-info.commission = ENTRY(2, rgast.steuernr, "|") 
        res-info.commission = REPLACE(res-info.commission, "%", "")
        NO-ERROR. */

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
    
END.


DEFINE VARIABLE loop-i AS INTEGER NO-UNDO.
DEFINE VARIABLE firstname AS CHARACTER NO-UNDO.
DEFINE VARIABLE lastname AS CHARACTER NO-UNDO.

loop-i = 0.
FOR EACH room-list:
	/*NC - 08/02/22*/
	IF room-list.ankunft LT TODAY OR room-list.abreise LT TODAY THEN
	DO:
		error-str = "Expired Modify Checkin / Checkout Date ".
		RETURN.
	END.
    loop-i = loop-i + 1.
    room-list.reslinnr = loop-i.

    CREATE detRes.
    BUFFER-COPY room-list TO detRes.

    detRes.reslinnr = loop-i.

    FIND FIRST guest-list WHERE guest-list.gastnr = room-list.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest-list THEN
        ASSIGN
            detRes.firstname = guest-list.given-name
            detRes.lastname  = guest-list.sure-name
            firstname        = guest-list.given-name
            lastname         = guest-list.sure-name.
    ELSE 
        ASSIGN
            detRes.firstname = res-info.given-name
            detRes.lastname  = res-info.sure-name
            firstname        = res-info.given-name
            lastname         = res-info.sure-name.


    IF cat-flag THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.char1 = room-list.room-type NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND FIRST t-resline WHERE t-resline.typ = queasy.number1 AND 
                NOT t-resline.flag AND t-resline.firstname = firstname AND t-resline.lastname = lastname NO-ERROR.
            IF NOT AVAILABLE t-resline THEN
                FIND FIRST t-resline WHERE t-resline.typ = queasy.number1 AND NOT t-resline.flag NO-ERROR.  
            IF AVAILABLE t-resline THEN
                ASSIGN
                    detRes.zikatnr = t-resline.zikatnr
                    t-resline.flag = YES.
                
            IF detRes.zikatnr = 0 THEN
            DO:
                FIND FIRST zimkateg WHERE zimkateg.typ = queasy.number1 NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN
                    detRes.zikatnr = zimkateg.zikatnr.
            END.
        END.
		ELSE DO: /*#C0F204 - 12/02/25*/ 
			error-str = error-str + CHR(10) + room-list.room-type  + "No such Room Category".
            RETURN.
		END.
    END.
    ELSE
    DO:
        FIND FIRST zimkateg WHERE zimkateg.kurzbez = room-list.room-type NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN
        DO:
            FIND FIRST t-resline WHERE t-resline.zikatnr = zimkateg.zikatnr AND 
                NOT t-resline.flag AND t-resline.firstname = firstname AND t-resline.lastname = lastname NO-ERROR.
            IF NOT AVAILABLE t-resline THEN
                FIND FIRST t-resline WHERE t-resline.zikatnr = zimkateg.zikatnr AND NOT t-resline.flag NO-ERROR.

            IF AVAILABLE t-resline THEN
                ASSIGN
                    t-resline.flag = YES
                    detRes.zikatnr = t-resline.zikatnr.
            
            IF detRes.zikatnr = 0 THEN
                detRes.zikatnr = zimkateg.zikatnr.
        END.
		ELSE DO: /*#C0F204 - 12/02/25*/
			error-str = error-str + CHR(10) + room-list.room-type  + "No such Room Category".
            RETURN.
		END.
    END.    
END.
    
FOR EACH t-resline WHERE t-resline.SELECTED = NO BY t-resline.reslinnr:
    FIND FIRST detRes WHERE detRes.firstname = t-resline.firstname 
        AND detRes.lastname = t-resline.lastname 
        AND detRes.zikatnr = t-resline.zikatnr 
		AND detRes.reslinnr = t-resline.reslinnr
        AND detRes.SELECTED = NO NO-ERROR.
    IF AVAILABLE detRes THEN
    DO: 
        FIND FIRST tb-detRes NO-ERROR.
        IF NOT AVAILABLE tb-detRes THEN CREATE tb-detRes.
        BUFFER-COPY detRes TO tb-detRes.
        ASSIGN
            t-resline.SELECTED = YES
            detRes.SELECTED    = YES
        .
        RUN modify-res(t-resline.resnr, t-resline.reslinnr).

        /* RVN 07/10/2025 Add Modify Reservation Flag for DataWarehouse*/
        RUN intevent-1.p(9, t-resline.zinr, "Priscilla", t-resline.resnr, t-resline.reslinnr).

    END.
END.     
   
EMPTY TEMP-TABLE tb-detRes.

FIND FIRST t-resline WHERE t-resline.SELECTED = NO NO-ERROR.
IF AVAILABLE t-resline THEN
FOR EACH t-resline WHERE t-resline.SELECTED = NO:
    FIND FIRST detRes WHERE detRes.zikatnr = t-resline.zikatnr 
		AND detRes.reslinnr = t-resline.reslinnr
        AND detRes.SELECTED = NO NO-ERROR.
    IF AVAILABLE detRes THEN
    DO: 
        FIND FIRST tb-detRes NO-ERROR.
        IF NOT AVAILABLE tb-detRes THEN CREATE tb-detRes.
        BUFFER-COPY detRes TO tb-detRes.
        ASSIGN
            t-resline.SELECTED = YES
            detRes.SELECTED    = YES
        .
        RUN modify-res(t-resline.resnr, t-resline.reslinnr).

        /* RVN 07/10/2025 Add Modify Reservation Flag for DataWarehouse*/
        RUN intevent-1.p(9, t-resline.zinr, "Priscilla", t-resline.resnr, t-resline.reslinnr).

    END.
END.

EMPTY TEMP-TABLE tb-detRes.

FIND FIRST t-resline WHERE t-resline.SELECTED = NO NO-ERROR.
IF AVAILABLE t-resline THEN
FOR EACH t-resline WHERE t-resline.SELECTED = NO:
    FIND FIRST detRes WHERE detRes.firstname = t-resline.firstname 
        AND detRes.lastname = t-resline.lastname 
		/* AND detRes.reslinnr = t-resline.reslinnr */ /*NC - 01/08/23 use reslinnr make wrong selected #7FAD9B*/
		AND detRes.zikatnr = t-resline.zikatnr 
        AND detRes.SELECTED = NO NO-ERROR.
    IF AVAILABLE detRes THEN
    DO: 
        FIND FIRST tb-detRes NO-ERROR.
        IF NOT AVAILABLE tb-detRes THEN CREATE tb-detRes.
        BUFFER-COPY detRes TO tb-detRes.
        ASSIGN
            t-resline.SELECTED = YES
            detRes.SELECTED    = YES
        .
        RUN modify-res(t-resline.resnr, t-resline.reslinnr).

        /* RVN 07/10/2025 Add Modify Reservation Flag for DataWarehouse*/
        RUN intevent-1.p(9, t-resline.zinr, "Priscilla", t-resline.resnr, t-resline.reslinnr).

    END.
END.

EMPTY TEMP-TABLE tb-detRes.

FIND FIRST t-resline WHERE t-resline.SELECTED = NO NO-ERROR.
IF AVAILABLE t-resline THEN
FOR EACH t-resline WHERE t-resline.SELECTED = NO:
    /*FIND FIRST detRes WHERE detRes.SELECTED = NO 
		AND detRes.reslinnr = t-resline.reslinnr NO-ERROR. */ /* NC 12/02/25 - reslinnr can not match in case splited reservation*/
	FIND FIRST detRes WHERE detRes.SELECTED = NO 
		AND ( detRes.zikatnr = t-resline.zikatnr OR detRes.reslinnr = t-resline.reslinnr ) NO-ERROR. /* NC 04/04/25 #D2493E */
    IF AVAILABLE detRes THEN
    DO: 	
        FIND FIRST tb-detRes NO-ERROR.
        IF NOT AVAILABLE tb-detRes THEN CREATE tb-detRes.
        BUFFER-COPY detRes TO tb-detRes.
        ASSIGN
            t-resline.SELECTED = YES
            detRes.SELECTED    = YES
        .
        RUN modify-res(t-resline.resnr, t-resline.reslinnr).

        /* RVN 07/10/2025 Add Modify Reservation Flag for DataWarehouse*/
        RUN intevent-1.p(9, t-resline.zinr, "Priscilla", t-resline.resnr, t-resline.reslinnr).

    END.
    ELSE /* detRes not available */
    DO:
        RUN del-reslinebl.p(1, "cancel", t-resline.resnr, t-resline.reslinnr, 
            "**", "BookEngine " + t-resline.uniq-id + " Modified - Cancelled RoomType", /*#BDA275*/ /*NC 04/04/25*/
            OUTPUT del-mainres, OUTPUT cancel-msg).
    END.
    
END.

FOR EACH res-line WHERE res-line.resnr = reservation.resnr NO-LOCK
    BY res-line.reslinnr DESCENDING:
    curr-reslinnr = res-line.reslinnr.
    LEAVE.
END.

/* the remaining detRes represent(s) new res-line to be insert */
FOR EACH detRes: 
    IF detRes.SELECTED = NO THEN DO:
        ASSIGN
            curr-reslinnr = curr-reslinnr + 1
            detRes.reslinnr = curr-reslinnr 
        .
        CREATE room-list1.
        BUFFER-COPY detRes TO room-list1. /*NC 04/04/25*/
    END.
    ELSE DELETE detRes.
END.

FIND FIRST res-info NO-ERROR.
RUN if-vhp-bookeng-store-resbl.p(TABLE res-info, TABLE room-list1, TABLE service-list,
                      TABLE guest-list,"insert", dyna-code, beCode, curr-resnr, chDelimeter, 
                      chDelimeter1, chDelimeter2, chDelimeter3,
                      t-guest-nat, t-curr-name, OUTPUT error-str, OUTPUT done).

done = YES.

PROCEDURE modify-res:
    DEF INPUT PARAMETER curr-resnr      AS INTEGER NO-UNDO.
    DEF INPUT PARAMETER curr-reslinnr   AS INTEGER NO-UNDO.
    
    DEF VARIABLE curr-i                 AS INTEGER NO-UNDO INIT 0.
    DEF VARIABLE accompany1             AS CHAR    NO-UNDO INIT "".
    DEF VARIABLE accompany2             AS CHAR    NO-UNDO INIT "".
    DEF VARIABLE accompany3             AS CHAR    NO-UNDO INIT "".
    
    RUN if-vhp-modify-reslinebl.p(curr-resnr, curr-reslinnr, t-curr-name, dyna-code,
    accompany1, accompany2, accompany3, 
    TABLE tb-detRes, TABLE res-info, TABLE service-list, dcommission, commission-dec, artnr-comm). /*NC - 21/09/22*/ 
      
END PROCEDURE.

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
