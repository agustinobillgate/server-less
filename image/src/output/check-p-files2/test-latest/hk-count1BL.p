DEFINE INPUT  PARAMETER AswaitTime                   AS INTEGER. /*ITA*/
DEFINE INPUT  PARAMETER price-decimal                AS INTEGER.
DEFINE OUTPUT PARAMETER arrived1                     AS INTEGER.
DEFINE OUTPUT PARAMETER arrived2                     AS INTEGER.
DEFINE OUTPUT PARAMETER arriving1                    AS INTEGER.
DEFINE OUTPUT PARAMETER arriving2                    AS INTEGER.
DEFINE OUTPUT PARAMETER tot-arrive1                  AS INTEGER.
DEFINE OUTPUT PARAMETER tot-arrive2                  AS INTEGER.
DEFINE OUTPUT PARAMETER avrg-rate1                   AS DECIMAL.
DEFINE OUTPUT PARAMETER avrg-rate2                   AS DECIMAL.
DEFINE OUTPUT PARAMETER rm-rate                      AS DECIMAL.
DEFINE OUTPUT PARAMETER departed1                    AS INTEGER.
DEFINE OUTPUT PARAMETER departed2                    AS INTEGER.
DEFINE OUTPUT PARAMETER departing1                   AS INTEGER.
DEFINE OUTPUT PARAMETER departing2                   AS INTEGER.
DEFINE OUTPUT PARAMETER tot-depart1                  AS INTEGER.
DEFINE OUTPUT PARAMETER tot-depart2                  AS INTEGER.
DEFINE OUTPUT PARAMETER vclean                       AS INTEGER. 
DEFINE OUTPUT PARAMETER vuncheck                     AS INTEGER. 
DEFINE OUTPUT PARAMETER oclean                       AS INTEGER.
DEFINE OUTPUT PARAMETER odirty                       AS INTEGER.
DEFINE OUTPUT PARAMETER vdirty                       AS INTEGER. 
DEFINE OUTPUT PARAMETER atoday                       AS INTEGER. 
DEFINE OUTPUT PARAMETER oroom1                       AS INTEGER. 
DEFINE OUTPUT PARAMETER oroom2                       AS INTEGER. 
DEFINE OUTPUT PARAMETER oooroom1                     AS INTEGER.
DEFINE OUTPUT PARAMETER oooroom2                     AS INTEGER.
DEFINE OUTPUT PARAMETER compRoom1                    AS INTEGER. 
DEFINE OUTPUT PARAMETER compRoom2                    AS INTEGER.
DEFINE OUTPUT PARAMETER houseRoom1                   AS INTEGER. 
DEFINE OUTPUT PARAMETER houseRoom2                   AS INTEGER.
DEFINE OUTPUT PARAMETER iroom1                       AS INTEGER. 
DEFINE OUTPUT PARAMETER iroom2                       AS INTEGER.
DEFINE OUTPUT PARAMETER eocc1                        AS INTEGER. 
DEFINE OUTPUT PARAMETER eocc2                        AS INTEGER.
DEFINE OUTPUT PARAMETER tot-zimmer                   AS INTEGER.
DEFINE OUTPUT PARAMETER expired-id                   AS INTEGER. /*ITA*/
DEFINE OUTPUT PARAMETER user-wig                     AS LOGICAL. /*ITA*/

DEFINE VARIABLE uhr                                  AS INTEGER INITIAL -100. 
DEFINE VARIABLE uhr-str                              AS CHAR FONT 1 FGCOLOR 9. 
DEFINE VARIABLE pvLStopped                           AS LOGICAL INITIAL false NO-UNDO. 
DEFINE VARIABLE curr-time                            AS INTEGER. 
DEFINE VARIABLE min-unit                             AS INTEGER FORMAT "9  " INITIAL 1. 
DEFINE VARIABLE occ-rm1                              AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE VARIABLE occ-rm2                              AS INTEGER INITIAL 0 NO-UNDO. 

RUN init-var.
RUN expiredid-countbl.p(AswaitTime,OUTPUT expired-id, OUTPUT user-wig).

PROCEDURE init-var: 
DEFINE VARIABLE ci-date AS DATE                     NO-UNDO. 
DEFINE VARIABLE rm-active AS LOGICAL                NO-UNDO. 
 
    ASSIGN 
        departed1   = 0 
        departed2   = 0 
        departing1  = 0 
        departing2  = 0 
        arrived1    = 0 
        arrived2    = 0 
        arriving1   = 0 
        arriving2   = 0 
        vclean      = 0 
        vuncheck    = 0 
        oclean      = 0 
        vdirty      = 0 
        odirty      = 0 
        atoday      = 0 
        oroom1      = 0 
        oroom2      = 0 
        oooroom1    = 0 
        oooroom2    = 0 
        iroom1      = 0 
        iroom2      = 0 
        eocc1       = 0 
        eocc2       = 0 
        houseRoom1  = 0 
        houseRoom2  = 0 
        compRoom1   = 0 
        compRoom2   = 0 
        tot-zimmer  = 0 
 
        occ-rm1     = 0 
        occ-rm2     = 0 
        rm-rate     = 0 
        avrg-rate1  = 0 
        . 

    FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
    ci-date = htparam.fdate. 
    /*CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait").
      PROCESS EVENTS. */ 
 
    /* departing guests */ 
    FOR EACH res-line NO-LOCK WHERE 
            res-line.active-flag    = 1         AND 
            res-line.resstatus      NE 12       AND 
            res-line.ankunft        LE ci-date  AND 
            res-line.abreise        = ci-date   AND
            res-line.l-zuordnung[3] = 0, 
        FIRST zimmer NO-LOCK WHERE 
            zimmer.zinr             = res-line.zinr 
        /* AND zimmer.sleeping         EQ TRUE */ : 
        IF res-line.resstatus = 6 THEN ASSIGN 
            departing1 = departing1 + 1. 
        departing2 = departing2 + res-line.erwachs + res-line.gratis 
          + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
    END. 
 
    /* resident guest OF active rooms */ 
    FOR EACH res-line NO-LOCK WHERE 
        res-line.active-flag EQ 1               AND 
            res-line.resstatus      NE 12       AND 
            res-line.ankunft        LE ci-date  AND 
            res-line.abreise        GE ci-date  AND
            res-line.l-zuordnung[3] = 0, 
        FIRST zimmer NO-LOCK WHERE 
            zimmer.zinr             = res-line.zinr, 
        FIRST reservation NO-LOCK WHERE 
            reservation.resnr         = res-line.resnr:
        FIND FIRST segment WHERE 
            segment.segmentcode     = reservation.segmentcode NO-LOCK NO-ERROR . 
        IF ((res-line.abreise GT ci-date) OR 
            (res-line.ankunft = ci-date AND res-line.abreise = ci-date 
            AND res-line.zipreis GT 0)) THEN 
        DO: 
            IF res-line.resstatus = 6 AND zimmer.sleeping THEN 
            DO:
              ASSIGN 
                occ-rm2     = occ-rm2 + 1
                oroom1    = oroom1 + 1 
                eocc1     = eocc1 + 1 
                oroom2 = oroom2 + res-line.erwachs + res-line.gratis 
                  + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                eocc2 = eocc2 + res-line.erwachs + res-line.gratis 
                  + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]
              .
              IF res-line.zipreis GT 0 THEN occ-rm1 = occ-rm1 + 1.
            END.
            RUN cal-local-rmrate. 
        END. 
        IF res-line.ankunft = ci-date THEN DO: 
            IF res-line.resstatus = 6 THEN 
                arrived1 = arrived1 + 1. 
            arrived2 = arrived2 + (res-line.erwachs + res-line.gratis) 
               + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
        END. 
        IF AVAILABLE segment THEN
        DO:
            IF segment.betriebsnr EQ 2 THEN DO: 
                IF res-line.resstatus = 6 THEN ASSIGN 
                    houseRoom1 = houseRoom1 + 1. 
                houseRoom2 = houseRoom2 + res-line.erwachs + res-line.gratis 
                    + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
            END. 
            ELSE IF segment.betriebsnr EQ 1 OR res-line.gratis GT 0 THEN DO: 
                IF res-line.resstatus = 6 THEN ASSIGN 
                    compRoom1 = compRoom1 + 1. 
                compRoom2 = compRoom2 + res-line.erwachs + res-line.gratis 
                    + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
            END. 
        END.
        IF NOT zimmer.sleeping THEN 
            iroom2 = iroom2 + res-line.erwachs + res-line.gratis 
            + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
    END. 
 
    /* today departed guests */ 
    FOR EACH res-line NO-LOCK WHERE 
            res-line.active-flag    = 2             AND 
            res-line.resstatus      = 8             AND 
            res-line.ankunft        LE ci-date      AND 
            res-line.abreise        EQ ci-date      AND
            res-line.l-zuordnung[3] EQ 0,            
        FIRST zimmer NO-LOCK WHERE 
            zimmer.zinr             = res-line.zinr 
        /*  AND zimmer.sleeping         = TRUE */ : 
        IF NOT res-line.zimmerfix THEN departed1 = departed1 + 1.
        ASSIGN 
            departed2 = departed2 + res-line.erwachs + res-line.gratis 
              + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
 
    END. 
    ASSIGN 
        tot-depart1 = departed1 + departing1 
        tot-depart2 = departed2 + departing2. 
 
    /* arriving guests OF active rooms */ 
    FOR EACH res-line NO-LOCK WHERE 
            res-line.active-flag    = 0             AND 
            res-line.ankunft        = ci-date       AND
            res-line.l-zuordnung[3] = 0:
        FIND FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr NO-LOCK NO-ERROR. 
        rm-active = YES. 
        IF (AVAILABLE zimmer AND NOT zimmer.sleeping) THEN 
            rm-active = NO. 
 
        IF (resstatus = 1 OR resstatus = 2 OR resstatus = 5) THEN 
        DO: 
            arriving1 = arriving1 + res-line.zimmeranz. 
            IF rm-active THEN 
            DO: 
              ASSIGN
                eocc1 = eocc1 + res-line.zimmeranz
                occ-rm2 = occ-rm2 + res-line.zimmeranz
              . 
             IF res-line.zipreis GT 0 THEN occ-rm1 = occ-rm1 + res-line.zimmeranz. 
            END.
        END.
        IF (res-line.resstatus = 1 OR res-line.resstatus = 2 
            OR res-line.resstatus = 5 
            OR res-line.resstatus = 11) THEN 
        DO: 
            arriving2 = arriving2 + res-line.zimmeranz 
              * (res-line.erwachs + res-line.gratis 
               + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]). 
            IF rm-active THEN 
            DO: 
                eocc2 = eocc2 + res-line.zimmeranz 
                  * (res-line.erwachs + res-line.gratis 
                   + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]). 
              RUN cal-local-rmrate. 
            END. 
        END. 
    END. 
 
    ASSIGN
      avrg-rate1 = rm-rate / occ-rm1
      avrg-rate2 = rm-rate / occ-rm2
    . 
 
    tot-arrive1 = arrived1 + arriving1. 
    tot-arrive2 = arrived2 + arriving2. 
 
    FOR EACH zimmer NO-LOCK, 
        FIRST zimkateg NO-LOCK WHERE 
            zimkateg.zikatnr    = zimmer.zikatnr: 
        IF zimkateg.verfuegbarkeit THEN DO: 
            IF (zimmer.zistatus = 0 OR zimmer.zistatus = 1 
                OR zimmer.zistatus = 5) THEN 
            DO: 
                IF zimmer.zistatus = 0 THEN vclean = vclean + 1. 
                ELSE IF zimmer.zistatus = 1 THEN vuncheck = vuncheck + 1. 
                ELSE IF zimmer.zistatus = 5 THEN oclean = oclean + 1. 
            END. 
            ELSE IF (zimmer.zistatus = 2 OR zimmer.zistatus = 3 
                OR zimmer.zistatus = 4) THEN DO: 
                IF zimmer.zistatus = 2 THEN vdirty = vdirty + 1. 
                ELSE IF zimmer.zistatus = 4 THEN odirty = odirty + 1. 
                ELSE IF zimmer.zistatus = 3 THEN atoday = atoday + 1. 
            END. 
            ELSE IF zimmer.zistatus = 6 THEN oooroom1 = oooroom1 + 1. 
            IF NOT zimmer.sleeping THEN iroom1 = iroom1 + 1. 
            IF zimmer.sleeping THEN tot-zimmer = tot-zimmer + 1. 
        END. 
    END. 
END. 

PROCEDURE cal-local-rmrate: 
DEFINE VARIABLE frate AS DECIMAL INITIAL 1 NO-UNDO. 
DEFINE VARIABLE Rate  AS DECIMAL NO-UNDO.

  IF res-line.zipreis = 0 THEN RETURN. 
  IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
  ELSE 
  DO: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN frate = waehrung.ankauf / waehrung.einheit. 
  END. 
  rm-rate = rm-rate + ROUND(res-line.zipreis * frate, price-decimal)
      * res-line.zimmeranz. 
END. 

