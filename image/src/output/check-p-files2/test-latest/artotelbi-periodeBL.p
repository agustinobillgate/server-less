DEFINE TEMP-TABLE his-res        
    FIELD resnr          AS INTEGER
    FIELD reslinnr       AS INTEGER
    FIELD staydate       AS DATE
    FIELD ci-date        AS DATE
    FIELD co-date        AS DATE
    FIELD nbrofroom      AS INTEGER
    FIELD room-type-name AS CHARACTER    
    FIELD rm-rev         AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD fb-rev         AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD other-rev      AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD resstatus      AS INTEGER
    FIELD reserveID      AS INTEGER
    FIELD reserveName    AS CHARACTER
    FIELD bookdate       AS DATE
    FIELD booktime       AS CHARACTER
    FIELD rate-code      AS CHARACTER
    FIELD nationality    AS CHARACTER
    FIELD segmentcode    AS CHARACTER
    FIELD cancel-date    AS DATE
    FIELD zinr           AS CHARACTER
    FIELD memozinr       AS CHARACTER /*entry(2,res-line.memozinr,";")*/
    FIELD food-rev       AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD beverage-rev   AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD card-type      AS CHARACTER
    FIELD company-code   AS CHARACTER /*Ref Id*/
    FIELD source-code    AS CHARACTER /*reservation.resart*/
    FIELD adult          AS INTEGER
    FIELD child          AS INTEGER
    FIELD infant         AS INTEGER /*kind2*/
    FIELD compliment     AS INTEGER
    FIELD compliment-ch  AS INTEGER /*l-zuordnung[4]*/
    FIELD age            AS CHARACTER /*zimmer-wunsch matches "ChAge"*/
    FIELD argtnr         AS INTEGER    
    FIELD res-logi       AS LOGICAL INIT YES
    FIELD RTC            AS CHARACTER /*l-zuordnung[1]*/
    FIELD arrangement    AS CHARACTER /*res-line.arrangement*/
    FIELD voucher-nr     AS CHARACTER /*reservation.vesrdepot*/
    FIELD rm-rate        AS DECIMAL FORMAT "->,>>>,>>>,>>9" /*zipreis*/
    FIELD fixed-rate     AS LOGICAL /*available reslin-queasy*/
    FIELD currency       AS CHARACTER /*res-line.betriebsnr - waehrung.waehrungsnr - wabkurz*/
    FIELD guestname      AS CHARACTER /*res-line.name*/
    FIELD bill-receiver  AS CHARACTER /*res-line.gastnrpay*/
    FIELD bill-instruction AS CHARACTER /*res-line.code*/
    FIELD purpose        AS CHARACTER /*zimmer-wunsch matches "SEGM_PUR", QUEASY 143 char3*/
    FIELD grpname        AS CHARACTER /*reservation.groupname*/
    FIELD letterno       AS INTEGER /*reservation.briefnr*/
    FIELD localregion    AS CHARACTER /*guest.nation2*/
    FIELD cancel-reason  AS CHARACTER /*reservation.vesrdepot2*/
    FIELD CODE           AS CHARACTER /*sales-ID guest.phonetik3*/
    FIELD early-booking  AS CHARACTER
    FIELD bona-fide      AS CHARACTER
    FIELD tot-tax        AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD tot-svc        AS DECIMAL FORMAT "->,>>>,>>>,>>9"
.

DEFINE TEMP-TABLE temp-res LIKE his-res.
DEFINE TEMP-TABLE future-res LIKE his-res.
	
DEF TEMP-TABLE rev-list
    FIELD dept     AS INTEGER
    FIELD s-dept   AS CHAR FORMAT "x(20)"   
    FIELD datum    AS DATE
	FIELD s-grp AS CHAR FORMAT "x(20)"
    FIELD subgrp   AS INTEGER
    FIELD s-subgrp AS CHAR FORMAT "x(20)"
    FIELD revart   AS INTEGER
    FIELD s-revart AS CHAR FORMAT "x(20)"
    FIELD amount   AS DECIMAL FORMAT "->,>>>,>>>,>>9"
.

DEFINE TEMP-TABLE b1-list
    FIELD datum         LIKE zinrstat.datum
	FIELD zinr         	LIKE zinrstat.zinr
    FIELD betriebsnr    LIKE zinrstat.betriebsnr
    FIELD bezeich       LIKE akt-code.bezeich
    FIELD zimmeranz     LIKE zinrstat.zimmeranz
    FIELD personen      LIKE zinrstat.personen
	FIELD argtumsatz	LIKE zinrstat.argtumsatz
    FIELD logisumsatz   LIKE zinrstat.logisumsatz
.
DEFINE TEMP-TABLE budget-umsatz
    FIELD datum AS DATE
    FIELD department AS INT
	FIELD s-dept   AS CHAR FORMAT "x(20)"
    FIELD umsatzart AS INT
	FIELD s-umsatzart AS CHAR FORMAT "x(20)"
    FIELD zwkum AS DECIMAL
    FIELD budget AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
.

DEFINE INPUT PARAMETER start-date    AS DATE.
DEFINE INPUT PARAMETER end-date    AS DATE.
DEFINE OUTPUT PARAMETER htl-name    AS CHARACTER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR his-res.
DEFINE OUTPUT PARAMETER TABLE FOR future-res.
DEFINE OUTPUT PARAMETER TABLE FOR rev-list.
DEFINE OUTPUT PARAMETER TABLE FOR budget-umsatz.
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.

DEFINE VARIABLE exclude-article AS CHARACTER INIT "" NO-UNDO.

DEFINE VARIABLE datum   AS DATE             NO-UNDO.
DEFINE VARIABLE datum2  AS DATE             NO-UNDO.
DEFINE VARIABLE ci-date AS DATE             NO-UNDO.
DEFINE VARIABLE sysdate AS DATE             NO-UNDO.
DEFINE VARIABLE i       AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE j       AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE iftask  AS CHARACTER        NO-UNDO.

DEFINE BUFFER gbuff FOR guest.
DEFINE BUFFER gbuff2 FOR guest.
DEFINE BUFFER natbuff FOR nation.
DEFINE BUFFER bufres-line FOR res-line.
DEFINE BUFFER buf-genstat FOR genstat.
DEFINE BUFFER buf-zimkateg FOR zimkateg.

DEFINE VARIABLE curr-i          AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE    NO-UNDO.   

DEFINE VARIABLE Fnet-lodg       AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-lodg        AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-breakfast   AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-lunch       AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-dinner      AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-other       AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-rmrev       AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-vat         AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-service     AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-fb          AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-food        AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-beverage    AS DECIMAL NO-UNDO.
DEFINE VARIABLE do-it1          AS LOGICAL INIT NO NO-UNDO.

DEFINE VARIABLE vat-proz                AS DECIMAL    NO-UNDO INIT 10.
DEFINE VARIABLE do-it                   AS LOGICAL    NO-UNDO.
DEFINE VARIABLE serv-taxable            AS LOGICAL    NO-UNDO.
DEFINE VARIABLE serv                    AS DECIMAL    NO-UNDO.
DEFINE VARIABLE vat                     AS DECIMAL    NO-UNDO.
DEFINE VARIABLE netto                   AS DECIMAL    NO-UNDO.
DEFINE VARIABLE serv-betrag             AS DECIMAL    NO-UNDO.
DEFINE VARIABLE outStr                  AS CHAR       NO-UNDO.
DEFINE VARIABLE outStr1                 AS CHAR       NO-UNDO.
DEFINE VARIABLE revCode                 AS CHAR       NO-UNDO.
DEFINE VARIABLE rechnr-notTax           AS INTEGER    NO-UNDO.
DEFINE VARIABLE bill-date               AS DATE       NO-UNDO.

DEFINE VARIABLE bill-resnr       AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-reslinnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-parentnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-gastnr      AS INTEGER NO-UNDO.
DEFINE VARIABLE ex-article       AS CHARACTER NO-UNDO.
DEFINE VARIABLE t-reslinnr       AS INTEGER NO-UNDO.

DEFINE VARIABLE hServer       AS HANDLE     NO-UNDO.
DEFINE VARIABLE lReturn       AS LOGICAL    NO-UNDO.
DEFINE VARIABLE HOappParam    AS CHAR       NO-UNDO.
DEFINE VARIABLE vHost         AS CHAR       NO-UNDO.
DEFINE VARIABLE vService      AS CHAR       NO-UNDO.
DEFINE VARIABLE htl-code      AS CHAR       NO-UNDO.
DEFINE VARIABLE storage-dur   AS INT        NO-UNDO.

DEFINE VARIABLE query-str AS CHARACTER  NO-UNDO.
FIND FIRST paramtext WHERE txtnr = 200 NO-LOCK NO-ERROR.
IF AVAILABLE paramtext THEN
        htl-name = TRIM(paramtext.ptexte).
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN 
ASSIGN 
	bill-date = htparam.fdate - 1
	ci-date = htparam.fdate.  

IF end-date GT bill-date THEN 
	end-date = bill-date.

/***************************************************/
FIND FIRST genstat WHERE ( genstat.datum GE start-date
    AND genstat.datum LE end-date )   
    AND genstat.resstatus NE 0    
    AND genstat.zikatnr NE 0 AND genstat.res-logic[2] USE-INDEX date_ix NO-LOCK NO-ERROR.

DO WHILE AVAILABLE genstat:
    FIND FIRST his-res WHERE his-res.zinr = genstat.zinr
                        AND his-res.staydate = genstat.datum
                        AND his-res.resnr = genstat.resnr
                        AND his-res.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
    IF NOT AVAILABLE his-res THEN
    DO:
        CREATE his-res.
        ASSIGN
            his-res.zinr = genstat.zinr 
            his-res.resnr = genstat.resnr
            his-res.reslinnr = genstat.res-int[1]          
            his-res.ci-date   = genstat.res-date[1]
            his-res.co-date   = genstat.res-date[2]
            his-res.adult = genstat.erwachs
            his-res.child = genstat.kind1
            his-res.compliment = genstat.gratis
            his-res.staydate  = genstat.datum
           /* his-res.source-code = genstat.source			
            his-res.rate-code = genstat.res-char[3]*/
            his-res.res-logi = genstat.res-logi[2]
            his-res.arrangement = genstat.argt
            his-res.rm-rate = genstat.zipreis
            his-res.nbrofroom = 1. /*default room number in case res-line table is
                                     already outside of storage duration*/
            
            his-res.rm-rev = genstat.logis. 
            his-res.fb-rev = genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4].
            /*his-res.beverage-rev = genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4].*/
            his-res.other-rev = genstat.res-deci[5] + genstat.res-deci[6] + genstat.res-deci[1]. /*termasuk additional F/O items*/
			
        FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.
		IF AVAILABLE segment THEN his-res.segmentcode   = segment.bezeich.
		FIND FIRST sourccod WHERE sourccod.source-code EQ genstat.source NO-LOCK NO-ERROR.
		IF AVAILABLE sourccod THEN his-res.source-code   = sourccod.bezeich.
		
		FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "arrangement"
            AND reslin-queasy.resnr = genstat.resnr
            AND reslin-queasy.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
        his-res.fixed-rate = AVAILABLE reslin-queasy.

        FIND FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            his-res.currency = waehrung.wabkurz.

        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
            AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.    

        FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR.
		IF AVAILABLE arrangement THEN
			ASSIGN
				his-res.argtnr = arrangement.argtnr. 

        FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN
        DO:
            ASSIGN
                his-res.room-type-name = zimkateg.kurzbez.
        END.  

        FIND FIRST buf-zimkateg WHERE buf-zimkateg.zikatnr = res-line.l-zuordnung[1] NO-LOCK NO-ERROR.
        IF AVAILABLE buf-zimkateg THEN
        DO:
            ASSIGN
                his-res.RTC = buf-zimkateg.kurzbez.
        END.
        
        IF AVAILABLE res-line THEN
        DO: 
            IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
            DO:
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF iftask MATCHES "*$CODE$*" THEN 
                        his-res.rate-code  = ENTRY(3, iftask, "$").
                END.
            END.

            FIND FIRST gbuff2 WHERE gbuff2.gastnr = res-line.gastnrpay NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff2 THEN
                his-res.bill-receiver = REPLACE(gbuff2.NAME + ", " + gbuff2.vorname1,CHR(10),"").

            ASSIGN
                his-res.reserveID = res-line.gastnr
                his-res.booktime = SUBSTR(res-line.reserve-char, 9, 5)
                his-res.nbrofroom = res-line.zimmeranz                
                his-res.compliment-ch = res-line.l-zuordnung[4]
                /* his-res.guestname = REPLACE(res-line.NAME,CHR(10),"") */
                .                  

            IF NUM-ENTRIES(res-line.memozinr, ";") GE 2 THEN
                his-res.memozinr = ENTRY(2, res-line.memozinr, ";").

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                IF ENTRY(i, res-line.zimmer-wunsch, ";") MATCHES "*ChAge*" THEN
                    his-res.age = SUBSTR(ENTRY(i, res-line.zimmer-wunsch, ";"),6). 
                IF ENTRY(i, res-line.zimmer-wunsch, ";") MATCHES "*SEGM_PUR*" THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 143
                        AND queasy.number1 = INT(SUBSTR(ENTRY(2,zimmer-wunsch,";"),9)) NO-LOCK NO-ERROR.
					IF NOT AVAILABLE queasy THEN
						FIND FIRST queasy WHERE queasy.KEY = 143
                        AND queasy.number1 = INT(SUBSTR(ENTRY(3,zimmer-wunsch,";"),9)) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                        his-res.purpose = queasy.char3.
                END.
            END.
        
            IF res-line.ankunft NE res-line.abreise THEN
				datum2 = res-line.abreise - 1.
			ELSE
				datum2 = res-line.abreise.
            DO datum = res-line.ankunft TO datum2: 
                IF datum GE start-date AND datum LE end-date THEN
                DO:        
                    RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                             OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                             OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                             OUTPUT tot-dinner, OUTPUT tot-other,
                                             OUTPUT tot-rmrev, OUTPUT tot-vat,
                                             OUTPUT tot-service).                                
                                                   
                    ASSIGN
                        his-res.tot-tax = tot-vat
                        his-res.tot-svc = tot-service.
                END.
            END.

            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
				IF guest.karteityp = 0 THEN his-res.card-type = "Individual".
				ELSE IF guest.karteityp = 1 THEN his-res.card-type = "Company".
				ELSE IF guest.karteityp = 1 THEN his-res.card-type = "Travel Agent".
				ASSIGN 
					his-res.company-code = ENTRY(1,guest.steuernr,"|")
					.

                IF guest.vorname1 NE "" THEN
                    his-res.reservename = guest.NAME + " " + guest.vorname1.
                ELSE
                    his-res.reservename = guest.NAME.
				FIND FIRST bediener WHERE bediener.userinit EQ guest.phonetik3 NO-LOCK NO-ERROR.
				IF AVAILABLE bediener THEN
					his-res.CODE   = bediener.username. /*Sales name*/
            END.  

            IF res-line.resstatus = 6 THEN
			DO:
                his-res.resstatus = 6.
				IF NOT genstat.res-logic[2] THEN /* Reservation use room not active*/
					his-res.nbrofroom = 0.
			END.
            ELSE IF res-line.resstatus = 13 THEN
                ASSIGN
                    his-res.resstatus = 13
                    his-res.nbrofroom = 0
                    his-res.adult = 0
                    his-res.child = 0.
            ELSE IF res-line.resstatus = 8 THEN
            DO:
				IF NOT genstat.res-logic[2] THEN /* Reservation use room not active*/
					his-res.nbrofroom = 0.
                ELSE IF genstat.resstatus = 13 THEN
                    ASSIGN
                        his-res.resstatus = 14
                        his-res.nbrofroom = 0
                        his-res.adult = 0
                        his-res.child = 0.
                ELSE IF genstat.resstatus = 6 THEN
                    his-res.resstatus = 8.
                ELSE IF genstat.resstatus = 8 THEN
                    his-res.resstatus = 8. /*DAY-USE*/
            END.            

            FIND FIRST nation WHERE nation.natcode EQ 0 AND nation.nationnr = genstat.nation NO-LOCK NO-ERROR.  
            IF AVAILABLE nation THEN
                ASSIGN
                    his-res.nationality = nation.bezeich.
					
			IF genstat.gastnrmember EQ res-line.gastnrmember THEN
			DO:
				FIND FIRST natbuff WHERE natbuff.untergruppe EQ 1 AND natbuff.natcode NE 0
				AND natbuff.nationnr = genstat.domestic NO-LOCK NO-ERROR.  
				IF AVAILABLE natbuff THEN
					ASSIGN
						his-res.localregion = natbuff.bezeich.
			END.
			ELSE his-res.localregion = "".
        END.

        FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
            ASSIGN
                his-res.voucher-nr = reservation.vesrdepot
                his-res.grpname = reservation.groupname
                his-res.letterno = reservation.briefnr
                his-res.cancel-reason = REPLACE(reservation.vesrdepot2,CHR(10),"").

            IF reservation.resdat NE ? THEN
                his-res.bookdate    = reservation.resdat.
			
        END.
    END.

        FIND NEXT genstat WHERE (genstat.datum GE start-date
        AND genstat.datum LE end-date)   
        AND genstat.resstatus NE 0    
        AND genstat.zikatnr NE 0 AND genstat.res-logic[2] USE-INDEX date_ix NO-LOCK NO-ERROR.
END.  

/*generating ALL Revenue*/
FOR EACH umsatz WHERE umsatz.datum GE start-date AND umsatz.datum LE end-date USE-INDEX umdate_index NO-LOCK:
    netto = 0.

    FIND FIRST artikel WHERE artikel.artnr = umsatz.artnr
        AND artikel.departement = umsatz.departement NO-LOCK NO-ERROR.
    IF AVAILABLE artikel AND 
        (artikel.artart = 0 OR artikel.artart = 8) THEN
    DO:
       RUN calc-servvat.p (artikel.departement, artikel.artnr, umsatz.datum,
           artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).

       IF vat = 1 THEN
           ASSIGN netto = umsatz.betrag * 100 / vat-proz.
       ELSE 
       DO:    
           IF serv = 1 THEN ASSIGN serv-betrag = netto.
           ELSE IF vat GT 0 THEN
           ASSIGN 
               netto = umsatz.betrag / (1 + serv + vat)
               serv-betrag = netto * serv
           .
           IF serv = 0 OR vat = 0 THEN
               netto = umsatz.betrag / (1 + serv + vat).
       END.

       FIND FIRST zwkum WHERE zwkum.departement = artikel.departement
           AND zwkum.zknr = artikel.zwkum NO-LOCK.
       FIND FIRST rev-list WHERE rev-list.dept = umsatz.departement
           AND rev-list.datum = umsatz.datum
           AND rev-list.subgrp = zwkum.zknr
		   AND rev-list.s-revart = artikel.bezeich NO-ERROR.
       IF NOT AVAILABLE rev-list THEN
       DO:
           CREATE rev-list.
           FIND FIRST hoteldpt WHERE hoteldpt.num = umsatz.departement
              NO-LOCK NO-ERROR.
           ASSIGN
               rev-list.dept = umsatz.departement
               rev-list.datum = umsatz.datum
               rev-list.subgrp = zwkum.zknr
               rev-list.s-subgrp = zwkum.bezeich
               rev-list.revart = artikel.umsatzart
			   rev-list.s-revart = artikel.bezeich
           .
           IF AVAILABLE hoteldpt THEN 
               rev-list.s-dept = hoteldpt.depart.
           CASE artikel.umsatz:
               WHEN 1 THEN rev-list.s-grp = "Lodging".
               WHEN 3 THEN rev-list.s-grp = "Food".
               WHEN 4 THEN rev-list.s-grp = "Other".
               WHEN 5 THEN rev-list.s-grp = "Food".
               WHEN 6 THEN rev-list.s-grp = "Beverage".
           END CASE.
       END.
       rev-list.amount = rev-list.amount + netto.    
    END.
END.

/*Generating Budget Umsatz*/
FOR EACH budget WHERE budget.datum GE start-date /* AND budget.datum LE end-date */ NO-LOCK BY budget.datum:

    FIND FIRST artikel WHERE artikel.departement EQ budget.departement AND
        artikel.artnr EQ budget.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE artikel AND artikel.umsatzart GT 0 THEN
    DO:
        FIND FIRST budget-umsatz WHERE budget-umsatz.datum EQ budget.datum AND
            budget-umsatz.department EQ budget.departement AND
            budget-umsatz.s-umsatzart EQ artikel.bezeich
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE budget-umsatz THEN
        DO:
            CREATE budget-umsatz.
			ASSIGN
            budget-umsatz.datum = budget.datum
            budget-umsatz.department = budget.departement
            budget-umsatz.umsatzart = artikel.umsatzart
            budget-umsatz.s-umsatzart = artikel.bezeich
            budget-umsatz.zwkum = artikel.zwkum	
			budget-umsatz.budget = budget.betrag			
			.
			FIND FIRST hoteldpt WHERE hoteldpt.num = budget.departement
              NO-LOCK NO-ERROR.
			IF AVAILABLE hoteldpt THEN 
               	budget-umsatz.s-dept = hoteldpt.depart.			  
        END.
    END.
END.
/*Generating Competitor*/
FOR EACH zinrstat WHERE zinrstat.zinr = "Competitor"
    AND zinrstat.datum GE start-date AND zinrstat.datum LE end-date
    NO-LOCK /*M , FIRST queasy WHERE queasy.number1 = zinrstat.betriebsnr
    AND queasy.KEY = 136 NO-LOCK . */,
    FIRST akt-code WHERE akt-code.aktionscode = zinrstat.betriebsnr
    AND akt-code.aktiongrup = 4 NO-LOCK:
    CREATE b1-list.
    ASSIGN
      b1-list.datum         = zinrstat.datum
      b1-list.zinr         	= zinrstat.zinr
      b1-list.betriebsnr    = zinrstat.betriebsnr
      b1-list.bezeich       = akt-code.bezeich
      b1-list.zimmeranz     = zinrstat.zimmeranz
      b1-list.personen      = zinrstat.personen
	  b1-list.argtumsatz   	= zinrstat.argtumsatz
      b1-list.logisumsatz   = zinrstat.logisumsatz.
END.

/*generating future reservation data*/
EMPTY TEMP-TABLE temp-res.
FOR EACH res-line WHERE ((res-line.ankunft GE ci-date OR res-line.abreise GT ci-date)
    AND res-line.active-flag LE 1 /*only guaranted and inhouse*/
	AND res-line.resstatus LE 13
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 10
	AND res-line.resstatus NE 4 ) OR
	(res-line.ankunft = ci-date AND res-line.abreise = ci-date) /*day use*/
    AND res-line.l-zuordnung[3] = 0 
	AND res-line.gastnr GT 0
	USE-INDEX gnrank_ix NO-LOCK BY res-line.resnr:

    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
    
	FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.	
	do-it = AVAILABLE segment AND segment.vip-level = 0.
	
	FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
    IF do-it AND AVAILABLE zimmer THEN 
        DO: /*Checking if ratecode is exist*/
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
            AND queasy.date1 LE ci-date AND queasy.date2 GE ci-date NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
               IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                do-it = NO. 
            END. 
            ELSE 
            DO: 
               IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
               ELSE do-it = NO. 
            END. 
        END. 
    IF do-it THEN 
    DO: 
		CREATE temp-res.
		ASSIGN
			temp-res.resnr       = res-line.resnr
			temp-res.reslinnr    = res-line.reslinnr
			temp-res.ci-date     = res-line.ankunft
			temp-res.co-date     = res-line.abreise        
			temp-res.booktime    = SUBSTR(res-line.reserve-char, 9, 5)
			temp-res.adult       = res-line.erwachs
			temp-res.child       = res-line.kind1
			temp-res.infant      = res-line.kind2
			temp-res.compliment  = res-line.gratis
			temp-res.compliment-ch = res-line.l-zuordnung[4]
			temp-res.resstatus   = res-line.resstatus
			temp-res.zinr        = res-line.zinr            
			temp-res.arrangement = res-line.arrangement
			temp-res.rm-rate     = res-line.zipreis       
			.

		IF NUM-ENTRIES(res-line.memozinr, ";") GE 2 THEN
			temp-res.memozinr    = ENTRY(2, res-line.memozinr, ";").
			
		IF res-line.cancelled NE ? THEN
			temp-res.cancel-date    = res-line.cancelled.
		ELSE temp-res.cancel-date = 01/01/01.
			
		FIND FIRST gbuff2 WHERE gbuff2.gastnr = res-line.gastnrpay NO-LOCK NO-ERROR.
		IF AVAILABLE gbuff2 THEN
			temp-res.bill-receiver = REPLACE(gbuff2.NAME + ", " + gbuff2.vorname1,CHR(10),"").

		FIND FIRST buf-zimkateg WHERE buf-zimkateg.zikatnr = res-line.l-zuordnung[1] NO-LOCK NO-ERROR.
		IF AVAILABLE buf-zimkateg THEN
		DO:
			ASSIGN
				temp-res.RTC = buf-zimkateg.kurzbez.
		END.

		DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
			IF ENTRY(i, res-line.zimmer-wunsch, ";") MATCHES "*ChAge*" THEN
				temp-res.age = SUBSTR(ENTRY(i, res-line.zimmer-wunsch, ";"),6). 
			IF ENTRY(i, res-line.zimmer-wunsch, ";") MATCHES "*SEGM_PUR*" THEN
			DO:
				FIND FIRST queasy WHERE queasy.KEY = 143
					AND queasy.number1 = INT(SUBSTR(ENTRY(2,zimmer-wunsch,";"),9)) NO-LOCK NO-ERROR.
				IF NOT AVAILABLE queasy THEN
						FIND FIRST queasy WHERE queasy.KEY = 143
                        AND queasy.number1 = INT(SUBSTR(ENTRY(3,zimmer-wunsch,";"),9)) NO-LOCK NO-ERROR.
				IF AVAILABLE queasy THEN
					temp-res.purpose = queasy.char3.
			END.
		END.

		FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "arrangement"
			AND reslin-queasy.resnr = res-line.resnr
			AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
		temp-res.fixed-rate = AVAILABLE reslin-queasy.

		FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
		IF AVAILABLE arrangement THEN
			ASSIGN
				temp-res.argtnr = arrangement.argtnr.

		FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
		IF AVAILABLE waehrung THEN
			temp-res.currency = waehrung.wabkurz.
			
		FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.		
		IF AVAILABLE zimkateg THEN
		DO:
			ASSIGN
				temp-res.room-type-name = zimkateg.kurzbez.
		END.

		IF res-line.resstatus EQ 11 OR res-line.resstatus EQ 13 OR res-line.zimmerfix OR res-line.ankunft EQ res-line.abreise THEN
			temp-res.nbrofroom   = 0.
		ELSE
			temp-res.nbrofroom   = res-line.zimmeranz.
			
		FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
		IF AVAILABLE guest THEN
		DO:
			ASSIGN        
			temp-res.company-code = ENTRY(1,guest.steuernr,"|")
			temp-res.reserveID   = guest.gastnr
			.
			IF guest.karteityp = 0 THEN temp-res.card-type = "Individual".
			ELSE IF guest.karteityp = 1 THEN temp-res.card-type = "Company".
			ELSE IF guest.karteityp = 1 THEN temp-res.card-type = "Travel Agent".
			IF guest.vorname1 NE "" THEN
				temp-res.reservename = guest.NAME + " " + guest.vorname1.
			ELSE
				temp-res.reservename = guest.NAME.
				
			FIND FIRST bediener WHERE bediener.userinit EQ guest.phonetik3 NO-LOCK NO-ERROR.
			IF AVAILABLE bediener THEN
					temp-res.CODE   = bediener.username. /*Sales name*/
		END.
		
		FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
		IF AVAILABLE gbuff THEN DO:
			FIND FIRST nation WHERE nation.kurzbez = gbuff.nation1 NO-LOCK NO-ERROR.
			IF AVAILABLE nation THEN temp-res.nationality = nation.bezeich.
			
			FIND FIRST nation WHERE nation.kurzbez = gbuff.nation2 NO-LOCK NO-ERROR.
			IF AVAILABLE nation THEN temp-res.localregion = nation.bezeich.
/* 			ASSIGN
				temp-res.localregion = gbuff.nation2
				temp-res.nationality = gbuff.nation1. */
		END.
		IF AVAILABLE reservation THEN
		DO: 
			ASSIGN
				temp-res.bookdate    = reservation.resdat
				temp-res.voucher-nr  = reservation.vesrdepot
				temp-res.grpname     = reservation.groupname
				temp-res.cancel-reason = REPLACE(reservation.vesrdepot2,CHR(10),"").
				
			FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
			IF AVAILABLE segment THEN temp-res.segmentcode   = segment.bezeich.
			
			FIND FIRST sourccod WHERE sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
			IF AVAILABLE sourccod THEN temp-res.source-code = sourccod.bezeich.
		END.        

		IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
		DO:
			DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
				iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
				IF iftask MATCHES "*$CODE$*" THEN 
					temp-res.rate-code  = ENTRY(3, iftask, "$").
			END.
		END.

		IF res-line.ankunft NE res-line.abreise THEN
			datum2 = res-line.abreise - 1.
		ELSE
			datum2 = res-line.abreise.

		DO datum = res-line.ankunft TO datum2:
			IF datum GE ci-date THEN
			DO:        
				RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
											 OUTPUT Fnet-lodg, OUTPUT net-lodg,
											 OUTPUT tot-breakfast, OUTPUT tot-lunch,
											 OUTPUT tot-dinner, OUTPUT tot-other,
											 OUTPUT tot-rmrev, OUTPUT tot-vat,
											 OUTPUT tot-service). /*NC - future room-rev selisih saat pakai get-room-breakdown-bi*/
		
				tot-food = tot-breakfast + tot-lunch + tot-dinner.
		
				CREATE future-res.
				BUFFER-COPY temp-res TO future-res.
				ASSIGN
					future-res.staydate = datum
					future-res.rm-rev = net-lodg
					future-res.food-rev = tot-food
					future-res.beverage-rev = 0 /*tot-beverage - beverage not exist on get-room-breakdown vhp*/
					future-res.other-rev = tot-other
					future-res.tot-tax = tot-vat
					future-res.tot-svc = tot-service
					future-res.fb-rev = tot-food + tot-beverage /*tot-beverage - beverage not exist on get-room-breakdown vhp*/
					.
			END.
		END.   
			
		DELETE temp-res.
		RELEASE temp-res.
	END.
END.
success-flag = YES.
