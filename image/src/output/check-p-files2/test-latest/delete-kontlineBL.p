
DEFINE INPUT  PARAMETER case-type    AS INT.
DEFINE INPUT  PARAMETER kontignr     AS INT.
DEFINE INPUT  PARAMETER kontcode     AS CHAR.
DEFINE INPUT  PARAMETER gastNo       AS INT.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEFINE VARIABLE curr-date       AS DATE         NO-UNDO INITIAL ?. /*NC-19/08/20*/
DEFINE VARIABLE zikatnr AS INTEGER 			NO-UNDO.
DEF BUFFER qsy   FOR queasy.

DEF BUFFER kline FOR kontline.

CASE case-type:
    WHEN 1 THEN
    DO:
		FIND FIRST kontline WHERE kontline.kontignr = kontignr 
            AND kontline.gastnr  = gastNo NO-LOCK NO-ERROR.
		FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK NO-ERROR. 
		IF AVAILABLE zimkateg THEN
		DO:
			FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
			IF AVAILABLE queasy AND zimkateg.typ NE 0 THEN
				zikatnr = zimkateg.typ.
			ELSE
				zikatnr = zimkateg.zikatnr.
		END.
		DO curr-date = kontline.ankunft TO kontline.abreise:
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = curr-date
				AND queasy.number1 = zikatnr NO-LOCK NO-ERROR.
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
            kontline.kontignr    = kontignr 
            AND kontline.gastnr  = gastNo EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE kontline THEN
        DO:
            DELETE kontline.
            RELEASE kontline.
            ASSIGN success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST kontline WHERE kontline.kontcode = kontcode 
          AND kontline.kontstat = gastNo NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE kontline:
			FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK NO-ERROR. 
			IF AVAILABLE zimkateg THEN
			DO:
				FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
				IF AVAILABLE queasy AND zimkateg.typ NE 0 THEN
					zikatnr = zimkateg.typ.
				ELSE
					zikatnr = zimkateg.zikatnr.
			END.
			DO curr-date = kontline.ankunft TO kontline.abreise:
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
			END.
          FIND FIRST kline WHERE ROWID(kline) = ROWID(kontline) EXCLUSIVE-LOCK. 
          DELETE kline. 
          FIND NEXT kontline WHERE kontline.kontcode = kontcode NO-LOCK NO-ERROR.
        END.
    END.
END CASE.

