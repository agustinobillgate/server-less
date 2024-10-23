
DEF TEMP-TABLE z-list
    FIELD zinr              LIKE zimmer.zinr
    FIELD setup             LIKE zimmer.setup
    FIELD zikatnr           LIKE zimmer.zikatnr
    FIELD etage             LIKE zimmer.etage
    FIELD zistatus          LIKE zimmer.zistatus
    FIELD CODE              LIKE zimmer.CODE
    FIELD bediener-nr-stat  LIKE zimmer.bediener-nr-stat
    FIELD checkout          AS LOGICAL INITIAL NO
    FIELD str-reason        AS CHAR.

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD ind AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE bline-list 
  FIELD zinr AS CHAR 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD bl-recid AS INTEGER. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR bline-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR om-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resflag         AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER dept            AS INT     NO-UNDO.
DEF INPUT PARAMETER zinr            AS CHAR    NO-UNDO.
DEF INPUT PARAMETER user-nr         AS INT     NO-UNDO.
DEF INPUT PARAMETER from-date       AS DATE    NO-UNDO.
DEF INPUT PARAMETER to-date         AS DATE    NO-UNDO.
DEF INPUT PARAMETER ci-date         AS DATE    NO-UNDO.
DEF INPUT PARAMETER reason          AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR z-list.

DEF VARIABLE return-flag AS LOGICAL INIT NO NO-UNDO.
DEF VARIABLE from-stat AS CHAR FORMAT "x(100)".
DEF VARIABLE to-stat   AS CHAR FORMAT "x(100)".
DEF VARIABLE curr-date AS DATE.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-statadmin".
DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(23)" NO-UNDO. /*william C2CAD7*/
stat-list[1] = translateExtended ("Vacant Clean Checked", lvCAREA,""). 
stat-list[2] = translateExtended ("Vacant Clean Unchecked", lvCAREA,""). 
stat-list[3] = translateExtended ("Vacant Dirty", lvCAREA,""). 
stat-list[4] = translateExtended ("Expected Departure", lvCAREA,""). 
stat-list[5] = translateExtended ("Occupied Dirty", lvCAREA,""). 
stat-list[6] = translateExtended ("Occupied Cleaned", lvCAREA,""). 
stat-list[7] = translateExtended ("Out-of-Order", lvCAREA,""). 
stat-list[8] = translateExtended ("Off-Market", lvCAREA,""). 
stat-list[9] = translateExtended ("Do not Disturb", lvCAREA,""). 
stat-list[10] = translateExtended ("Out-of-Service",lvCAREA,""). 

DEFINE BUFFER resline FOR res-line. 

FIND FIRST res-line WHERE res-line.resnr = dept 
    AND res-line.zinr = zinr NO-LOCK NO-ERROR. 

FOR EACH bline-list WHERE bline-list.selected = YES: 
  FIND FIRST zimmer WHERE zimmer.zinr = bline-list.zinr NO-LOCK. 

  /*FDL Sept 11, 2024: 7469D8*/
  DO curr-date = from-date TO to-date:
      FIND FIRST outorder WHERE outorder.zinr EQ zimmer.zinr
          AND (outorder.gespstart GE curr-date AND outorder.gespstart LE curr-date 
              OR outorder.gespstart LE curr-date AND outorder.gespende GE curr-date)
          AND outorder.betriebsnr EQ 2 NO-LOCK NO-ERROR.
      IF AVAILABLE outorder THEN
      DO:
          msg-str = msg-str 
              + translateExtended ("Overlapping Off-Market found:",lvCAREA,"")
              + CHR(10) 
              + translateExtended ("Room No",lvCAREA,"") + " " + outorder.zinr + " - "
              + STRING(outorder.gespstart) + " To " + STRING(outorder.gespende)
              .
          RETURN.
      END.
  END.
  
/* with reservation */
  IF NOT resflag THEN FIND FIRST resline WHERE resline.active-flag LE 1 
      AND resline.resnr NE res-line.resnr AND 
      resline.resstatus NE 12 AND 
      NOT resline.abreise LE from-date AND
      NOT resline.ankunft GT to-date   AND
          resline.zinr EQ zinr NO-LOCK NO-ERROR.
  ELSE 
/* without reservation */
  FIND FIRST resline WHERE resline.active-flag LE 1 
      AND resline.resstatus NE 12 AND 
      NOT resline.abreise LE from-date AND
      NOT resline.ankunft GT to-date   AND
          resline.zinr EQ zinr NO-LOCK NO-ERROR.
   
  IF AVAILABLE resline THEN 
  DO:
    msg-str = msg-str + 
            translateExtended ("Reservation exists under ResNo",lvCAREA,"") +
            " = " + STRING(resline.resnr) + CHR(10) +
            translateExtended ("Guest Name",lvCAREA,"") + " = " + resline.name +
            CHR(10) +
            translateExtended ("Arrival :",lvCAREA,"") + " " + 
            STRING(resline.ankunft) + "   " + 
            translateExtended ("Departure :",lvCAREA,"") + " " + 
            STRING(resline.abreise).
    /*MTAPPLY "entry" TO from-date.*/
    return-flag = YES.
    RETURN.
  END. 
END.

FOR EACH bline-list WHERE bline-list.selected = YES: 
  FIND FIRST zimmer WHERE zimmer.zinr = bline-list.zinr NO-LOCK. 
  DO TRANSACTION: 
      FIND FIRST om-list WHERE om-list.zinr EQ bline-list.zinr. /*william C2CAD7*/
      from-stat = STRING(zimmer.zistatus) + " " + stat-list[om-list.ind]. /*william add om-list.ind C2CAD7*/
      CREATE outorder. 
      outorder.zinr = bline-list.zinr. 
      outorder.gespstart = from-date. 
      outorder.gespende  = to-date. 
      IF resflag THEN outorder.betriebsnr = 2. 
      ELSE outorder.betriebsnr = dept. 
      outorder.gespgrund = reason + "$" + STRING(user-nr). 
      FIND CURRENT outorder NO-LOCK. 
      IF outorder.gespstart EQ ci-date THEN 
      DO: 
        FIND FIRST om-list WHERE om-list.zinr = outorder.zinr. 
        om-list.ind = 8.
        to-stat = STRING(zimmer.zistatus) + " " + stat-list[om-list.ind]. /*william add om-list.ind C2CAD7*/ 
        
        FIND FIRST bediener WHERE bediener.nr = user-nr NO-LOCK. 
        CREATE res-history. 
        ASSIGN 
          res-history.nr = bediener.nr 
          res-history.datum = TODAY 
          res-history.zeit = TIME 
          res-history.aenderung = "Room " + zimmer.zinr 
             + " Status Changed From " 
             + FROM-stat + " to " + to-stat
          res-history.action = "HouseKeeping". 
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history.
      END. 
	  /*NC- 02/12/22 tiket A76996*/
	  RUN update-queasy(zimmer.zikatnr).
      FIND CURRENT zimmer EXCLUSIVE-LOCK. 
      zimmer.bediener-nr-stat = user-nr. 
      FIND CURRENT zimmer NO-LOCK. 
      bline-list.selected = NO. 
  END. 
END.

IF return-flag THEN RETURN.

FOR EACH z-list:
  DELETE z-list.
END.

FOR EACH zimmer NO-LOCK:
  CREATE z-list.
  BUFFER-COPY zimmer TO z-list.
  IF zimmer.zistatus = 2 THEN 
  DO:
      FIND FIRST res-line WHERE res-line.resstatus = 8 
          AND res-line.zinr = zimmer.zinr
          AND res-line.abreise = ci-date NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN z-list.checkout = YES.
  END.

  /*ITA 030717*/
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
        AND outorder.betriebsnr LE 2 
        AND outorder.gespstart LE ci-date 
        AND outorder.gespende GE ci-date NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN 
        ASSIGN z-list.str-reason = ENTRY(1, outorder.gespgrund, "$").
    ELSE ASSIGN z-list.str-reason = " ".
END.
PROCEDURE update-queasy:
DEF INPUT  PARAMETER zikatnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
DEFINE VARIABLE z-nr      AS INT INIT 0.


DEFINE BUFFER qsy   FOR queasy.

	FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
	IF AVAILABLE queasy THEN cat-flag = YES.

	FIND FIRST zimkateg WHERE zimkateg.zikatnr = zikatnr NO-LOCK NO-ERROR.
	IF AVAILABLE zimkateg THEN DO:
		IF cat-flag THEN z-nr = zimkateg.typ.
		ELSE z-nr = zimkateg.zikatnr.
	END.


	FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 GE ci-date
            AND queasy.number1 = z-nr NO-LOCK NO-ERROR.
	DO WHILE AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO :
		FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
		IF AVAILABLE qsy THEN
		DO:
			qsy.logi2 = YES.
			FIND CURRENT qsy NO-LOCK.
			RELEASE qsy.
		END.
		FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 GE ci-date
            AND queasy.number1 = z-nr NO-LOCK NO-ERROR.
	END.
END.
