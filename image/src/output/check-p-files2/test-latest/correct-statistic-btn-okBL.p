
DEFINE TEMP-TABLE t-segmentstat LIKE segmentstat.
DEFINE TEMP-TABLE t-sources     LIKE sources.

DEF INPUT PARAMETER fdate   AS DATE     NO-UNDO.
DEF INPUT PARAMETER tdate   AS DATE     NO-UNDO.
DEF INPUT PARAMETER rm-serv AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER rm-vat  AS LOGICAL  NO-UNDO.

DEFINE VARIABLE bill-date   AS DATE     NO-UNDO.
DEFINE VARIABLE curr-i      AS INTEGER  NO-UNDO.
DEFINE VARIABLE vat         AS DECIMAL  NO-UNDO.
DEFINE VARIABLE vat2        AS DECIMAL  NO-UNDO.
DEFINE VARIABLE service     AS DECIMAL  NO-UNDO.
DEFINE VARIABLE fact-scvat  AS DECIMAL  NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
rm-vat = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
rm-serv = htparam.flogical. 

DO TRANSACTION:
    RUN reorg-stat.
    RUN reorg-guestat.
END.


PROCEDURE reorg-stat:
   DEF VAR anz      AS INTEGER NO-UNDO.
   DEF VAR isSharer AS LOGICAL INITIAL NO.
   DEF VAR do-it    AS LOGICAL INITIAL YES.
   DEF BUFFER segbuff  FOR segmentstat.
   DEF BUFFER natbuff  FOR nationstat. 
   DEF BUFFER nsbuff   FOR natstat1.
   DEF BUFFER scbuff   FOR sources.
   DEF BUFFER landbuff FOR landstat.
   DEF BUFFER gsbuff   FOR guestat1.
   DEF BUFFER gubuff   FOR guestat.
   DEF BUFFER zibuff   FOR zinrstat.
   DEF BUFFER genbuff  FOR genstat.
   DEF BUFFER zimbuff  FOR zimmer.
   DEF BUFFER zkbuff   FOR zkstat.

   DEFINE VARIABLE num-date AS INTEGER. /* Malik Serverless 627 */

   DO bill-date = fdate TO tdate:
       FIND FIRST segmentstat WHERE segmentstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE segmentstat:
         DO TRANSACTION:
           FIND FIRST segbuff WHERE RECID(segbuff) = RECID(segmentstat)
               EXCLUSIVE-LOCK.
           /*MT*/
           CREATE t-segmentstat.
           ASSIGN
               t-segmentstat.datum = bill-date
               t-segmentstat.segmentcode = segbuff.segmentcode
               t-segmentstat.budlogis = segbuff.budlogis
               t-segmentstat.budzimmeranz = segbuff.budzimmeranz
               t-segmentstat.budpersanz = segbuff.budpersanz.
           /*MT*/
           DELETE segbuff.
           RELEASE segbuff.
         END.
         FIND NEXT segmentstat WHERE segmentstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST nationstat WHERE nationstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE nationstat:
         DO TRANSACTION:
           FIND FIRST natbuff WHERE RECID(natbuff) = RECID(nationstat)
               EXCLUSIVE-LOCK.
           DELETE natbuff.
           RELEASE natbuff.
         END.
         FIND NEXT nationstat WHERE nationstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST natstat1 WHERE natstat1.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE natstat1:
         DO TRANSACTION:
           FIND FIRST nsbuff WHERE RECID(nsbuff) = RECID(natstat1) 
               EXCLUSIVE-LOCK.
           DELETE nsbuff.
           RELEASE nsbuff.
         END.
         FIND NEXT natstat1 WHERE natstat1.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST sources WHERE sources.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE sources:
         DO TRANSACTION:
           FIND FIRST scbuff WHERE RECID(scbuff) = RECID(sources)
               EXCLUSIVE-LOCK.
           /*FT*/
           CREATE t-sources.
           ASSIGN
               t-sources.datum = bill-date
               t-sources.source-code = scbuff.source-code
               t-sources.budlogis = scbuff.budlogis
               t-sources.budzimmeranz = scbuff.budzimmeranz
               t-sources.budpersanz = scbuff.budpersanz.
           /*FT*/
           DELETE scbuff.
           RELEASE scbuff.
         END.
         FIND NEXT sources WHERE sources.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST landstat WHERE landstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE landstat:
         DO TRANSACTION:
           FIND FIRST landbuff WHERE RECID(landbuff) = RECID(landstat)
               EXCLUSIVE-LOCK.
           DELETE landstat.
           RELEASE landstat.
         END.
         FIND NEXT landstat WHERE landstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST guestat1 WHERE guestat1.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE guestat1:
         DO TRANSACTION:
           FIND FIRST gsbuff WHERE RECID(gsbuff) = RECID(guestat1) 
               EXCLUSIVE-LOCK .
           DELETE gsbuff.
           RELEASE gsbuff.
         END.
         FIND NEXT guestat1 WHERE guestat1.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST guestat WHERE guestat.jahr = YEAR(bill-date) 
           AND guestat.monat = MONTH(bill-date) NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE guestat:
         DO TRANSACTION:
           FIND FIRST gubuff WHERE RECID(gubuff) = RECID(guestat)
               EXCLUSIVE-LOCK.
           DELETE gubuff.
           RELEASE gubuff.
         END.
         FIND NEXT guestat WHERE guestat.jahr = YEAR(bill-date) 
             AND guestat.monat = MONTH(bill-date) NO-LOCK NO-ERROR.
       END.

       FIND FIRST zinrstat WHERE zinrstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE zinrstat:
         FIND FIRST zimmer WHERE zimmer.zinr = zinrstat.zinr NO-LOCK
           NO-ERROR.
         IF AVAILABLE zimmer THEN
         DO TRANSACTION:
           FIND FIRST zibuff WHERE RECID(zibuff) = RECID(zinrstat)
               EXCLUSIVE-LOCK.
           DELETE zibuff.
           RELEASE zibuff.
         END.
         FIND NEXT zinrstat WHERE zinrstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST zkstat WHERE zkstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE zkstat:
         DO TRANSACTION:
           FIND FIRST zkbuff WHERE RECID(zkbuff) = RECID(zkstat) EXCLUSIVE-LOCK.
           ASSIGN
               zkbuff.personen             = 0
               zkbuff.anz-ankunft          = 0
               zkbuff.anz-abr              = 0
               zkbuff.betriebsnr           = 0
           .
           DO curr-i = 1 TO 9:
               ASSIGN
                   zkbuff.arrangement-art[curr-i] = 0
                   zkbuff.anz100argtart[curr-i]   = 0
               .
           END.
           FIND CURRENT zkbuff NO-LOCK.
           RELEASE zkbuff.
         END.
         FIND NEXT zkstat WHERE zkstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FOR EACH genstat WHERE genstat.datum = bill-date AND genstat.resstatus = 13
           AND genstat.zipreis GT 0 NO-LOCK:
           FIND FIRST genbuff WHERE genbuff.datum = bill-date 
               AND genbuff.zinr = genstat.zinr AND genbuff.resstatus = 6 NO-LOCK NO-ERROR.
           IF NOT AVAILABLE genbuff THEN
           DO TRANSACTION:
               FIND FIRST genbuff WHERE RECID(genbuff) = RECID(genstat) EXCLUSIVE-LOCK.
               ASSIGN genbuff.resstatus = 6.
               FIND CURRENT genbuff NO-LOCK.
           END.
       END.

       FOR EACH genstat WHERE genstat.datum = bill-date AND genstat.zinr NE ""
           AND genstat.res-logic[2] EQ YES NO-LOCK:
           do-it = YES.
           IF genstat.res-date[2] = bill-date AND genstat.resstatus = 8
               AND genstat.zipreis = 0 THEN
           DO:
               FIND FIRST genbuff WHERE RECID(genbuff) = RECID(genstat)
                   EXCLUSIVE-LOCK.
               DELETE genbuff.
               RELEASE genbuff.
               do-it = NO.
           END.
           IF do-it THEN
           DO:
               FIND FIRST segmentstat WHERE segmentstat.datum = bill-date
                   AND segmentstat.segmentcode = genstat.segmentcode 
                   EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE segmentstat THEN
               DO: 
                   CREATE segmentstat.
                   ASSIGN segmentstat.datum = bill-date
                          segmentstat.segmentcode = genstat.segmentcode.
               END.
               isSharer = genstat.resstatus = 13.

               /*IF ((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                            AND genstat.resstatus NE 13)) THEN*/
               IF NOT isSharer THEN
               DO:
                   segmentstat.zimmeranz  = segmentstat.zimmeranz  + 1.
                   IF genstat.zipreis = 0 AND (genstat.gratis GT 0) THEN
                    segmentstat.betriebsnr = segmentstat.betriebsnr + 1.
               END.

               ASSIGN
                      /*segmentstat.zimmeranz  = segmentstat.zimmeranz  + 1*/
                      segmentstat.persanz    = segmentstat.persanz    + genstat.erwachs
                      segmentstat.kind1      = segmentstat.kind1      + genstat.kind1
                                             + genstat.kind3
                      segmentstat.kind2      = segmentstat.kind2      + genstat.kind2 
                      segmentstat.gratis     = segmentstat.gratis     + genstat.gratis 
                      segmentstat.logis      = segmentstat.logis      + genstat.logis
                    .  

               FIND CURRENT segmentstat NO-LOCK.
               IF genstat.domestic NE 0 THEN
               DO:
                   FIND FIRST nationstat WHERE nationstat.datum = bill-date 
                     AND nationstat.nationnr = genstat.domestic EXCLUSIVE-LOCK NO-ERROR.
                   IF NOT AVAILABLE nationstat THEN
                   DO:
                     CREATE nationstat.
                     ASSIGN nationstat.datum = bill-date
                         nationstat.nationnr = genstat.domestic.
                   END.
                   IF NOT isSharer THEN
                   DO: 
                    nationstat.dankzimmer = nationstat.dankzimmer + 1. 
                    IF genstat.zipreis EQ 0 THEN nationstat.betriebsnr = nationstat.betriebsnr + 1. 
                   END. 
                   ASSIGN
                     nationstat.logerwachs  = nationstat.logerwachs + genstat.erwachs
                     nationstat.loggratis   = nationstat.loggratis + genstat.gratis
                     nationstat.logkind1    = nationstat.logkind1 + genstat.kind1 + genstat.kind3
                     nationstat.logkind2    = nationstat.logkind2 + genstat.kind2
                   . 
                   IF NOT isSharer AND genstat.res-date[1] = bill-date THEN 
                   ASSIGN
                     nationstat.ankerwachs   = nationstat.ankerwachs + genstat.erwachs
                     nationstat.ankkind1     = nationstat.ankkind1 + genstat.kind1 + genstat.kind3
                     nationstat.ankkind2     = nationstat.ankkind2 + genstat.kind2 
                     nationstat.ankgratis    = nationstat.ankgratis + genstat.gratis
                   . 
                   FIND CURRENT nationstat NO-LOCK.
               END.

               FIND FIRST nationstat WHERE nationstat.datum = bill-date 
                   AND nationstat.nationnr = genstat.nationnr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE nationstat THEN
               DO:
                   CREATE nationstat.
                   ASSIGN nationstat.datum = bill-date
                       nationstat.nationnr = genstat.nationnr.
               END.

               IF /*(genstat.resstatus = 6) OR ((genstat.res-date[1] = genstat.res-date[2])
                                                  AND genstat.resstatus NE 13)*/
                   NOT isSharer THEN
               DO: 
                   nationstat.dankzimmer = nationstat.dankzimmer + 1. 
                   IF genstat.zipreis EQ 0 THEN nationstat.betriebsnr = nationstat.betriebsnr + 1. 
               END. 

               ASSIGN
                   nationstat.logerwachs  = nationstat.logerwachs + genstat.erwachs
                   nationstat.loggratis   = nationstat.loggratis + genstat.gratis
                   nationstat.logkind1    = nationstat.logkind1 + genstat.kind1 + genstat.kind3
                   nationstat.logkind2    = nationstat.logkind2 + genstat.kind2
                 . 

               /*IF genstat.zipreis = 0 AND genstat.resstatus NE 13 
                   AND genstat.erwachs GT 0  THEN 
                 nationstat.loggratis = nationstat.loggratis + genstat.erwachs.*/

               IF /*((genstat.resstatus = 6) OR ((genstat.res-date[1] = genstat.res-date[2])
                                               AND genstat.resstatus NE 13))*/
                  NOT isSharer
                  AND genstat.res-date[1] = bill-date THEN 
                ASSIGN
                  nationstat.ankerwachs   = nationstat.ankerwachs + genstat.erwachs
                  nationstat.ankkind1     = nationstat.ankkind1 + genstat.kind1 + genstat.kind3
                  nationstat.ankkind2     = nationstat.ankkind2 + genstat.kind2 
                  nationstat.ankgratis    = nationstat.ankgratis + genstat.gratis
                . 
               /* Malik Serverless 627 update operation beetween date and integer */ 
               IF genstat.res-date[2] > genstat.res-date[1] THEN 
               DO:
                num-date = genstat.res-date[2] - genstat.res-date[1].
                /* nationstat.dlogkind1 = nationstat.dlogkind1 
                  + genstat.res-date[2] - genstat.res-date[1]. */
                  nationstat.dlogkind1 = nationstat.dlogkind1  + num-date.
               END.   
               ELSE
               DO:
                nationstat.dlogkind1 = nationstat.dlogkind1 + 1. 
               END.
               /* END Malik */
               /* used FOR number OF number OF stay 
                 thus average stay = dlogkind1 / dlogkind2 */ 
               nationstat.dlogkind2 = nationstat.dlogkind2 + 1.

               FIND CURRENT nationstat NO-LOCK.

               FIND FIRST natstat1 WHERE natstat1.datum = bill-date AND 
                   natstat1.nationnr = genstat.nationnr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE natstat1 THEN
               DO:
                   CREATE natstat1.
                   ASSIGN natstat1.datum = bill-date
                       natstat1.nationnr = genstat.nationnr.
               END.
               IF NOT isSharer THEN
               DO:
                   natstat1.zimmeranz = natstat1.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN natstat1.betriebsnr = natstat1.betriebsnr + 1. 
               END.
               natstat1.persanz = natstat1.persanz + genstat.erwachs 
                + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN natstat1.logis = natstat1.logis + genstat.logis. 
               FIND CURRENT natstat1 NO-LOCK.

               IF genstat.domestic NE 0 THEN
               DO:
                 FIND FIRST natstat1 WHERE natstat1.datum = bill-date AND 
                   natstat1.nationnr = genstat.domestic EXCLUSIVE-LOCK NO-ERROR.
                 IF NOT AVAILABLE natstat1 THEN
                 DO:
                   CREATE natstat1.
                   ASSIGN natstat1.datum = bill-date
                       natstat1.nationnr = genstat.domestic.
                 END.
                 IF NOT isSharer THEN
                 DO:
                   natstat1.zimmeranz = natstat1.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN natstat1.betriebsnr = natstat1.betriebsnr + 1. 
                 END.
                 natstat1.persanz = natstat1.persanz + genstat.erwachs 
                   + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
                 IF genstat.zipreis NE 0 THEN natstat1.logis = natstat1.logis + genstat.logis. 
                 FIND CURRENT natstat1 NO-LOCK.
               END.

               FIND FIRST sources WHERE sources.datum = bill-date AND
                   sources.source-code = genstat.SOURCE EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE sources THEN
               DO:
                   CREATE sources.
                   ASSIGN sources.datum = bill-date
                       sources.source-code = genstat.SOURCE.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2]
                                                   AND genstat.resstatus NE 13))*/
                 NOT isSharer THEN
               DO: 
                 sources.zimmeranz = sources.zimmeranz + 1. 
                 IF genstat.zipreis EQ 0 THEN sources.betriebsnr = sources.betriebsnr + 1. 
               END. 

               ASSIGN
                   sources.persanz = sources.persanz + genstat.erwachs 
                     + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN sources.logis = sources.logis + genstat.logis. 

               FIND CURRENT sources NO-LOCK.

               FIND FIRST landstat WHERE landstat.datum = bill-date AND
                   landstat.nationnr = genstat.resident EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE landstat THEN
               DO:
                   CREATE landstat.
                   ASSIGN landstat.datum = bill-date
                       landstat.nationnr = genstat.resident.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                                 AND genstat.resstatus NE 13))*/
                  NOT isSharer THEN
               DO: 
                   landstat.zimmeranz = landstat.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN landstat.betriebsnr = landstat.betriebsnr + 1. 
               END. 
               landstat.persanz = landstat.persanz + genstat.erwachs 
                   + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN landstat.logis = landstat.logis + genstat.logis. 
               FIND CURRENT landstat NO-LOCK.

               FIND FIRST guestat1 WHERE guestat1.datum = bill-date AND guestat1.gastnr 
                   = genstat.gastnr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE guestat1 THEN
               DO:
                   CREATE guestat1.
                   ASSIGN guestat1.datum = bill-date
                       guestat1.gastnr = genstat.gastnr.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                                 AND genstat.resstatus NE 13))*/
                   NOT isSharer THEN
               DO: 
                   guestat1.zimmeranz = guestat1.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN guestat1.betriebsnr = guestat1.betriebsnr + 1. 
               END. 
               guestat1.persanz = guestat1.persanz + genstat.erwachs 
                   + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN guestat1.logis = guestat1.logis + genstat.logis. 
               FIND CURRENT guestat1 NO-LOCK.

               FIND FIRST zinrstat WHERE zinrstat.datum = bill-date AND
                  zinrstat.zinr = genstat.zinr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE zinrstat THEN
               DO:
                  CREATE zinrstat.
                  ASSIGN zinrstat.datum = bill-date
                      zinrstat.zinr = genstat.zinr.
               END.
               FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR.
               IF AVAILABLE arrangement THEN
               DO:
                    FIND FIRST artikel WHERE artikel.artnr = arrangement.artnr-logis 
                       AND artikel.departement = 0 NO-LOCK NO-ERROR. 
                    IF AVAILABLE artikel THEN
                    DO:
                       /* SY AUG 13 2017 */
                       RUN calc-servtaxesbl.p(2, artikel.artnr, artikel.departement,
                           bill-date, OUTPUT service, OUTPUT vat, OUTPUT vat2, 
                           OUTPUT fact-scvat).
/*                       
                       IF rm-serv THEN
                       DO:
                         FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code 
                           NO-LOCK NO-ERROR. 
                         IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                           service = htparam.fdecimal / 100. 
                       END.
                       IF rm-vat THEN
                       DO:
                         FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code 
                           NO-LOCK NO-ERROR. 
                         IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                           vat = htparam.fdecimal / 100. 
                         FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
                         IF htparam.flogical THEN vat = vat + vat * service. 
                         vat = round(vat, 2). 
                       END.
*/                       
                    END.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                            AND genstat.resstatus NE 13))*/
                   NOT isSharer THEN
               DO: 
                 zinrstat.zimmeranz = zinrstat.zimmeranz + 1. 
                 IF genstat.zipreis EQ 0 THEN zinrstat.betriebsnr = zinrstat.betriebsnr + 1. 
               END. 
               zinrstat.personen = zinrstat.personen + genstat.erwachs 
                 + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 

               IF genstat.rateLocal NE 0 THEN /* Malik Serverless 627 genstat.rate -> genstat.rateLocal */
               ASSIGN
                 zinrstat.logisumsatz  = zinrstat.logisumsatz + genstat.logis
                 zinrstat.argtumsatz   = zinrstat.argtumsatz + genstat.rateLocal / fact-scvat.
               IF rm-serv THEN
                 zinrstat.gesamtumsatz = zinrstat.gesamtumsatz + genstat.rateLocal * fact-scvat. 
               ELSE zinrstat.gesamtumsatz = zinrstat.gesamtumsatz + genstat.rateLocal. 

               FIND FIRST zkstat WHERE zkstat.zikatnr = genstat.zikatnr AND
                   zkstat.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE zkstat THEN
               DO:
                   CREATE zkstat.
                   ASSIGN zkstat.datum = bill-date
                       zkstat.zikatnr = genstat.zikatnr.
               END.
               anz = 0. 
               FOR EACH zimbuff WHERE zimbuff.zikatnr = genstat.zikatnr 
                 AND zimbuff.sleeping NO-LOCK: 
                 anz = anz + 1. 
               END. 
               IF NOT isSharer THEN
               DO:
                   ASSIGN zkstat.zimmeranz = zkstat.zimmeranz + 1.
                   IF genstat.zipreis = 0 THEN
                       zkstat.betriebsnr = zkstat.betriebsnr + 1.
               END.
               ASSIGN
                   zkstat.personen = zkstat.personen +  genstat.erwachs + genstat.kind1 + 
                   genstat.kind2 + genstat.kind3 + genstat.gratis.
               IF genstat.zipreis = 0  THEN
               DO: 
                   /*zkstat.betriebsnr = zkstat.betriebsnr + 1.*/
                   IF genstat.gratis = 0 AND (genstat.erwachs + genstat.kind1) GT 0 THEN 
                     zkstat.arrangement-art[1] = zkstat.arrangement-art[1] + 1. /* comp B */ 
               END.
               IF genstat.res-date[1] = bill-date AND genstat.res-date[2] GT bill-date THEN
                   zkstat.anz-ankunft = zkstat.anz-ankunft + 1.
               IF genstat.res-date[1] = genstat.res-date[2] THEN
                   zkstat.anz-abr = zkstat.anz-abr + 1.
               FIND CURRENT zkstat NO-LOCK.
           END. /* IF do-it */
        END.
    
    /*    FOR EACH genbuff WHERE YEAR(genbuff.datum) = YEAR(bill-date) 
            AND MONTH(genbuff.datum) = MONTH(bill-date) AND genbuff.zinr NE "" NO-LOCK:
            FIND FIRST guestat WHERE guestat.monat = MONTH(bill-date) 
                AND guestat.jahr = YEAR(bill-date)
                AND guestat.gastnr = genbuff.gastnr EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE guestat THEN
            DO:
                CREATE guestat.
                ASSIGN guestat.monat = MONTH(bill-date)
                    guestat.jahr = YEAR(bill-date)
                    guestat.gastnr = genbuff.gastnr.
            END.
            IF genbuff.resstatus = 6 OR (genbuff.res-date[1] = genbuff.res-date[2] 
                                     AND genbuff.resstatus NE 13) THEN
            guestat.room-nights = guestat.room-nights  + 1.
            FIND CURRENT guestat NO-LOCK.
    
        END.*/

          /*MT*/
          DO:
              FOR EACH t-segmentstat :
                  FIND FIRST segmentstat WHERE segmentstat.datum = t-segmentstat.datum
                      AND segmentstat.segmentcode = t-segmentstat.segmentcode
                      NO-ERROR.
                  IF NOT AVAILABLE segmentstat THEN
                  DO:
                      CREATE segmentstat.
                      ASSIGN segmentstat.datum = t-segmentstat.datum
                             segmentstat.segmentcode = t-segmentstat.segmentcode.
                  END.
                  ASSIGN
                      segmentstat.budlogis = t-segmentstat.budlogis
                      segmentstat.budzimmeranz = t-segmentstat.budzimmeranz
                      segmentstat.budpersanz = t-segmentstat.budpersanz.
              END.
          END.
          /*MT*/

          /*FT*/
          DO:
              FOR EACH t-sources :
                  FIND FIRST sources WHERE sources.datum = t-sources.datum
                      AND sources.source-code = t-sources.source-code
                      NO-ERROR.
                  IF NOT AVAILABLE sources THEN
                  DO:
                      CREATE sources.
                      ASSIGN sources.datum = t-sources.datum
                             sources.source-code = t-sources.source-code.
                  END.
                  ASSIGN
                      sources.budlogis = t-sources.budlogis
                      sources.budzimmeranz = t-sources.budzimmeranz
                      sources.budpersanz = t-sources.budpersanz.
              END.
          END.
          /*FT*/
   END.
END.

PROCEDURE reorg-guestat:
    DEF VAR dd AS DATE.
    DEF VAR mm AS INTEGER.
    DEF VAR yy AS INTEGER. 
    DEF BUFFER genbuff FOR genstat.

    DO mm = MONTH(fdate) TO MONTH(tdate):
         FOR EACH genbuff WHERE YEAR(genbuff.datum) = YEAR(fdate) 
            AND MONTH(genbuff.datum) = mm AND genbuff.zinr NE "" NO-LOCK:
            FIND FIRST guestat WHERE guestat.monat = mm
                AND guestat.jahr = YEAR(fdate)
                AND guestat.gastnr = genbuff.gastnr EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE guestat THEN
            DO:
                CREATE guestat.
                ASSIGN guestat.monat = MONTH(bill-date)
                    guestat.jahr = YEAR(bill-date)
                    guestat.gastnr = genbuff.gastnr.
            END.
            IF genbuff.resstatus NE 13 THEN
            guestat.room-nights = guestat.room-nights  + 1.
            FIND CURRENT guestat NO-LOCK.
        END.
    END.
    
END. 

/*MT
PROCEDURE reorg-stat:
   DEF VAR anz      AS INTEGER NO-UNDO.
   DEF VAR isSharer AS LOGICAL INITIAL NO.
   DEF VAR do-it    AS LOGICAL INITIAL YES.
   DEF BUFFER segbuff  FOR segmentstat.
   DEF BUFFER natbuff  FOR nationstat. 
   DEF BUFFER nsbuff   FOR natstat1.
   DEF BUFFER scbuff   FOR sources.
   DEF BUFFER landbuff FOR landstat.
   DEF BUFFER gsbuff   FOR guestat1.
   DEF BUFFER gubuff   FOR guestat.
   DEF BUFFER zibuff   FOR zinrstat.
   DEF BUFFER genbuff  FOR genstat.
   DEF BUFFER zimbuff  FOR zimmer.
   DEF BUFFER zkbuff   FOR zkstat.

   DO bill-date = fdate TO tdate:
       FIND FIRST segmentstat WHERE segmentstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE segmentstat:
         DO TRANSACTION:
           FIND FIRST segbuff WHERE RECID(segbuff) = RECID(segmentstat)
               EXCLUSIVE-LOCK.
           /*MT*/
           CREATE t-segmentstat.
           ASSIGN
               t-segmentstat.datum = bill-date
               t-segmentstat.segmentcode = segbuff.segmentcode
               t-segmentstat.budlogis = segbuff.budlogis
               t-segmentstat.budzimmeranz = segbuff.budzimmeranz
               t-segmentstat.budpersanz = segbuff.budpersanz.
           /*MT*/
           DELETE segbuff.
           RELEASE segbuff.
         END.
         FIND NEXT segmentstat WHERE segmentstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST nationstat WHERE nationstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE nationstat:
         DO TRANSACTION:
           FIND FIRST natbuff WHERE RECID(natbuff) = RECID(nationstat)
               EXCLUSIVE-LOCK.
           DELETE natbuff.
           RELEASE natbuff.
         END.
         FIND NEXT nationstat WHERE nationstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST natstat1 WHERE natstat1.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE natstat1:
         DO TRANSACTION:
           FIND FIRST nsbuff WHERE RECID(nsbuff) = RECID(natstat1) 
               EXCLUSIVE-LOCK.
           DELETE nsbuff.
           RELEASE nsbuff.
         END.
         FIND NEXT natstat1 WHERE natstat1.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST sources WHERE sources.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE sources:
         DO TRANSACTION:
           FIND FIRST scbuff WHERE RECID(scbuff) = RECID(sources)
               EXCLUSIVE-LOCK.
           /*FT*/
           CREATE t-sources.
           ASSIGN
               t-sources.datum = bill-date
               t-sources.source-code = scbuff.source-code
               t-sources.budlogis = scbuff.budlogis
               t-sources.budzimmeranz = scbuff.budzimmeranz
               t-sources.budpersanz = scbuff.budpersanz.
           /*FT*/
           DELETE scbuff.
           RELEASE scbuff.
         END.
         FIND NEXT sources WHERE sources.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST landstat WHERE landstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE landstat:
         DO TRANSACTION:
           FIND FIRST landbuff WHERE RECID(landbuff) = RECID(landstat)
               EXCLUSIVE-LOCK.
           DELETE landstat.
           RELEASE landstat.
         END.
         FIND NEXT landstat WHERE landstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST guestat1 WHERE guestat1.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE guestat1:
         DO TRANSACTION:
           FIND FIRST gsbuff WHERE RECID(gsbuff) = RECID(guestat1) 
               EXCLUSIVE-LOCK .
           DELETE gsbuff.
           RELEASE gsbuff.
         END.
         FIND NEXT guestat1 WHERE guestat1.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST guestat WHERE guestat.jahr = YEAR(bill-date) 
           AND guestat.monat = MONTH(bill-date) NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE guestat:
         DO TRANSACTION:
           FIND FIRST gubuff WHERE RECID(gubuff) = RECID(guestat)
               EXCLUSIVE-LOCK.
           DELETE gubuff.
           RELEASE gubuff.
         END.
         FIND NEXT guestat WHERE guestat.jahr = YEAR(bill-date) 
             AND guestat.monat = MONTH(bill-date) NO-LOCK NO-ERROR.
       END.

       FIND FIRST zinrstat WHERE zinrstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE zinrstat:
         FIND FIRST zimmer WHERE zimmer.zinr = zinrstat.zinr NO-LOCK
           NO-ERROR.
         IF AVAILABLE zimmer THEN
         DO TRANSACTION:
           FIND FIRST zibuff WHERE RECID(zibuff) = RECID(zinrstat)
               EXCLUSIVE-LOCK.
           DELETE zibuff.
           RELEASE zibuff.
         END.
         FIND NEXT zinrstat WHERE zinrstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FIND FIRST zkstat WHERE zkstat.datum = bill-date NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE zkstat:
         DO TRANSACTION:
           FIND FIRST zkbuff WHERE RECID(zkbuff) = RECID(zkstat) EXCLUSIVE-LOCK.
           ASSIGN
               zkbuff.personen             = 0
               zkbuff.anz-ankunft          = 0
               zkbuff.anz-abr              = 0
               zkbuff.betriebsnr           = 0
           .
           DO curr-i = 1 TO 9:
               ASSIGN
                   zkbuff.arrangement-art[curr-i] = 0
                   zkbuff.anz100argtart[curr-i]   = 0
               .
           END.
           FIND CURRENT zkbuff NO-LOCK.
           RELEASE zkbuff.
         END.
         FIND NEXT zkstat WHERE zkstat.datum = bill-date NO-LOCK NO-ERROR.
       END.

       FOR EACH genstat WHERE genstat.datum = bill-date AND genstat.resstatus = 13
           AND genstat.zipreis GT 0 NO-LOCK:
           FIND FIRST genbuff WHERE genbuff.datum = bill-date 
               AND genbuff.zinr = genstat.zinr AND genbuff.resstatus = 6 NO-LOCK NO-ERROR.
           IF NOT AVAILABLE genbuff THEN
           DO TRANSACTION:
               FIND FIRST genbuff WHERE RECID(genbuff) = RECID(genstat) EXCLUSIVE-LOCK.
               ASSIGN genbuff.resstatus = 6.
               FIND CURRENT genbuff NO-LOCK.
           END.
       END.

       FOR EACH genstat WHERE genstat.datum = bill-date AND genstat.zinr NE ""
           AND genstat.res-logic[2] EQ YES NO-LOCK:
           do-it = YES.
           IF genstat.res-date[2] = bill-date AND genstat.resstatus = 8
               AND genstat.zipreis = 0 THEN
           DO:
               FIND FIRST genbuff WHERE RECID(genbuff) = RECID(genstat)
                   EXCLUSIVE-LOCK.
               DELETE genbuff.
               RELEASE genbuff.
               do-it = NO.
           END.
           IF do-it THEN
           DO:
               FIND FIRST segmentstat WHERE segmentstat.datum = bill-date
                   AND segmentstat.segmentcode = genstat.segmentcode 
                   EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE segmentstat THEN
               DO: 
                   CREATE segmentstat.
                   ASSIGN segmentstat.datum = bill-date
                          segmentstat.segmentcode = genstat.segmentcode.
               END.
               isSharer = genstat.resstatus = 13.

               /*IF ((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                            AND genstat.resstatus NE 13)) THEN*/
               IF NOT isSharer THEN
               DO:
                   segmentstat.zimmeranz  = segmentstat.zimmeranz  + 1.
                   IF genstat.zipreis = 0 AND (genstat.gratis GT 0) THEN
                    segmentstat.betriebsnr = segmentstat.betriebsnr + 1.
               END.

               ASSIGN
                      /*segmentstat.zimmeranz  = segmentstat.zimmeranz  + 1*/
                      segmentstat.persanz    = segmentstat.persanz    + genstat.erwachs
                      segmentstat.kind1      = segmentstat.kind1      + genstat.kind1
                                             + genstat.kind3
                      segmentstat.kind2      = segmentstat.kind2      + genstat.kind2 
                      segmentstat.gratis     = segmentstat.gratis     + genstat.gratis 
                      segmentstat.logis      = segmentstat.logis      + genstat.logis
                    .  

               FIND CURRENT segmentstat NO-LOCK.
               IF genstat.domestic NE 0 THEN
               DO:
                   FIND FIRST nationstat WHERE nationstat.datum = bill-date 
                     AND nationstat.nationnr = genstat.domestic EXCLUSIVE-LOCK NO-ERROR.
                   IF NOT AVAILABLE nationstat THEN
                   DO:
                     CREATE nationstat.
                     ASSIGN nationstat.datum = bill-date
                         nationstat.nationnr = genstat.domestic.
                   END.
                   IF NOT isSharer THEN
                   DO: 
                    nationstat.dankzimmer = nationstat.dankzimmer + 1. 
                    IF genstat.zipreis EQ 0 THEN nationstat.betriebsnr = nationstat.betriebsnr + 1. 
                   END. 
                   ASSIGN
                     nationstat.logerwachs  = nationstat.logerwachs + genstat.erwachs
                     nationstat.loggratis   = nationstat.loggratis + genstat.gratis
                     nationstat.logkind1    = nationstat.logkind1 + genstat.kind1 + genstat.kind3
                     nationstat.logkind2    = nationstat.logkind2 + genstat.kind2
                   . 
                   IF NOT isSharer AND genstat.res-date[1] = bill-date THEN 
                   ASSIGN
                     nationstat.ankerwachs   = nationstat.ankerwachs + genstat.erwachs
                     nationstat.ankkind1     = nationstat.ankkind1 + genstat.kind1 + genstat.kind3
                     nationstat.ankkind2     = nationstat.ankkind2 + genstat.kind2 
                     nationstat.ankgratis    = nationstat.ankgratis + genstat.gratis
                   . 
                   FIND CURRENT nationstat NO-LOCK.
               END.

               FIND FIRST nationstat WHERE nationstat.datum = bill-date 
                   AND nationstat.nationnr = genstat.nationnr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE nationstat THEN
               DO:
                   CREATE nationstat.
                   ASSIGN nationstat.datum = bill-date
                       nationstat.nationnr = genstat.nationnr.
               END.

               IF /*(genstat.resstatus = 6) OR ((genstat.res-date[1] = genstat.res-date[2])
                                                  AND genstat.resstatus NE 13)*/
                   NOT isSharer THEN
               DO: 
                   nationstat.dankzimmer = nationstat.dankzimmer + 1. 
                   IF genstat.zipreis EQ 0 THEN nationstat.betriebsnr = nationstat.betriebsnr + 1. 
               END. 

               ASSIGN
                   nationstat.logerwachs  = nationstat.logerwachs + genstat.erwachs
                   nationstat.loggratis   = nationstat.loggratis + genstat.gratis
                   nationstat.logkind1    = nationstat.logkind1 + genstat.kind1 + genstat.kind3
                   nationstat.logkind2    = nationstat.logkind2 + genstat.kind2
                 . 

               /*IF genstat.zipreis = 0 AND genstat.resstatus NE 13 
                   AND genstat.erwachs GT 0  THEN 
                 nationstat.loggratis = nationstat.loggratis + genstat.erwachs.*/

               IF /*((genstat.resstatus = 6) OR ((genstat.res-date[1] = genstat.res-date[2])
                                               AND genstat.resstatus NE 13))*/
                  NOT isSharer
                  AND genstat.res-date[1] = bill-date THEN 
                ASSIGN
                  nationstat.ankerwachs   = nationstat.ankerwachs + genstat.erwachs
                  nationstat.ankkind1     = nationstat.ankkind1 + genstat.kind1 + genstat.kind3
                  nationstat.ankkind2     = nationstat.ankkind2 + genstat.kind2 
                  nationstat.ankgratis    = nationstat.ankgratis + genstat.gratis
                . 

               IF genstat.res-date[2] > genstat.res-date[1] THEN 
                nationstat.dlogkind1 = nationstat.dlogkind1 
                  + genstat.res-date[2] - genstat.res-date[1]. 
               ELSE nationstat.dlogkind1 = nationstat.dlogkind1 + 1. 
               /* used FOR number OF number OF stay 
                 thus average stay = dlogkind1 / dlogkind2 */ 
               nationstat.dlogkind2 = nationstat.dlogkind2 + 1.

               FIND CURRENT nationstat NO-LOCK.

               FIND FIRST natstat1 WHERE natstat1.datum = bill-date AND 
                   natstat1.nationnr = genstat.nationnr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE natstat1 THEN
               DO:
                   CREATE natstat1.
                   ASSIGN natstat1.datum = bill-date
                       natstat1.nationnr = genstat.nationnr.
               END.
               IF NOT isSharer THEN
               DO:
                   natstat1.zimmeranz = natstat1.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN natstat1.betriebsnr = natstat1.betriebsnr + 1. 
               END.
               natstat1.persanz = natstat1.persanz + genstat.erwachs 
                + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN natstat1.logis = natstat1.logis + genstat.logis. 
               FIND CURRENT natstat1 NO-LOCK.

               IF genstat.domestic NE 0 THEN
               DO:
                 FIND FIRST natstat1 WHERE natstat1.datum = bill-date AND 
                   natstat1.nationnr = genstat.domestic EXCLUSIVE-LOCK NO-ERROR.
                 IF NOT AVAILABLE natstat1 THEN
                 DO:
                   CREATE natstat1.
                   ASSIGN natstat1.datum = bill-date
                       natstat1.nationnr = genstat.domestic.
                 END.
                 IF NOT isSharer THEN
                 DO:
                   natstat1.zimmeranz = natstat1.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN natstat1.betriebsnr = natstat1.betriebsnr + 1. 
                 END.
                 natstat1.persanz = natstat1.persanz + genstat.erwachs 
                   + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
                 IF genstat.zipreis NE 0 THEN natstat1.logis = natstat1.logis + genstat.logis. 
                 FIND CURRENT natstat1 NO-LOCK.
               END.

               FIND FIRST sources WHERE sources.datum = bill-date AND
                   sources.source-code = genstat.SOURCE EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE sources THEN
               DO:
                   CREATE sources.
                   ASSIGN sources.datum = bill-date
                       sources.source-code = genstat.SOURCE.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2]
                                                   AND genstat.resstatus NE 13))*/
                 NOT isSharer THEN
               DO: 
                 sources.zimmeranz = sources.zimmeranz + 1. 
                 IF genstat.zipreis EQ 0 THEN sources.betriebsnr = sources.betriebsnr + 1. 
               END. 

               ASSIGN
                   sources.persanz = sources.persanz + genstat.erwachs 
                     + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN sources.logis = sources.logis + genstat.logis. 

               FIND CURRENT sources NO-LOCK.

               FIND FIRST landstat WHERE landstat.datum = bill-date AND
                   landstat.nationnr = genstat.resident EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE landstat THEN
               DO:
                   CREATE landstat.
                   ASSIGN landstat.datum = bill-date
                       landstat.nationnr = genstat.resident.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                                 AND genstat.resstatus NE 13))*/
                  NOT isSharer THEN
               DO: 
                   landstat.zimmeranz = landstat.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN landstat.betriebsnr = landstat.betriebsnr + 1. 
               END. 
               landstat.persanz = landstat.persanz + genstat.erwachs 
                   + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN landstat.logis = landstat.logis + genstat.logis. 
               FIND CURRENT landstat NO-LOCK.

               FIND FIRST guestat1 WHERE guestat1.datum = bill-date AND guestat1.gastnr 
                   = genstat.gastnr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE guestat1 THEN
               DO:
                   CREATE guestat1.
                   ASSIGN guestat1.datum = bill-date
                       guestat1.gastnr = genstat.gastnr.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                                 AND genstat.resstatus NE 13))*/
                   NOT isSharer THEN
               DO: 
                   guestat1.zimmeranz = guestat1.zimmeranz + 1. 
                   IF genstat.zipreis EQ 0 THEN guestat1.betriebsnr = guestat1.betriebsnr + 1. 
               END. 
               guestat1.persanz = guestat1.persanz + genstat.erwachs 
                   + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 
               IF genstat.zipreis NE 0 THEN guestat1.logis = guestat1.logis + genstat.logis. 
               FIND CURRENT guestat1 NO-LOCK.

               FIND FIRST zinrstat WHERE zinrstat.datum = bill-date AND
                  zinrstat.zinr = genstat.zinr EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE zinrstat THEN
               DO:
                  CREATE zinrstat.
                  ASSIGN zinrstat.datum = bill-date
                      zinrstat.zinr = genstat.zinr.
               END.
               ASSIGN vat = 0 service = 0.
               FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR.
               IF AVAILABLE arrangement THEN
               DO:
                    FIND FIRST artikel WHERE artikel.artnr = arrangement.artnr-logis 
                       AND artikel.departement = 0 NO-LOCK NO-ERROR. 
                    IF AVAILABLE artikel THEN
                    DO:
                        IF rm-serv THEN
                       DO:
                         FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code 
                           NO-LOCK NO-ERROR. 
                         IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                           service = htparam.fdecimal / 100. 
                       END.

                       IF rm-vat THEN
                       DO:
                         FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code 
                           NO-LOCK NO-ERROR. 
                         IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                           vat = htparam.fdecimal / 100. 
                         FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
                         IF htparam.flogical THEN vat = vat + vat * service. 
                         vat = round(vat, 2). 
                       END.
                    END.
               END.

               IF /*((genstat.resstatus = 6) OR (genstat.res-date[1] = genstat.res-date[2] 
                                            AND genstat.resstatus NE 13))*/
                   NOT isSharer THEN
               DO: 
                 zinrstat.zimmeranz = zinrstat.zimmeranz + 1. 
                 IF genstat.zipreis EQ 0 THEN zinrstat.betriebsnr = zinrstat.betriebsnr + 1. 
               END. 
               zinrstat.personen = zinrstat.personen + genstat.erwachs 
                 + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3. 

               IF genstat.rate NE 0 THEN 
               ASSIGN
                 zinrstat.logisumsatz  = zinrstat.logisumsatz + genstat.logis
                 zinrstat.argtumsatz   = zinrstat.argtumsatz + genstat.rateLocal / (1 + vat + service).
               IF rm-serv THEN
                 zinrstat.gesamtumsatz = zinrstat.gesamtumsatz + genstat.rateLocal * (1 + vat + service). 
               ELSE zinrstat.gesamtumsatz = zinrstat.gesamtumsatz + genstat.rateLocal. 

               FIND FIRST zkstat WHERE zkstat.zikatnr = genstat.zikatnr AND
                   zkstat.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.
               IF NOT AVAILABLE zkstat THEN
               DO:
                   CREATE zkstat.
                   ASSIGN zkstat.datum = bill-date
                       zkstat.zikatnr = genstat.zikatnr.
               END.
               anz = 0. 
               FOR EACH zimbuff WHERE zimbuff.zikatnr = genstat.zikatnr 
                 AND zimbuff.sleeping NO-LOCK: 
                 anz = anz + 1. 
               END. 
               IF NOT isSharer THEN
               DO:
                   ASSIGN zkstat.zimmeranz = zkstat.zimmeranz + 1.
                   IF genstat.zipreis = 0 THEN
                       zkstat.betriebsnr = zkstat.betriebsnr + 1.
               END.
               ASSIGN
                   zkstat.personen = zkstat.personen +  genstat.erwachs + genstat.kind1 + 
                   genstat.kind2 + genstat.kind3 + genstat.gratis.
               IF genstat.zipreis = 0  THEN
               DO: 
                   /*zkstat.betriebsnr = zkstat.betriebsnr + 1.*/
                   IF genstat.gratis = 0 AND (genstat.erwachs + genstat.kind1) GT 0 THEN 
                     zkstat.arrangement-art[1] = zkstat.arrangement-art[1] + 1. /* comp B */ 
               END.
               IF genstat.res-date[1] = bill-date AND genstat.res-date[2] GT bill-date THEN
                   zkstat.anz-ankunft = zkstat.anz-ankunft + 1.
               IF genstat.res-date[1] = genstat.res-date[2] THEN
                   zkstat.anz-abr = zkstat.anz-abr + 1.
               FIND CURRENT zkstat NO-LOCK.
           END. /* IF do-it */
        END.
    
    /*    FOR EACH genbuff WHERE YEAR(genbuff.datum) = YEAR(bill-date) 
            AND MONTH(genbuff.datum) = MONTH(bill-date) AND genbuff.zinr NE "" NO-LOCK:
            FIND FIRST guestat WHERE guestat.monat = MONTH(bill-date) 
                AND guestat.jahr = YEAR(bill-date)
                AND guestat.gastnr = genbuff.gastnr EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE guestat THEN
            DO:
                CREATE guestat.
                ASSIGN guestat.monat = MONTH(bill-date)
                    guestat.jahr = YEAR(bill-date)
                    guestat.gastnr = genbuff.gastnr.
            END.
            IF genbuff.resstatus = 6 OR (genbuff.res-date[1] = genbuff.res-date[2] 
                                     AND genbuff.resstatus NE 13) THEN
            guestat.room-nights = guestat.room-nights  + 1.
            FIND CURRENT guestat NO-LOCK.
    
        END.*/

          /*MT*/
          DO:
              FOR EACH t-segmentstat :
                  FIND FIRST segmentstat WHERE segmentstat.datum = t-segmentstat.datum
                      AND segmentstat.segmentcode = t-segmentstat.segmentcode
                      NO-ERROR.
                  IF NOT AVAILABLE segmentstat THEN
                  DO:
                      CREATE segmentstat.
                      ASSIGN segmentstat.datum = t-segmentstat.datum
                             segmentstat.segmentcode = t-segmentstat.segmentcode.
                  END.
                  ASSIGN
                      segmentstat.budlogis = t-segmentstat.budlogis
                      segmentstat.budzimmeranz = t-segmentstat.budzimmeranz
                      segmentstat.budpersanz = t-segmentstat.budpersanz.
              END.
          END.
          /*MT*/

          /*FT*/
          DO:
              FOR EACH t-sources :
                  FIND FIRST sources WHERE sources.datum = t-sources.datum
                      AND sources.source-code = t-sources.source-code
                      NO-ERROR.
                  IF NOT AVAILABLE sources THEN
                  DO:
                      CREATE sources.
                      ASSIGN sources.datum = t-sources.datum
                             sources.source-code = t-sources.source-code.
                  END.
                  ASSIGN
                      sources.budlogis = t-sources.budlogis
                      sources.budzimmeranz = t-sources.budzimmeranz
                      sources.budpersanz = t-sources.budpersanz.
              END.
          END.
          /*FT*/
   END.
END.

PROCEDURE reorg-guestat:
    DEF VAR dd AS DATE.
    DEF VAR mm AS INTEGER.
    DEF VAR yy AS INTEGER. 
    DEF BUFFER genbuff FOR genstat.

    DO mm = MONTH(fdate) TO MONTH(tdate):
         FOR EACH genbuff WHERE YEAR(genbuff.datum) = YEAR(fdate) 
            AND MONTH(genbuff.datum) = mm AND genbuff.zinr NE "" NO-LOCK:
            FIND FIRST guestat WHERE guestat.monat = mm
                AND guestat.jahr = YEAR(fdate)
                AND guestat.gastnr = genbuff.gastnr EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE guestat THEN
            DO:
                CREATE guestat.
                ASSIGN guestat.monat = MONTH(bill-date)
                    guestat.jahr = YEAR(bill-date)
                    guestat.gastnr = genbuff.gastnr.
            END.
            IF genbuff.resstatus NE 13 THEN
            guestat.room-nights = guestat.room-nights  + 1.
            FIND CURRENT guestat NO-LOCK.
        END.
    END.
    
END. 
*/
