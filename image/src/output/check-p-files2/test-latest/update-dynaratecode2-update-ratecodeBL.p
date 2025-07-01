DEFINE TEMP-TABLE rate-list1
    FIELD origcode  AS CHAR
    FIELD counter   AS INTEGER
    FIELD w-day     AS INTEGER FORMAT "9" COLUMN-LABEL "WD" INIT 0
    FIELD rooms     AS CHAR FORMAT "x(8)" COLUMN-LABEL "Rooms"
    FIELD rcode     AS CHAR FORMAT "x(15)" EXTENT 31 COLUMN-LABEL "Rcode"
.

DEF INPUT PARAMETER TABLE FOR rate-list1.
DEF INPUT PARAMETER avail-room AS CHAR.
DEF INPUT PARAMETER chg-wday   AS INT.
DEF INPUT PARAMETER from-date  AS DATE.
DEF INPUT PARAMETER f-date     AS DATE.
DEF INPUT PARAMETER to-date    AS DATE.
DEF INPUT PARAMETER inp-str    AS CHAR.
DEF INPUT PARAMETER contrate-value AS CHAR.
DEF INPUT PARAMETER rmtype     AS CHAR.
DEF INPUT PARAMETER user-init  AS CHAR.

DEFINE VARIABLE inp-zikatnr    AS INTEGER NO-UNDO INIT 0.
DEFINE BUFFER buf-rate-list1   FOR rate-list1.

DEF VARIABLE currcode   AS CHAR    NO-UNDO.
DEF VARIABLE bookengID  AS INTEGER NO-UNDO.

DEF VARIABLE lastrcode    AS CHAR    NO-UNDO.
DEFINE BUFFER buffqueasy FOR queasy.

IF NUM-ENTRIES(inp-str,";") GT 1 THEN
    ASSIGN
        currcode = ENTRY(1,inp-str,";")
        bookengID = INT(ENTRY(2,inp-str,";"))
    .
ELSE currcode = inp-str.

IF bookengID = 0 THEN bookengID = 1.

FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmtype NO-LOCK NO-ERROR.
IF AVAILABLE zimkateg THEN inp-zikatnr = zimkateg.zikatnr.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

RUN update-ratecode.
IF bookengID NE 0 THEN RUN update-bookengine-config.

PROCEDURE update-ratecode:
DEF VAR curr-date AS DATE           NO-UNDO.
DEF VAR curr-i    AS INTEGER INIT 0 NO-UNDO.
  
/* SY 28Sept 2019 NOTE:
queasy.char1 dynamicc ratecode
queasy.char2 current static ratecode
queasy.char3 changed to new static ratecode
*/
DEF VARIABLE current-counter AS INTEGER NO-UNDO INIT 1.
DEF VARIABLE prev-ratecode   AS CHAR    NO-UNDO.
DEF VARIABLE avail-queasy    AS LOGICAL NO-UNDO.
DEF BUFFER qbuff FOR queasy.

  FOR EACH queasy WHERE queasy.KEY = 209 AND queasy.char1 = currcode
    NO-LOCK BY queasy.deci3 DESCENDING:
    current-counter = queasy.deci3 + 1.
    LEAVE.
  END.

  IF avail-room NE "ALL" THEN
  FOR EACH rate-list1 WHERE rate-list1.rooms = avail-room
    AND rate-list1.w-day = chg-wday:

    curr-i = from-date - f-date.
    DO curr-date = from-date TO to-date:
        curr-i = curr-i + 1.
        IF rate-list1.origcode = contrate-value THEN
        DO:
		
          FIND FIRST queasy WHERE queasy.KEY  = 145
            AND queasy.char1                  = currcode
            AND queasy.char2                  = rate-list1.origcode
            AND queasy.number1                = inp-zikatnr
            AND queasy.deci1                  = rate-list1.w-day
            AND queasy.deci2                  = rate-list1.counter
            AND queasy.date1                  = curr-date 
            EXCLUSIVE-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN 
          DO:    
              CREATE qbuff.
              BUFFER-COPY queasy EXCEPT KEY TO qbuff.
              ASSIGN
                  qbuff.KEY   = 209
                  qbuff.deci3 = current-counter
              .
              FIND CURRENT qbuff NO-LOCK.
              DELETE queasy.
          END.
        END.
        ELSE IF rate-list1.rcode[curr-i] NE ? THEN
        DO:
		
          IF user-init NE "" THEN
          DO:
			
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
            FIND FIRST buffqueasy WHERE buffqueasy.KEY = 145
            AND buffqueasy.char1                   = currcode
            AND buffqueasy.char2                   = rate-list1.origcode
            AND buffqueasy.number1                 = inp-zikatnr
            AND buffqueasy.deci1                   = rate-list1.w-day
            AND buffqueasy.deci2                   = rate-list1.counter
            AND buffqueasy.date1                   = curr-date 
            NO-LOCK NO-ERROR.
            IF AVAILABLE buffqueasy THEN
            lastrcode = buffqueasy.char3.            
            
            CREATE res-history. 
            ASSIGN 
                res-history.nr     = bediener.nr 
                res-history.datum  = TODAY 
                res-history.zeit   = TIME 
                res-history.action = "UpdateDynaRateCode"
                res-history.aenderung = "RateCode: " + currcode + ", Occupancy: " + rate-list1.rooms + " Date: " + STRING(YEAR(curr-date),"9999") + STRING(MONTH(curr-date),"99") +
                    STRING(DAY(curr-date),"99") + "," + lastrcode + " ChangeTo " + contrate-value. 
            . 
          END.

          FIND FIRST queasy WHERE queasy.KEY  = 145
            AND queasy.char1                  = currcode
            AND queasy.char2                  = rate-list1.origcode
            AND queasy.number1                = inp-zikatnr
            AND queasy.deci1                  = rate-list1.w-day
            AND queasy.deci2                  = rate-list1.counter
            AND queasy.date1                  = curr-date 
            EXCLUSIVE-LOCK NO-ERROR.
          IF NOT AVAILABLE queasy THEN 
          DO:
            prev-ratecode = rate-list1.origcode.
            CREATE queasy.
            ASSIGN
                queasy.KEY     = 145
                queasy.char1   = currcode
                queasy.char2   = rate-list1.origcode
                queasy.deci2   = rate-list1.counter
                queasy.number1 = inp-zikatnr
                queasy.deci1   = rate-list1.w-day
                queasy.date1 = curr-date
            .
          END.
          ELSE prev-ratecode = queasy.char3.
          ASSIGN 
              queasy.char3   = contrate-value
              queasy.number2 = bediener.nr
              queasy.number3 = TIME
              queasy.date2   = TODAY.
          FIND FIRST buf-rate-list1 WHERE RECID(buf-rate-list1) = RECID(rate-list1).
              buf-rate-list1.rcode[curr-i] = contrate-value
          .
          FIND CURRENT queasy NO-LOCK.
          /* SY 28Sept 2019 */   
          CREATE qbuff.
          BUFFER-COPY queasy EXCEPT KEY TO qbuff.
          ASSIGN
              qbuff.KEY   = 209
              qbuff.char3 = prev-ratecode
              qbuff.deci3 = current-counter
          .
          FIND CURRENT qbuff NO-LOCK.
        END.
    END.
  END.
  ELSE
  FOR EACH rate-list1 WHERE rate-list1.w-day = chg-wday:
    curr-i = from-date - f-date.
    DO curr-date = from-date TO to-date:
        curr-i = curr-i + 1.
        IF rate-list1.origcode = contrate-value THEN
        DO: 

        FIND FIRST queasy WHERE queasy.KEY  = 145
            AND queasy.char1                  = currcode
            AND queasy.char2                  = rate-list1.origcode
            AND queasy.number1                = inp-zikatnr
            AND queasy.deci1                  = rate-list1.w-day
            AND queasy.deci2                  = rate-list1.counter
            AND queasy.date1                  = curr-date 
            EXCLUSIVE-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO: /* SY 28Sept 2019 */   
              CREATE qbuff.
              BUFFER-COPY queasy EXCEPT KEY TO qbuff.
              ASSIGN
                  qbuff.KEY   = 209
                  qbuff.deci3 = current-counter
              .
              FIND CURRENT qbuff NO-LOCK.
              DELETE queasy.
          END.
        END.
        ELSE IF rate-list1.rcode[curr-i] NE ? THEN
        DO:
			IF user-init NE "" THEN
			DO:
				FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
				FIND FIRST buffqueasy WHERE buffqueasy.KEY = 145
				AND buffqueasy.char1                   = currcode
				AND buffqueasy.char2                   = rate-list1.origcode
				AND buffqueasy.number1                 = inp-zikatnr
				AND buffqueasy.deci1                   = rate-list1.w-day
				AND buffqueasy.deci2                   = rate-list1.counter
				AND buffqueasy.date1                   = curr-date 
				NO-LOCK NO-ERROR.
				IF AVAILABLE buffqueasy THEN
				lastrcode = buffqueasy.char3.            
				
				CREATE res-history. 
				ASSIGN 
					res-history.nr     = bediener.nr 
					res-history.datum  = TODAY 
					res-history.zeit   = TIME 
					res-history.action = "UpdateDynaRateCode"
					res-history.aenderung = "RateCode: " + currcode + ", Occupancy: ALL, Date: " + STRING(YEAR(curr-date),"9999") + STRING(MONTH(curr-date),"99") +
						STRING(DAY(curr-date),"99") + "," + lastrcode + " ChangeTo " + contrate-value. 
				 
			END.		
          FIND FIRST queasy WHERE queasy.KEY  = 145
            AND queasy.char1                  = currcode
            AND queasy.char2                  = rate-list1.origcode
            AND queasy.number1                = inp-zikatnr
            AND queasy.deci1                  = rate-list1.w-day
            AND queasy.deci2                  = rate-list1.counter
            AND queasy.date1                  = curr-date 
            EXCLUSIVE-LOCK NO-ERROR.
          IF NOT AVAILABLE queasy THEN 
          DO:    
            prev-ratecode = rate-list1.origcode.
            CREATE queasy.
            ASSIGN
                queasy.KEY     = 145
                queasy.char1   = currcode
                queasy.char2   = rate-list1.origcode
                queasy.number1 = inp-zikatnr
                queasy.deci1   = rate-list1.w-day
                queasy.deci2   = rate-list1.counter
                queasy.date1   = curr-date
            .
          END.
          ELSE prev-ratecode = queasy.char3.
          ASSIGN 
              queasy.char3   = contrate-value
              queasy.number2 = bediener.nr
              queasy.number3 = TIME
              queasy.date2   = TODAY.
          FIND FIRST buf-rate-list1 WHERE RECID(buf-rate-list1) = RECID(rate-list1).
              buf-rate-list1.rcode[curr-i] = contrate-value.
          
          FIND CURRENT queasy NO-LOCK.
          /* SY 28Sept 2019 */   
          CREATE qbuff.
          BUFFER-COPY queasy EXCEPT KEY TO qbuff.
          ASSIGN
              qbuff.KEY   = 209
              qbuff.char3 = prev-ratecode
              qbuff.deci3 = current-counter
          .
          FIND CURRENT qbuff NO-LOCK.
        END.
    END.
  END.
  /*MTb11:REFRESH().*/
END.

PROCEDURE update-bookengine-config:
    DEFINE VARIABLE cm-gastno AS INT NO-UNDO INIT 0.
    DEFINE BUFFER qsy FOR queasy.
    DEFINE BUFFER bqueasy FOR queasy.
    DEFINE VARIABLE datum AS DATE NO-UNDO.

    DEFINE VARIABLE ifTask      AS CHAR INIT "".
    DEFINE VARIABLE mesToken    AS CHAR INIT "".
    DEFINE VARIABLE mesValue    AS CHAR INIT "".
    DEFINE VARIABLE tokcounter  AS INT  INIT 0.

    DO datum = from-date TO to-date:
        FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum AND qsy.char1 = currcode
            AND qsy.logi1 = NO AND qsy.logi2 = NO NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE qsy:
            FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(qsy) EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE bqueasy THEN
            DO:
                ASSIGN bqueasy.logi2 = YES.
                FIND CURRENT bqueasy NO-LOCK.
                RELEASE bqueasy.
            END.                
            FIND NEXT qsy WHERE qsy.KEY = 170 AND qsy.date1 = datum AND qsy.char1 = currcode
                AND qsy.logi1 = NO AND qsy.logi2 = NO NO-LOCK NO-ERROR.
        END.
    END.
END.

