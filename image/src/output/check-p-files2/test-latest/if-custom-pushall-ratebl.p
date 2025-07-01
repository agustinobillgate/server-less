/*
    Program       : if-custom-pushall-rateBL.p
    Author        : Fadly
    Created       : 05/09/19
    last update   : 20/09/23 by NC
    Purpose       : For push all method on interfacing
                    with parameter from date and to date and roomType(category).
*/

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

DEFINE TEMP-TABLE temp-list NO-UNDO
    FIELD rcode   AS CHAR
    FIELD rmtype  AS CHAR
    FIELD zikatnr AS INT
.
DEFINE INPUT PARAMETER currcode    AS CHAR.
DEFINE INPUT PARAMETER start-counter  AS INTEGER.
DEFINE INPUT PARAMETER inp-str   AS CHAR.
DEFINE INPUT PARAMETER fdate     AS DATE.
DEFINE INPUT PARAMETER tdate     AS DATE.
DEFINE INPUT PARAMETER adult     AS INTEGER.
DEFINE INPUT PARAMETER child     AS INTEGER.
DEFINE INPUT PARAMETER beCode    AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR temp-list.
DEFINE OUTPUT PARAMETER done     AS LOGICAL.
/*
code for without parameter
*/
DEFINE VARIABLE curr-scode AS CHAR NO-UNDO.
DEFINE VARIABLE rline-origcode  AS CHARACTER NO-UNDO.
DEFINE VARIABLE ifTask          AS CHARACTER NO-UNDO. 
DEFINE VARIABLE def-rate        AS CHARACTER NO-UNDO INIT "".
DEFINE VARIABLE mesToken        AS CHARACTER NO-UNDO.
DEFINE VARIABLE mesValue        AS CHARACTER NO-UNDO.

DEFINE VARIABLE end-date        AS DATE NO-UNDO.
DEFINE VARIABLE start-date      AS DATE NO-UNDO.
DEFINE VARIABLE date-110        AS DATE NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE NO-UNDO.
DEFINE VARIABLE ci-date         AS DATE NO-UNDO.
DEFINE VARIABLE ankunft         AS DATE NO-UNDO.

DEFINE VARIABLE cat-flag        AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE pushPax        	AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE do-it           AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE incl-tentative  AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE tax-included    AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE global-occ      AS LOGICAL NO-UNDO INIT NO.

DEFINE VARIABLE zikatnr         AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE cm-gastno       AS INTEGER NO-UNDO INIT 0. 
DEFINE VARIABLE i               AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE w-day           AS INTEGER NO-UNDO.
DEFINE VARIABLE wd-array        AS INTEGER EXTENT 8 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 
DEFINE VARIABLE maxroom         AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE tokcounter      AS INTEGER NO-UNDO.
DEFINE VARIABLE counter         AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE occ-room        AS INTEGER NO-UNDO INIT 0.

DEFINE VARIABLE serv            AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat             AS DECIMAL NO-UNDO.
DEFINE VARIABLE rmrate          AS DECIMAL FORMAT ">>>,>>>,>>9.99" NO-UNDO.
DEFINE VARIABLE scode           AS CHARACTER NO-UNDO.
DEFINE VARIABLE tmp-date        AS INTEGER NO-UNDO.                             /* Rulita 210124 | Fixing serverless issue git 308 */

DEFINE BUFFER qsy       FOR queasy.
DEFINE BUFFER currqsy   FOR queasy.
DEFINE BUFFER kline 	FOR kontline.
DEFINE BUFFER bqsy170   FOR queasy.
DEFINE BUFFER qsy170    FOR queasy.
DEFINE BUFFER qsy159    FOR queasy.

DEFINE TEMP-TABLE bratecode NO-UNDO LIKE ratecode.
DEFINE TEMP-TABLE t-zimkateg NO-UNDO LIKE zimkateg.
DEFINE TEMP-TABLE t-waehrung NO-UNDO LIKE waehrung.
DEFINE TEMP-TABLE t-arrangement NO-UNDO LIKE arrangement.
DEFINE TEMP-TABLE t-queasy NO-UNDO LIKE queasy .
DEFINE TEMP-TABLE bqueasy NO-UNDO LIKE queasy.  /* qsy.key = 2 */
DEFINE TEMP-TABLE t-qsy18 NO-UNDO LIKE queasy.
DEFINE TEMP-TABLE t-qsy145 NO-UNDO LIKE queasy.
DEFINE TEMP-TABLE t-qsy152 NO-UNDO LIKE queasy.
DEFINE TEMP-TABLE q-curr NO-UNDO LIKE queasy.   /* qsy key = 164 */
DEFINE TEMP-TABLE t-qsy171 NO-UNDO LIKE queasy.
/****************************TEMP-TABLE PREPARATION***********************/
EMPTY TEMP-TABLE bratecode.
EMPTY TEMP-TABLE t-zimkateg.
EMPTY TEMP-TABLE t-waehrung.
EMPTY TEMP-TABLE t-arrangement.
EMPTY TEMP-TABLE t-queasy.
EMPTY TEMP-TABLE bqueasy.
EMPTY TEMP-TABLE t-qsy18.
EMPTY TEMP-TABLE t-qsy145.
EMPTY TEMP-TABLE t-qsy152.
EMPTY TEMP-TABLE q-curr.
EMPTY TEMP-TABLE t-qsy171.


FOR EACH dynarate-list:
	DELETE dynarate-list.
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

FIND FIRST queasy WHERE queasy.KEY = 145 AND queasy.date1 GE fdate AND queasy.date1 LE tdate  NO-LOCK NO-ERROR.
REPEAT WHILE AVAILABLE queasy:
	CREATE t-qsy145.
	BUFFER-COPY queasy TO t-qsy145.
	FIND NEXT queasy WHERE queasy.KEY = 145 AND queasy.date1 GE fdate AND queasy.date1 LE tdate NO-LOCK NO-ERROR.
END.
FIND FIRST t-qsy152 NO-LOCK NO-ERROR.
IF AVAILABLE t-qsy152 THEN cat-flag = YES.

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
IF currcode EQ "*" THEN DO:
	FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 GE fdate AND queasy.date1 LE tdate AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	REPEAT WHILE AVAILABLE queasy:
		CREATE t-qsy171.
		BUFFER-COPY queasy TO t-qsy171.
		FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 GE fdate AND queasy.date1 LE tdate AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	END.
END.
ELSE DO:
	FIND FIRST temp-list WHERE temp-list.rmtype EQ currcode NO-LOCK NO-ERROR.
	IF AVAILABLE temp-list THEN zikatnr = temp-list.zikatnr.
	FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.number1 EQ zikatnr AND queasy.date1 GE fdate AND queasy.date1 LE tdate AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	REPEAT WHILE AVAILABLE queasy:
		CREATE t-qsy171.
		BUFFER-COPY queasy TO t-qsy171.
		FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.number1 EQ zikatnr AND queasy.date1 GE fdate AND queasy.date1 LE tdate AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
	END.
END.

/**********************************VALIDATE************************************/
ASSIGN
    adult = 2
    done = NO.
IF NUM-ENTRIES(inp-str,"=") GE 2 THEN
    ASSIGN
        incl-tentative          = LOGICAL(ENTRY(1,inp-str,"="))
        pushPax					= LOGICAL(ENTRY(2,inp-str,"=")).
FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
tax-included = htparam.flogical.
/*night audit NC - 15/08/23 WHEN NA = yes but invoice date already change to TODAY still can push availability*/

/* Rulita 170125 | Fixing serverless issue git 308 */
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN 
DO:
	ASSIGN date-110 = htparam.fdate.
END.

FIND FIRST htparam WHERE htparam.paramnr = 253 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN 
DO: 
    IF htparam.flogical THEN
    DO:
        IF date-110 LT TODAY THEN RETURN.
    END.
END.
/* End Rulita */

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

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
IF AVAILABLE htparam THEN
ASSIGN ci-date = htparam.fdate.

IF fDate = ci-date THEN ankunft = ci-date.
ELSE ankunft = fDate + 2.

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
DO TRANSACTION:

    DEFINE VARIABLE loopi AS INT INIT 0.
    DEFINE VARIABLE n     AS INT INIT 0.
    DEFINE VARIABLE m     AS INT INIT 0.

    DEFINE VARIABLE loopj AS INT INIT 0.
    DEFINE VARIABLE k     AS INT INIT 0.
    DEFINE VARIABLE j     AS INT INIT 0.
    /* Rulita 090125 | Fixing serverless issue git 308 */
    IF pushPax THEN
        /* ASSIGN n = 1 k = 0. /*NC- reassign m and j move down*/ */
        ASSIGN 
            n = 1 
            k = 0.
    /* ELSE ASSIGN n = adult m = adult k = 0 j = 0. */
    ELSE 
        ASSIGN 
        n = adult 
        m = adult 
        k = 0 
        j = 0.
    /* End Rulita */
	
	FOR EACH r-list NO-LOCK,
        FIRST bqueasy WHERE bqueasy.char1 = r-list.rcode NO-LOCK:
		IF bqueasy.logi2 THEN /*dynamic rate only*/
		DO:
			FOR EACH ratecode WHERE ratecode.CODE = r-list.rcode NO-LOCK:
				CREATE dynarate-list.
				ASSIGN
					dynarate-list.dynacode = ratecode.CODE
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
						WHEN "RC" THEN dynarate-list.rcode   = mesValue.
					END CASE.
				END.

				IF dynarate-list.to-room GT maxroom THEN
				DO:
					ASSIGN
						def-rate = dynarate-list.rcode
						maxroom = dynarate-list.to-room.
				END.  
			END.
		END.
	END.
/* dynamic rate option = 0, 1 or 2 */
	FIND FIRST htparam WHERE htparam.paramnr = 439 NO-LOCK NO-ERROR.
	
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
    
    /* Rulita 210125 | Fixing serverless issue git 308 find first find next chg to for each  */
    /* FIND FIRST t-qsy171 WHERE t-qsy171.char1 = "" NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE t-qsy171: */
    FOR EACH t-qsy171 WHERE t-qsy171.char1 = "" NO-LOCK:
        ASSIGN w-day = wd-array[WEEKDAY(t-qsy171.date1)]. 
        FOR EACH r-list NO-LOCK,
            FIRST bqueasy WHERE bqueasy.char1 = r-list.rcode NO-LOCK
            /*BY bqueasy.logi2 
            BY bqueasy.number3 DESCENDING /* min advance booking */
            BY bqueasy.deci3 DESCENDING */  /* max advance booking */:
            
            IF cat-flag THEN
                FIND FIRST t-zimkateg WHERE t-zimkateg.typ = t-qsy171.number1 NO-LOCK NO-ERROR.
            ELSE 
                FIND FIRST t-zimkateg WHERE t-zimkateg.zikatnr = t-qsy171.number1 NO-LOCK NO-ERROR.

		    /* Rulita 210125 | Fixing serverless issue git 308 */
			tmp-date = ankunft - ci-date.
            /* minimum advance booking not fulfilled */
            /* IF bqueasy.number3 GT (ankunft - ci-date) THEN .  */
            IF bqueasy.number3 GT tmp-date THEN . 
          
            /* maximum advance booking not fulfilled */
            /* ELSE IF bqueasy.deci3 GT 0 AND bqueasy.deci3 LT (ankunft - ci-date) THEN .  */
            ELSE IF bqueasy.deci3 GT 0 AND bqueasy.deci3 LT tmp-date THEN . 
			/* End Rulita */
        
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
						AND dynarate-list.dynacode EQ r-list.rcode 
						AND dynarate-list.rmType EQ t-zimkateg.kurzbez NO-LOCK NO-ERROR.
					IF NOT AVAILABLE dynarate-list THEN DO:
						FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
							AND dynarate-list.days1 = 0
							AND dynarate-list.days2 = 0 
							AND dynarate-list.fr-room LE occ-room
							AND dynarate-list.to-room GE occ-room 
							AND dynarate-list.dynacode EQ r-list.rcode 
							AND dynarate-list.rmType EQ t-zimkateg.kurzbez NO-LOCK NO-ERROR.
					END.
				END.
				ELSE DO:
					FIND FIRST dynarate-list WHERE dynarate-list.w-day = w-day
						AND dynarate-list.days1 = 0
						AND dynarate-list.days2 = 0 
						AND dynarate-list.fr-room LE occ-room
						AND dynarate-list.to-room GE occ-room 
						AND dynarate-list.dynacode EQ r-list.rcode NO-LOCK NO-ERROR.
					IF NOT AVAILABLE dynarate-list THEN
						FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
							AND dynarate-list.days1 = 0
							AND dynarate-list.days2 = 0 
							AND dynarate-list.fr-room LE occ-room
							AND dynarate-list.to-room GE occ-room 
							AND dynarate-list.dynacode EQ r-list.rcode NO-LOCK NO-ERROR.
				END.
                IF AVAILABLE dynarate-list THEN
                DO:
                    IF NOT global-occ THEN
					DO:
						FIND FIRST t-qsy145 WHERE t-qsy145.char1    = r-list.rcode 
							AND t-qsy145.char2    = dynarate-list.rcode 
							AND t-qsy145.number1  = t-zimkateg.zikatnr
							AND t-qsy145.deci1    = dynarate-list.w-day
							AND t-qsy145.deci2    = dynarate-list.counter 
							AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
						/* if a particular DayofWeek is not found then search for DW 0 as the default value (CRG 25/02/2022) */
                        IF NOT AVAILABLE t-qsy145 THEN
                            FIND FIRST t-qsy145 WHERE 
                                    t-qsy145.char1    = r-list.rcode 
                                AND t-qsy145.char2    = dynarate-list.rcode 
                                AND t-qsy145.number1  = t-zimkateg.zikatnr
                                AND t-qsy145.deci1    = 0
                                AND t-qsy145.deci2    = dynarate-list.counter 
                                AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
					END.
                    ELSE 
					DO:
                        FIND FIRST t-qsy145 WHERE t-qsy145.char1 = r-list.rcode 
                            AND t-qsy145.char2    = dynarate-list.rcode 
                            AND t-qsy145.number1  = 0
                            AND t-qsy145.deci1    = dynarate-list.w-day
                            AND t-qsy145.deci2    = dynarate-list.counter 
                            AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
						IF NOT AVAILABLE t-qsy145 THEN
                            FIND FIRST t-qsy145 WHERE 
                                    t-qsy145.char1    = r-list.rcode 
                                AND t-qsy145.char2    = dynarate-list.rcode 
                                AND t-qsy145.number1  = 0
                                AND t-qsy145.deci1    = 0
                                AND t-qsy145.deci2    = dynarate-list.counter 
                                AND t-qsy145.date1    = t-qsy171.date1 NO-LOCK NO-ERROR.
					END.
                    IF AVAILABLE t-qsy145 THEN
                    curr-scode  = t-qsy145.char3.
					ELSE curr-scode = dynarate-list.rcode.     
					
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
/*         FIND NEXT t-qsy171 WHERE t-qsy171.char1 = "" NO-LOCK NO-ERROR. */
/*     END. /*end do while*/                                              */
    END. /* End For each t-qsy171 */
    /* End Rulita */
    
    /* Rulita 210125 | Fixing serverless issue git 308 find first find last chg for each */
    /* FIND FIRST rate-list WHERE rate-list.startperiode GE fdate AND rate-list.endperiode LE tdate NO-LOCK NO-ERROR.
    REPEAT WHILE AVAILABLE rate-list: */
    FOR EACH rate-list WHERE rate-list.startperiode GE fdate AND rate-list.endperiode LE tdate NO-LOCK :
		
        FIND FIRST qsy170 WHERE qsy170.char1 = rate-list.rcode 
            AND qsy170.number1 = rate-list.zikatnr AND qsy170.date1 = rate-list.startperiode 
            AND qsy170.number2 = rate-list.pax AND qsy170.number3 = rate-list.child AND qsy170.betriebsnr = beCode NO-LOCK NO-ERROR.                     
        IF AVAILABLE qsy170 THEN
        DO:
			
				FIND FIRST qsy WHERE RECID(qsy) = RECID(qsy170) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
				IF AVAILABLE qsy THEN 
				DO:
					ASSIGN
						qsy.logi3 = YES
						qsy.deci1 = rate-list.rmrate
						qsy.char2 = rate-list.scode.
					FIND CURRENT qsy NO-LOCK.
					RELEASE qsy.
				END.
		
        END.
		ELSE IF NOT AVAILABLE qsy170 THEN
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
			t-queasy.logi1   = NO
			t-queasy.logi2   = NO
			t-queasy.logi3   = YES
			t-queasy.betriebsnr   = beCode
		.
        END. 
        /* FIND NEXT rate-list  WHERE rate-list.startperiode GE fdate AND rate-list.endperiode LE tdate NO-LOCK NO-ERROR. */
    END. /* End Rulita */
END.
FOR EACH t-queasy :

  CREATE bqsy170.
  BUFFER-COPY t-queasy TO bqsy170.
  /* q-recid = RECID(bqsy170).*/ 

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
		rm-allot = 0.
	
    IF global-occ THEN
	DO:
		/*GLOBAL RESERVATION all Room type*/
		FOR EACH kontline WHERE kontline.kontstat = 1 AND kontline.betriebsnr = 1
            AND curr-date GE kontline.ankunft AND curr-date LE kontline.abreise NO-LOCK:
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
        FOR EACH res-line WHERE res-line.active-flag LE 1 
            AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
            AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
            AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
            AND res-line.ankunft LE curr-date AND res-line.abreise GT curr-date 
            AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
            
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
                rm-occ = rm-occ + res-line.zimmeranz. 
				
			/*Find reservation that using global reservation*/
			FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
				AND kline.kontstat = 1 NO-LOCK NO-ERROR.
			IF AVAILABLE kline THEN
			DO:
				FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
					AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kontline THEN
				DO:
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
						rm-allot = rm-allot - res-line.zimmeranz. 
					END.
				END.    
			END.

        END. 

		rm-occ = rm-occ + rm-allot. 
    END.
	ELSE
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
        FOR EACH res-line WHERE res-line.active-flag LE 1 
            AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
            AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
            AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
            AND res-line.zikatnr = i-typ 
            AND res-line.ankunft LE curr-date AND res-line.abreise GT curr-date 
            AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK:

            do-it = YES. 
            IF res-line.zinr NE "" THEN 
            DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
            END. 
    
            IF do-it AND vhp-limited THEN
            DO:
                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
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
                rm-occ = rm-occ + res-line.zimmeranz. 
			
			/*Find reservation that using global reservation*/
			FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
				AND kline.kontstat = 1 NO-LOCK NO-ERROR.
			IF AVAILABLE kline THEN
			DO:
				FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
					AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				IF AVAILABLE kontline THEN
				DO:
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
						rm-allot = rm-allot - res-line.zimmeranz. 
					END.
				END.    
			END.
        END.
		
		rm-occ = rm-occ + rm-allot. 
	END.
END.
