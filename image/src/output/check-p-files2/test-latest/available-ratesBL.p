
DEFINE TEMP-TABLE created-list
    FIELD rateCode      AS CHARACTER
    FIELD marknr        AS INTEGER INIT 0
    FIELD rmcateg       AS INTEGER
    FIELD argtno        AS INTEGER
    FIELD statCode      AS CHARACTER EXTENT 30
    FIELD rmRate        AS DECIMAL   EXTENT 30 
      INIT [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
.

DEFINE TEMP-TABLE rate-list
    FIELD rateCode      AS CHARACTER
    FIELD segmentcode   AS CHAR
    FIELD dynaflag      AS LOGICAL INIT NO
    FIELD expired       AS LOGICAL INIT NO
    FIELD room-type     AS INTEGER
    FIELD argtno        AS INTEGER
    FIELD statCode      AS CHARACTER EXTENT 30
    FIELD rmRate        AS DECIMAL   EXTENT 30 
      INIT [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    FIELD minstay       AS INTEGER INIT 0
    FIELD maxstay       AS INTEGER INIT 0
    FIELD minadvance    AS INTEGER INIT 0
    FIELD maxadvance    AS INTEGER INIT 0    
    FIELD frdate        AS DATE INIT ?
    FIELD todate        AS DATE INIT ?
    FIELD adult         AS INTEGER
    FIELD child         AS INTEGER    
    FIELD currency      AS INTEGER
    FIELD wabkurz       AS CHAR
    FIELD occ-rooms     AS INTEGER INIT 0
    FIELD marknr        AS INTEGER INIT 0
    FIELD i-counter     AS INTEGER
.

DEFINE TEMP-TABLE dynaRate-list
  FIELD counter  AS INTEGER
  FIELD w-day    AS INTEGER FORMAT "9"     LABEL "WeekDay" INIT 0 /* week day 0=ALL, 1=Mon..7=Sun */
  FIELD rmType   AS CHAR    FORMAT "x(10)" LABEL "Room Type"
  FIELD fr-room  AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
  FIELD to-room  AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
  FIELD days1    AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
  FIELD days2    AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
  FIELD rCode    AS CHAR    FORMAT "x(10)" LABEL "RateCode" /* statcode */
  FIELD dynaCode AS CHAR    FORMAT "x(10)" LABEL "RateCode" /* dynacode */.

DEF TEMP-TABLE selected-ratelist
    FIELD rateCode  AS CHARACTER
    FIELD marknr    AS INTEGER
    FIELD argtno    AS INTEGER
    FIELD adult     AS INTEGER
    FIELD child     AS INTEGER
    FIELD minstay   AS INTEGER
    FIELD maxstay   AS INTEGER
.

DEFINE BUFFER buff-rlist    FOR rate-list.
DEFINE BUFFER buff-dynaRate FOR dynaRate-list.
DEFINE BUFFER bratecode     FOR ratecode.
DEFINE BUFFER bqueasy       FOR queasy.
DEFINE BUFFER qsy18         FOR queasy.

DEFINE INPUT  PARAMETER frDate              AS DATE     NO-UNDO.
DEFINE INPUT  PARAMETER toDate              AS DATE     NO-UNDO.
DEFINE INPUT  PARAMETE  i-zikatnr           AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETE  i-counter           AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER adult-child-str     AS CHAR     NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER ind-gastno    AS INTEGER  NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR created-list.
DEFINE OUTPUT PARAMETER TABLE FOR rate-list.

/*
DEFINE VARIABLE frDate      AS DATE INITIAL 08/19/2014.
DEFINE VARIABLE toDate      AS DATE.
todate = frDate + 29.
DEFINE VARIABLE ind-gastno  AS INTEGER INIT 4.
DEFINE VARIABLE i-counter   AS INTEGER INIT 1.
DEFINE VARIABLE i-zikatnr   AS INTEGER INIT 1.
DEFINE VARIABLE adult-child-str AS CHAR NO-UNDO INIT "&A2,0".
*/

DEFINE VARIABLE adult          AS INTEGER          NO-UNDO.
DEFINE VARIABLE child          AS INTEGER          NO-UNDO.
DEFINE VARIABLE rooms          AS INTEGER INIT 1   NO-UNDO.
DEFINE VARIABLE inp-resnr      AS INTEGER          NO-UNDO INIT 0.
DEFINE VARIABLE inp-reslinnr   AS INTEGER INIT 0   NO-UNDO.

DEFINE VARIABLE rmType      AS INTEGER          NO-UNDO.
DEFINE VARIABLE argtNo      AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE markNo      AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE wahrNo      AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE tokcounter  AS INTEGER          NO-UNDO.
DEFINE VARIABLE ifTask      AS CHAR             NO-UNDO.
DEFINE VARIABLE mesToken    AS CHAR             NO-UNDO.
DEFINE VARIABLE mesValue    AS CHAR             NO-UNDO.
DEFINE VARIABLE currency    AS CHAR INIT ""     NO-UNDO.
DEFINE VARIABLE mapcode     AS CHAR INIT ""     NO-UNDO.
DEFINE VARIABLE datum       AS DATE             NO-UNDO.
DEFINE VARIABLE ankunft     AS DATE             NO-UNDO.
DEFINE VARIABLE dynacode    AS CHAR INIT ""     NO-UNDO.
DEFINE VARIABLE num-date    AS INTEGER          NO-UNDO. /* Malik Serverless 143 */


DEFINE VARIABLE rmtype-str  AS CHAR             NO-UNDO INIT "".
DEFINE VARIABLE curr-i      AS INTEGER          NO-UNDO.
DEFINE VARIABLE curr-date   AS DATE             NO-UNDO.

DEFINE VARIABLE rm-rate     AS DECIMAL           NO-UNDO.
DEFINE VARIABLE rate-found  AS LOGICAL           NO-UNDO.
DEFINE VARIABLE restricted  AS LOGICAL           NO-UNDO.
DEFINE VARIABLE kback-flag  AS LOGICAL           NO-UNDO.
DEFINE VARIABLE global-occ  AS LOGICAL           NO-UNDO INIT NO.

DEFINE VARIABLE dd                  AS INTEGER  NO-UNDO.
DEFINE VARIABLE mm                  AS INTEGER  NO-UNDO.
DEFINE VARIABLE yyyy                AS INTEGER  NO-UNDO.

DEFINE VARIABLE ci-date             AS DATE     NO-UNDO.
DEFINE VARIABLE co-date             AS DATE     NO-UNDO INIT ?.
DEFINE VARIABLE map-code            AS CHAR     NO-UNDO.
DEFINE VARIABLE use-it              AS LOGICAL  NO-UNDO.
DEFINE VARIABLE w-day               AS INTEGER  NO-UNDO.
DEFINE VARIABLE occ-rooms           AS INTEGER  NO-UNDO INIT 0.
DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE VARIABLE occ-room-array AS INTEGER EXTENT 30 NO-UNDO.
DEFINE VARIABLE not-found-flag AS LOGICAL           NO-UNDO INIT NO.
DEFINE VARIABLE do-it          AS LOGICAL           NO-UNDO.
DEFINE VARIABLE rate-created   AS LOGICAL           NO-UNDO INIT NO.
DEFINE VARIABLE allotment-ok   AS LOGICAL           NO-UNDO INIT NO.
DEFINE VARIABLE calc-rm        AS LOGICAL           NO-UNDO INIT NO.

DEFINE BUFFER ratebuff FOR ratecode.
DEFINE BUFFER dynabuff FOR dynaRate-list.

/*************************** MAIN LOGIC *******************************/

FIND FIRST htparam WHERE htparam.paramnr = 459 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN calc-rm = htparam.flogical.

IF ind-gastno = 0 THEN
DO:
  RUN htpint.p(123, OUTPUT ind-gastno).
  IF ind-gastno = 0 THEN RETURN.
END.

ASSIGN
    adult-child-str = SUBSTR(adult-child-str,3)
    adult           = INTEGER(ENTRY(1, adult-child-str, ","))
    child           = INTEGER(ENTRY(2, adult-child-str, ",")) NO-ERROR
.

IF NUM-ENTRIES(adult-child-str,",") GT 2 THEN
DO:
  ASSIGN
    i-counter = i-counter * 100
    mm        = INTEGER(SUBSTR(ENTRY(3, adult-child-str, ","),1,2))
    dd        = INTEGER(SUBSTR(ENTRY(3, adult-child-str, ","),3,2))
    yyyy      = INTEGER(SUBSTR(ENTRY(3, adult-child-str, ","),5,4))
    co-date   = DATE(mm, dd, yyyy) + 1
  .
  IF toDate GT co-date THEN toDate = co-date.
END.

IF NUM-ENTRIES(adult-child-str,",") GT 3 THEN
ASSIGN
    rooms       = INTEGER(ENTRY(4, adult-child-str, ","))
    inp-resnr   = INTEGER(ENTRY(5, adult-child-str, ","))
    inp-reslinnr= INTEGER(ENTRY(6, adult-child-str, ",")) NO-ERROR
.

FIND FIRST zimkateg WHERE zimkateg.zikatnr = i-zikatnr NO-LOCK NO-ERROR. /* Malik Serverless 143 */
IF NOT AVAILABLE zimkateg THEN RETURN. /* Malik Serverless 143 */


FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

IF frDate = ci-date THEN ankunft = ci-date.
ELSE ankunft = frDate + 2.

num-date = ankunft - ci-date. /* Malik Serverless 143 */

FOR EACH guest-pr WHERE guest-pr.gastnr = ind-gastno NO-LOCK,
  FIRST bqueasy WHERE bqueasy.KEY = 2 
  AND bqueasy.char1 = guest-pr.CODE NO-LOCK 
  BY bqueasy.logi2 
  BY bqueasy.number3 DESCENDING /* min advance booking */
  BY bqueasy.deci3 DESCENDING   /* max advance booking */:
  
  /* minimum advance booking not fulfilled */
  IF bqueasy.number3 GT num-date THEN . 
  
   /* maximum advance booking not fulfilled */
  ELSE IF bqueasy.deci3 GT 0 
      AND bqueasy.deci3 LT num-date THEN . 

  ELSE IF NOT bqueasy.logi2 THEN
  DO:
    FOR EACH bratecode WHERE bratecode.CODE = guest-pr.CODE 
        AND bratecode.zikatnr = i-zikatnr 
        AND bratecode.erwachs = adult
        AND bratecode.kind1   = child
        AND NOT (bratecode.startperiode GT toDate) 
        AND NOT (bratecode.endperiode LT frDate) NO-LOCK
        BY bratecode.wday DESCENDING BY bratecode.erwachs 
        BY bratecode.startperiode:
        do-it = YES.
        IF bqueasy.number3 NE 0 THEN
        DO:
          FIND FIRST buff-rlist WHERE buff-rlist.ratecode NE bratecode.CODE /* Malik Serverless 143 : buff-rlist.rateCode -> buff-rlist.ratecode */
            AND buff-rlist.room-type = bratecode.zikatnr
            AND buff-rlist.argtno = bratecode.argtnr
            AND buff-rlist.adult = bratecode.erwachs
            AND buff-rlist.child = bratecode.kind1
            AND buff-rlist.marknr = bratecode.marknr 
            NO-ERROR.
          do-it =  NOT AVAILABLE buff-rlist.
        END.

        IF do-it THEN
        DO:
            FIND FIRST rate-list WHERE rate-list.ratecode = bratecode.CODE /* Malik Serverless 143 : rate-list.rateCode -> rate-list.ratecode */
                AND rate-list.room-type = bratecode.zikatnr
                AND rate-list.argtno = bratecode.argtnr
                AND rate-list.adult = bratecode.erwachs
                AND rate-list.child = bratecode.kind1
                AND rate-list.marknr = bratecode.marknr NO-ERROR.
            IF NOT AVAILABLE rate-list THEN
            DO:
                FIND FIRST qsy18 WHERE qsy18.key = 18 
                  AND qsy18.number1 = bratecode.marknr NO-LOCK NO-ERROR.
                FIND FIRST waehrung WHERE waehrung.wabkurz = qsy18.char3
                    NO-LOCK.
                CREATE rate-list.
                ASSIGN
                    i-counter            = i-counter + 1
                    rate-list.i-counter  = i-counter
                    rate-list.ratecode   = bratecode.CODE /* Malik Serverless 143 : rate-list.rateCode -> rate-list.ratecode */
                    rate-list.room-type  = bratecode.zikatnr
                    rate-list.argtno     = bratecode.argtnr
                    rate-list.adult      = bratecode.erwachs
                    rate-list.child      = bratecode.kind1
                    rate-list.marknr     = bratecode.marknr
                    rate-list.currency   = bqueasy.number1
                    rate-list.minstay    = bqueasy.number2
                    rate-list.maxstay    = bqueasy.deci2
                    rate-list.minadvance = bqueasy.number3
                    rate-list.maxadvance = bqueasy.deci3
                    rate-list.frdate     = bqueasy.date1
                    rate-list.todate     = bqueasy.date2
                    rate-list.wabkurz    = waehrung.wabkurz
                .
                IF bqueasy.char3 NE "" THEN
                DO:
                  FIND FIRST segment WHERE segment.bezeich = bqueasy.char3
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE segment THEN rate-list.segmentcode = 
                      STRING(segment.segmentcode) + " " + segment.bezeich.
                END.
                IF bqueasy.date1 NE ? AND (ci-date LT bqueasy.date1) 
                    THEN rate-list.expired = YES.
                IF bqueasy.date2 NE ? AND (ci-date GT bqueasy.date2) 
                    THEN rate-list.expired = YES.
            END.
            curr-i = 0.
            IF NOT rate-list.expired THEN
            DO curr-date = frDate TO toDate:
                curr-i = curr-i + 1.
                RUN check-allotment (bqueasy.char1, bqueasy.char1,
                    curr-date, OUTPUT allotment-ok).
                ASSIGN rate-found = allotment-ok.
                IF allotment-ok THEN
                RUN ratecode-rate.p(NO, NO, 0, 1, ("!" + bqueasy.char1), 
                  ci-date, curr-date, curr-date, curr-date, 
                  rate-list.marknr, rate-list.argtno, i-zikatnr, 
                  rate-list.adult, rate-list.child, 0, 0, 
                  rate-list.currency, OUTPUT rate-found, OUTPUT rm-Rate, 
                  OUTPUT restricted, OUTPUT kback-flag).
                IF rate-found THEN
                ASSIGN 
                    rate-list.rmRate[curr-i] = rm-rate
                    rate-list.statcode[curr-i] = bqueasy.char1 /* Malik Serverless 143 : rate-list.statCode -> rate-list.statcode */
                .
                /* SY 05 Aug 2015 */
                ELSE rate-list.rmRate[curr-i] = -0.001.
            END.
        END.
    END.
  END.
  ELSE IF bqueasy.logi2 THEN
  DO: 
    FOR EACH dynarate-list:
        DELETE dynarate-list.
    END.

    FOR EACH bratecode WHERE bratecode.CODE = guest-pr.CODE NO-LOCK:
      CREATE dynarate-list.
      ASSIGN
        dynarate-list.dynaCode = bratecode.CODE
        ifTask                 = bratecode.char1[5]
      .
      DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
        mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
        mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
        CASE mesToken:
            WHEN "CN" THEN dynarate-list.counter = INTEGER(mesValue).
            WHEN "RT" THEN dynarate-list.rmType  = mesValue.
            WHEN "WD" THEN dynarate-list.w-day   = INTEGER(mesValue).
            WHEN "FR" THEN dynarate-list.fr-room = INTEGER(mesValue).
            WHEN "TR" THEN dynarate-list.to-room = INTEGER(mesValue).
            WHEN "D1" THEN dynarate-list.days1   = INTEGER(mesValue).
            WHEN "D2" THEN dynarate-list.days2   = INTEGER(mesValue).
            WHEN "RC" THEN dynarate-list.rCode   = mesValue.
        END CASE.
      END.
    END.

    /* dynamic rate option = 0, 1 or 2 */
    FIND FIRST htparam WHERE htparam.paramnr = 439 NO-LOCK.
    
    FIND FIRST dynarate-list WHERE dynarate-list.rmtype EQ "*"
        NO-ERROR.
    global-occ = AVAILABLE dynarate-list AND htparam.finteger = 1.
    IF global-occ THEN
    FOR EACH dynarate-list WHERE dynarate-list.rmtype NE "*":
        DELETE dynarate-list.
    END.
    ELSE    
    FOR EACH dynarate-list WHERE dynarate-list.rmtype NE zimkateg.kurzbez:
        DELETE dynarate-list.
    END.

    FOR EACH dynarate-list:
      FOR EACH bratecode WHERE bratecode.CODE = dynarate-list.rcode 
        AND bratecode.zikatnr = i-zikatnr 
        AND bratecode.erwachs = adult
        AND bratecode.kind1   = child
        AND NOT (bratecode.startperiode GT toDate) 
        AND NOT (bratecode.endperiode LT frDate) NO-LOCK,
        FIRST arrangement WHERE arrangement.argtnr = bratecode.argtnr
        NO-LOCK
        BY bratecode.wday BY arrangement.arrangement
        BY bratecode.erwachs BY bratecode.startperiode:
         
/* SY 20/08/2014 */
        /* Malik Serverless 143 : buff-rlist.rateCode -> buff-rlist.ratecode */
        FIND FIRST buff-rlist WHERE buff-rlist.ratecode /* NE bratecode.CODE*/
          EQ guest-pr.CODE
          AND buff-rlist.room-type = bratecode.zikatnr
          AND buff-rlist.argtno = bratecode.argtnr
          AND buff-rlist.adult = bratecode.erwachs
          AND buff-rlist.child = bratecode.kind1
          AND buff-rlist.marknr = bratecode.marknr NO-ERROR.
        do-it =  NOT AVAILABLE buff-rlist.
        
        IF do-it THEN
        DO:
          FIND FIRST rate-list WHERE 
            rate-list.ratecode = guest-pr.CODE /* Malik Serverless 143 : rate-list.rateCode -> rate-list.ratecode */
            AND rate-list.room-type = i-zikatnr
            AND rate-list.argtno = bratecode.argtnr
            AND rate-list.adult = bratecode.erwachs
            AND rate-list.child = bratecode.kind1 NO-ERROR.
          IF NOT AVAILABLE rate-list THEN
          DO:
            
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = bqueasy.number1
                NO-LOCK.
            CREATE rate-list.
            ASSIGN
                i-counter            = i-counter + 1
                rate-list.i-counter  = i-counter
                rate-list.ratecode   = guest-pr.CODE /* Malik Serverless 143 : rate-list.rateCode -> rate-list.ratecode */
                rate-list.dynaflag   = YES
                rate-list.room-type  = i-zikatnr
                rate-list.argtno     = bratecode.argtnr
                rate-list.adult      = bratecode.erwachs
                rate-list.child      = bratecode.kind1
                rate-list.marknr     = bratecode.marknr
                rate-list.currency   = bqueasy.number1
                rate-list.minstay    = bqueasy.number2
                rate-list.maxstay    = bqueasy.deci2
                rate-list.minadvance = bqueasy.number3
                rate-list.maxadvance = bqueasy.deci3
                rate-list.frdate     = bqueasy.date1
                rate-list.todate     = bqueasy.date2
                rate-list.wabkurz    = waehrung.wabkurz
            .
            IF bqueasy.char3 NE "" THEN
            DO:
              FIND FIRST segment WHERE segment.bezeich = bqueasy.char3
                  NO-LOCK NO-ERROR.
              IF AVAILABLE segment THEN rate-list.segmentcode = 
                  STRING(segment.segmentcode) + " " + segment.bezeich.
            END.
            IF bqueasy.date1 NE ? AND bqueasy.date2 NE ?
                AND ((ci-date LT bqueasy.date1) 
                OR (ci-date GT bqueasy.date2)) THEN rate-list.expired = YES.
          END.
        END.
      END.
    END.
    
    IF zimkateg.typ GT 0 THEN
    FOR EACH rate-list:
        FIND FIRST created-list WHERE 
            created-list.rateCode = rate-list.ratecode AND /* Malik Serverless 143 : rate-list.rateCode -> rate-list.ratecode */
            created-list.marknr   = rate-list.marknr   AND
            created-list.rmcateg  = zimkateg.typ       AND
            created-list.argtno   = rate-list.argtno   NO-ERROR.
        IF AVAILABLE created-list THEN
        DO:
          ASSIGN 
              rate-created        = YES
              rate-list.i-counter = - rate-list.i-counter
          .
          DO curr-i = 1 TO 30:
            ASSIGN 
                rate-list.rmRate[curr-i]   = created-list.rmRate[curr-i]
                rate-list.statcode[curr-i] = created-list.statCode[curr-i] /* Malik Serverless 143 : rate-list.statCode -> rate-list.statcode */
            .
          END.
        END.
    END.
    
    IF calc-rm = YES THEN rate-created = NO.

/* calculate the rates if rate-list have no rates yet */
    FIND FIRST rate-list NO-ERROR.
    IF AVAILABLE rate-list AND NOT rate-created THEN
    DO: 
        curr-i = 0.
        DO curr-date = frDate TO toDate:
            curr-i = curr-i + 1.
            ASSIGN w-day = wd-array[WEEKDAY(curr-date)]. 
            RUN calculate-occupied-roomsbl.p(curr-date, zimkateg.kurzbez, 
                global-occ, OUTPUT occ-rooms).
            ASSIGN occ-room-array[curr-i] = occ-rooms.

            
/* 
            DISP frdate curr-date zimkateg.kurzbez occ-rooms.
            FOR EACH dynarate-list:
                DISP dynarate-list.
            END.
            PAUSE.
*/              
            FIND FIRST dynarate-list WHERE dynarate-list.w-day = w-day
                AND dynarate-list.days1 = 0
                AND dynarate-list.days2 = 0
                AND (dynaRate-list.fr-room LE occ-rooms)
                AND (dynaRate-list.to-room GE occ-rooms) NO-ERROR.
            IF NOT AVAILABLE dynarate-list THEN
            FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
                AND dynarate-list.days1 = 0
                AND dynarate-list.days2 = 0
                AND (dynaRate-list.fr-room LE occ-rooms)
                AND (dynaRate-list.to-room GE occ-rooms) NO-ERROR.
            IF AVAILABLE dynarate-list THEN
            DO:
              mapcode = dynaRate-list.rcode.     
              IF NOT global-occ THEN
              FIND FIRST queasy WHERE queasy.KEY  = 145
                AND queasy.char1                = guest-pr.CODE
                AND queasy.char2                = mapcode
                AND queasy.number1              = i-zikatnr
                AND queasy.deci1                = dynarate-list.w-day
                AND queasy.deci2                = dynarate-list.counter
                AND queasy.date1                = curr-date 
                NO-LOCK NO-ERROR.
              ELSE
              FIND FIRST queasy WHERE queasy.KEY  = 145
                AND queasy.char1                = guest-pr.CODE
                AND queasy.char2                = mapcode
                AND queasy.number1              = 0
                AND queasy.deci1                = dynarate-list.w-day
                AND queasy.deci2                = dynarate-list.counter
                AND queasy.date1                = curr-date 
                NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN mapcode = queasy.char3.
              
              
              FOR EACH rate-list WHERE rate-list.dynaflag = YES
                  AND rate-list.ratecode = guest-pr.CODE: /* Malik Serverless 143 : rate-list.rateCode -> rate-list.ratecode */                      
                RUN check-allotment (bqueasy.char1, mapcode,
                    curr-date, OUTPUT rate-found).
                IF rate-found THEN
                RUN ratecode-rate.p(NO, NO, 0, 1, ("!" + mapcode), 
                  ci-date, curr-date, curr-date, curr-date, 
                  rate-list.marknr, rate-list.argtno, i-zikatnr, 
                  rate-list.adult, rate-list.child, 0, 0, 
                  rate-list.currency, OUTPUT rate-found, OUTPUT rm-Rate, 
                  OUTPUT restricted, OUTPUT kback-flag).
                IF rate-found THEN
                ASSIGN 
                    rate-list.rmRate[curr-i] = rm-rate
                    rate-list.statcode[curr-i] = mapcode /* Malik Serverless 143 : rate-list.statCode -> rate-list.statcode */
                .
                ELSE 
                DO:    
                  ASSIGN rate-list.rmRate[curr-i] = -0.001.
                  IF dynarate-list.w-day NE 0 THEN 
                    ASSIGN not-found-flag = YES.
                END.
              END.
            END.
        END.
        curr-i = 0.

        IF not-found-flag THEN
        DO curr-date = frDate TO toDate:
            curr-i = curr-i + 1.
            ASSIGN occ-rooms = occ-room-array[curr-i].
            FIND FIRST dynarate-list WHERE dynarate-list.w-day = 0
                AND dynarate-list.days1 = 0
                AND dynarate-list.days2 = 0
                AND (dynaRate-list.fr-room LE occ-rooms)
                AND (dynaRate-list.to-room GE occ-rooms) NO-ERROR.
            IF AVAILABLE dynarate-list THEN
            DO:
              mapcode = dynaRate-list.rcode.
              IF NOT global-occ THEN
              FIND FIRST queasy WHERE queasy.KEY  = 145
                AND queasy.char1                = guest-pr.CODE
                AND queasy.char2                = mapcode
                AND queasy.number1              = i-zikatnr
                AND queasy.deci1                = 0
                AND queasy.deci2                = dynarate-list.counter
                AND queasy.date1                = curr-date 
                NO-LOCK NO-ERROR.
              ELSE
              FIND FIRST queasy WHERE queasy.KEY  = 145
                AND queasy.char1                = guest-pr.CODE
                AND queasy.char2                = mapcode
                AND queasy.number1              = 0
                AND queasy.deci1                = dynarate-list.w-day
                AND queasy.deci2                = dynarate-list.counter
                AND queasy.date1                = curr-date 
                NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN mapcode = queasy.char3.
              
            
              FOR EACH rate-list WHERE rate-list.dynaflag = YES
                  AND rate-list.ratecode = guest-pr.CODE: /* Malik Serverless 143 : rate-list.rateCode -> rate-list.ratecode */
                IF rate-list.rmRate[curr-i] = 0 THEN
                DO:
                  RUN ratecode-rate.p(NO, NO, 0, 1, ("!" + mapcode), 
                    ci-date, curr-date, curr-date, curr-date, 
                    rate-list.marknr, rate-list.argtno, i-zikatnr, 
                    rate-list.adult, rate-list.child, 0, 0, 
                    rate-list.currency, OUTPUT rate-found, OUTPUT rm-Rate, 
                    OUTPUT restricted, OUTPUT kback-flag).
                  
                  IF rate-found THEN
                  ASSIGN 
                      rate-list.rmRate[curr-i] = rm-rate
                      rate-list.statcode[curr-i] = mapcode /* Malik Serverless 143 : rate-list.statCode -> rate-list.statcode */
                  .
                END.
              END.
            END.
        END.
    END.
  END.
END.

/* 
following is to provide unique early booking rates. for example
there are EB1 and EB2, EB1 advance booking = 7, EB2 14 days
if guest's (ci-date - today) = 20, then EB1 rates will be removed
*/

FOR EACH rate-list WHERE rate-list.minadvance GT 0 
    BY rate-list.minadvance DESCENDING:
    FIND FIRST selected-ratelist WHERE 
/*      selected-ratelist.ratecode = rate-list.rateCode AND  */
        selected-ratelist.marknr   = rate-list.marknr   AND
        selected-ratelist.argtno   = rate-list.argtno   AND
        selected-ratelist.adult    = rate-list.adult    AND
        selected-ratelist.child    = rate-list.child    AND
        selected-ratelist.minstay  = rate-list.minstay  AND
        selected-ratelist.maxstay  = rate-list.maxstay 
        NO-ERROR.
    IF NOT AVAILABLE selected-ratelist THEN
    DO:
        CREATE selected-ratelist.
        ASSIGN
/*          selected-ratelist.ratecode = rate-list.rateCode */
            selected-ratelist.marknr   = rate-list.marknr
            selected-ratelist.argtno   = rate-list.argtno
            selected-ratelist.adult    = rate-list.adult 
            selected-ratelist.child    = rate-list.child 
            selected-ratelist.minstay  = rate-list.minstay
            selected-ratelist.maxstay  = rate-list.maxstay 
        .
    END.

    ELSE DELETE rate-list.

END.

IF zimkateg.typ GT 0 THEN
FOR EACH rate-list WHERE rate-list.dynaflag:

    IF rate-list.i-counter LT 0 THEN 
        rate-list.i-counter = - rate-list.i-counter.
    ELSE
    DO:
        CREATE created-list.
        BUFFER-COPY rate-list TO created-list.
        ASSIGN created-list.rmcateg = zimkateg.typ.
    END.
END.



/********************* DEFINE PROCEDURES **************************/

PROCEDURE check-allotment:
DEF INPUT PARAMETER origcode        AS CHAR     NO-UNDO.
DEF INPUT PARAMETER statcode        AS CHAR     NO-UNDO.
DEF INPUT PARAMETER curr-date       AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER allotment-ok   AS LOGICAL  NO-UNDO INIT YES.

DEF VARIABLE occ-room           AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE allotment          AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE curr-i             AS INTEGER  NO-UNDO.
DEF VARIABLE rline-origcode        AS CHAR     NO-UNDO.
DEF VARIABLE str                AS CHAR     NO-UNDO.
DEF VARIABLE ratecode-found     AS LOGICAL  NO-UNDO INIT NO.
DEF VARIABLE doit-flag          AS LOGICAL  NO-UNDO.
DEF BUFFER zbuff FOR zimkateg.
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = rate-list.room-type
      NO-LOCK.
  IF zimkateg.typ = 0 THEN
  DO:
    FIND FIRST ratecode WHERE ratecode.CODE EQ statcode
      AND ratecode.zikatnr EQ rate-list.room-type
      AND ratecode.argtnr  EQ rate-list.argtno
      AND ratecode.startperiode LE curr-date
      AND ratecode.endperiode GE curr-date
      AND ratecode.num1[1] GT 0 NO-LOCK NO-ERROR.
    ASSIGN ratecode-found = AVAILABLE ratecode.
    IF ratecode-found THEN allotment = ratecode.num1[1].
  END.
  ELSE
  DO:
      FOR EACH ratecode WHERE ratecode.CODE EQ statcode
        AND ratecode.zikatnr EQ rate-list.room-type
        AND ratecode.argtnr  EQ rate-list.argtno
        AND ratecode.startperiode LE curr-date
        AND ratecode.endperiode GE curr-date
        AND ratecode.num1[1] GT 0 NO-LOCK,
        FIRST zbuff WHERE zbuff.zikatnr = ratecode.zikatnr
            AND zbuff.typ = zimkateg.typ NO-LOCK:
        ASSIGN 
            ratecode-found  = YES
            allotment       = ratecode.num1[1].
        .
        LEAVE.
      END.
  END.
  IF NOT (allotment GT 0) THEN RETURN.
  
  FOR EACH res-line WHERE res-line.gastnr = ind-gastno
      AND res-line.active-flag LE 1
      AND res-line.ankunft LE curr-date
      AND res-line.abreise GT curr-date
      AND (res-line.resstatus LE 6 AND res-line.resstatus NE 3
           AND res-line.resstatus NE 4) 
      AND res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") NO-LOCK:
      doit-flag = (res-line.resnr NE inp-resnr) OR
                  (res-line.reslinnr NE inp-reslinnr).
      IF doit-flag = YES AND zimkateg.typ = 0 THEN
      DO:
        IF res-line.zikatnr NE zimkateg.zikatnr
          THEN doit-flag = NO.
      END.
      ELSE
      DO: 
        FIND FIRST zbuff WHERE zbuff.zikatnr = res-line.zikatnr
          NO-LOCK.
        IF zbuff.typ NE zimkateg.typ THEN doit-flag = NO.
      END.
      IF doit-flag THEN
      DO:
        FIND FIRST arrangement WHERE arrangement.arrangement
          = res-line.arrangement NO-LOCK.
        IF arrangement.argtnr NE rate-list.argtno THEN doit-flag = NO.
      END.
      IF doit-flag THEN
      DO curr-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
          str = ENTRY(curr-i, res-line.zimmer-wunsch, ";").
          IF SUBSTR(str,1,10) = "$OrigCode$" THEN 
          DO:
              rline-origcode  = SUBSTR(str,11).
              IF rline-origcode = origcode THEN 
                occ-room = occ-room + res-line.zimmeranz.
              LEAVE.
          END.
      END.
  END.
  IF (occ-room + rooms) GT allotment THEN allotment-ok = NO. /* allotment overbook */
END.
