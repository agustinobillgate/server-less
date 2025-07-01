DEFINE TEMP-TABLE output-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD STR AS CHAR FORMAT "x(68)" 
  FIELD str1 AS CHAR. 

DEF INPUT PARAMETER pvILanguage         AS INTEGER NO-UNDO.
DEF INPUT PARAMETER ankunft             AS DATE        NO-UNDO.
DEF INPUT PARAMETER abreise             AS DATE        NO-UNDO.
DEF INPUT PARAMETER contcode            AS CHAR        NO-UNDO.
DEF INPUT PARAMETER currency            AS CHAR        NO-UNDO.
DEF INPUT PARAMETER curr-rmcat          AS CHAR        NO-UNDO.
DEF INPUT PARAMETER curr-argt           AS CHAR        NO-UNDO.
DEF INPUT PARAMETER rate-zikat          AS CHAR        NO-UNDO.
DEF INPUT PARAMETER zimmer-wunsch       AS CHAR        NO-UNDO.
DEF INPUT PARAMETER inp-gastnr          AS INTEGER     NO-UNDO.
DEF INPUT PARAMETER inp-resnr           AS INTEGER     NO-UNDO.
DEF INPUT PARAMETER inp-reslinnr        AS INTEGER     NO-UNDO.
DEF INPUT PARAMETER marketnr            AS INTEGER     NO-UNDO.
DEF INPUT PARAMETER zimmeranz           AS INTEGER     NO-UNDO.
DEF INPUT PARAMETER pax                 AS INTEGER     NO-UNDO.
DEF INPUT PARAMETER kind1               AS INTEGER     NO-UNDO.
DEF INPUT PARAMETER inp-rmrate          AS DECIMAL     NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE wd-array AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 
DEFINE VARIABLE bonus-array         AS LOGICAL EXTENT 999 INITIAL NO. 
DEFINE VARIABLE ci-date             AS DATE NO-UNDO.

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
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST waehrung WHERE waehrung.wabkurz = currency NO-LOCK.
IF NOT AVAILABLE waehrung THEN 
    FIND FIRST waehrung WHERE waehrung.wabkurz = "1" NO-LOCK.
/*
FIND FIRST arrangement WHERE arrangement.arrangement = curr-argt 
    NO-LOCK.  
RUN check-bonus.

RUN cal-revenue.*/

/************** PROCEDURE *******************/
/* FD Dec 12, 2019 -> comment for issue output value argt-line with in %(percentage) 
    not percentage from room rate, but is that percentage

PROCEDURE cal-revenue: 
DEFINE VARIABLE datum           AS DATE NO-UNDO. 
DEFINE VARIABLE co-date         AS DATE NO-UNDO. 
DEFINE VARIABLE argt-rate       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE rm-rate         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE daily-rate      AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-rate        AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE add-it          AS LOGICAL NO-UNDO. 
DEFINE VARIABLE c               AS CHAR NO-UNDO. 
DEFINE VARIABLE fixed-rate      AS LOGICAL NO-UNDO INITIAL NO. 
DEFINE VARIABLE argt-defined    AS LOGICAL NO-UNDO INITIAL NO. 
DEFINE VARIABLE delta           AS INTEGER NO-UNDO. 
DEFINE VARIABLE start-date      AS DATE NO-UNDO. 
DEFINE VARIABLE qty             AS INTEGER NO-UNDO. 
DEFINE VARIABLE it-exist        AS LOGICAL NO-UNDO INITIAL NO. 
DEFINE VARIABLE exrate1         AS DECIMAL NO-UNDO INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL NO-UNDO INITIAL 1. 
DEFINE VARIABLE pax             AS INTEGER              NO-UNDO. 
DEFINE VARIABLE child1          AS INTEGER              NO-UNDO. 
DEFINE VARIABLE n               AS INTEGER              NO-UNDO.
DEFINE VARIABLE created-date    AS DATE    INITIAL ?    NO-UNDO.
DEFINE VARIABLE bill-date       AS DATE                 NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE curr-i          AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE w-day           AS INTEGER              NO-UNDO. 
DEFINE VARIABLE rack-rate       AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE fix-exrate      AS DECIMAL INITIAL 0    NO-UNDO.

DEFINE BUFFER w1 FOR waehrung. 
  
  FIND FIRST res-line WHERE res-line.resnr = inp-resnr
      AND res-line.reslinnr = inp-reslinnr NO-LOCK NO-ERROR.
  IF AVAILABLE res-line THEN fix-exrate = res-line.reserve-dec.

  n = 0.
  IF zimmer-wunsch MATCHES ("*DATE,*") THEN
  n = INDEX(zimmer-wunsch,"Date,").
  IF n > 0 THEN
  DO:
    c = SUBSTR(zimmer-wunsch, n + 5, 8).
    created-date = DATE(INTEGER(SUBSTR(c,5,2)), INTEGER(SUBSTR(c,7,2)),
      INTEGER(SUBSTR(c,1,4))).
  END.
  IF created-date = ? THEN created-date = ci-date.

  ebdisc-flag = zimmer-wunsch MATCHES ("*ebdisc*").
  kbdisc-flag = zimmer-wunsch MATCHES ("*kbdisc*").
  IF rate-zikat NE "" THEN 
  DO:    
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = rate-zikat NO-LOCK.
      curr-zikatnr = zimkateg.zikatnr. 
  END.
  ELSE
  DO:
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = curr-rmcat NO-LOCK.
      curr-zikatnr = zimkateg.zikatnr. 
  END.
 
  co-date = abreise.
  IF abreise GT ankunft THEN co-date = co-date - 1.

  DO datum = ankunft TO co-date: 
    ASSIGN
      curr-i        = curr-i + 1
      bill-date     = datum 
      argt-rate     = 0 
      daily-rate    = 0 
      fixed-rate    = NO
    . 
    
    IF datum LT ci-date THEN
    DO:
      rm-rate = ?.
      FIND FIRST genstat WHERE genstat.datum = datum
          AND genstat.resnr = inp-resnr
          AND genstat.res-int[1] = inp-reslinnr NO-LOCK NO-ERROR.
      IF AVAILABLE genstat THEN 
      DO:    
        rm-rate = genstat.zipreis.
        FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt
            NO-LOCK NO-ERROR.
      END.
    END.
    IF datum GE ci-date OR NOT AVAILABLE arrangement THEN
    FIND FIRST arrangement WHERE arrangement.arrangement 
      = curr-argt NO-LOCK.  

    IF (datum GE ci-date) OR rm-rate = ? THEN
    DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = inp-resnr 
        AND reslin-queasy.reslinnr = inp-reslinnr 
        AND datum GE reslin-queasy.date1 
        AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        fixed-rate = YES. 
        rm-rate = reslin-queasy.deci1. 
        IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
        IF reslin-queasy.char1 NE "" THEN 
        FIND FIRST arrangement WHERE arrangement.arrangement 
          = reslin-queasy.char1 NO-LOCK.  
      END. 
      IF NOT fixed-rate THEN 
      DO: 
          IF contcode NE "" THEN 
          DO: 
            FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
              = marketnr NO-LOCK NO-ERROR. 
            IF AVAILABLE queasy AND queasy.logi3 THEN 
               bill-date = ankunft. 

            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, inp-resnr, 
              inp-reslinnr, contcode, ?, bill-date, ankunft,
              abreise, marketnr, arrangement.argtnr,
              curr-zikatnr, pax, kind1, 0,
              fix-exrate, waehrung.waehrungsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
          END.    /* available guest-pr */

          IF NOT rate-found THEN
          DO: 
            w-day = wd-array[WEEKDAY(bill-date)]. 
            IF (bill-date = ci-date) OR (bill-date = ankunft) THEN 
            DO: 
              rm-rate = inp-rmrate. 
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
              IF AVAILABLE katpreis AND get-rackrate(pax,kind1, 0) = rm-rate 
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
              IF AVAILABLE katpreis AND get-rackrate(pax, kind1, 0) > 0 
              THEN 
                rm-rate = get-rackrate(pax, kind1, 0). 
            END. /* if rack-rate   */ 
            IF bonus-array[curr-i] = YES THEN rm-rate = 0.  
          END.   /* publish rate   */  
      END.       /* not fixed rate */
    END.         /* datum GE ci-date OR rm-rate = ? */

    CREATE output-list. 
    STR = STRING(datum) + "   " + translateExtended ("Roomrate",lvCAREA,"") 
      + "   = " + TRIM(STRING(rm-rate,"->>>,>>>,>>9.99")). 
    tot-rate = tot-rate + rm-rate. 
    daily-rate = rm-rate. 
 
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
      ELSE IF argt-line.vt-percnt = 1 THEN qty = kind1. 
      ELSE IF argt-line.vt-percnt = 2 THEN qty = 0. 
      IF qty GT 0 THEN 
      DO: 
        IF argt-line.fakt-modus = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 2 THEN 
        DO: 
          IF ankunft EQ datum THEN add-it = YES. 
        END. 
        ELSE IF argt-line.fakt-modus = 3 THEN 
        DO: 
          IF (ankunft + 1) EQ datum THEN add-it = YES. 
        END. 
        ELSE IF argt-line.fakt-modus = 4 AND day(datum) = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 5 
          AND day(datum + 1) = 1 THEN add-it = YES. 
        ELSE IF argt-line.fakt-modus = 6 THEN 
        DO: 
          IF (ankunft + (argt-line.intervall - 1)) GE datum 
            THEN add-it = YES. 
        END. 
      END. 
      IF add-it THEN 
      DO: 
        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
          AND artikel.departement = argt-line.departement NO-LOCK. 
        argt-rate = argt-line.betrag. 
        argt-defined = NO. 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
          AND reslin-queasy.char1 = "" 
          AND reslin-queasy.number1 = argt-line.departement 
          AND reslin-queasy.number2 = argt-line.argtnr 
          AND reslin-queasy.resnr = inp-resnr 
          AND reslin-queasy.reslinnr = inp-reslinnr 
          AND reslin-queasy.number3 = argt-line.argt-artnr 
          AND bill-date GE reslin-queasy.date1 
          AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO: 
          argt-defined = YES. 
          IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
          ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
          ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3. 
        END. 
 
        IF AVAILABLE guest-pr AND NOT argt-defined THEN 
        DO: 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
            AND reslin-queasy.char1 = contcode 
            AND reslin-queasy.number1 = marketnr 
            AND reslin-queasy.number2 = arrangement.argtnr 
            AND reslin-queasy.reslinnr = curr-zikatnr 
            AND reslin-queasy.number3 = argt-line.argt-artnr 
            AND reslin-queasy.resnr = argt-line.departement 
            AND bill-date GE reslin-queasy.date1 
            AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy THEN 
          DO: 
            IF argt-line.vt-percnt = 0 THEN argt-rate = reslin-queasy.deci1. 
            ELSE IF argt-line.vt-percnt = 1 THEN argt-rate = reslin-queasy.deci2. 
            ELSE IF argt-line.vt-percnt = 2 THEN argt-rate = reslin-queasy.deci3. 
          END. 
        END. 
        argt-rate = argt-rate * qty. 
 
        IF argt-rate NE 0 THEN
        DO:
            CREATE output-list. 
            output-list.flag = 1. 
            c = STRING(qty) + " " + artikel.bezeich. 
            STR = STRING(translateExtended ("     Incl.",lvCAREA,""),"x(10)") 
              + " " + STRING(c, "x(16)") 
              + " = " + TRIM(STRING(argt-rate,"->>>,>>>,>>9.99")).
        END.        
      END. /* IF addi-it */ 
    END.   /* each argt-line */ 
 
/**** additional fix cost ******/ 
    FOR EACH fixleist WHERE fixleist.resnr = inp-resnr 
        AND fixleist.reslinnr = inp-reslinnr NO-LOCK: 
      add-it = NO. 
      argt-rate = 0. 
      IF fixleist.sequenz = 1 THEN add-it = YES. 
      ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
      DO: 
        IF ankunft EQ datum THEN add-it = YES. 
      END. 
      ELSE IF fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
      ELSE IF fixleist.sequenz = 5 
        AND day(datum + 1) = 1 THEN add-it = YES. 
      ELSE IF fixleist.sequenz = 6 THEN 
      DO: 
        IF lfakt = ? THEN delta = 0. 
        ELSE 
        DO: 
          delta = lfakt - ankunft. 
          IF delta LT 0 THEN delta = 0. 
        END. 
        start-date = ankunft + delta. 
        IF (abreise - start-date) LT fixleist.dekade 
          THEN start-date = ankunft. 
        IF datum LE (start-date + (fixleist.dekade - 1)) THEN add-it = YES. 
        IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
      END. 
      IF add-it THEN 
      DO: 
        FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
          AND artikel.departement = fixleist.departement NO-LOCK. 
        argt-rate = fixleist.betrag * fixleist.number. 
      END. 
      IF argt-rate NE 0 THEN 
      DO: 
        create output-list. 
        STR = STRING("","x(8)") + "   " + STRING(artikel.bezeich, "x(16)") 
          + " = " + TRIM(STRING(argt-rate,"->>>,>>>,>>9.99")). 
        tot-rate = tot-rate + argt-rate. 
        daily-rate = daily-rate + argt-rate. 
      END. 
    END. 
    STR = STR + "  Total = " + TRIM(STRING(daily-rate,"->>>,>>>,>>9.99")). 
  END. 
 
  CREATE output-list. 
  ASSIGN 
    STR = "  " + translateExtended ("Expected total revenue    =",lvCAREA,"") 
      + " " + TRIM(STRING(tot-rate,"->,>>>,>>>,>>9.99")) 
    str1 = "expected". 
 
END. 
 */

RUN view-staycostbl.p  
    (pvILanguage, inp-resnr, inp-reslinnr, contcode, OUTPUT TABLE output-list).
