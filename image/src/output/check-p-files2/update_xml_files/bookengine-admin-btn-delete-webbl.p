
DEF INPUT  PARAMETER number1 AS INT.
DEF INPUT  PARAMETER user-init    AS CHAR.

FIND FIRST queasy WHERE queasy.KEY = 159
    AND queasy.number1 = number1 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
	FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
	IF AVAILABLE bediener THEN DO:
	CREATE res-history. 
	ASSIGN 
		res-history.nr     = bediener.nr 
		res-history.datum  = TODAY 
		res-history.zeit   = TIME 
		res-history.action = "Booking Engine Interface"
		res-history.aenderung = "Deleted Booking Engine : BE Code=" +  STRING(queasy.number1) + "; Name=" + queasy.char1 + "; Gastnr=" + STRING(queasy.number2) + " by " + STRING(bediener.nr) + " - " + bediener.username
	.
	END.
	
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    DELETE queasy.
    RELEASE queasy.
END.
