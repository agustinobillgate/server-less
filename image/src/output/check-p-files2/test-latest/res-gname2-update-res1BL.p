
DEFINE TEMP-TABLE s-list 
  FIELD res-recid   AS INTEGER 
  FIELD resstatus   AS INTEGER 
  FIELD active-flag AS INTEGER
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD karteityp   AS INTEGER 
  FIELD zimmeranz   AS INTEGER
  FIELD erwachs     AS INTEGER FORMAT ">9" LABEL "Adult" 
  FIELD kind1       AS INTEGER LABEL "Ch1" FORMAT ">9"    FIELD kind2       AS INTEGER LABEL "Ch2" FORMAT ">9" 
  FIELD old-zinr    AS CHAR 
  FIELD name        AS CHAR FORMAT "x(36)" LABEL "Name, Firstname, Title" 
  FIELD nat         AS CHAR FORMAT "x(3)" LABEL "Nation" 
  FIELD land        AS CHAR FORMAT "x(3)" LABEL "Cntry" 
  FIELD zinr        LIKE zimmer.zinr LABEL "RmNo " 
  FIELD eta         AS CHAR FORMAT "99:99" LABEL "ETA" INITIAL "0000"
  FIELD etd         AS CHAR FORMAT "99:99" LABEL "ETD" INITIAL "0000"
  FIELD flight1     AS CHAR
  FIELD flight2     AS CHAR
  FIELD rmcat       AS CHAR FORMAT "x(6)" LABEL "RmCat" 
  FIELD ankunft     AS DATE LABEL "Arrival" 
  FIELD abreise     AS DATE LABEL "Departure" 
  FIELD zipreis     AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" LABEL "Room Rate"
  FIELD bemerk      AS CHAR
. 

DEF INPUT PARAMETER inp-resnr   AS INTEGER  NO-UNDO. 
DEF INPUT PARAMETER name        AS CHAR     NO-UNDO.
DEF INPUT PARAMETER fname       AS CHAR     NO-UNDO.
DEF INPUT PARAMETER ftitle      AS CHAR     NO-UNDO.
DEF INPUT PARAMETER name-screen AS CHAR     NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR     NO-UNDO.
DEF INPUT PARAMETER if-flag     AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER ci-date     AS DATE     NO-UNDO.
DEF INPUT PARAMETER answer      AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER TABLE       FOR s-list.

DEFINE VARIABLE res-mode        AS CHAR     NO-UNDO.
DEFINE VARIABLE curr-reslinnr   AS INTEGER  NO-UNDO.
DEFINE VARIABLE priscilla-active AS LOGICAL NO-UNDO INIT YES.

DEFINE TEMP-TABLE t-resline     LIKE res-line.
DEFINE BUFFER resline           FOR res-line. 
DEFINE BUFFER resline1          FOR res-line. 

/*MTDEF VAR inp-resnr AS INT INIT 16702.
DEF VAR name AS CHAR INIT "AGIS ELECTRONIC".
DEF VAR fname AS CHAR INIT "".
DEF VAR ftitle AS CHAR INIT "".
DEF VAR name-screen AS CHAR INIT "AGIS ELECTRONIC".
DEF VAR user-init AS CHAR INIT "01".
DEF VAR if-flag AS LOGICAL INIT YES.
DEF VAR ci-date AS DATE INIT 01/30/10.
DEF VAR answer AS LOGICAL INIT YES.
  FOR EACH res-line WHERE res-line.resnr = inp-resnr 
    AND active-flag LT 2 AND resstatus NE 12 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikat NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
    CREATE s-list.
    ASSIGN
      s-list.res-recid   = RECID(res-line)
      s-list.name        = res-line.NAME
      s-list.nat         = guest.nation1 
      s-list.land        = guest.land
      s-list.zinr        = "2716"
      s-list.old-zinr    = res-line.zinr
      s-list.flight1     = SUBSTR(res-line.flight-nr,1,6)
      s-list.eta         = SUBSTR(res-line.flight-nr,7,4)
      s-list.flight2     = SUBSTR(res-line.flight-nr,12,6)
      s-list.etd         = SUBSTR(res-line.flight-nr,18,4)
      s-list.zimmeranz   = res-line.zimmeranz 
      s-list.resstatus   = res-line.resstatus 
      s-list.active-flag = res-line.active-flag
      s-list.karteityp   = guest.karteityp
      s-list.erwachs     = res-line.erwachs 
      s-list.rmcat       = zimkateg.kurzbez
      s-list.ankunft     = res-line.ankunft 
      s-list.abreise     = res-line.abreise 
      s-list.kind1       = res-line.kind1
      s-list.kind2       = res-line.kind2 
      s-list.zipreis     = res-line.zipreis
      s-list.bemerk      = res-line.bemerk
    . 
  END.*/

CREATE t-resline.
FIND FIRST reservation WHERE reservation.resnr = inp-resnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE reservation THEN RETURN. /*FT serverless*/
RUN update-res1.

PROCEDURE update-res1:
DEFINE BUFFER accBuff  FOR res-line.
DEFINE VARIABLE still-error         AS LOGICAL. 
DEFINE VARIABLE gcf-found           AS LOGICAL INITIAL NO. 
DEFINE VARIABLE master-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prev-zinr           AS CHAR.
DEFINE VARIABLE gastmember          AS INTEGER NO-UNDO.
DEFINE VARIABLE flight-info         AS CHAR    NO-UNDO.
  
  FOR EACH s-list: 
    FIND FIRST res-line WHERE RECID(res-line) = s-list.res-recid NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      BUFFER-COPY res-line TO t-resline.
      
      IF priscilla-active THEN
      DO:
        RUN intevent-1.p(9, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
      END.
      
      FIND CURRENT res-line EXCLUSIVE-LOCK.
      IF NUM-ENTRIES(s-list.bemerk, CHR(2)) = 2 
        OR s-list.flag NE res-line.gastnrmember THEN /*FDL for vhpCloud*/
      DO:
        IF s-list.flag NE res-line.gastnrmember THEN gastmember = s-list.flag. /*FDL for vhpCloud*/
        ELSE gastmember = INTEGER(ENTRY(2, s-list.bemerk, CHR(2))).

        IF gastmember GT 0 THEN
          FIND FIRST guest WHERE guest.gastnr = gastmember NO-LOCK NO-ERROR.
        ELSE IF gastmember = 0 THEN
        DO:
          RUN create-gcf(OUTPUT gastmember).
          FIND FIRST guest WHERE guest.gastnr = gastmember NO-LOCK NO-ERROR.
        END.

        /*FDL Debug CatchLog*/
        IF res-line.gastnrmember NE gastmember THEN
        DO:
          MESSAGE 
              "CatchLog Update Guest Name from Manage RSV " inp-resnr SKIP
              "Gastnrmember from " res-line.gastnrmember " => " gastmember SKIP
              "Guest Name from " res-line.NAME " => " guest.NAME 
              ", " guest.vorname1 " " guest.anrede1 SKIP
              "END CatchLog"
              VIEW-AS ALERT-BOX INFO BUTTONS OK.
        END.

        ASSIGN
          res-line.gastnrmember = gastmember
          res-line.NAME         = guest.NAME + ", " + guest.vorname1 
                              + " " + guest.anrede1
          res-line.changed      = ci-date
          res-line.changed-id   = user-init. 
      END.
      ELSE FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
      FIND CURRENT res-line NO-LOCK.

/* SY
      FIND FIRST guest WHERE guest.name = name AND guest.vorname1 = fname 
        AND guest.gastnr GT 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE guest THEN gcf-found = YES. 
*/
      IF AVAILABLE guest THEN
      DO:
        FIND CURRENT guest EXCLUSIVE-LOCK.
        IF ((s-list.nat NE guest.nation1) AND s-list.nat NE "") OR 
          ((s-list.land NE guest.land) AND s-list.land NE "") THEN 
        DO:
          IF s-list.nat  NE "" THEN guest.nation1 = s-list.nat.
          IF s-list.land NE "" THEN guest.land    = s-list.land.
          guest.char2   = user-init.
        END.
        FIND CURRENT guest NO-LOCK. 
      END.
      
    
      FIND FIRST resline WHERE RECID(resline) = s-list.res-recid EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE resline THEN
      DO:
        IF answer THEN 
        DO: 
          IF resline.gastnrpay NE guest.gastnr AND resline.active-flag = 1 THEN 
          DO: 
            FIND FIRST bill WHERE bill.resnr = resline.resnr 
              AND bill.reslinnr = resline.reslinnr EXCLUSIVE-LOCK NO-ERROR. 
            IF AVAILABLE bill THEN 
            DO: 
              bill.gastnr = guest.gastnr. 
              bill.name = guest.name. 
              FIND CURRENT bill NO-LOCK.
              RELEASE bill. 
            END. 
          END. 
          resline.gastnrpay = guest.gastnr. 
          resline.changed = ci-date. 
          resline.changed-id = user-init. 
        END. 
        flight-info = STRING(s-list.flight1,"x(6)")
                   + STRING(s-list.eta, "x(5)")
                   + STRING(s-list.flight2, "x(6)")
                   + STRING(s-list.etd, "x(5)").
     
        IF resline.flight-nr NE flight-info THEN
          ASSIGN
            resline.flight-nr  = flight-info
            resline.changed    = ci-date
            resline.changed-id = user-init
          . 
    
        IF resline.zinr NE s-list.zinr THEN 
        DO: 
          IF resline.active-flag = 0 THEN res-mode = "Modify". 
          ELSE res-mode = "Inhouse". 
          curr-reslinnr = resline.reslinnr. 
          IF s-list.zinr NE "" THEN RUN assign-zinr(RECID(resline), resline.ankunft, 
            resline.abreise, s-list.zinr, resline.resstatus, resline.gastnrmember, 
            resline.bemerk, resline.name, OUTPUT still-error). 
          IF NOT still-error THEN 
          DO: 
            IF resline.zinr NE "" THEN 
            DO: 
              RUN release-zinr(s-list.zinr). 
              IF res-line.resstatus = 6 AND if-flag THEN 
                RUN intevent-1.p(2, resline.zinr, "Move out", resline.resnr, resline.reslinnr). 
            END. 
            prev-zinr = resline.zinr. 
            resline.zinr = s-list.zinr. 
            IF s-list.zinr NE "" THEN 
            DO: 
              FIND FIRST zimmer WHERE zimmer.zinr = s-list.zinr NO-LOCK NO-ERROR. 
              IF AVAILABLE zimmer THEN
              ASSIGN 
                resline.setup = zimmer.setup 
                resline.zikatnr = zimmer.zikatnr. 
            END. 
            FOR EACH accBuff WHERE accBuff.resnr = resline.resnr
              AND accBuff.kontakt-nr = resline.reslinnr
              AND accBuff.l-zuordnung[3] = 1:
              ASSIGN accBuff.zinr = resline.zinr.
            END.
            IF resline.active-flag = 1 THEN 
            DO: 
              IF resline.resstatus = 6 AND if-flag THEN 
                RUN intevent-1.p(1, resline.zinr, "Change Name", resline.resnr, resline.reslinnr). 
                RUN create-history.p(resline.resnr, resline.reslinnr, 
              prev-zinr, "roomchg"). 
              FOR EACH bill WHERE bill.resnr = resline.resnr 
                AND bill.parent-nr = resline.reslinnr AND bill.flag = 0: 
                bill.zinr = s-list.zinr. 
                FIND FIRST resline1 WHERE resline.resnr = bill.resnr 
                  AND resline1.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
                IF AVAILABLE resline1 THEN
                DO:
                  IF resline1.resstatus = 12 /* i.e. res-line FOR additional bill */ THEN 
                  DO: 
                    FIND CURRENT resline1 EXCLUSIVE-LOCK. 
                    resline1.zinr = s-list.zinr. 
                    FIND CURRENT resline1 NO-LOCK. 
                  END.                             
                END.
                RELEASE bill. 
              END. 
            END.
          END. 
        END. 
        resline.changed = ci-date. 
        resline.changed-id = user-init. 
        FIND CURRENT resline NO-LOCK. 
	    IF t-resline.zinr NE resline.zinr THEN RUN update-qsy171. /*NC #DA5A48 06/11/23*/
        IF t-resline.NAME NE resline.NAME OR t-resline.zinr NE resline.zinr THEN RUN res-changes.
      END.
    END.
  END. 
END. 

PROCEDURE update-qsy171:
DEFINE VARIABLE curr-date       AS DATE    NO-UNDO.
DEFINE VARIABLE upto-date       AS DATE    NO-UNDO.
DEFINE VARIABLE curr-i          AS INTEGER NO-UNDO.
DEFINE VARIABLE stat-code       AS CHAR    NO-UNDO INIT "".
DEFINE VARIABLE iftask      	AS CHAR INIT "" NO-UNDO.
DEFINE VARIABLE origcode    	AS CHAR INIT "" NO-UNDO.
DEFINE VARIABLE cat-flag    	AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE roomnr      	AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE zikatnr      	AS INT INIT 0 NO-UNDO.

DEFINE BUFFER qsy   FOR queasy.
DEFINE BUFFER zbuff FOR zimkateg.

	DO curr-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
		iftask = ENTRY(curr-i, res-line.zimmer-wunsch, ";").
		IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
		DO:
		  origcode  = SUBSTR(iftask,11).
		  LEAVE.
		END.
	END. 
	FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
		IF AVAILABLE queasy THEN cat-flag = YES.
		
	FIND FIRST zbuff WHERE zbuff.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
	IF AVAILABLE zbuff THEN
	DO:
		IF cat-flag THEN roomnr = zbuff.typ.
		ELSE roomnr = zbuff.zikatnr.
	END.
	FIND FIRST zbuff WHERE zbuff.zikatnr = t-resline.zikatnr NO-LOCK NO-ERROR.
	IF AVAILABLE zbuff THEN
	DO:
		IF cat-flag THEN zikatnr = zbuff.typ.
		ELSE zikatnr = zbuff.zikatnr.
	END.
	upto-date = res-line.abreise - 1.
	IF upto-date LT res-line.ankunft THEN upto-date = res-line.ankunft.
	DO curr-date = res-line.ankunft TO upto-date:
		FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date
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
		FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date
			AND queasy.number1 = zikatnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
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
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date
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
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date
				AND queasy.number1 = zikatnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
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
END.

PROCEDURE res-changes: 
DEFINE VARIABLE cid   AS CHAR FORMAT "x(2)" INITIAL "  ". 
DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        ". 
  CREATE reslin-queasy. 
  ASSIGN
    reslin-queasy.key = "ResChanges"
    reslin-queasy.resnr = resline.resnr 
    reslin-queasy.reslinnr = resline.reslinnr 
    reslin-queasy.date2 = TODAY 
    reslin-queasy.number2 = TIME
  . 
  reslin-queasy.char3 = STRING(t-resline.ankunft) + ";" 
                        + STRING(resline.ankunft) + ";" 
                        + STRING(t-resline.abreise) + ";" 
                        + STRING(resline.abreise) + ";" 
                        + STRING(t-resline.zimmeranz) + ";" 
                        + STRING(resline.zimmeranz) + ";" 
                        + STRING(t-resline.erwachs) + ";" 
                        + STRING(resline.erwachs) + ";" 
                        + STRING(t-resline.kind1) + ";" 
                        + STRING(resline.kind1) + ";" 
                        + STRING(t-resline.gratis) + ";" 
                        + STRING(resline.gratis) + ";" 
                        + STRING(t-resline.zikatnr) + ";" 
                        + STRING(resline.zikatnr) + ";" 
                        + STRING(t-resline.zinr) + ";" 
                        + STRING(resline.zinr) + ";" 
                        + STRING(t-resline.arrangement) + ";" 
                        + STRING(resline.arrangement) + ";"
                        + STRING(t-resline.zipreis) + ";" 
                        + STRING(resline.zipreis) + ";"
                        + STRING(user-init) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(t-resline.NAME) + ";" 
                        + STRING(resline.NAME) + ";".  
  FIND CURRENT reslin-queasy NO-LOCK.
  RELEASE reslin-queasy. 
 
END. 

PROCEDURE create-gcf:
DEFINE OUTPUT PARAMETER curr-gastnr AS INTEGER NO-UNDO INIT 0. 
DEFINE VARIABLE i        AS INTEGER NO-UNDO.
DEFINE VARIABLE inp-name AS CHAR    NO-UNDO.
DEFINE VARIABLE lname    AS CHAR    NO-UNDO INIT "".
DEFINE VARIABLE fname    AS CHAR    NO-UNDO INIT "".
DEFINE VARIABLE ftitle   AS CHAR    NO-UNDO INIT "".
  ASSIGN inp-name = s-list.NAME.
  DO i = 1 TO NUM-ENTRIES(inp-name, ","):
      CASE i:
          WHEN 1 THEN lname  = TRIM(ENTRY(1, inp-name, ",")).
          WHEN 2 THEN fname  = TRIM(ENTRY(2, inp-name, ",")).
          WHEN 3 THEN ftitle = TRIM(ENTRY(3, inp-name, ",")).
      END CASE.
  END.

  FIND LAST guest NO-LOCK NO-ERROR. 
  IF AVAILABLE guest THEN curr-gastnr = guest.gastnr + 1. 
  ELSE curr-gastnr = 1. 
  CREATE guest. 
  ASSIGN
    guest.gastnr    = curr-gastnr
    guest.karteityp = 0
    guest.nation1   = s-list.nat 
    guest.land      = s-list.land
    guest.name      = lname
    guest.vorname1  = fname 
    guest.anrede1   = ftitle 
    guest.char1     = user-init
  . 
  FIND CURRENT guest NO-LOCK. 
 
  CREATE guestseg. 
  ASSIGN
      guestseg.gastnr      = guest.gastnr
      guestseg.reihenfolge = 1 
      guestseg.segmentcode = reservation.segmentcode
  . 
  FIND CURRENT guestseg NO-LOCK.
  RELEASE guestseg. 
END. 

PROCEDURE assign-zinr:
  DEFINE INPUT  PARAMETER resline-recid AS INTEGER.
  DEFINE INPUT  PARAMETER ankunft AS DATE.
  DEFINE INPUT  PARAMETER abreise AS DATE.
  DEFINE INPUT  PARAMETER zinr LIKE zimmer.zinr.
  DEFINE INPUT  PARAMETER resstatus AS INTEGER.
  DEFINE INPUT  PARAMETER gastnrmember AS INTEGER.
  DEFINE INPUT  PARAMETER bemerk AS CHAR.
  DEFINE INPUT  PARAMETER name AS CHAR.
  DEFINE output PARAMETER room-blocked AS LOGICAL INITIAL NO.
  
  DEFINE VARIABLE sharer AS LOGICAL.
  DEFINE VARIABLE curr-datum AS DATE.
  DEFINE VARIABLE beg-datum AS DATE.
  DEFINE VARIABLE res-recid AS INTEGER.
  DEFINE BUFFER res-line1 FOR res-line.
  DEFINE BUFFER zimplan1 FOR zimplan.
  DEFINE BUFFER resline FOR res-line.
    
  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.

  sharer = (resstatus = 11) OR (resstatus = 13).
  if zinr NE "" AND NOT sharer THEN
  DO:
    if res-mode = "inhouse" THEN beg-datum = htparam.fdate.
    ELSE beg-datum = ankunft.
    room-blocked = no.
    do curr-datum = beg-datum TO (abreise - 1): 
      FIND FIRST zimplan1 WHERE zimplan1.datum = curr-datum
          AND zimplan1.zinr = zinr NO-LOCK NO-ERROR.
      if (NOT AVAILABLE zimplan1) AND (NOT room-blocked) THEN 
      DO:
        CREATE zimplan.
        zimplan.datum = curr-datum.
        zimplan.zinr = zinr.
        zimplan.res-recid = resline-recid.
        zimplan.gastnrmember = gastnrmember.
        zimplan.bemerk = bemerk.
        zimplan.resstatus = resstatus.
        zimplan.name = name.
        FIND CURRENT zimplan NO-LOCK.
        RELEASE zimplan.
      END.
      ELSE 
      DO: 
/* it is possible that it is the zimplan of it's own res-line exists, 
   THEN room-blocked is false */       
        IF AVAILABLE zimplan1 AND (zimplan1.res-recid NE resline-recid) THEN
        DO:
          FIND FIRST resline WHERE RECID(resline) = zimplan1.res-recid 
            NO-LOCK NO-ERROR.
          if AVAILABLE resline AND resline.zinr = zinr 
            AND resline.active-flag LT 2 
            AND resline.ankunft LE zimplan1.datum
            AND resline.abreise GT zimplan1.datum THEN
          DO:
            curr-datum = abreise.
            room-blocked = yes.
          END.
          ELSE
          DO: /* try to fix the room plan by deleting wrong zimplan records */
            /*ITA 28 maret 16 -- > share-lock to exclusive-lock*/
            FIND CURRENT zimplan1 EXCLUSIVE-LOCK.
            ASSIGN 
                zimplan1.res-recid      = resline-recid
                zimplan1.gastnrmember   = gastnrmember
                zimplan1.bemerk         = bemerk
                zimplan1.resstatus      = resstatus
                zimplan1.name           = name.
            FIND CURRENT zimplan1 NO-LOCK.
            RELEASE zimplan1.
          END.
        END.
      END.
    END.
    if room-blocked THEN
    DO:
      do curr-datum = beg-datum TO (abreise - 1): 
        FIND FIRST zimplan WHERE zimplan.datum = curr-datum
          AND zimplan.zinr = zinr 
          AND zimplan.res-recid = resline-recid EXCLUSIVE-LOCK NO-ERROR.
        if AVAILABLE zimplan THEN 
        DO:
          DELETE zimplan.
          RELEASE zimplan.
        END.
      END.
      /*MTHIDE MESSAGE NO-PAUSE.
      MESSAGE "RoomNo " + zinr 
        + " already blocked; room assignment not possible."
        VIEW-AS ALERT-BOX INFORMATION.*/
    END.
    ELSE DO:
      IF resstatus = 6 OR resstatus = 13 THEN
      DO:
        FIND FIRST zimmer WHERE zimmer.zinr = zinr EXCLUSIVE-LOCK.
        if abreise GT htparam.fdate AND zimmer.zistatus = 0 
          THEN zimmer.zistatus = 5. /* occupied clean */
        ELSE IF abreise GT htparam.fdate AND zimmer.zistatus = 3 /* ED */
          THEN zimmer.zistatus = 4. /* occupied dirty */
        ELSE if abreise = htparam.fdate THEN
        DO:
          FIND FIRST res-line1 WHERE RECID(res-line1) NE resline-recid 
            AND res-line1.abreise = abreise 
            AND res-line1.zinr = zimmer.zinr AND
            (res-line1.resstatus = 6 OR res-line1.resstatus = 13) 
            NO-LOCK NO-ERROR.
          if not AVAILABLE res-line1 THEN zimmer.zistatus = 3. /* ED */
        END.
/*      zimmer.bediener-nr-stat = 0.   */
        FIND CURRENT zimmer NO-LOCK.
        RELEASE zimmer.
      END.
    END.
  END.
END.


PROCEDURE release-zinr:
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr.
DEFINE VARIABLE res-recid1 AS INTEGER.
DEFINE BUFFER res-line1 FOR res-line.
DEFINE BUFFER res-line2 FOR res-line.
DEFINE BUFFER rline FOR res-line.
DEFINE VARIABLE beg-datum AS DATE.
DEFINE VARIABLE answer AS LOGICAL.
DEFINE VARIABLE parent-nr AS INTEGER.

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.

  FIND FIRST rline WHERE rline.resnr = inp-resnr 
      AND rline.reslinnr = curr-reslinnr NO-LOCK.
  if rline.zinr NE "" THEN
  DO: 
    beg-datum = rline.ankunft. 
    res-recid1 = 0.

    if res-mode = "delete" OR res-mode = "cancel" 
      AND rline.resstatus = 1 THEN 
    DO TRANSACTION:
      FIND FIRST res-line1 WHERE res-line1.resnr = inp-resnr
        AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 11
        NO-LOCK NO-ERROR.
      if AVAILABLE res-line1 THEN 
      DO:
        FIND CURRENT res-line1 EXCLUSIVE-LOCK.
        res-line1.resstatus = 1.
        FIND CURRENT res-line1 NO-LOCK.
        res-recid1 = RECID(res-line1).
      END.
    END.    
    if res-mode = "inhouse" THEN 
    DO:
      answer = yes.
      beg-datum = htparam.fdate.

      if rline.resstatus = 6 AND (rline.zinr NE new-zinr) THEN
      DO TRANSACTION:
        FIND FIRST res-line1 WHERE res-line1.resnr = inp-resnr
          AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 13 
          NO-LOCK NO-ERROR.
        if AVAILABLE res-line1 THEN 
/*        
        DO:
          HIDE MESSAGE NO-PAUSE.
          MESSAGE "Room-change FOR the RoomSharer too?"         
            VIEW-AS ALERT-BOX question buttons yes-no update answer.
        END.
        if answer = no THEN 
        DO:
          FIND CURRENT res-line1 EXCLUSIVE-LOCK.
          res-line1.resstatus = 6.
          FIND CURRENT res-line1 NO-LOCK.
          res-recid1 = RECID(res-line1).
        END.
        ELSE 
*/
        DO:       
          FOR EACH res-line2 WHERE res-line2.resnr = inp-resnr
              AND res-line2.zinr = rline.zinr AND res-line2.resstatus = 13 
              EXCLUSIVE-LOCK:
            FIND FIRST bill WHERE bill.resnr = inp-resnr
              AND bill.reslinnr = res-line2.reslinnr AND bill.flag = 0 
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK.
            bill.zinr = new-zinr.
            parent-nr = bill.parent-nr.
            FIND CURRENT bill NO-LOCK.
            FOR EACH bill WHERE bill.resnr = inp-resnr 
              AND bill.parent-nr = parent-nr AND bill.flag = 0
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK:
              bill.zinr = new-zinr.
              release bill.
            END.
            res-line2.zinr = new-zinr.
            release res-line2.
          END.
          FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr EXCLUSIVE-LOCK.
          zimmer.zistatus = 2.
          FIND CURRENT zimmer NO-LOCK.
        END.
      END.
    END.
    DO:
      FOR EACH zimplan WHERE zimplan.zinr = rline.zinr 
          AND zimplan.datum GE beg-datum
          AND zimplan.datum LT rline.abreise EXCLUSIVE-LOCK:
        if res-recid1 NE 0 THEN zimplan.res-recid = res-recid1.
        ELSE delete zimplan.
      END.
    END.
  END.
END. 
