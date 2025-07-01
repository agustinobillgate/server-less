.
DEFINE TEMP-TABLE room-list 
  FIELD wd                  AS INTEGER 
  FIELD datum               AS DATE 
  FIELD bezeich             AS CHAR FORMAT "x(15)" FONT 2 
  FIELD room                AS DECIMAL FORMAT " >>9.99" EXTENT 17 INITIAL 0 
  FIELD coom                AS CHAR EXTENT /*21*/ 17 FORMAT "x(7)" FONT 2 INITIAL "" 
  FIELD k-pax               AS INTEGER INITIAL 0
  FIELD t-pax               AS INTEGER INITIAL 0
  FIELD lodg                AS DECIMAL EXTENT 4 FORMAT "->>>,>>>,>>9.99"
  FIELD avrglodg            AS DECIMAL FORMAT "->,>>>,>>9.99" 
  FIELD resnr               AS CHAR FORMAT "x(7)" 
  FIELD rmno                LIKE zimmer.zinr
  FIELD rmcat               AS CHAR FORMAT "x(6)" 
  FIELD name                AS CHAR FORMAT "x(24)" 
  FIELD argt                AS CHAR FORMAT "x(4)" 
  FIELD company             AS CHAR FORMAT "x(18)" 
  FIELD segment             AS CHAR FORMAT "x(16)"
  FIELD currency            AS CHAR FORMAT "x(4)"
  FIELD Adult               AS INTEGER FORMAT ">>9" 
  FIELD ch1                 AS INTEGER FORMAT ">>9" 
  FIELD ch2                 AS INTEGER FORMAT ">>9" 
  FIELD compli              AS INTEGER FORMAT ">>9" 
  FIELD depart              AS DATE 
  FIELD arrival             AS DATE 
  FIELD nights              AS INTEGER FORMAT ">>>>>9" 
  FIELD ArrTime             AS CHAR
  FIELD DepTime             AS CHAR
  FIELD qty                 AS INTEGER FORMAT "999" 
  FIELD pax                 AS INTEGER FORMAT ">999"
  FIELD pocc                AS DECIMAL
  FIELD sleeping            AS LOGICAL
  FIELD t-avail             AS INTEGER
  FIELD t-ooo               AS INTEGER
  FIELD t-alot              AS INTEGER
  FIELD t-occ               AS INTEGER
  FIELD zikatnr             AS INTEGER 
  FIELD kurzbez             AS CHAR
.

DEFINE TEMP-TABLE segm-list 
  FIELD selected            AS LOGICAL INITIAL NO 
  FIELD segm                AS INTEGER 
  FIELD bezeich             AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE argt-list 
  FIELD selected            AS LOGICAL INITIAL NO 
  FIELD argtnr              AS INTEGER
  FIELD argt                AS CHAR 
  FIELD bezeich             AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE zikat-list 
  FIELD selected            AS LOGICAL INITIAL NO 
  FIELD zikatnr             AS INTEGER 
  FIELD bezeich             AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE rmcat-list 
  FIELD zikatnr             AS INTEGER 
  FIELD anzahl              AS INTEGER 
  FIELD sleeping            AS LOGICAL INITIAL YES
  FIELD kurzbez             AS CHAR 
  FIELD bezeich             AS CHAR FORMAT "x(20)" 
  FIELD zinr                AS CHAR 
  .

DEFINE INPUT PARAMETER case-type       AS INTEGER.
DEFINE INPUT PARAMETER datum           AS DATE.
DEFINE INPUT PARAMETER curr-date       AS DATE.
DEFINE INPUT PARAMETER to-date         AS DATE.
DEFINE INPUT PARAMETER all-segm        AS LOGICAL. 
DEFINE INPUT PARAMETER all-argt        AS LOGICAL.
DEFINE INPUT PARAMETER all-zikat       AS LOGICAL.
DEFINE INPUT PARAMETER incl-tent       AS LOGICAL. 
DEFINE INPUT PARAMETER exclOOO         AS LOGICAL.

DEFINE INPUT PARAMETER TABLE FOR argt-list.
DEFINE INPUT PARAMETER TABLE FOR segm-list.
DEFINE INPUT PARAMETER TABLE FOR zikat-list.

DEF OUTPUT PARAMETER TABLE FOR room-list.

DEF VARIABLE tot-room    AS INTEGER     NO-UNDO.
DEF VARIABLE vhp-limited AS LOGICAL     NO-UNDO INIT NO.
DEF VARIABLE pax         AS INTEGER     NO-UNDO. 

DEF BUFFER rline1 FOR res-line.


RUN create-browse1.

PROCEDURE create-browse1: /*forecast*/
DEFINE VARIABLE p-room      AS INTEGER. 
DEFINE VARIABLE p-lodg      AS DECIMAL.
DEFINE VARIABLE prev-room   AS INTEGER. 
DEFINE VARIABLE p-pax       AS INTEGER. 
DEFINE VARIABLE avrg-rate   AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL. 
DEFINE VARIABLE consider-it AS LOGICAL. 
DEFINE VARIABLE n           AS INTEGER INITIAL 0. 
DEFINE VARIABLE kont-doit   AS LOGICAL. 
DEFINE VARIABLE allot-doit  AS LOGICAL.
DEFINE VARIABLE mtd-occ     AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-lodg    AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-i      AS INTEGER.
DEFINE VARIABLE Fnet-lodg   AS DECIMAL NO-UNDO.     /*Alder - Ticket A43151*/

DEFINE VARIABLE rsvStat      AS CHAR    NO-UNDO.
DEFINE VARIABLE avrg-lodging AS DECIMAL NO-UNDO.

DEFINE BUFFER s-list FOR segm-list. 
DEFINE BUFFER a-list FOR argt-list. 
DEFINE BUFFER z-list FOR zikat-list. 
DEFINE BUFFER kline  FOR kontline.

DEFINE VAR tot-breakfast    AS DECIMAL.
DEFINE VAR tot-Lunch        AS DECIMAL.
DEFINE VAR tot-dinner       AS DECIMAL.
DEFINE VAR tot-Other        AS DECIMAL.

DEFINE VAR sum-breakfast    AS DECIMAL.
DEFINE VAR sum-Lunch        AS DECIMAL.
DEFINE VAR sum-dinner       AS DECIMAL.
DEFINE VAR sum-Other        AS DECIMAL.

DEFINE VAR tot-pax              AS INTEGER.
DEFINE VAR tot-adult            AS INTEGER.
DEFINE VAR tot-ch1              AS INTEGER.
DEFINE VAR tot-ch2              AS INTEGER.
DEFINE VAR tot-compli           AS INTEGER.
DEFINE VAR tot-nights           AS INTEGER.
DEFINE VAR tot-qty              AS INTEGER.
DEFINE VAR tot-pocc             AS DECIMAL.
DEFINE VAR tot-lodg             AS DECIMAL. /*Alder - Ticket A43151*/

DEFINE VARIABLE tot-rmrev       AS DECIMAL. /*Alder - Ticket A43151*/
DEFINE VARIABLE tot-vat         AS DECIMAL. /*Alder - Ticket A43151*/
DEFINE VARIABLE tot-service     AS DECIMAL. /*Alder - Ticket A43151*/

DEFINE VARIABLE tmp-date        AS DATE NO-UNDO.   /* Rulita 211124 | Fixing for serverless */

DEFINE VAR ci-date              AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN ci-date = htparam.fdate.

  /*ini total room, room category mempengaruhi tot room*/
  tot-room = 0. 
  FOR EACH zimmer WHERE sleeping NO-LOCK: 
    IF all-zikat THEN tot-room = tot-room + 1. 
    ELSE 
    DO: 
      FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
        AND z-list.selected NO-LOCK NO-ERROR. 
      IF AVAILABLE z-list THEN tot-room = tot-room + 1. 
    END. 
  END.
  
  ASSIGN 
    tot-pax     = 0
    tot-adult   = 0
    tot-ch1     = 0
    tot-ch2     = 0
    tot-compli  = 0
    tot-qty     = 0
    tot-pocc    = 0
    .

  IF case-type = 1 THEN
  DO:
     /*IF datum LE ci-date THEN RUN cal-lastday-occ.
     ELSE
     DO:*/

        FOR EACH res-line WHERE res-line.active-flag LE 2 
            AND res-line.resstatus LE 13 
            AND res-line.resstatus NE 4 
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12
            AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK,
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
            FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK,
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK BY res-line.resnr:

            IF NOT vhp-limited THEN do-it = YES.
            ELSE
            DO:
              /*FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                NO-LOCK NO-ERROR.*/
              do-it = /*AVAILABLE segment AND*/ segment.vip-level = 0.
            END.
        
            IF do-it AND NOT all-segm THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
                AND s-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE s-list. 
            END. 
            IF do-it AND NOT all-argt THEN 
            DO: 
              FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
                AND a-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE a-list. 
            END. 
            IF do-it AND NOT all-zikat THEN 
            DO: 
              FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
                AND z-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE z-list. 
            END. 
         
            kont-doit = YES. 
            IF do-it AND (NOT all-segm) AND (res-line.kontignr LT 0) THEN 
            DO: 
              /*FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK. */
              FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
              IF NOT AVAILABLE guestseg THEN 
                FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                  NO-LOCK NO-ERROR. 
              IF AVAILABLE guestseg THEN 
              DO: 
                FIND FIRST s-list WHERE s-list.segm = guestseg.segmentcode 
                  AND s-list.selected NO-LOCK NO-ERROR. 
                kont-doit = AVAILABLE s-list. 
              END. 
            END. 
             
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
            IF do-it AND AVAILABLE zimmer THEN 
            DO: 
              tmp-date = datum - 1.                                                             /* Rulita 211124 | Fixing for serverless */
              FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
                AND queasy.date1 LE tmp-date AND queasy.date2 GE tmp-date NO-LOCK NO-ERROR. 
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
                pax = res-line.erwachs. 
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
                
                tmp-date = datum - 1.                                           /* Rulita 211124 | Fixing for serverless */
                IF tmp-date = res-line.ankunft AND consider-it 
                    AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent))
                    AND res-line.active-flag LE 1 THEN
                DO: 
                  
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND NOT res-line.zimmerfix THEN
                  IF res-line.abreise GT res-line.ankunft THEN 
                  DO: 
                     CREATE room-list.
                     IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                     ASSIGN
                      room-list.resnr          = STRING(res-line.resnr) 
                      room-list.name           = res-line.name 
                      room-list.rmno           = res-line.zinr 
                      room-list.depart         =  res-line.abreise 
                      room-list.arrival        = res-line.ankunft
                      room-list.argt           = res-line.arrangement
                      room-list.Adult          = pax
                      room-list.compli         = res-line.gratis * res-line.zimmeranz
                      room-list.ch1            = res-line.kind1 * res-line.zimmeranz
                      room-list.ch2            = res-line.kind2 * res-line.zimmeranz
                      room-list.currency       = waehrung.wabkurz  
                      room-list.segment        = segment.bezeich
                      room-list.qty            = res-line.zimmeranz /*1*/
                      room-list.pax            = (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                 + res-line.gratis) * res-line.zimmeranz 
                      .
                      IF guest.karteityp NE 0 THEN
                      room-list.company        = guest.name + ", " + guest.vorname1 
                                                 + " " + guest.anrede1 + guest.anredefirma. 
                      tot-pax                  = tot-pax + ((pax + res-line.kind1 + res-line.kind2 
                                                 + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                      tot-adult                = tot-adult + (pax).
                      tot-ch1                  = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                      tot-ch2                  = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                      tot-compli               = tot-compli + (res-line.gratis * res-line.zimmeranz).
                      tot-nights               = tot-nights + res-line.anztage.
                      tot-qty                  = tot-qty + res-line.zimmeranz.
                  END. 
                  
                END. /*  Arrival */ 
                
                tmp-date = datum - 1.                                                             /* Rulita 211124 | Fixing for serverless */
                IF res-line.resstatus NE 3 AND res-line.resstatus NE 4 
                  AND consider-it 
                  AND (res-line.abreise GT tmp-date AND res-line.ankunft LT tmp-date
                  AND res-line.ankunft NE tmp-date
                  AND res-line.abreise NE tmp-date)
                  AND res-line.active-flag LE 1 THEN 
                DO: 
                 
                  IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                  AND NOT res-line.zimmerfix THEN 
                     CREATE room-list.
                     IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                     ASSIGN
                      room-list.resnr          = STRING(res-line.resnr) 
                      room-list.name           = res-line.name 
                      room-list.rmno           = res-line.zinr 
                      room-list.depart         =  res-line.abreise 
                      room-list.arrival        = res-line.ankunft
                      room-list.argt           = res-line.arrangement
                      room-list.Adult          = pax 
                      room-list.compli         = res-line.gratis * res-line.zimmeranz
                      room-list.ch1            = res-line.kind1 * res-line.zimmeranz
                      room-list.ch2            = res-line.kind2 * res-line.zimmeranz
                      room-list.currency       = waehrung.wabkurz  
                      room-list.segment        = segment.bezeich
                      room-list.qty            = res-line.zimmeranz /*1*/
                      room-list.pax            = (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                 + res-line.gratis) * res-line.zimmeranz
                    .

                      IF guest.karteityp NE 0 THEN
                      room-list.company        = guest.name + ", " + guest.vorname1 
                                                 + " " + guest.anrede1 + guest.anredefirma. 
                      tot-pax                  = tot-pax + ((pax + res-line.kind1 + res-line.kind2 
                                                 + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                      tot-adult                = tot-adult + (pax).
                      tot-ch1                  = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                      tot-ch2                  = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                      tot-compli               = tot-compli + (res-line.gratis * res-line.zimmeranz).
                      tot-qty                  = tot-qty + res-line.zimmeranz.
                END. /* Inhouse */ 
                
                /* ITA 130220 checkout same today checkin */
                IF res-line.resstatus EQ 8 AND consider-it 
                  AND res-line.active-flag = 2
                  AND res-line.abreise EQ (datum - 1) AND res-line.ankunft EQ (datum - 1) THEN 
                DO: 
                   IF NOT res-line.zimmerfix THEN 
                     CREATE room-list.
                     IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                     ASSIGN
                      room-list.resnr          = STRING(res-line.resnr) 
                      room-list.name           = res-line.name 
                      room-list.rmno           = res-line.zinr 
                      room-list.depart         =  res-line.abreise 
                      room-list.arrival        = res-line.ankunft
                      room-list.argt           = res-line.arrangement
                      room-list.Adult          = pax
                      room-list.compli         = res-line.gratis * res-line.zimmeranz
                      room-list.ch1            = res-line.kind1 * res-line.zimmeranz
                      room-list.ch2            = res-line.kind2 * res-line.zimmeranz
                      room-list.currency       = waehrung.wabkurz  
                      room-list.segment        = segment.bezeich
                      room-list.qty            = res-line.zimmeranz /*1*/
                      room-list.pax            = (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                 + res-line.gratis) * res-line.zimmeranz.

                      IF guest.karteityp NE 0 THEN
                      room-list.company        = guest.name + ", " + guest.vorname1 
                                                 + " " + guest.anrede1 + guest.anredefirma. 
                      tot-pax                  = tot-pax + ((pax + res-line.kind1 + res-line.kind2 
                                                 + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                      tot-adult                = tot-adult + (pax).
                      tot-ch1                  = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                      tot-ch2                  = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                      tot-compli               = tot-compli + (res-line.gratis * res-line.zimmeranz).
                      tot-qty                  = tot-qty + res-line.zimmeranz.
                END. /* checkout same today checkin */ 
            END. /*do-it*/
        END. /*for each res-line*/         
     /*END. /*do*/*/
  END. /*case-type = 1*/

  ELSE IF case-type = 3 THEN
  DO:
     FOR EACH res-line WHERE (res-line.active-flag LE 1 
         AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 
         AND res-line.resstatus NE 9 
         AND res-line.resstatus NE 10 
         AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT to-date) 
         AND NOT (res-line.abreise LT datum)) OR
         (res-line.active-flag = 2 AND res-line.resstatus = 8
         AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
         AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
         NO-LOCK,
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
         FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
         FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK,
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
         FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK BY res-line.resnr:

         
         IF NOT vhp-limited THEN do-it = YES.
         ELSE
         DO:
            do-it = AVAILABLE segment AND segment.vip-level = 0.
         END. 
         
         IF do-it AND NOT all-segm THEN 
         DO: 
            FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
              AND s-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE s-list. 
         END. 
         IF do-it AND NOT all-argt THEN 
         DO: 
            FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
               AND a-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE a-list. 
         END. 
         IF do-it AND NOT all-zikat THEN 
         DO: 
            FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
            AND z-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE z-list. 
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
              pax = res-line.erwachs. 
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                  AND reslin-queasy.resnr = res-line.resnr 
                  AND reslin-queasy.reslinnr = res-line.reslinnr 
                  AND reslin-queasy.date1 LE datum 
                  AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
              IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                  pax = reslin-queasy.number3. 
              
              FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
              consider-it = YES. 
              IF res-line.zimmerfix THEN 
              DO: 
                  FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                    AND rline1.reslinnr NE res-line.reslinnr 
                    AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                    AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                  IF AVAILABLE rline1 THEN consider-it = NO. 
              END.
    
              IF datum = res-line.ankunft 
                AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent))
                AND NOT res-line.zimmerfix THEN DO: 
                CREATE room-list.
                IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.

                ASSIGN 
                      room-list.resnr           = STRING(res-line.resnr) 
                      room-list.name            = res-line.name 
                      room-list.rmno            = res-line.zinr 
                      room-list.depart          = res-line.abreise 
                      room-list.arrival         = res-line.ankunft 
                      room-list.argt            = res-line.arrangement
                      room-list.pax             = (pax + res-line.kind1 + res-line.kind2 
                                                  + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz
                      room-list.Adult           = pax
                      room-list.compli          = res-line.gratis * res-line.zimmeranz
                      room-list.ch1             = res-line.kind1 * res-line.zimmeranz
                      room-list.ch2             = res-line.kind2 * res-line.zimmeranz
                      room-list.ArrTime         = STRING(res-line.ankzeit, "HH:MM:SS")
                      room-list.currency        = waehrung.wabkurz  
                      room-list.segment         = segment.bezeich
                      room-list.qty             = res-line.zimmeranz 
                      .
    
                     IF guest.karteityp NE 0 THEN
                        room-list.company       = guest.name + ", " + guest.vorname1 
                                                  + " " + guest.anrede1 + guest.anredefirma. 
                        tot-pax                 = tot-pax + ((pax + res-line.kind1 + res-line.kind2 
                                                  + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                        tot-adult               = tot-adult + (pax).
                        tot-ch1                 = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                        tot-ch2                 = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                        tot-compli              = tot-compli + (res-line.gratis * res-line.zimmeranz).
                        tot-nights              = tot-nights + res-line.anztage.
                        tot-qty                 = tot-qty + res-line.zimmeranz.
    
              END. /*  Arrival */ 
         END. /*do-it*/
     END. /*for*/
  END. /*case-type = 3*/

  ELSE IF case-type = 5 THEN
  DO:
     FOR EACH res-line WHERE (res-line.active-flag LE 1 
         AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 
         AND res-line.resstatus NE 9 
         AND res-line.resstatus NE 10 
         AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT to-date) 
         AND NOT (res-line.abreise LT datum)) OR 
         (res-line.active-flag = 2 AND res-line.resstatus = 8 
         AND res-line.abreise = ci-date)
         AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
         NO-LOCK,
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
         FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
         FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK, 
         FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY res-line.resnr:
         
            
         IF NOT vhp-limited THEN do-it = YES.
         ELSE
         DO:
            do-it = AVAILABLE segment AND segment.vip-level = 0.
         END. 
         IF do-it AND NOT all-segm THEN 
         DO: 
            FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
              AND s-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE s-list. 
         END. 
         IF do-it AND NOT all-argt THEN 
         DO: 
            FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
               AND a-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE a-list. 
         END. 
         IF do-it AND NOT all-zikat THEN 
         DO: 
            FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
            AND z-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE z-list. 
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
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                  AND reslin-queasy.resnr = res-line.resnr 
                  AND reslin-queasy.reslinnr = res-line.reslinnr 
                  AND reslin-queasy.date1 LE datum 
                  AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                  pax = reslin-queasy.number3. 
                FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
         
                consider-it = YES. 
                IF res-line.zimmerfix THEN 
                DO: 
                  FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                    AND rline1.reslinnr NE res-line.reslinnr 
                    AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                    AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                  IF AVAILABLE rline1 THEN consider-it = NO. 
             END.
                
             IF datum = res-line.abreise AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent)) THEN 
             DO:
                CREATE room-list.
                IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                ASSIGN 
                  room-list.resnr           = string(res-line.resnr) 
                  room-list.name            = res-line.name 
                  room-list.rmno            = res-line.zinr 
                  room-list.depart          = res-line.abreise 
                  room-list.arrival         = res-line.ankunft 
                  room-list.argt            = res-line.arrangement
                  room-list.pax             = (res-line.erwachs + res-line.kind1 + res-line.kind2 
                                              + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz
                  room-list.Adult           = res-line.erwachs * res-line.zimmeranz
                  room-list.compli          = res-line.gratis * res-line.zimmeranz
                  room-list.ch1             = res-line.kind1 * res-line.zimmeranz
                  room-list.ch2             = res-line.kind2 * res-line.zimmeranz
                  room-list.DepTime         = STRING(res-line.abreisezeit, "HH:MM:SS")
                  room-list.currency        = waehrung.wabkurz
                  room-list.segment         = segment.bezeich
                  room-list.qty             = res-line.zimmeranz 
                .
                 
                IF guest.karteityp NE 0 THEN
                  room-list.company         = guest.name + ", " + guest.vorname1 
                                              + " " + guest.anrede1 + guest.anredefirma. 
                  tot-pax                   = tot-pax + ((res-line.erwachs + res-line.kind1 + res-line.kind2 
                                              + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                  tot-adult                 = tot-adult + (res-line.erwachs * res-line.zimmeranz).
                  tot-ch1                   = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                  tot-ch2                   = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                  tot-compli                = tot-compli + (res-line.gratis * res-line.zimmeranz).
                  tot-qty                   = tot-qty + res-line.zimmeranz.
             
             END. /*  Departure */ 
         END. /*do-it*/
     END. /*for*/
  END. /*case-type = 5*/

  ELSE IF case-type = 7 THEN
  DO:
     FOR EACH res-line WHERE res-line.active-flag LE 1
        AND res-line.resstatus LE 13 
        AND res-line.resstatus NE 4 
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        NO-LOCK BY res-line.resnr: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR. 
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
        FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.

        /*Alder - Ticket A43151 - Start*/
        RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                         OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                         OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                         OUTPUT tot-dinner, OUTPUT tot-other,
                                         OUTPUT tot-rmrev, OUTPUT tot-vat,
                                         OUTPUT tot-service).
        /*Alder - Ticket A43151 - End*/

        IF NOT vhp-limited THEN do-it = YES.
        ELSE
        DO:
          FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
    
        IF do-it AND NOT all-segm THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
            AND s-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE s-list. 
        END. 
        
        
        IF do-it AND NOT all-argt THEN 
        DO: 
          FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
            AND a-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE a-list. 
        END. 

        IF do-it AND NOT all-zikat THEN 
        DO: 
          FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
            AND z-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE z-list. 
        END. 
     
        kont-doit = YES. 
        IF do-it AND (NOT all-segm) AND (res-line.kontignr LT 0) THEN 
        DO: 
          FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK. 
          FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
            AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE guestseg THEN 
            FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
              NO-LOCK NO-ERROR. 
          IF AVAILABLE guestseg THEN 
          DO: 
            FIND FIRST s-list WHERE s-list.segm = guestseg.segmentcode 
              AND s-list.selected NO-LOCK NO-ERROR. 
            kont-doit = AVAILABLE s-list. 
          END. 
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
            pax = res-line.erwachs. 
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

            IF datum = res-line.ankunft AND consider-it 
               AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent)) THEN
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13
                AND NOT res-line.zimmerfix THEN
              IF /*res-line.abreise GT res-line.ankunft*/
                 res-line.abreise GE res-line.ankunft  THEN 
              DO: 
                 CREATE room-list.
                 IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                 ASSIGN
                  room-list.resnr          = STRING(res-line.resnr) 
                  room-list.name           = res-line.name 
                  room-list.rmno           = res-line.zinr 
                  room-list.depart         = res-line.abreise 
                  room-list.arrival        = res-line.ankunft
                  room-list.argt           = res-line.arrangement
                  room-list.Adult          = res-line.erwachs 
                  room-list.compli         = res-line.gratis * res-line.zimmeranz
                  room-list.ch1            = res-line.kind1 * res-line.zimmeranz
                  room-list.ch2            = res-line.kind2 * res-line.zimmeranz
                  room-list.currency       = waehrung.wabkurz  
                  room-list.segment        = segment.bezeich
                  room-list.qty            = res-line.zimmeranz /*1*/
                  room-list.pax            = (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                             + res-line.gratis) * res-line.zimmeranz 
                  room-list.pocc           = (room-list.qty / tot-room) * 100
                  room-list.lodg[4]        = net-lodg   /*Alder - Ticket A43151*/
                  .
                  IF guest.karteityp NE 0 THEN
                  room-list.company        = guest.name + ", " + guest.vorname1 
                                             + " " + guest.anrede1 + guest.anredefirma. 
                  tot-pax                  = tot-pax + ((res-line.erwachs + res-line.kind1 + res-line.kind2 
                                             + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                  tot-adult                = tot-adult + (res-line.erwachs * res-line.zimmeranz).
                  tot-ch1                  = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                  tot-ch2                  = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                  tot-compli               = tot-compli + (res-line.gratis * res-line.zimmeranz).
                  tot-nights               = tot-nights + res-line.anztage.
                  tot-qty                  = tot-qty + res-line.zimmeranz.
                  tot-pocc                 = tot-pocc + (room-list.qty / tot-room) * 100.
                  tot-lodg                 = tot-lodg + net-lodg.   /*Alder - Ticket A43151*/
              END. 
            END. /*  Arrival */ 

            IF res-line.resstatus NE 3  
              AND res-line.resstatus NE 4 
              AND consider-it 
              AND (res-line.abreise GT datum AND res-line.ankunft LT datum
              AND res-line.ankunft NE datum
              AND res-line.abreise NE datum) THEN 
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13
              AND NOT res-line.zimmerfix THEN 
                 CREATE room-list.
                 IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                 ASSIGN
                  room-list.resnr          = STRING(res-line.resnr) 
                  room-list.name           = res-line.name 
                  room-list.rmno           = res-line.zinr 
                  room-list.depart         =  res-line.abreise 
                  room-list.arrival        = res-line.ankunft
                  room-list.argt           = res-line.arrangement
                  room-list.Adult          = res-line.erwachs 
                  room-list.compli         = res-line.gratis * res-line.zimmeranz
                  room-list.ch1            = res-line.kind1 * res-line.zimmeranz
                  room-list.ch2            = res-line.kind2 * res-line.zimmeranz
                  room-list.currency       = waehrung.wabkurz  
                  room-list.segment        = segment.bezeich
                  room-list.qty            = res-line.zimmeranz /*1*/
                  room-list.pax            = (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                             + res-line.gratis) * res-line.zimmeranz
                  room-list.pocc           = (room-list.qty / tot-room) * 100
                  room-list.lodg[4]        = net-lodg   /*Alder - Ticket A43151*/
                .

                  IF guest.karteityp NE 0 THEN
                  room-list.company        = guest.name + ", " + guest.vorname1 
                                             + " " + guest.anrede1 + guest.anredefirma. 
                  tot-pax                  = tot-pax + ((res-line.erwachs + res-line.kind1 + res-line.kind2 
                                             + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                  tot-adult                = tot-adult + (res-line.erwachs * res-line.zimmeranz).
                  tot-ch1                  = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                  tot-ch2                  = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                  tot-compli               = tot-compli + (res-line.gratis * res-line.zimmeranz).
                  tot-qty                  = tot-qty + res-line.zimmeranz.
                  tot-pocc                 = tot-pocc + (room-list.qty / tot-room) * 100.
                  tot-lodg                 = tot-lodg + net-lodg.   /*Alder - Ticket A43151*/
            END. /* Inhouse */ 
        END. /*do-it*/
     END. /*for each res-line*/ 
  END. /*case-type = 7*/

  ELSE IF case-type = 11 THEN
  DO:
    DEFINE VARIABLE tot-actroom             AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-occrm               AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-ooo                 AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-alot                AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-avail               AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-avail2              AS INTEGER INITIAL 0.
   
    FOR EACH room-list: 
        delete room-list. 
    END. 

    RUN count-rmcateg.
    FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES 
        NO-LOCK BY zimkateg.zikatnr: 
      FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimkateg.zikatnr 
        AND rmcat-list.sleeping NO-ERROR. 
      IF AVAILABLE rmcat-list THEN 
      DO: 
        create room-list. 
        ASSIGN
          room-list.sleeping        = YES
          room-list.pax             = rmcat-list.anzahl
          room-list.t-avail         = rmcat-list.anzahl
          room-list.qty             = rmcat-list.anzahl
          room-list.zikatnr         = zimkateg.zikatnr
          room-list.bezeich         = STRING(zimkateg.kurzbez,"x(6)") 
          room-list.datum           = datum
          room-list.rmcat           = zimkateg.kurzbez                  /* Rulita 2C5C87 08/08/24 */
        .
      END.
    END.
    FOR EACH rmcat-list WHERE NOT rmcat-list.sleeping, 
          FIRST zimkateg WHERE zimkateg.zikatnr = rmcat-list.zikatnr NO-LOCK 
          BY zimkateg.zikatnr:
          create room-list.
          ASSIGN
          room-list.sleeping        = NO
          room-list.pax             = rmcat-list.anzahl
          room-list.t-avail         = rmcat-list.anzahl
          room-list.qty             = rmcat-list.anzahl
          room-list.zikatnr         = zimkateg.zikatnr
          room-list.bezeich         = STRING(zimkateg.kurzbez,"x(6)") 
          room-list.datum           = datum
          .
    END.

    FOR EACH res-line WHERE res-line.active-flag LE 1 
          AND res-line.resstatus LE 6 
          AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
               OR (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
          AND res-line.zikatnr = room-list.zikatnr 
          AND res-line.zinr NE "" AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
          FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND 
          NOT zimmer.sleeping NO-LOCK: 
              IF NOT vhp-limited THEN do-it = YES.
              ELSE
              DO:
                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                  NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                  NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
              END.
              IF do-it THEN ASSIGN room-list.t-avail  = room-list.t-avail - 1.
    END. 

    FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
          FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
          AND zimmer.sleeping = YES NO-LOCK :
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
          FIND FIRST room-list WHERE room-list.zikatnr = zimmer.zikatnr 
            AND room-list.sleeping NO-LOCK NO-ERROR. 
          IF AVAILABLE room-list THEN
          DO:
              IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
               ASSIGN
                    room-list.t-ooo     = room-list.t-ooo + 1
                    room-list.t-avail   = room-list.t-avail  - 1
                    .
          END.
    END. /*OOO*/
  /**/
    FOR EACH room-list WHERE room-list.sleeping: 
        FOR EACH res-line WHERE res-line.active-flag LE 1 
          AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
          AND res-line.resstatus NE 4 
          AND res-line.zikatnr = room-list.zikatnr 
          AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
               OR (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
          AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
          do-it = YES. 
          IF res-line.zinr NE "" THEN 
          DO: 
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
            do-it = zimmer.sleeping. 
          END. 

          IF res-line.resstatus = 3 AND NOT incl-tent THEN
              do-it = NO.

          IF do-it AND vhp-limited THEN
          DO:
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK NO-ERROR.
            do-it = AVAILABLE segment AND segment.vip-level = 0.
          END.
          
          IF do-it THEN 
          ASSIGN
              room-list.t-occ      = room-list.t-occ + res-line.zimmeranz 
              room-list.t-avail    = room-list.t-avail - res-line.zimmeranz
              .

        END.
    END. /*occupied room*/
 
    FOR EACH kontline WHERE kontline.betriebsnr = 0 
          AND datum GE kontline.ankunft AND datum LT kontline.abreise
          AND kontline.zikatnr = room-list.zikatnr 
          AND kontline.kontstat = 1 NO-LOCK: 
          ASSIGN
          room-list.t-alot  = room-list.t-alot + kontline.zimmeranz
          room-list.t-avail = room-list.t-avail  - kontline.zimmeranz
          . 
    END. /*allotment*/

    IF tot-actroom NE 0 THEN
    DO:
        CREATE room-list.
        ASSIGN 
              room-list.bezeich      = "TOTAL" 
              room-list.pax          = tot-avail2
              room-list.t-avail      = tot-avail
              room-list.qty          = tot-actroom
              room-list.t-ooo        = tot-ooo
              room-list.t-occ        = tot-occrm
        .
               
        END.
  END.

  ELSE IF case-type = 13 THEN
  DO:
     FOR EACH res-line WHERE res-line.active-flag LE 1 
         AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 
         AND res-line.resstatus NE 9 
         AND res-line.resstatus NE 10 
         AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT to-date) 
         AND NOT (res-line.abreise LE datum) 
         AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
         NO-LOCK,
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
         FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
         FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY res-line.resnr:
         FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
         NO-LOCK NO-ERROR.

         IF NOT vhp-limited THEN do-it = YES.
         ELSE
         DO:
            do-it = AVAILABLE segment AND segment.vip-level = 0.
         END. 
         IF do-it AND NOT all-segm THEN 
         DO: 
            FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
              AND s-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE s-list. 
         END. 
         IF do-it AND NOT all-argt THEN 
         DO: 
            FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
               AND a-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE a-list. 
         END. 
         IF do-it AND NOT all-zikat THEN 
         DO: 
            FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
            AND z-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE z-list. 
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
              pax = res-line.erwachs. 
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                  AND reslin-queasy.resnr = res-line.resnr 
                  AND reslin-queasy.reslinnr = res-line.reslinnr 
                  AND reslin-queasy.date1 LE datum 
                  AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                  pax = reslin-queasy.number3. 
                FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
         
                consider-it = YES. 
                IF res-line.zimmerfix THEN 
                DO: 
                  FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                    AND rline1.reslinnr NE res-line.reslinnr 
                    AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                    AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                  IF AVAILABLE rline1 THEN consider-it = NO. 
             END.
    
             IF res-line.resstatus = 3 AND datum GE res-line.ankunft THEN 
             DO:
                CREATE room-list.
                IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                ASSIGN 
                      room-list.qty             = res-line.zimmeranz 
                      room-list.resnr           = string(res-line.resnr) 
                      room-list.name            = res-line.name 
                      room-list.rmno            = res-line.zinr 
                      room-list.arrival         = res-line.ankunft 
                      room-list.depart          = res-line.abreise 
                      room-list.argt            = res-line.arrangement
                      room-list.segment         = segment.bezeich
                      room-list.Adult           = res-line.erwachs * res-line.zimmeranz
                      room-list.compli          = res-line.gratis * res-line.zimmeranz
                      room-list.ch1             = res-line.kind1 * res-line.zimmeranz
                      room-list.ch2             = res-line.kind2 * res-line.zimmeranz
                      room-list.currency        = waehrung.wabkurz
                      room-list.pax             = (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                  + res-line.gratis) * res-line.zimmeranz

                .
                IF guest.karteityp NE 0 THEN
                  room-list.company         = guest.name + ", " + guest.vorname1 
                                              + " " + guest.anrede1 + guest.anredefirma. 
                  tot-pax                   = tot-pax + ((res-line.erwachs + res-line.kind1 + res-line.kind2 
                                              + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                  tot-adult                 = tot-adult + (res-line.erwachs * res-line.zimmeranz).
                  tot-ch1                   = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                  tot-ch2                   = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                  tot-compli                = tot-compli + (res-line.gratis * res-line.zimmeranz).
                  tot-qty                   = tot-qty + res-line.zimmeranz.
             
             END. /* Tentative */ 
         END. /*do-it*/
     END. /*for*/
  END. /*case-type = 13*/

  ELSE IF case-type = 14 THEN
  DO:
     FOR EACH res-line WHERE res-line.kontignr GT 0 
         AND res-line.active-flag LT 2 
         AND NOT (res-line.ankunft GT to-date) 
         AND NOT (res-line.abreise LT datum) 
         AND res-line.resstatus LT 11 
         AND res-line.gastnr GT 0
         AND res-line.l-zuordnung[3] = 0 NO-LOCK :
         FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
         NO-LOCK NO-ERROR. 
         FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
         AND kontline.kontstat = 1 NO-LOCK NO-ERROR.
         IF AVAILABLE kontline THEN
         DO:
             FIND FIRST guest WHERE guest.gastnr = kontline.gastnr NO-LOCK NO-ERROR.
             IF datum GE res-line.ankunft AND datum LT res-line.abreise THEN
             DO:
                FIND FIRST zimmer WHERE zimmer.zikatnr = kontline.zikatnr 
                AND zimmer.sleeping NO-LOCK NO-ERROR. 
                CREATE room-list.
                ASSIGN
                    room-list.resnr                     = STRING(res-line.resnr)
                    room-list.qty                       = kontline.zimmeranz
                    room-list.rmno                      = zimmer.zinr 
                    room-list.name                      = kontline.kontcode 
                    room-list.depart                    = kontline.abreise 
                    room-list.arrival                   = kontline.ankunft 
                    room-list.t-alot                    = res-line.zimmeranz
                .
                IF guest.karteityp NE 0 THEN
                ASSIGN room-list.company = guest.name + ", " + guest.vorname1 
                                    + " " + guest.anrede1 + guest.anredefirma.
             END.
         END.
     END.
  END. /*case-type = 14*/

  ELSE IF case-type = 15 THEN
  DO:
     FIND FIRST zinrstat WHERE zinrstat.zinr = "ooo" 
        AND zinrstat.datum = datum NO-LOCK NO-ERROR.      /* Rulita 04/11/24 | Bugs Serverless From zinrstat.datum = room-list.datum To zinrstat.datum = datum */
      IF AVAILABLE zinrstat THEN
      DO:
          CREATE room-list.
          ASSIGN room-list.qty = zinrstat.zimmeranz. 
      END.
      ELSE 
      DO: 
          FOR EACH outorder WHERE outorder.gespstart LE datum 
            AND outorder.gespende GE datum AND outorder.betriebsnr LE 1 
            NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping 
            NO-LOCK: 
            CREATE room-list.
            ASSIGN
                room-list.qty                   = room-list.qty + 1
                room-list.rmno                  = outorder.zinr 
                room-list.name                  = outorder.gespgrund 
                room-list.depart                = outorder.gespende 
                room-list.arrival               = outorder.gespstart 
                room-list.bezeich               = zimmer.bezeich
                .
          END. 
     END. 
  END. /*ooo rooms*/

  ELSE IF case-type = 16 THEN
  DO:
     FOR EACH res-line WHERE res-line.active-flag LE 1 
         AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
         AND res-line.resstatus NE 4 
         AND res-line.ankunft LE datum AND res-line.abreise GT datum 
         AND res-line.kontignr LT 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK,
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
         FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
         FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY res-line.resnr:
         FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
         NO-LOCK NO-ERROR.

         IF NOT vhp-limited THEN do-it = YES.
         ELSE
         DO:
            do-it = AVAILABLE segment AND segment.vip-level = 0.
         END. 
         IF do-it AND NOT all-segm THEN 
         DO: 
            FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
              AND s-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE s-list. 
         END. 
         IF do-it AND NOT all-argt THEN 
         DO: 
            FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
               AND a-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE a-list. 
         END. 
         IF do-it AND NOT all-zikat THEN 
         DO: 
            FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
            AND z-list.selected NO-LOCK NO-ERROR. 
            do-it = AVAILABLE z-list. 
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
              pax = res-line.erwachs. 
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                  AND reslin-queasy.resnr = res-line.resnr 
                  AND reslin-queasy.reslinnr = res-line.reslinnr 
                  AND reslin-queasy.date1 LE datum 
                  AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                  pax = reslin-queasy.number3. 
                FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
         
                consider-it = YES. 
                IF res-line.zimmerfix THEN 
                DO: 
                  FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                    AND rline1.reslinnr NE res-line.reslinnr 
                    AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                    AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
                  IF AVAILABLE rline1 THEN consider-it = NO. 
             END.
            
                CREATE room-list.
                IF AVAILABLE zimkateg THEN room-list.rmcat = zimkateg.kurzbez.
                ASSIGN 
                      room-list.qty             = res-line.zimmeranz 
                      room-list.resnr           = string(res-line.resnr) 
                      room-list.name            = res-line.name 
                      room-list.rmno            = res-line.zinr 
                      room-list.arrival         = res-line.ankunft 
                      room-list.depart          = res-line.abreise 
                      room-list.argt            = res-line.arrangement
                      room-list.segment         = segment.bezeich
                      room-list.Adult           = res-line.erwachs * res-line.zimmeranz
                      room-list.compli          = res-line.gratis * res-line.zimmeranz
                      room-list.ch1             = res-line.kind1 * res-line.zimmeranz
                      room-list.ch2             = res-line.kind2 * res-line.zimmeranz
                      room-list.currency        = waehrung.wabkurz
                      room-list.pax             = (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                  + res-line.gratis) * res-line.zimmeranz

                .
                IF guest.karteityp NE 0 THEN
                  room-list.company         = guest.name + ", " + guest.vorname1 
                                              + " " + guest.anrede1 + guest.anredefirma. 
                  tot-pax                   = tot-pax + ((res-line.erwachs + res-line.kind1 + res-line.kind2 
                                              + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz).
                  tot-adult                 = tot-adult + (res-line.erwachs * res-line.zimmeranz).
                  tot-ch1                   = tot-ch1 + (res-line.kind1 * res-line.zimmeranz).
                  tot-ch2                   = tot-ch2 + (res-line.kind2 * res-line.zimmeranz).
                  tot-compli                = tot-compli + (res-line.gratis * res-line.zimmeranz).
                  tot-qty                   = tot-qty + res-line.zimmeranz.
             
             END. /* Global Reservation */ 
         
     END. /*for*/
  END. /*case-type = 16*/


  IF tot-pax NE 0 THEN
  DO:
        CREATE room-list.
        ASSIGN
         room-list.name           = "T O T A L"
         room-list.adult          = tot-adult
         room-list.compli         = tot-compli
         room-list.ch1            = tot-ch1
         room-list.ch2            = tot-ch2
         room-list.qty            = tot-qty
         room-list.pax            = tot-pax
         room-list.pocc           = tot-pocc
         .
        IF case-type EQ 7 THEN DO:
            ASSIGN
                room-list.lodg[4] = tot-lodg.
        END. /*Alder - Ticket A43151*/
  END.
END.

PROCEDURE count-rmcateg: 
DEFINE VARIABLE zikatnr AS INTEGER INITIAL 0. 
  FOR EACH rmcat-list: 
    delete rmcat-list. 
  END. 
  tot-room = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK BY zimmer.zikatnr: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR. 
    IF AVAILABLE zimkateg AND zimkateg.verfuegbarkeit THEN 
    DO: 
      tot-room = tot-room + 1. 
      IF zikatnr NE zimkateg.zikatnr THEN 
      DO: 
        create rmcat-list. 
        rmcat-list.zikatnr = zimkateg.zikatnr. 
        rmcat-list.anzahl = 1. 
        zikatnr = zimkateg.zikatnr. 
      END. 
      ELSE rmcat-list.anzahl = rmcat-list.anzahl + 1. 
    END. 
  END. 
END. 

