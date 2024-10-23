/*
    Program       : if-custom-pushall-availBL.p
    Author        : Fadly
    Created       : 05/09/19
    last update   : 20/09/23 by NC
    Purpose       : For push all method on interfacing
                    with parameter from date and to date and roomType(category).
*/

DEFINE TEMP-TABLE allotment NO-UNDO
    FIELD datum     AS DATE
    FIELD zikatnr   AS INT
    FIELD res-allot AS INT
    FIELD allot     AS INT
	FIELD ruecktage AS INT /*NC 20/04/23 used for cutdays*/
.

DEF TEMP-TABLE temp-list NO-UNDO
    FIELD rcode  AS CHAR
    FIELD rmtype AS CHAR
    FIELD zikatnr AS INT
.

DEFINE TEMP-TABLE rmcat-list NO-UNDO
    FIELD zikatnr  AS INTEGER 
    FIELD anzahl   AS INTEGER 
    FIELD typ      AS INTEGER
    FIELD sleeping AS LOGICAL INITIAL YES
. 

DEFINE TEMP-TABLE r-list NO-UNDO
    FIELD rcode    AS CHAR
.

DEFINE INPUT PARAMETER currcode    AS CHAR.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER beCode       AS INTEGER.
DEFINE INPUT PARAMETER inp-str    AS CHAR.
DEFINE INPUT PARAMETER pushrate     AS LOGICAL.
DEFINE INPUT PARAMETER TABLE FOR temp-list.
DEFINE OUTPUT PARAMETER done        AS LOGICAL.
/*
code for without parameter
*/
DEFINE VARIABLE incl-tentative      AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE allotment		    AS LOGICAL INIT NO  NO-UNDO.

DEFINE VARIABLE end-date        AS DATE NO-UNDO.
DEFINE VARIABLE ci-date      	AS DATE NO-UNDO.
DEFINE VARIABLE date-110        AS DATE NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE NO-UNDO.

DEFINE VARIABLE cat-flag        AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE all-room        AS LOGICAL NO-UNDO INIT YES.
DEFINE VARIABLE do-it           AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE bedsetup	    AS LOGICAL NO-UNDO INIT NO.

DEFINE VARIABLE catnr           AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE cm-gastno       AS INTEGER NO-UNDO INIT 0. 
DEFINE VARIABLE i               AS INTEGER NO-UNDO INIT 0.

DEFINE BUFFER qsy   FOR queasy.
DEFINE BUFFER kline FOR kontline.

DEFINE VARIABLE rm-occ AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE rm-ooo AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE rm-allot AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE occ-room AS INT INIT 0 NO-UNDO.

/*************************************VALIDATION**********************************/
ASSIGN done = NO.
IF NUM-ENTRIES(inp-str,"=") GE 2 THEN
    ASSIGN
        incl-tentative          = LOGICAL(ENTRY(1,inp-str,"="))
        /* re-calculateRate = LOGICAL(ENTRY(2,inp-str,"=")) */
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
IF AVAILABLE queasy THEN cat-flag = YES.
IF bedsetup THEN cat-flag = NO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

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
DO:
    FOR EACH temp-list:
        FIND FIRST r-list WHERE r-list.rcode = temp-list.rcode NO-LOCK NO-ERROR.
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

RUN count-rmcateg.
IF currcode EQ "*" THEN RUN custom-pushall-avail.
ELSE RUN rmtype-pushall-avail.

done = YES.
/*************************************PROCEDURE*************************************/
PROCEDURE custom-pushall-avail:
DEFINE VARIABLE vhp-limited AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE rline-origcode    AS CHAR    NO-UNDO.
DEFINE VARIABLE ifTask      AS CHAR    NO-UNDO.
/*
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 = ""
        AND queasy.date1 GE from-date AND queasy.date1 LE to-date NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
		FIND FIRST rmcat-list WHERE rmcat-list.typ = queasy.number1 NO-LOCK NO-ERROR.
		IF AVAILABLE rmcat-list THEN
		DO:
			 RUN count-availability (queasy.date1,rmcat-list.typ,OUTPUT rm-occ, OUTPUT rm-ooo, OUTPUT rm-allot).
			FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
			IF AVAILABLE qsy THEN DO:
				ASSIGN
					qsy.number3 = rm-ooo
					qsy.logi3 = YES.
				IF allotment THEN
					ASSIGN
                    qsy.number2 = rm-occ + rm-allot.
                ELSE ASSIGN qsy.number2 = rm-occ.
				FIND CURRENT qsy NO-LOCK.				
				RELEASE qsy.
			END.
		END.
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.char1 = ""
            AND queasy.date1 GE from-date AND queasy.date1 LE to-date NO-LOCK NO-ERROR.
    END.
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.char1 NE ""
        AND queasy.date1 GE from-date AND queasy.date1 LE to-date NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
		FIND FIRST rmcat-list WHERE rmcat-list.typ = queasy.number1 NO-LOCK NO-ERROR.
		IF AVAILABLE rmcat-list THEN
		DO:
			FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
			IF AVAILABLE qsy THEN DO:
				ASSIGN
					qsy.number2 = 0
					qsy.logi1 = NO
					qsy.logi2 = NO
					qsy.logi3 = YES.
				RELEASE qsy.
			END.
		END.
        FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.char1 NE ""
            AND queasy.date1 GE from-date AND queasy.date1 LE to-date NO-LOCK NO-ERROR.
    END.
*/	
DO TRANSACTION:
	/*queasy change flag logi3*/
	DO curr-date = from-date TO to-date:
		FOR EACH rmcat-list NO-LOCK:
			ASSIGN
			rm-occ = 0
            rm-ooo = 0
            rm-allot = 0.
			
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date AND queasy.char1 = "" AND queasy.number1 EQ rmcat-list.zikatnr AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
			IF AVAILABLE queasy THEN
			DO:
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
			END.
			ELSE DO:
				RUN count-availability (curr-date,rmcat-list.zikatnr,OUTPUT rm-occ, OUTPUT rm-ooo, OUTPUT rm-allot).
					
				CREATE queasy.
				ASSIGN
					queasy.KEY = 171
					queasy.number1 = rmcat-list.zikatnr
					queasy.number3 = rm-ooo
					queasy.date1 = curr-date
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
			
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date AND queasy.char1 NE "" AND queasy.number1 EQ rmcat-list.zikatnr AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
			IF AVAILABLE queasy THEN DO:
				/*FIND FIRST q-list WHERE q-list.dcode = queasy.char1 AND q-list.zikatnr = queasy.number1 
					AND q-list.allot-flag NO-LOCK NO-ERROR.
				IF AVAILABLE q-list THEN
				DO: */
					occ-room = 0.
					IF cat-flag THEN
						FOR EACH res-line WHERE res-line.active-flag LE 1 
							AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
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
							AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
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
			END.
			
		END.
    END.
END.    
END PROCEDURE.

PROCEDURE rmtype-pushall-avail:
DEFINE VARIABLE vhp-limited AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE rline-origcode    AS CHAR    NO-UNDO.
DEFINE VARIABLE ifTask      AS CHAR    NO-UNDO.
DEFINE VARIABLE zikatnr AS INTEGER INITIAL 0. 

FIND FIRST temp-list WHERE temp-list.rmtype EQ currcode NO-LOCK NO-ERROR.
IF AVAILABLE temp-list THEN zikatnr = temp-list.zikatnr.
DO TRANSACTION:
	/*queasy change flag logi3*/
	DO curr-date = from-date TO to-date:
		/*FOR EACH rmcat-list WHERE rmcat-list.zikatnr = zikatnr NO-LOCK:*/
			ASSIGN
			rm-occ = 0
            rm-ooo = 0
            rm-allot = 0.
			
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date AND queasy.char1 = "" AND queasy.number1 EQ zikatnr AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
			IF AVAILABLE queasy THEN
			DO:
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
			END.
			ELSE DO:
				RUN count-availability (curr-date,zikatnr,OUTPUT rm-occ, OUTPUT rm-ooo, OUTPUT rm-allot).
					
				CREATE queasy.
				ASSIGN
					queasy.KEY = 171
					queasy.number1 = zikatnr
					queasy.number3 = rm-ooo
					queasy.date1 = curr-date
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
			
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date AND queasy.char1 NE "" AND queasy.number1 EQ zikatnr AND queasy.betriebsnr = beCode NO-LOCK NO-ERROR.
			IF AVAILABLE queasy THEN DO:
				/*FIND FIRST q-list WHERE q-list.dcode = queasy.char1 AND q-list.zikatnr = queasy.number1 
					AND q-list.allot-flag NO-LOCK NO-ERROR.
				IF AVAILABLE q-list THEN
				DO: */
					occ-room = 0.
					IF cat-flag THEN
						FOR EACH res-line WHERE res-line.active-flag LE 1 
							AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
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
							AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
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
			END.
			
		/*END.*/
    END.
END.    
END PROCEDURE.

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
        FOR EACH res-line WHERE res-line.active-flag LE 1 
            AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
            AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
            AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
            AND res-line.ankunft LE curr-date AND res-line.abreise GT curr-date 
            AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.typ = i-typ NO-LOCK: 
            
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
				IF allotment AND curr-date GE (ci-date + kline.ruecktage ) THEN
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				ELSE /*NC - 31/08/21 enhanced  kontline.betriebsnr = 1 -> global reservation*/	
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
						rm-allot = rm-allot - res-line.zimmeranz. 
				END.
			END.
			

        END. 
    ELSE
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
				IF allotment AND curr-date GE (ci-date + kline.ruecktage ) THEN
					FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
						AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
				ELSE /*NC - 31/08/21 enhanced  kontline.betriebsnr = 1 -> global reservation*/	
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

    FOR EACH outorder WHERE outorder.betriebsnr LE 1 
        AND curr-date GE outorder.gespstart AND curr-date LE outorder.gespende NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping = YES NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK:

        IF cat-flag AND zimkateg.typ = i-typ THEN rm-ooo = rm-ooo + 1.
        ELSE IF NOT cat-flag AND zimkateg.zikatnr = i-typ THEN rm-ooo = rm-ooo + 1.
    END.
	IF NOT allotment THEN rm-occ = rm-occ + rm-allot.
END.
