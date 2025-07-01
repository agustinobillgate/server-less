
DEF TEMP-TABLE book-engine-list LIKE queasy.

DEF INPUT  PARAMETER TABLE FOR book-engine-list.
DEF INPUT  PARAMETER icase AS INT.
DEF INPUT  PARAMETER user-init    AS CHAR.

FIND FIRST book-engine-list.
IF icase = 1 THEN
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY     = 159
        queasy.number1 = book-engine-list.number1
        queasy.char1   = book-engine-list.char1
        queasy.number2 = book-engine-list.number2.
		
	FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
	IF AVAILABLE bediener THEN DO:
	CREATE res-history. 
	ASSIGN 
		res-history.nr     = bediener.nr 
		res-history.datum  = TODAY 
		res-history.zeit   = TIME 
		res-history.action = "Booking Engine Interface"
		res-history.aenderung = "Created New Booking Engine : BE Code=" +  STRING(book-engine-list.number1) + "; Name=" + book-engine-list.char1 + "; Gastnr=" + STRING(book-engine-list.number2) + " by " + STRING(bediener.nr) + " - " + bediener.username
	.
	END.
END.
ELSE
DO:
    FIND FIRST queasy WHERE queasy.KEY = 159 AND 
        queasy.number1 = book-engine-list.number1 NO-ERROR.
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
			res-history.aenderung = "Modified Booking Engine : from BE Code=" +  STRING(queasy.number1) + " to BE Code=" + STRING(book-engine-list.number1) + "; From Name=" + queasy.char1 + " to Name=" + book-engine-list.char1 + " from Gastnr=" + STRING(queasy.number2) + " To Gastnr=" + STRING(book-engine-list.number2) + " by " + STRING(bediener.nr) + " - " + bediener.username
		.
		END.
	
        BUFFER-COPY book-engine-list TO queasy.
    END.
END.
