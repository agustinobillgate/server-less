/*THIS program to handle request from VHPCloud Based on discusion with Pak Michael*/
/*Created by Narco 31/05/24 */
DEF TEMP-TABLE t-push-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0.

DEF TEMP-TABLE outlist
    FIELD KEY       AS INT
    FIELD number1   AS INT
    FIELD char1     AS CHAR.

DEF INPUT PARAMETER TABLE FOR t-push-list.
DEF INPUT PARAMETER bookengID AS INT.
/*naufal - add for logfile*/
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER case-type AS INT. /*NC - add for vhpcloud*/

DEF VAR str AS CHAR.
DEF VAR old-str AS CHAR.
DEF BUFFER bufQ FOR queasy.
DEF BUFFER qsy FOR queasy.


CASE case-type:
	WHEN 1 THEN /*new*/
	DO:
		FOR EACH t-push-list NO-LOCK:
			ASSIGN
			str = ""
			str = t-push-list.rcodeVHP   + ";"
				+ t-push-list.rcodeBE    + ";"
				+ t-push-list.rmtypeVHP  + ";"
				+ t-push-list.rmtypeBE   + ";"
				+ t-push-list.argtVHP.

			/*DISP
				str FORMAT "x(50)".
				outlist.char1   "x(50)"*/

			CREATE bufQ.
			ASSIGN
				bufQ.KEY = 163
				bufQ.number1 = bookengID
				bufQ.char1 = str.
			RELEASE bufQ.

			/*naufal - add for logfile*/
			FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
			IF AVAILABLE bediener THEN
			DO:
				CREATE res-history.
				ASSIGN
					res-history.nr          = bediener.nr       
					res-history.datum       = TODAY
					res-history.zeit        = TIME
					res-history.aenderung   = "Add Pull Mapping RateCode, Booking Engine ID: " + STRING(bookengID) + ", RateCode: " + str
					res-history.action      = "Booking Engine".
				FIND CURRENT res-history NO-LOCK.
				RELEASE res-history.
			END.


		END.
	END.
	WHEN 2 THEN /*modify*/
	DO:
		FOR EACH t-push-list NO-LOCK:
			ASSIGN
			str = ""
			str = t-push-list.rcodeVHP   + ";"
				+ t-push-list.rcodeBE    + ";"
				+ t-push-list.rmtypeVHP  + ";"
				+ t-push-list.rmtypeBE   + ";"
				+ t-push-list.argtVHP.
			FIND FIRST qsy WHERE RECID(qsy) = t-push-list.flag EXCLUSIVE-LOCK NO-ERROR.
			IF AVAILABLE qsy THEN
			DO:
				ASSIGN 
					old-str = qsy.char1
					qsy.char1 = str
				.
				FIND CURRENT qsy NO-LOCK.
				RELEASE qsy.
				
			END.
			
			/*naufal - add for logfile*/
			FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
			IF AVAILABLE bediener THEN
			DO:
				CREATE res-history.
				ASSIGN
					res-history.nr          = bediener.nr       
					res-history.datum       = TODAY
					res-history.zeit        = TIME
					res-history.aenderung   = "Modify Pull Mapping RateCode, Booking Engine ID: " + STRING(bookengID) + ", From: " + old-str + " To " + str
					res-history.action      = "Booking Engine".
				FIND CURRENT res-history NO-LOCK.
				RELEASE res-history.
			END.
		END.
	END.
	WHEN 3 THEN /*delete*/
	DO:
		FOR EACH t-push-list NO-LOCK:
			FIND FIRST qsy WHERE RECID(qsy) = t-push-list.flag EXCLUSIVE-LOCK NO-ERROR.
			IF AVAILABLE qsy THEN
			DO:
				DELETE qsy.
				RELEASE qsy.
			END.
		END.
		
		/*naufal - add for logfile*/
		FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
		IF AVAILABLE bediener THEN
		DO:
			CREATE res-history.
			ASSIGN
				res-history.nr          = bediener.nr       
				res-history.datum       = TODAY
				res-history.zeit        = TIME
				res-history.aenderung   = "Deleted Pull Mapping RateCode, Booking Engine ID: " + STRING(bookengID) + ", RateCode: " + str
				res-history.action      = "Booking Engine".
			FIND CURRENT res-history NO-LOCK.
			RELEASE res-history.
		END.
	END.
END.