
DEFINE TEMP-TABLE dynaRate-list NO-UNDO
    FIELD counter  AS INTEGER
    FIELD w-day    AS INTEGER FORMAT "9"     LABEL "WeekDay" INIT 0 /* week day 0=ALL, 1=Mon..7=Sun */
    FIELD rmType   AS CHAR    FORMAT "x(10)" LABEL "Room Type"
    FIELD fr-room  AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
    FIELD to-room  AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
    FIELD days1    AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
    FIELD days2    AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
    FIELD rCode    AS CHAR    FORMAT "x(10)" LABEL "RateCode" /* statcode */
    FIELD dynaCode AS CHAR    FORMAT "x(10)" LABEL "RateCode" /* dynacode */.

DEFINE TEMP-TABLE r-list NO-UNDO
    FIELD rcode    AS CHAR
.
/*NC - 20/07/23 for STATIC RateCode according contract rate setup*/
DEFINE TEMP-TABLE s-list NO-UNDO
    FIELD static-code    AS CHAR
.
DEFINE TEMP-TABLE rate-list NO-UNDO
    FIELD startperiode AS DATE
    FIELD endperiode   AS DATE
    FIELD zikatnr      AS INT
    FIELD counter      AS INT
    FIELD rcode        AS CHAR
    FIELD bezeich      AS CHAR
    FIELD pax          AS INT
    FIELD child        AS INT
    FIELD rmrate       AS DECIMAL FORMAT ">>>,>>>,>>9.99"
    FIELD flag         AS LOGICAL INIT YES
    FIELD currency     AS CHAR
    FIELD scode        AS CHAR
.

DEFINE TEMP-TABLE push-rate-list NO-UNDO LIKE rate-list
    FIELD str-date1    AS CHAR
    FIELD str-date2    AS CHAR.

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

DEF TEMP-TABLE grp-type
    FIELD gtype AS CHAR
    FIELD rm-type AS INTEGER
.

DEFINE TEMP-TABLE bratecode NO-UNDO LIKE ratecode.
DEFINE TEMP-TABLE t-zimkateg NO-UNDO LIKE zimkateg.
DEFINE TEMP-TABLE t-waehrung NO-UNDO LIKE waehrung.
DEFINE TEMP-TABLE t-arrangement NO-UNDO LIKE arrangement.
DEFINE TEMP-TABLE t-queasy NO-UNDO LIKE queasy .
DEFINE TEMP-TABLE t-queasy170 NO-UNDO LIKE queasy .
DEFINE TEMP-TABLE bqueasy NO-UNDO LIKE queasy.  /* qsy.key = 2 */
DEFINE TEMP-TABLE t-qsy18 NO-UNDO LIKE queasy.
DEFINE TEMP-TABLE t-qsy145 NO-UNDO LIKE queasy.
DEFINE TEMP-TABLE t-qsy152 NO-UNDO LIKE queasy.
DEFINE TEMP-TABLE q-curr NO-UNDO LIKE queasy.   /* qsy key = 164 */
DEFINE TEMP-TABLE t-qsy171 NO-UNDO LIKE queasy.
DEFINE TEMP-TABLE t-qsy170 NO-UNDO LIKE queasy
	FIELD rec-id AS INT.
	
DEFINE TEMP-TABLE grtype NO-UNDO LIKE grp-type. /*#574A5F NC - 15/11/24*/ 

DEFINE BUFFER qsy       FOR queasy.
DEFINE BUFFER currqsy   FOR queasy.
DEFINE BUFFER kline 	FOR kontline.
DEFINE BUFFER bqsy170   FOR queasy.
DEFINE BUFFER qsy170    FOR queasy.
DEFINE BUFFER qsy159    FOR queasy.
DEFINE BUFFER bresline  FOR res-line.


DEFINE INPUT  PARAMETER inp-str   AS CHAR.
DEFINE INPUT  PARAMETER start-counter AS INT.
DEFINE INPUT  PARAMETER pushPax   AS LOGICAL.
DEFINE INPUT  PARAMETER fdate     AS DATE.
DEFINE INPUT  PARAMETER tdate     AS DATE.
DEFINE INPUT  PARAMETER adult     AS INTEGER.
DEFINE INPUT  PARAMETER child     AS INTEGER.
DEFINE INPUT  PARAMETER beCode    AS INTEGER.
DEFINE INPUT  PARAMETER TABLE FOR temp-list.
DEFINE OUTPUT PARAMETER done     AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR push-rate-list.

/*
DEFINE VAR inp-str   AS CHAR INIT "no=no".
DEFINE VAR start-counter AS INT INIT 1.
DEFINE var pushPax   AS LOGICAL INIT NO.
DEFINE VAR pushRate  AS LOGICAL INIT YES.
DEFINE VARIABLE beCode AS INT INIT 1.
DEFINE VARIABLE fdate AS DATE INIT 08/25/16.
DEFINE VARIABLE tdate AS DATE INIT 08/24/17.
DEFINE VARIABLE adult     AS INT INIT 2.
DEFINE VARIABLE child     AS INT INIT 0.
DEFINE VARIABLE done  AS LOGICAL INIT NO.
*/

DEFINE VARIABLE curr-rate AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-recid AS INT NO-UNDO.
DEFINE VARIABLE curr-scode AS CHAR NO-UNDO.
DEFINE VARIABLE curr-bezeich AS CHAR NO-UNDO.
DEFINE VARIABLE temp-zikat AS CHAR NO-UNDO.
DEFINE VARIABLE starttime AS INT NO-UNDO.
starttime = TIME. 

DEFINE VARIABLE curr-date AS DATE NO-UNDO.          
DEFINE VARIABLE ankunft   AS DATE NO-UNDO.
DEFINE VARIABLE ci-date   AS DATE NO-UNDO.
DEFINE VARIABLE co-date   AS DATE NO-UNDO.
DEFINE VARIABLE datum     AS DATE NO-UNDO.

DEFINE VARIABLE tokcounter  AS INTEGER NO-UNDO.
DEFINE VARIABLE ifTask      AS CHAR    NO-UNDO.
DEFINE VARIABLE mesToken    AS CHAR    NO-UNDO.
DEFINE VARIABLE mesValue          AS CHAR    NO-UNDO.
DEFINE VARIABLE grpcode    AS CHAR    NO-UNDO.
DEFINE VARIABLE global-occ  AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE splited-occ  AS LOGICAL NO-UNDO INIT NO. /*#574A5F NC - 15/11/24*/ 
DEFINE VARIABLE q-recid  AS INTEGER INIT 0 NO-UNDO.
                                     
DEFINE VARIABLE vhp-limited     AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE do-it           AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE exist  			AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE cat-flag        AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE pushAll              AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE re-calculateRate     AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE createRate     AS LOGICAL INIT NO NO-UNDO.

DEFINE VARIABLE cm-gastno     AS INT INIT 0 NO-UNDO.  
DEFINE VARIABLE counter       AS INT INIT 0 NO-UNDO.  
DEFINE VARIABLE counter170 AS INT INIT 0 NO-UNDO.    
DEFINE VARIABLE i             AS INT INIT 0 NO-UNDO.  
DEFINE VARIABLE occ-room      AS INT INIT 0 NO-UNDO.

DEFINE VARIABLE end-date AS DATE NO-UNDO.

DEFINE VARIABLE max-occ  AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE rm-occ AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE rm-ooo AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE room   AS INT INIT 0 NO-UNDO.

DEFINE VARIABLE maxroom AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE def-rate AS CHAR INIT "" NO-UNDO.

DEFINE VARIABLE w-day               AS INTEGER  NO-UNDO.
DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8 NO-UNDO
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE VARIABLE tax-included AS LOGICAL INITIAL NO NO-UNDO.
DEFINE VARIABLE serv         AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat          AS DECIMAL NO-UNDO.

DEFINE VARIABLE strl        AS CHAR     NO-UNDO.
DEFINE VARIABLE strll       AS CHAR     NO-UNDO.
DEFINE VARIABLE loopi       AS INTEGER  NO-UNDO.
DEFINE VARIABLE loopj       AS INTEGER  NO-UNDO.
DEFINE VARIABLE currType    AS CHAR     NO-UNDO.
DEFINE VARIABLE frmType     AS INTEGER  NO-UNDO.

EMPTY TEMP-TABLE bratecode.
EMPTY TEMP-TABLE t-zimkateg.
EMPTY TEMP-TABLE t-waehrung.
EMPTY TEMP-TABLE t-arrangement.
EMPTY TEMP-TABLE bqueasy.
EMPTY TEMP-TABLE t-qsy18.
EMPTY TEMP-TABLE t-qsy145.
EMPTY TEMP-TABLE t-qsy152.
EMPTY TEMP-TABLE t-qsy170.
EMPTY TEMP-TABLE t-qsy171.
EMPTY TEMP-TABLE q-curr.
EMPTY TEMP-TABLE t-queasy.

FOR EACH dynarate-list:
	DELETE dynarate-list.
END.

FOR EACH grp-type:
	DELETE grp-type.
END.
/* NC - 20/07/23 ratecode proses too long
FIND FIRST ratecode USE-INDEX code_ix NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE ratecode:
    CREATE bratecode.
    BUFFER-COPY ratecode TO bratecode.
    FIND NEXT ratecode USE-INDEX code_ix NO-LOCK NO-ERROR.
END.
*/
FIND FIRST htparam WHERE htparam.paramnr = 1364 AND htparam.bezeich NE "not used" NO-LOCK NO-ERROR. /*nc 09/05/25*/
IF AVAILABLE htparam AND htparam.fchar NE " " THEN DO:
  
    DO  loopi = 1 TO NUM-ENTRIES(htparam.fchar, ";"):
        ASSIGN strl = ENTRY(loopi, htparam.fchar, ";" ).
    
        DO loopj = 1 TO NUM-ENTRIES(strl, ","):
            strll = ENTRY(loopj, strl, ",").
            
            IF loopj = 1 THEN 
                ASSIGN currType = SUBSTR(strll,1,1)
                       frmType  = INTEGER(SUBSTR(strll,2,1)).
    
            CREATE grp-type.
            ASSIGN grp-type.gtype = currType.
            IF loopj = 1 THEN ASSIGN grp-type.rm-type = frmType.
            ELSE ASSIGN grp-type.rm-type = INTEGER(strll).
        END.
    END.
END.
FIND FIRST waehrung NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE waehrung:
	CREATE t-waehrung.
	BUFFER-COPY waehrung TO t-waehrung.
	FIND NEXT waehrung NO-LOCK NO-ERROR.
END.

FIND FIRST arrangement NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE arrangement:
	CREATE t-arrangement.
	BUFFER-COPY arrangement TO t-arrangement.
	FIND NEXT arrangement NO-LOCK NO-ERROR.
END.

FIND FIRST zimkateg WHERE zimkateg.ACTIVE NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE zimkateg:
	CREATE t-zimkateg.
	BUFFER-COPY zimkateg TO t-zimkateg.
	FIND NEXT zimkateg WHERE zimkateg.ACTIVE NO-LOCK NO-ERROR.
END.

FIND FIRST queasy WHERE queasy.KEY = 2 NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE queasy:
	CREATE bqueasy.
	BUFFER-COPY queasy TO bqueasy.
	FIND NEXT queasy WHERE queasy.KEY = 2 NO-LOCK NO-ERROR.
END.

FIND FIRST queasy WHERE queasy.KEY = 18  NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE queasy:
	CREATE t-qsy18.
	BUFFER-COPY queasy TO t-qsy18.
	FIND NEXT queasy WHERE queasy.KEY = 18 NO-LOCK NO-ERROR.
END.

FIND FIRST queasy WHERE queasy.KEY = 152  NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE queasy:
	CREATE t-qsy152.
	BUFFER-COPY queasy TO t-qsy152.
	FIND NEXT queasy WHERE queasy.KEY = 152  NO-LOCK NO-ERROR.
END.

FIND FIRST queasy WHERE queasy.KEY = 164  NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE queasy:
	CREATE q-curr.
	BUFFER-COPY queasy TO q-curr.
	FIND NEXT queasy WHERE queasy.KEY = 164  NO-LOCK NO-ERROR.
END.
/*
FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.date1 GE fdate AND queasy.date1 LE tdate NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE queasy:
    CREATE t-qsy170.
    BUFFER-COPY queasy TO t-qsy170.
	ASSIGN t-qsy170.rec-id = RECID(queasy).
	FIND NEXT queasy WHERE queasy.KEY = 170 AND queasy.date1 GE fdate AND queasy.date1 LE tdate NO-LOCK NO-ERROR.
END.
*/


ASSIGN
    adult = 2
    done  = NO
	maxroom = 0
	def-rate = "".

IF NUM-ENTRIES(inp-str,"=") GE 2 THEN
    ASSIGN
        pushAll          = LOGICAL(ENTRY(1,inp-str,"="))
        re-calculateRate = LOGICAL(ENTRY(2,inp-str,"=")).

FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
tax-included = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 253 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
IF htparam.flogic THEN RETURN.

FIND FIRST queasy WHERE queasy.KEY = 159 AND queasy.number1 = beCode NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
DO:
    FIND FIRST guest WHERE guest.gastnr = queasy.number2 NO-LOCK NO-ERROR.
	IF AVAILABLE guest THEN
	DO:
		FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK NO-ERROR.
		IF AVAILABLE guest-pr THEN cm-gastno = guest.gastnr.
		ELSE RETURN.
	END.
END.

FIND FIRST t-qsy152 NO-LOCK NO-ERROR.
IF AVAILABLE t-qsy152 THEN cat-flag = YES.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
IF AVAILABLE htparam THEN
ASSIGN ci-date = htparam.fdate.

IF fDate = ci-date THEN ankunft = ci-date.
ELSE ankunft = fDate + 2.

FOR EACH temp-list:
    IF cat-flag THEN
    DO:
        FIND FIRST t-qsy152 WHERE t-qsy152.char1 = temp-list.rmtype NO-LOCK NO-ERROR.
        IF AVAILABLE t-qsy152 THEN 
		DO:
			temp-list.zikatnr = t-qsy152.number1.
			
		END.
    END.  
    ELSE 
    DO:
        FIND FIRST t-zimkateg WHERE t-zimkateg.kurzbez = temp-list.rmtype  NO-LOCK NO-ERROR.
        IF AVAILABLE t-zimkateg THEN 
		DO:
			temp-list.zikatnr = t-zimkateg.zikatnr.
			
		END.
    END.                                                             
END.

EMPTY TEMP-TABLE r-list.
EMPTY TEMP-TABLE s-list.

FIND FIRST temp-list NO-LOCK NO-ERROR.
IF AVAILABLE temp-list THEN
DO:
	FOR EACH temp-list:
		FIND FIRST r-list WHERE r-list.rcode = temp-list.rcode  NO-LOCK NO-ERROR.
		IF NOT AVAILABLE r-list THEN
		DO:
			CREATE r-list.
			r-list.rcode = temp-list.rcode.
		END.
	END.
END.
ELSE
DO:
    FOR EACH guest-pr WHERE guest-pr.gastnr = cm-gastno NO-LOCK:
        CREATE r-list.
        r-list.rcode = guest-pr.CODE.
    END.
END.
/*NC - 07/09/23*/
/* DO TRANSACTION: */
	FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.betriebsnr GT 0 NO-LOCK NO-ERROR.
	IF AVAILABLE queasy THEN DO:
		FOR EACH qsy159 WHERE KEY = 159 AND qsy159.number2 EQ 0 NO-LOCK: /*NC - BE not active*/
			FOR EACH qsy170 WHERE qsy170.KEY = 170 AND qsy170.betriebsnr = qsy159.number1 NO-LOCK :
				DO TRANSACTION:
					FIND FIRST qsy WHERE RECID(qsy) = RECID(qsy170) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
					IF AVAILABLE qsy THEN 
						DELETE qsy.
				END.
				
			END.
		END.
		FOR EACH qsy170 WHERE qsy170.KEY = 170 AND qsy170.betriebsnr = 0 NO-LOCK :
			DO TRANSACTION :
				FIND FIRST qsy WHERE RECID(qsy) = RECID(qsy170) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
				IF AVAILABLE qsy THEN
					DELETE qsy.
			END.
		END.
	END.
	ELSE DO:
		FOR EACH queasy WHERE queasy.KEY = 170 AND queasy.betriebsnr = 0 NO-LOCK :
				FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) NO-LOCK NO-ERROR.
				IF AVAILABLE qsy THEN
				DO:
					FIND CURRENT qsy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
					ASSIGN qsy.betriebsnr = beCode.
					FIND CURRENT qsy NO-LOCK.
					RELEASE qsy.
				END.

		END.
	END.
/* END. */

/* DO TRANSACTION: */

IF pushALL THEN
DO :
	FOR EACH currqsy WHERE currqsy.KEY = 170 AND currqsy.betriebsnr = beCode EXCLUSIVE-LOCK :
			DELETE currqsy.
	END.

	/*NC - 22/07/23 this use when push-all only*/
	FOR EACH queasy WHERE queasy.KEY = 171 AND queasy.date1 GE fdate AND queasy.date1 LE tdate AND queasy.betriebsnr = beCode NO-LOCK :
		CREATE t-qsy171.
		BUFFER-COPY queasy TO t-qsy171.
	END.
	
	FOR EACH queasy WHERE queasy.KEY = 145 AND queasy.date1 GE fdate AND queasy.date1 LE tdate  NO-LOCK:
		CREATE t-qsy145.
		BUFFER-COPY queasy TO t-qsy145.
	END.
    /*RUN update-bookengine-configbl.p (8,beCode,NO,"").*/
END.
ELSE 
DO:
	FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.date1 LT fdate - 2 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	IF AVAILABLE queasy THEN
	DO :
		FOR EACH currqsy WHERE currqsy.KEY = 170 AND currqsy.date1 LT fdate - 2 AND currqsy.betriebsnr = beCode EXCLUSIVE-LOCK :

				DELETE currqsy.
	
		END.
	END.
	/*NC - 12/03/24 #176EA5 */ /*untuk todate jika blm terbentuk to keep periode days*/
	FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.date1 EQ tdate AND qsy.betriebsnr = beCode NO-LOCK NO-ERROR.
	IF NOT AVAILABLE qsy THEN DO:
		createRate = YES.
		
		FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 EQ tdate AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
		REPEAT WHILE AVAILABLE queasy:
			CREATE t-qsy171.
			BUFFER-COPY queasy TO t-qsy171.
			FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 EQ tdate AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
		END.
	
		FIND FIRST queasy WHERE queasy.KEY = 145 AND queasy.date1 EQ tdate  NO-LOCK NO-ERROR.
		REPEAT WHILE AVAILABLE queasy:
			CREATE t-qsy145.
			BUFFER-COPY queasy TO t-qsy145.
			FIND NEXT queasy WHERE queasy.KEY = 145 AND queasy.date1 EQ tdate NO-LOCK NO-ERROR.
		END.
	END.
END.
/* END. end do transaction*/

FOR EACH r-list NO-LOCK,
	FIRST bqueasy WHERE bqueasy.char1 = r-list.rcode NO-LOCK:
	IF bqueasy.logi2 THEN /*dynamic rate only*/
	DO:
		FOR EACH ratecode WHERE ratecode.CODE = r-list.rcode NO-LOCK:
			CREATE dynarate-list.
			ASSIGN
				dynarate-list.dynaCode = ratecode.CODE
				ifTask                 = ratecode.char1[5]
			.
			DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
				mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
				mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
				CASE mesToken:
					WHEN "CN" THEN dynarate-list.counter = INTEGER(mesValue).
					WHEN "RT" THEN dynarate-list.rmType  = mesValue.
					WHEN "WD" THEN dynarate-list.w-day   = INTEGER(mesValue).
					WHEN "FR" THEN dynarate-list.fr-room = INTEGER(mesValue).
					WHEN "TR" THEN dynarate-list.to-room = INTEGER(mesValue).
					WHEN "D1" THEN dynarate-list.days1   = INTEGER(mesValue).
					WHEN "D2" THEN dynarate-list.days2   = INTEGER(mesValue).
					WHEN "RC" THEN dynarate-list.rCode   = mesValue.
				END CASE.
			END.

			IF dynarate-list.to-room GT maxroom THEN
			DO:
				ASSIGN
					def-rate = dynarate-list.rCode
					maxroom = dynarate-list.to-room.
			END.  
		END.
	END.
END.
/* dynamic rate option = 0, 1 or 2 */
FIND FIRST htparam WHERE htparam.paramnr = 439 NO-LOCK NO-ERROR.
FIND FIRST grp-type NO-LOCK NO-ERROR.
IF AVAILABLE grp-type THEN splited-occ = YES.
FIND FIRST dynarate-list WHERE dynarate-list.rmtype EQ "*" NO-LOCK NO-ERROR.
global-occ = AVAILABLE dynarate-list AND htparam.finteger = 1.
IF global-occ THEN
FOR EACH dynarate-list WHERE dynarate-list.rmtype NE "*":
	DELETE dynarate-list.
END.
ELSE DO:
	FOR EACH dynarate-list :
		FIND FIRST t-zimkateg WHERE t-zimkateg.kurzbez EQ dynarate-list.rmtype NO-LOCK NO-ERROR.
		IF cat-flag THEN DO:
			FIND FIRST temp-list WHERE temp-list.zikatnr EQ t-zimkateg.typ NO-LOCK NO-ERROR.
			IF NOT AVAILABLE temp-list THEN
				DELETE dynarate-list.
		END.
		ELSE DO:
			FIND FIRST temp-list WHERE temp-list.zikatnr EQ t-zimkateg.zikatnr NO-LOCK NO-ERROR.
			IF NOT AVAILABLE temp-list THEN
				DELETE dynarate-list.
		END.
		
	END.
	
END.
FIND FIRST dynarate-list NO-ERROR.
IF AVAILABLE dynarate-list THEN
DO:
	/*NC - 20/07/23 for STATIC RateCode according contract rate setup*/
	FOR EACH dynarate-list:
		FIND FIRST s-list WHERE s-list.static-code = dynarate-list.rcode  NO-LOCK NO-ERROR.
		IF NOT AVAILABLE s-list THEN
		DO:
			CREATE s-list.
			s-list.static-code = dynarate-list.rcode.
		END.
	END.
		
	FOR EACH s-list :
		IF cat-flag THEN
		DO:
			FOR EACH ratecode WHERE ratecode.CODE EQ s-list.static-code
				AND ratecode.startperiode LE tdate
				AND ratecode.endperiode GE fdate
				AND ratecode.erwachs GT 0 NO-LOCK :
					FIND FIRST t-zimkateg WHERE t-zimkateg.zikatnr EQ ratecode.zikatnr NO-LOCK NO-ERROR.
					FIND FIRST temp-list WHERE temp-list.zikatnr EQ t-zimkateg.typ NO-LOCK NO-ERROR.
					IF AVAILABLE temp-list THEN DO:
						CREATE bratecode.
						BUFFER-COPY ratecode TO bratecode.
					END.
				
			END.
		END.
		ELSE DO:
			FOR EACH ratecode WHERE ratecode.CODE EQ s-list.static-code
				AND ratecode.startperiode LE tdate 
				AND ratecode.endperiode GE fdate
				AND ratecode.erwachs GT 0 NO-LOCK :
					FIND FIRST temp-list WHERE temp-list.zikatnr EQ ratecode.zikatnr NO-LOCK NO-ERROR.
					IF AVAILABLE temp-list THEN DO:
						CREATE bratecode.
						BUFFER-COPY ratecode TO bratecode.
					END.
				
			END.
		END.
	END.

END.

DO TRANSACTION :
IF pushALL OR start-counter = 0 OR re-calculateRate OR createRate THEN 
DO :

    DEFINE VARIABLE n     AS INT INIT 0.
    DEFINE VARIABLE m     AS INT INIT 0.

    DEFINE VARIABLE k     AS INT INIT 0.
    DEFINE VARIABLE j     AS INT INIT 0.
	
	ASSIGN 
		loopi = 0
		loopj = 0
	.

    IF pushPax THEN
        ASSIGN n = 1 k = 0. /*NC- reassign m and j move down*/
    ELSE ASSIGN n = adult m = adult k = 0 j = 0.
	IF createRate THEN
		FIND FIRST t-qsy171 WHERE t-qsy171.char1 = "" AND t-qsy171.date1 EQ tdate NO-LOCK NO-ERROR.
	ELSE
		FIND FIRST t-qsy171 WHERE t-qsy171.char1 = "" NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE t-qsy171:
        ASSIGN w-day = wd-array[WEEKDAY(t-qsy171.date1)]. 
        FOR EACH r-list NO-LOCK,
            FIRST bqueasy WHERE bqueasy.char1 = r-list.rcode NO-LOCK
            /*BY bqueasy.logi2 
            BY bqueasy.number3 DESCENDING /* min advance booking */
            BY bqueasy.deci3 DESCENDING */  /* max advance booking */:

            do-it = YES.

            IF cat-flag THEN
                FIND FIRST t-zimkateg WHERE t-zimkateg.typ = t-qsy171.number1 NO-LOCK NO-ERROR.
            ELSE 
                FIND FIRST t-zimkateg WHERE t-zimkateg.zikatnr = t-qsy171.number1 NO-LOCK NO-ERROR.
                
            FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.char1 = r-list.rcode AND queasy.date1 = 
                t-qsy171.date1 AND queasy.number1 = t-qsy171.number1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN do-it = NO. /*FT 200217*/ /*check if queasy 170 still exist*/
                
            /* minimum advance booking not fulfilled */
            ELSE IF bqueasy.number3 GT 0 AND bqueasy.number3 GT (ankunft - ci-date) THEN do-it = NO. /*#6E8759*/
            
            /* maximum advance booking not fulfilled */
            ELSE IF bqueasy.deci3 GT 0 AND bqueasy.deci3 LT (ankunft - ci-date) THEN do-it = NO. 
            
            IF NOT do-it THEN.

            ELSE IF NOT bqueasy.logi2 THEN  /*static*/
            DO:
				IF pushpax THEN 
				DO:
					FOR EACH ratecode WHERE ratecode.CODE = r-list.rcode
                    AND ratecode.zikatnr = t-zimkateg.zikatnr
                    AND ratecode.startperiode LE t-qsy171.date1
                    AND ratecode.endperiode GE t-qsy171.date1 
					AND ratecode.erwachs GT 0 NO-LOCK BY ratecode.erwachs DESC:
						ASSIGN
                            m = ratecode.erwachs
							j = ratecode.kind1.
						LEAVE. 
					END.
				END.

                DO loopi = n TO m:
					/*DO loopj = k TO j:*/ /*static ratecode direct queary to table ratecode*/
						FIND FIRST ratecode WHERE ratecode.CODE = r-list.rcode 
							AND ratecode.zikatnr = t-zimkateg.zikatnr 
							AND ratecode.startperiode LE t-qsy171.date1
							AND ratecode.endperiode GE t-qsy171.date1
							AND ratecode.wday = w-day 
							AND ratecode.kind1   = /* loopj */ child
							AND ratecode.erwachs = loopi NO-LOCK NO-ERROR.
						IF NOT AVAILABLE ratecode THEN
							FIND FIRST ratecode WHERE ratecode.CODE = r-list.rcode 
								AND ratecode.zikatnr = t-zimkateg.zikatnr 
								AND ratecode.startperiode LE t-qsy171.date1
								AND ratecode.endperiode GE t-qsy171.date1
								AND ratecode.wday = 0
								AND ratecode.kind1   = /*loopj*/ child
								AND ratecode.erwachs = loopi NO-LOCK NO-ERROR.
						IF AVAILABLE ratecode THEN
						DO:
							FIND FIRST t-arrangement WHERE t-arrangement.argtnr = ratecode.argtnr  NO-LOCK NO-ERROR.
                            IF AVAILABLE t-arrangement THEN
							DO:                            
								FIND FIRST artikel WHERE artikel.artnr = t-arrangement.argt-artikelnr NO-LOCK NO-ERROR.
								IF AVAILABLE artikel THEN
									RUN calc-servvat.p (artikel.departement, artikel.artnr, t-qsy171.date1,
												artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
							END.

							counter = counter + 1.
							CREATE rate-list.
							ASSIGN
								rate-list.zikatnr      = t-qsy171.number1
								rate-list.rcode        = ratecode.CODE
								rate-list.startperiode = t-qsy171.date1
								rate-list.endperiode   = t-qsy171.date1
								rate-list.counter      = counter
								rate-list.pax          = ratecode.erwachs
								rate-list.child        = ratecode.kind1.
							IF ratecode.erwachs NE 0 THEN
								rate-list.rmrate = ratecode.zipreis.
							ELSE rate-list.rmrate = ratecode.ch1preis.

							IF NOT tax-included THEN                               
								rate-list.rmrate        = ROUND(DECIMAL(rate-list.rmrate * (1 + serv + vat)),0).

							FIND FIRST t-qsy18 WHERE t-qsy18.number1 = ratecode.marknr NO-LOCK NO-ERROR.
							IF AVAILABLE t-qsy18 THEN
							DO:
								FIND FIRST t-waehrung WHERE t-waehrung.wabkurz = t-qsy18.char3 NO-LOCK NO-ERROR.
								IF AVAILABLE t-waehrung THEN
								DO:
									FIND FIRST q-curr WHERE q-curr.char1 = t-waehrung.wabkurz 
										AND q-curr.number1 = beCode NO-LOCK NO-ERROR.
									IF AVAILABLE q-curr THEN rate-list.currency = q-curr.char2.
									ELSE rate-list.currency = "IDR".
								END.
								ELSE rate-list.currency = "IDR".
							END.
							IF cat-flag THEN
							DO:
								FIND FIRST t-qsy152 WHERE t-qsy152.number1 = t-qsy171.number1 NO-LOCK NO-ERROR.
								IF AVAILABLE t-qsy152 THEN
								rate-list.bezeich = t-qsy152.char1.
							END.
							ELSE ASSIGN rate-list.bezeich = t-zimkateg.kurzbez.
							
						END.
					/* END. */
                END.
            END. /*end if not logi2*/
            ELSE IF bqueasy.logi2 THEN  /*dynamic rate*/
            DO: 
				ASSIGN
				curr-scode = ""
                occ-room = 0.
				RUN count-availability (t-qsy171.date1, t-qsy171.number1, OUTPUT occ-room). /*NC-08/09/21 occ from 171 cannot use to calc for global reservation */
                /*IF global-occ THEN
                    FOR EACH queasy WHERE queasy.KEY = 171 AND queasy.date1 = t-qsy171.date1 AND queasy.char1 = "":
                        occ-room = occ-room + queasy.number2.
                    END.
                ELSE occ-room = t-qsy171.number2.*/
				
				IF NOT global-occ THEN
				DO:
					FIND FIRST dynarate-list WHERE dynarate-list.w-day = w-day
						AND dynarate-list.days1 = 0
						AND dynarate-list.days2 = 0 
						AND dynarate-list.fr-room LE occ-room
						AND dynarate-list.to-room GE occ-room 
						AND dynarate-list.dynaCode EQ r-list.rcode 
						AND dynarate-list.rmType EQ t-zimkateg.kurzbez NO-LOCK NO-ERROR.
					IF NOT AVAILABLE dynarate-list THEN DO:
						FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
							AND dynarate-list.days1 = 0
							AND dynarate-list.days2 = 0 
							AND dynarate-list.fr-room LE occ-room
							AND dynarate-list.to-room GE occ-room 
							AND dynarate-list.dynaCode EQ r-list.rcode 
							AND dynarate-list.rmType EQ t-zimkateg.kurzbez NO-LOCK NO-ERROR.
					END.
				END.
				ELSE DO:
					FIND FIRST dynarate-list WHERE dynarate-list.w-day = w-day
						AND dynarate-list.days1 = 0
						AND dynarate-list.days2 = 0 
						AND dynarate-list.fr-room LE occ-room
						AND dynarate-list.to-room GE occ-room 
						AND dynarate-list.dynaCode EQ r-list.rcode NO-LOCK NO-ERROR.
					IF NOT AVAILABLE dynarate-list THEN
						FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
							AND dynarate-list.days1 = 0
							AND dynarate-list.days2 = 0 
							AND dynarate-list.fr-room LE occ-room
							AND dynarate-list.to-room GE occ-room 
							AND dynarate-list.dynaCode EQ r-list.rcode NO-LOCK NO-ERROR.
				END.
                IF AVAILABLE dynarate-list THEN
                DO:
                    IF NOT global-occ THEN
					DO:
						FIND FIRST t-qsy145 WHERE t-qsy145.char1    = r-list.rcode 
							AND t-qsy145.char2    = dynarate-list.rCode 
							AND t-qsy145.number1  = t-zimkateg.zikatnr
							AND t-qsy145.deci1    = dynarate-list.w-day
							AND t-qsy145.deci2    = dynarate-list.counter 
							AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
						/* if a particular DayofWeek is not found then search for DW 0 as the default value (CRG 25/02/2022) */
                        IF NOT AVAILABLE t-qsy145 THEN
                            FIND FIRST t-qsy145 WHERE 
                                    t-qsy145.char1    = r-list.rcode 
                                AND t-qsy145.char2    = dynarate-list.rCode 
                                AND t-qsy145.number1  = t-zimkateg.zikatnr
                                AND t-qsy145.deci1    = 0
                                AND t-qsy145.deci2    = dynarate-list.counter 
                                AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
					END.
                    ELSE 
					DO:
                        FIND FIRST t-qsy145 WHERE t-qsy145.char1 = r-list.rcode 
                            AND t-qsy145.char2    = dynarate-list.rCode 
                            AND t-qsy145.number1  = 0
                            AND t-qsy145.deci1    = dynarate-list.w-day
                            AND t-qsy145.deci2    = dynarate-list.counter 
                            AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
						IF NOT AVAILABLE t-qsy145 THEN
                            FIND FIRST t-qsy145 WHERE 
                                    t-qsy145.char1    = r-list.rcode 
                                AND t-qsy145.char2    = dynarate-list.rCode 
                                AND t-qsy145.number1  = 0
                                AND t-qsy145.deci1    = 0
                                AND t-qsy145.deci2    = dynarate-list.counter 
                                AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
					END.
                    IF AVAILABLE t-qsy145 THEN
                    curr-scode  = t-qsy145.char3.
					ELSE curr-scode = dynarate-list.rCode.     
					
					IF pushpax THEN 
					DO:
						FOR EACH bratecode WHERE bratecode.CODE = curr-scode
                        AND bratecode.zikatnr = t-zimkateg.zikatnr
                        AND bratecode.startperiode LE t-qsy171.date1
                        AND bratecode.endperiode GE t-qsy171.date1 
						AND bratecode.erwachs GT 0 NO-LOCK BY bratecode.erwachs DESC:
						
							 ASSIGN
                                m = bratecode.erwachs
								j = bratecode.kind1.
							LEAVE.
						END.
					END. 
                    
                    DO loopi = n TO m:
						
						/* DO loopj = k TO j: */
							FIND FIRST bratecode WHERE bratecode.CODE = curr-scode
								AND bratecode.zikatnr = t-zimkateg.zikatnr 
								AND bratecode.erwachs = loopi
								AND bratecode.kind1   = /* loopj */ child
								AND bratecode.startperiode LE t-qsy171.date1
								AND bratecode.endperiode GE t-qsy171.date1
								AND bratecode.wday = w-day  NO-LOCK NO-ERROR.
							IF NOT AVAILABLE bratecode THEN
								FIND FIRST bratecode WHERE bratecode.CODE = curr-scode 
									AND bratecode.zikatnr = t-zimkateg.zikatnr 
									AND bratecode.erwachs = loopi
									AND bratecode.kind1   = /* loopj */ child
									AND bratecode.startperiode LE t-qsy171.date1
									AND bratecode.endperiode GE t-qsy171.date1
									AND bratecode.wday = 0 NO-LOCK NO-ERROR.
							IF AVAILABLE bratecode THEN
							DO:
								
								FIND FIRST t-arrangement WHERE t-arrangement.argtnr = bratecode.argtnr  NO-LOCK NO-ERROR.
								IF AVAILABLE t-arrangement THEN
								DO:                            
									FIND FIRST artikel WHERE artikel.artnr = t-arrangement.argt-artikelnr NO-LOCK NO-ERROR.
									IF AVAILABLE artikel THEN
										RUN calc-servvat.p (artikel.departement, artikel.artnr, t-qsy171.date1,
													artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
								END.

								counter = counter + 1.
								CREATE rate-list.
								ASSIGN
									rate-list.zikatnr       = t-qsy171.number1
									rate-list.rcode         = r-list.rcode
									rate-list.startperiode  = t-qsy171.date1
									rate-list.endperiode    = t-qsy171.date1
									rate-list.counter       = counter
									rate-list.scode         = curr-scode 
									rate-list.pax           = bratecode.erwachs
									rate-list.child         = bratecode.kind1
								.
								IF bratecode.erwachs NE 0 THEN
									rate-list.rmrate = bratecode.zipreis.
								ELSE rate-list.rmrate = bratecode.ch1preis.

								IF NOT tax-included THEN                               
									rate-list.rmrate        = ROUND(DECIMAL(rate-list.rmrate * (1 + serv + vat)),0).

								FIND FIRST t-qsy18 WHERE t-qsy18.number1 = bratecode.marknr NO-LOCK NO-ERROR.
							
								FIND FIRST t-waehrung WHERE t-waehrung.wabkurz = t-qsy18.char3 NO-LOCK NO-ERROR.
								IF AVAILABLE t-waehrung THEN
								DO:
									FIND FIRST q-curr WHERE q-curr.char1 = t-waehrung.wabkurz 
										AND q-curr.number1 = beCode NO-LOCK NO-ERROR.
									IF AVAILABLE q-curr THEN rate-list.currency = q-curr.char2.
									ELSE rate-list.currency = "IDR".
								END.
								ELSE rate-list.currency = "IDR".
				
								IF cat-flag THEN
								DO:
									FIND FIRST t-qsy152 WHERE t-qsy152.number1 = t-qsy171.number1 NO-LOCK NO-ERROR.
									rate-list.bezeich = t-qsy152.char1.
								END.
								ELSE  
								DO:
									
									rate-list.bezeich = t-zimkateg.kurzbez.
								END.
								
							END.
						/* END. */
                    END.
                END.
            END.
        END. /*end for each r-list*/
		IF createRate THEN
			FIND NEXT t-qsy171 WHERE t-qsy171.char1 = "" AND t-qsy171.date1 EQ tdate NO-LOCK NO-ERROR.
		ELSE
			FIND NEXT t-qsy171 WHERE t-qsy171.char1 = "" NO-LOCK NO-ERROR.
    END. /*end do while*/

    FIND FIRST rate-list WHERE rate-list.startperiode GE fdate AND rate-list.endperiode LE tdate NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE rate-list:
		
        FIND FIRST t-qsy170 WHERE t-qsy170.char1 = rate-list.rcode 
            AND t-qsy170.number1 = rate-list.zikatnr AND t-qsy170.date1 = rate-list.startperiode 
            AND t-qsy170.number2 = rate-list.pax AND t-qsy170.number3 = rate-list.child AND t-qsy170.betriebsnr = beCode NO-LOCK NO-ERROR.
        IF AVAILABLE t-qsy170 AND t-qsy170.deci1 = rate-list.rmrate THEN
        DO:
            IF t-qsy170.logi1 THEN rate-list.flag = YES.
            ELSE rate-list.flag = NO.
        END.                            
        ELSE IF AVAILABLE t-qsy170 AND t-qsy170.deci1 NE rate-list.rmrate THEN
        DO:
			
				FIND FIRST qsy WHERE RECID(qsy) = RECID(t-qsy170) NO-LOCK NO-ERROR.
				IF AVAILABLE qsy THEN 
				DO:
					FIND CURRENT qsy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
					ASSIGN
						qsy.logi1 = YES
						qsy.deci1 = rate-list.rmrate
						qsy.char2 = rate-list.scode.
					FIND CURRENT qsy NO-LOCK.
					RELEASE qsy.
				END.
		
        END.
		ELSE IF NOT AVAILABLE t-qsy170 THEN
        DO: /*NC - 31/03/21*/

			CREATE t-queasy.
			ASSIGN
			t-queasy.KEY     = 170
			t-queasy.date1   = rate-list.startperiode
			t-queasy.number1 = rate-list.zikatnr
			t-queasy.number2 = rate-list.pax
			t-queasy.number3 = rate-list.child
			t-queasy.deci1   = rate-list.rmrate
			t-queasy.char1   = rate-list.rcode
			t-queasy.char2   = rate-list.scode
			t-queasy.char3   = rate-list.currency
			t-queasy.betriebsnr   = beCode
		.
			IF createRate THEN
				ASSIGN 
					t-queasy.logi1   = NO
					t-queasy.logi2   = NO
					t-queasy.logi3   = YES
				.
        END. 
        FIND NEXT rate-list  WHERE rate-list.startperiode GE fdate AND rate-list.endperiode LE tdate NO-LOCK NO-ERROR.
    END.
	
	IF createRate THEN. /*NC - 12/03/24 push-rate-list created at the bottom */
	ELSE /*NC - 31/03/21*/                 
	FOR EACH rate-list WHERE rate-list.startperiode GE fdate AND rate-list.endperiode LE tdate AND rate-list.flag NO-LOCK:

		CREATE push-rate-list.
		BUFFER-COPY rate-list TO push-rate-list.
	END.
END.
END.

FOR EACH t-queasy :
  CREATE bqsy170.
  BUFFER-COPY t-queasy TO bqsy170.
  /* q-recid = RECID(bqsy170).*/ 
END.
/* NC - solved use DO TRANSACTION #FE9976
curr-recid = 0.
FOR EACH queasy WHERE queasy.KEY = 170 AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK:
	curr-recid = curr-recid + 1.
END.

IF curr-recid GE 500 THEN
	FOR EACH queasy WHERE queasy.KEY = 170 AND queasy.logi1 AND queasy.betriebsnr = beCode :
	
			ASSIGN 
				queasy.logi2 = NO
				queasy.logi1 = NO.
			
		
	END.
*/
/*NC - 22/07/23 use when delta only
DO TRANSACTION:*/
IF pushPax THEN /*NC - 14/01/22 queasy 170 pax 1 or pax 0 can be exist from trigger contract rate */
DO:
	FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.number2 EQ 0 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	IF AVAILABLE queasy THEN
	DO :
		FOR EACH bqsy170 WHERE bqsy170.KEY = 170 AND bqsy170.number2 EQ 0 AND bqsy170.betriebsnr = beCode EXCLUSIVE-LOCK :
				DELETE bqsy170.
		END.
	END.
END.
ELSE
DO:
	FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.number2 LE 1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	IF AVAILABLE queasy THEN
	DO:
		FOR EACH bqsy170 WHERE bqsy170.KEY = 170 AND bqsy170.number2 LE 1 AND bqsy170.betriebsnr = beCode EXCLUSIVE-LOCK :
			DELETE bqsy170.
		END.
	END.

END.
IF NOT pushALL OR NOT createRate THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 170 AND queasy.logi2 AND queasy.betriebsnr = beCode NO-LOCK :
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) NO-LOCK NO-ERROR.
        IF AVAILABLE qsy THEN
        DO:
			FIND CURRENT qsy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            ASSIGN
                qsy.logi1 = qsy.logi2
                qsy.logi2 = NO.

            FIND CURRENT qsy NO-LOCK.
            RELEASE qsy.
        END.
    END.
	/*NC - 22/07/23 use when delta only
	FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	REPEAT WHILE AVAILABLE queasy:
		CREATE t-qsy170.
		BUFFER-COPY queasy TO t-qsy170.
		ASSIGN t-qsy170.rec-id = RECID(queasy).
		FIND NEXT queasy WHERE queasy.KEY = 170 AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	END.*/
	/* NC - 30/01/24 move to top, sharing used 
	FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	REPEAT WHILE AVAILABLE queasy:
        FIND FIRST bqueasy WHERE bqueasy.char1 = queasy.char1 NO-LOCK NO-ERROR.
		IF bqueasy.logi2 THEN /*dynamic rate only*/
		DO:
			FOR EACH ratecode WHERE ratecode.CODE = queasy.char1:
				CREATE dynarate-list.
				ASSIGN
					dynarate-list.dynaCode = ratecode.CODE
					ifTask                 = ratecode.char1[5]
				.
				DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
					mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
					mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
					CASE mesToken:
						WHEN "CN" THEN dynarate-list.counter = INTEGER(mesValue).
						WHEN "RT" THEN dynarate-list.rmType  = mesValue.
						WHEN "WD" THEN dynarate-list.w-day   = INTEGER(mesValue).
						WHEN "FR" THEN dynarate-list.fr-room = INTEGER(mesValue).
						WHEN "TR" THEN dynarate-list.to-room = INTEGER(mesValue).
						WHEN "D1" THEN dynarate-list.days1   = INTEGER(mesValue).
						WHEN "D2" THEN dynarate-list.days2   = INTEGER(mesValue).
						WHEN "RC" THEN dynarate-list.rCode   = mesValue.
					END CASE.
				END.

				IF dynarate-list.to-room GT maxroom THEN
				DO:
					ASSIGN
						def-rate = dynarate-list.rCode
						maxroom = dynarate-list.to-room.
				END.  
            END.
		END.
		FIND NEXT queasy WHERE queasy.KEY = 170 AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	END.
	*/
    
    FIND FIRST queasy WHERE queasy.key EQ 170 AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    DO TRANSACTION WHILE AVAILABLE queasy:
        ASSIGN 
            w-day = wd-array[WEEKDAY(queasy.date1)]
            do-it = YES. 
        
        IF cat-flag THEN
            FIND FIRST t-zimkateg WHERE t-zimkateg.typ = queasy.number1 NO-LOCK NO-ERROR.
        ELSE 
            FIND FIRST t-zimkateg WHERE t-zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
            
        FIND FIRST bqueasy WHERE bqueasy.char1 = queasy.char1 NO-LOCK NO-ERROR.
		IF NOT AVAILABLE bqueasy THEN do-it = NO. /*NC - 08/04/25*/
        ELSE IF AVAILABLE bqueasy AND bqueasy.number3 GT 0 AND bqueasy.number3 GT (ankunft - ci-date) THEN do-it = NO. /* minimum advance booking not fulfilled */ /*#6E8759*/
        ELSE IF AVAILABLE bqueasy AND bqueasy.deci3 GT 0 AND bqueasy.deci3 LT (ankunft - ci-date) THEN do-it = NO. /* maximum advance booking not fulfilled */
        IF NOT do-it THEN
        DO :
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) NO-LOCK NO-ERROR.
            IF AVAILABLE qsy THEN
            DO:
				FIND CURRENT qsy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                qsy.logi1 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.
            END.
        END.
        ELSE IF NOT bqueasy.logi2 THEN /* static rate code direct queary to table ratecode */
        DO:
            FIND FIRST ratecode WHERE ratecode.CODE = queasy.char1
                AND ratecode.zikatnr = t-zimkateg.zikatnr
                AND ratecode.erwachs = queasy.number2
                AND ratecode.kind1   = queasy.number3
                AND ratecode.startperiode LE queasy.date1
                AND ratecode.endperiode GE queasy.date1
                AND ratecode.wday = w-day NO-LOCK NO-ERROR.
            IF NOT AVAILABLE ratecode THEN
                FIND FIRST ratecode WHERE ratecode.CODE = queasy.char1
                    AND ratecode.zikatnr = t-zimkateg.zikatnr 
                    AND ratecode.erwachs = queasy.number2
                    AND ratecode.kind1   = queasy.number3
                    AND ratecode.startperiode LE queasy.date1
                    AND ratecode.endperiode GE queasy.date1
                    AND ratecode.wday = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE ratecode THEN
            DO:
                FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) NO-LOCK NO-ERROR.
                IF AVAILABLE qsy THEN
                DO:
					FIND CURRENT qsy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                    IF ratecode.erwachs NE 0 THEN
                    DO:
                        IF ratecode.zipreis NE qsy.deci1 THEN
                            ASSIGN
                                qsy.deci1 = ratecode.zipreis
                                qsy.logi3 = YES
                                qsy.logi1 = NO
								/* t-qsy170.logi1 = NO
								t-qsy170.logi3 = YES
								t-qsy170.deci1 = ratecode.zipreis. */
								.
                        ELSE 
							ASSIGN
								/* t-qsy170.logi1 = NO */
								qsy.logi1 = NO.
                    END.
                    ELSE IF ratecode.kind1 NE 0 THEN
                    DO:
                        IF ratecode.ch1preis NE qsy.deci1 THEN
                            ASSIGN
                                qsy.deci1 = ratecode.ch1preis
                                qsy.logi3 = YES
                                qsy.logi1 = NO
								/* t-qsy170.logi1 = NO
								t-qsy170.logi3 = YES
								t-qsy170.deci1 = ratecode.zipreis */
								.
                        ELSE ASSIGN 
							/* t-qsy170.logi1 = NO */
							qsy.logi1 = NO.
                    END.
                    
                    FIND CURRENT qsy NO-LOCK.
                    RELEASE qsy.
                END.        
            END.                         
        END.
        ELSE IF bqueasy.logi2 THEN /* dynamic rate code */
        DO: 
			ASSIGN
            occ-room = 0
			curr-scode = "".
			RUN count-availability (queasy.date1, queasy.number1, OUTPUT occ-room). /*NC-08/09/21 occ in 171 cannot calc to rate for global reservation */
            /*IF global-occ THEN
                FOR EACH qsy171 WHERE qsy171.KEY = 171 AND qsy171.date1 = queasy.date1 AND qsy171.char1 = "" NO-LOCK:
                    occ-room = occ-room + qsy171.number2.
                END.
            ELSE 
            DO:
                FIND FIRST qsy171 WHERE qsy171.KEY = 171 AND qsy171.date1 = queasy.date1 AND qsy171.number1 = queasy.number1 NO-LOCK NO-ERROR.
                IF AVAILABLE qsy171 THEN occ-room = qsy171.number2.
            END.*/
			IF NOT global-occ THEN
			DO:
				FIND FIRST dynarate-list WHERE dynarate-list.w-day = w-day
					AND dynarate-list.days1 = 0
					AND dynarate-list.days2 = 0 
					AND dynarate-list.fr-room LE occ-room
					AND dynarate-list.to-room GE occ-room 
					AND dynarate-list.dynaCode EQ queasy.char1 
					AND dynarate-list.rmType EQ t-zimkateg.kurzbez NO-LOCK NO-ERROR.
				IF NOT AVAILABLE dynarate-list THEN DO:
					FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
						AND dynarate-list.days1 = 0
						AND dynarate-list.days2 = 0 
						AND dynarate-list.fr-room LE occ-room
						AND dynarate-list.to-room GE occ-room 
						AND dynarate-list.dynaCode EQ queasy.char1 
						AND dynarate-list.rmType EQ t-zimkateg.kurzbez NO-LOCK NO-ERROR.
				END.
			END.
			ELSE DO:
				FIND FIRST dynarate-list WHERE dynarate-list.w-day = w-day
					AND dynarate-list.days1 = 0
					AND dynarate-list.days2 = 0
					AND dynarate-list.fr-room LE occ-room 
					AND dynarate-list.to-room GE occ-room 
					AND dynarate-list.dynaCode EQ queasy.char1 NO-LOCK NO-ERROR.
				IF NOT AVAILABLE dynarate-list THEN
					FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
						AND dynarate-list.days1 = 0
						AND dynarate-list.days2 = 0
						AND dynarate-list.fr-room LE occ-room 
						AND dynarate-list.to-room GE occ-room 
						AND dynarate-list.dynaCode EQ queasy.char1 NO-LOCK NO-ERROR.
			END.
            IF AVAILABLE dynarate-list THEN
            DO:
                IF NOT global-occ THEN
                DO:
                    FIND FIRST qsy WHERE qsy.KEY = 145
                        AND qsy.char1    = queasy.char1 
                        AND qsy.char2    = dynarate-list.rCode 
                        AND qsy.number1  = t-zimkateg.zikatnr
                        AND qsy.deci1    = dynarate-list.w-day
                        AND qsy.deci2    = dynarate-list.counter 
                        AND qsy.date1    = queasy.date1 NO-LOCK NO-ERROR.
                    /* if a particular DayofWeek is not found then search for DW 0 as the default value (CRG 25/02/2022) */
                    IF NOT AVAILABLE qsy THEN
                        FIND FIRST qsy WHERE qsy.KEY = 145
                            AND qsy.char1    = queasy.char1
                            AND qsy.char2    = dynarate-list.rCode 
                            AND qsy.number1  = t-zimkateg.zikatnr
                            AND qsy.deci1    = 0
                            AND qsy.deci2    = dynarate-list.counter 
                            AND qsy.date1    = queasy.date1 NO-LOCK NO-ERROR.
                END.
                ELSE
                DO:

                    FIND FIRST qsy WHERE qsy.KEY = 145
                        AND qsy.char1   = queasy.char1 
                        AND qsy.char2   = dynarate-list.rCode
                        AND qsy.number1 = 0
                        AND qsy.deci1   = dynarate-list.w-day 
                        AND qsy.deci2   = dynarate-list.counter 
                        AND qsy.date1   = queasy.date1 NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE qsy THEN
					DO:
						
                        FIND FIRST qsy WHERE qsy.KEY = 145
                            AND qsy.char1   = queasy.char1 
                            AND qsy.char2   = dynarate-list.rCode
                            AND qsy.number1 = 0
                            AND qsy.deci1   = 0
                            AND qsy.deci2   = dynarate-list.counter 
                            AND qsy.date1   = queasy.date1 NO-LOCK NO-ERROR.
					END.
                END.
                IF AVAILABLE qsy THEN
                    curr-scode  = qsy.char3.
				ELSE curr-scode = dynarate-list.rCode.

                FIND FIRST bratecode WHERE bratecode.CODE = curr-scode
                    AND bratecode.zikatnr = t-zimkateg.zikatnr
                    AND bratecode.kind1   = queasy.number3
                    AND bratecode.erwach  = queasy.number2
                    AND bratecode.startperiode LE queasy.date1
                    AND bratecode.endperiode GE queasy.date1
                    AND bratecode.wday = w-day NO-LOCK NO-ERROR.
                IF NOT AVAILABLE bratecode THEN
                    FIND FIRST bratecode WHERE bratecode.CODE = curr-scode
                        AND bratecode.zikatnr = t-zimkateg.zikatnr
                        AND bratecode.kind1   = queasy.number3
                        AND bratecode.erwach  = queasy.number2
                        AND bratecode.startperiode LE queasy.date1
                        AND bratecode.endperiode GE queasy.date1
                        AND bratecode.wday = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE bratecode THEN
                DO :
                    FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) NO-LOCK NO-ERROR.
                    IF AVAILABLE qsy THEN
                    DO:
						FIND CURRENT qsy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                        IF bratecode.erwachs NE 0 THEN
                        DO:
                            IF bratecode.zipreis NE qsy.deci1 THEN
                            DO:
                                ASSIGN
                                    qsy.deci1 = bratecode.zipreis
                                    qsy.logi3 = YES
                                    qsy.logi1 = NO
									/* t-qsy170.logi1 = NO
									t-qsy170.logi3 = YES
									t-qsy170.deci1 = bratecode.zipreis */
									qsy.char2 = bratecode.CODE
									/* t-qsy170.char2 = bratecode.CODE */
									.
                            END.
                            ELSE ASSIGN 
								/* t-qsy170.logi1 = NO */
								qsy.logi1 = NO.
                        END.
                        ELSE IF bratecode.kind1 NE 0 THEN
                        DO:
                            IF bratecode.ch1preis NE qsy.deci1 THEN
                            DO:
                                ASSIGN
                                    qsy.deci1 = bratecode.zipreis
                                    qsy.logi3 = YES
                                    qsy.logi1 = NO
									/* t-qsy170.logi1 = NO
									t-qsy170.logi3 = YES
									t-qsy170.deci1 = bratecode.zipreis */
									qsy.char2 = bratecode.CODE
									/* t-qsy170.char2 = bratecode.CODE */
									.
                            END.
                             ELSE ASSIGN 
								/* t-qsy170.logi1 = NO */
								qsy.logi1 = NO.
                        END.

                        FIND CURRENT qsy NO-LOCK.
                        RELEASE qsy.
                    END.            
                END.
            END.
        END.
        FIND NEXT queasy WHERE queasy.key EQ 170 AND queasy.logi1 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
    END.
END.
/*END. end transaction*/
/*IF re-calculateRate THEN
    RUN update-bookengine-configbl.p (9,beCode,NO,"").*/
/*NC 01-02-20 pushpax needs other pax to push */
IF pushPax THEN
DO:
	FOR EACH queasy WHERE queasy.KEY = 170 AND queasy.logi3 AND queasy.betriebsnr = beCode NO-LOCK:
		FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.number1 = queasy.number1
				AND qsy.char1 = queasy.char1 AND qsy.date1 = queasy.date1
				AND qsy.logi3 = NO AND qsy.betriebsnr = beCode NO-LOCK NO-ERROR.
		IF AVAILABLE qsy THEN
		DO :
			FIND FIRST currqsy WHERE RECID(currqsy) = RECID(qsy) NO-LOCK NO-ERROR.
			IF AVAILABLE currqsy THEN DO:
				FIND CURRENT currqsy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
				ASSIGN currqsy.logi3 = YES.
				FIND CURRENT currqsy NO-LOCK.
				RELEASE currqsy.
			END.
		END.
	END.
END.

FIND FIRST queasy WHERE queasy.KEY = 170 AND queasy.logi3 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy:
	IF cat-flag THEN
	DO:
		FIND FIRST t-qsy152 WHERE t-qsy152.number1 = queasy.number1 NO-LOCK NO-ERROR.
		IF AVAILABLE t-qsy152 THEN curr-bezeich = t-qsy152.char1.
	END.
	ELSE 
	DO:
		FIND FIRST t-zimkateg WHERE t-zimkateg.zikatnr = queasy.number1 NO-LOCK NO-ERROR.
		IF AVAILABLE t-zimkateg THEN curr-bezeich = t-zimkateg.kurzbez.
	END.
	CREATE push-rate-list.
	ASSIGN
		push-rate-list.rcode        = queasy.char1
		push-rate-list.startperiode = queasy.date1
		push-rate-list.endperiode   = queasy.date1
		push-rate-list.zikatnr      = queasy.number1
		push-rate-list.pax          = queasy.number2
		push-rate-list.child        = queasy.number3
		push-rate-list.rmrate       = queasy.deci1
		push-rate-list.currency     = queasy.char3
		push-rate-list.bezeich 		= curr-bezeich.
	
	FIND NEXT queasy WHERE queasy.KEY = 170 AND queasy.logi3 AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
END.

done = YES. /*NC - 08/04/25 case push-rate-list not created but done still yes*/

/*NC - 31/03/21*/
PROCEDURE create-queasy170:
	DEFINE INPUT PARAMETER q-date 	 AS DATE.
	DEFINE INPUT PARAMETER q-zikatnr AS INT.
	DEFINE INPUT PARAMETER q-pax 	 AS INT.
	DEFINE INPUT PARAMETER q-child 	 AS INT.
	DEFINE INPUT PARAMETER q-rmrate  AS DECIMAL FORMAT ">>>,>>>,>>9.99".
	DEFINE INPUT PARAMETER q-rcode 	 AS CHAR.
	DEFINE INPUT PARAMETER q-scode 	 AS CHAR.
	DEFINE INPUT PARAMETER q-currency AS CHAR.


	CREATE queasy.

     ASSIGN
		queasy.KEY     = 170
		queasy.date1   = q-date
		queasy.number1 = q-zikatnr
		queasy.number2 = q-pax
		queasy.number3 = q-child
		queasy.deci1   = q-rmrate
		queasy.char1   = q-rcode
		queasy.char2   = q-scode
		queasy.char3   = q-currency
		queasy.betriebsnr = beCode
    . 

END.

PROCEDURE count-availability:
    DEFINE INPUT PARAMETER curr-date AS DATE.
    DEFINE INPUT PARAMETER i-typ   AS INT.
    DEFINE OUTPUT PARAMETER rm-occ   AS INT.
    
    DEFINE VARIABLE vhp-limited AS LOGICAL INIT NO NO-UNDO.
    DEFINE VARIABLE do-it       AS LOGICAL INIT NO NO-UNDO.
	DEFINE VARIABLE rm-allot    AS INTEGER NO-UNDO.
	ASSIGN
		rm-occ = 0
		rm-allot = 0
		grpcode = "".
	FOR EACH grtype :
		DELETE grtype.
	END.
	IF NOT splited-occ THEN DO:	
		
		IF global-occ THEN
		DO:
			/*GLOBAL RESERVATION all Room type*/
			FOR EACH kontline WHERE kontline.kontstat = 1 AND kontline.betriebsnr = 1
				AND curr-date GE kontline.ankunft AND curr-date LE kontline.abreise NO-LOCK :
				/*
				IF allotment AND kontline.betriebsnr = 0 THEN 
					do-it = YES.
				ELSE IF NOT allotment AND kontline.betriebsnr = 1 THEN 
					do-it = YES.
				IF do-it THEN
				DO:
					IF cat-flag AND zimkateg.typ = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
					ELSE IF NOT cat-flag AND zimkateg.zikatnr = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
				END.*/
				
				rm-allot = rm-allot + kontline.zimmeranz.
			END.
			FIND FIRST bresline WHERE bresline.active-flag LE 1 
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
				AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
				AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
				AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
				AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
			DO WHILE AVAILABLE bresline :   
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
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
				AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
				AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
				AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
				AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
			END. 

			rm-occ = rm-occ + rm-allot. 
		END.
		IF NOT global-occ THEN
		DO:
			IF cat-flag THEN 
			DO:
				FIND FIRST t-zimkateg WHERE t-zimkateg.typ = i-typ  NO-ERROR.
				IF AVAILABLE t-zimkateg THEN
					i-typ = t-zimkateg.zikatnr.
			END.		
		/*GLOBAL RESERVATION for spesific RT*/
			FOR EACH kontline WHERE kontline.kontstat = 1 AND kontline.betriebsnr = 1 AND kontline.zikatnr = i-typ AND curr-date GE kontline.ankunft AND curr-date LE kontline.abreise NO-LOCK :
				/*
				IF allotment AND kontline.betriebsnr = 0 THEN 
					do-it = YES.
				ELSE IF NOT allotment AND kontline.betriebsnr = 1 THEN 
					do-it = YES.
				IF do-it THEN
				DO:
					IF cat-flag AND zimkateg.typ = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
					ELSE IF NOT cat-flag AND zimkateg.zikatnr = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
				END.*/
				rm-allot = rm-allot + kontline.zimmeranz.
			END.
			FIND FIRST bresline WHERE bresline.active-flag LE 1 
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
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
						NO-LOCK NO-ERROR.
					IF AVAILABLE reservation THEN
					DO:
						FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
							NO-LOCK NO-ERROR.
						do-it = AVAILABLE segment AND segment.vip-level = 0.
					END.
					ELSE do-it = NO.
				END.
		
				IF do-it THEN 
					rm-occ = rm-occ + bresline.zimmeranz. 
				
				/*Find reservation that using global reservation*/
				FIND FIRST kline WHERE kline.kontignr = bresline.kontignr 
					AND kline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kline THEN
				DO:
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
							IF AVAILABLE reservation THEN
							DO:
							FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
								NO-LOCK NO-ERROR.
							do-it = AVAILABLE segment AND segment.vip-level = 0.
							END.
							ELSE do-it = NO.
						END.
				
						IF do-it THEN 
						DO:
							rm-allot = rm-allot - bresline.zimmeranz. 
						END.
					END.    
				END.
				FIND NEXT bresline WHERE bresline.active-flag LE 1 
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
				AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
				AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
				AND bresline.zikatnr = i-typ 
				AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
				AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
			END.
			
			rm-occ = rm-occ + rm-allot. 
		END.
	END.
	
	IF splited-occ THEN DO:	
		IF cat-flag THEN 
		DO:
			FIND FIRST t-zimkateg WHERE t-zimkateg.typ = i-typ  NO-ERROR.
			IF AVAILABLE t-zimkateg THEN
				i-typ = t-zimkateg.zikatnr.
		END.
		FIND FIRST grp-type WHERE grp-type.rm-type = i-typ NO-ERROR.
		IF AVAILABLE grp-type THEN DO:
			ASSIGN grpcode = grp-type.gtype.
			FOR EACH grp-type WHERE grp-type.gtype EQ grpcode :
				CREATE grtype.
				BUFFER-COPY grp-type TO grtype.
			END.
		END.
		IF global-occ THEN
		DO:
			/*GLOBAL RESERVATION all Room type*/
			FOR EACH kontline WHERE kontline.kontstat = 1 AND kontline.betriebsnr = 1
				AND curr-date GE kontline.ankunft AND curr-date LE kontline.abreise NO-LOCK,
				FIRST grtype WHERE grtype.rm-type = kontline.zikatnr :
				/*
				IF allotment AND kontline.betriebsnr = 0 THEN 
					do-it = YES.
				ELSE IF NOT allotment AND kontline.betriebsnr = 1 THEN 
					do-it = YES.
				IF do-it THEN
				DO:
					IF cat-flag AND zimkateg.typ = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
					ELSE IF NOT cat-flag AND zimkateg.zikatnr = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
				END.*/
				
				rm-allot = rm-allot + kontline.zimmeranz.
			END.
			FIND FIRST bresline WHERE bresline.active-flag LE 1 
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
				AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
				AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
				AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
				AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
				
			DO WHILE AVAILABLE bresline : 
				FIND FIRST grtype WHERE grtype.rm-type = bresline.zikatnr NO-ERROR.
				IF AVAILABLE grtype THEN DO:
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
				END.
				FIND NEXT bresline WHERE bresline.active-flag LE 1 
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
				AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
				AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
				AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
				AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
				
			END. 

			rm-occ = rm-occ + rm-allot. 
		END.
		IF NOT global-occ THEN
		DO:
			IF cat-flag THEN 
			DO:
				FIND FIRST t-zimkateg WHERE t-zimkateg.typ = i-typ  NO-ERROR.
				IF AVAILABLE t-zimkateg THEN
					i-typ = t-zimkateg.zikatnr.
			END.		
		/*GLOBAL RESERVATION for spesific RT*/
			FOR EACH kontline WHERE kontline.kontstat = 1 AND kontline.betriebsnr = 1 AND kontline.zikatnr = i-typ AND curr-date GE kontline.ankunft AND curr-date LE kontline.abreise NO-LOCK :
				/*
				IF allotment AND kontline.betriebsnr = 0 THEN 
					do-it = YES.
				ELSE IF NOT allotment AND kontline.betriebsnr = 1 THEN 
					do-it = YES.
				IF do-it THEN
				DO:
					IF cat-flag AND zimkateg.typ = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
					ELSE IF NOT cat-flag AND zimkateg.zikatnr = i-typ THEN rm-allot = rm-allot + kontline.zimmeranz.
				END.*/
				rm-allot = rm-allot + kontline.zimmeranz.
			END.
			FIND FIRST bresline WHERE bresline.active-flag LE 1 
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
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
						NO-LOCK NO-ERROR.
					IF AVAILABLE reservation THEN
					DO:
						FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
							NO-LOCK NO-ERROR.
						do-it = AVAILABLE segment AND segment.vip-level = 0.
					END.
					ELSE do-it = NO.
				END.
		
				IF do-it THEN 
					rm-occ = rm-occ + bresline.zimmeranz. 
				
				/*Find reservation that using global reservation*/
				FIND FIRST kline WHERE kline.kontignr = bresline.kontignr 
					AND kline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kline THEN
				DO:
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
							IF AVAILABLE reservation THEN
							DO:
							FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
								NO-LOCK NO-ERROR.
							do-it = AVAILABLE segment AND segment.vip-level = 0.
							END.
							ELSE do-it = NO.
						END.
				
						IF do-it THEN 
						DO:
							rm-allot = rm-allot - bresline.zimmeranz. 
						END.
					END.    
				END.
				FIND NEXT bresline WHERE bresline.active-flag LE 1 
				AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
				AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
				AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
				AND bresline.zikatnr = i-typ 
				AND bresline.ankunft LE curr-date AND bresline.abreise GT curr-date 
				AND bresline.kontignr GE 0 AND bresline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
			END.
			
			rm-occ = rm-occ + rm-allot. 
		END.
	END.
END.
/*for testing push rate
DEF VAR curr-pax AS INT INIT 0.
FOR EACH rate-list WHERE rate-list.flag BY rate-list.rcode BY rate-list.zikatnr BY rate-list.pax 
    BY rate-list.startperiode:
    IF curr-rate NE rate-list.rmrate THEN
        ASSIGN
            curr-rcode = rate-list.rcode
            curr-bezeich = rate-list.bezeich
            curr-recid  = rate-list.counter
            curr-rate  = rate-list.rmrate
            curr-pax   = rate-list.pax
        .
    ELSE IF curr-rate = rate-list.rmrate AND (curr-rcode NE rate-list.rcode OR curr-bezeich NE rate-list.bezeich
                                              OR curr-pax NE push-rate-list.pax) THEN
        ASSIGN 
            curr-rcode = rate-list.rcode
            curr-bezeich = rate-list.bezeich
            curr-recid  = rate-list.counter
            curr-rate  = rate-list.rmrate
            curr-pax     = push-rate-list.pax.
    ELSE IF curr-rate = rate-list.rmrate AND curr-rcode = rate-list.rcode AND curr-bezeich = rate-list.bezeich THEN
    DO:
        FIND FIRST buffrate WHERE buffrate.counter = curr-recid EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE buffrate AND (buffrate.endperiode = rate-list.startperiode - 1 OR 
                                   buffrate.endperiode GE rate-list.startperiode)
            AND buffrate.rcode = rate-list.rcode
            AND buffrate.bezeich = rate-list.bezeich THEN
        DO:
            
            IF buffrate.endperiode GT rate-list.endperiode THEN.
            ELSE buffrate.endperiode = rate-list.endperiode.
            DELETE rate-list.
            RELEASE rate-list.
        END.
    END.    
END.


DEFINE VARIABLE filenm AS CHAR INIT "C:\vhp-SM\vhplib\RG\debug3\rate1.csv".
DEFINE STREAM s1.

OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.  
FOR EACH rate-list WHERE rate-list.flag BY rate-list.rcode BY rate-list.zikatnr BY rate-list.startperiode:
    
    PUT STREAM s1 UNFORMATTED 
      rate-list.counter "," rate-list.rcode "," rate-list.bezeich "," STRING(rate-list.pax) ","
      rate-list.startperiode "," rate-list.endperiode "," STRING(rate-list.rmrate) SKIP.
END.
OUTPUT STREAM s1 CLOSE. */

