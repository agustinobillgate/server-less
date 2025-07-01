DEFINE TEMP-TABLE zimmer-list LIKE zimmer.
DEFINE TEMP-TABLE t-zimmer    LIKE zimmer.
DEFINE TEMP-TABLE dynaRate-list
  FIELD prCode  AS CHAR 
  FIELD to-room AS INTEGER 
.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER case-type      AS INT.
DEF INPUT  PARAMETER TABLE          FOR zimmer-list.
DEF INPUT  PARAMETER rm-feature     AS CHAR.
DEF INPUT  PARAMETER curr-mode      AS CHAR.
DEF INPUT  PARAMETER rmNo           AS CHAR.
DEF INPUT  PARAMETER rmcatBez       AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER TABLE          FOR t-zimmer.
DEF OUTPUT PARAMETER TABLE          FOR dynaRate-list.
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "add-room-admin".
DEF VAR sleeping AS LOGICAL NO-UNDO. /*NC - 02/12/22*/
FIND FIRST zimmer-list.
IF case-type = 1 THEN
DO:
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer-list.zikatnr 
     EXCLUSIVE-LOCK. 
    zimkateg.maxzimanz = zimkateg.maxzimanz + 1. 
    FIND CURRENT zimkateg NO-LOCK. 
    create zimmer.
    RUN fill-zimmer.
	RUN update-queasy. /*NC - 02/12/22*/
END.
ELSE
DO:
    FIND FIRST zimmer WHERE zimmer.zinr = rmNo EXCLUSIVE-LOCK NO-ERROR.
	sleeping = zimmer.sleeping. /*NC - 02/12/22*/
    RUN fill-zimmer.
END.
FOR EACH dynaRate-list:
    DELETE dynaRate-list.
END.
PROCEDURE fill-zimmer: 
  IF (case-type NE 1) AND (zimmer-list.sleeping NE zimmer.sleeping) THEN DO:
      FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. 
      CREATE res-history.
      ASSIGN 
          res-history.nr        = bediener.nr 
          res-history.datum     = TODAY 
          res-history.zeit      = TIME 
          res-history.aenderung = "RoomNo: " + zimmer.zinr + " change room active " 
                                  + STRING(zimmer.sleeping) + " to " + STRING(zimmer-list.sleeping).
          res-history.action = "Room Admin". 
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history. 
  END.
  BUFFER-COPY zimmer-list TO zimmer.
  zimmer.himmelsr = rm-feature.
  IF curr-mode = "chg" AND zimmer.setup NE zimmer-list.setup 
    AND zimmer.setup NE 0 THEN 
  DO: 
    FIND FIRST res-line WHERE res-line.active-flag = 1 
      AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE res-line: 
      FIND CURRENT res-line EXCLUSIVE-LOCK. 
      res-line.setup = zimmer-list.setup. 
      FIND CURRENT res-line NO-LOCK. 
      FIND NEXT res-line WHERE res-line.active-flag = 1 
        AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
    END. 
    FIND FIRST res-line WHERE res-line.active-flag = 0 
      AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE res-line: 
      FIND CURRENT res-line EXCLUSIVE-LOCK. 
      res-line.setup = zimmer-list.setup. 
      FIND CURRENT res-line NO-LOCK. 
      FIND NEXT res-line WHERE res-line.active-flag = 0 
        AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
    END. 
  END. 
  zimmer.setup = zimmer-list.setup.
/*NC- 02/12/22 tiket A76996*/
  IF curr-mode = "chg" AND sleeping NE zimmer-list.sleeping THEN
	DO:
		RUN update-queasy.
	END.  
END. 
FOR EACH zimmer NO-LOCK BY zimmer.zinr:
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
END.
PROCEDURE check-dynaRate:
DEF VAR tokcounter          AS INTEGER      NO-UNDO.
DEF VAR ifTask              AS CHAR         NO-UNDO.
DEF VAR ct                  AS CHAR INIT "" NO-UNDO.
DEF VAR mesToken            AS CHAR         NO-UNDO.
DEF VAR mesValue            AS CHAR         NO-UNDO.
DEF VAR days1               AS INTEGER      NO-UNDO.
DEF VAR days2               AS INTEGER      NO-UNDO.
DEF VAR to-room             AS INTEGER      NO-UNDO.
  FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.logi2 NO-LOCK NO-ERROR.
  IF NOT AVAILABLE queasy THEN RETURN.
  
  FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmcatBez NO-LOCK.
  FOR EACH queasy WHERE queasy.KEY = 2 AND queasy.logi2 NO-LOCK:
    CREATE dynaRate-list.
    ASSIGN
        dynaRate-list.prCode  = queasy.char1
        dynaRate-list.to-room = 0
        to-room               = 0
        days1                 = 0
        days2                 = 0
    .
    FOR EACH ratecode WHERE ratecode.CODE = queasy.char1 NO-LOCK:
      ifTask = ratecode.char1[5].
      DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
        mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
        mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
        CASE mesToken:
          WHEN "TR" THEN to-room = INTEGER(mesValue).
          WHEN "D1" THEN days1   = INTEGER(mesValue).
          WHEN "D2" THEN days2   = INTEGER(mesValue).
        END CASE.
      END.
      IF days1 = 0 AND days2 = 0 AND dynaRate-list.to-room LT to-room THEN
        ASSIGN dynaRate-list.to-room = to-room.
    END.
    IF dynaRate-list.to-room = 0 THEN DELETE dynaRate-list.
  END.
  FOR EACH dynaRate-list WHERE dynaRate-list.to-room LT zimkateg.maxzimanz:
      ct = ct + dynaRate-list.prCode + " " + STRING(dynaRate-list.to-room) + "; ".
  END.
  IF ct NE "" THEN
      msg-str = msg-str + CHR(2)
              + translateExtended ("The MAX To-Room of following Ratecode(s) < Room QTY of the related Room Type",lvCAREA,"")
              + " (= " + STRING(zimkateg.maxzimanz) + ")."
              + CHR(10)
              + ct.
END.
PROCEDURE update-queasy:
DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
DEFINE VARIABLE zikatnr      AS INT INIT 0.

DEFINE BUFFER qsy   FOR queasy.

	FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
	IF AVAILABLE queasy THEN cat-flag = YES.

	FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer-list.zikatnr NO-LOCK NO-ERROR.
	IF AVAILABLE zimkateg THEN DO:
		IF cat-flag THEN zikatnr = zimkateg.typ.
		ELSE zikatnr = zimkateg.zikatnr.
	END.


	FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 GE TODAY
            AND queasy.number1 = zikatnr NO-LOCK NO-ERROR.
	DO WHILE AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO :
		FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
		IF AVAILABLE qsy THEN
		DO:
			qsy.logi2 = YES.
			FIND CURRENT qsy NO-LOCK.
			RELEASE qsy.
		END.
		FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 GE TODAY
            AND queasy.number1 = zikatnr NO-LOCK NO-ERROR.
	END.
END.