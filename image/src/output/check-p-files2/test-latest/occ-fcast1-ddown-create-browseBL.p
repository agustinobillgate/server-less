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

DEFINE INPUT PARAMETER TABLE FOR argt-list.
DEFINE INPUT PARAMETER TABLE FOR segm-list.
DEFINE INPUT PARAMETER TABLE FOR zikat-list.

DEF OUTPUT PARAMETER TABLE FOR room-list.

RUN create-browse.

PROCEDURE create-browse:  /*history*/
DEFINE VARIABLE curr-i      AS INTEGER.
DEFINE VARIABLE net-lodg    AS DECIMAL.
/*DEFINE VARIABLE datum       AS DATE. */
DEFINE VARIABLE datum1      AS DATE. 
DEFINE VARIABLE datum2      AS DATE. 
DEFINE VARIABLE d2          AS DATE. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE wd          AS INTEGER. 
DEFINE VARIABLE p-room      AS INTEGER. 
DEFINE VARIABLE prev-room   AS INTEGER. 
DEFINE VARIABLE p-pax       AS INTEGER. 
DEFINE VARIABLE avrg-rate   AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL. 
DEFINE VARIABLE consider-it AS LOGICAL. 
DEFINE VARIABLE rm-array    AS INTEGER EXTENT 18.  /* FOR calculation OF TOTAL */ 
DEFINE VARIABLE kont-doit   AS LOGICAL.
DEFINE VARIABLE allot-doit  AS LOGICAL.
DEFINE VARIABLE mtd-occ     AS DECIMAL NO-UNDO.
DEFINE VARIABLE rmsharer    AS LOGICAL INITIAL NO.

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

DEFINE VAR tot-pax          AS INTEGER.
DEFINE VAR tot-adult        AS INTEGER.
DEFINE VAR tot-ch1          AS INTEGER.
DEFINE VAR tot-ch2          AS INTEGER.
DEFINE VAR tot-compli       AS INTEGER.
DEFINE VAR tot-nights       AS INTEGER.
DEFINE VAR tot-qty          AS INTEGER.
DEFINE VAR tot-pocc         AS DECIMAL.
DEFINE VAR tot-lodg         AS DECIMAL.     /*Alder - Ticket A43151*/

DEFINE VARIABLE tot-room        AS INTEGER NO-UNDO.
DEFINE VARIABLE mtd-tot-room    AS INTEGER NO-UNDO. 
DEFINE VARIABLE accum-tot-room  AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE actual-tot-room AS INTEGER NO-UNDO. 

    tot-room = 0. 
    FOR EACH zimmer WHERE sleeping NO-LOCK: 
      IF all-zikat THEN tot-room = tot-room + 1. 
      ELSE 
      DO: 
        FIND FIRST zikat-list WHERE zikat-list.zikatnr = zimmer.zikatnr 
          AND zikat-list.selected NO-LOCK NO-ERROR. 
        IF AVAILABLE zikat-list THEN tot-room = tot-room + 1. 
      END. 
    END.     
    
    IF case-type = 1 THEN
    DO:
        FOR EACH genstat WHERE genstat.datum GE (datum - 1)
            AND genstat.datum LE to-date 
            AND genstat.resstatus NE 13 
            AND genstat.segmentcode NE 0 
            AND genstat.res-logic[2] EQ YES 
            USE-INDEX gastnrmember_ix NO-LOCK ,
            FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK ,
            FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK,
            FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-LOCK,
            FIRST res-line WHERE res-line.resnr = genstat.resnr 
            AND res-line.reslinnr = genstat.res-int[1] NO-LOCK ,
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode :  
             
             IF genstat.datum EQ (datum - 1) THEN
             DO:
                do-it = YES.
                IF genstat.res-date[1] LT genstat.datum
                    AND genstat.res-date[2] = genstat.datum AND genstat.resstatus = 8 THEN do-it = NO.
                
                IF do-it AND NOT all-segm THEN 
                DO: 
                  FIND FIRST s-list WHERE s-list.segm = genstat.segmentcode 
                    AND s-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE s-list. 
                END. 
                IF do-it AND NOT all-argt THEN 
                DO: 
                  FIND FIRST a-list WHERE a-list.argt = genstat.argt 
                    AND a-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE a-list. 
                END. 
                IF do-it AND NOT all-zikat THEN 
                DO: 
                  FIND FIRST z-list WHERE z-list.zikatnr = genstat.zikatnr 
                    AND z-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE z-list. 
                END. 


                IF do-it = YES THEN DO:
                    CREATE room-list.
                    ASSIGN 
                      room-list.qty                   = room-list.qty + 1
                      room-list.name                  = guest.name + ", " + guest.vorname1 + " " 
                                                               + guest.anrede1 + guest.anredefirma
                      room-list.resnr                 = STRING(genstat.resnr)
                      room-list.rmcat                 = zimkateg.kurzbez 
                      room-list.rmno                  = genstat.zinr 
                      room-list.pocc                  = (room-list.qty / tot-room) * 100
                      
                      room-list.depart                = genstat.res-date[2] 
                      room-list.arrival               = genstat.res-date[1] 
                      room-list.argt                  = genstat.argt
                      room-list.nights                = res-line.anztage
                      room-list.currency              = waehrung.wabkurz  
                      room-list.segment               = segment.bezeich
                      room-list.pax                   = genstat.erwachs + genstat.kind1 + genstat.kind2 +  genstat.gratis
                      room-list.Adult                 = genstat.erwachs
                      room-list.compli                = genstat.gratis
                      room-list.ch1                   = genstat.kind1
                      room-list.ch2                   = genstat.kind2.

                    
                    IF guest.karteityp NE 0 THEN
                        room-list.company          = guest.name + ", " + guest.vorname1 
                                                     + " " + guest.anrede1 + guest.anredefirma. 
                        tot-adult   = tot-adult + genstat.erwachs.
                        tot-ch1     = tot-ch1 + genstat.kind1.
                        tot-compli  = tot-compli + genstat.gratis .
                        tot-ch2     = tot-ch2 + genstat.kind2 + genstat.kind3.
                        tot-pocc    = tot-pocc + (room-list.qty / tot-room) * 100.
                        tot-nights  = tot-nights + res-line.anztage.
                        tot-qty     = tot-qty + 1.
                        tot-pax     = tot-adult + tot-ch1 + tot-ch2 + tot-compli.                                      
                END.                           
            END.
        END.
    END. /*Inhouse*/
    ELSE IF case-type = 3 THEN
    DO:
        FOR EACH genstat WHERE genstat.res-date[1] GE datum
            AND genstat.res-date[1] LE to-date 
            AND genstat.resstatus NE 13 
            AND genstat.segmentcode NE 0 
            AND genstat.res-logic[2] EQ YES 
            USE-INDEX gastnrmember_ix NO-LOCK,
            FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK,
            FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode :
             IF genstat.datum EQ datum THEN
             DO:
                ASSIGN do-it = YES.
                IF do-it AND NOT all-segm THEN 
                DO: 
                  FIND FIRST s-list WHERE s-list.segm = genstat.segmentcode 
                    AND s-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE s-list. 
                END. 
                IF do-it AND NOT all-argt THEN 
                DO: 
                  FIND FIRST a-list WHERE a-list.argt = genstat.argt 
                    AND a-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE a-list. 
                END. 
                IF do-it AND NOT all-zikat THEN 
                DO: 
                  FIND FIRST z-list WHERE z-list.zikatnr = genstat.zikatnr 
                    AND z-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE z-list. 
                END. 
                
                IF do-it THEN DO:
                    CREATE room-list.
                    ASSIGN 
                      room-list.qty                   = room-list.qty + 1
                      room-list.name                  = guest.name + ", " + guest.vorname1 + " " 
                                                        + guest.anrede1 + guest.anredefirma
                      room-list.resnr                 = STRING(genstat.resnr)
                      room-list.rmcat                 = zimkateg.kurzbez 
                      room-list.rmno                  = genstat.zinr 
                      room-list.kurzbez               = zimkateg.kurzbez
                      room-list.depart                = genstat.res-date[2] 
                      room-list.arrival               = genstat.res-date[1] 
                      room-list.argt                  = genstat.argt
                      room-list.pax                   = genstat.erwachs + genstat.kind1 + genstat.kind2 +  genstat.gratis
                      room-list.Adult                 = genstat.erwachs
                      room-list.compli                = genstat.gratis
                      room-list.ch1                   = genstat.kind1
                      room-list.ch2                   = genstat.kind2
                      room-list.currency              = waehrung.wabkurz  
                      room-list.segment               =  segment.bezeich
                     .
                     IF guest.karteityp NE  0 THEN
                            room-list.company          = guest.name + ", " + guest.vorname1 
                                                                 + " " + guest.anrede1 + guest.anredefirma. 
                            tot-pax     = tot-pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 
                                                + genstat.gratis).
                            tot-adult   = tot-adult + genstat.erwachs.
                            tot-ch1     = tot-ch1 + genstat.kind1 .
                            tot-compli = tot-compli + genstat.gratis .
                            tot-ch2     = tot-ch2 + genstat.kind2 .
                            tot-pocc   = tot-pocc + (room-list.qty / tot-room) * 100.
                           /* tot-compli = tot-compli + (res-line.gratis * res-line.zimmeranz).
                            tot-nights = tot-nights + res-line.anztage.*/
                            tot-qty      = tot-qty + 1.
                     END.
                END.                
            END.
    END. /*arrival*/

    ELSE IF case-type = 5 THEN
    DO:
        FOR EACH genstat WHERE genstat.res-date[2] GE datum
            AND genstat.res-date[2] LE to-date 
            AND genstat.resstatus NE 13 
            AND genstat.segmentcode NE 0 
            AND genstat.res-logic[2] EQ YES 
            AND genstat.zinr NE " "
            USE-INDEX gastnrmember_ix NO-LOCK,
            FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK,
            FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode :
            DO:
                IF genstat.res-date[2] EQ datum THEN DO:
                    ASSIGN do-it = YES.
                    IF do-it AND NOT all-segm THEN 
                    DO: 
                      FIND FIRST s-list WHERE s-list.segm = genstat.segmentcode 
                        AND s-list.selected NO-LOCK NO-ERROR. 
                      do-it = AVAILABLE s-list. 
                    END. 

                    IF do-it AND NOT all-argt THEN 
                    DO: 
                      FIND FIRST a-list WHERE a-list.argt = genstat.argt 
                        AND a-list.selected NO-LOCK NO-ERROR. 
                      do-it = AVAILABLE a-list. 
                    END. 
                    
                    IF do-it AND NOT all-zikat THEN 
                    DO: 
                      FIND FIRST z-list WHERE z-list.zikatnr = genstat.zikatnr 
                        AND z-list.selected NO-LOCK NO-ERROR. 
                      do-it = AVAILABLE z-list. 
                    END. 

                    IF do-it THEN DO:
                        FIND FIRST room-list WHERE room-list.resnr = STRING(genstat.resnr)
                            AND room-list.rmno = genstat.zinr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE room-list THEN DO:
                            CREATE room-list.
                            ASSIGN 
                              room-list.qty                   = room-list.qty + 1
                              room-list.name                  = guest.name + ", " + guest.vorname1 + " " 
                                                                + guest.anrede1 + guest.anredefirma
                              room-list.resnr                 = STRING(genstat.resnr)
                              room-list.rmcat                 = zimkateg.kurzbez 
                              room-list.rmno                  = genstat.zinr 
                              room-list.pocc                  = (room-list.qty / tot-room) * 100
                              room-list.kurzbez               = zimkateg.kurzbez 
                              room-list.depart                = genstat.res-date[2] 
                              room-list.arrival               = genstat.res-date[1] 
                              room-list.argt                  = genstat.argt
                              room-list.pax                   = genstat.erwachs + genstat.kind1 + genstat.kind2 +  genstat.gratis
                              room-list.Adult                 = genstat.erwachs
                              room-list.compli                = genstat.gratis
                              room-list.ch1                   = genstat.kind1
                              room-list.ch2                   = genstat.kind2
                              room-list.currency              = waehrung.wabkurz  
                              room-list.segment               = segment.bezeich
                              .
                            IF guest.karteityp NE 0 THEN
                                room-list.company       = guest.name + ", " + guest.vorname1 
                                                                     + " " + guest.anrede1 + guest.anredefirma. 
                                tot-pax     = tot-pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 
                                              + genstat.gratis).
                                tot-adult   = tot-adult + genstat.erwachs.
                                tot-ch1     = tot-ch1 + genstat.kind1 .
                                tot-compli  = tot-compli + genstat.gratis .
                                tot-ch2     = tot-ch2 + genstat.kind2 .
                                tot-pocc    = tot-pocc + (room-list.qty / tot-room) * 100.
                                tot-qty     = tot-qty + 1.
                        END.
                    END.                                       
                END.                
            END.
        END.
        /*FOR EACH genstat WHERE genstat.datum GE datum
            AND genstat.datum LE to-date 
            AND genstat.resstatus NE 13 
            AND genstat.segmentcode NE 0 
            AND genstat.res-logic[2] EQ YES 
            USE-INDEX gastnrmember_ix NO-LOCK,
            FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK,
            FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode :
            IF genstat.res-date[1] LT datum AND genstat.res-date[2] GT datum THEN 
            DO:
            CREATE room-list.
            ASSIGN 
              room-list.qty                   = room-list.qty + 1
              room-list.name                  = guest.name + ", " + guest.vorname1 + " " 
                                                       + guest.anrede1 + guest.anredefirma
              room-list.resnr                 = STRING(genstat.resnr)
              room-list.rmcat                 = zimkateg.kurzbez 
              room-list.rmno                  = genstat.zinr 
              room-list.pocc                  = (room-list.qty / tot-room) * 100
              /*room-list.groupname           = reservation.groupname*/
              room-list.kurzbez               = zimkateg.kurzbez 
              /*room-list.bezeich             = zimkateg.bezeich*/
              room-list.depart                = genstat.res-date[2] 
              room-list.arrival               = genstat.res-date[1] 
              room-list.argt                  = genstat.argt
              room-list.pax                   = genstat.erwachs + genstat.kind1 + genstat.kind2 +  genstat.gratis
              room-list.Adult                 = genstat.erwachs
              room-list.compli                = genstat.gratis
              room-list.ch1                   = genstat.kind1
              room-list.ch2                   = genstat.kind2
              room-list.currency              = waehrung.wabkurz  
              room-list.segment               =  segment.bezeich
              .
                IF guest.karteityp NE 0 THEN
                      room-list.company       = guest.name + ", " + guest.vorname1 
                                                         + " " + guest.anrede1 + guest.anredefirma. 
                    tot-pax     = tot-pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 
                                  + genstat.gratis).
                    tot-adult   = tot-adult + genstat.erwachs.
                    tot-ch1     = tot-ch1 + genstat.kind1 .
                    tot-compli  = tot-compli + genstat.gratis .
                    tot-ch2     = tot-ch2 + genstat.kind2 .
                    tot-pocc    = tot-pocc + (room-list.qty / tot-room) * 100.
                    tot-qty     = tot-qty + 1.
            END.
        END.*/
    END. /*Depart*/
    ELSE IF case-type = 7 THEN
    DO:
        FOR EACH genstat WHERE genstat.datum GE datum
            AND genstat.datum LE to-date 
            AND genstat.resstatus NE 13 
            AND genstat.segmentcode NE 0 
            AND genstat.res-logic[2] EQ YES 
            USE-INDEX gastnrmember_ix NO-LOCK,
            FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK,
            FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode :
              IF genstat.res-date[1] LT genstat.datum
                AND genstat.res-date[2] = genstat.datum 
                AND genstat.resstatus = 8 THEN .
              ELSE IF genstat.datum EQ datum THEN DO:       
                
                ASSIGN do-it = YES.
                IF do-it AND NOT all-segm THEN 
                DO: 
                  FIND FIRST s-list WHERE s-list.segm = genstat.segmentcode 
                    AND s-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE s-list. 
                END. 
                IF do-it AND NOT all-argt THEN 
                DO: 
                  FIND FIRST a-list WHERE a-list.argt = genstat.argt 
                    AND a-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE a-list. 
                END. 
                IF do-it AND NOT all-zikat THEN 
                DO: 
                  FIND FIRST z-list WHERE z-list.zikatnr = genstat.zikatnr 
                    AND z-list.selected NO-LOCK NO-ERROR. 
                  do-it = AVAILABLE z-list. 
                END. 

                IF do-it THEN DO:
                    CREATE room-list.
                    ASSIGN 
                      room-list.qty                   = room-list.qty + 1
                      room-list.name                  = guest.name + ", " + guest.vorname1 + " " 
                                                        + guest.anrede1 + guest.anredefirma
                      room-list.resnr                 = STRING(genstat.resnr)
                      room-list.rmcat                 = zimkateg.kurzbez 
                      room-list.rmno                  = genstat.zinr 
                      room-list.pocc                  = (room-list.qty / tot-room) * 100
                      /*room-list.groupname           = reservation.groupname*/
                      room-list.kurzbez               = zimkateg.kurzbez 
                      /*room-list.bezeich             = zimkateg.bezeich*/
                      room-list.depart                = genstat.res-date[2] 
                      room-list.arrival               = genstat.res-date[1] 
                      room-list.argt                  = genstat.argt
                      room-list.pax                   = genstat.erwachs + genstat.kind1 + genstat.kind2 +  genstat.gratis
                      room-list.Adult                 = genstat.erwachs
                      room-list.compli                = genstat.gratis
                      room-list.ch1                   = genstat.kind1
                      room-list.ch2                   = genstat.kind2
                      room-list.currency              = waehrung.wabkurz  
                      room-list.segment               =  segment.bezeich
                      room-list.pocc                  = (room-list.qty / tot-room) * 100
                      room-list.lodg[4]               = genstat.logis   /*Alder - Ticket A43151*/
                     .
            
                    IF guest.karteityp NE 0 THEN
                        room-list.company     = guest.name + ", " + guest.vorname1 
                                                + " " + guest.anrede1 + guest.anredefirma. 
                        tot-pax               = tot-pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 
                                                + genstat.gratis).
                        tot-adult             = tot-adult + genstat.erwachs.
                        tot-ch1               = tot-ch1 + genstat.kind1 .
                        tot-compli            = tot-compli + genstat.gratis .
                        tot-ch2               = tot-ch2 + genstat.kind2 .
                        tot-pocc              = tot-pocc + (room-list.qty / tot-room) * 100.
                        tot-qty               = tot-qty + 1.
                        tot-lodg              = tot-lodg + genstat.logis.   /*Alder - Ticket A43151*/
    
                    END.                
            END.
        END.
        END. /*Occupied room*/
     
        ELSE IF case-type = 15 THEN
         DO:
             FIND FIRST zinrstat WHERE zinrstat.zinr = "ooo" 
                AND zinrstat.datum = datum NO-LOCK NO-ERROR. 
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
        IF tot-pax NE 0 THEN
        DO:
                CREATE room-list.
                ASSIGN
                 room-list.name                 = "T O T A L"
                 room-list.adult                = tot-adult
                 room-list.compli               = tot-compli
                 room-list.ch1                  = tot-ch1
                 room-list.ch2                  = tot-ch2
                 room-list.nights               = tot-nights
                 room-list.qty                  = tot-qty
                 room-list.pax                  = tot-pax
                 room-list.pocc                 = tot-pocc
                 .
                IF case-type EQ 7 THEN DO:
                    ASSIGN room-list.lodg[4] = tot-lodg.
                END. /*Alder - Ticket A43151*/
         END.
END.

