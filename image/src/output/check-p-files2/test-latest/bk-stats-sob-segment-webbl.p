DEFINE TEMP-TABLE bk-statistic-list
    FIELD CODE    AS INTEGER FORMAT ">>>" INITIAL 0
    FIELD bezeich AS CHARACTER FORMAT "x(32)"
    FIELD dgroom  AS INTEGER FORMAT ">>>9" INITIAL 0
    FIELD proz1   AS DECIMAL FORMAT ">>9.99" 
    FIELD mgroom  AS INTEGER FORMAT ">>9" INITIAL 0
    FIELD proz2   AS DECIMAL FORMAT ">>9.99" 
    FIELD ygroom  AS INTEGER FORMAT ">>9" INITIAL 0
    FIELD proz3   AS DECIMAL FORMAT ">>9.99"
    FIELD dpax    AS INTEGER FORMAT ">>9" INITIAL 0
    FIELD mpax    AS INTEGER FORMAT ">>>9" INITIAL 0
    FIELD ypax    AS INTEGER FORMAT ">>>9" INITIAL 0
    FIELD drev    AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD mrev    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD yrev    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD d-fbrev AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD m-fbrev AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD y-fbrev AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD dorev   AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD morev   AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD yorev   AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    .

DEFINE TEMP-TABLE input-payload
    FIELD disp-flag AS INTEGER
    FIELD to-date   AS CHARACTER
    .

DEFINE INPUT PARAMETER TABLE FOR input-payload.
DEFINE OUTPUT PARAMETER TABLE FOR bk-statistic-list.

DEFINE VARIABLE from-date     AS DATE.
DEFINE VARIABLE fb-rev        AS DECIMAL INIT 0.
DEFINE VARIABLE other-rev     AS DECIMAL INIT 0.
DEFINE VARIABLE tot-dgroom    AS INTEGER INIT 0.
DEFINE VARIABLE tot-mgroom    AS INTEGER INIT 0.
DEFINE VARIABLE tot-ygroom    AS INTEGER INIT 0.
DEFINE VARIABLE tot-dpax      AS INTEGER INIT 0.
DEFINE VARIABLE tot-mpax      AS INTEGER INIT 0.
DEFINE VARIABLE tot-ypax      AS INTEGER INIT 0.
DEFINE VARIABLE tot-drev      AS DECIMAL INIT 0.
DEFINE VARIABLE tot-mrev      AS DECIMAL INIT 0.
DEFINE VARIABLE tot-yrev      AS DECIMAL INIT 0.
DEFINE VARIABLE tot-d-fbrev   AS DECIMAL INIT 0.
DEFINE VARIABLE tot-m-fbrev   AS DECIMAL INIT 0.
DEFINE VARIABLE tot-y-fbrev   AS DECIMAL INIT 0.
DEFINE VARIABLE tot-dorev     AS DECIMAL INIT 0.
DEFINE VARIABLE tot-morev     AS DECIMAL INIT 0.
DEFINE VARIABLE tot-yorev     AS DECIMAL INIT 0.


FIND FIRST input-payload NO-LOCK NO-ERROR.

IF input-payload.disp-flag EQ 0 THEN RUN create-list.
ELSE RUN create-list1.


PROCEDURE create-list:
    FOR EACH bk-statistic-list:
        DELETE bk-statistic-list.
    END.

    from-date = DATE(1,1,YEAR(DATE(input-payload.to-date))).

    FOR EACH bk-func WHERE bk-func.datum GE from-date 
        AND bk-func.datum LE DATE(input-payload.to-date) USE-INDEX datum_ix NO-LOCK,
        FIRST bk-veran WHERE bk-veran.veran-nr EQ bk-func.veran-nr NO-LOCK
        BY bk-veran.segmentcode:

        FIND FIRST bk-statistic-list WHERE bk-statistic-list.CODE EQ bk-veran.segmentcode NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bk-statistic-list THEN
        DO:
            CREATE bk-statistic-list.

            ASSIGN bk-statistic-list.CODE = bk-veran.segmentcode.

            FIND FIRST queasy WHERE queasy.KEY EQ 146 AND queasy.char1 EQ STRING(bk-veran.segmentcode) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN ASSIGN bk-statistic-list.bezeich = queasy.char3.
            ELSE ASSIGN bk-statistic-list.bezeich = "Unknown".
            
            fb-rev = 0.
            other-rev = 0.
        END.

        FOR EACH bk-rart WHERE bk-rart.veran-nr EQ bk-func.veran-nr 
            AND bk-rart.veran-seite EQ bk-func.veran-seite NO-LOCK,
            FIRST artikel WHERE artikel.artnr EQ bk-rart.veran-artnr
            AND artikel.departement EQ bk-rart.departement NO-LOCK:

            IF artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 6 THEN
            DO:
                fb-rev = fb-rev + (bk-rart.preis * bk-rart.anzahl).
            END.
            ELSE IF artikel.umsatzart EQ 4 THEN other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
        END.

        IF bk-func.datum EQ DATE(input-payload.to-date) THEN
        DO:
            ASSIGN
                bk-statistic-list.dgroom  = bk-statistic-list.dgroom + 1
                bk-statistic-list.dpax    = bk-statistic-list.dpax + bk-func.rpersonen[1]
                bk-statistic-list.drev    = bk-statistic-list.drev + bk-func.rpreis[1]
                bk-statistic-list.d-fbrev = bk-statistic-list.d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                bk-statistic-list.dorev   = bk-statistic-list.dorev + other-rev
                tot-dgroom                = tot-dgroom + 1
                tot-dpax                  = tot-dpax + bk-func.rpersonen[1]
                tot-drev                  = tot-drev + bk-func.rpreis[1]
                tot-d-fbrev               = tot-d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-dorev                 = tot-dorev + other-rev
                .
        END.
        ELSE IF MONTH(bk-func.datum) EQ MONTH(DATE(input-payload.to-date)) THEN
        DO:
            ASSIGN
                bk-statistic-list.mgroom  = bk-statistic-list.mgroom + 1
                bk-statistic-list.mpax    = bk-statistic-list.mpax + bk-func.rpersonen[1]
                bk-statistic-list.mrev    = bk-statistic-list.mrev + bk-func.rpreis[1]
                bk-statistic-list.m-fbrev = bk-statistic-list.m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                bk-statistic-list.morev   = bk-statistic-list.morev + other-rev
                tot-mgroom                = tot-mgroom + 1
                tot-mpax                  = tot-mpax + bk-func.rpersonen[1]
                tot-mrev                  = tot-mrev + bk-func.rpreis[1]
                tot-m-fbrev               = tot-m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-morev                 = tot-morev + other-rev
                .
        END.

        ASSIGN
            bk-statistic-list.ygroom  = bk-statistic-list.ygroom + 1
            bk-statistic-list.ypax    = bk-statistic-list.ypax + bk-func.rpersonen[1]
            bk-statistic-list.yrev    = bk-statistic-list.yrev + bk-func.rpreis[1]
            bk-statistic-list.y-fbrev = bk-statistic-list.y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            bk-statistic-list.yorev   = bk-statistic-list.yorev + other-rev
            tot-ygroom                = tot-ygroom + 1
            tot-ypax                  = tot-ypax + bk-func.rpersonen[1]
            tot-yrev                  = tot-yrev + bk-func.rpreis[1]
            tot-y-fbrev               = tot-y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            tot-yorev                 = tot-yorev + other-rev
            .
    END.

    FOR EACH bk-statistic-list:
        ASSIGN 
            bk-statistic-list.proz1 = 100.0 * (bk-statistic-list.dgroom / tot-dgroom)
            bk-statistic-list.proz2 = 100.0 * (bk-statistic-list.mgroom / tot-mgroom)
            bk-statistic-list.proz3 = 100.0 * (bk-statistic-list.ygroom / tot-ygroom)
            .
    END.

    CREATE bk-statistic-list.
    ASSIGN
        bk-statistic-list.bezeich = "T O T A L"
        bk-statistic-list.dgroom  = tot-dgroom
        bk-statistic-list.proz1   = 100.00
        bk-statistic-list.mgroom  = tot-mgroom
        bk-statistic-list.proz2   = 100.00
        bk-statistic-list.ygroom  = tot-ygroom
        bk-statistic-list.proz3   = 100.00
        bk-statistic-list.dpax    = tot-dpax
        bk-statistic-list.mpax    = tot-mpax
        bk-statistic-list.ypax    = tot-ypax
        bk-statistic-list.drev    = tot-drev
        bk-statistic-list.mrev    = tot-mrev
        bk-statistic-list.yrev    = tot-yrev
        bk-statistic-list.d-fbrev = tot-d-fbrev
        bk-statistic-list.m-fbrev = tot-m-fbrev
        bk-statistic-list.y-fbrev = tot-y-fbrev
        bk-statistic-list.dorev   = tot-dorev
        bk-statistic-list.morev   = tot-morev
        bk-statistic-list.yorev   = tot-yorev
        .

    IF tot-dgroom EQ 0 THEN
        ASSIGN bk-statistic-list.proz1 = 0.
    IF tot-mgroom EQ 0 THEN
        ASSIGN bk-statistic-list.proz2 = 0.
    IF tot-ygroom EQ 0 THEN
        ASSIGN bk-statistic-list.proz3 = 0.
END.

PROCEDURE create-list1:
    FOR EACH bk-statistic-list:
        DELETE bk-statistic-list.
    END.

    from-date = DATE(1,1,YEAR(DATE(input-payload.to-date))).

    FOR EACH bk-func WHERE bk-func.datum GE from-date 
        AND bk-func.datum LE DATE(input-payload.to-date) USE-INDEX datum_ix NO-LOCK
        BY bk-func.technik[2]:

        FIND FIRST bk-statistic-list WHERE bk-statistic-list.CODE EQ INT(bk-func.technik[2]) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bk-statistic-list THEN
        DO:
            CREATE bk-statistic-list.

            ASSIGN bk-statistic-list.CODE = INT(bk-func.technik[2]).

            FIND FIRST queasy WHERE queasy.KEY EQ 151 AND queasy.char1 EQ STRING(bk-func.technik[2]) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN ASSIGN bk-statistic-list.bezeich = queasy.char3.
            ELSE ASSIGN bk-statistic-list.bezeich = "Unknown".
            
            fb-rev = 0.
            other-rev = 0.
        END.

        FOR EACH bk-rart WHERE bk-rart.veran-nr EQ bk-func.veran-nr 
            AND bk-rart.veran-seite EQ bk-func.veran-seite NO-LOCK,
            FIRST artikel WHERE artikel.artnr EQ bk-rart.veran-artnr
            AND artikel.departement EQ bk-rart.departement NO-LOCK:

            IF artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 6 THEN
            DO:
                fb-rev = fb-rev + (bk-rart.preis * bk-rart.anzahl).
            END.
            ELSE IF artikel.umsatzart EQ 4 THEN other-rev = other-rev + (bk-rart.preis * bk-rart.anzahl).
        END.

        IF bk-func.datum EQ DATE(input-payload.to-date) THEN
        DO:
            ASSIGN
                bk-statistic-list.dgroom  = bk-statistic-list.dgroom + 1
                bk-statistic-list.dpax    = bk-statistic-list.dpax + bk-func.rpersonen[1]
                bk-statistic-list.drev    = bk-statistic-list.drev + bk-func.rpreis[1]
                bk-statistic-list.d-fbrev = bk-statistic-list.d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                bk-statistic-list.dorev   = bk-statistic-list.dorev + other-rev
                tot-dgroom                = tot-dgroom + 1
                tot-dpax                  = tot-dpax + bk-func.rpersonen[1]
                tot-drev                  = tot-drev + bk-func.rpreis[1]
                tot-d-fbrev               = tot-d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-dorev                 = tot-dorev + other-rev
                .
        END.
        ELSE IF MONTH(bk-func.datum) EQ MONTH(DATE(input-payload.to-date)) THEN
        DO:
            ASSIGN
                bk-statistic-list.mgroom  = bk-statistic-list.mgroom + 1
                bk-statistic-list.mpax    = bk-statistic-list.mpax + bk-func.rpersonen[1]
                bk-statistic-list.mrev    = bk-statistic-list.mrev + bk-func.rpreis[1]
                bk-statistic-list.m-fbrev = bk-statistic-list.m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                bk-statistic-list.morev   = bk-statistic-list.morev + other-rev
                tot-mgroom                = tot-mgroom + 1
                tot-mpax                  = tot-mpax + bk-func.rpersonen[1]
                tot-mrev                  = tot-mrev + bk-func.rpreis[1]
                tot-m-fbrev               = tot-m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-morev                 = tot-morev + other-rev
                .
        END.

        ASSIGN
            bk-statistic-list.ygroom  = bk-statistic-list.ygroom + 1
            bk-statistic-list.ypax    = bk-statistic-list.ypax + bk-func.rpersonen[1]
            bk-statistic-list.yrev    = bk-statistic-list.yrev + bk-func.rpreis[1]
            bk-statistic-list.y-fbrev = bk-statistic-list.y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            bk-statistic-list.yorev   = bk-statistic-list.yorev + other-rev
            tot-ygroom                = tot-ygroom + 1
            tot-ypax                  = tot-ypax + bk-func.rpersonen[1]
            tot-yrev                  = tot-yrev + bk-func.rpreis[1]
            tot-y-fbrev               = tot-y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            tot-yorev                 = tot-yorev + other-rev
            .
    END.

    FOR EACH bk-statistic-list:
        ASSIGN 
            bk-statistic-list.proz1 = 100.0 * (bk-statistic-list.dgroom / tot-dgroom)
            bk-statistic-list.proz2 = 100.0 * (bk-statistic-list.mgroom / tot-mgroom)
            bk-statistic-list.proz3 = 100.0 * (bk-statistic-list.ygroom / tot-ygroom)
            .
    END.

    CREATE bk-statistic-list.
    ASSIGN
        bk-statistic-list.bezeich = "T O T A L"
        bk-statistic-list.dgroom  = tot-dgroom
        bk-statistic-list.proz1   = 100.00
        bk-statistic-list.mgroom  = tot-mgroom
        bk-statistic-list.proz2   = 100.00
        bk-statistic-list.ygroom  = tot-ygroom
        bk-statistic-list.proz3   = 100.00
        bk-statistic-list.dpax    = tot-dpax
        bk-statistic-list.mpax    = tot-mpax
        bk-statistic-list.ypax    = tot-ypax
        bk-statistic-list.drev    = tot-drev
        bk-statistic-list.mrev    = tot-mrev
        bk-statistic-list.yrev    = tot-yrev
        bk-statistic-list.d-fbrev = tot-d-fbrev
        bk-statistic-list.m-fbrev = tot-m-fbrev
        bk-statistic-list.y-fbrev = tot-y-fbrev
        bk-statistic-list.dorev   = tot-dorev
        bk-statistic-list.morev   = tot-morev
        bk-statistic-list.yorev   = tot-yorev
        .

    IF tot-dgroom EQ 0 THEN
        ASSIGN bk-statistic-list.proz1 = 0.
    IF tot-mgroom EQ 0 THEN
        ASSIGN bk-statistic-list.proz2 = 0.
    IF tot-ygroom EQ 0 THEN
        ASSIGN bk-statistic-list.proz3 = 0.
END.
