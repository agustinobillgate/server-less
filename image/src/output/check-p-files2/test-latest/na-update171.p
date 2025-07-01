DEFINE VARIABLE ci-date AS DATE NO-UNDO.
DEFINE BUFFER qsy FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ci-date = htparam.fdate.

DO TRANSACTION:
	FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = ci-date AND queasy.logi2 = NO AND queasy.logi1 = NO NO-LOCK NO-ERROR.
	REPEAT WHILE AVAILABLE queasy:

		FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
		IF AVAILABLE qsy THEN
		DO:

			ASSIGN
				qsy.logi2 = YES.
			FIND CURRENT qsy NO-LOCK.
			RELEASE qsy.
		END.
	   
		FIND NEXT queasy WHERE queasy.KEY = 171 AND queasy.date1 = ci-date AND queasy.logi2 = NO AND queasy.logi1 = NO NO-LOCK NO-ERROR. 
	END.
END.	