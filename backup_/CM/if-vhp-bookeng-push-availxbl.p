DEFINE TEMP-TABLE rmcat-list NO-UNDO
    FIELD zikatnr  AS INTEGER 
    FIELD anzahl   AS INTEGER 
    FIELD typ      AS INTEGER
    FIELD sleeping AS LOGICAL INITIAL YES
. 

DEFINE TEMP-TABLE r-list NO-UNDO
    FIELD rcode    AS CHAR
.

DEFINE TEMP-TABLE push-allot-list NO-UNDO
    FIELD startperiode AS DATE
    FIELD endperiode   AS DATE
    FIELD zikatnr      AS INT
    FIELD counter      AS INT
    FIELD rcode        AS CHAR
    FIELD bezeich      AS CHAR
    FIELD qty          AS INT
    FIELD flag         AS LOGICAL INIT YES
    FIELD str-date1    AS CHAR
    FIELD str-date2    AS CHAR
    FIELD minLOS       AS INT
    FIELD maxLOS       AS INT
    FIELD statnr       AS INT
    FIELD ota          AS CHAR
    FIELD bsetup       AS CHAR
    FIELD rmtype       AS CHAR
.

DEFINE BUFFER buff FOR push-allot-list.

DEFINE TEMP-TABLE q-list NO-UNDO
    FIELD rcode AS CHAR
    FIELD scode AS CHAR
    FIELD dcode AS CHAR
    FIELD zikatnr AS INT
    FIELD allot-flag AS LOGICAL INIT NO
.

DEFINE TEMP-TABLE change-room NO-UNDO
    FIELD datum AS DATE
    FIELD zikatnr AS INT
    FIELD occ     AS INT
.

DEF TEMP-TABLE temp-list NO-UNDO
    FIELD rcode  AS CHAR
    FIELD rmtype AS CHAR
    FIELD zikatnr AS INT
.

DEFINE TEMP-TABLE allotment NO-UNDO
    FIELD datum     AS DATE
    FIELD zikatnr   AS INT
    FIELD res-allot AS INT
    FIELD allot     AS INT
	FIELD ruecktage AS INT /*NC 20/04/23 used for cutdays*/
.

DEFINE TEMP-TABLE rmlist NO-UNDO
    FIELD typ AS INT
    FIELD rmcode AS CHAR
.

DEFINE INPUT  PARAMETER pushRate  AS LOGICAL.
DEFINE INPUT  PARAMETER inp-str   AS CHAR.
DEFINE INPUT  PARAMETER fdate     AS DATE.
DEFINE INPUT  PARAMETER tdate     AS DATE.
DEFINE INPUT  PARAMETER beCode    AS INTEGER.
DEFINE INPUT  PARAMETER TABLE FOR temp-list.
DEFINE OUTPUT PARAMETER done     AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR push-allot-list.
/* 
DEFINE VAR inp-str   AS CHAR INIT "no=no=yes".
DEFINE VARIABLE beCode AS INT INIT 1.
DEFINE VARIABLE fdate AS DATE INIT 07/01/17.
DEFINE VARIABLE tdate AS DATE INIT 07/01/17.
DEFINE VARIABLE done AS LOGICAL.
DEFINE VARIABLE pushRate  AS LOGICAL INIT YES.

*/
DEFINE VARIABLE curr-rate    AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-recid   AS INT NO-UNDO.
DEFINE VARIABLE curr-rcode   AS CHAR NO-UNDO.
DEFINE VARIABLE curr-bezeich AS CHAR NO-UNDO.
DEFINE VARIABLE curr-anz     AS INT NO-UNDO.

DEFINE VARIABLE starttime AS INT NO-UNDO.
starttime = TIME. 

DEFINE VARIABLE curr-date AS DATE NO-UNDO.          
DEFINE VARIABLE ankunft   AS DATE NO-UNDO.
DEFINE VARIABLE ci-date   AS DATE NO-UNDO.
DEFINE VARIABLE date-110   AS DATE NO-UNDO.
DEFINE VARIABLE datum     AS DATE NO-UNDO.

DEFINE VARIABLE tokcounter  AS INTEGER NO-UNDO.
DEFINE VARIABLE ifTask      AS CHAR    NO-UNDO.
DEFINE VARIABLE mesToken    AS CHAR    NO-UNDO.
DEFINE VARIABLE mesValue          AS CHAR    NO-UNDO.
DEFINE VARIABLE rline-origcode    AS CHAR    NO-UNDO.
DEFINE VARIABLE global-occ  AS LOGICAL NO-UNDO INIT NO.
                                     
DEFINE VARIABLE vhp-limited         AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE do-it               AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE zero-flag           AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE availbratecode      AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE cat-flag            AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE pushAll             AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE re-calculateRate    AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE change-allot        AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE all-room            AS LOGICAL INIT YES NO-UNDO. 
DEFINE VARIABLE allotment           AS LOGICAL INIT NO  NO-UNDO. 
DEFINE VARIABLE bedsetup            AS LOGICAL INIT NO  NO-UNDO. 
DEFINE VARIABLE avail-rmcat         AS LOGICAL INIT NO  NO-UNDO. 

DEFINE VARIABLE cm-gastno     AS INT INIT 0 NO-UNDO.  
DEFINE VARIABLE z-nr          AS INT INIT 0 NO-UNDO.  
DEFINE VARIABLE counter-avail AS INT INIT 0 NO-UNDO.    
DEFINE VARIABLE i             AS INT INIT 0 NO-UNDO.  
DEFINE VARIABLE occ-room      AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE push-quantity AS INT INIT 0 NO-UNDO.

DEFINE BUFFER bqueasy   FOR queasy.
DEFINE BUFFER q-curr    FOR queasy.
DEFINE BUFFER qsy       FOR queasy.
DEFINE BUFFER qsy159    FOR queasy.
DEFINE BUFFER qsy-allot FOR queasy.
DEFINE BUFFER qsy2      FOR queasy.
DEFINE BUFFER bratecode FOR ratecode.
DEFINE BUFFER bresline FOR res-line. /*12/12/23 NC - stuck when procedure calc avail*/

DEFINE VARIABLE end-date   AS DATE NO-UNDO.
DEFINE VARIABLE start-date AS DATE NO-UNDO.
DEFINE VARIABLE valid-date AS DATE NO-UNDO.

DEFINE VARIABLE catnr  AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE rm-occ AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE rm-ooo AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE rm-allot AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE res-allot AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE room   AS INT INIT 0 NO-UNDO.

DEFINE VARIABLE w-day               AS INTEGER  NO-UNDO.
DEFINE VARIABLE wd-array            AS INTEGER NO-UNDO EXTENT 8 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 
EMPTY TEMP-TABLE allotment.
ASSIGN
    done  = NO.

IF NUM-ENTRIES(inp-str,"=") GE 2 THEN
    ASSIGN
        pushAll          = LOGICAL(ENTRY(1,inp-str,"="))
        re-calculateRate = LOGICAL(ENTRY(2,inp-str,"="))
    .
IF NUM-ENTRIES(inp-str,"=") GE 3 THEN
    allotment        = LOGICAL(ENTRY(3,inp-str,"=")).
IF NUM-ENTRIES(inp-str,"=") GE 4 THEN
    bedSetup         = LOGICAL(ENTRY(4,inp-str,"=")).

/*night audit NC - 15/08/23 WHEN NA = yes but invoice date already change to TODAY still can push availability*/
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
ASSIGN date-110 = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 253 NO-LOCK NO-ERROR. 
IF htparam.flogic THEN
DO:
	IF date-110 LT TODAY THEN RETURN.
END.

FIND FIRST temp-list NO-LOCK NO-ERROR.
IF AVAILABLE temp-list THEN
    all-room = NO.

FIND FIRST queasy WHERE queasy.KEY = 159 AND queasy.number1 = beCode
    NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
DO:
    FIND FIRST guest WHERE guest.gastnr = queasy.number2 NO-LOCK NO-ERROR.
    FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest-pr THEN
    DO:
        cm-gastno = guest.gastnr.
    END.
    ELSE RETURN.
END.

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
DO:
    ASSIGN
        avail-rmcat = YES
        cat-flag = YES.

    FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK:
        CREATE rmlist.
        ASSIGN
            rmlist.typ = queasy.number1.
            rmlist.rmcode = queasy.char1.
    END.                                 
END.
FIND FIRST htparam WHERE htparam.paramnr = 439 NO-LOCK.
    global-occ = htparam.finteger = 1.
IF bedsetup = YES THEN cat-flag = NO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

IF fDate = ci-date THEN ankunft = ci-date.
ELSE ankunft = fDate + 2.

FOR EACH temp-list:
    IF cat-flag THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 152 
            AND queasy.char1 = temp-list.rmtype NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN temp-list.zikatnr = queasy.number1.
    END.  
    ELSE 
    DO:
        FIND FIRST zimkateg WHERE zimkateg.kurzbez = temp-list.rmtype
            AND zimkateg.kurzbez = temp-list.rmtype NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN temp-list.zikatnr = zimkateg.zikatnr.
    END.                                                             
END.

EMPTY TEMP-TABLE r-list.

IF NOT all-room THEN
    FOR EACH temp-list NO-LOCK:
        FIND FIRST r-list WHERE r-list.rcode = temp-list.rcode NO-LOCK NO-ERROR.
        IF NOT AVAILABLE r-list THEN
        DO:
            CREATE r-list.
            r-list.rcode = temp-list.rcode.
        END.
    END.
ELSE
    FOR EACH guest-pr WHERE guest-pr.gastnr = cm-gastno NO-LOCK:
        CREATE r-list.
        r-list.rcode = guest-pr.CODE.
    END.

RUN count-rmcateg.

DEFINE BUFFER kline FOR kontline.
/*NC - 07/09/23*/
DO TRANSACTION:
	FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.betriebsnr GT 0 NO-LOCK NO-ERROR.
	IF AVAILABLE queasy THEN DO:
		FOR EACH qsy159 WHERE qsy159.KEY = 159 AND qsy159.number2 EQ 0 NO-LOCK: /*NC - BE not active*/
			FIND FIRST q-curr WHERE q-curr.KEY = 171 AND q-curr.betriebsnr = qsy159.number1 NO-LOCK NO-ERROR.
			DO WHILE AVAILABLE q-curr:
				FIND FIRST qsy WHERE RECID(qsy) = RECID(q-curr) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
				IF AVAILABLE qsy THEN
				DO:
					DELETE qsy.
					RELEASE qsy.
				END.
				FIND NEXT q-curr WHERE q-curr.KEY = 171 AND q-curr.betriebsnr = qsy159.number1 NO-LOCK NO-ERROR.
			END.
		END.
		FIND FIRST q-curr WHERE q-curr.KEY = 171 AND q-curr.betriebsnr = 0 NO-LOCK NO-ERROR.
		DO WHILE AVAILABLE q-curr:
			FIND FIRST qsy WHERE RECID(qsy) = RECID(q-curr) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
			IF AVAILABLE qsy THEN
			DO:
				DELETE qsy.
				RELEASE qsy.
			END.
			FIND NEXT q-curr WHERE q-curr.KEY = 171 AND q-curr.betriebsnr = 0 NO-LOCK NO-ERROR.
		END.
	END.
	ELSE DO:
		FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.betriebsnr = 0 NO-LOCK NO-ERROR.
		DO WHILE AVAILABLE queasy:
			FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
			IF AVAILABLE qsy THEN
			DO:
				ASSIGN qsy.betriebsnr = beCode.
				FIND CURRENT qsy NO-LOCK.
				RELEASE qsy.
			END.
			FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.betriebsnr = 0 NO-LOCK NO-ERROR.
		END.
	END.
	
	FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.number3 GT 0 NO-LOCK NO-ERROR. /*#3CBF36*/
	DO WHILE AVAILABLE queasy :
		FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
		IF AVAILABLE qsy THEN
		DO:
			DELETE qsy.
			RELEASE qsy.
		END.
		FIND NEXT queasy WHERE queasy.KEY = 174 AND queasy.number3 GT 0 NO-LOCK NO-ERROR.
	END.
	
	FIND FIRST queasy WHERE queasy.KEY = 175 AND queasy.number3 GT 0 NO-LOCK NO-ERROR. /*#3CBF36*/
	DO WHILE AVAILABLE queasy :
		FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
		IF AVAILABLE qsy THEN
		DO:
			DELETE qsy.
			RELEASE qsy.
		END.
		FIND NEXT queasy WHERE queasy.KEY = 175 AND queasy.number3 GT 0 NO-LOCK NO-ERROR.
	END.
END.
DO TRANSACTION:
IF pushALL THEN
DO:
    /*NC - 31/03/21 enhance push all create queasy date based on contract rate setup*/
	FOR EACH temp-list NO-LOCK:
		IF cat-flag THEN
		DO:
			FIND FIRST zimkateg WHERE zimkateg.typ = temp-list.zikatnr NO-LOCK NO-ERROR.
			IF AVAILABLE zimkateg THEN
				ASSIGN z-nr = zimkateg.zikatnr.
		END.
		ELSE 
		DO:
			FIND FIRST zimkateg WHERE zimkateg.zikatnr = temp-list.zikatnr NO-LOCK NO-ERROR.
			IF AVAILABLE zimkateg THEN
				ASSIGN z-nr = zimkateg.zikatnr.
		END.
		ASSIGN valid-date = tdate.
		/*NC 26/06/23 add validation ratecode from temp-list*/
		FOR EACH bratecode WHERE bratecode.zikatnr = z-nr AND bratecode.CODE EQ temp-list.rcode
			AND bratecode.endperiode GE fdate NO-LOCK BY bratecode.endperiode DESC:

			IF bratecode.endperiode GT valid-date THEN
				ASSIGN
					valid-date = bratecode.endperiode.

			LEAVE.
		END.
	END.

    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 = "" AND queasy.betriebsnr = beCode EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
    REPEAT WHILE AVAILABLE queasy:
        /* FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE qsy THEN DO: */
			DELETE queasy.
			RELEASE queasy.	
        /* END.  */
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.char1 = "" AND queasy.betriebsnr = beCode EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
    END.
	
DO curr-date = fdate TO tdate: /*NC 26/06/23 add validation to date*/
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 NE "" AND queasy.date1 = curr-date AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE queasy:
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE qsy THEN DO: 
			ASSIGN
				qsy.number2 = 0
				qsy.logi1 = NO
				qsy.logi2 = NO
				qsy.logi3 = YES.
			FIND CURRENT qsy NO-LOCK.
			RELEASE qsy.
         END.
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.char1 NE "" AND queasy.date1 = curr-date AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    END.
END.
    
    /*IF NOT pushRate THEN
        RUN update-bookengine-configbl.p (8,beCode,NO,"").*/

/*    IF allotment THEN
    DO: /*NC - 31/08/21 enhanced  kontline.betriebsnr = 1 -> global reservation*/
        FOR EACH res-line WHERE res-line.active-flag LE 1 
            AND res-line.resstatus LE 6 /* AND res-line.resstatus NE 3 */
            AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
            AND res-line.resstatus NE 11 AND res-line.resstatus NE 13
            AND res-line.kontignr GT 0 AND res-line.l-zuordnung[3] = 0
            AND res-line.ankunft LE valid-date
            AND res-line.abreise GE fdate
            AND res-line.kontignr GT 0 NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK:

            IF res-line.ankunft = res-line.abreise THEN end-date = res-line.abreise.
            ELSE end-date = res-line.abreise - 1.

            IF cat-flag THEN catnr = zimkateg.typ.
            ELSE catnr = zimkateg.zikatnr. 

            IF res-line.ankunft LE fdate THEN
                start-date = fdate.
            ELSE start-date = res-line.ankunft.

            IF end-date GE valid-date THEN
                end-date = valid-date.

            DO datum = start-date TO end-date:
                FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
                    AND kline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kline THEN
				DO:
					IF allotment THEN
						FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
							AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
					ELSE /*GLOBAL RESERVATION*/
						FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
							AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
						
				END.
                IF AVAILABLE kontline THEN
                DO:
                    FIND FIRST allotment WHERE allotment.zikatnr = catnr AND 
                        allotment.datum = datum NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE allotment THEN
                    DO:
                        CREATE allotment.
                        ASSIGN
                            allotment.zikatnr = catnr
                            allotment.datum = datum
                            allotment.res-allot = res-line.zimmeranz
                        . 
                    END.
                    ELSE allotment.res-allot = allotment.res-allot + res-line.zimmeranz.
                END.                                                                    
            END.                                                                        
        END. */  /*10/04/23 NC - efisien process #EA91AC*/
        
        FOR EACH kontline WHERE kontline.kontstat = 1 
            AND kontline.ankunft LE valid-date AND kontline.abreise GE fdate,
            FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK:
						
			IF allotment AND kontline.betriebsnr = 0 THEN 
				do-it = YES.
			ELSE IF NOT allotment AND kontline.betriebsnr = 1 THEN /*GLOBAL RESERVATION*/
				do-it = YES.
			IF do-it THEN
			DO:
				IF cat-flag THEN catnr = zimkateg.typ.
				ELSE catnr = zimkateg.zikatnr. 

				IF kontline.ankunft LE fdate THEN
					start-date = fdate.
				ELSE start-date = kontline.ankunft.

				IF kontline.abreise GT valid-date THEN 
					end-date = valid-date.
				ELSE end-date = kontline.abreise. 
				
				DO datum = start-date TO end-date:
					FIND FIRST allotment WHERE allotment.zikatnr = catnr AND 
						allotment.datum = datum NO-LOCK NO-ERROR.
					IF NOT AVAILABLE allotment THEN
					DO:
						CREATE allotment.
						ASSIGN
							allotment.zikatnr = catnr
							allotment.datum = datum
							allotment.allot = kontline.zimmeranz
							allotment.ruecktage = kontline.ruecktage
						. 
					END.
					ELSE allotment.allot = allotment.allot + kontline.zimmeranz.
				END.
			END.
			do-it = NO.
        END.
/*    END.*/
    
    DO curr-date = fdate TO valid-date:
        FOR EACH rmcat-list NO-LOCK:
            CREATE queasy.
            ASSIGN
                queasy.KEY = 171
                queasy.number1 = rmcat-list.zikatnr
                queasy.date1 = curr-date
                queasy.logi1 = NO
                queasy.logi2 = NO
                queasy.logi3 = NO
                queasy.char1 = ""
				queasy.betriebsnr   = beCode
            .
            FIND FIRST allotment WHERE allotment.datum = curr-date AND allotment.zikatnr = rmcat-list.zikatnr NO-LOCK NO-ERROR.
            IF AVAILABLE allotment AND curr-date GE (ci-date + allotment.ruecktage) THEN
                queasy.number2 = allotment.allot. /* - allotment.res-allot */ /*NC- 10/04/23 allotment global reservation move down #EA91AC*/ 
        END.
    END.                                 

    FOR EACH outorder WHERE outorder.betriebsnr LE 1 AND (outorder.gespstart GE fdate
        OR outorder.gespende GE fdate) NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping = YES NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK:

        IF cat-flag THEN catnr = zimkateg.typ.
        ELSE catnr = zimkateg.zikatnr.        
        
        DO datum = outorder.gespstart TO outorder.gespende:
            FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.number1 = catnr 
                AND queasy.date1 = datum AND queasy.char1 = "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN 
            DO:
                FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                IF AVAILABLE qsy THEN
                DO:
                    ASSIGN qsy.number3 = qsy.number3 + 1.
                    FIND CURRENT qsy NO-LOCK.
                    RELEASE qsy.
                END.
            END.
        END.
    END.
    /*count-availability*/
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 /* AND res-line.resstatus NE 3 */
        AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 11 AND res-line.resstatus NE 13
        AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0
        AND res-line.ankunft LE valid-date
        AND res-line.abreise GE fdate NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK:

        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
            do-it = zimmer.sleeping. 
        END. 

        IF do-it AND vhp-limited THEN
        DO:
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                NO-LOCK NO-ERROR.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.       

        IF do-it THEN
        DO:
			
            IF res-line.ankunft = res-line.abreise THEN end-date = res-line.abreise.
            ELSE end-date = res-line.abreise - 1.

            IF cat-flag THEN catnr = zimkateg.typ.
            ELSE catnr = zimkateg.zikatnr. 

            IF res-line.ankunft LE fdate THEN
                start-date = fdate.
            ELSE start-date = res-line.ankunft.

            IF end-date GE valid-date THEN
                end-date = valid-date.

            DO datum = start-date TO end-date:
				res-allot = 0.
				IF res-line.kontignr GT 0 THEN /*#EA91AC*/
				DO:
					FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
						AND kline.kontstat = 1 NO-LOCK NO-ERROR.
					IF AVAILABLE kline THEN
					DO:
						IF allotment AND datum GE (ci-date + kontline.ruecktage) THEN
						FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
							AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
						ELSE /*GLOBAL RESERVATION*/
						FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
							AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
						IF AVAILABLE kontline THEN
							ASSIGN res-allot = res-line.zimmeranz.
					END.
				END.
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.number1 = catnr 
                    AND queasy.date1 = datum AND queasy.char1 = "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN 
                DO:
					 
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
						
                        ASSIGN qsy.number2 = qsy.number2 + res-line.zimmeranz - res-allot. /*rm-occ*/
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.
                END.            
            END.

            IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
            DO:
                rline-origcode = "".
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                    DO:
                        rline-origcode  = SUBSTR(iftask,11).
                        LEAVE.
                    END.
                END.

                IF rline-origcode NE "" THEN
                DO datum = start-date TO end-date:
                    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                        AND queasy.number1 = catnr AND queasy.char1 = rline-origcode AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN 
                    DO:
                        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                        IF AVAILABLE qsy THEN
                        DO:
                            ASSIGN qsy.number2 = qsy.number2 + res-line.zimmeranz.
                            FIND CURRENT qsy NO-LOCK.
                            RELEASE qsy.
                        END.
                    END. 
                END.
            END.
        END.
    END.
    /*NC - 31/03/21 push all data based on periode BE setup */
	DO curr-date = fdate TO tdate:
		FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date AND queasy.betriebsnr = beCode EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        REPEAT WHILE AVAILABLE queasy:
			/* FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
			IF AVAILABLE qsy THEN
			DO: */
				ASSIGN queasy.logi3 = YES.
				FIND CURRENT queasy NO-LOCK.
				RELEASE queasy.
			/* END. */
            FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date AND queasy.betriebsnr = beCode EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
		END.
	END.
END.
END. /* end transaction*/
DO TRANSACTION:
IF NOT pushALL THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 LT fdate - 2 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE queasy:
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE qsy THEN
        DO:
            DELETE qsy.
			RELEASE qsy.
        END. 
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 LT fdate - 2 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    END.

    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.logi2 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE queasy:

            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN
            DO:
                ASSIGN
                    qsy.logi1 = qsy.logi2
                    qsy.logi2 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.
            END.
           
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.logi2 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR. 
    END.

    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.logi1 AND queasy.char1 = "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE queasy:
        ASSIGN
            rm-occ = 0
            rm-ooo = 0
            rm-allot = 0.
        RUN count-availability (queasy.date1,queasy.number1,OUTPUT rm-occ, OUTPUT rm-ooo, OUTPUT rm-allot).

        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE qsy THEN
        DO:
            ASSIGN
                qsy.number3 = rm-ooo
                qsy.logi1   = NO
                qsy.logi3   = YES
            .
			
            IF allotment THEN
                qsy.number2 = rm-occ + rm-allot.
            ELSE qsy.number2 = rm-occ.

            FIND CURRENT qsy NO-LOCK.
            RELEASE qsy.
        END.

        IF pushRate THEN
        DO:
            FOR EACH r-list NO-LOCK: /*19/10/2020 - NC proces flag only mapped ratecode*/
				/*28/11/2018 - NC penambahan Global-occ push rate*/
				IF global-occ THEN
				DO:
					FIND FIRST bqueasy WHERE bqueasy.KEY = 170 
					AND bqueasy.date1 = queasy.date1	
					AND bqueasy.char1 = r-list.rcode 
					AND bqueasy.logi1 = NO AND bqueasy.logi2 = NO AND bqueasy.betriebsnr = beCode NO-LOCK NO-ERROR. /*exclude Room Type*/
					REPEAT WHILE AVAILABLE bqueasy:
						FIND FIRST qsy2 WHERE qsy2.KEY = 2 AND qsy2.char1 = bqueasy.char1 AND qsy2.logi2 NO-LOCK NO-ERROR.
						IF AVAILABLE qsy2 THEN
						DO:
							FIND FIRST qsy WHERE RECID(qsy) = RECID(bqueasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
							IF AVAILABLE qsy THEN
							DO:
								ASSIGN 
									qsy.logi1 = YES
									qsy.logi2 = NO.
								FIND CURRENT qsy NO-LOCK.
								RELEASE qsy.
							END.
						END.
						FIND NEXT bqueasy WHERE bqueasy.KEY = 170 
						AND bqueasy.date1 = queasy.date1 
						AND bqueasy.char1 = r-list.rcode
						AND bqueasy.logi1 = NO AND bqueasy.logi2 = NO AND bqueasy.betriebsnr = beCode NO-LOCK NO-ERROR.
					END.
				END.
				ELSE
				DO:
					FIND FIRST bqueasy WHERE bqueasy.KEY = 170 
					AND bqueasy.date1 = queasy.date1 
					AND bqueasy.number1 = queasy.number1
					AND bqueasy.char1 = r-list.rcode
					AND bqueasy.logi1 = NO AND bqueasy.logi2 = NO AND bqueasy.betriebsnr = beCode NO-LOCK NO-ERROR.
					REPEAT WHILE AVAILABLE bqueasy:
						FIND FIRST qsy2 WHERE qsy2.KEY = 2 AND qsy2.char1 = bqueasy.char1 AND qsy2.logi2 NO-LOCK NO-ERROR.
						IF AVAILABLE qsy2 THEN
						DO:
							FIND FIRST qsy WHERE RECID(qsy) = RECID(bqueasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
							IF AVAILABLE qsy THEN
							DO:
								ASSIGN 
									qsy.logi1 = YES
									qsy.logi2 = NO.
								FIND CURRENT qsy NO-LOCK.
								RELEASE qsy.
							END.
						END.
						FIND NEXT bqueasy WHERE bqueasy.KEY = 170 
						AND bqueasy.date1 = queasy.date1 
						AND bqueasy.number1 = queasy.number1
						AND bqueasy.char1 = r-list.rcode
						AND bqueasy.logi1 = NO AND bqueasy.logi2 = NO AND bqueasy.betriebsnr = beCode NO-LOCK NO-ERROR.
					END.
				END.
			END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.logi1 AND queasy.char1 = "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    END.
    
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 NE "" AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        /*FIND FIRST q-list WHERE q-list.dcode = queasy.char1 AND q-list.zikatnr = queasy.number1 
            AND q-list.allot-flag NO-LOCK NO-ERROR.
        IF AVAILABLE q-list THEN
        DO: */
            occ-room = 0.
            IF cat-flag THEN
                FOR EACH res-line WHERE res-line.active-flag LE 1 
                    AND res-line.resstatus LE 6 /* AND res-line.resstatus NE 3 */
                    AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
                    AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND res-line.ankunft LE queasy.date1 AND res-line.abreise GT queasy.date1
                    AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 
                    AND res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") NO-LOCK,
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.typ = queasy.number1 NO-LOCK: 
                    do-it = YES. 
                    IF res-line.zinr NE "" THEN 
                    DO: 
                        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                        do-it = zimmer.sleeping. 
                    END. 
            
                    IF do-it AND vhp-limited THEN
                    DO:
                        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                            NO-LOCK.
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                            NO-LOCK NO-ERROR.
                        do-it = AVAILABLE segment AND segment.vip-level = 0.
                    END.
            
                    IF do-it THEN 
                    DO:
                        rline-origcode = "".
                        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                            iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                            IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                            DO:
                                rline-origcode  = SUBSTR(iftask,11).
                                LEAVE.
                            END.
                        END.  
                        IF rline-origcode = queasy.char1 THEN occ-room = occ-room + res-line.zimmeranz.
                    END.
                END. /*end for each res-line if cat-flag*/ 
            ELSE
                FOR EACH res-line WHERE res-line.active-flag LE 1 
                    AND res-line.resstatus LE 6 /* AND res-line.resstatus NE 3 */
                    AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
                    AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND res-line.ankunft LE queasy.date1 AND res-line.abreise GT queasy.date1
                    AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 
                    AND res-line.zimmer-wunsch MATCHES ("*$OrigCode$*")
                    AND res-line.zikatnr = queasy.number1 NO-LOCK:
                    
                    do-it = YES. 
                    IF res-line.zinr NE "" THEN 
                    DO: 
                        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                        do-it = zimmer.sleeping. 
                    END. 
            
                    IF do-it AND vhp-limited THEN
                    DO:
                        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                            NO-LOCK.
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                            NO-LOCK NO-ERROR.
                        do-it = AVAILABLE segment AND segment.vip-level = 0.
                    END.
            
                    IF do-it THEN 
                    DO:
                        rline-origcode = "".
                        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                            iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                            IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                            DO:
                                rline-origcode  = SUBSTR(iftask,11).
                                LEAVE.
                            END.
                        END.

                        IF rline-origcode = queasy.char1 THEN occ-room = occ-room + res-line.zimmeranz.
                    END.
                END. /*end for each res-line not cat flag*/ 

            IF cat-flag THEN FIND FIRST zimkateg WHERE zimkateg.typ = queasy.number1 NO-LOCK NO-ERROR.
            ELSE FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.

            /*ASSIGN w-day = wd-array[WEEKDAY(curr-date)]. 
            FIND FIRST ratecode WHERE ratecode.startperiode LE queasy.date1 AND ratecode.endperiode GE queasy.date1 AND 
                ratecode.zikatnr = zimkateg.zikatnr AND ratecode.CODE = q-list.scode AND ratecode.num1[1] NE 0 AND 
                ratecode.wday = w-day NO-LOCK NO-ERROR.
            IF NOT AVAILABLE ratecode THEN
                FIND FIRST ratecode WHERE ratecode.startperiode LE queasy.date1 AND ratecode.endperiode GE queasy.date1 AND 
                    ratecode.zikatnr = zimkateg.zikatnr AND ratecode.CODE = q-list.scode AND ratecode.num1[1] NE 0 AND 
                    ratecode.wday = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE ratecode THEN
            DO:*/
                IF queasy.number2 NE occ-room THEN
                DO:
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
                        ASSIGN 
                            qsy.number2 = occ-room
                            qsy.logi1   = NO
                            qsy.logi2   = NO
                            qsy.logi3   = YES.
                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.
                END.    
           /*  END. */
        /* END. */
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.char1 NE "" AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    END.

    IF tdate NE ? THEN 	/*untuk todate jika blm terbentuk*/
    DO:
		FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = tdate AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            FOR EACH rmcat-list NO-LOCK:
                RUN count-availability (tdate,rmcat-list.zikatnr,OUTPUT rm-occ, OUTPUT rm-ooo, OUTPUT rm-allot).
                CREATE queasy.
                ASSIGN
                    queasy.KEY = 171
                    queasy.number1 = rmcat-list.zikatnr
                    queasy.number3 = rm-ooo
                    queasy.date1 = tdate
                    queasy.logi1 = NO
                    queasy.logi2 = NO
                    queasy.logi3 = YES
                    queasy.char1 = ""
					queasy.betriebsnr   = beCode
                .
				
                IF allotment THEN
                    queasy.number2 = rm-occ + rm-allot.
                ELSE queasy.number2 = rm-occ.
            END.
        END.
    END.
	/*IF allotment THEN NC 20/04/23 - release allotment after cutdays; 19/04/24 planning move to Night Audit proses
	DO:
		FIND FIRST kontline WHERE kontline.kontstat = 1 
			AND kontline.betriebsnr = 0 NO-LOCK NO-ERROR.
		DO WHILE AVAILABLE kontline :
			IF ci-date GT (kontline.ankunft - kontline.ruecktage) AND (ci-date + (kontline.ruecktage - 1)) LE kontline.abreise THEN
			DO:
				FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK NO-ERROR.
				IF AVAILABLE zimkateg THEN
				DO:
					IF cat-flag THEN catnr = zimkateg.typ.
					ELSE catnr = zimkateg.zikatnr.
				END.
				
				FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 =  (ci-date + (kontline.ruecktage - 1)) AND queasy.number1 = catnr AND queasy.char1 = "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
				IF AVAILABLE queasy THEN
				DO:
					ASSIGN
					rm-occ = 0
					rm-ooo = 0
					rm-allot = 0.
					RUN count-availability (queasy.date1,queasy.number1,OUTPUT rm-occ, OUTPUT rm-ooo, OUTPUT rm-allot).
					rm-occ = rm-occ + rm-allot.
					IF queasy.number2 NE rm-occ THEN
					DO:
						FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
						IF AVAILABLE qsy THEN
						DO:
							ASSIGN
								qsy.number2 = rm-occ
								qsy.number3 = rm-ooo
								qsy.logi3 = YES
								.
							FIND CURRENT qsy NO-LOCK.
							RELEASE qsy.
						END.
					END.
				END.
			END.
			FIND NEXT kontline WHERE kontline.kontstat = 1 AND kontline.betriebsnr = 0 NO-LOCK NO-ERROR.
		END.
		
	END.*/
END.
END. /*end transaction*/
/*
IF change-allot THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 171 AND NOT queasy.logi3 AND queasy.char1 = "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN
            queasy.logi1 = NO
            queasy.logi3 = YES.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
        FIND NEXT queasy WHERE queasy.KEY = 171 AND NOT queasy.logi3 AND queasy.char1 = "" NO-LOCK NO-ERROR.
    END.
END.*/

DEF VAR statnr AS INT INIT 0.
DEF BUFFER rqsy FOR queasy.
DEF BUFFER da-qsy FOR queasy.    
DO TRANSACTION:
FOR EACH queasy WHERE queasy.KEY = 171 AND queasy.char1 = "" AND queasy.logi3 AND queasy.betriebsnr = beCode NO-LOCK:
    FIND FIRST bqueasy WHERE bqueasy.KEY = 171 AND bqueasy.betriebsnr = beCode AND bqueasy.char1 NE "" AND bqueasy.date1 = queasy.date1 
        AND bqueasy.number1 = queasy.number1 AND NOT bqueasy.logi3 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE bqueasy:
        FIND CURRENT bqueasy EXCLUSIVE-LOCK.
        bqueasy.logi3 = YES.
        FIND CURRENT bqueasy NO-LOCK.
        RELEASE bqueasy.
		
        FIND NEXT bqueasy WHERE bqueasy.KEY = 171 AND bqueasy.betriebsnr = beCode AND bqueasy.char1 NE "" AND bqueasy.date1 = queasy.date1 
            AND bqueasy.number1 = queasy.number1 AND NOT bqueasy.logi3 NO-LOCK NO-ERROR.
    END.
END.
END. /*end transaction*/
FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.logi3 AND queasy.char1 = "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy:
    FOR EACH r-list NO-LOCK:
        FIND FIRST qsy-allot WHERE qsy-allot.KEY = 171 AND qsy-allot.char1 = r-list.rcode AND qsy-allot.date1 = queasy.date1 AND qsy-allot.betriebsnr = beCode 
            AND qsy-allot.number1 = queasy.number1 AND qsy-allot.number3 NE 0 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE qsy-allot THEN
        DO:
            FIND FIRST qsy2 WHERE qsy2.KEY = 2 AND qsy2.char1 = r-list.rcode NO-LOCK NO-ERROR.
            IF AVAILABLE qsy2 THEN
            DO:
                statnr = 0.
                curr-anz = 0.
                /*
                IF queasy.date1 GE qsy2.date1 AND queasy.date1 LE qsy2.date2 AND qsy2.date1 NE ? AND qsy2.date2 NE ? THEN.
                ELSE IF queasy.date1 GE qsy2.date1 AND qsy2.date1 NE ? AND qsy2.date2 = ? THEN.
                ELSE IF queasy.date1 LE qsy2.date2 AND qsy2.date1 = ? AND qsy2.date2 NE ? THEN.
                ELSE IF qsy2.date1 = ? AND qsy2.date2 = ? THEN.
                ELSE statnr = 1.

                FIND FIRST rqsy WHERE rqsy.KEY = 174 AND rqsy.char1 = r-list.rcode AND rqsy.number2 = YEAR(queasy.date1)
                    AND rqsy.number1 = queasy.number1 NO-LOCK NO-ERROR.
                IF AVAILABLE rqsy THEN
                DO:
                    RUN find-date(queasy.date1, OUTPUT curr-anz).
                    IF statnr = 0 THEN
                        statnr = INT(ENTRY(curr-anz,rqsy.char2,";")).
                END.
                */

                FIND FIRST rqsy WHERE rqsy.KEY = 174 AND rqsy.char1 = r-list.rcode
                    AND rqsy.date1 EQ queasy.date1
                    AND rqsy.number1 = queasy.number1 NO-LOCK NO-ERROR.

                IF AVAILABLE rqsy THEN
                DO:            
                    IF INT(ENTRY(1,rqsy.char2,";")) EQ 1 THEN
                    DO:
                        statnr = 1. /*CLOSE*/
                    END.
                    ELSE IF INT(ENTRY(2,rqsy.char2,";")) EQ 1 AND INT(ENTRY(3,rqsy.char2,";")) EQ 0 THEN
                    DO:
                        statnr = 2. /*CTA*/         
                    END.
                    ELSE IF INT(ENTRY(3,rqsy.char2,";")) EQ 1 AND INT(ENTRY(2,rqsy.char2,";")) EQ 0 THEN
                    DO:
                        statnr = 3. /*CTD*/
                    END.
					ELSE IF INT(ENTRY(2,rqsy.char2,";")) EQ 1 AND INT(ENTRY(3,rqsy.char2,";")) EQ 1 THEN
                    DO:
                        statnr = 4. /*CTAD*/
                    END.
                END.
				/*Check where is Open status came from*/
                FIND FIRST rqsy WHERE rqsy.KEY = 175 AND rqsy.char1 = r-list.rcode
                    AND rqsy.date1 EQ queasy.date1
                    AND rqsy.number1 = queasy.number1 NO-LOCK NO-ERROR.
				IF AVAILABLE rqsy THEN
                DO:
					IF rqsy.char2 EQ "CLOSE" AND rqsy.number2 = 0 THEN
					DO:
						statnr = 0. /*Open*/
					END.
					IF rqsy.char2 EQ "CTA" AND rqsy.number2 = 0 THEN
					DO:
						statnr = 5. /*Open CTA*/
					END.
					IF rqsy.char2 EQ "CTD" AND rqsy.number2 = 0 THEN
					DO:
						statnr = 6. /*Open CTD*/
					END.
					
					IF rqsy.char2 EQ "CLOSE" AND rqsy.number2 = 1 THEN
					DO:
						statnr = 1. /*Close*/
					END.
					IF rqsy.char2 EQ "CTA" AND rqsy.number2 = 1 THEN
					DO:
						statnr = 2. /*CTA*/
					END.
					IF rqsy.char2 EQ "CTD" AND rqsy.number2 = 1 THEN
					DO:
						statnr = 3. /*CTD*/
					END.
				END.

                counter-avail = counter-avail + 1.
                CREATE push-allot-list.
                ASSIGN
                    push-allot-list.startperiode = queasy.date1
                    push-allot-list.endperiode   = queasy.date1
                    push-allot-list.rcode        = r-list.rcode
                    push-allot-list.zikatnr      = queasy.number1
                    push-allot-list.counter      = counter-avail
                    push-allot-list.minLOS       = qsy2.number2
                    push-allot-list.maxLOS       = qsy2.deci2
                    push-allot-list.statnr       = statnr.
                .
				/* NC-06/12/23 qty must same as pms
                IF statnr = 1 THEN push-allot-list.qty = 0.
                ELSE
                DO:
				*/
                    FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                    push-allot-list.qty = rmcat-list.anzahl - queasy.number2 - queasy.number3.
                   /* push-quantity = push-allot-list.qty. NC - Not used*/

                    /*IF push-allot-list.qty NE 0 THEN
                    DO:
                        FIND FIRST da-qsy WHERE da-qsy.KEY = 178 AND da-qsy.number1 = queasy.number1 AND da-qsy.date1 = queasy.date1 NO-LOCK NO-ERROR.
                        IF AVAILABLE da-qsy THEN
                            push-allot-list.qty = TRUNCATE(da-qsy.deci1 / 100 * push-allot-list.qty,0).
                        ELSE
                        DO:
                            FOR EACH allot-list BY allot-list.qty DESC:
                                do-it = NO.
                                IF push-allot-list.qty LE allot-list.qty THEN
                                DO:
                                    IF SUBSTR(allot-list.rmtype,1,1) = "*" THEN do-it = YES.
                                    ELSE
                                    DO i = 1 TO NUM-ENTRIES(allot-list.rmtype,","):
                                        IF ENTRY(i,allot-list.rmtype,",") = push-allot-list.bezeich THEN do-it = YES.
                                        IF do-it THEN LEAVE.
                                    END.
                                    IF do-it THEN
                                    DO:
                                        push-allot-list.qty = TRUNCATE(allot-list.percentage / 100 * push-allot-list.qty,0).
                                        LEAVE.  
                                    END.
                                END.    
                            END.
                        END.    
                    END. */
                /* END. */
                    
                IF cat-flag THEN
                DO:
                    FIND FIRST qsy WHERE qsy.KEY = 152 AND qsy.number1 = queasy.number1 NO-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN 
                        ASSIGN
                            push-allot-list.bezeich = qsy.char1
                            push-allot-list.rmtype  = qsy.char1
                        .
                END.
                ELSE IF NOT bedsetup AND NOT avail-rmcat THEN
                DO:
                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN 
                        ASSIGN
                            push-allot-list.bezeich = zimkateg.kurzbez
                            push-allot-list.rmtype  = zimkateg.kurzbez.
                END.
                ELSE IF bedsetup AND avail-rmcat THEN
                DO:
                    FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                    IF AVAILABLE rmcat-list THEN
                    DO:
                        FIND FIRST rmlist WHERE rmlist.typ = rmcat-list.typ NO-LOCK NO-ERROR.
                        IF AVAILABLE rmlist THEN push-allot-list.bezeich = rmlist.rmcode.
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN push-allot-list.rmtype = zimkateg.kurzbez.
                        FIND FIRST zimmer WHERE zimmer.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                        IF AVAILABLE zimmer THEN
                        DO:
                            FIND FIRST paramtext WHERE paramtext.txtnr = 9200 + zimmer.setup NO-LOCK NO-ERROR.
                            IF AVAILABLE paramtext THEN
                                push-allot-list.bsetup = paramtext.ptexte.
                        END.   
                    END. 
                END.
                ELSE IF bedsetup AND NOT avail-rmcat THEN
                DO:
                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN 
                        ASSIGN
                            push-allot-list.bezeich = zimkateg.kurzbez
                            push-allot-list.rmtype = zimkateg.kurzbez
                        .

                    FIND FIRST zimmer WHERE zimmer.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                    IF AVAILABLE zimmer THEN
                    DO:
                        FIND FIRST paramtext WHERE paramtext.txtnr = 9200 + zimmer.setup NO-LOCK NO-ERROR.
                        IF AVAILABLE paramtext THEN
                            push-allot-list.bsetup = paramtext.ptexte.
                    END.   
                END.
            END.
        END.
    END.
	
    FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.logi3 AND queasy.char1 = "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
END.

FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.logi3 AND queasy.char1 NE "" AND queasy.betriebsnr = beCode  NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy:
    FIND FIRST qsy2 WHERE qsy2.KEY = 2 AND qsy2.char1 = queasy.char1 NO-LOCK NO-ERROR.
    IF AVAILABLE qsy2 THEN
    DO:
        statnr = 0.
        curr-anz = 0.
        /*
        IF queasy.date1 GE qsy2.date1 AND queasy.date1 LE qsy2.date2 AND qsy2.date1 NE ? AND qsy2.date2 NE ? THEN.
        ELSE IF queasy.date1 GE qsy2.date1 AND qsy2.date1 NE ? AND qsy2.date2 = ? THEN.
        ELSE IF queasy.date1 LE qsy2.date2 AND qsy2.date1 = ? AND qsy2.date2 NE ? THEN.
        ELSE IF qsy2.date1 = ? AND qsy2.date2 = ? THEN.
        ELSE statnr = 1.

        FIND FIRST rqsy WHERE rqsy.KEY = 174 AND rqsy.char1 = queasy.char1 AND rqsy.number2 = YEAR(queasy.date1)
            AND rqsy.number1 = queasy.number1 AND rqsy.number3 = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE rqsy THEN
        DO:
            RUN find-date(queasy.date1, OUTPUT curr-anz).
            IF statnr = 0 THEN
                statnr = INT(ENTRY(curr-anz,rqsy.char2,";")).
        END.
        */

        FIND FIRST rqsy WHERE rqsy.KEY = 174 AND rqsy.char1 = queasy.char1 AND rqsy.date1 = queasy.date1
            AND rqsy.number1 = queasy.number1 AND rqsy.number3 = 0 NO-LOCK NO-ERROR.
			IF AVAILABLE rqsy THEN
			DO:            
				IF INT(ENTRY(1,rqsy.char2,";")) EQ 1 THEN
				DO:
					statnr = 1. /*CLOSE*/
				END.
				ELSE IF INT(ENTRY(2,rqsy.char2,";")) EQ 1 AND INT(ENTRY(3,rqsy.char2,";")) EQ 0 THEN
				DO:
					statnr = 2. /*CTA*/         
				END.
				ELSE IF INT(ENTRY(3,rqsy.char2,";")) EQ 1 AND INT(ENTRY(2,rqsy.char2,";")) EQ 0 THEN
				DO:
					statnr = 3. /*CTD*/
				END.
				ELSE IF INT(ENTRY(2,rqsy.char2,";")) EQ 1 AND INT(ENTRY(3,rqsy.char2,";")) EQ 1 THEN
				DO:
					statnr = 4. /*CTAD*/
				END.
			END.
			/*Check where is Open status came from*/
			FIND FIRST rqsy WHERE rqsy.KEY = 175 AND rqsy.char1 = r-list.rcode
				AND rqsy.date1 EQ queasy.date1
				AND rqsy.number1 = queasy.number1 NO-LOCK NO-ERROR.
			IF AVAILABLE rqsy THEN
			DO:
				IF rqsy.char2 EQ "CLOSE" AND rqsy.number2 = 0 THEN
				DO:
					statnr = 0. /*Open*/
				END.
				IF rqsy.char2 EQ "CTA" AND rqsy.number2 = 0 THEN
				DO:
					statnr = 5. /*Open CTA*/
				END.
				IF rqsy.char2 EQ "CTD" AND rqsy.number2 = 0 THEN
				DO:
					statnr = 6. /*Open CTD*/
				END.
				
				IF rqsy.char2 EQ "CLOSE" AND rqsy.number2 = 1 THEN
				DO:
					statnr = 1. /*Close*/
				END.
				IF rqsy.char2 EQ "CTA" AND rqsy.number2 = 1 THEN
				DO:
					statnr = 2. /*CTA*/
				END.
				IF rqsy.char2 EQ "CTD" AND rqsy.number2 = 1 THEN
				DO:
					statnr = 3. /*CTD*/
				END.
			END.

        counter-avail = counter-avail + 1.
        CREATE push-allot-list.
        ASSIGN
            push-allot-list.startperiode = queasy.date1
            push-allot-list.endperiode   = queasy.date1
            push-allot-list.rcode        = queasy.char1
            push-allot-list.zikatnr      = queasy.number1
            push-allot-list.counter      = counter-avail
            push-allot-list.minLOS       = qsy2.number2
            push-allot-list.maxLOS       = qsy2.deci2
            push-allot-list.statnr       = statnr
        .
		/* NC-06/12/23 qty must same as pms
        IF statnr = 1 THEN push-allot-list.qty = 0.
        ELSE
        DO:
		*/
            FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
            push-allot-list.qty = queasy.number3 - queasy.number2.

            FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.char1 = ""                                  /* = changed to ne -> NC Revert Back to "=" */
                AND qsy.date1 = queasy.date1 AND qsy.number1 = queasy.number1 AND qsy.betriebsnr = beCode NO-LOCK NO-ERROR.
            IF AVAILABLE qsy THEN
            DO:
                room = rmcat-list.anzahl - qsy.number2 - qsy.number3.
                IF room LT push-allot-list.qty THEN                                                 /* LT changed to GT -> NC Revert Back to "LT " */        
                    push-allot-list.qty = room.
            END.
            /* push-quantity = push-allot-list.qty. NC - Not used*/
        /* END. */
            
        IF cat-flag THEN
        DO:
            FIND FIRST qsy WHERE qsy.KEY = 152 AND qsy.number1 = queasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE qsy THEN
				ASSIGN 
					push-allot-list.bezeich = qsy.char1
					push-allot-list.rmtype = qsy.char1. /*NC - for mapping on UI*/
        END.
        ELSE IF NOT bedsetup AND NOT avail-rmcat THEN
        DO:
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE zimkateg THEN
				ASSIGN 
					push-allot-list.bezeich = zimkateg.kurzbez
					push-allot-list.rmtype  = zimkateg.kurzbez. /*NC - for mapping on UI*/
        END.   
        ELSE IF bedsetup AND avail-rmcat THEN
        DO:                              
            FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE rmcat-list THEN
            DO:
                FIND FIRST rmlist WHERE rmlist.typ = rmcat-list.typ NO-LOCK NO-ERROR.
                IF AVAILABLE rmlist THEN push-allot-list.bezeich = rmlist.rmcode.
				FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
				IF AVAILABLE zimkateg THEN push-allot-list.rmtype = zimkateg.kurzbez. /*NC - for mapping on UI*/
                FIND FIRST zimmer WHERE zimmer.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
                IF AVAILABLE zimmer THEN
                DO:
                    FIND FIRST paramtext WHERE paramtext.txtnr = 9200 + zimmer.setup NO-LOCK NO-ERROR.
                    IF AVAILABLE paramtext THEN
                        push-allot-list.bsetup = paramtext.ptexte.
                END.   
            END. 
        END.
        ELSE IF bedsetup AND NOT avail-rmcat THEN
        DO:      
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE zimkateg THEN
				ASSIGN
					push-allot-list.bezeich = zimkateg.kurzbez
					push-allot-list.rmtype = zimkateg.kurzbez. /* NC - for mapping on UI */
            
            FIND FIRST zimmer WHERE zimmer.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer THEN
            DO:
                FIND FIRST paramtext WHERE paramtext.txtnr = 9200 + zimmer.setup NO-LOCK NO-ERROR.
                IF AVAILABLE paramtext THEN
                    push-allot-list.bsetup = paramtext.ptexte.
            END.   
        END.
    END. 
	
    FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.logi3 AND queasy.char1 NE "" AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
END.

/* for siteminder
FOR EACH push-allot-list:
    RUN find-date(push-allot-list.startperiode, OUTPUT curr-anz).
    FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = push-allot-list.rcode
        AND queasy.number1 = push-allot-list.zikatnr AND queasy.number2 = YEAR(push-allot-list.startperiode)
        AND queasy.number3 NE 0
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY = 174 AND queasy.char1 = push-allot-list.rcode
            AND queasy.number1 = push-allot-list.zikatnr AND queasy.number2 = YEAR(push-allot-list.startperiode)
            AND queasy.number3 NE 0 NO-LOCK:
                CREATE buff.
                BUFFER-COPY push-allot-list TO buff.
                buff.statnr = INT(ENTRY(curr-anz,queasy.char2,";")).
                FIND FIRST guest WHERE guest.gastnr = queasy.number3 AND guest.karteityp = 2 AND guest.steuernr NE "" 
                    NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                    buff.ota = TRIM(ENTRY(1,guest.steuernr,"|")).
        END.  
        DELETE push-allot-list.
    END.
    ELSE IF NOT AVAILABLE queasy THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = push-allot-list.rcode
            AND queasy.number1 = push-allot-list.zikatnr AND queasy.number2 = YEAR(push-allot-list.startperiode)
            NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            push-allot-list.statnr = INT(ENTRY(curr-anz,queasy.char2,";")).
            FIND FIRST guest WHERE guest.gastnr = queasy.number3 AND guest.karteityp = 2 AND guest.steuernr NE "" 
                NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
                push-allot-list.ota = TRIM(ENTRY(1,guest.steuernr,"|")).
        END. 
    END.     
END.*/
/* FIND FIRST push-allot-list NO-LOCK NO-ERROR. NC - 09/10/24 revertback */
FIND FIRST queasy WHERE queasy.KEY = 175 AND queasy.logi3 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy :
    FIND FIRST push-allot-list WHERE push-allot-list.startperiode = queasy.date1
        AND push-allot-list.rcode = queasy.char1 AND push-allot-list.zikatnr = queasy.number1
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE push-allot-list THEN
    DO:  /* NC - 09/10/24 revertback since restriction only run 1x */
		counter-avail = counter-avail + 1.
		CREATE push-allot-list.
		ASSIGN
			push-allot-list.startperiode = queasy.date1
			push-allot-list.endperiode   = queasy.date1
			push-allot-list.rcode        = queasy.char1
			push-allot-list.zikatnr      = queasy.number1
			push-allot-list.counter      = counter-avail
			/*push-allot-list.statnr       = queasy.number2
			 push-allot-list.qty          = push-quantity */
		.
		IF queasy.number3 NE 0 THEN
		DO:
			FIND FIRST guest WHERE guest.gastnr = queasy.number3 AND guest.karteityp = 2 AND guest.steuernr NE "" 
				NO-LOCK NO-ERROR.
			IF AVAILABLE guest THEN
				push-allot-list.ota = TRIM(ENTRY(1,guest.steuernr,"|")).
		END.

		IF cat-flag THEN
		DO:
			FIND FIRST qsy WHERE qsy.KEY = 152 AND qsy.number1 = queasy.number1 NO-LOCK NO-ERROR.
			IF AVAILABLE qsy THEN
				ASSIGN 
					push-allot-list.bezeich = qsy.char1
					push-allot-list.rmtype 	= qsy.char1. /*NC - for mapping on UI*/
		END.
		ELSE IF NOT bedsetup AND NOT avail-rmcat THEN
		DO:
			FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
			IF AVAILABLE zimkateg THEN 
				ASSIGN
				push-allot-list.bezeich = zimkateg.kurzbez
				push-allot-list.rmtype 	= zimkateg.kurzbez. /*NC - for mapping on UI*/
		END.  
		ELSE IF bedsetup AND avail-rmcat THEN
		DO:
			FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
			IF AVAILABLE rmcat-list THEN
			DO:
				FIND FIRST rmlist WHERE rmlist.typ = rmcat-list.typ NO-LOCK NO-ERROR.
				IF AVAILABLE rmlist THEN push-allot-list.bezeich = rmlist.rmcode.
				FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
				IF AVAILABLE zimkateg THEN push-allot-list.rmtype = zimkateg.kurzbez. /*NC - for mapping on UI*/
				FIND FIRST zimmer WHERE zimmer.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
				IF AVAILABLE zimmer THEN
				DO:
					FIND FIRST paramtext WHERE paramtext.txtnr = 9200 + zimmer.setup NO-LOCK NO-ERROR.
					IF AVAILABLE paramtext THEN
						push-allot-list.bsetup = paramtext.ptext.
				END.   
			END. 
		END.
		ELSE IF bedsetup AND NOT avail-rmcat THEN
		DO:
			FIND FIRST zimkateg WHERE zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
			IF AVAILABLE zimkateg THEN
				ASSIGN 
					push-allot-list.bezeich = zimkateg.kurzbez
					push-allot-list.rmtype = zimkateg.kurzbez. /*NC - for mapping on UI*/
			
			FIND FIRST zimmer WHERE zimmer.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
			IF AVAILABLE zimmer THEN
			DO:
				FIND FIRST paramtext WHERE paramtext.txtnr = 9200 + zimmer.setup NO-LOCK NO-ERROR.
				IF AVAILABLE paramtext THEN
					push-allot-list.bsetup = paramtext.ptext.
			END.   
		END.

		IF queasy.number2 = 1 THEN /*Restriction Radio Button [YES]*/
		DO:    
			IF queasy.char2 EQ "Close" THEN
			DO:                    
				push-allot-list.statnr = 1. 
				/* push-allot-list.qty = 0. */ /* NC-06/12/23 qty must same as pms */
			END.
			ELSE IF queasy.char2 EQ "CTA" THEN
			DO:
				push-allot-list.statnr = 2.
			END.
			ELSE IF  queasy.char2 EQ "CTD" THEN
			DO:        
				push-allot-list.statnr = 3.       
			END.
		END.
		ELSE IF queasy.number2 = 0 THEN /*Restriction Radio Button[NO]*/
		DO:    
			IF queasy.char2 EQ "Close" THEN
			DO:                    
				push-allot-list.statnr = 0. /*Open*/
			END.
			ELSE IF queasy.char2 EQ "CTA" THEN
			DO:
				push-allot-list.statnr = 5. /*OpenCTA*/
			END.
			ELSE IF  queasy.char2 EQ "CTD" THEN
			DO:        
				push-allot-list.statnr = 6. /*OpenCTD*/
			END.
		END. 

		/* NC-06/12/23 qty must same as pms */
		IF push-allot-list.statnr GE 0 /*and queasy.number3 = 0*/ THEN /*NC-18/07/19 cari availnya selain close*/
		DO:
		
			FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.char1 = queasy.char1 
				AND qsy.date1 = queasy.date1 AND qsy.number1 = queasy.number1 AND qsy.betriebsnr = beCode NO-LOCK NO-ERROR.
			IF NOT AVAILABLE qsy THEN
				FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.char1 = ""
					AND qsy.date1 = queasy.date1 AND qsy.number1 = queasy.number1 AND qsy.betriebsnr = beCode NO-LOCK NO-ERROR.
			IF AVAILABLE qsy THEN
			DO:
				FIND FIRST qsy2 WHERE qsy2.KEY = 2 AND qsy2.char1 = queasy.char1 NO-LOCK NO-ERROR.
				IF AVAILABLE qsy2 THEN
				DO:
					zero-flag = NO.
					IF qsy2.date1 NE ? OR qsy2.date2 NE ? THEN
					DO:
						IF qsy2.date1 NE ? AND qsy2.date2 = ? AND ci-date LT qsy2.date1 THEN zero-flag = YES.
						ELSE IF qsy2.date1 = ? AND qsy2.date2 NE ? AND ci-date GT qsy2.date2 THEN zero-flag = YES.
						ELSE IF qsy2.date1 NE ? AND qsy2.date2 NE ? AND (ci-date LT qsy2.date1 OR ci-date GT qsy2.date2) THEN zero-flag = YES.
					END.
		
					IF zero-flag THEN push-allot-list.qty = 0.
					ELSE
					DO:
						IF qsy.char1 NE "" THEN
						DO:
							FIND FIRST bqueasy WHERE bqueasy.KEY = 171 AND bqueasy.char1 = ""
								AND bqueasy.date1 = queasy.date1 AND bqueasy.number1 = queasy.number1 AND bqueasy.betriebsnr = beCode NO-LOCK NO-ERROR.
							IF AVAILABLE bqueasy THEN
							DO:
								FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
								IF AVAILABLE rmcat-list THEN
									room = rmcat-list.anzahl - bqueasy.number2 - bqueasy.number3.
							END.
							
							push-allot-list.qty = qsy.number3 - qsy.number2.
		
							IF room LT push-allot-list.qty THEN push-allot-list.qty = room.
						END.
						ELSE IF qsy.char1 = "" THEN
						DO:
							FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
							IF AVAILABLE rmcat-list THEN
							DO:
								ASSIGN
									room = rmcat-list.anzahl - qsy.number2 - qsy.number3
									push-allot-list.qty = room.
							END.
								
						END.
					END.
				END.
			END.
		END.
	END.
	FIND NEXT queasy WHERE queasy.KEY = 175 AND queasy.logi3 NO-LOCK NO-ERROR.
END. 

PROCEDURE find-date:
    DEFINE INPUT PARAMETER curr-date AS DATE.
    DEFINE OUTPUT PARAMETER curr-anz AS INT.
    
    DEFINE VARIABLE mm        AS INT.
    DEFINE VARIABLE yy        AS INT.
    DEFINE VARIABLE datum     AS DATE.
    DEFINE VARIABLE end-month AS INT.
    DEFINE VARIABLE prev-day  AS INT.

    ASSIGN
        mm = MONTH(curr-date)
        yy = YEAR(curr-date).

    IF mm = 1 THEN prev-day = 0.
    ELSE
    DO:
        DO i = 1 TO mm - 1:
            ASSIGN
                datum = DATE(i + 1, 1, yy)
                datum = datum - 1
                prev-day = prev-day + DAY(datum)
            .
        END.
    END.

    curr-anz = prev-day + DAY(curr-date).
END.
                                           
/*for testing push availability
DEFINE VARIABLE curr-qty AS INT INIT 0.

DEF BUFFER buffallot FOR push-allot-list.
FOR EACH push-allot-list WHERE push-allot-list.flag BY push-allot-list.rcode BY push-allot-list.zikatnr BY push-allot-list.startperiode:
    IF curr-qty NE push-allot-list.qty THEN
        ASSIGN
            curr-rcode   = push-allot-list.rcode
            curr-bezeich = push-allot-list.bezeich
            curr-recid   = push-allot-list.counter
            curr-qty    = push-allot-list.qty
        .
    ELSE IF curr-qty = push-allot-list.qty AND (curr-rcode NE push-allot-list.rcode OR curr-bezeich NE push-allot-list.bezeich) THEN
        ASSIGN 
            curr-rcode = push-allot-list.rcode
            curr-bezeich = push-allot-list.bezeich
            curr-recid  = push-allot-list.counter
            curr-qty  = push-allot-list.qty.
    ELSE IF curr-qty = push-allot-list.qty AND curr-rcode = push-allot-list.rcode AND curr-bezeich = push-allot-list.bezeich THEN
    DO:
        FIND FIRST buffallot WHERE buffallot.counter = curr-recid EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE buffallot AND (buffallot.endperiode = push-allot-list.startperiode - 1 OR 
                                   buffallot.endperiode GE push-allot-list.startperiode)
            AND buffallot.rcode = push-allot-list.rcode
            AND buffallot.bezeich = push-allot-list.bezeich THEN
        DO:
            
            IF buffallot.endperiode GT push-allot-list.endperiode THEN.
            ELSE buffallot.endperiode = push-allot-list.endperiode.
            DELETE push-allot-list.
            RELEASE push-allot-list.
        END.
    END.    
END.

filenm = "C:\vhp-SM\vhplib\RG\debug3\avail" + STRING(TIME) + ".csv".
DEFINE STREAM s1.
OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.  
FOR EACH push-allot-list WHERE push-allot-list.flag BY push-allot-list.rcode BY push-allot-list.zikatnr BY push-allot-list.startperiode:
    PUT STREAM s1 UNFORMATTED 
      push-allot-list.counter "," push-allot-list.rcode "," push-allot-list.bezeich "," push-allot-list.startperiode "," 
      push-allot-list.endperiode "," STRING(push-allot-list.qty) SKIP.
END.
OUTPUT STREAM s1 CLOSE. */

PROCEDURE count-rmcateg: 
DEFINE VARIABLE zikatnr AS INTEGER INITIAL 0. 
    EMPTY TEMP-TABLE  rmcat-list.
    
    FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK BY zimmer.zikatnr: 
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR. 
        IF AVAILABLE zimkateg AND zimkateg.verfuegbarkeit THEN 
        DO: 
            IF cat-flag AND zimkateg.typ NE 0 THEN
                zikatnr = zimkateg.typ.
            ELSE zikatnr = zimkateg.zikatnr. 
            
            FIND FIRST temp-list WHERE temp-list.zikatnr = zikatnr NO-LOCK NO-ERROR.
            IF (NOT all-room AND AVAILABLE temp-list) OR all-room THEN
            DO:
                FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zikatnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE rmcat-list THEN
                DO: 
                    CREATE rmcat-list.
                    ASSIGN 
                        rmcat-list.zikatnr = zikatnr
                        rmcat-list.typ     = zimkateg.typ
                        rmcat-list.anzahl = 1.
                END.
                ELSE rmcat-list.anzahl = rmcat-list.anzahl + 1. 
            END.
        END. 
    END.
END. 

PROCEDURE count-availability:
    DEFINE INPUT PARAMETER curr-date AS DATE.
    DEFINE INPUT PARAMETER i-typ   AS INT.
    DEFINE OUTPUT PARAMETER rm-occ   AS INT.
    DEFINE OUTPUT PARAMETER rm-ooo   AS INT.
    DEFINE OUTPUT PARAMETER rm-allot AS INT.
    
    DEFINE VARIABLE vhp-limited AS LOGICAL INIT NO NO-UNDO.
    DEFINE VARIABLE do-it       AS LOGICAL INIT NO NO-UNDO.

	FOR EACH kontline WHERE kontline.kontstat = 1 
		AND curr-date GE kontline.ankunft AND curr-date LE kontline.abreise NO-LOCK,
		FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK :
		
		IF allotment AND kontline.betriebsnr = 0 
			AND curr-date GE (ci-date + kontline.ruecktage ) THEN do-it = YES.
		ELSE IF NOT allotment AND kontline.betriebsnr = 1 THEN /*GLOBAL RESERVATION*/
			do-it = YES.
		IF do-it THEN
		DO:
			IF cat-flag AND zimkateg.typ = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
			ELSE IF NOT cat-flag AND zimkateg.zikatnr = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
		END.
	END.

    IF cat-flag THEN
    DO:
        FIND FIRST bresline WHERE bresline.active-flag LE 1 
            AND bresline.resstatus LE 6 /* AND bresline.resstatus NE 3 */
            AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
            AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
            AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
            AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
            
        DO WHILE AVAILABLE bresline :
			FIND FIRST zimkateg WHERE zimkateg.zikatnr = bresline.zikatnr AND zimkateg.typ = i-typ NO-LOCK NO-ERROR.
			IF AVAILABLE zimkateg THEN DO:
				do-it = YES. 
				IF bresline.zinr NE "" THEN 
				DO: 
					FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
					do-it = zimmer.sleeping. 
				END. 
		
				IF do-it AND vhp-limited THEN
				DO:
					FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
						NO-LOCK.
					FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
						NO-LOCK NO-ERROR.
					do-it = AVAILABLE segment AND segment.vip-level = 0.
				END.
		
				IF do-it THEN 
					rm-occ = rm-occ + bresline.zimmeranz. 
					
				/*Find reservation that using global reservation*/
				FIND FIRST kline WHERE kline.kontignr = bresline.kontignr 
						AND kline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kline THEN
				DO:
					IF allotment AND curr-date GE (ci-date + kline.ruecktage ) THEN
						FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
							AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
					ELSE /*NC - 31/08/21 enhanced  kontline.betriebsnr = 1 -> global reservation*/	
						FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
							AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
					IF AVAILABLE kontline THEN
					DO:
						do-it = YES. 
						IF bresline.zinr NE "" THEN 
						DO: 
							FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
							do-it = zimmer.sleeping. 
						END. 
				
						IF do-it AND vhp-limited THEN
						DO:
							FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
								NO-LOCK.
							FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
								NO-LOCK NO-ERROR.
							do-it = AVAILABLE segment AND segment.vip-level = 0.
						END.
				
						IF do-it THEN 
							rm-allot = rm-allot - bresline.zimmeranz. 
					END.
				END.
			END.

            FIND NEXT bresline WHERE bresline.active-flag LE 1 
            AND bresline.resstatus LE 6 /* AND bresline.resstatus NE 3 */
            AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
            AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
            AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
            AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
            
        END.
        /*dody 14/01/24 stuck trace
        FOR EACH bresline WHERE bresline.active-flag LE 1 
            AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
            AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
            AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
            AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
            AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = bresline.zikatnr AND zimkateg.typ = i-typ NO-LOCK: 
            
            do-it = YES. 
            IF bresline.zinr NE "" THEN 
            DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
            END. 
    
            IF do-it AND vhp-limited THEN
            DO:
                FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
                    NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                    NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
            END.
    
            IF do-it THEN 
                rm-occ = rm-occ + bresline.zimmeranz. 
				
			/*Find reservation that using global reservation*/
			FIND FIRST kline WHERE kline.kontignr = bresline.kontignr 
                    AND kline.kontstat = 1 NO-LOCK NO-ERROR.
			IF AVAILABLE kline THEN
			DO:
				IF allotment AND curr-date GE (ci-date + kline.ruecktage ) THEN
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				ELSE /*NC - 31/08/21 enhanced  kontline.betriebsnr = 1 -> global reservation*/	
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kontline THEN
				DO:
					do-it = YES. 
					IF bresline.zinr NE "" THEN 
					DO: 
						FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
						do-it = zimmer.sleeping. 
					END. 
			
					IF do-it AND vhp-limited THEN
					DO:
						FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
							NO-LOCK.
						FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
							NO-LOCK NO-ERROR.
						do-it = AVAILABLE segment AND segment.vip-level = 0.
					END.
			
					IF do-it THEN 
						rm-allot = rm-allot - bresline.zimmeranz. 
				END.
			END.
        END. */
    END.
    ELSE
    DO:
        FIND FIRST bresline WHERE bresline.active-flag LE 1 
            AND bresline.resstatus LE 6 /* AND bresline.resstatus NE 3 */
            AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
            AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
            AND bresline.zikatnr = i-typ 
            AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
            AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE bresline:

            do-it = YES. 
            IF bresline.zinr NE "" THEN 
            DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
            END. 
    
            IF do-it AND vhp-limited THEN
            DO:
                FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
                    NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                    NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
            END.
    
            IF do-it THEN 
                rm-occ = rm-occ + bresline.zimmeranz. 
				
			/*Find reservation that using global reservation*/	
			FIND FIRST kline WHERE kline.kontignr = bresline.kontignr 
                    AND kline.kontstat = 1 NO-LOCK NO-ERROR.
			IF AVAILABLE kline THEN
			DO:
				IF allotment AND curr-date GE (ci-date + kline.ruecktage ) THEN
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				ELSE /*NC - 31/08/21 enhanced  kontline.betriebsnr = 1 -> global reservation*/	
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kontline THEN
				DO:
					do-it = YES. 
					IF bresline.zinr NE "" THEN 
					DO: 
						FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
						do-it = zimmer.sleeping. 
					END. 
			
					IF do-it AND vhp-limited THEN
					DO:
						FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
							NO-LOCK.
						FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
							NO-LOCK NO-ERROR.
						do-it = AVAILABLE segment AND segment.vip-level = 0.
					END.
			
					IF do-it THEN 
					DO:
						rm-allot = rm-allot - bresline.zimmeranz. 
					END.
				END.
			END.


            FIND NEXT bresline WHERE bresline.active-flag LE 1 
            AND bresline.resstatus LE 6 /* AND bresline.resstatus NE 3 */
            AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
            AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
            AND bresline.zikatnr = i-typ 
            AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
            AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        END.
    END.
        /*dody 14/01/24 stuck trace
        FOR EACH bresline WHERE bresline.active-flag LE 1 
            AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
            AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
            AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
            AND bresline.zikatnr = i-typ 
            AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
            AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK:

            do-it = YES. 
            IF bresline.zinr NE "" THEN 
            DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
            END. 
    
            IF do-it AND vhp-limited THEN
            DO:
                FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
                    NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                    NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
            END.
    
            IF do-it THEN 
                rm-occ = rm-occ + bresline.zimmeranz. 
				
			/*Find reservation that using global reservation*/	
			FIND FIRST kline WHERE kline.kontignr = bresline.kontignr 
                    AND kline.kontstat = 1 NO-LOCK NO-ERROR.
			IF AVAILABLE kline THEN
			DO:
				IF allotment AND curr-date GE (ci-date + kline.ruecktage ) THEN
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				ELSE /*NC - 31/08/21 enhanced  kontline.betriebsnr = 1 -> global reservation*/	
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kontline THEN
				DO:
					do-it = YES. 
					IF bresline.zinr NE "" THEN 
					DO: 
						FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
						do-it = zimmer.sleeping. 
					END. 
			
					IF do-it AND vhp-limited THEN
					DO:
						FIND FIRST reservation WHERE reservation.resnr = bresline.resnr
							NO-LOCK.
						FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
							NO-LOCK NO-ERROR.
						do-it = AVAILABLE segment AND segment.vip-level = 0.
					END.
			
					IF do-it THEN 
					DO:
						rm-allot = rm-allot - bresline.zimmeranz. 
					END.
				END.
			END.
        END.*/
    FOR EACH outorder WHERE outorder.betriebsnr LE 1 
        AND curr-date GE outorder.gespstart AND curr-date LE outorder.gespende NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping = YES NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK:

        IF cat-flag AND zimkateg.typ = i-typ THEN rm-ooo = rm-ooo + 1.
        ELSE IF NOT cat-flag AND zimkateg.zikatnr = i-typ THEN rm-ooo = rm-ooo + 1.
    END.
    IF NOT allotment THEN rm-occ = rm-occ + rm-allot.
END.

done = YES.
