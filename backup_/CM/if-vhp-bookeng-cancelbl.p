DEFINE INPUT PARAMETER BEcode           AS INT      NO-UNDO.
DEFINE INPUT PARAMETER uniq-id          AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER ota-code         AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR     NO-UNDO INIT "".

DEFINE VARIABLE cancel-msg      AS CHAR    INIT ""      NO-UNDO.
DEFINE VARIABLE del-mainres     AS LOGICAL INIT NO      NO-UNDO.
DEFINE VARIABLE cm-gastno       AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE ota-gastnr      AS INTEGER INIT 0       NO-UNDO.
DEFINE VARIABLE check-integer   AS INTEGER INIT 0       NO-UNDO.

/*NC - 21/06/22*/
DEFINE VARIABLE cat-flag        AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE bill-date       AS DATE         NO-UNDO.
DEFINE VARIABLE upto-date       AS DATE         NO-UNDO.
DEFINE VARIABLE zikatnr 		AS INTEGER NO-UNDO.
DEFINE VARIABLE ifTask      	AS CHAR    NO-UNDO.
DEFINE VARIABLE rline-origcode  AS CHAR    NO-UNDO.
DEFINE VARIABLE i             AS INT INIT 0 NO-UNDO.  
DEFINE BUFFER qsy       FOR queasy.
DEFINE BUFFER rqueasy   FOR queasy.
DEFINE BUFFER bqueasy   FOR queasy.

FIND FIRST queasy WHERE queasy.KEY = 159 AND queasy.number1 = beCode
    NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
    ASSIGN cm-gastno = queasy.number2.
	
FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.
IF ota-code NE "" THEN
DO:
    FIND FIRST guest WHERE TRIM(ENTRY(1, guest.steuernr, "|")) MATCHES 
    TRIM(ota-code) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE guest THEN     /*tidak ketemu guest dengan OTA code*/
    DO:
        FIND FIRST guest WHERE guest.gastnr = cm-gastno NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
            ota-gastnr = guest.gastnr. /*Dialihkan ke GuestCard Booking Engine*/
        ELSE
        DO:        
            msg-str = "GuestNo " + STRING(cm-gastno) + " not found".
            RETURN.
        END.
    END.
    ELSE ota-gastnr = guest.gastnr. /*ketemu guest dengan OTA code*/
END.
ELSE
    ota-gastnr = cm-gastno.

FIND FIRST reservation WHERE reservation.gastnr = ota-gastnr 
    AND reservation.vesrdepot = uniq-id AND reservation.activeflag = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE reservation THEN
FIND FIRST reservation WHERE reservation.vesrdepot = uniq-id
    AND reservation.activeflag = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE reservation THEN
DO:
    msg-str = "Reservation " + uniq-id + " not found".
	/*NC - 21/06/22 trigger to push availability*/
	FIND FIRST reservation WHERE reservation.vesrdepot = uniq-id NO-LOCK NO-ERROR.
	IF AVAILABLE reservation THEN
	DO:
		FOR EACH res-line WHERE res-line.resnr = reservation.resnr NO-LOCK :
			IF res-line.ankunft EQ res-line.abreise THEN upto-date = res-line.abreise.
			ELSE upto-date = res-line.abreise - 1.
			DO bill-date = res-line.ankunft TO upto-date :
				FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
				IF AVAILABLE zimkateg THEN
				DO:
					IF cat-flag THEN
						zikatnr = zimkateg.typ.
					ELSE
						zikatnr = zimkateg.zikatnr.
				END.
				
				rline-origcode = "".
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                    DO:
                        rline-origcode  = SUBSTR(iftask,11).
                        LEAVE.
                    END.
                END.

				FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
				  AND qsy.number1 = zikatnr AND qsy.char1 = rline-origcode NO-LOCK NO-ERROR.
				IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
				DO:
					FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
					IF AVAILABLE bqueasy THEN
					DO:
						bqueasy.logi2 = YES.
						FIND CURRENT bqueasy NO-LOCK.
						RELEASE bqueasy.
					END.
				END.
				
				FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.date1 = bill-date
				  AND qsy.number1 = zikatnr AND qsy.char1 = "" NO-LOCK NO-ERROR.
				IF AVAILABLE qsy AND qsy.logi1 = NO AND qsy.logi2 = NO THEN
				DO:
					FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
					IF AVAILABLE bqueasy THEN
					DO:
						bqueasy.logi2 = YES.
						FIND CURRENT bqueasy NO-LOCK.
						RELEASE bqueasy.
					END.
				END.
			END.
		END.
	END.
	RETURN.
END.
ELSE
FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
        AND res-line.l-zuordnung[3] = 0 
        AND res-line.active-flag = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN
DO:
    msg-str = "Cancel Reservation " + uniq-id + " not possible.".
    RETURN.
END.
ELSE
DO:    
    IF reservation.depositgef NE 0 THEN
    DO:
		/*
        FIND CURRENT reservation EXCLUSIVE-LOCK.
        reservation.vesrdepot2 = "Cancelled by BookEngine".
        FIND CURRENT reservation NO-LOCK.
		*/
		RUN reservation-cancel-with-deposit_1bl.p(res-line.resnr,res-line.reslinnr, "Cancelled by BookEngine").

        /* CRG 17/07/2023 cancel data trigger for crm */
        RUN intevent-1.p(14, "", "Priscilla", res-line.resnr, res-line.reslinnr).
    END.
    ELSE
    FOR EACH res-line WHERE res-line.resnr = reservation.resnr 
        AND (res-line.active-flag NE 1 AND res-line.resstatus NE 6 AND res-line.resstatus NE 13
             AND res-line.resstatus NE 8 AND res-line.resstatus NE 10) NO-LOCK:
        RUN del-reslinebl.p(1, "cancel", res-line.resnr, res-line.reslinnr, 
            "**", "Cancelled by BookEngine", OUTPUT del-mainres, OUTPUT cancel-msg).
        IF cancel-msg NE "" THEN
            ASSIGN msg-str = msg-str + cancel-msg + " ".

        /* CRG 17/07/2023 cancel data trigger for crm */
        RUN intevent-1.p(14, "", "Priscilla", res-line.resnr, res-line.reslinnr).
    END.

    success-flag = YES.
END.
