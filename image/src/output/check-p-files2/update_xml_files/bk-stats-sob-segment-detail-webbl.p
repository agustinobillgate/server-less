DEFINE TEMP-TABLE t-list                         
    FIELD CODE           AS INTEGER FORMAT ">>>"   INITIAL 0
    FIELD veran-nr       AS INTEGER FORMAT ">,>>9" INITIAL 0
    FIELD gastnr         AS INTEGER FORMAT ">,>>9" INITIAL 0
    FIELD bestellt_durch AS CHARACTER FORMAT "x(32)"
    FIELD dgroom         AS INTEGER FORMAT ">>>9"  INITIAL 0
    FIELD mgroom         AS INTEGER FORMAT ">>>9"  INITIAL 0
    FIELD ygroom         AS INTEGER FORMAT ">>>9"  INITIAL 0
    FIELD drev           AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD mrev           AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD yrev           AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD d-fbrev        AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD m-fbrev        AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD y-fbrev        AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD dorev          AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD morev          AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD yorev          AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    .

DEFINE TEMP-TABLE input-payload
    FIELD disp-flag AS INTEGER
    FIELD CODE      AS INTEGER
    FIELD to-date   AS CHARACTER
    .

DEFINE INPUT PARAMETER TABLE FOR input-payload.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE from-date     AS DATE.          
DEFINE VARIABLE fb-rev        AS DECIMAL INIT 0.
DEFINE VARIABLE other-rev     AS DECIMAL INIT 0.
DEFINE VARIABLE tot-dgroom    AS INTEGER INIT 0.
DEFINE VARIABLE tot-mgroom    AS INTEGER INIT 0.
DEFINE VARIABLE tot-ygroom    AS INTEGER INIT 0.
DEFINE VARIABLE tot-drev      AS DECIMAL INIT 0.
DEFINE VARIABLE tot-mrev      AS DECIMAL INIT 0.
DEFINE VARIABLE tot-yrev      AS DECIMAL INIT 0.
DEFINE VARIABLE tot-d-fbrev   AS DECIMAL INIT 0.
DEFINE VARIABLE tot-m-fbrev   AS DECIMAL INIT 0.
DEFINE VARIABLE tot-y-fbrev   AS DECIMAL INIT 0.
DEFINE VARIABLE tot-dorev     AS DECIMAL INIT 0.
DEFINE VARIABLE tot-morev     AS DECIMAL INIT 0.
DEFINE VARIABLE tot-yorev     AS DECIMAL INIT 0.

/* DEFINE VARIABLE disp-flag AS INTEGER INIT 1.   */
/* DEFINE VARIABLE CODE AS INTEGER INIT 1.        */
/* DEFINE VARIABLE to-date AS DATE INIT 01/31/19. */

FIND FIRST input-payload NO-LOCK NO-ERROR.

IF input-payload.disp-flag EQ 0 THEN RUN create-list.
ELSE RUN create-list1.


PROCEDURE create-list:
    FOR EACH t-list:
        DELETE t-list.
    END.

    from-date = DATE(1,1,YEAR(DATE(input-payload.to-date))).

    FOR EACH bk-func WHERE bk-func.datum GE from-date 
        AND bk-func.datum LE DATE(input-payload.to-date) USE-INDEX datum_ix NO-LOCK,
        FIRST bk-veran WHERE bk-veran.veran-nr EQ bk-func.veran-nr
        AND bk-veran.segmentcode EQ input-payload.CODE NO-LOCK:

        FIND FIRST t-list WHERE t-list.veran-nr EQ bk-veran.veran-nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-list THEN
        DO:
            CREATE t-list.

            ASSIGN
                t-list.CODE           = bk-veran.segmentcode
                t-list.veran-nr       = bk-veran.veran-nr
                t-list.bestellt_durch = bk-func.bestellt_durch
                t-list.gastnr         = bk-veran.gastnr
                .
            
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
                t-list.dgroom  = t-list.dgroom + 1
                t-list.drev    = t-list.drev + bk-func.rpreis[1]
                t-list.d-fbrev = t-list.d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                t-list.dorev   = t-list.dorev + other-rev
                tot-dgroom     = tot-dgroom + 1
                tot-drev       = tot-drev + bk-func.rpreis[1]
                tot-d-fbrev    = tot-d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-dorev      = tot-dorev + other-rev
                .
        END.
        ELSE IF MONTH(bk-func.datum) EQ MONTH(DATE(input-payload.to-date)) THEN
        DO:
            ASSIGN
                t-list.mgroom  = t-list.mgroom + 1
                t-list.mrev    = t-list.mrev + bk-func.rpreis[1]
                t-list.m-fbrev = t-list.m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                t-list.morev   = t-list.morev + other-rev
                tot-mgroom     = tot-mgroom + 1
                tot-mrev       = tot-mrev + bk-func.rpreis[1]
                tot-m-fbrev    = tot-m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-morev      = tot-morev + other-rev
                .
        END.

        ASSIGN
            t-list.ygroom  = t-list.ygroom + 1
            t-list.yrev    = t-list.yrev + bk-func.rpreis[1]
            t-list.y-fbrev = t-list.y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            t-list.yorev   = t-list.yorev + other-rev
            tot-ygroom     = tot-ygroom + 1
            tot-yrev       = tot-yrev + bk-func.rpreis[1]
            tot-y-fbrev    = tot-y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            tot-yorev      = tot-yorev + other-rev
            .
    END.
    
    CREATE t-list.
    ASSIGN
        t-list.bestellt_durch = "T O T A L"
        t-list.dgroom         = tot-dgroom
        t-list.mgroom         = tot-mgroom
        t-list.ygroom         = tot-ygroom
        t-list.drev           = tot-drev
        t-list.mrev           = tot-mrev
        t-list.yrev           = tot-yrev
        t-list.d-fbrev        = tot-d-fbrev
        t-list.m-fbrev        = tot-m-fbrev
        t-list.y-fbrev        = tot-y-fbrev
        t-list.dorev          = tot-dorev
        t-list.morev          = tot-morev
        t-list.yorev          = tot-yorev
        .
END.

PROCEDURE create-list1:
    FOR EACH t-list:
        DELETE t-list.
    END.

    from-date = DATE(1,1,YEAR(DATE(input-payload.to-date))).

    FOR EACH bk-func WHERE bk-func.datum GE from-date 
        AND bk-func.datum LE DATE(input-payload.to-date)
        AND bk-func.technik[2] EQ STRING(input-payload.CODE) NO-LOCK
        BY bk-func.datum:

        FIND FIRST t-list WHERE t-list.veran-nr EQ bk-func.veran-nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-list THEN
        DO:
            CREATE t-list.

            ASSIGN
                t-list.CODE           = INT(bk-func.technik[2])
                t-list.veran          = bk-func.veran-nr
                t-list.bestellt_durch = bk-func.bestellt_durch
                .

            FIND FIRST bk-veran WHERE bk-veran.veran-nr EQ bk-func.veran-nr NO-LOCK NO-ERROR.
            IF AVAILABLE bk-veran THEN ASSIGN t-list.gastnr = bk-veran.gastnr.
            
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
                t-list.dgroom  = t-list.dgroom + 1
                t-list.drev    = t-list.drev + bk-func.rpreis[1]
                t-list.d-fbrev = t-list.d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                t-list.dorev   = t-list.dorev + other-rev
                tot-dgroom     = tot-dgroom + 1
                tot-drev       = tot-drev + bk-func.rpreis[1]
                tot-d-fbrev    = tot-d-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-dorev      = tot-dorev + other-rev
                .
        END.
        ELSE IF MONTH(bk-func.datum) EQ MONTH(DATE(input-payload.to-date)) THEN
        DO:
            ASSIGN
                t-list.mgroom  = t-list.mgroom + 1
                t-list.mrev    = t-list.mrev + bk-func.rpreis[1]
                t-list.m-fbrev = t-list.m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                t-list.morev   = t-list.morev + other-rev
                tot-mgroom     = tot-mgroom + 1
                tot-mrev       = tot-mrev + bk-func.rpreis[1]
                tot-m-fbrev    = tot-m-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
                tot-morev      = tot-morev + other-rev
                .
        END.

        ASSIGN
            t-list.ygroom  = t-list.ygroom + 1
            t-list.yrev    = t-list.yrev + bk-func.rpreis[1]
            t-list.y-fbrev = t-list.y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            t-list.yorev   = t-list.yorev + other-rev
            tot-ygroom     = tot-ygroom + 1
            tot-yrev       = tot-yrev + bk-func.rpreis[1]
            tot-y-fbrev    = tot-y-fbrev + ((bk-func.rpreis[7] * bk-func.rpersonen[1]) + fb-rev)
            tot-yorev      = tot-yorev + other-rev
            .
    END.
    
    CREATE t-list.
    ASSIGN
        t-list.bestellt_durch = "T O T A L"
        t-list.dgroom         = tot-dgroom
        t-list.mgroom         = tot-mgroom
        t-list.ygroom         = tot-ygroom
        t-list.drev           = tot-drev
        t-list.mrev           = tot-mrev
        t-list.yrev           = tot-yrev
        t-list.d-fbrev        = tot-d-fbrev
        t-list.m-fbrev        = tot-m-fbrev
        t-list.y-fbrev        = tot-y-fbrev
        t-list.dorev          = tot-dorev
        t-list.morev          = tot-morev
        t-list.yorev          = tot-yorev
        .
END.
