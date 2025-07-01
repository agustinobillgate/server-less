DEFINE TEMP-TABLE t-list
    FIELD resnr AS INT
    FIELD reslinnr AS INT
    FIELD logis-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
    FIELD bfast-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
    FIELD lunch-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
    FIELD dinner-guaranteed AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
    FIELD misc-guaranteed   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
    FIELD pax-guaranteed    AS INT
    FIELD room-guaranteed   AS INT

    FIELD logis-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD bfast-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD lunch-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD dinner-tentative  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD misc-tentative    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD pax-tentative     AS INT
    FIELD room-tentative    AS INT

    FIELD rsv-karteityp     AS INT
    FIELD rsv-name          AS CHAR
    FIELD rsv-nationnr      AS INT

    FIELD guest-karteityp   AS INT
    FIELD guest-name        AS CHAR
    FIELD guest-nationnr    AS INT

    FIELD sob               AS INT
    FIELD resstatus         AS INT
    FIELD currency          AS CHAR
    FIELD zipreis           AS DECIMAL
    FIELD flag-history      AS LOGICAL INIT NO

    FIELD firmen-nr         AS INT
    FIELD steuernr          LIKE guest.steuernr

    /* Add by Michael for Sol Beach Benoa request per segment */
    FIELD segmentcode       AS INT
    FIELD segmentbez        AS CHAR
    /* End of add */
    FIELD fcost             AS DECIMAL
/* add by damen 15/05/23  DCB8A3*/
    FIELD argtcode          AS CHARACTER
    FIELD argtbez           AS CHARACTER
    .

DEFINE INPUT  PARAMETER fr-date     AS DATE.
DEFINE INPUT  PARAMETER to-date     AS DATE.
DEFINE INPUT  PARAMETER excl-comp   AS LOGICAL.
DEFINE INPUT  PARAMETER vhp-limited AS LOGICAL.
DEFINE INPUT  PARAMETER scin        AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
/*
DEF VAR vhp-limited AS LOGICAL.
DEF VAR fr-date AS DATE INIT 04/07/14.
DEF VAR to-date AS DATE INIT 04/07/14.
DEF VAR excl-comp AS LOGICAL INIT NO.
*/
DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.
FOR EACH t-list:
    DELETE t-list.
END.

/***
IF fr-date LT ci-date THEN 
DO:
    IF NOT excl-comp THEN RUN create-umsatz.   /* history */
    ELSE RUN create-umsatz-excl-compliment.
END.
ELSE
DO: 
    IF NOT excl-comp THEN RUN create-umsatz1.    /* forecast */
    ELSE RUN create-umsatz1-excl-compliment.
END.
***/
IF fr-date LT ci-date THEN 
DO:
    IF NOT excl-comp THEN RUN create-umsatz.   /* history */
    ELSE RUN create-umsatz-excl-compliment.

    IF to-date GE ci-date THEN 
    DO:
        IF NOT excl-comp THEN RUN create-umsatz1.    /* forecast */
        ELSE RUN create-umsatz1-excl-compliment.
    END.
END.
ELSE
DO:
    IF NOT excl-comp THEN RUN create-umsatz1.    /* forecast */
    ELSE RUN create-umsatz1-excl-compliment.
END.


FOR EACH t-list WHERE 
    (t-list.pax-guaranteed = 0 AND t-list.room-guaranteed = 0
     AND t-list.logis-guaranteed = 0)
    AND
    (t-list.pax-tentative = 0 AND t-list.room-tentative = 0
     AND t-list.logis-tentative = 0):
    DELETE t-list.
END. 

PROCEDURE create-umsatz:
DEFINE VARIABLE do-it           AS LOGICAL.
DEFINE VARIABLE cur-date        AS DATE. 
DEFINE VARIABLE mm              AS INTEGER. 
DEFINE VARIABLE yy              AS INTEGER. 

DEFINE VARIABLE d2              AS DATE.
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE rmsharer        AS LOGICAL INITIAL NO.
DEFINE VARIABLE dayuse-flag     AS LOGICAL. 

DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 
DEFINE VARIABLE local-net-lodg  AS DECIMAL.
DEFINE VARIABLE net-lodg        AS DECIMAL.
DEFINE VARIABLE consider-it     AS LOGICAL.

DEFINE VARIABLE tot-breakfast   AS DECIMAL.
DEFINE VARIABLE tot-Lunch       AS DECIMAL.
DEFINE VARIABLE tot-dinner      AS DECIMAL.
DEFINE VARIABLE tot-Other       AS DECIMAL.
DEFINE VARIABLE tot-rmrev       AS DECIMAL INITIAL 0.

DEFINE VARIABLE tot-vat         AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-service     AS DECIMAL INITIAL 0.

DEFINE VARIABLE Fnet-lodg       AS DECIMAL NO-UNDO. /* Add by Michael for Sol Benoa revenue incl service charge request - ticket no */

DEFINE BUFFER rline1  FOR res-line.
DEFINE BUFFER kline   FOR kontline.
DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gnation FOR nation.

    datum1 = fr-date. 
    IF to-date LT (ci-date - 1) THEN d2 = to-date.
    ELSE d2 = ci-date - 1. 
    
    FOR EACH genstat WHERE genstat.datum GE datum1 AND genstat.datum LE d2
        AND genstat.res-logic[2] EQ YES
        AND genstat.zinr NE "" 
        USE-INDEX date_ix NO-LOCK:
        IF NOT vhp-limited THEN do-it = YES.
        DO:
            IF genstat.res-date[1] LT genstat.datum
                AND genstat.res-date[2] = genstat.datum 
                AND genstat.resstatus = 8 THEN do-it = NO.
        END.
        IF do-it THEN
        DO:
            FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
                NO-LOCK NO-ERROR.
            FIND FIRST sourccod WHERE sourccod.source-code = genstat.source
            NO-LOCK NO-ERROR.
            FIND FIRST arrangement where arrangement.arrangement eq genstat.argt no-lock no-error.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.

        rmsharer = (genstat.resstatus = 13).

        IF do-it THEN
        DO:
            CREATE t-list.
            /*OLD
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK.
            ASSIGN
                t-list.firmen-nr = guest.firmen-nr
                t-list.steuernr = guest.steuernr.

            FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
            ASSIGN
                t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                          + guest.anrede1 + guest.anredefirma
                t-list.rsv-karteityp = guest.karteityp.
            IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            ELSE t-list.rsv-nationnr = 999.*/
            
            /*New Eko 1 feb 2016*/
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN DO:
                ASSIGN
                    t-list.firmen-nr = guest.firmen-nr
                    t-list.steuernr = guest.steuernr.

                FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
                ASSIGN
                    t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                              + guest.anrede1 + guest.anredefirma
                    t-list.rsv-karteityp = guest.karteityp.
                IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            END.
            ELSE t-list.rsv-nationnr = 999.
            /*End of New*/

            FIND FIRST gmember WHERE gmember.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
            FIND FIRST gnation WHERE gnation.kurzbez = gmember.nation1 NO-LOCK NO-ERROR. 
            IF AVAILABLE gmember THEN
            ASSIGN
                t-list.guest-name = gmember.name + ", " + gmember.vorname1 + " " 
                          + gmember.anrede1 + gmember.anredefirma
                t-list.guest-karteityp = gmember.karteityp.
                
            IF AVAILABLE gnation THEN t-list.guest-nationnr = gnation.nationnr.
            ELSE t-list.guest-nationnr = 999.

            IF AVAILABLE sourccod THEN t-list.sob = sourccod.source-code.
            ELSE t-list.sob = 999.

            FIND FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-ERROR. 
            IF AVAILABLE waehrung THEN t-list.currency = waehrung.wabkurz.

            IF NOT rmSharer THEN
                t-list.room-guaranteed   = t-list.room-guaranteed   + 1.

            /*ASSIGN
                t-list.logis-guaranteed  = t-list.logis-guaranteed  + genstat.logis
                t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + genstat.res-deci[2]
                t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + genstat.res-deci[3]
                t-list.dinner-guaranteed = t-list.dinner-guaranteed + genstat.res-deci[4]
                t-list.misc-guaranteed   = t-list.misc-guaranteed   + genstat.res-deci[5] + genstat.res-deci[6]
                t-list.pax-guaranteed    = t-list.pax-guaranteed    + genstat.erwachs + genstat.kind1
                    + genstat.kind2 + genstat.gratis + genstat.kind3
                t-list.zipreis = t-list.zipreis + genstat.zipreis
                t-list.flag-history      = YES.*/

            /* Modify by Michael for Sol Benoa revenue incl service charge request - ticket no 3D424D */
            IF scin THEN
            DO:
                FIND FIRST res-line WHERE res-line.resnr EQ genstat.resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    RUN get-room-breakdown.p(RECID(res-line), datum1, 0, d2,
                                             OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                             OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                             OUTPUT tot-dinner, OUTPUT tot-other,
                                             OUTPUT tot-rmrev, OUTPUT tot-vat,
                                             OUTPUT tot-service).      
                    ASSIGN
                        t-list.logis-guaranteed  = t-list.logis-guaranteed  + genstat.logis + tot-service
                        t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + genstat.res-deci[2]
                        t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + genstat.res-deci[3]
                        t-list.dinner-guaranteed = t-list.dinner-guaranteed + genstat.res-deci[4]
                        t-list.misc-guaranteed   = t-list.misc-guaranteed   + genstat.res-deci[5] /*+ genstat.res-deci[6]*/
                        t-list.fcost             = t-list.fcost             + genstat.res-deci[6] /*FDL August 08, 24 => 9705F1*/
                        t-list.pax-guaranteed    = t-list.pax-guaranteed    + genstat.erwachs + genstat.kind1
                            + genstat.kind2 + genstat.gratis + genstat.kind3
                        t-list.zipreis = t-list.zipreis + genstat.zipreis + tot-service
                        t-list.flag-history      = YES
                        t-list.segmentcode = genstat.segmentcode /* Add by Michael for Sol Beach Benoa request per segment */
                        t-list.argtcode = res-line.arrangement /* add by damen 15/05/23  DCB8A3*/
                        /*t-list.argtbez = arrangement.argt-bez*/
                        .
                END.                
            END.
            ELSE
            DO:
                ASSIGN                                                                             
                    t-list.logis-guaranteed  = t-list.logis-guaranteed  + genstat.logis      
                    t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + genstat.res-deci[2]
                    t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + genstat.res-deci[3]
                    t-list.dinner-guaranteed = t-list.dinner-guaranteed + genstat.res-deci[4]
                    t-list.misc-guaranteed   = t-list.misc-guaranteed   + genstat.res-deci[5] /*+ genstat.res-deci[6]*/
                    t-list.fcost             = t-list.fcost             + genstat.res-deci[6] /*FDL August 08, 24 => 9705F1*/
                    t-list.pax-guaranteed    = t-list.pax-guaranteed    + genstat.erwachs + genstat.kind1
                        + genstat.kind2 + genstat.gratis + genstat.kind3
                    t-list.zipreis = t-list.zipreis + genstat.zipreis
                    t-list.flag-history      = YES
                    t-list.segmentcode = genstat.segmentcode /* Add by Michael for Sol Beach Benoa request per segment */
                    t-list.argtcode = genstat.Argt /* add by damen 15/05/23  DCB8A3*/
                    /* t-list.argtbez = arrangement.argt-bez*/
                    .                                
            END.                
            /* End of modify */
        END.
    END.

      /****
      d2 = d2 + 1. 
      IF to-date GE ci-date THEN 
      DO:
          FOR EACH res-line WHERE 
              ((res-line.resstatus LE 13 AND res-line.resstatus NE 4
                AND res-line.resstatus NE 8 AND res-line.resstatus NE 9
                AND res-line.resstatus NE 10 AND res-line.resstatus NE 12
                AND res-line.active-flag LE 1 AND NOT 
                (res-line.ankunft GT to-date) AND NOT 
                (res-line.abreise LT d2))) OR 
              (res-line.resstatus = 8 AND res-line.active-flag = 2
               AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
              AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
              NO-LOCK USE-INDEX gnrank_ix 
              BY res-line.resnr BY res-line.reslinnr descending :

              FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
                  NO-LOCK NO-ERROR.
              FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
                  NO-LOCK NO-ERROR.

              ASSIGN
                  tot-breakfast = 0
                  tot-lunch     = 0
                  tot-dinner    = 0
                  tot-other     = 0
                  dayuse-flag   = NO.

              IF NOT vhp-limited THEN do-it = YES.
              ELSE
              DO:
                  FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                    NO-LOCK NO-ERROR.
                  do-it = AVAILABLE segment AND segment.vip-level = 0.
              END.

              IF do-it AND res-line.resstatus = 8 THEN
              DO:
                  dayuse-flag = YES.     
                  FIND FIRST arrangement WHERE arrangement.arrangement 
                    =  res-line.arrangement NO-LOCK. 
                  FIND FIRST bill-line WHERE bill-line.departement = 0
                    AND bill-line.artnr = arrangement.argt-artikelnr
                    AND bill-line.bill-datum = ci-date
                    AND bill-line.massnr = res-line.resnr
                    AND bill-line.billin-nr = res-line.reslinnr
                    USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
                  do-it = AVAILABLE bill-line.
              END.

              FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
              IF do-it AND AVAILABLE zimmer THEN 
              DO: 
                  FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
                    AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
                  IF zimmer.sleeping THEN 
                  DO: 
                    IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                      do-it = NO. 
                  END. 
                  ELSE 
                  DO: 
                    IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                    ELSE do-it = NO. 
                  END. 
              END. 

              IF do-it THEN 
              DO:
                  CREATE t-list.

                  FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
                  ASSIGN
                      t-list.firmen-nr = guest.firmen-nr
                      t-list.steuernr = guest.steuernr.
                  FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
                  ASSIGN
                      t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                                + guest.anrede1 + guest.anredefirma
                      t-list.rsv-karteityp = guest.karteityp.
                  IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
                  ELSE t-list.rsv-nationnr = 999.

                  FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                  FIND FIRST gnation WHERE gnation.kurzbez = gmember.nation1 NO-LOCK NO-ERROR. 
                  IF AVAILABLE gmember THEN
                  ASSIGN
                      t-list.guest-name = gmember.name + ", " + gmember.vorname1 + " " 
                                + gmember.anrede1 + gmember.anredefirma
                      t-list.guest-karteityp = gmember.karteityp.
                      
                  IF AVAILABLE gnation THEN t-list.guest-nationnr = gnation.nationnr.
                  ELSE t-list.guest-nationnr = 999.

                  IF AVAILABLE sourccod THEN t-list.sob = sourccod.source-code.
                  ELSE t-list.sob = 999.

                  FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-ERROR. 
                  IF AVAILABLE waehrung THEN t-list.currency = waehrung.wabkurz.

                  t-list.resstatus = res-line.resstatus.

                  datum1 = d2. 
                  IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
                  datum2 = to-date. 
                  IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

                  DO datum = datum1 TO datum2: 
                      pax = res-line.erwachs. 
                      local-net-lodg = 0.
                      net-lodg = 0.
                      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                        AND reslin-queasy.resnr = res-line.resnr 
                        AND reslin-queasy.reslinnr = res-line.reslinnr 
                        AND reslin-queasy.date1 LE datum 
                        AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                      IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                        pax = reslin-queasy.number3. 

                      consider-it = YES. 
                      IF res-line.zimmerfix THEN 
                      DO: 
                        FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                          AND rline1.reslinnr NE res-line.reslinnr 
                          AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                          AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                        IF AVAILABLE rline1 THEN consider-it = NO. 
                      END. 

                      /* START Breakfast lunch Dinner other From Room Rev*/
                      ASSIGN 
                          local-net-lodg = 0
                          net-lodg       = 0
                          tot-breakfast  = 0
                          tot-lunch      = 0
                          tot-dinner     = 0
                          tot-other      = 0. 

                      /*
                      IF res-line.resstatus NE 3 
                          OR (res-line.resstatus = 3 AND stattype = 0) 
                          OR (res-line.resstatus = 3 AND stattype = 3) THEN
                      */

                      RUN get-room-breakdown.p(RECID(res-line), datum, 0, fr-date,
                                               OUTPUT net-lodg, OUTPUT local-net-lodg,
                                               OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                               OUTPUT tot-dinner, OUTPUT tot-other,
                                               OUTPUT tot-rmrev, OUTPUT tot-vat,
                                               OUTPUT tot-service).
                      t-list.zipreis          = t-list.zipreis + (res-line.zipreis * res-line.zimmeranz).

                      IF datum = ci-date THEN
                      DO:
                          IF res-line.active-flag = 1 OR dayuse-flag THEN
                          DO:
                              IF res-line.resstatus = 3 THEN
                              ASSIGN
                                  t-list.bfast-tentative  = t-list.bfast-tentative  + tot-breakfast
                                  t-list.lunch-tentative  = t-list.lunch-tentative  + tot-lunch
                                  t-list.dinner-tentative = t-list.dinner-tentative + tot-dinner
                                  t-list.misc-tentative   = t-list.misc-tentative   + tot-other.
                              ELSE
                              ASSIGN
                                  t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + tot-breakfast
                                  t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + tot-lunch
                                  t-list.dinner-guaranteed = t-list.dinner-guaranteed + tot-dinner
                                  t-list.misc-guaranteed   = t-list.misc-guaranteed   + tot-other.
                          END.
                      END.
                      ELSE
                      DO:
                          IF datum < res-line.abreise THEN
                          DO:
                              IF res-line.resstatus = 3 THEN
                              ASSIGN
                                  t-list.bfast-tentative  = t-list.bfast-tentative  + tot-breakfast
                                  t-list.lunch-tentative  = t-list.lunch-tentative  + tot-lunch
                                  t-list.dinner-tentative = t-list.dinner-tentative + tot-dinner
                                  t-list.misc-tentative   = t-list.misc-tentative   + tot-other.
                              ELSE
                              ASSIGN
                                  t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + tot-breakfast
                                  t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + tot-lunch
                                  t-list.dinner-guaranteed = t-list.dinner-guaranteed + tot-dinner
                                  t-list.misc-guaranteed   = t-list.misc-guaranteed   + tot-other.
                          END.
                      END.
                      /* END Breakfast lunch Dinner other From Room Rev*/

                      IF datum = res-line.ankunft AND consider-it 
                          AND (res-line.resstatus NE 3 /*OR (res-line.resstatus = 3 AND stattype = 0)*/) THEN
                      DO: 
                        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                          AND NOT res-line.zimmerfix THEN 
                        DO: 
                            /*MT
                            ASSIGN
                            t-list.logis = t-list.logis + net-lodg.
                            t-list.room  = to-list.room + res-line.zimmeranz.
                            room-list.lodg[2] = room-list.lodg[2] + net-lodg.
                            room-list.room[3] = room-list.room[3] + res-line.zimmeranz. 
                            rm-array[3] = rm-array[3] + res-line.zimmeranz. 
                            t-lodg[2]   = t-lodg[2] + net-lodg.

                            IF (res-line.kontignr LT 0) AND kont-doit THEN 
                            DO: 
                              room-list.room[16] = room-list.room[16] - res-line.zimmeranz. 
                              rm-array[16] = rm-array[16] - res-line.zimmeranz. 
                            END. 
                            */
                        END.  

                        /*MT
                        to-list.pax = to-list.pax + (pax + res-line.kind1 
                                                     + res-line.kind2 
                                                     + res-line.l-zuordnung[4] 
                                                     + res-line.gratis) 
                                      * res-line.zimmeranz.

                        ASSIGN
                          room-list.room[4] = room-list.room[4] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz
                          rm-array[4] = rm-array[4] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz
                        .
                        */

                        IF res-line.ankunft LT res-line.abreise OR dayuse-flag THEN 
                        DO: 
                          IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                            /*AND res-line.resstatus NE 3*/
                            AND NOT res-line.zimmerfix THEN
                          DO:
                              IF res-line.resstatus = 3 THEN
                              ASSIGN
                                  t-list.logis-tentative  = t-list.logis-tentative + local-net-lodg
                                  t-list.room-tentative   = t-list.room-tentative + res-line.zimmeranz.
                              ELSE
                              ASSIGN
                                  t-list.logis-guaranteed  = t-list.logis-guaranteed + local-net-lodg
                                  t-list.room-guaranteed   = t-list.room-guaranteed + res-line.zimmeranz.
                              /*MT
                              ASSIGN
                                room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                                room-list.lodg[4] = room-list.lodg[4] + net-lodg
                                rm-array[7] = rm-array[7] + res-line.zimmeranz 
                                t-lodg[4]   = t-lodg[4]   + net-lodg
                              . 
                              */
                          END.
                          IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                              /*AND res-line.resstatus NE 3*/ THEN
                          DO:
                              IF res-line.resstatus = 3 THEN
                              t-list.pax-tentative = t-list.pax-tentative + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz.
                              ELSE
                              t-list.pax-guaranteed = t-list.pax-guaranteed + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz.
                              /*MT
                              to-list.pax = to-list.pax + (pax + res-line.kind1 
                                                           + res-line.kind2 
                                                           + res-line.l-zuordnung[4] 
                                                           + res-line.gratis) 
                                          * res-line.zimmeranz.
                              ASSIGN
                                room-list.room[8] = room-list.room[8] 
                                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                  + res-line.gratis) * res-line.zimmeranz 
                                rm-array[8] = rm-array[8] 
                                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                  + res-line.gratis) * res-line.zimmeranz 
                              .
                              */
                          END.
                        END. 
                      END. /*  Arrival */ 

                      IF datum = res-line.abreise AND res-line.resstatus NE 3 
                        AND consider-it THEN 
                      DO: 
                        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                          AND NOT res-line.zimmerfix THEN
                        DO:
                            /*MT
                            ASSIGN
                                to-list.logis = to-list.logis + net-lodg

                                to-list.room  = to-list.room + res-line.zimmeranz
                                .
                            ASSIGN
                              room-list.room[5] = room-list.room[5] + res-line.zimmeranz
                              room-list.lodg[3] = room-list.lodg[3] + net-lodg
                              rm-array[5] = rm-array[5] + res-line.zimmeranz
                              t-lodg[3] = t-lodg[3] + net-lodg
                            .
                            */
                        END.
                        IF datum NE fr-date THEN
                        DO:
                            /*MT
                            to-list.logis = to-list.logis + net-lodg.
                            room-list.lodg[1] = room-list.lodg[1] + net-lodg.
                            */
                        END.

                        /*MT
                        to-list.pax = to-list.pax + (pax + res-line.kind1 
                                                     + res-line.kind2 
                                                     + res-line.l-zuordnung[4] 
                                                     + res-line.gratis) 
                                    * res-line.zimmeranz.
                        ASSIGN
                          room-list.room[6] = room-list.room[6] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz 
                          rm-array[6] = rm-array[6] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz 

                        .
                        */
                      END. /* Departure */ 

                      IF res-line.resstatus NE 3 AND res-line.resstatus NE 4 
                        AND consider-it 
                        AND (res-line.abreise GT res-line.ankunft 
                          AND res-line.ankunft NE datum
                          AND res-line.abreise NE datum) THEN 
                      DO: 
                        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                          /*AND res-line.resstatus NE 3*/
                          AND NOT res-line.zimmerfix THEN 
                        DO:
                            IF res-line.resstatus = 3 THEN
                            ASSIGN
                                t-list.logis-tentative = t-list.logis-tentative + local-net-lodg
                                t-list.room-tentative  = t-list.room-tentative + res-line.zimmeranz.
                            ELSE
                            ASSIGN
                                t-list.logis-guaranteed = t-list.logis-guaranteed + local-net-lodg
                                t-list.room-guaranteed  = t-list.room-guaranteed + res-line.zimmeranz.
                            /*MT
                            ASSIGN
                              room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                              room-list.lodg[4] = room-list.lodg[4] + net-lodg
                              rm-array[7] = rm-array[7]   + res-line.zimmeranz
                              t-lodg[4]   = t-lodg[4]     + net-lodg
                              .
                            */
                        END.

                        IF datum NE fr-date THEN
                        DO:
                            /*MT
                            to-list.logis = to-list.logis + net-lodg.
                            room-list.lodg[1] = room-list.lodg[1] + net-lodg.
                            */
                        END.

                        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                            /*AND res-line.resstatus NE 3*/ THEN
                        DO:
                            IF res-line.resstatus = 3 THEN
                            t-list.pax-tentative = t-list.pax-tentative + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz.
                            ELSE
                            t-list.pax-guaranteed = t-list.pax-guaranteed + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                       + res-line.gratis) * res-line.zimmeranz.
                            /*MT
                            to-list.room  = to-list.room + res-line.zimmeranz.

                            ASSIGN
                              room-list.room[8] = room-list.room[8] 
                                + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                + res-line.gratis) * res-line.zimmeranz 
                              rm-array[8] = rm-array[8] 
                                + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                + res-line.gratis) * res-line.zimmeranz 
                            .
                            */
                        END.
                      END. /* Inhouse */ 

                      IF res-line.resstatus = 3 AND datum LT res-line.abreise THEN 
                      DO:
                          /*MT
                          to-list.room  = to-list.room + res-line.zimmeranz.
                          ASSIGN 
                            room-list.room[13] = room-list.room[13] + res-line.zimmeranz
                            rm-array[13] = rm-array[13] + res-line.zimmeranz
                            room-list.t-pax = room-list.t-pax + (res-line.erwachs * res-line.zimmeranz)
                            tent-pers = tent-pers + (res-line.erwachs * res-line.zimmeranz)
                          . 
                          */
                      END.

                      IF res-line.kontignr > 0 /* AND NOT res-line.zimmerfix */
                        AND res-line.active-flag LE 1 AND res-line.resstatus LE 6
                        AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
                        AND res-line.abreise GT datum THEN 
                      DO: 
                          FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
                            AND kline.kontstat = 1 NO-LOCK.
                          FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
                            AND kontline.ankunft LE datum AND kontline.abreise GE datum
                            AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 
                            NO-LOCK NO-ERROR.
                          IF AVAILABLE kontline AND datum GE (ci-date + kontline.ruecktage) THEN
                          DO:
                              /*MT
                              to-list.room  = to-list.room + res-line.zimmeranz.

                              ASSIGN
                                room-list.room[14] = room-list.room[14] - res-line.zimmeranz
                                rm-array[14] = rm-array[14] - res-line.zimmeranz
                              .
                              */
                          END.
                      END.
                  END. 
              END. 
              PROCESS EVENTS. 
          END.

          DO datum = fr-date TO to-date: 
              FOR EACH kontline WHERE kontline.ankunft LE datum 
                  AND kontline.abreise GE datum AND kontline.betriebsnr = 1 
                  AND kontline.kontstat = 1 NO-LOCK: 
                  do-it = YES. 

                  IF do-it THEN 
                  DO: 
                    /*MT
                    FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
                    ASSIGN
                      room-list.room[16] = room-list.room[16] + kontline.zimmeranz
                      room-list.room[17] = room-list.room[17] 
                        + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                        * kontline.zimmeranz
                      rm-array[16] = rm-array[16] + kontline.zimmeranz
                      rm-array[17] = rm-array[17] 
                        + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                        * kontline.zimmeranz
                    . 
                    */
                  END. 
              END. 
              PROCESS EVENTS.
          END.
      END.
      */
END.

PROCEDURE create-umsatz-excl-compliment:
DEFINE VARIABLE do-it           AS LOGICAL.
DEFINE VARIABLE cur-date        AS DATE. 
DEFINE VARIABLE mm              AS INTEGER. 
DEFINE VARIABLE yy              AS INTEGER. 

DEFINE VARIABLE d2              AS DATE.
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE rmsharer        AS LOGICAL INITIAL NO.
DEFINE VARIABLE dayuse-flag     AS LOGICAL. 

DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 
DEFINE VARIABLE local-net-lodg  AS DECIMAL.
DEFINE VARIABLE net-lodg        AS DECIMAL.
DEFINE VARIABLE consider-it     AS LOGICAL.

DEFINE VARIABLE tot-breakfast   AS DECIMAL.
DEFINE VARIABLE tot-Lunch       AS DECIMAL.
DEFINE VARIABLE tot-dinner      AS DECIMAL.
DEFINE VARIABLE tot-Other       AS DECIMAL.
DEFINE VARIABLE tot-rmrev       AS DECIMAL INITIAL 0.

DEFINE VARIABLE tot-vat         AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-service     AS DECIMAL INITIAL 0.

DEFINE VARIABLE Fnet-lodg       AS DECIMAL NO-UNDO. /* Add by Michael for Sol Benoa revenue incl service charge request - ticket no */

DEFINE BUFFER rline1  FOR res-line.
DEFINE BUFFER kline   FOR kontline.
DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gnation FOR nation.

    datum1 = fr-date. 
    IF to-date LT (ci-date - 1) THEN d2 = to-date.
    ELSE d2 = ci-date - 1. 
    
    FOR EACH genstat WHERE genstat.datum GE datum1 AND genstat.datum LE d2
        AND genstat.res-logic[2] EQ YES
        AND genstat.zinr NE "" 
        AND genstat.gratis EQ 0
        USE-INDEX date_ix NO-LOCK:
        IF NOT vhp-limited THEN do-it = YES.
        DO:
            IF genstat.res-date[1] LT genstat.datum
                AND genstat.res-date[2] = genstat.datum 
                AND genstat.resstatus = 8 THEN do-it = NO.
        END.
        IF do-it THEN
        DO:
            FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
                NO-LOCK NO-ERROR.
            find first sourccod WHERE sourccod.source-code = genstat.SOURCE no-lock no-error.
            FIND FIRST arrangement where arrangement.arrangement = genstat.argt
              no-lock no-error.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.

        rmsharer = (genstat.resstatus = 13).

        IF do-it THEN
        DO:
            CREATE t-list.

            /*OLD
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK.
            ASSIGN
                t-list.firmen-nr = guest.firmen-nr
                t-list.steuernr = guest.steuernr.

            FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
            ASSIGN
                t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                          + guest.anrede1 + guest.anredefirma
                t-list.rsv-karteityp = guest.karteityp.
            IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            ELSE t-list.rsv-nationnr = 999.*/

            /*New Eko 1 feb 2016*/
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN DO:
                ASSIGN
                    t-list.firmen-nr = guest.firmen-nr
                    t-list.steuernr = guest.steuernr.

                FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
                ASSIGN
                    t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                              + guest.anrede1 + guest.anredefirma
                    t-list.rsv-karteityp = guest.karteityp.
                IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            END.
            ELSE t-list.rsv-nationnr = 999.
            /*End of New*/

            FIND FIRST gmember WHERE gmember.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
            FIND FIRST gnation WHERE gnation.kurzbez = gmember.nation1 NO-LOCK NO-ERROR. 
            IF AVAILABLE gmember THEN
            ASSIGN
                t-list.guest-name = gmember.name + ", " + gmember.vorname1 + " " 
                          + gmember.anrede1 + gmember.anredefirma
                t-list.guest-karteityp = gmember.karteityp.
                
            IF AVAILABLE gnation THEN t-list.guest-nationnr = gnation.nationnr.
            ELSE t-list.guest-nationnr = 999.

            IF AVAILABLE sourccod THEN t-list.sob = sourccod.source-code.
            ELSE t-list.sob = 999.

            FIND FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-ERROR. 
            IF AVAILABLE waehrung THEN t-list.currency = waehrung.wabkurz.

            IF NOT rmSharer THEN
                t-list.room-guaranteed   = t-list.room-guaranteed   + 1.

            /*ASSIGN
                t-list.logis-guaranteed  = t-list.logis-guaranteed  + genstat.logis
                t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + genstat.res-deci[2]
                t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + genstat.res-deci[3]
                t-list.dinner-guaranteed = t-list.dinner-guaranteed + genstat.res-deci[4]
                t-list.misc-guaranteed   = t-list.misc-guaranteed   + genstat.res-deci[5] + genstat.res-deci[6]
                t-list.pax-guaranteed    = t-list.pax-guaranteed    + genstat.erwachs + genstat.kind1
                    + genstat.kind2 + genstat.gratis + genstat.kind3
                t-list.zipreis = t-list.zipreis + genstat.zipreis
                t-list.flag-history      = YES.*/

            /* Modify by Michael for Sol Benoa revenue incl service charge request - ticket no 3D424D */
            IF scin THEN
            DO:
                FIND FIRST res-line WHERE res-line.resnr EQ genstat.resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    RUN get-room-breakdown.p(RECID(res-line), datum1, 0, d2,
                                             OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                             OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                             OUTPUT tot-dinner, OUTPUT tot-other,
                                             OUTPUT tot-rmrev, OUTPUT tot-vat,
                                             OUTPUT tot-service).      
                    ASSIGN
                        t-list.logis-guaranteed  = t-list.logis-guaranteed  + genstat.logis + tot-service
                        t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + genstat.res-deci[2]
                        t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + genstat.res-deci[3]
                        t-list.dinner-guaranteed = t-list.dinner-guaranteed + genstat.res-deci[4]
                        t-list.misc-guaranteed   = t-list.misc-guaranteed   + genstat.res-deci[5] /*+ genstat.res-deci[6]*/
                        t-list.fcost             = t-list.fcost             + genstat.res-deci[6] /*FDL August 08, 24 => 9705F1*/
                        t-list.pax-guaranteed    = t-list.pax-guaranteed    + genstat.erwachs + genstat.kind1
                            + genstat.kind2 + genstat.gratis + genstat.kind3
                        t-list.zipreis = t-list.zipreis + genstat.zipreis + tot-service
                        t-list.flag-history      = YES
                        t-list.segmentcode = genstat.segmentcode /* Add by Michael for Sol Beach Benoa request per segment */
                        t-list.argtcode = res-line.arrangement /* add by damen 15/05/23  DCB8A3*/
                        /*t-list.argtbez = arrangement.argt-bez*/
                        .
                END.                
            END.
            ELSE
                ASSIGN
                    t-list.logis-guaranteed  = t-list.logis-guaranteed  + genstat.logis
                    t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + genstat.res-deci[2]
                    t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + genstat.res-deci[3]
                    t-list.dinner-guaranteed = t-list.dinner-guaranteed + genstat.res-deci[4]
                    t-list.misc-guaranteed   = t-list.misc-guaranteed   + genstat.res-deci[5] /*+ genstat.res-deci[6]*/
                    t-list.fcost             = t-list.fcost             + genstat.res-deci[6] /*FDL August 08, 24 => 9705F1*/
                    t-list.pax-guaranteed    = t-list.pax-guaranteed    + genstat.erwachs + genstat.kind1
                        + genstat.kind2 + genstat.gratis + genstat.kind3
                    t-list.zipreis = t-list.zipreis + genstat.zipreis
                    t-list.flag-history      = YES
                    t-list.segmentcode = genstat.segmentcode /* Add by Michael for Sol Beach Benoa request per segment */
                    t-list.argtcode = genstat.argt /* add by damen 15/05/23  DCB8A3*/
                    /* t-list.argtbez = arrangement.argt-bez*/
                    .
            /* End of modify */
        END.
    END.
END.


/**********************************************************************/
PROCEDURE create-umsatz1:    /* forecast */
DEFINE VARIABLE do-it           AS LOGICAL.
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE d2              AS DATE.
DEFINE VARIABLE local-net-lodg  AS DECIMAL.
DEFINE VARIABLE net-lodg        AS DECIMAL.
DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 

DEFINE VAR tot-breakfast        AS DECIMAL.
DEFINE VAR tot-Lunch            AS DECIMAL.
DEFINE VAR tot-dinner           AS DECIMAL.
DEFINE VAR tot-Other            AS DECIMAL.
DEFINE VAR dayuse-flag          AS LOGICAL. 
DEFINE VAR consider-it          AS LOGICAL.
DEFINE VAR tot-rmrev            AS DECIMAL INITIAL 0.
DEFINE VAR tot-vat              AS DECIMAL INITIAL 0.
DEFINE VAR tot-service          AS DECIMAL INITIAL 0.
DEF VAR a AS INT.

DEFINE VARIABLE Fnet-lodg       AS DECIMAL NO-UNDO. /* Add by Michael for Sol Benoa revenue incl service charge request - ticket no */

DEFINE BUFFER rline1  FOR res-line.
DEFINE BUFFER kline   FOR kontline.
DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gnation FOR nation.

    IF fr-date NE ci-date AND fr-date LT ci-date THEN fr-date = ci-date.
    datum1 = fr-date. 
    IF to-date LT (ci-date - 1) THEN d2 = to-date.
    ELSE d2 = ci-date - 1. 
    d2 = d2 + 1. 
    
    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT to-date) AND 
         NOT (res-line.abreise LT fr-date)) 
        OR (res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK BY res-line.resnr: /*MT 13/08/12 */
    
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
            NO-LOCK NO-ERROR.
    
        ASSIGN
            tot-breakfast = 0
            tot-lunch     = 0
            tot-dinner    = 0
            tot-other     = 0
            dayuse-flag   = NO.
    
        IF NOT vhp-limited THEN do-it = YES.
        ELSE
        DO:
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK NO-ERROR.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
    
        IF do-it AND res-line.resstatus = 8 THEN
        DO:
            dayuse-flag = YES.     
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.
    
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
              AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                  do-it = NO. 
            END. 
            ELSE 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
            END. 
        END. 
    
        IF do-it THEN 
        DO:
            CREATE t-list.
            ASSIGN
              t-list.resnr = res-line.resnr
              t-list.reslinnr = res-line.reslinnr.

            /*OLD
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK.
            ASSIGN
                t-list.firmen-nr = guest.firmen-nr
                t-list.steuernr = guest.steuernr.

            FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
            ASSIGN
                t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                          + guest.anrede1 + guest.anredefirma
                t-list.rsv-karteityp = guest.karteityp.
            IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            ELSE t-list.rsv-nationnr = 999.*/

            /*New Eko 1 feb 2016*/
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN DO:
                ASSIGN
                    t-list.firmen-nr = guest.firmen-nr
                    t-list.steuernr = guest.steuernr.

                FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
                ASSIGN
                    t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                              + guest.anrede1 + guest.anredefirma
                    t-list.rsv-karteityp = guest.karteityp.
                IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            END.
            ELSE t-list.rsv-nationnr = 999.
            /*End of New*/
    
            FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            FIND FIRST gnation WHERE gnation.kurzbez = gmember.nation1 NO-LOCK NO-ERROR. 
            IF AVAILABLE gmember THEN
            ASSIGN
                t-list.guest-name = gmember.name + ", " + gmember.vorname1 + " " 
                          + gmember.anrede1 + gmember.anredefirma
                t-list.guest-karteityp = gmember.karteityp.
                
            IF AVAILABLE gnation THEN t-list.guest-nationnr = gnation.nationnr.
            ELSE t-list.guest-nationnr = 999.
    
            IF AVAILABLE sourccod THEN t-list.sob = sourccod.source-code.
            ELSE t-list.sob = 999.
    
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-ERROR. 
            IF AVAILABLE waehrung THEN t-list.currency = waehrung.wabkurz.
    
            t-list.resstatus = res-line.resstatus.
            t-list.segmentcode = reservation.segmentcode. /* Add by Michael for Sol Beach Benoa request per segment */
            t-list.argtcode = res-line.arrangement. /* add by damen 22/05/2023 DCB8A3*/
            IF res-line.ankunft GE fr-date THEN datum1 = res-line.ankunft. 
            ELSE datum1 = fr-date.
            IF res-line.abreise LE to-date THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = to-date.

            DO datum = datum1 TO datum2: 
                a = a + 1.
                pax = res-line.erwachs. 
                local-net-lodg = 0.
                net-lodg = 0.
                FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                    AND reslin-queasy.resnr = res-line.resnr 
                    AND reslin-queasy.reslinnr = res-line.reslinnr 
                    AND reslin-queasy.date1 LE datum 
                    AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                    pax = reslin-queasy.number3. 
    
                consider-it = YES. 
                IF res-line.zimmerfix THEN 
                DO: 
                    FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                      AND rline1.reslinnr NE res-line.reslinnr 
                      AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                      AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE rline1 THEN consider-it = NO. 
                END. 
    
                /* START Breakfast lunch Dinner other From Room Rev*/
                ASSIGN 
                    local-net-lodg      = 0
                    net-lodg = 0
                    tot-breakfast = 0
                    tot-lunch     = 0
                    tot-dinner    = 0
                    tot-other     = 0. 
    
                /*
                IF res-line.resstatus NE 3 
                    OR (res-line.resstatus = 3 AND stattype = 0) 
                    OR (res-line.resstatus = 3 AND stattype = 3) THEN
                */
                
                RUN get-room-breakdown.p(RECID(res-line), datum, 0, fr-date,
                                         OUTPUT net-lodg, OUTPUT local-net-lodg,
                                         OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                         OUTPUT tot-dinner, OUTPUT tot-other,
                                         OUTPUT tot-rmrev, OUTPUT tot-vat,
                                         OUTPUT tot-service).
                /*MTzt-list.zipreis          = t-list.zipreis + tot-rmrev.*/

                IF tot-rmrev = 0 THEN  /*ITA 020117*/
                    ASSIGN 
                        local-net-lodg      = 0
                        net-lodg            = 0
                        tot-breakfast       = 0
                        tot-lunch           = 0
                        tot-dinner          = 0
                        tot-other           = 0. 

                t-list.zipreis          = t-list.zipreis + (tot-rmrev * res-line.zimmeranz).
                
                IF datum = ci-date THEN
                DO: 
                    /*IF res-line.active-flag = 1 OR dayuse-flag THEN*/
                    IF res-line.active-flag EQ 0 OR 
                        (res-line.active-flag EQ 1 AND res-line.resstatus NE 8) OR 
                        (res-line.active-flag EQ 1 AND res-line.resstatus NE 99) THEN /* Modify by Michael @ 01/07/2018 for fixing Yellow Pascal Bandung bugs - ticket no 717717*/
                    DO:
                        IF res-line.resstatus = 3 THEN
                        ASSIGN
                            t-list.bfast-tentative  = t-list.bfast-tentative  + tot-breakfast
                            t-list.lunch-tentative  = t-list.lunch-tentative  + tot-lunch
                            t-list.dinner-tentative = t-list.dinner-tentative + tot-dinner
                            t-list.misc-tentative   = t-list.misc-tentative   + tot-other.
                        ELSE
                        ASSIGN
                            t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + tot-breakfast
                            t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + tot-lunch
                            t-list.dinner-guaranteed = t-list.dinner-guaranteed + tot-dinner
                            t-list.misc-guaranteed   = t-list.misc-guaranteed   + tot-other.
                    END.
                END.
                ELSE
                DO:
                    IF datum < res-line.abreise THEN
                    DO:
                        IF res-line.resstatus = 3 THEN
                        ASSIGN
                            t-list.bfast-tentative  = t-list.bfast-tentative  + tot-breakfast
                            t-list.lunch-tentative  = t-list.lunch-tentative  + tot-lunch
                            t-list.dinner-tentative = t-list.dinner-tentative + tot-dinner
                            t-list.misc-tentative   = t-list.misc-tentative   + tot-other.
                        ELSE
                        ASSIGN
                            t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + tot-breakfast
                            t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + tot-lunch
                            t-list.dinner-guaranteed = t-list.dinner-guaranteed + tot-dinner
                            t-list.misc-guaranteed   = t-list.misc-guaranteed   + tot-other.
                    END.
                END.
                /* END Breakfast lunch Dinner other From Room Rev*/
    
                IF datum = res-line.ankunft AND consider-it THEN
                DO: 
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND NOT res-line.zimmerfix THEN 
                  DO: 
                      /*MT
                      ASSIGN
                      t-list.logis = t-list.logis + net-lodg.
                      t-list.room  = to-list.room + res-line.zimmeranz.
                      room-list.lodg[2] = room-list.lodg[2] + net-lodg.
                      room-list.room[3] = room-list.room[3] + res-line.zimmeranz. 
                      rm-array[3] = rm-array[3] + res-line.zimmeranz. 
                      t-lodg[2]   = t-lodg[2] + net-lodg.
    
                      IF (res-line.kontignr LT 0) AND kont-doit THEN 
                      DO: 
                        room-list.room[16] = room-list.room[16] - res-line.zimmeranz. 
                        rm-array[16] = rm-array[16] - res-line.zimmeranz. 
                      END. 
                      */
                  END.  
    
                  /*MT
                  to-list.pax = to-list.pax + (pax + res-line.kind1 
                                               + res-line.kind2 
                                               + res-line.l-zuordnung[4] 
                                               + res-line.gratis) 
                                * res-line.zimmeranz.
    
                  ASSIGN
                    room-list.room[4] = room-list.room[4] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz
                    rm-array[4] = rm-array[4] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz
                  .
                  */
    
                  IF res-line.ankunft LT res-line.abreise OR dayuse-flag THEN 
                  DO: 
                    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                      /*AND res-line.resstatus NE 3*/
                      AND NOT res-line.zimmerfix THEN
                    DO:                                                
                        IF res-line.resstatus = 3 THEN
                        ASSIGN
                            t-list.logis-tentative  = t-list.logis-tentative + local-net-lodg
                            t-list.room-tentative   = t-list.room-tentative + res-line.zimmeranz.
                        ELSE
                        ASSIGN
                            t-list.logis-guaranteed  = t-list.logis-guaranteed + local-net-lodg
                            t-list.room-guaranteed   = t-list.room-guaranteed + res-line.zimmeranz.
                        /*MT
                        ASSIGN
                          room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                          room-list.lodg[4] = room-list.lodg[4] + net-lodg
                          rm-array[7] = rm-array[7] + res-line.zimmeranz 
                          t-lodg[4]   = t-lodg[4]   + net-lodg
                        . 
                        */
                    END.
                    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                        /*AND res-line.resstatus NE 3*/ THEN
                    DO:
                        IF res-line.resstatus = 3 THEN
                        t-list.pax-tentative = t-list.pax-tentative + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                        ELSE
                        t-list.pax-guaranteed = t-list.pax-guaranteed + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                        /*MT
                        to-list.pax = to-list.pax + (pax + res-line.kind1 
                                                     + res-line.kind2 
                                                     + res-line.l-zuordnung[4] 
                                                     + res-line.gratis) 
                                    * res-line.zimmeranz.
                        ASSIGN
                          room-list.room[8] = room-list.room[8] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz 
                          rm-array[8] = rm-array[8] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz 
                        .
                        */
                    END.
                  END. 
                END. /*  Arrival */ 
    
                IF datum = res-line.abreise AND res-line.resstatus NE 3 
                  AND consider-it THEN 
                DO: 
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND NOT res-line.zimmerfix THEN
                  DO:
                      /*MT
                      ASSIGN
                          to-list.logis = to-list.logis + net-lodg
    
                          to-list.room  = to-list.room + res-line.zimmeranz
                          .
                      ASSIGN
                        room-list.room[5] = room-list.room[5] + res-line.zimmeranz
                        room-list.lodg[3] = room-list.lodg[3] + net-lodg
                        rm-array[5] = rm-array[5] + res-line.zimmeranz
                        t-lodg[3] = t-lodg[3] + net-lodg
                      .
                      */
                  END.
                  IF datum NE fr-date THEN
                  DO:
                      /*MT
                      to-list.logis = to-list.logis + net-lodg.
                      room-list.lodg[1] = room-list.lodg[1] + net-lodg.
                      */
                  END.
    
                  /*MT
                  to-list.pax = to-list.pax + (pax + res-line.kind1 
                                               + res-line.kind2 
                                               + res-line.l-zuordnung[4] 
                                               + res-line.gratis) 
                              * res-line.zimmeranz.
                  ASSIGN
                    room-list.room[6] = room-list.room[6] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz 
                    rm-array[6] = rm-array[6] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz 
    
                  .
                  */
                END. /* Departure */ 
    
                IF res-line.resstatus NE 4 AND consider-it 
                    AND (res-line.abreise GT res-line.ankunft 
                         AND res-line.ankunft NE datum
                         AND res-line.abreise NE datum) THEN 
                DO: 
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    /*AND res-line.resstatus NE 3*/
                    AND NOT res-line.zimmerfix THEN 
                  DO:
                      IF res-line.resstatus = 3 THEN
                      ASSIGN
                          t-list.logis-tentative = t-list.logis-tentative + local-net-lodg
                          t-list.room-tentative  = t-list.room-tentative + res-line.zimmeranz.
                      ELSE
                      ASSIGN
                          t-list.logis-guaranteed = t-list.logis-guaranteed + local-net-lodg
                          t-list.room-guaranteed  = t-list.room-guaranteed + res-line.zimmeranz.
                      /*MT
                      ASSIGN
                        room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                        room-list.lodg[4] = room-list.lodg[4] + net-lodg
                        rm-array[7] = rm-array[7]   + res-line.zimmeranz
                        t-lodg[4]   = t-lodg[4]     + net-lodg
                        .
                      */
                  END.
    
                  IF datum NE fr-date THEN
                  DO:
                      /*MT
                      to-list.logis = to-list.logis + net-lodg.
                      room-list.lodg[1] = room-list.lodg[1] + net-lodg.
                      */
                  END.
    
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                      /*AND res-line.resstatus NE 3*/ THEN
                  DO:
                      IF res-line.resstatus = 3 THEN
                      t-list.pax-tentative = t-list.pax-tentative + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                      ELSE
                      t-list.pax-guaranteed = t-list.pax-guaranteed + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                      /*MT
                      to-list.room  = to-list.room + res-line.zimmeranz.
    
                      ASSIGN
                        room-list.room[8] = room-list.room[8] 
                          + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                          + res-line.gratis) * res-line.zimmeranz 
                        rm-array[8] = rm-array[8] 
                          + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                          + res-line.gratis) * res-line.zimmeranz 
                      .
                      */
                  END.
                END. /* Inhouse */ 
    
                IF res-line.resstatus = 3 AND datum LT res-line.abreise THEN 
                DO:
                    /*MT
                    to-list.room  = to-list.room + res-line.zimmeranz.
                    ASSIGN 
                      room-list.room[13] = room-list.room[13] + res-line.zimmeranz
                      rm-array[13] = rm-array[13] + res-line.zimmeranz
                      room-list.t-pax = room-list.t-pax + (res-line.erwachs * res-line.zimmeranz)
                      tent-pers = tent-pers + (res-line.erwachs * res-line.zimmeranz)
                    . 
                    */
                END.
    
                IF res-line.kontignr > 0 /* AND NOT res-line.zimmerfix */
                  AND res-line.active-flag LE 1 AND res-line.resstatus LE 6
                  AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
                  AND res-line.abreise GT datum THEN 
                DO: 
                    FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
                      AND kline.kontstat = 1 NO-LOCK.
                    FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
                      AND kontline.ankunft LE datum AND kontline.abreise GE datum
                      AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 
                      NO-LOCK NO-ERROR.
                    IF AVAILABLE kontline AND datum GE (ci-date + kontline.ruecktage) THEN
                    DO:
                        /*MT
                        to-list.room  = to-list.room + res-line.zimmeranz.
    
                        ASSIGN
                          room-list.room[14] = room-list.room[14] - res-line.zimmeranz
                          rm-array[14] = rm-array[14] - res-line.zimmeranz
                        .
                        */
                    END.
                END.
            END. 
        END. 
        PROCESS EVENTS. 
    END.
    
    DO datum = d2 TO to-date: 
        FOR EACH kontline WHERE kontline.ankunft LE datum 
            AND kontline.abreise GE datum AND kontline.betriebsnr = 1 
            AND kontline.kontstat = 1 NO-LOCK: 
            do-it = YES. 
    
            IF do-it THEN 
            DO:
              /*MT
              FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
              ASSIGN
                room-list.room[16] = room-list.room[16] + kontline.zimmeranz
                room-list.room[17] = room-list.room[17] 
                  + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                  * kontline.zimmeranz
                rm-array[16] = rm-array[16] + kontline.zimmeranz
                rm-array[17] = rm-array[17] 
                  + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                  * kontline.zimmeranz
              . 
              */
            END. 
        END. 
        PROCESS EVENTS.
    END.
END.


PROCEDURE create-umsatz1-excl-compliment:    /* forecast */
DEFINE VARIABLE do-it           AS LOGICAL.
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE d2              AS DATE.
DEFINE VARIABLE local-net-lodg  AS DECIMAL.
DEFINE VARIABLE net-lodg        AS DECIMAL.
DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 

DEFINE VAR tot-breakfast        AS DECIMAL.
DEFINE VAR tot-Lunch            AS DECIMAL.
DEFINE VAR tot-dinner           AS DECIMAL.
DEFINE VAR tot-Other            AS DECIMAL.
DEFINE VAR dayuse-flag          AS LOGICAL. 
DEFINE VAR consider-it          AS LOGICAL.
DEFINE VAR tot-rmrev            AS DECIMAL INITIAL 0.
DEFINE VAR tot-vat              AS DECIMAL INITIAL 0.
DEFINE VAR tot-service          AS DECIMAL INITIAL 0.
DEF VAR a AS INT.

DEFINE BUFFER rline1  FOR res-line.
DEFINE BUFFER kline   FOR kontline.
DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gnation FOR nation.
    
    IF fr-date NE ci-date AND fr-date LT ci-date THEN fr-date = ci-date. /*ITA*/
    datum1 = fr-date. 
    IF to-date LT (ci-date - 1) THEN d2 = to-date.
    ELSE d2 = ci-date - 1. 
    d2 = d2 + 1. 
    FOR EACH res-line WHERE 
        res-line.gratis EQ 0
        AND res-line.erwachs GE 1
        AND res-line.zipreis NE 0
        AND 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT to-date) AND 
         NOT (res-line.abreise LT fr-date)) 
        OR (res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        
        USE-INDEX gnrank_ix NO-LOCK BY res-line.resnr: /*MT 13/08/12 */
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
            NO-LOCK NO-ERROR.
    
        ASSIGN
            tot-breakfast = 0
            tot-lunch     = 0
            tot-dinner    = 0
            tot-other     = 0
            dayuse-flag   = NO.
    
        IF NOT vhp-limited THEN do-it = YES.
        ELSE
        DO:
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK NO-ERROR.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
    
        IF do-it AND res-line.resstatus = 8 THEN
        DO:
            dayuse-flag = YES.     
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.
    
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
              AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                  do-it = NO. 
            END. 
            ELSE 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
            END. 
        END. 
    
        IF do-it THEN 
        DO:
            CREATE t-list.
    
            /*OLD
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK.
            ASSIGN
                t-list.firmen-nr = guest.firmen-nr
                t-list.steuernr = guest.steuernr.

            FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
            ASSIGN
                t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                          + guest.anrede1 + guest.anredefirma
                t-list.rsv-karteityp = guest.karteityp.
            IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            ELSE t-list.rsv-nationnr = 999.*/
            
            /*New Eko 1 feb 2016*/
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN DO:
                ASSIGN
                    t-list.firmen-nr = guest.firmen-nr
                    t-list.steuernr = guest.steuernr.

                FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
                ASSIGN
                    t-list.rsv-name = guest.name + ", " + guest.vorname1 + " " 
                              + guest.anrede1 + guest.anredefirma
                    t-list.rsv-karteityp = guest.karteityp.
                IF AVAILABLE nation THEN t-list.rsv-nationnr = nation.nationnr.
            END.
            ELSE t-list.rsv-nationnr = 999.
            /*End of New*/
    
            FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            FIND FIRST gnation WHERE gnation.kurzbez = gmember.nation1 NO-LOCK NO-ERROR. 
            IF AVAILABLE gmember THEN
            ASSIGN
                t-list.guest-name = gmember.name + ", " + gmember.vorname1 + " " 
                          + gmember.anrede1 + gmember.anredefirma
                t-list.guest-karteityp = gmember.karteityp.
                
            IF AVAILABLE gnation THEN t-list.guest-nationnr = gnation.nationnr.
            ELSE t-list.guest-nationnr = 999.
    
            IF AVAILABLE sourccod THEN t-list.sob = sourccod.source-code.
            ELSE t-list.sob = 999.
    
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-ERROR. 
            IF AVAILABLE waehrung THEN t-list.currency = waehrung.wabkurz.
    
            t-list.resstatus = res-line.resstatus.
            t-list.segmentcode = reservation.segmentcode. /* Add by Michael for Sol Beach Benoa request per segment */
            t-list.argtcode = res-line.arrangement. /* add by damen */
            /*t-list.argtbez = arrangement.argt-bez.*/
    
            IF res-line.ankunft GE fr-date THEN datum1 = res-line.ankunft. 
            ELSE datum1 = fr-date.
            IF res-line.abreise LE to-date THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = to-date.

            DO datum = datum1 TO datum2: 
                a = a + 1.
                pax = res-line.erwachs. 
                local-net-lodg = 0.
                net-lodg = 0.
                FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                    AND reslin-queasy.resnr = res-line.resnr 
                    AND reslin-queasy.reslinnr = res-line.reslinnr 
                    AND reslin-queasy.date1 LE datum 
                    AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                    pax = reslin-queasy.number3. 
    
                consider-it = YES. 
                IF res-line.zimmerfix THEN 
                DO: 
                    FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                      AND rline1.reslinnr NE res-line.reslinnr 
                      AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                      AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE rline1 THEN consider-it = NO. 
                END. 
    
                /* START Breakfast lunch Dinner other From Room Rev*/
                ASSIGN 
                    local-net-lodg      = 0
                    net-lodg = 0
                    tot-breakfast = 0
                    tot-lunch     = 0
                    tot-dinner    = 0
                    tot-other     = 0. 
    
                /*
                IF res-line.resstatus NE 3 
                    OR (res-line.resstatus = 3 AND stattype = 0) 
                    OR (res-line.resstatus = 3 AND stattype = 3) THEN
                */
    
                RUN get-room-breakdown.p(RECID(res-line), datum, 0, fr-date,
                                         OUTPUT net-lodg, OUTPUT local-net-lodg,
                                         OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                         OUTPUT tot-dinner, OUTPUT tot-other,
                                         OUTPUT tot-rmrev, OUTPUT tot-vat,
                                         OUTPUT tot-service).
                IF tot-rmrev = 0 THEN  /*ITA 020117*/
                    ASSIGN 
                        local-net-lodg      = 0
                        net-lodg            = 0
                        tot-breakfast       = 0
                        tot-lunch           = 0
                        tot-dinner          = 0
                        tot-other           = 0. 

                t-list.zipreis          = t-list.zipreis + (tot-rmrev * res-line.zimmeranz).
                /*ITA 020117
                t-list.zipreis          = t-list.zipreis + (res-line.zipreis * res-line.zimmeranz).*/
                
                IF datum = ci-date THEN
                DO:
                    IF res-line.active-flag = 1 OR dayuse-flag THEN
                    DO:
                        IF res-line.resstatus = 3 THEN
                        ASSIGN
                            t-list.bfast-tentative  = t-list.bfast-tentative  + tot-breakfast
                            t-list.lunch-tentative  = t-list.lunch-tentative  + tot-lunch
                            t-list.dinner-tentative = t-list.dinner-tentative + tot-dinner
                            t-list.misc-tentative   = t-list.misc-tentative   + tot-other.
                        ELSE
                        ASSIGN
                            t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + tot-breakfast
                            t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + tot-lunch
                            t-list.dinner-guaranteed = t-list.dinner-guaranteed + tot-dinner
                            t-list.misc-guaranteed   = t-list.misc-guaranteed   + tot-other.
                    END.
                END.
                ELSE
                DO:
                    IF datum < res-line.abreise THEN
                    DO:
                        IF res-line.resstatus = 3 THEN
                        ASSIGN
                            t-list.bfast-tentative  = t-list.bfast-tentative  + tot-breakfast
                            t-list.lunch-tentative  = t-list.lunch-tentative  + tot-lunch
                            t-list.dinner-tentative = t-list.dinner-tentative + tot-dinner
                            t-list.misc-tentative   = t-list.misc-tentative   + tot-other.
                        ELSE
                        ASSIGN
                            t-list.bfast-guaranteed  = t-list.bfast-guaranteed  + tot-breakfast
                            t-list.lunch-guaranteed  = t-list.lunch-guaranteed  + tot-lunch
                            t-list.dinner-guaranteed = t-list.dinner-guaranteed + tot-dinner
                            t-list.misc-guaranteed   = t-list.misc-guaranteed   + tot-other.
                    END.
                END.
                /* END Breakfast lunch Dinner other From Room Rev*/
    
                IF datum = res-line.ankunft AND consider-it THEN
                DO: 
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND NOT res-line.zimmerfix THEN 
                  DO: 
                      /*MT
                      ASSIGN
                      t-list.logis = t-list.logis + net-lodg.
                      t-list.room  = to-list.room + res-line.zimmeranz.
                      room-list.lodg[2] = room-list.lodg[2] + net-lodg.
                      room-list.room[3] = room-list.room[3] + res-line.zimmeranz. 
                      rm-array[3] = rm-array[3] + res-line.zimmeranz. 
                      t-lodg[2]   = t-lodg[2] + net-lodg.
    
                      IF (res-line.kontignr LT 0) AND kont-doit THEN 
                      DO: 
                        room-list.room[16] = room-list.room[16] - res-line.zimmeranz. 
                        rm-array[16] = rm-array[16] - res-line.zimmeranz. 
                      END. 
                      */
                  END.  
    
                  /*MT
                  to-list.pax = to-list.pax + (pax + res-line.kind1 
                                               + res-line.kind2 
                                               + res-line.l-zuordnung[4] 
                                               + res-line.gratis) 
                                * res-line.zimmeranz.
    
                  ASSIGN
                    room-list.room[4] = room-list.room[4] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz
                    rm-array[4] = rm-array[4] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz
                  .
                  */
    
                  IF res-line.ankunft LT res-line.abreise OR dayuse-flag THEN 
                  DO: 
                    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                      /*AND res-line.resstatus NE 3*/
                      AND NOT res-line.zimmerfix THEN
                    DO:
                        IF res-line.resstatus = 3 THEN
                        ASSIGN
                            t-list.logis-tentative  = t-list.logis-tentative + local-net-lodg
                            t-list.room-tentative   = t-list.room-tentative + res-line.zimmeranz.
                        ELSE
                        ASSIGN
                            t-list.logis-guaranteed  = t-list.logis-guaranteed + local-net-lodg
                            t-list.room-guaranteed   = t-list.room-guaranteed + res-line.zimmeranz.
                        /*MT
                        ASSIGN
                          room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                          room-list.lodg[4] = room-list.lodg[4] + net-lodg
                          rm-array[7] = rm-array[7] + res-line.zimmeranz 
                          t-lodg[4]   = t-lodg[4]   + net-lodg
                        . 
                        */
                    END.
                    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                        /*AND res-line.resstatus NE 3*/ THEN
                    DO:
                        IF res-line.resstatus = 3 THEN
                        t-list.pax-tentative = t-list.pax-tentative + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                        ELSE
                        t-list.pax-guaranteed = t-list.pax-guaranteed + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                        /*MT
                        to-list.pax = to-list.pax + (pax + res-line.kind1 
                                                     + res-line.kind2 
                                                     + res-line.l-zuordnung[4] 
                                                     + res-line.gratis) 
                                    * res-line.zimmeranz.
                        ASSIGN
                          room-list.room[8] = room-list.room[8] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz 
                          rm-array[8] = rm-array[8] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                            + res-line.gratis) * res-line.zimmeranz 
                        .
                        */
                    END.
                  END. 
                END. /*  Arrival */ 
    
                IF datum = res-line.abreise AND res-line.resstatus NE 3 
                  AND consider-it THEN 
                DO: 
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND NOT res-line.zimmerfix THEN
                  DO:
                      /*MT
                      ASSIGN
                          to-list.logis = to-list.logis + net-lodg
    
                          to-list.room  = to-list.room + res-line.zimmeranz
                          .
                      ASSIGN
                        room-list.room[5] = room-list.room[5] + res-line.zimmeranz
                        room-list.lodg[3] = room-list.lodg[3] + net-lodg
                        rm-array[5] = rm-array[5] + res-line.zimmeranz
                        t-lodg[3] = t-lodg[3] + net-lodg
                      .
                      */
                  END.
                  IF datum NE fr-date THEN
                  DO:
                      /*MT
                      to-list.logis = to-list.logis + net-lodg.
                      room-list.lodg[1] = room-list.lodg[1] + net-lodg.
                      */
                  END.
    
                  /*MT
                  to-list.pax = to-list.pax + (pax + res-line.kind1 
                                               + res-line.kind2 
                                               + res-line.l-zuordnung[4] 
                                               + res-line.gratis) 
                              * res-line.zimmeranz.
                  ASSIGN
                    room-list.room[6] = room-list.room[6] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz 
                    rm-array[6] = rm-array[6] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz 
    
                  .
                  */
                END. /* Departure */ 
    
                IF res-line.resstatus NE 4 AND consider-it 
                    AND (res-line.abreise GT res-line.ankunft 
                         AND res-line.ankunft NE datum
                         AND res-line.abreise NE datum) THEN 
                DO: 
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    /*AND res-line.resstatus NE 3*/
                    AND NOT res-line.zimmerfix THEN 
                  DO:
                      IF res-line.resstatus = 3 THEN
                      ASSIGN
                          t-list.logis-tentative = t-list.logis-tentative + local-net-lodg
                          t-list.room-tentative  = t-list.room-tentative + res-line.zimmeranz.
                      ELSE
                      ASSIGN
                          t-list.logis-guaranteed = t-list.logis-guaranteed + local-net-lodg
                          t-list.room-guaranteed  = t-list.room-guaranteed + res-line.zimmeranz.
                      /*MT
                      ASSIGN
                        room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                        room-list.lodg[4] = room-list.lodg[4] + net-lodg
                        rm-array[7] = rm-array[7]   + res-line.zimmeranz
                        t-lodg[4]   = t-lodg[4]     + net-lodg
                        .
                      */
                  END.
    
                  IF datum NE fr-date THEN
                  DO:
                      /*MT
                      to-list.logis = to-list.logis + net-lodg.
                      room-list.lodg[1] = room-list.lodg[1] + net-lodg.
                      */
                  END.
    
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                      /*AND res-line.resstatus NE 3*/ THEN
                  DO:
                      IF res-line.resstatus = 3 THEN
                      t-list.pax-tentative = t-list.pax-tentative + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                      ELSE
                      t-list.pax-guaranteed = t-list.pax-guaranteed + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                 + res-line.gratis) * res-line.zimmeranz.
                      /*MT
                      to-list.room  = to-list.room + res-line.zimmeranz.
    
                      ASSIGN
                        room-list.room[8] = room-list.room[8] 
                          + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                          + res-line.gratis) * res-line.zimmeranz 
                        rm-array[8] = rm-array[8] 
                          + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                          + res-line.gratis) * res-line.zimmeranz 
                      .
                      */
                  END.
                END. /* Inhouse */ 
    
                IF res-line.resstatus = 3 AND datum LT res-line.abreise THEN 
                DO:
                    /*MT
                    to-list.room  = to-list.room + res-line.zimmeranz.
                    ASSIGN 
                      room-list.room[13] = room-list.room[13] + res-line.zimmeranz
                      rm-array[13] = rm-array[13] + res-line.zimmeranz
                      room-list.t-pax = room-list.t-pax + (res-line.erwachs * res-line.zimmeranz)
                      tent-pers = tent-pers + (res-line.erwachs * res-line.zimmeranz)
                    . 
                    */
                END.
    
                IF res-line.kontignr > 0 /* AND NOT res-line.zimmerfix */
                  AND res-line.active-flag LE 1 AND res-line.resstatus LE 6
                  AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
                  AND res-line.abreise GT datum THEN 
                DO: 
                    FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
                      AND kline.kontstat = 1 NO-LOCK.
                    FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
                      AND kontline.ankunft LE datum AND kontline.abreise GE datum
                      AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 
                      NO-LOCK NO-ERROR.
                    IF AVAILABLE kontline AND datum GE (ci-date + kontline.ruecktage) THEN
                    DO:
                        /*MT
                        to-list.room  = to-list.room + res-line.zimmeranz.
    
                        ASSIGN
                          room-list.room[14] = room-list.room[14] - res-line.zimmeranz
                          rm-array[14] = rm-array[14] - res-line.zimmeranz
                        .
                        */
                    END.
                END.
            END. 
        END. 
        PROCESS EVENTS. 
    END.
    
    DO datum = d2 TO to-date: 
        FOR EACH kontline WHERE kontline.ankunft LE datum 
            AND kontline.abreise GE datum AND kontline.betriebsnr = 1 
            AND kontline.kontstat = 1 NO-LOCK: 
            do-it = YES. 
    
            IF do-it THEN 
            DO: 
              /*MT
              FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
              ASSIGN
                room-list.room[16] = room-list.room[16] + kontline.zimmeranz
                room-list.room[17] = room-list.room[17] 
                  + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                  * kontline.zimmeranz
                rm-array[16] = rm-array[16] + kontline.zimmeranz
                rm-array[17] = rm-array[17] 
                  + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                  * kontline.zimmeranz
              . 
              */
            END. 
        END. 
        PROCESS EVENTS.
    END.
END.
