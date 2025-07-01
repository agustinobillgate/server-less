DEF TEMP-TABLE t-kontline   LIKE kontline.

DEF INPUT PARAMETER case-type   AS INTEGER.
DEF INPUT PARAMETER TABLE FOR t-kontline.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.
DEF VARIABLE curr-date       AS DATE         NO-UNDO INITIAL ?. /*NC-19/08/20*/

DEF BUFFER qsy   FOR queasy.

FIND FIRST t-kontline NO-ERROR.
IF NOT AVAILABLE t-kontline THEN
    RETURN NO-APPLY.

CASE case-type :
    WHEN 1 THEN
    DO: 
		DO curr-date = t-kontline.ankunft TO t-kontline.abreise:
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date
				AND queasy.number1 = t-kontline.zikatnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
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
        FIND FIRST kontline WHERE
            kontline.kontignr EQ t-kontline.kontignr
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE kontline THEN
        DO:
            BUFFER-COPY t-kontline TO kontline.
            FIND CURRENT kontline NO-LOCK.
            success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
		DO curr-date = t-kontline.ankunft TO t-kontline.abreise:
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date
				AND queasy.number1 = t-kontline.zikatnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
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
        CREATE kontline.
        BUFFER-COPY t-kontline TO kontline.
        success-flag = YES.
        FIND CURRENT kontline NO-LOCK.
    END.
END CASE.

