/*FDL Sept 18, 2023 => Ticket D482D0 - Expected Revenue With Same Reservation [API]*/

DEFINE TEMP-TABLE output-list   
    FIELD flag              AS INTEGER INITIAL -1  
    FIELD datum             AS DATE
    FIELD rmtype-no         AS INTEGER
    FIELD article-no        AS INTEGER
    FIELD dept-no           AS INTEGER INITIAL -1
    FIELD str-rmtype        AS CHARACTER
    FIELD str-desc          AS CHARACTER
    FIELD str-amount        AS CHARACTER
    FIELD str1              AS CHARACTER
    FIELD calc-rmrate       AS DECIMAL
    FIELD calc-argtrate     AS DECIMAL
    FIELD calc-argtrate2    AS DECIMAL
    FIELD calc-argtrate-all AS DECIMAL
    FIELD calc-qty          AS DECIMAL
    FIELD calc-fixcost      AS DECIMAL
    FIELD calc-lodg         AS DECIMAL
    FIELD calc-totrev       AS DECIMAL
    FIELD count-break       AS DECIMAL
.  

DEFINE TEMP-TABLE expectedrev-list   
    FIELD flag              AS INTEGER INITIAL -1  
    FIELD datum             AS DATE
    FIELD rmtype-no         AS INTEGER
    FIELD article-no        AS INTEGER
    FIELD dept-no           AS INTEGER INITIAL -1
    FIELD str-rmtype        AS CHARACTER
    FIELD str-desc          AS CHARACTER
    FIELD str-amount        AS CHARACTER
    FIELD str1              AS CHARACTER
    FIELD calc-rmrate       AS DECIMAL
    FIELD calc-argtrate     AS DECIMAL
    FIELD calc-argtrate2    AS DECIMAL
    FIELD calc-argtrate-all AS DECIMAL
    FIELD calc-qty          AS DECIMAL
    FIELD calc-fixcost      AS DECIMAL
    FIELD calc-lodg         AS DECIMAL
    FIELD calc-totrev       AS DECIMAL
    FIELD count-break       AS DECIMAL
.  
  
DEFINE TEMP-TABLE t-res-line  
    FIELD resnr         LIKE res-line.resnr
    FIELD reslinnr      LIKE res-line.reslinnr
    FIELD name          LIKE res-line.name  
    FIELD zinr          LIKE res-line.zinr  
    FIELD ankunft       LIKE res-line.ankunft  
    FIELD abreise       LIKE res-line.abreise
    FIELD contcode      AS CHARACTER
    FIELD str-argt      AS CHARACTER
    FIELD ct-code       AS CHARACTER
    FIELD kurzbez       AS CHARACTER
    FIELD curr-rmcat    AS CHARACTER
    FIELD rmcat-bez     AS CHARACTER
    FIELD bonus-array   AS LOGICAL EXTENT 9999
    FIELD curr-date     AS DATE
    FIELD rmcat-no      AS INTEGER
.  

DEFINE TEMP-TABLE argt-list 
    FIELD argtnr          AS INTEGER INITIAL 0 
    FIELD argt-artnr      AS INTEGER INITIAL 0 
    FIELD resnr           AS INTEGER INITIAL 0 
    FIELD reslinnr        AS INTEGER INITIAL 0 
    FIELD departement     AS INTEGER INITIAL 0
    FIELD is-charged      AS INTEGER INITIAL 0
    FIELD period          AS INTEGER INITIAL 0
    FIELD vt-percnt       AS INTEGER INITIAL 0
. 

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER resno            AS INTEGER.   
DEFINE OUTPUT PARAMETER ci-date         AS DATE.    
DEFINE OUTPUT PARAMETER title-str       AS CHAR.   
DEFINE OUTPUT PARAMETER TABLE FOR t-res-line.  
DEFINE OUTPUT PARAMETER TABLE FOR expectedrev-list.  
/* Local Test
DEFINE VARIABLE pvILanguage     AS INTEGER  NO-UNDO INIT 1.
DEFINE VARIABLE resno           AS INTEGER INIT 27679.   
DEFINE VARIABLE ci-date         AS DATE.    
DEFINE VARIABLE title-str       AS CHAR.
*/
DEFINE VARIABLE new-contrate    AS LOGICAL INITIAL NO.     
DEFINE VARIABLE bonus-array     AS LOGICAL EXTENT 9999 INITIAL NO.   
DEFINE VARIABLE wd-array        AS INTEGER EXTENT 8 INITIAL [7, 1, 2, 3, 4, 5, 6, 7].
DEFINE VARIABLE zim-wunsch      AS CHARACTER.
DEFINE VARIABLE rsv-name        AS CHARACTER.
DEFINE VARIABLE str-common      AS CHARACTER.
DEFINE VARIABLE tot-rate        AS DECIMAL INITIAL 0.
DEFINE VARIABLE abreise-date    AS DATE.    
DEFINE VARIABLE curr-datum      AS DATE.

DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE co-date         AS DATE. 
DEFINE VARIABLE argt-rate       AS DECIMAL. 
DEFINE VARIABLE argt-rate2      AS DECIMAL. 
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE daily-rate      AS DECIMAL.  
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
DEFINE VARIABLE ratecode-qsy    AS CHAR                 NO-UNDO.
DEFINE VARIABLE count-break     AS DECIMAL              NO-UNDO.
DEFINE VARIABLE fixcost-rate    AS DECIMAL              NO-UNDO.

DEFINE BUFFER w1 FOR waehrung. 
/************************************ PROCESS ************************************/
FOR EACH output-list:
    DELETE output-list.
END.

FOR EACH expectedrev-list:
    DELETE expectedrev-list.
END.

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

FIND FIRST htparam WHERE htparam.paramnr EQ 550 NO-LOCK NO-ERROR.  
IF AVAILABLE htparam AND htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.  
  
FIND FIRST htparam WHERE htparam.paramnr EQ 87 NO-LOCK NO-ERROR.   
IF AVAILABLE htparam THEN ci-date = htparam.fdate.

FIND FIRST reservation WHERE reservation.resnr EQ resno NO-LOCK NO-ERROR.
IF AVAILABLE reservation THEN rsv-name = reservation.name.

FOR EACH res-line WHERE res-line.resnr EQ resno 
    AND res-line.resstatus NE 99 
    AND NOT (res-line.resstatus LE 12 AND res-line.resstatus GE 9) /* Dzikri 611B79 - exclude cancel and delete reservation from calculation,
    Also add bill, noshow and roomsharer */
    NO-LOCK BY res-line.reslinnr:

    IF res-line.abreise GT res-line.ankunft THEN abreise-date = res-line.abreise - 1. 
    ELSE abreise-date = res-line.abreise.

    DO curr-datum = res-line.ankunft TO abreise-date:
        CREATE t-res-line.
        ASSIGN
            t-res-line.name         = res-line.name    
            t-res-line.zinr         = res-line.zinr    
            t-res-line.ankunft      = res-line.ankunft 
            t-res-line.abreise      = res-line.abreise
            t-res-line.resnr        = res-line.resnr
            t-res-line.reslinnr     = res-line.reslinnr
            t-res-line.curr-date    = curr-datum
            t-res-line.rmcat-no     = res-line.zikatnr
            .
    
        FIND FIRST guest-pr WHERE guest-pr.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.   
        IF AVAILABLE guest-pr THEN
        DO:
            t-res-line.contcode = guest-pr.CODE.  
            t-res-line.ct-code = res-line.zimmer-wunsch.
            zim-wunsch = res-line.zimmer-wunsch.          
            IF zim-wunsch MATCHES("*$CODE$*") THEN  
            DO:  
                t-res-line.ct-code = SUBSTR(zim-wunsch,INDEX(zim-wunsch,"$CODE$") + 6).  
                t-res-line.contcode = SUBSTR(zim-wunsch, 1, INDEX(zim-wunsch,";") - 1).  
            END.
        END.
    
        IF res-line.l-zuordnung[1] NE 0 THEN   
        DO:   
            FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ res-line.l-zuordnung[1] NO-LOCK NO-ERROR.   
            IF AVAILABLE zimkateg THEN
            DO:
                t-res-line.curr-rmcat = zimkateg.kurzbez.   
                t-res-line.rmcat-bez = zimkateg.bezeich.
            END.                
        END. 
    
        FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ res-line.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN
        DO:
            ASSIGN
                t-res-line.kurzbez = zimkateg.kurzbez
                t-res-line.rmcat-bez = zimkateg.bezeich.
        END.
        FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.  
        IF AVAILABLE arrangement THEN t-res-line.str-argt = arrangement.arrangement.  
            
    END.    
END.
title-str = "Expected Room Revenue" + " " + rsv-name.

RUN check-bonus.

/***** Create RoomRate, Breakdown Argt & Fix Cost Article *****/
FOR EACH t-res-line NO-LOCK,
    FIRST res-line WHERE res-line.resnr EQ t-res-line.resnr
    AND res-line.reslinnr EQ t-res-line.reslinnr NO-LOCK,
    FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement     
    NO-LOCK BY t-res-line.curr-date BY t-res-line.rmcat-no:
        
    FIND FIRST guest-pr WHERE guest-pr.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
    RUN cal-revenue.
END.

/***** Create Lodging *****/
DEFINE BUFFER buf-list FOR output-list.
FOR EACH output-list NO-LOCK BY output-list.datum BY output-list.rmtype-no BY output-list.flag:
    IF output-list.flag EQ 0 OR output-list.flag EQ 1 THEN
    DO:
        FIND FIRST buf-list WHERE buf-list.flag EQ 2
            AND buf-list.datum EQ output-list.datum
            AND buf-list.rmtype-no EQ output-list.rmtype-no NO-LOCK NO-ERROR.
        IF NOT AVAILABLE buf-list THEN
        DO:
            CREATE buf-list. 
            buf-list.flag = 2. 
            buf-list.str-desc = "Lodging".
            buf-list.datum = output-list.datum.
            buf-list.rmtype-no = output-list.rmtype-no. 
            buf-list.calc-lodg = DEC(output-list.str-amount). 
            buf-list.str-amount = TRIM(STRING(buf-list.calc-lodg,"->>>,>>>,>>>,>>9.99")).
        END.
        ELSE
        DO:
            buf-list.calc-lodg = buf-list.calc-lodg - DEC(output-list.str-amount).
            buf-list.str-amount = TRIM(STRING(buf-list.calc-lodg,"->>>,>>>,>>>,>>9.99")).             
        END.
    END.
END.

/***** Create Total Revenue *****/
DEFINE BUFFER buf-out FOR output-list.
FOR EACH output-list NO-LOCK BY output-list.datum BY output-list.rmtype-no BY output-list.flag:
    IF output-list.flag EQ 0 OR output-list.flag EQ 3 THEN
    DO:
        FIND FIRST buf-out WHERE buf-out.flag EQ 4
            AND buf-out.datum EQ output-list.datum
            AND buf-out.rmtype-no EQ output-list.rmtype-no NO-LOCK NO-ERROR.
        IF NOT AVAILABLE buf-out THEN
        DO:
            CREATE buf-out. 
            buf-out.flag = 4. 
            buf-out.str-desc = "Total Revenue".
            buf-out.datum = output-list.datum.
            buf-out.rmtype-no = output-list.rmtype-no. 
            buf-out.calc-totrev = DEC(output-list.str-amount).   
            buf-out.str-amount = TRIM(STRING(buf-out.calc-totrev,"->>>,>>>,>>>,>>9.99")). 
        END.
        ELSE
        DO:
            buf-out.calc-totrev = buf-out.calc-totrev + DEC(output-list.str-amount).
            buf-out.str-amount = TRIM(STRING(buf-out.calc-totrev,"->>>,>>>,>>>,>>9.99")).   
        END.
    END.
END.

/***** Get Expected Total Revenue *****/
tot-rate = 0.
FOR EACH output-list WHERE output-list.flag EQ 0 NO-LOCK:
    tot-rate = tot-rate + DEC(output-list.str-amount).
END.

/***** Break Line *****/
CREATE output-list. 
output-list.flag = 10.

/***** Create Expected Total Revenue *****/
CREATE output-list. 
ASSIGN 
    output-list.flag = 99
    output-list.str-desc = "Expected Total Revenue"
    output-list.str-amount = TRIM(STRING(tot-rate,"->>>,>>>,>>>,>>9.99"))
    .

FOR EACH output-list BY output-list.datum BY output-list.rmtype-no BY output-list.flag:
    CREATE expectedrev-list.
    BUFFER-COPY output-list TO expectedrev-list.
END.

/* Debugging
CURRENT-WINDOW:WIDTH = 200.
FOR EACH expectedrev-list BY expectedrev-list.datum BY expectedrev-list.rmtype-no BY expectedrev-list.flag:
    DISP expectedrev-list.flag expectedrev-list.str-rmtype FORMAT "x(30)" 
        expectedrev-list.str-desc FORMAT "x(50)" expectedrev-list.str-amount FORMAT "x(30)"
        expectedrev-list.rmtype-no expectedrev-list.datum WITH WIDTH 190.
END.
*/
/************************************ PROCEDURE ************************************/
PROCEDURE check-bonus: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE stay AS INTEGER. 
DEFINE VARIABLE pay  AS INTEGER. 
DEFINE VARIABLE num-bonus AS INTEGER INITIAL 0. 

    FOR EACH t-res-line NO-LOCK,
        FIRST arrangement WHERE arrangement.arrangement EQ t-res-line.str-argt 
        NO-LOCK BY t-res-line.reslinnr:

        j = 1. 
        DO i = 1 TO 4: 
            stay = INTEGER(SUBSTR(arrangement.options, j, 2)). 
            pay  = INTEGER(SUBSTR(arrangement.options, j + 2, 2)). 
            IF (stay - pay) GT 0 THEN 
            DO: 
                n = num-bonus + pay  + 1. 
                DO k = n TO stay: 
                    t-res-line.bonus-array[k] = YES. 
                END. 
                num-bonus = stay - pay. 
            END. 
            j = j + 4. 
        END. 
    END.    
END. 

PROCEDURE cal-revenue: 
    curr-i = curr-i + 1.
    bill-date = t-res-line.curr-date.
    argt-rate = 0. 
    daily-rate = 0. 
    fixcost-rate = 0.
    pax = res-line.erwachs. 
    fixed-rate = NO. 
    ratecode-qsy = "Undefined". 
    argt-rate2 = 0.

    n = 0.
    IF res-line.zimmer-wunsch MATCHES ("*DATE,*") THEN n = INDEX(res-line.zimmer-wunsch,"Date,").
    IF n > 0 THEN
    DO:
        c = SUBSTR(res-line.zimmer-wunsch, n + 5, 8).
        created-date = DATE(INTEGER(SUBSTR(c,5,2)), INTEGER(SUBSTR(c,7,2)),INTEGER(SUBSTR(c,1,4))).
    END.
    ELSE created-date = reservation.resdat.
    
    ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*").
    kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").
    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
    ELSE curr-zikatnr = res-line.zikatnr. 
        
    rm-rate = res-line.zipreis.
    daily-rate = res-line.zipreis.

    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        AND bill-date GE reslin-queasy.date1 
        AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
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
        FIND FIRST arrangement WHERE arrangement.arrangement = reslin-queasy.char1 NO-LOCK.  
        RUN usr-prog1(t-res-line.curr-date, INPUT-OUTPUT rm-rate, OUTPUT it-exist). 
    END. 
    
    IF NOT fixed-rate THEN 
    DO: 
        RUN usr-prog1(t-res-line.curr-date, INPUT-OUTPUT rm-rate, OUTPUT it-exist). 
        IF NOT it-exist THEN 
        DO: 
            IF AVAILABLE guest-pr THEN 
            DO: 
                FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = res-line.reserve-int NO-LOCK NO-ERROR. 
                IF AVAILABLE queasy AND queasy.logi3 THEN bill-date = res-line.ankunft. 
                
                IF new-contrate THEN 
                RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                    res-line.reslinnr, t-res-line.contcode, ?, bill-date, res-line.ankunft,
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
                    RUN usr-prog2(t-res-line.curr-date, INPUT-OUTPUT rm-rate, OUTPUT it-exist).
                    IF it-exist THEN rate-found = YES.
                    IF NOT it-exist AND t-res-line.bonus-array[curr-i] = YES THEN rm-rate = 0.  
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
                    IF AVAILABLE katpreis 
                        AND get-rackrate(res-line.erwachs, res-line.kind1, res-line.kind2) = rm-rate 
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
                    IF AVAILABLE katpreis 
                        AND get-rackrate(res-line.erwachs, res-line.kind1, res-line.kind2) > 0 
                    THEN rm-rate = get-rackrate(res-line.erwachs,res-line.kind1, res-line.kind2). 
                END. /* if rack-rate   */ 
                IF t-res-line.bonus-array[curr-i] = YES THEN rm-rate = 0.  
            END.   /* publish rate   */  
        END.     /* not exist      */ 
    END.       /* not fixed rate */

    FIND FIRST output-list WHERE output-list.datum EQ t-res-line.curr-date NO-LOCK NO-ERROR.
    IF NOT AVAILABLE output-list THEN
    DO:                
        count-break = 0.

        CREATE output-list.
        output-list.datum = t-res-line.curr-date.
        output-list.str-rmtype = STRING(t-res-line.curr-date).
        output-list.rmtype-no = t-res-line.rmcat-no.

        FIND FIRST output-list WHERE output-list.rmtype-no EQ t-res-line.rmcat-no
            AND output-list.flag EQ 0
            AND output-list.datum EQ t-res-line.curr-date NO-LOCK NO-ERROR.
        IF NOT AVAILABLE output-list THEN
        DO:
            CREATE output-list.
            ASSIGN
                output-list.flag = 0
                output-list.datum = t-res-line.curr-date
                output-list.rmtype-no = t-res-line.rmcat-no                    
                output-list.str-rmtype = t-res-line.rmcat-bez                                       
                .
        END.
        output-list.str-desc = "Room Rate".
        output-list.calc-rmrate = rm-rate.
        output-list.str-amount = TRIM(STRING(rm-rate,"->>>,>>>,>>>,>>9.99")).
        
        IF rm-rate NE 0 THEN
        DO:
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
                        IF res-line.ankunft EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 3 THEN 
                    DO: 
                        IF (res-line.ankunft + 1) EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 4 AND day(t-res-line.curr-date) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 5 AND day(t-res-line.curr-date + 1) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 6 THEN 
                    DO: 
                        /* Dzikri 3DC423 - Repair Arrangemnt type 6
                            IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE t-res-line.curr-date THEN
                                add-it = YES.  */
                            FIND FIRST argt-list WHERE argt-list.argtnr EQ argt-line.argtnr 
                                AND argt-list.departement EQ argt-line.departement 
                                AND argt-list.argt-artnr  EQ argt-line.argt-artnr 
                                AND argt-list.vt-percnt   EQ argt-line.vt-percnt
                                AND argt-list.resnr       EQ res-line.resnr 
                                AND argt-list.reslinnr    EQ res-line.reslinnr 
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
                                    argt-list.resnr       = res-line.resnr 
                                    argt-list.reslinnr    = res-line.reslinnr 
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
                                    AND reslin-queasy.date2 GE res-line.ankunft NO-LOCK NO-ERROR.
                                IF AVAILABLE reslin-queasy THEN 
                                DO:
                                    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                                        AND reslin-queasy.char1    = "" 
                                        AND reslin-queasy.number1  = argt-line.departement 
                                        AND reslin-queasy.number2  = argt-line.argtnr 
                                        AND reslin-queasy.resnr    = res-line.resnr 
                                        AND reslin-queasy.reslinnr = res-line.reslinnr 
                                        AND reslin-queasy.number3  = argt-line.argt-artnr 
                                        AND reslin-queasy.date1 LE curr-date 
                                        AND reslin-queasy.date2 GE curr-date NO-LOCK NO-ERROR. 
                                    IF AVAILABLE reslin-queasy THEN 
                                    DO:
                                        IF (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE curr-date THEN
                                        DO:
                                            add-it = YES. 
                                            argt-list.period = argt-list.period + 1.
                                        END.
                                    END.
                                END.
                                ELSE
                                DO:
                                    IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE curr-date THEN
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
                            IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                                argt-rate = rm-rate * INT(reslin-queasy.char2) / 100. 
                            ELSE
                            DO:
                                /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3.                  */
                            
                                IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                                ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                                ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                            END.    
                            
                            /*ITA 29/10/18 --> jika yang diisi in%*/
                            IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                            ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                              
                            /*argt-rate = argt-rate * qty.*/                
                            
                            IF argt-rate NE 0 THEN
                            DO:
                                CREATE output-list. 
                                output-list.flag = 1. 
                                output-list.datum = t-res-line.curr-date.
                                output-list.article-no = artikel.artnr. 
                                output-list.dept-no = artikel.departement.  
                                output-list.rmtype-no = t-res-line.rmcat-no.
                                output-list.calc-qty = qty.
                                str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich.  
                                output-list.str-desc = "Incl." + " " + str-common.    
                                output-list.calc-argtrate-all = argt-rate.
                                output-list.str-amount = TRIM(STRING(argt-rate,"->>>,>>>,>>>,>>9.99")).                                
                                output-list.calc-argtrate = argt-rate.
                                count-break = argt-rate.
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
                                IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3. 
                            
                                /*ITA 29/10/18 --> jika yang diisi in%*/
                                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                                  
                                /*argt-rate = argt-rate * qty.*/
                            
                                IF argt-rate NE 0 THEN
                                DO:
                                    CREATE output-list. 
                                    output-list.flag = 1. 
                                    output-list.datum = t-res-line.curr-date.
                                    output-list.article-no = artikel.artnr. 
                                    output-list.dept-no = artikel.departement.     
                                    output-list.rmtype-no = t-res-line.rmcat-no.
                                    output-list.calc-qty = qty.
                                    str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                                    output-list.str-desc = "Incl." + " " + str-common.        
                                    output-list.calc-argtrate-all = argt-rate.
                                    output-list.str-amount = TRIM(STRING(argt-rate,"->>>,>>>,>>>,>>9.99")).
                                    output-list.calc-argtrate = argt-rate.
                                    count-break = argt-rate.
                                END.
                            END.
                        END. 
                    END. 
                            
                    /*ITA 29/10/18 --> jika yang diisi in%*/
                    IF argt-rate2 GT 0 THEN argt-rate2 = argt-rate2 * qty. 
                    ELSE argt-rate2 = (rm-rate * (- argt-rate2 / 100)) * qty.          
                    /*argt-rate = argt-rate * qty.*/
                    
                    IF argt-rate2 NE 0 AND argt-rate = 0 THEN
                    DO:
                        CREATE output-list. 
                        output-list.flag = 1. 
                        output-list.datum = t-res-line.curr-date.
                        output-list.article-no = artikel.artnr. 
                        output-list.dept-no = artikel.departement.      
                        output-list.rmtype-no = t-res-line.rmcat-no.
                        output-list.calc-qty = qty.
                        str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                        output-list.str-desc = "Incl." + " " + str-common.    
                        output-list.calc-argtrate-all = argt-rate2.
                        output-list.str-amount = TRIM(STRING(argt-rate2,"->>>,>>>,>>>,>>9.99")).
                        output-list.calc-argtrate2 = argt-rate2.
                        count-break = argt-rate2.
                        output-list.count-break = argt-rate2.
                    END.
                END. /* IF addi-it */ 
            END.   /* each argt-line */

            /****** FDL: 0E0B99 - additional fix cost from arrangement ******/
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
                        IF res-line.ankunft EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 3 THEN 
                    DO: 
                        IF (res-line.ankunft + 1) EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 4 AND day(t-res-line.curr-date) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 5 AND day(t-res-line.curr-date + 1) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 6 THEN 
                    DO: 
                        /* Dzikri 3DC423 - Repair Arrangemnt type 6
                            IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE t-res-line.curr-date THEN
                                add-it = YES.  */
                            FIND FIRST argt-list WHERE argt-list.argtnr EQ argt-line.argtnr 
                                AND argt-list.departement EQ argt-line.departement 
                                AND argt-list.argt-artnr  EQ argt-line.argt-artnr 
                                AND argt-list.vt-percnt   EQ argt-line.vt-percnt
                                AND argt-list.resnr       EQ res-line.resnr 
                                AND argt-list.reslinnr    EQ res-line.reslinnr 
                                AND argt-list.is-charged  EQ 1  NO-LOCK NO-ERROR.
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
                                    argt-list.resnr       = res-line.resnr 
                                    argt-list.reslinnr    = res-line.reslinnr 
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
                                    AND reslin-queasy.date2 GE res-line.ankunft NO-LOCK NO-ERROR.
                                IF AVAILABLE reslin-queasy THEN 
                                DO:
                                    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                                        AND reslin-queasy.char1    = "" 
                                        AND reslin-queasy.number1  = argt-line.departement 
                                        AND reslin-queasy.number2  = argt-line.argtnr 
                                        AND reslin-queasy.resnr    = res-line.resnr 
                                        AND reslin-queasy.reslinnr = res-line.reslinnr 
                                        AND reslin-queasy.number3  = argt-line.argt-artnr 
                                        AND reslin-queasy.date1 LE curr-date 
                                        AND reslin-queasy.date2 GE curr-date NO-LOCK NO-ERROR. 
                                    IF AVAILABLE reslin-queasy THEN 
                                    DO:
                                        IF (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE curr-date THEN
                                        DO:
                                            add-it = YES. 
                                            argt-list.period = argt-list.period + 1.
                                        END.
                                    END.
                                END.
                                ELSE
                                DO:
                                    IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE curr-date THEN
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
                            IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                                argt-rate = rm-rate * INT(reslin-queasy.char2) / 100. 
                            ELSE
                            DO:
                                /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3.                  */
                            
                                IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                                ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                                ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                            END.    
                            
                            /*ITA 29/10/18 --> jika yang diisi in%*/
                            IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                            ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                              
                            /*argt-rate = argt-rate * qty.*/                
                            
                            IF argt-rate NE 0 THEN
                            DO:
                                CREATE output-list. 
                                output-list.flag = 3. 
                                output-list.datum = t-res-line.curr-date.
                                output-list.article-no = artikel.artnr. 
                                output-list.dept-no = artikel.departement.  
                                output-list.rmtype-no = t-res-line.rmcat-no.
                                output-list.calc-qty = qty.
                                str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich.  
                                output-list.str-desc = "Excl." + " " + str-common.                                         
                                output-list.str-amount = TRIM(STRING(argt-rate,"->>>,>>>,>>>,>>9.99")).
                                output-list.calc-argtrate = argt-rate.
                                count-break = argt-rate.
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
                                IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3. 
                            
                                /*ITA 29/10/18 --> jika yang diisi in%*/
                                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                                  
                                /*argt-rate = argt-rate * qty.*/
                            
                                IF argt-rate NE 0 THEN
                                DO:
                                    CREATE output-list. 
                                    output-list.flag = 3. 
                                    output-list.datum = t-res-line.curr-date.
                                    output-list.article-no = artikel.artnr. 
                                    output-list.dept-no = artikel.departement.     
                                    output-list.rmtype-no = t-res-line.rmcat-no.
                                    output-list.calc-qty = qty.
                                    str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                                    output-list.str-desc = "Excl." + " " + str-common.                                         
                                    output-list.str-amount = TRIM(STRING(argt-rate,"->>>,>>>,>>>,>>9.99")).
                                    output-list.calc-argtrate = argt-rate.
                                    count-break = argt-rate.
                                END.
                            END.
                        END. 
                    END. 
                            
                    /*ITA 29/10/18 --> jika yang diisi in%*/
                    IF argt-rate2 GT 0 THEN argt-rate2 = argt-rate2 * qty. 
                    ELSE argt-rate2 = (rm-rate * (- argt-rate2 / 100)) * qty.          
                    /*argt-rate = argt-rate * qty.*/
                    
                    IF argt-rate2 NE 0 AND argt-rate = 0 THEN
                    DO:
                        CREATE output-list. 
                        output-list.flag = 3. 
                        output-list.datum = t-res-line.curr-date.
                        output-list.article-no = artikel.artnr. 
                        output-list.dept-no = artikel.departement.      
                        output-list.rmtype-no = t-res-line.rmcat-no.
                        output-list.calc-qty = qty.
                        str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                        output-list.str-desc = "Excl." + " " + str-common.                                         
                        output-list.str-amount = TRIM(STRING(argt-rate2,"->>>,>>>,>>>,>>9.99")).
                        output-list.calc-argtrate2 = argt-rate2.
                        count-break = argt-rate2.
                        output-list.count-break = argt-rate2.
                    END.
                END. /* IF addi-it */ 
            END.   /* each argt-line */

            /**** additional fix cost ******/ 
            FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
                AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
              
                add-it = NO. 
                argt-rate = 0. 
                IF fixleist.sequenz = 1 THEN add-it = YES. 
                ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
                DO: 
                    IF res-line.ankunft EQ t-res-line.curr-date THEN add-it = YES. 
                END. 
                ELSE IF fixleist.sequenz = 4 AND day(t-res-line.curr-date) = 1 THEN add-it = YES. 
                ELSE IF fixleist.sequenz = 5 AND day(t-res-line.curr-date + 1) = 1 THEN add-it = YES. 
                ELSE IF fixleist.sequenz = 6 THEN 
                DO: 
                    IF lfakt = ? THEN delta = 0. 
                    ELSE 
                    DO: 
                        delta = lfakt - res-line.ankunft. 
                        IF delta LT 0 THEN delta = 0. 
                    END. 
                    start-date = res-line.ankunft + delta. 
                    IF (res-line.abreise - start-date) LT fixleist.dekade THEN start-date = res-line.ankunft. 
                    IF t-res-line.curr-date LE (start-date + (fixleist.dekade - 1)) THEN add-it = YES. 
                    IF t-res-line.curr-date LT start-date THEN add-it = no. /* may NOT post !! */ 
                END. 
                IF add-it THEN 
                DO: 
                    FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
                        AND artikel.departement = fixleist.departement NO-LOCK. 
                    argt-rate = fixleist.betrag * fixleist.number.                              
                END. 
                IF argt-rate NE 0 THEN 
                DO: 
                    CREATE output-list. 
                    output-list.flag = 3.
                    output-list.datum = t-res-line.curr-date.
                    output-list.article-no = artikel.artnr.
                    output-list.dept-no = artikel.departement.
                    output-list.str-desc = artikel.bezeich.
                    output-list.rmtype-no = t-res-line.rmcat-no.
                    output-list.str-amount = TRIM(STRING(argt-rate,"->>>,>>>,>>>,>>9.99")).
                    output-list.calc-fixcost = argt-rate.
                    tot-rate = tot-rate + argt-rate.                                                                         
                    fixcost-rate = fixcost-rate + argt-rate.
                    /*daily-rate = daily-rate + argt-rate. */
                END.       
            END. 
        END. /*rm-rate NE 0*/
    END.             
    ELSE
    DO:
        FIND FIRST output-list WHERE output-list.rmtype-no EQ t-res-line.rmcat-no
            AND output-list.flag EQ 0
            AND output-list.datum EQ t-res-line.curr-date NO-LOCK NO-ERROR.
        IF NOT AVAILABLE output-list THEN
        DO:
            CREATE output-list.
            ASSIGN
                output-list.flag = 0
                output-list.datum = t-res-line.curr-date
                output-list.rmtype-no = t-res-line.rmcat-no                    
                output-list.str-rmtype = t-res-line.rmcat-bez                                       
                .
        END.

        output-list.str-desc = "Room Rate".
        output-list.calc-rmrate = output-list.calc-rmrate + rm-rate.
        output-list.str-amount = TRIM(STRING(output-list.calc-rmrate,"->>>,>>>,>>>,>>9.99")).
        
        IF rm-rate NE 0 THEN
        DO:
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
                        IF res-line.ankunft EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 3 THEN 
                    DO: 
                        IF (res-line.ankunft + 1) EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 4 AND day(t-res-line.curr-date) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 5 AND day(t-res-line.curr-date + 1) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 6 THEN 
                    DO: 
                        /* Dzikri 3DC423 - Repair Arrangemnt type 6
                            IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE t-res-line.curr-date THEN
                                add-it = YES.  */
                            FIND FIRST argt-list WHERE argt-list.argtnr EQ argt-line.argtnr 
                                AND argt-list.departement EQ argt-line.departement 
                                AND argt-list.argt-artnr  EQ argt-line.argt-artnr 
                                AND argt-list.vt-percnt   EQ argt-line.vt-percnt
                                AND argt-list.resnr       EQ res-line.resnr 
                                AND argt-list.reslinnr    EQ res-line.reslinnr 
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
                                    argt-list.resnr       = res-line.resnr 
                                    argt-list.reslinnr    = res-line.reslinnr 
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
                                    AND reslin-queasy.date2 GE res-line.ankunft NO-LOCK NO-ERROR.
                                IF AVAILABLE reslin-queasy THEN 
                                DO:
                                    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                                        AND reslin-queasy.char1    = "" 
                                        AND reslin-queasy.number1  = argt-line.departement 
                                        AND reslin-queasy.number2  = argt-line.argtnr 
                                        AND reslin-queasy.resnr    = res-line.resnr 
                                        AND reslin-queasy.reslinnr = res-line.reslinnr 
                                        AND reslin-queasy.number3  = argt-line.argt-artnr 
                                        AND reslin-queasy.date1 LE curr-date 
                                        AND reslin-queasy.date2 GE curr-date NO-LOCK NO-ERROR. 
                                    IF AVAILABLE reslin-queasy THEN 
                                    DO:
                                        IF (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE curr-date THEN
                                        DO:
                                            add-it = YES. 
                                            argt-list.period = argt-list.period + 1.
                                        END.
                                    END.
                                END.
                                ELSE
                                DO:
                                    IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE curr-date THEN
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
                            IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                                argt-rate = rm-rate * INT(reslin-queasy.char2) / 100. 
                            ELSE
                            DO:
                                /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3.                  */
                            
                                IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                                ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                                ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                            END.    
                            
                            /*ITA 29/10/18 --> jika yang diisi in%*/
                            IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                            ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                              
                            /*argt-rate = argt-rate * qty.*/                
                            
                            IF argt-rate NE 0 THEN
                            DO:
                                FIND FIRST output-list WHERE output-list.flag EQ 1
                                    AND output-list.article-no EQ artikel.artnr
                                    AND output-list.dept-no EQ artikel.departement
                                    AND output-list.datum EQ t-res-line.curr-date
                                    AND output-list.rmtype-no EQ t-res-line.rmcat-no NO-LOCK NO-ERROR.
                                IF NOT AVAILABLE output-list THEN
                                DO:
                                    CREATE output-list. 
                                    output-list.flag = 1.
                                    output-list.article-no = artikel.artnr.
                                    output-list.dept-no = artikel.departement.
                                    output-list.datum = t-res-line.curr-date.
                                    output-list.rmtype-no = t-res-line.rmcat-no.
                                END.
                                output-list.calc-qty = output-list.calc-qty + qty.
                                str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                                output-list.str-desc = "Incl." + " " + str-common.
        
                                output-list.calc-argtrate = output-list.calc-argtrate + argt-rate.    
                                output-list.calc-argtrate-all = output-list.calc-argtrate-all + argt-rate.
                                output-list.str-amount = TRIM(STRING(output-list.calc-argtrate,"->>>,>>>,>>>,>>9.99")).
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
                                IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3. 
                            
                                /*ITA 29/10/18 --> jika yang diisi in%*/
                                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                                  
                                /*argt-rate = argt-rate * qty.*/
                            
                                IF argt-rate NE 0 THEN
                                DO:
                                     FIND FIRST output-list WHERE output-list.flag EQ 1
                                        AND output-list.article-no EQ artikel.artnr
                                        AND output-list.dept-no EQ artikel.departement
                                        AND output-list.datum EQ t-res-line.curr-date
                                        AND output-list.rmtype-no EQ t-res-line.rmcat-no NO-LOCK NO-ERROR.
                                    IF NOT AVAILABLE output-list THEN
                                    DO:
                                        CREATE output-list. 
                                        output-list.flag = 1.
                                        output-list.article-no = artikel.artnr.
                                        output-list.dept-no = artikel.departement.
                                        output-list.datum = t-res-line.curr-date.
                                        output-list.rmtype-no = t-res-line.rmcat-no.
                                    END.
                                    output-list.calc-qty = output-list.calc-qty + qty.
                                    str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                                    output-list.str-desc = "Incl." + " " + str-common.
            
                                    output-list.calc-argtrate = output-list.calc-argtrate + argt-rate.    
                                    output-list.calc-argtrate-all = output-list.calc-argtrate-all + argt-rate.
                                    output-list.str-amount = TRIM(STRING(output-list.calc-argtrate,"->>>,>>>,>>>,>>9.99")).
                                    count-break = count-break + argt-rate.                                    
                                END.
                            END.
                        END. 
                    END. 
                            
                    /*ITA 29/10/18 --> jika yang diisi in%*/
                    IF argt-rate2 GT 0 THEN argt-rate2 = argt-rate2 * qty. 
                    ELSE argt-rate2 = (rm-rate * (- argt-rate2 / 100)) * qty.          
                    /*argt-rate = argt-rate * qty.*/
                    
                    IF argt-rate2 NE 0 AND argt-rate = 0 THEN
                    DO:
                        FIND FIRST output-list WHERE output-list.flag EQ 1
                            AND output-list.article-no EQ artikel.artnr
                            AND output-list.dept-no EQ artikel.departement
                            AND output-list.datum EQ t-res-line.curr-date
                            AND output-list.rmtype-no EQ t-res-line.rmcat-no NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE output-list THEN
                        DO:
                            CREATE output-list. 
                            output-list.flag = 1.
                            output-list.article-no = artikel.artnr.
                            output-list.dept-no = artikel.departement.
                            output-list.datum = t-res-line.curr-date.
                            output-list.rmtype-no = t-res-line.rmcat-no.
                        END.
                        output-list.calc-qty = output-list.calc-qty + qty.
                        str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                        output-list.str-desc = "Incl." + " " + str-common.

                        output-list.calc-argtrate2 = output-list.calc-argtrate2 + argt-rate2.   
                        output-list.calc-argtrate-all = output-list.calc-argtrate-all + argt-rate2.
                        output-list.str-amount = TRIM(STRING(output-list.calc-argtrate2,"->>>,>>>,>>>,>>9.99")).
                        count-break = count-break + argt-rate2.
                        output-list.count-break = output-list.count-break + argt-rate2.
                    END.
                    output-list.str-amount = TRIM(STRING(output-list.calc-argtrate-all,"->>>,>>>,>>>,>>9.99")).
                END. /* IF addi-it */ 
            END.   /* each argt-line */

            /****** FDL: 0E0B99 - additional fix cost from arrangement ******/
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
                        IF res-line.ankunft EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 3 THEN 
                    DO: 
                        IF (res-line.ankunft + 1) EQ t-res-line.curr-date THEN add-it = YES. 
                    END. 
                    ELSE IF argt-line.fakt-modus = 4 AND day(t-res-line.curr-date) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 5 AND day(t-res-line.curr-date + 1) = 1 THEN add-it = YES. 
                    ELSE IF argt-line.fakt-modus = 6 THEN 
                    DO: 
                        /* Dzikri 3DC423 - Repair Arrangemnt type 6
                            IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE t-res-line.curr-date THEN
                                add-it = YES.  */
                            FIND FIRST argt-list WHERE argt-list.argtnr EQ argt-line.argtnr 
                                AND argt-list.departement EQ argt-line.departement 
                                AND argt-list.argt-artnr  EQ argt-line.argt-artnr 
                                AND argt-list.vt-percnt   EQ argt-line.vt-percnt
                                AND argt-list.resnr       EQ res-line.resnr 
                                AND argt-list.reslinnr    EQ res-line.reslinnr 
                                AND argt-list.is-charged  EQ 1  NO-LOCK NO-ERROR.
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
                                    argt-list.resnr       = res-line.resnr 
                                    argt-list.reslinnr    = res-line.reslinnr 
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
                                    AND reslin-queasy.date2 GE res-line.ankunft NO-LOCK NO-ERROR.
                                IF AVAILABLE reslin-queasy THEN 
                                DO:
                                    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                                        AND reslin-queasy.char1    = "" 
                                        AND reslin-queasy.number1  = argt-line.departement 
                                        AND reslin-queasy.number2  = argt-line.argtnr 
                                        AND reslin-queasy.resnr    = res-line.resnr 
                                        AND reslin-queasy.reslinnr = res-line.reslinnr 
                                        AND reslin-queasy.number3  = argt-line.argt-artnr 
                                        AND reslin-queasy.date1 LE curr-date 
                                        AND reslin-queasy.date2 GE curr-date NO-LOCK NO-ERROR. 
                                    IF AVAILABLE reslin-queasy THEN 
                                    DO:
                                        IF (reslin-queasy.date1 + (argt-line.intervall - 1 /**/)) GE curr-date THEN
                                        DO:
                                            add-it = YES. 
                                            argt-list.period = argt-list.period + 1.
                                        END.
                                    END.
                                END.
                                ELSE
                                DO:
                                    IF (res-line.ankunft + (argt-line.intervall - 1 /**/)) GE curr-date THEN
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
                            IF reslin-queasy.char2 NE "" AND reslin-queasy.char2 NE "0" THEN 
                                argt-rate = rm-rate * INT(reslin-queasy.char2) / 100. 
                            ELSE
                            DO:
                                /*IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3.                  */
                            
                                IF reslin-queasy.deci1 NE 0 THEN argt-rate = reslin-queasy.deci1.
                                ELSE IF reslin-queasy.deci2 NE 0 THEN argt-rate = reslin-queasy.deci2.
                                ELSE IF reslin-queasy.deci3 NE 0 THEN argt-rate = reslin-queasy.deci3.
                            END.    
                            
                            /*ITA 29/10/18 --> jika yang diisi in%*/
                            IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                            ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                              
                            /*argt-rate = argt-rate * qty.*/                
                            
                            IF argt-rate NE 0 THEN
                            DO:
                                FIND FIRST output-list WHERE output-list.flag EQ 1
                                    AND output-list.article-no EQ artikel.artnr
                                    AND output-list.dept-no EQ artikel.departement
                                    AND output-list.datum EQ t-res-line.curr-date
                                    AND output-list.rmtype-no EQ t-res-line.rmcat-no NO-LOCK NO-ERROR.
                                IF NOT AVAILABLE output-list THEN
                                DO:
                                    CREATE output-list. 
                                    output-list.flag = 3.
                                    output-list.article-no = artikel.artnr.
                                    output-list.dept-no = artikel.departement.
                                    output-list.datum = t-res-line.curr-date.
                                    output-list.rmtype-no = t-res-line.rmcat-no.
                                END.
                                output-list.calc-qty = output-list.calc-qty + qty.
                                str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                                output-list.str-desc = "Excl." + " " + str-common.
        
                                output-list.calc-argtrate = output-list.calc-argtrate + argt-rate.      
                                output-list.str-amount = TRIM(STRING(output-list.calc-argtrate,"->>>,>>>,>>>,>>9.99")).
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
                                IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
                                ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
                                ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3. 
                            
                                /*ITA 29/10/18 --> jika yang diisi in%*/
                                IF argt-rate GT 0 THEN argt-rate = argt-rate * qty. 
                                ELSE argt-rate = (rm-rate * (- argt-rate / 100)) * qty.
                                  
                                /*argt-rate = argt-rate * qty.*/
                            
                                IF argt-rate NE 0 THEN
                                DO:
                                     FIND FIRST output-list WHERE output-list.flag EQ 1
                                        AND output-list.article-no EQ artikel.artnr
                                        AND output-list.dept-no EQ artikel.departement
                                        AND output-list.datum EQ t-res-line.curr-date
                                        AND output-list.rmtype-no EQ t-res-line.rmcat-no NO-LOCK NO-ERROR.
                                    IF NOT AVAILABLE output-list THEN
                                    DO:
                                        CREATE output-list. 
                                        output-list.flag = 3.
                                        output-list.article-no = artikel.artnr.
                                        output-list.dept-no = artikel.departement.
                                        output-list.datum = t-res-line.curr-date.
                                        output-list.rmtype-no = t-res-line.rmcat-no.
                                    END.
                                    output-list.calc-qty = output-list.calc-qty + qty.
                                    str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                                    output-list.str-desc = "Excl." + " " + str-common.
            
                                    output-list.calc-argtrate = output-list.calc-argtrate + argt-rate.      
                                    output-list.str-amount = TRIM(STRING(output-list.calc-argtrate,"->>>,>>>,>>>,>>9.99")).
                                    count-break = count-break + argt-rate.                                    
                                END.
                            END.
                        END. 
                    END. 
                            
                    /*ITA 29/10/18 --> jika yang diisi in%*/
                    IF argt-rate2 GT 0 THEN argt-rate2 = argt-rate2 * qty. 
                    ELSE argt-rate2 = (rm-rate * (- argt-rate2 / 100)) * qty.          
                    /*argt-rate = argt-rate * qty.*/
                    
                    IF argt-rate2 NE 0 AND argt-rate = 0 THEN
                    DO:
                        FIND FIRST output-list WHERE output-list.flag EQ 1
                            AND output-list.article-no EQ artikel.artnr
                            AND output-list.dept-no EQ artikel.departement
                            AND output-list.datum EQ t-res-line.curr-date
                            AND output-list.rmtype-no EQ t-res-line.rmcat-no NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE output-list THEN
                        DO:
                            CREATE output-list. 
                            output-list.flag = 3.
                            output-list.article-no = artikel.artnr.
                            output-list.dept-no = artikel.departement.
                            output-list.datum = t-res-line.curr-date.
                            output-list.rmtype-no = t-res-line.rmcat-no.
                        END.
                        output-list.calc-qty = output-list.calc-qty + qty.
                        str-common = STRING(output-list.calc-qty) + " " + artikel.bezeich. 
                        output-list.str-desc = "Excl." + " " + str-common.

                        output-list.calc-argtrate2 = output-list.calc-argtrate2 + argt-rate2.      
                        output-list.str-amount = TRIM(STRING(output-list.calc-argtrate2,"->>>,>>>,>>>,>>9.99")).
                        count-break = count-break + argt-rate2.
                        output-list.count-break = output-list.count-break + argt-rate2.
                    END.
                END. /* IF addi-it */ 
            END.   /* each argt-line */

            /**** additional fix cost ******/ 
            FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
                AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
              
                add-it = NO. 
                argt-rate = 0. 
                IF fixleist.sequenz = 1 THEN add-it = YES. 
                ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
                DO: 
                    IF res-line.ankunft EQ t-res-line.curr-date THEN add-it = YES. 
                END. 
                ELSE IF fixleist.sequenz = 4 AND day(t-res-line.curr-date) = 1 THEN add-it = YES. 
                ELSE IF fixleist.sequenz = 5 AND day(t-res-line.curr-date + 1) = 1 THEN add-it = YES. 
                ELSE IF fixleist.sequenz = 6 THEN 
                DO: 
                    IF lfakt = ? THEN delta = 0. 
                    ELSE 
                    DO: 
                        delta = lfakt - res-line.ankunft. 
                        IF delta LT 0 THEN delta = 0. 
                    END. 
                    start-date = res-line.ankunft + delta. 
                    IF (res-line.abreise - start-date) LT fixleist.dekade THEN start-date = res-line.ankunft. 
                    IF t-res-line.curr-date LE (start-date + (fixleist.dekade - 1)) THEN add-it = YES. 
                    IF t-res-line.curr-date LT start-date THEN add-it = no. /* may NOT post !! */ 
                END. 
                IF add-it THEN 
                DO: 
                    FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
                        AND artikel.departement = fixleist.departement NO-LOCK. 
                    argt-rate = fixleist.betrag * fixleist.number.                              
                END. 
                IF argt-rate NE 0 THEN 
                DO: 
                    FIND FIRST output-list WHERE output-list.flag EQ 2
                        AND output-list.article-no EQ artikel.artnr
                        AND output-list.dept-no EQ artikel.departement
                        AND output-list.datum EQ t-res-line.curr-date
                        AND output-list.rmtype-no EQ t-res-line.rmcat-no NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN
                    DO:
                        CREATE output-list. 
                        output-list.flag = 3.
                        output-list.article-no = artikel.artnr.
                        output-list.dept-no = artikel.departement.
                        output-list.str-desc = artikel.bezeich.
                        output-list.datum = t-res-line.curr-date.
                        output-list.rmtype-no = t-res-line.rmcat-no.
                    END.
                    output-list.calc-fixcost = output-list.calc-fixcost + argt-rate.
                    output-list.str-amount = TRIM(STRING(output-list.calc-fixcost,"->>>,>>>,>>>,>>9.99")).                    
                    tot-rate = tot-rate + argt-rate.                                                                         
                    fixcost-rate = fixcost-rate + argt-rate.
                    /*daily-rate = daily-rate + argt-rate. */
                END.       
            END. 
        END. /*rm-rate NE 0*/        
    END.
END. 

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
/*   
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
*/
END. 
