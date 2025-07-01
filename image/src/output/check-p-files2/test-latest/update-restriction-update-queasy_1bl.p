DEFINE TEMP-TABLE room-list
    FIELD bezeich AS CHAR
.

DEFINE TEMP-TABLE rcode-list
    FIELD bezeich AS CHAR
.

DEFINE INPUT PARAMETER from-date   AS DATE.
DEFINE INPUT PARAMETER to-date     AS DATE.
DEFINE INPUT PARAMETER inp-str     AS CHAR.
DEFINE INPUT PARAMETER rmtype      AS CHAR.
DEFINE INPUT PARAMETER ota         AS CHAR.
DEFINE INPUT PARAMETER restriction AS INT.
DEFINE INPUT PARAMETER flag        AS INT.

DEFINE VARIABLE i          AS INT NO-UNDO.
DEFINE VARIABLE cat-flag   AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE datum      AS DATE.
DEFINE VARIABLE ci-date    AS DATE.
DEFINE VARIABLE otanr      AS INT INIT 0.
DEFINE VARIABLE roomno     AS INT INIT 0.
DEFINE VARIABLE rcode      AS CHAR INIT "".
DEFINE VARIABLE user-init  AS CHAR INIT "".
DEFINE VARIABLE stat       AS CHAR INIT "".

IF restriction = 0 THEN
    stat = "CLOSE".
ELSE IF restriction = 1 THEN
    stat = "CTA".
IF restriction = 2 THEN
    stat = "CTD".

IF NUM-ENTRIES(inp-str,";") GT 1 THEN
    ASSIGN
        rcode = ENTRY(1,inp-str,";")
        user-init = ENTRY(2,inp-str,";").
ELSE
    rcode = inp-str.

DEFINE BUFFER qsy FOR queasy.
DEFINE BUFFER buffqsy FOR queasy.
DEFINE BUFFER qsy160 FOR queasy.
DEFINE BUFFER checkqsy FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.

FUNCTION rmstr2int RETURNS INT
    (INPUT roomstr AS CHAR).
    DEFINE VARIABLE roomnr AS INT.
    IF cat-flag THEN
    DO:
        FIND FIRST buffqsy WHERE buffqsy.KEY = 152 AND buffqsy.char1 = roomstr NO-LOCK NO-ERROR.
        IF AVAILABLE buffqsy THEN
            roomnr = buffqsy.number1.
    END.
    ELSE 
    DO:
        FIND FIRST zimkateg WHERE zimkateg.kurzbez = roomstr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN
            roomnr = zimkateg.zikatnr.
    END.
    RETURN roomnr.
END FUNCTION.

IF ota NE "" AND ota NE "*" THEN
DO:
    FIND FIRST guest WHERE guest.karteityp = 2 AND guest.steuernr NE "" 
        AND TRIM(ENTRY(1,guest.steuernr,"|")) = ota NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN otanr = guest.gastnr.
END.

IF rmtype = "*" THEN
DO:
    IF cat-flag THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK:
            FIND FIRST room-list WHERE room-list.bezeich = queasy.char1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE room-list THEN
            DO:
                CREATE room-list.
                ASSIGN
                    room-list.bezeich = queasy.char1.
            END.
        END.
    END.
    ELSE 
    DO:
        FOR EACH zimkateg NO-LOCK:
            FIND FIRST room-list WHERE room-list.bezeich = zimkateg.kurzbez NO-LOCK NO-ERROR.
            IF NOT AVAILABLE room-list THEN
            DO:
                CREATE room-list.
                ASSIGN
                    room-list.bezeich = zimkateg.kurzbez.
            END.
        END.
    END.
END.

IF rcode = "*" THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 159 NO-LOCK:
        FOR EACH guest-pr WHERE guest-pr.gastnr = queasy.number2 NO-LOCK:
            FIND FIRST qsy WHERE qsy.KEY = 2 AND qsy.char1 = guest-pr.CODE NO-LOCK NO-ERROR.
            IF AVAILABLE qsy THEN
            DO:
                FIND FIRST rcode-list WHERE rcode-list.bezeich = qsy.char1 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE rcode-list THEN
                DO:
                    CREATE rcode-list.
                    ASSIGN
                        rcode-list.bezeich = qsy.char1 .
                END.  
            END.
        END.
    END.
END.

IF rmtype NE "*" AND rcode NE "*" THEN
DO:
    roomno = rmstr2int(rmtype).

    DO datum = from-date TO to-date:
        FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
            AND queasy.date1 = datum AND queasy.number1 = roomno 
            AND queasy.number3 = otanr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
            RUN create-new-queasy(rcode,roomno).
        ELSE RUN update-queasy(rcode,roomno).

        IF ota = "*" THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
                AND queasy.date1 = datum AND queasy.number1 = roomno 
                AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE queasy:
                RUN update-queasy(rcode,roomno).
                FIND NEXT queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
                    AND queasy.date1 = datum AND queasy.number1 = roomno 
                    AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
    
            END.
        END.
    END.
END.
ELSE IF rmtype = "*" AND rcode NE "*" THEN
DO: 
    FOR EACH room-list NO-LOCK:
        roomno = rmstr2int(room-list.bezeich).
        DO datum = from-date TO to-date:
            FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
                AND queasy.number1 = roomno AND queasy.date1 = datum
                AND queasy.number3 = otanr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN RUN create-new-queasy(rcode,roomno).
            ELSE IF AVAILABLE queasy THEN RUN update-queasy(rcode,roomno).
    
            IF ota = "*" THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
                    AND queasy.number1 = roomno AND queasy.date1 = datum 
                    AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE queasy:
                    RUN update-queasy(rcode,roomno).
                    FIND NEXT queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
                        AND queasy.number1 = roomno AND queasy.date1 = datum
                        AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
                END.                                             
            END.
        END.
    END.    
END.
ELSE IF rmtype NE "*" AND rcode = "*" THEN
DO:
    roomno = rmstr2int(rmtype).
    FOR EACH rcode-list NO-LOCK:
        DO datum = from-date TO to-date:
            FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode-list.bezeich
                AND queasy.number1 = roomno  AND queasy.date1 = datum
                AND queasy.number3 = otanr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
                RUN create-new-queasy(rcode-list.bezeich,roomno).
            ELSE IF AVAILABLE queasy THEN
                RUN update-queasy(rcode-list.bezeich,roomno).
    
            IF ota = "*" THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode-list.bezeich
                    AND queasy.number1 = roomno AND queasy.date1 = datum
                    AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE queasy:
                    RUN update-queasy(rcode-list.bezeich,roomno).
                    FIND NEXT queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode-list.bezeich
                        AND queasy.number1 = roomno AND queasy.date1 = datum
                        AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
                END.                                             
            END.
        END.
    END.     
END.
ELSE IF rmtype = "*" AND rcode = "*" THEN
DO:
    FOR EACH rcode-list NO-LOCK:
        FOR EACH room-list NO-LOCK:
            DO datum = from-date TO to-date:
                roomno = rmstr2int(room-list.bezeich).
                FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode-list.bezeich
                    AND queasy.number1 = roomno AND queasy.date1 = datum
                    AND queasy.number3 = otanr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE queasy THEN
                    RUN create-new-queasy(rcode-list.bezeich,roomno).
                ELSE IF AVAILABLE queasy THEN
                    RUN update-queasy(rcode-list.bezeich,roomno).

                IF ota = "*" THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode-list.bezeich
                        AND queasy.number1 = roomno AND queasy.date1 = datum
                        AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
                    DO WHILE AVAILABLE queasy:
                        RUN update-queasy(rcode-list.bezeich,roomno).
                        FIND NEXT queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode-list.bezeich
                            AND queasy.number1 = roomno AND queasy.date1 = datum
                            AND queasy.number3 NE 0 NO-LOCK NO-ERROR.
                    END.                                             
                END.
            END.    
        END.
    END.
END.


/* force restriction-flag for all becode to be yes if any restriction update occurs (05/07/2021) */
DEF VAR str AS CHAR.
DEF VAR progavail AS LONGCHAR.
FOR EACH qsy160 WHERE qsy160.KEY = 160:
    DO i = 1 TO NUM-ENTRIES(qsy160.char1,";"):
        str = ENTRY(i, qsy160.char1, ";").
        IF SUBSTR(str,1,10) = "$progname$" THEN 
        DO:
            progavail = SUBSTR(str,11).
            IF NUM-ENTRIES(progavail,"=") GE 10 THEN
                ASSIGN
                    ENTRY(10,progavail,"=") = "yes"
                    ENTRY(i, qsy160.char1, ";") = "$progname$" + progavail.
        END.
    END.
END.



PROCEDURE create-new-queasy:
    DEFINE INPUT PARAMETER rate-code AS CHAR.
    DEFINE INPUT PARAMETER roomno    AS INT.
    
    DEFINE VARIABLE j AS INT INIT 0.

    CREATE queasy.
    ASSIGN
        queasy.KEY = 174
        queasy.char1   = rate-code
        queasy.number1 = roomno        
        queasy.number3 = otanr
        queasy.date1   = datum
        queasy.logi1   = YES
    .

    IF restriction = 0 THEN
        queasy.char2 = STRING(flag) + ";0;0".
    ELSE IF restriction = 1 THEN
        queasy.char2 = "0;" + STRING(flag) + ";0".
    ELSE IF restriction = 2 THEN
        queasy.char2 = "0;0;" + STRING(flag).
		
    CREATE queasy.
    ASSIGN
        queasy.KEY = 175
        queasy.char1   = rate-code
        queasy.char2   = stat
        queasy.number1 = roomno
        queasy.number2 = flag
        queasy.number3 = otanr
        queasy.date1   = datum
        queasy.date2   = ci-date
		queasy.logi3   = YES
    . 
	IF user-init NE "" THEN
	DO:
		FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
		CREATE res-history. 
		ASSIGN 
			res-history.nr     = bediener.nr 
			res-history.datum  = TODAY 
			res-history.zeit   = TIME 
			res-history.action = "Restriction"
		.
		res-history.aenderung = "RCode:" + rcode + ",Rmtype:" + rmtype + 
			"OTA:" + ota + ",Date:" + STRING(datum,"99/99/99") + ",".
		IF restriction = 0 THEN 
			res-history.aenderung = res-history.aenderung + 
				"CLOSE: 0 ChangeTo " + STRING(flag).
		ELSE IF restriction = 1 THEN 
			res-history.aenderung = res-history.aenderung + 
				"CTA: 0 ChangeTo " + STRING(flag).
		ELSE IF restriction = 2 THEN 
			res-history.aenderung = res-history.aenderung + 
				"CTD: 0 ChangeTo " + STRING(flag).
	END.
END.

PROCEDURE update-queasy:
    DEFINE INPUT PARAMETER rate-code AS CHAR.
    DEFINE INPUT PARAMETER roomno    AS INT.

    DEFINE VARIABLE curr-anz   AS INT INIT 0.

    DEFINE VARIABLE old-status AS CHAR.
    DEFINE VARIABLE new-status AS CHAR.

    DEFINE VARIABLE do-it AS LOGICAL INIT NO.

    IF restriction = 0 THEN
    DO:
        IF ENTRY(1,queasy.char2,";") NE STRING(flag) THEN
            do-it = YES.
    END.
    ELSE IF restriction = 1 THEN
    DO:
        IF ENTRY(2,queasy.char2,";") NE STRING(flag) THEN
            do-it = YES.
    END.
    ELSE IF restriction = 2 THEN
    DO:
        IF ENTRY(3,queasy.char2,";") NE STRING(flag) THEN
            do-it = YES.
    END.
    
    
    IF do-it THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        IF restriction = 0 THEN
		ASSIGN
            ENTRY(1,queasy.char2,";") = STRING(flag)
			ENTRY(2,queasy.char2,";") = "0" /*CTA Open*/
			ENTRY(3,queasy.char2,";") = "0". /*CTD Open*/
        ELSE IF restriction = 1 THEN
		ASSIGN
			ENTRY(1,queasy.char2,";") = "0" /* if Close then it should be Open*/
            ENTRY(2,queasy.char2,";") = STRING(flag).
        ELSE IF restriction = 2 THEN
		ASSIGN
			ENTRY(1,queasy.char2,";") = "0" /*If Close it should be Open*/
            ENTRY(3,queasy.char2,";") = STRING(flag).
	
		IF user-init NE "" THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
                res-history.nr     = bediener.nr 
                res-history.datum  = TODAY 
                res-history.zeit   = TIME 
                res-history.action = "Restriction"
            .
            res-history.aenderung = "RCode:" + rcode + ",Rmtype:" + rmtype + 
                "OTA:" + ota + ",Date:" + STRING(datum,"99/99/99") + ",".
            IF restriction = 0 THEN 
                res-history.aenderung = res-history.aenderung + 
                    "CLOSE: " + ENTRY(1,queasy.char2,";") + "ChangeTo" + STRING(flag).
            ELSE IF restriction = 1 THEN 
                res-history.aenderung = res-history.aenderung + 
                    "CTA: " + ENTRY(1,queasy.char2,";") + "ChangeTo" + STRING(flag).
            ELSE IF restriction = 2 THEN 
                res-history.aenderung = res-history.aenderung + 
                    "CTD: " + ENTRY(1,queasy.char2,";") + "ChangeTo" + STRING(flag).
        END.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
		
        FIND FIRST qsy WHERE qsy.KEY = 175
            AND qsy.char1   = rate-code
            AND qsy.number1 = roomno
            AND qsy.number3 = otanr
            AND qsy.date1 = datum
            AND qsy.char2 = stat NO-LOCK NO-ERROR.
        IF AVAILABLE qsy AND qsy.number2 NE flag THEN
        DO: 
            FIND CURRENT qsy EXCLUSIVE-LOCK.
            ASSIGN
				qsy.number2 = flag
				qsy.logi3 = YES.
            FIND CURRENT qsy NO-LOCK.
            RELEASE qsy.
        END.
        ELSE IF NOT AVAILABLE qsy THEN
        DO:
            CREATE qsy.
            ASSIGN
                qsy.KEY = 175
                qsy.char1   = rate-code
                qsy.char2 = stat
                qsy.number1 = roomno
                qsy.number2 = flag
                qsy.number3 = otanr
                qsy.date1 = datum
                qsy.date2 = ci-date
				qsy.logi3 = YES
            . 
        END.
    END. 
END.
