

DEFINE INPUT PARAMETER pvILanguage   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER inp-resnr     AS INTEGER. 
DEFINE INPUT PARAMETER inp-reslinnr  AS INTEGER.
DEFINE INPUT PARAMETER co-date       AS DATE.
DEFINE INPUT PARAMETER user-init     AS CHAR.
DEFINE OUTPUT PARAMETER msg-int      AS INTEGER.
 
DEFINE VARIABLE ankunft         AS DATE. 
DEFINE VARIABLE departure       AS DATE. 
DEFINE VARIABLE resnr           AS INTEGER INITIAL 49. 
DEFINE VARIABLE reslinnr        AS INTEGER INITIAL 1. 
DEFINE VARIABLE zinr            LIKE zimmer.zinr.   /*MT 20/07/12 change zinr format */
DEFINE VARIABLE min-reslinnr    AS INTEGER INITIAL 0. 
DEFINE VARIABLE ci-date         AS DATE NO-UNDO.
DEFINE VARIABLE priscilla-active AS LOGICAL NO-UNDO INITIAL YES.

DEFINE BUFFER buf-rline FOR res-line.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
RUN htpdate.p(87, OUTPUT ci-date).

FIND FIRST res-line WHERE res-line.resnr = inp-resnr AND res-line.reslinnr = inp-reslinnr EXCLUSIVE-LOCK. 
FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
ankunft = res-line.ankunft. 
departure = res-line.ankunft + res-line.anztage. 
res-line.abreise = departure. 
resnr = res-line.resnr. 
reslinnr = res-line.reslinnr. 
zinr = res-line.zinr. 

RUN guest-recheckin.
FIND CURRENT res-line NO-LOCK.

/*FD Oct 13, 2022 => Ticket B1B3A0 - Create Reservation Log*/
FIND FIRST buf-rline WHERE buf-rline.resnr EQ resnr
    AND buf-rline.reslinnr EQ reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE buf-rline THEN
DO:
    CREATE reslin-queasy.
    ASSIGN
        reslin-queasy.key       = "ResChanges"
        reslin-queasy.resnr     = buf-rline.resnr 
        reslin-queasy.reslinnr  = buf-rline.reslinnr 
        reslin-queasy.date2     = TODAY 
        reslin-queasy.number2   = TIME
    .

    reslin-queasy.char3 = STRING(buf-rline.ankunft) + ";" 
                        + STRING(buf-rline.ankunft) + ";" 
                        + STRING(buf-rline.abreise) + ";" 
                        + STRING(buf-rline.abreise) + ";" 
                        + STRING(buf-rline.zimmeranz) + ";" 
                        + STRING(buf-rline.zimmeranz) + ";" 
                        + STRING(buf-rline.erwachs) + ";" 
                        + STRING(buf-rline.erwachs) + ";" 
                        + STRING(buf-rline.kind1) + ";" 
                        + STRING(buf-rline.kind1) + ";" 
                        + STRING(buf-rline.gratis) + ";" 
                        + STRING(buf-rline.gratis) + ";" 
                        + STRING(buf-rline.zikatnr) + ";" 
                        + STRING(buf-rline.zikatnr) + ";" 
                        + STRING(buf-rline.zinr) + ";" 
                        + STRING(buf-rline.zinr) + ";" 
                        + STRING(buf-rline.arrangement) + ";" 
                        + STRING(buf-rline.arrangement) + ";"
                        + STRING(buf-rline.zipreis) + ";" 
                        + STRING(buf-rline.zipreis) + ";"
                        + STRING(user-init) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(buf-rline.name) + ";" 
                        + STRING("RE-CI CO GUEST") + ";"
                        + STRING(" ") + ";" 
                        + STRING(" ") + ";"
                        .      

    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 
END.

PROCEDURE guest-recheckin: 
  DEFINE BUFFER bill1     FOR bill. 
  DEFINE BUFFER bill2     FOR bill. 
  DEFINE BUFFER res-line1 FOR res-line. 
  DEFINE BUFFER res-line2 FOR res-line. 
  DEFINE BUFFER resline   FOR res-line. 
  DEFINE BUFFER zbuff 	  FOR zimkateg.  /*NC- 20/02/24*/
  DEFINE BUFFER qsy   			FOR queasy.
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE tot-umsatz AS DECIMAL INITIAL 0. 
  /*NC- 20/02/24*/
  DEFINE VARIABLE i           AS INT INIT 0.
  DEFINE VARIABLE upto-date AS DATE.
  DEFINE VARIABLE iftask      AS CHAR INIT "".
  DEFINE VARIABLE origcode    AS CHAR INIT "".
  DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
  DEFINE VARIABLE roomnr      AS INT INIT 0.
  DEFINE VARIABLE tmp-date    AS DATE. /* Malik Serverless 714 */
 
  /******************** UPDATE room status *****************/ 
  FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK. 
  FIND FIRST res-line1 WHERE 
    (res-line1.resnr NE inp-resnr AND res-line1.reslinnr NE inp-reslinnr)
    AND res-line1.zinr = zinr 
    AND (res-line1.resstatus EQ 6 OR res-line1.resstatus EQ 13) 
    NO-LOCK NO-ERROR. 
 
  IF NOT AVAILABLE res-line1 THEN 
  DO: 
    FIND CURRENT zimmer EXCLUSIVE-LOCK. 
    zimmer.zistatus = 4.   /* 4 = occupied dirty,  5 = occupied clean */ 
    zimmer.bediener-nr-stat = 0. 
    IF res-line.abreise = ci-date THEN zimmer.zistatus = 3.
    FIND CURRENT zimmer NO-LOCK. 
  END. 
 
  /******************** UPDATE reservation status *****************/ 
  IF AVAILABLE res-line1 THEN res-line.resstatus = 13. 
  ELSE res-line.resstatus = 6. 
 
  FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
  IF reservation.activeflag = 1 THEN 
  DO: 
    FIND CURRENT reservation EXCLUSIVE-LOCK. 
    reservation.activeflag = 0. 
    FIND CURRENT reservation NO-LOCK. 
  END. 
 
  /****************** Check Master Bill ***/ 
  IF NOT AVAILABLE res-line1 THEN 
  DO: 
    FIND FIRST master WHERE master.resnr = resnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE master THEN 
    DO: 
      master.active = YES. 
      FIND CURRENT master NO-LOCK.
      msg-int = 1.
      /*FDL August 23, 2023 => Ticket BA1CE1 - Add no-error if available*/
      FIND FIRST bill1 WHERE bill1.resnr = resnr AND bill1.reslinnr = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE bill1 THEN
      DO:
        IF bill1.flag = 1 THEN 
        DO: 
          FIND CURRENT bill1 EXCLUSIVE-LOCK. 
          bill1.flag = 0. 
          FIND CURRENT bill1 NO-LOCK. 
        END. 
        IF bill1.rechnr NE 0 THEN 
        DO: 
          FIND FIRST guest WHERE guest.gastnr = bill1.gastnr EXCLUSIVE-LOCK. 
          ASSIGN 
            guest.logisumsatz = guest.logisumsatz - bill1.logisumsatz 
            guest.argtumsatz = guest.argtumsatz - bill1.argtumsatz 
            guest.f-b-umsatz = guest.f-b-umsatz - bill1.f-b-umsatz 
            guest.sonst-umsatz = guest.sonst-umsatz - bill1.sonst-umsatz 
            guest.gesamtumsatz = guest.gesamtumsatz - bill1.gesamtumsatz. 
          FIND CURRENT guest NO-LOCK. 
          RELEASE guest. 
        END.
      END.       
    END. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 307 NO-LOCK. 
  IF flogical THEN 
    RUN intevent-1.p( 1, res-line.zinr, "RE-Checkin!", res-line.resnr, res-line.reslinnr). 

  IF priscilla-active THEN
  DO:
    RUN intevent-1.p( 9, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
  END.

  /******************** UPDATE zimplan IF main guest **************/ 
  tmp-date = res-line.abreise - 1.
  IF res-line.resstatus = 6 THEN 
  DO datum = co-date TO tmp-date: /* Malik Serverless 714 (res-line.abreise - 1) -> tmp-date */
    FIND FIRST zimplan WHERE zimplan.zinr = zinr 
      AND zimplan.datum = datum NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE zimplan THEN 
    DO: 
      create zimplan. 
      ASSIGN 
        zimplan.datum = datum 
        zimplan.zinr = zinr.
        /*zimplan.res-recid = res-recid. */
    END. 
  END. 
 
  /******************** UPDATE resplan *******************/ 
  FOR EACH resplan WHERE resplan.datum GE co-date 
    AND resplan.datum LT res-line.abreise 
    AND resplan.zikatnr = zimmer.zikatnr EXCLUSIVE-LOCK: 
    resplan.anzzim[res-line.resstatus] = resplan.anzzim[res-line.resstatus] + 1. 
    RELEASE resplan.
  END. 
 
  /****************** create history */ 
  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
  /*ITA
  CREATE history. 
  ASSIGN 
    history.gastnr = res-line.gastnrmember 
    history.ankunft = res-line.ankunft 
    history.abreise = co-date 
    history.zimmeranz = res-line.zimmeranz 
    history.zikateg = zimkateg.kurzbez 
    history.zinr = res-line.zinr 
    history.erwachs = res-line.erwachs 
    history.gratis = res-line.gratis 
    history.zipreis = res-line.zipreis 
    history.arrangement = res-line.arrangement 
    history.gastinfo = res-line.name + " - " 
      + guest.adresse1 + ", " + guest.wohnort 
    history.abreisezeit = STRING(TIME, "HH:MM") 
    history.segmentcode = reservation.segmentcode 
    history.zi-wechsel = NO 
    history.resnr = res-line.resnr 
    history.reslinnr = res-line.reslinnr. 
  history.bemerk = "Cancel C/O and Re-checkin by"
    + " " + user-init. 
  FIND CURRENT history NO-LOCK. */
 
  CREATE res-history. 
  ASSIGN 
    res-history.nr = bediener.nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME 
    res-history.resnr = res-line.resnr 
    res-history.reslinnr = res-line.reslinnr 
    res-history.action = "RE-CI"
  .
  res-history.aenderung = "Cancel C/O and Re-checkin by"
    + " " + user-init 
    + " " + "ResNo" + " " + STRING(res-line.resnr)
    + " " + "RmNo"  + " " + res-line.zinr
  . 
 
  /****************** Update Availability when Cancel-CO***********/
  /*NC- 20/02/24*/ 	
 
  FIND FIRST res-line2 WHERE res-line2.resnr = resnr AND 
	  res-line2.reslinnr = reslinnr NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line2 THEN 
  DO:
	  /*FT update queasy availability booking engine*/
	  DO i = 1 TO NUM-ENTRIES(res-line2.zimmer-wunsch,";") - 1:
		iftask = ENTRY(i, res-line2.zimmer-wunsch, ";").
		IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
		DO:
		  origcode  = SUBSTR(iftask,11).
		  LEAVE.
		END.
	  END. 

	  FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
	  IF AVAILABLE queasy THEN cat-flag = YES.

	  FIND FIRST zbuff WHERE zbuff.zikatnr = res-line2.zikatnr NO-LOCK NO-ERROR.
	  IF AVAILABLE zbuff THEN
	  DO:
		IF cat-flag THEN roomnr = zbuff.typ.
		ELSE roomnr = zbuff.zikatnr.
	  END.

	  IF res-line2.ankunft = co-date THEN upto-date = co-date .
	  ELSE upto-date = res-line2.abreise  - 1. 
	  DO datum = co-date TO upto-date:
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
				AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
			IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
			DO:
				FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
				IF AVAILABLE qsy THEN
				DO:
					qsy.logi2 = YES.
					FIND CURRENT qsy NO-LOCK.
					RELEASE qsy.
				END.
			END. 
			
			IF origcode NE "" THEN
			DO:
				FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
					AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
				IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
				DO:
					FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
					IF AVAILABLE qsy THEN
					DO:
						qsy.logi2 = YES.
						FIND CURRENT qsy NO-LOCK.
						RELEASE qsy.
					END.
				END.
			END.
	  END.
      /*ITA 260525 log availability*/
        CREATE res-history. 
        ASSIGN 
            res-history.nr          = bediener.nr 
            res-history.resnr       = res-line2.resnr 
            res-history.reslinnr    = res-line2.reslinnr 
            res-history.datum       = TODAY
            res-history.zeit        = TIME 
            res-history.aenderung = "Cancel CO : ResNo " + STRING(res-line2.resnr ) + " No " 
                + STRING(res-line2.reslinnr ) + " - " + res-line.NAME
            res-history.action      = "Log Availability".  
        IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
        RELEASE res-history. 
  END.  
 
  /********************* Calculate guest turnover **********/ 
  FOR EACH bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = reslinnr 
    AND bill1.flag = 1 AND bill1.zinr = zinr NO-LOCK: 
    tot-umsatz = tot-umsatz + bill1.gesamtumsatz. 
  END. 
 
  /*********************** UPDATE Bills etc ********/   
  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay EXCLUSIVE-LOCK. 
  FOR EACH bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = reslinnr 
    AND bill1.flag = 1 AND bill1.zinr = zinr NO-LOCK:
    IF tot-umsatz NE 0 THEN 
    DO: 
      ASSIGN 
        guest.logisumsatz = guest.logisumsatz - bill1.logisumsatz 
        guest.argtumsatz = guest.argtumsatz - bill1.argtumsatz 
        guest.f-b-umsatz = guest.f-b-umsatz - bill1.f-b-umsatz 
        guest.sonst-umsatz = guest.sonst-umsatz - bill1.sonst-umsatz 
        guest.gesamtumsatz = guest.gesamtumsatz - bill1.gesamtumsatz. 
    END. 
  END.
  FIND CURRENT guest NO-LOCK. 

  FIND FIRST bill2 WHERE bill2.resnr = res-line.resnr
    AND bill2.reslinnr = res-line.reslinnr EXCLUSIVE-LOCK. 
  ASSIGN 
    bill2.flag = 0 
    bill2.datum = co-date. 
  FIND CURRENT bill2 NO-LOCK. 
 
  ASSIGN 
    res-line.abreise = departure 
    res-line.abreisezeit = 0 
    res-line.changed = TODAY 
    res-line.changed-id = user-init 
    res-line.active-flag = 1. 
 
  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember EXCLUSIVE-LOCK. 
  IF guest.zimmeranz GT 0 THEN guest.zimmeranz = guest.zimmeranz - 1. 
  IF guest.aufenthalte GT 0 THEN guest.aufenthalte = guest.aufenthalte - 1. 
  guest.resflag = 2. 
  FIND CURRENT guest NO-LOCK.
 
  IF res-line.gastnrmember NE res-line.gastnrpay THEN
  DO:
    RUN get-min-reslinnr. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay EXCLUSIVE-LOCK. 
    IF guest.zimmeranz GT 0 THEN guest.zimmeranz = guest.zimmeranz - 1. 
    IF min-reslinnr = 1 AND guest.aufenthalte GT 0 THEN 
    ASSIGN 
      guest.aufenthalte = guest.aufenthalte - 1.
    FIND CURRENT guest NO-LOCK. 
  END.

  FOR EACH resline WHERE resline.resnr = res-line.resnr
    AND resline.kontakt-nr = res-line.reslinnr
    AND resline.l-zuordnung[3] = 1:
    ASSIGN
        resline.active-flag = 1
        resline.resstatus   = 13
        resline.abreise     = res-line.abreise
        resline.abreisezeit = 0
        resline.changed-id  = user-init
    .
  END.

END. 

PROCEDURE get-min-reslinnr: 
DEFINE buffer resline FOR res-line. 
  FOR EACH resline WHERE resline.resnr = resnr AND 
    resline.active-flag = 1 AND resline.resstatus NE 12 NO-LOCK:  
    min-reslinnr = min-reslinnr + 1.
  END. 
END.
