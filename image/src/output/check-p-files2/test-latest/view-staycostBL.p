DEFINE TEMP-TABLE output-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD STR AS CHAR FORMAT "x(68)" 
  FIELD str1 AS CHAR. 

DEFINE TEMP-TABLE argt-list 
  FIELD argtnr          AS INTEGER INITIAL 0 
  FIELD argt-artnr      AS INTEGER INITIAL 0 
  FIELD departement     AS INTEGER INITIAL 0
  FIELD is-charged      AS INTEGER INITIAL 0
  FIELD period          AS INTEGER INITIAL 0
  FIELD vt-percnt       AS INTEGER INITIAL 0
. 

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER resnr       AS INTEGER. 
DEFINE INPUT  PARAMETER reslinnr    AS INTEGER. 
DEFINE INPUT  PARAMETER contcode    AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE ci-date             AS DATE NO-UNDO. 
DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE wd-array AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 
DEFINE VARIABLE bonus-array         AS LOGICAL EXTENT 999 INITIAL NO. 


{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "view-staycost". 

FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs  AS INTEGER, 
     INPUT kind1    AS INTEGER, 
     INPUT kind2    AS INTEGER). 
  DEF VAR rate AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN 
      rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 

/************** MAIN LOGIC *******************/
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST res-line WHERE res-line.resnr = resnr AND 
  res-line.reslinnr = reslinnr NO-LOCK. 
FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement 
    NO-LOCK.  
FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.

IF AVAILABLE arrangement THEN
    RUN check-bonus.
RUN cal-revenue.

/************** PROCEDURE *******************/

PROCEDURE check-bonus: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE stay AS INTEGER. 
DEFINE VARIABLE pay  AS INTEGER. 
DEFINE VARIABLE num-bonus AS INTEGER INITIAL 0. 

  j = 1. 
  DO i = 1 TO 4: 
    stay = INTEGER(SUBSTR(arrangement.options, j, 2)). 
    pay  = INTEGER(SUBSTR(arrangement.options, j + 2, 2)). 
    IF (stay - pay) GT 0 THEN 
    DO: 
      n = num-bonus + pay  + 1. 
      DO k = n TO stay: 
        bonus-array[k] = YES. 
      END. 
      num-bonus = stay - pay. 
    END. 
     j = j + 4. 
  END. 
END. 

PROCEDURE cal-revenue: 
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE co-date         AS DATE. 
DEFINE VARIABLE argt-rate       AS DECIMAL. 
DEFINE VARIABLE argt-rate2      AS DECIMAL. 
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE daily-rate      AS DECIMAL. 
DEFINE VARIABLE tot-rate        AS DECIMAL INITIAL 0. 
DEFINE VARIABLE add-it          AS LOGICAL. 
DEFINE VARIABLE c               AS CHAR. 
DEFINE VARIABLE fixed-rate      AS LOGICAL INITIAL NO. 
DEFINE VARIABLE argt-defined    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE delta           AS INTEGER. 
DEFINE VARIABLE start-date      AS DATE. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE pax             AS INTEGER              NO-UNDO. 
DEFINE VARIABLE child1          AS INTEGER              NO-UNDO. 
DEFINE VARIABLE n               AS INTEGER              NO-UNDO.
DEFINE VARIABLE created-date    AS DATE                 NO-UNDO.
DEFINE VARIABLE bill-date       AS DATE                 NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER              NO-UNDO. 
DEFINE VARIABLE curr-i          AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE w-day           AS INTEGER              NO-UNDO. 
DEFINE VARIABLE rack-rate       AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE ratecode-qsy    AS CHAR                 NO-UNDO. /* Add by Michael @ 18/09/2018 for Archipelago International request - ticket no FF7A71 */
DEFINE VARIABLE count-break     AS DECIMAL              NO-UNDO.
DEFINE VARIABLE fixcost-rate    AS DECIMAL              NO-UNDO.
DEFINE VARIABLE tmpInt          AS INTEGER              NO-UNDO.
DEFINE VARIABLE tmpDate         AS DATE                 NO-UNDO.

DEFINE BUFFER w1 FOR waehrung. 
  
  n = 0.
  IF res-line.zimmer-wunsch MATCHES ("*DATE,*") THEN
  n = INDEX(res-line.zimmer-wunsch,"Date,").
  IF n > 0 THEN
  DO:
    c = SUBSTR(res-line.zimmer-wunsch, n + 5, 8).
    created-date = DATE(INTEGER(SUBSTR(c,5,2)), INTEGER(SUBSTR(c,7,2)),
      INTEGER(SUBSTR(c,1,4))).
  END.
  ELSE created-date = reservation.resdat.

  ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*").
  kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").
  IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
  ELSE curr-zikatnr = res-line.zikatnr. 
 
  /* IF res-line.was-status = 1 THEN fixed-rate = yes.  */ 
  IF res-line.abreise GT res-line.ankunft THEN co-date = res-line.abreise - 1. 
  ELSE co-date = res-line.abreise. 
  rm-rate = res-line.zipreis. 
 
  DO datum = res-line.ankunft TO co-date: 
    curr-i = curr-i + 1. 
    bill-date = datum. 
    argt-rate = 0. 
    daily-rate = 0. 
    fixcost-rate = 0.
    pax = res-line.erwachs. 
    fixed-rate = NO. 
    ratecode-qsy = "Undefined". /* Add by Michael @ 18/09/2018 for Archipelago International request - ticket no FF7A71 */
    argt-rate2 = 0. 

    IF datum LT ci-date THEN
    DO:
      rm-rate = ?.
      FIND FIRST genstat WHERE genstat.datum = datum
          AND genstat.resnr = res-line.resnr
          AND genstat.res-int[1] = res-line.reslinnr NO-LOCK NO-ERROR.
      IF AVAILABLE genstat THEN 
      DO:    
        rm-rate = genstat.zipreis.
        pax = genstat.erwachs. /*FDL Nov 27, 2023 => Ticket BB5B5C*/

        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = genstat.resnr
            AND reslin-queasy.reslinnr = genstat.res-int[1]
            AND datum GE reslin-queasy.date1 
            AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO: 
            IF reslin-queasy.char2 NE "" THEN ratecode-qsy = reslin-queasy.char2. 
            ELSE ratecode-qsy = "Undefined".
        END.

        FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt
            NO-LOCK NO-ERROR.
      END.      
    END.
    
    IF datum GE ci-date OR NOT AVAILABLE arrangement THEN
    FIND FIRST arrangement WHERE arrangement.arrangement 
      = res-line.arrangement NO-LOCK.  

    IF (datum GE ci-date) OR rm-rate = ? THEN
    DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        /*AND datum GE reslin-queasy.date1 
        AND datum LE reslin-queasy.date2 FT serverless*/
        AND reslin-queasy.date1 LE datum
        AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        fixed-rate = YES. 
        rm-rate = reslin-queasy.deci1.
        /* Add by Michael @ 18/09/2018 for Archipelago International request - ticket no FF7A71 */
        IF reslin-queasy.char2 NE "" THEN ratecode-qsy = reslin-queasy.char2. 
        ELSE ratecode-qsy = "Undefined".
        /* End of add */
        IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
        IF reslin-queasy.char1 NE "" THEN 
        FIND FIRST arrangement WHERE arrangement.arrangement 
          = reslin-queasy.char1 NO-LOCK.  
          /*RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
      END. 

      IF NOT fixed-rate THEN 
      DO: 
        /*RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
        IF NOT it-exist THEN 
        DO: 
          IF AVAILABLE guest-pr THEN 
          DO: 
            FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
              = res-line.reserve-int NO-LOCK NO-ERROR. 
            IF AVAILABLE queasy AND queasy.logi3 THEN 
               bill-date = res-line.ankunft. 

            IF new-contrate THEN 
            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
              res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
              res-line.abreise, res-line.reserve-int, arrangement.argtnr,
              curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
              res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
            ELSE
            DO:
              RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                res-line.erwachs, res-line.kind1, res-line.kind2,
                res-line.reserve-dec, res-line.betriebsnr, 
                OUTPUT rm-rate, OUTPUT rate-found).
                /*RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist).*/
              IF it-exist THEN rate-found = YES.
              IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
            END.  /* old contract rate  */
          END.    /* available guest-pr */

          IF NOT rate-found THEN
          DO: 
            w-day = wd-array[WEEKDAY(bill-date)]. 
            IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
            DO: 
              rm-rate = res-line.zipreis. 
              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                AND katpreis.argtnr = arrangement.argtnr 
                AND katpreis.startperiode LE bill-date 
                AND katpreis.endperiode GE bill-date 
                AND katpreis.betriebsnr = w-day 
                NO-LOCK NO-ERROR. 
              IF NOT AVAILABLE katpreis THEN 
              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                AND katpreis.argtnr = arrangement.argtnr 
                AND katpreis.startperiode LE bill-date 
                AND katpreis.endperiode GE bill-date 
                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                res-line.kind1, res-line.kind2) = rm-rate 
              THEN rack-rate = YES. 
            END. 
            ELSE IF rack-rate THEN 
            DO: 
              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                AND katpreis.argtnr = arrangement.argtnr 
                AND katpreis.startperiode LE bill-date 
                AND katpreis.endperiode GE bill-date 
                AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
              IF NOT AVAILABLE katpreis THEN 
              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                AND katpreis.argtnr = arrangement.argtnr 
                AND katpreis.startperiode LE bill-date 
                AND katpreis.endperiode GE bill-date 
                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                res-line.kind1, res-line.kind2) > 0 
              THEN 
                rm-rate = get-rackrate(res-line.erwachs, 
                  res-line.kind1, res-line.kind2). 
            END. /* if rack-rate   */ 
            IF bonus-array[curr-i] = YES THEN rm-rate = 0.  
          END.   /* publish rate   */  
        END.     /* not exist      */ 
      END.       /* not fixed rate */
    END.         /* datum GE ci-date OR rm-rate = ? */

    CREATE output-list. 
    STR = STRING(datum) + "   " + translateExtended ("Roomrate",lvCAREA,"") 
      + "   = " + TRIM(STRING(rm-rate,"->>>,>>>,>>9.99")) + " - " + TRIM(ratecode-qsy). 
    tot-rate = tot-rate + rm-rate. 
    daily-rate = rm-rate. 
 
    ASSIGN count-break = 0.
/** argt-line prices **/ 
    IF rm-rate NE 0 THEN 
    FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
      /* AND argt-line.kind1 */ AND NOT argt-line.kind2: 
      add-it = NO.       
      IF argt-line.vt-percnt = 0 THEN 
      DO: 
        IF argt-line.betriebsnr = 0 THEN qty = pax. 
        ELSE qty = argt-line.betriebsnr. 
      END. 
      ELSE IF argt-line.vt-percnt = 1 THEN qty = res-line.kind1. 
      ELSE IF argt-line.vt-percnt = 2 THEN qty = res-line.kind2.       

      IF qty GT 0 THEN 
      DO: 
        IF argt-line.fakt-modus = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 2 THEN 
        DO: 
          IF res-line.ankunft EQ datum THEN add-it = YES. 
        END. 
        ELSE IF argt-line.fakt-modus = 3 THEN 
        DO: 
          IF (res-line.ankunft + 1) EQ datum THEN add-it = YES. 
        END. 
        ELSE IF argt-line.fakt-modus = 4 AND day(datum) = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 5 
          AND day(datum + 1) = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 6 THEN 
        DO: 
          /* Dzikri 3DC423 - Repair Arrangemnt type 6 
            IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE datum 
              THEN add-it = YES. */
            FIND FIRST argt-list WHERE argt-list.argtnr EQ argt-line.argtnr 
              AND argt-list.departement EQ argt-line.departement 
              AND argt-list.argt-artnr  EQ argt-line.argt-artnr 
              AND argt-list.vt-percnt   EQ argt-line.vt-percnt
              AND argt-list.is-charged  EQ 0  NO-LOCK NO-ERROR.
            IF NOT AVAILABLE argt-list THEN
            DO:
              CREATE argt-list.
              ASSIGN
                argt-list.argtnr      = argt-line.argtnr 
                argt-list.departement = argt-line.departement 
                argt-list.argt-artnr  = argt-line.argt-artnr 
                argt-list.vt-percnt   = argt-line.vt-percnt
                argt-list.is-charged  = 0
                argt-list.period      = 0
              .
            END.
            IF argt-list.period LT argt-line.intervall THEN
            DO:
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                AND reslin-queasy.char1    = "" 
                AND reslin-queasy.number1  = argt-line.departement 
                AND reslin-queasy.number2  = argt-line.argtnr 
                AND reslin-queasy.resnr    = res-line.resnr 
                AND reslin-queasy.reslinnr = res-line.reslinnr 
                AND reslin-queasy.number3  = argt-line.argt-artnr 
                AND reslin-queasy.date1 LE res-line.abreise
                AND reslin-queasy.date2 GE res-line.ankunft  NO-LOCK NO-ERROR. 
              IF AVAILABLE reslin-queasy THEN
              DO:
                IF reslin-queasy.date1 LE datum
                  AND reslin-queasy.date2 GE datum
                  AND (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE datum THEN
                DO:
                  add-it = YES.
                  argt-list.period = argt-list.period + 1.
                END.
                ELSE
                DO:
                  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                    AND reslin-queasy.char1    = "" 
                    AND reslin-queasy.number1  = argt-line.departement 
                    AND reslin-queasy.number2  = argt-line.argtnr 
                    AND reslin-queasy.resnr    = res-line.resnr 
                    AND reslin-queasy.reslinnr = res-line.reslinnr 
                    AND reslin-queasy.number3  = argt-line.argt-artnr 
                    AND reslin-queasy.date1 LE datum 
                    AND reslin-queasy.date2 GE datum
                    AND (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE datum NO-LOCK NO-ERROR.
                  IF AVAILABLE reslin-queasy THEN
                  DO:
                    add-it = YES.
                    argt-list.period = argt-list.period + 1.
                  END.
                END.
              END.
              ELSE
              DO:
                IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE datum THEN
                DO:
                  add-it = YES.
                  argt-list.period = argt-list.period + 1.
                END.
              END.
            END.
          /* Dzikri 3DC423 - END */
        END. 
      END. 
                 
      IF add-it THEN 
      DO:                 
        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
          AND artikel.departement = argt-line.departement NO-LOCK.         

        ASSIGN
            argt-rate    = 0
            argt-rate2   = argt-line.betrag 
            argt-defined = NO.                 

        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
          AND reslin-queasy.char1    = "" 
          AND reslin-queasy.number1  = argt-line.departement 
          AND reslin-queasy.number2  = argt-line.argtnr 
          AND reslin-queasy.resnr    = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND reslin-queasy.number3  = argt-line.argt-artnr 
          /*AND bill-date GE reslin-queasy.date1 
          AND bill-date LE reslin-queasy.date2 FT serverless*/ 
          AND reslin-queasy.date1 LE bill-date
          AND reslin-queasy.date2 GE bill-date NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:         
            FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
              AND reslin-queasy.char1    = "" 
              AND reslin-queasy.number1  = argt-line.departement 
              AND reslin-queasy.number2  = argt-line.argtnr 
              AND reslin-queasy.resnr    = res-line.resnr 
              AND reslin-queasy.reslinnr = res-line.reslinnr 
              AND reslin-queasy.number3  = argt-line.argt-artnr 
              AND reslin-queasy.date1 LE bill-date
              AND reslin-queasy.date2 GE bill-date NO-LOCK:
                argt-defined = YES. 
                /* Dzikri C5ABD0 - IN% DISCOUNT */
                IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                DO:
                  FIND FIRST zwkum WHERE zwkum.zknr EQ artikel.zwkum 
                    AND zwkum.departement EQ artikel.departement
                    AND zwkum.bezeich MATCHES "*DISCOUNT*" NO-LOCK NO-ERROR.
                  IF AVAILABLE zwkum THEN argt-rate = rm-rate * INT(reslin-queasy.char2) / 100 * (-1). 
                  ELSE argt-rate = rm-rate * INT(reslin-queasy.char2) / 100.
                END.
                ELSE
                DO:
                    /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                    ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                    ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3.                  */

                    IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                    ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                    ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                END.    
                
                /*ITA 29/10/18 --> jika yang diisi in%
                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.*/
                  
                argt-rate = argt-rate * qty.
                /* Dzikri C5ABD0 - END */ 
        
                IF argt-rate NE 0 THEN
                DO:
                  CREATE output-list. 
                  output-list.flag = 1. 
                  c = STRING(qty) + " " + artikel.bezeich. 
                  STR = STRING(translateExtended ("     Incl.",lvCAREA,""),"x(10)") 
                    + " " + STRING(c, "x(16)") 
                    + " = " + TRIM(STRING(argt-rate,"->>>,>>>,>>9.99")).
                  count-break = count-break + argt-rate.
                END.
            END.                  
        END. 

        IF AVAILABLE guest-pr AND NOT argt-defined THEN 
        DO: 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
            AND reslin-queasy.char1 = contcode 
            AND reslin-queasy.number1 = res-line.reserve-int 
            AND reslin-queasy.number2 = arrangement.argtnr 
            AND reslin-queasy.reslinnr = res-line.zikatnr 
            AND reslin-queasy.number3 = argt-line.argt-artnr 
            AND reslin-queasy.resnr = argt-line.departement 
            AND reslin-queasy.date1 LE bill-date
            AND reslin-queasy.date2 GE bill-date NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy THEN 
          DO:              
            FOR EACH reslin-queasy WHERE reslin-queasy.key = "argt-line" 
                AND reslin-queasy.char1 = contcode 
                AND reslin-queasy.number1 = res-line.reserve-int 
                AND reslin-queasy.number2 = arrangement.argtnr 
                AND reslin-queasy.reslinnr = res-line.zikatnr 
                AND reslin-queasy.number3 = argt-line.argt-artnr 
                AND reslin-queasy.resnr = argt-line.departement 
                AND reslin-queasy.date1 LE bill-date
                AND reslin-queasy.date2 GE bill-date NO-LOCK:

                argt-defined = YES.
                /* Dzikri C5ABD0 - IN% DISCOUNT */
                IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                DO:
                  FIND FIRST zwkum WHERE zwkum.zknr EQ artikel.zwkum 
                    AND zwkum.departement EQ artikel.departement
                    AND zwkum.bezeich MATCHES "*DISCOUNT*" NO-LOCK NO-ERROR.
                  IF AVAILABLE zwkum THEN argt-rate = rm-rate * INT(reslin-queasy.char2) / 100 * (-1). 
                  ELSE argt-rate = rm-rate * INT(reslin-queasy.char2) / 100.
                END.
                ELSE
                DO:
                    IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                    ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                    ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                END.    

                /*ITA 29/10/18 --> jika yang diisi in%
                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty.  
                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.*/
                  
                argt-rate = argt-rate * qty.
                /* Dzikri C5ABD0 - END */
        
                IF argt-rate NE 0 THEN
                DO:
                  CREATE output-list. 
                  output-list.flag = 1. 
                  c = STRING(qty) + " " + artikel.bezeich. 
                  STR = STRING(translateExtended ("     Incl.",lvCAREA,""),"x(10)") 
                    + " " + STRING(c, "x(16)") 
                    + " = " + TRIM(STRING(argt-rate,"->>>,>>>,>>9.99")).
                  count-break = count-break + argt-rate.
                END.
            END.
          END. 
        END. 
                
        /*ITA 29/10/18 --> jika yang diisi in%*/
        IF argt-rate2 GT 0 THEN argt-rate2 = argt-rate2 * qty. 
        /* Dzikri C5ABD0 - IN% DISCOUNT */
        /*ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.*/
        ELSE 
        DO:
          FIND FIRST zwkum WHERE zwkum.zknr EQ artikel.zwkum 
            AND zwkum.departement EQ artikel.departement
            AND zwkum.bezeich MATCHES "*DISCOUNT*" NO-LOCK NO-ERROR.
          IF AVAILABLE zwkum THEN argt-rate2 = (rm-rate * (argt-rate2 / 100)) * qty.
          ELSE argt-rate2 = (rm-rate * (- argt-rate2 / 100)) * qty.
        END.
        /* Dzikri C5ABD0 - END */
        /*argt-rate = argt-rate * qty.*/

        /* FDL Comment 
        IF argt-rate2 NE 0 AND argt-rate = 0 THEN*/
        IF argt-rate = 0 THEN   /*FDL April 24, 2024 => Ticket 87E884*/
        DO:
          CREATE output-list. 
          output-list.flag = 1. 
          c = STRING(qty) + " " + artikel.bezeich. 
          STR = STRING(translateExtended ("     Incl.",lvCAREA,""),"x(10)") 
            + " " + STRING(c, "x(16)") 
            + " = " + TRIM(STRING(argt-rate2,"->>>,>>>,>>9.99")).
          count-break = count-break + argt-rate2.
        END.
      END. /* IF addi-it */ 
    END.   /* each argt-line */ 
    
/**** additional fix cost from arrangement ******/ 
    /* Dzikri 796D85 - arrangment fixed cost appear in expected room revenue */
    FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
      /* AND argt-line.kind1 */ AND argt-line.kind2: 
      add-it = NO. 
      IF argt-line.vt-percnt = 0 THEN 
      DO: 
        IF argt-line.betriebsnr = 0 THEN qty = pax. 
        ELSE qty = argt-line.betriebsnr. 
      END. 
      ELSE IF argt-line.vt-percnt = 1 THEN qty = res-line.kind1. 
      ELSE IF argt-line.vt-percnt = 2 THEN qty = res-line.kind2.       

      IF qty GT 0 THEN 
      DO: 
        IF argt-line.fakt-modus = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 2 THEN 
        DO: 
          IF res-line.ankunft EQ datum THEN add-it = YES. 
        END. 
        ELSE IF argt-line.fakt-modus = 3 THEN 
        DO: 
          IF (res-line.ankunft + 1) EQ datum THEN add-it = YES. 
        END. 
        ELSE IF argt-line.fakt-modus = 4 AND day(datum) = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 5 
          AND day(datum + 1) = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 6 THEN 
        DO: 
          /* Dzikri 3DC423 - Repair Arrangemnt type 6
            IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE datum 
              THEN add-it = YES. */
            FIND FIRST argt-list WHERE argt-list.argtnr EQ argt-line.argtnr 
              AND argt-list.departement EQ argt-line.departement 
              AND argt-list.argt-artnr  EQ argt-line.argt-artnr 
              AND argt-list.vt-percnt   EQ argt-line.vt-percnt
              AND argt-list.is-charged  EQ 1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE argt-list THEN
            DO:
              CREATE argt-list.
              ASSIGN
                argt-list.argtnr      = argt-line.argtnr 
                argt-list.departement = argt-line.departement 
                argt-list.argt-artnr  = argt-line.argt-artnr 
                argt-list.vt-percnt   = argt-line.vt-percnt
                argt-list.is-charged  = 1
                argt-list.period      = 0
              .
            END.
            IF argt-list.period LT argt-line.intervall THEN
            DO:
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                AND reslin-queasy.char1    = "" 
                AND reslin-queasy.number1  = argt-line.departement 
                AND reslin-queasy.number2  = argt-line.argtnr 
                AND reslin-queasy.resnr    = res-line.resnr 
                AND reslin-queasy.reslinnr = res-line.reslinnr 
                AND reslin-queasy.number3  = argt-line.argt-artnr 
                AND reslin-queasy.date1 LE res-line.abreise
                AND reslin-queasy.date2 GE res-line.ankunft  NO-LOCK NO-ERROR. 
              IF AVAILABLE reslin-queasy THEN 
              DO:
                IF reslin-queasy.date1 LE bill-date 
                  AND reslin-queasy.date2 GE bill-date
                  AND (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE bill-date THEN
                DO:
                  add-it = YES.
                  argt-list.period = argt-list.period + 1.
                END.
                ELSE
                DO:
                  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                    AND reslin-queasy.char1    = "" 
                    AND reslin-queasy.number1  = argt-line.departement 
                    AND reslin-queasy.number2  = argt-line.argtnr 
                    AND reslin-queasy.resnr    = res-line.resnr 
                    AND reslin-queasy.reslinnr = res-line.reslinnr 
                    AND reslin-queasy.number3  = argt-line.argt-artnr 
                    AND reslin-queasy.date1 LE bill-date 
                    AND reslin-queasy.date2 GE bill-date
                    AND (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE bill-date NO-LOCK NO-ERROR.
                  IF AVAILABLE reslin-queasy THEN
                  DO:
                    add-it = YES.
                    argt-list.period = argt-list.period + 1.
                  END.
                END.
              END.
              ELSE
              DO:
                IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE bill-date THEN
                DO:
                  add-it = YES.
                  argt-list.period = argt-list.period + 1.
                END.
              END.
            END.
            
          /* Dzikri 3DC423 - END */
        END. 
      END. 
                 
      IF add-it THEN 
      DO:                 
        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
          AND artikel.departement = argt-line.departement NO-LOCK.         

        /* Dzikri 796D85 - selecting f-argt if exist*/
        ASSIGN
            argt-rate    = 0
            argt-rate2   = argt-line.betrag 
            argt-defined = NO.                 

        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
          AND reslin-queasy.char1    = "" 
          AND reslin-queasy.number1  = argt-line.departement 
          AND reslin-queasy.number2  = argt-line.argtnr 
          AND reslin-queasy.resnr    = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND reslin-queasy.number3  = argt-line.argt-artnr 
          AND bill-date GE reslin-queasy.date1 
          AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:         
            FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
              AND reslin-queasy.char1    = "" 
              AND reslin-queasy.number1  = argt-line.departement 
              AND reslin-queasy.number2  = argt-line.argtnr 
              AND reslin-queasy.resnr    = res-line.resnr 
              AND reslin-queasy.reslinnr = res-line.reslinnr 
              AND reslin-queasy.number3  = argt-line.argt-artnr 
              AND bill-date GE reslin-queasy.date1 
              AND bill-date LE reslin-queasy.date2 NO-LOCK:
                argt-defined = YES. 
                /* Dzikri C5ABD0 - IN% DISCOUNT */
                IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                DO:
                  FIND FIRST zwkum WHERE zwkum.zknr EQ artikel.zwkum 
                    AND zwkum.departement EQ artikel.departement
                    AND zwkum.bezeich MATCHES "*DISCOUNT*" NO-LOCK NO-ERROR.
                  IF AVAILABLE zwkum THEN argt-rate = rm-rate * INT(reslin-queasy.char2) / 100 * (-1). 
                  ELSE argt-rate = rm-rate * INT(reslin-queasy.char2) / 100.
                END.
                ELSE
                DO:
                    /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                    ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                    ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3.                  */

                    IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                    ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                    ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                END.
                
                /*ITA 29/10/18 --> jika yang diisi in%
                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.*/
                  
                argt-rate = argt-rate * qty.          
                /* Dzikri C5ABD0 - END */ /* Dzikri 796D85 - END*/
                IF argt-rate NE 0 THEN
                DO:
                  create output-list. 
                  STR = STRING("","x(5)") + "Excl. " + STRING(artikel.bezeich, "x(16)") 
                    + " = " + TRIM(STRING(argt-rate,"->>>,>>>,>>9.99")). 
                  tot-rate     = tot-rate + argt-rate. 
                  fixcost-rate = fixcost-rate + argt-rate.
                END.
            END.                  
        END. 

        IF AVAILABLE guest-pr AND NOT argt-defined THEN 
        DO: 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
            AND reslin-queasy.char1 = contcode 
            AND reslin-queasy.number1 = res-line.reserve-int 
            AND reslin-queasy.number2 = arrangement.argtnr 
            AND reslin-queasy.reslinnr = res-line.zikatnr 
            AND reslin-queasy.number3 = argt-line.argt-artnr 
            AND reslin-queasy.resnr = argt-line.departement 
            AND bill-date GE reslin-queasy.date1 
            AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy THEN 
          DO:              
            FOR EACH reslin-queasy WHERE reslin-queasy.key = "argt-line" 
                AND reslin-queasy.char1 = contcode 
                AND reslin-queasy.number1 = res-line.reserve-int 
                AND reslin-queasy.number2 = arrangement.argtnr 
                AND reslin-queasy.reslinnr = res-line.zikatnr 
                AND reslin-queasy.number3 = argt-line.argt-artnr 
                AND reslin-queasy.resnr = argt-line.departement 
                AND bill-date GE reslin-queasy.date1 
                AND bill-date LE reslin-queasy.date2 NO-LOCK:

                argt-defined = YES. 
                /* Dzikri C5ABD0 - IN% DISCOUNT */
                IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                DO:
                  FIND FIRST zwkum WHERE zwkum.zknr EQ artikel.zwkum 
                    AND zwkum.departement EQ artikel.departement
                    AND zwkum.bezeich MATCHES "*DISCOUNT*" NO-LOCK NO-ERROR.
                  IF AVAILABLE zwkum THEN argt-rate = rm-rate * INT(reslin-queasy.char2) / 100 * (-1). 
                  ELSE argt-rate = rm-rate * INT(reslin-queasy.char2) / 100.
                END.
                ELSE
                DO:
                    /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                    ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                    ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3.                  */

                    IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                    ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                    ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                END.
                /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3. */

                /*ITA 29/10/18 --> jika yang diisi in%
                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.*/
                  
                argt-rate = argt-rate * qty.
                /* Dzikri C5ABD0 - END */
        
                IF argt-rate NE 0 THEN
                DO:
                  create output-list. 
                  STR = STRING("","x(5)") + "Excl. " + STRING(artikel.bezeich, "x(16)") 
                    + " = " + TRIM(STRING(argt-rate,"->>>,>>>,>>9.99")). 
                  tot-rate     = tot-rate + argt-rate. 
                  fixcost-rate = fixcost-rate + argt-rate.
                END.
            END.
          END. 
        END. 
                
        /*ITA 29/10/18 --> jika yang diisi in%*/
        IF argt-rate2 GT 0 THEN argt-rate2 = argt-rate2 * qty. 
        /* Dzikri C5ABD0 - IN% DISCOUNT */
        /*ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.*/
        ELSE 
        DO:
          FIND FIRST zwkum WHERE zwkum.zknr EQ artikel.zwkum 
            AND zwkum.departement EQ artikel.departement
            AND zwkum.bezeich MATCHES "*DISCOUNT*" NO-LOCK NO-ERROR.
          IF AVAILABLE zwkum THEN argt-rate2 = (rm-rate * (argt-rate2 / 100)) * qty.
          ELSE argt-rate2 = (rm-rate * (- argt-rate2 / 100)) * qty.
        END.
        /* Dzikri C5ABD0 - END */
        /*argt-rate = argt-rate * qty.*/

        /* FDL Comment 
        IF argt-rate2 NE 0 AND argt-rate = 0 THEN*/
        IF argt-rate = 0 THEN
        DO: 
          create output-list. 
          STR = STRING("","x(5)") + "Excl. " + STRING(artikel.bezeich, "x(16)") 
            + " = " + TRIM(STRING(argt-rate2,"->>>,>>>,>>9.99")). 
          tot-rate     = tot-rate + argt-rate2. 
          fixcost-rate = fixcost-rate + argt-rate2.
          /*daily-rate = daily-rate + argt-rate. */
        END.
      END. /* IF add-it */ 
    END.   /* each argt-line */ 
    /* Dzikri 796D85 - END */
/**** additional fix cost ******/ 
    FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
        AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
      add-it = NO. 
      argt-rate = 0. 
      IF fixleist.sequenz = 1 THEN add-it = YES. 
      ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
      DO: 
        IF res-line.ankunft EQ datum THEN add-it = YES. 
      END. 
      ELSE IF fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
      ELSE IF fixleist.sequenz = 5 
        AND day(datum + 1) = 1 THEN add-it = YES. 
      ELSE IF fixleist.sequenz = 6 THEN 
      DO: 
        IF lfakt = ? THEN delta = 0. 
        ELSE 
        DO: 
          delta = lfakt - res-line.ankunft. 
          IF delta LT 0 THEN delta = 0. 
        END. 
        start-date = res-line.ankunft + delta. 
        tmpInt = res-line.abreise - start-date.
        IF tmpInt LT fixleist.dekade THEN start-date = res-line.ankunft.
        tmpInt = fixleist.dekade - 1.
        tmpDate = start-date + tmpInt.
        IF datum LE tmpDate THEN add-it = YES. 
        IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
      END. 
      IF add-it THEN 
      DO: 
        FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
          AND artikel.departement = fixleist.departement NO-LOCK. 
        argt-rate = fixleist.betrag * fixleist.number. 
/*
        IF NOT fixed-rate AND AVAILABLE guest-pr THEN 
        DO: 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
            AND reslin-queasy.char1 = contcode 
            AND reslin-queasy.number1 = res-line.reserve-int
            AND reslin-queasy.number2 = arrangement.argtnr 
            AND reslin-queasy.reslinnr = res-line.zikatnr 
            AND reslin-queasy.number3 = fixleist.artnr 
            AND reslin-queasy.resnr = fixleist.departement 
            AND bill-date GE reslin-queasy.date1 
            AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy THEN 
            argt-rate = reslin-queasy.deci1 * fixleist.number. 
        END. 
*/      
      END. 
      IF argt-rate NE 0 THEN 
      DO: 
        create output-list. 
        STR = STRING("","x(8)") + "   " + STRING(artikel.bezeich, "x(16)") 
          + " = " + TRIM(STRING(argt-rate,"->>>,>>>,>>9.99")). 
        tot-rate     = tot-rate + argt-rate. 
        fixcost-rate = fixcost-rate + argt-rate.
        /*daily-rate = daily-rate + argt-rate. */
      END.       
    END.

    IF count-break NE 0 THEN
    DO:
          CREATE output-list. 
          output-list.flag = 2. 
          STR = STRING(translateExtended ("    Lodging",lvCAREA,""),"x(11)") 
                + "                 = " + TRIM(STRING(daily-rate - count-break,"->>>,>>>,>>9.99")).
    END.

    STR = STR + "  Total = " + TRIM(STRING(daily-rate + fixcost-rate,"->>>,>>>,>>9.99")).
  END. 

  CREATE output-list. 
  ASSIGN 
    STR = "  " + translateExtended ("Expected total revenue    =",lvCAREA,"") 
      + " " + TRIM(STRING(tot-rate,"->,>>>,>>>,>>9.99")) 
    str1 = "expected".

  /*MTOPEN QUERY q1 FOR EACH output-list NO-LOCK.*/
END. 
/*
PROCEDURE usr-prog1: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog" 
    AND reslin-queasy.number1 = resnr 
    AND reslin-queasy.number2 = 0 AND reslin-queasy.char1 = "" 
    AND reslin-queasy.reslinnr = 1 USE-INDEX argt_ix NO-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy THEN prog-str = reslin-queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    /*MT
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, resnr, reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
    */
  END. 
END. 
 
PROCEDURE usr-prog2: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST queasy WHERE queasy.key = 2 
    AND queasy.char1 = contcode NO-LOCK NO-ERROR. 
  IF AVAILABLE queasy THEN prog-str = queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    /*MT
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, resnr, reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
    */
  END. 
END. 
*/
