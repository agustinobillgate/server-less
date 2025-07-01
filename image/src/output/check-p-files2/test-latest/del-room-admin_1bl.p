DEF INPUT PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER zinr            AS CHAR    NO-UNDO.
DEF INPUT PARAMETER zikatnr         AS INTEGER NO-UNDO.
DEF INPUT PARAMETER user-init       AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER room-limit     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER curr-anz       AS INTEGER NO-UNDO.
{SupertransBL.i} 

DEF VAR lvCAREA AS CHAR INITIAL "del-room-admin".
FIND FIRST res-line WHERE res-line.zinr = zinr NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
DO: 
 msg-str = msg-str + CHR(2)
         + translateExtended ("Reservation exists, deleting not possible.",lvCAREA,"").
END. 
ELSE 
DO: 
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = zikatnr EXCLUSIVE-LOCK. 
  zimkateg.maxzimanz = zimkateg.maxzimanz - 1. 
  FIND CURRENT zimkateg NO-LOCK. 
  FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK NO-ERROR.
  IF AVAILABLE zimmer THEN DO:      
      FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. 
      CREATE res-history.
      ASSIGN 
          res-history.nr        = bediener.nr 
          res-history.datum     = TODAY 
          res-history.zeit      = TIME 
          res-history.aenderung = "Delete Room Number " + zimmer.zinr.
          res-history.action    = "Room Admin". 
      FIND CURRENT res-history NO-LOCK. 
      RELEASE res-history.

      FIND CURRENT zimmer EXCLUSIVE-LOCK. 
      DELETE zimmer. 
      RELEASE zimmer.     
  END.
  RUN check-rm-limit.
  RUN update-queasy. /*NC- 02/12/22 tiket A76996*/
/* 
OPEN QUERY q1 FOR EACH zimmer WHERE zimmer.zikatnr = zikatnr 
   NO-LOCK BY zimmer.zinr. 
*/ 
END.
PROCEDURE check-rm-limit: 
DEF BUFFER rbuff FOR zimmer.
  FIND FIRST htparam WHERE htparam.paramnr = 975 NO-LOCK. 
  IF htparam.finteger GT 0 THEN room-limit = htparam.finteger. 
  curr-anz = 0. 
  FOR EACH rbuff NO-LOCK: 
     curr-anz = curr-anz + 1. 
   END. 
END. 
PROCEDURE update-queasy:
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


	FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 GE TODAY
            AND queasy.number1 = z-nr NO-LOCK NO-ERROR.
	DO WHILE AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO :
		FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
		IF AVAILABLE qsy THEN
		DO:
			qsy.logi2 = YES.
			FIND CURRENT qsy NO-LOCK.
			RELEASE qsy.
		END.
		FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 GE TODAY
            AND queasy.number1 = z-nr NO-LOCK NO-ERROR.
	END.
END.