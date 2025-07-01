
DEFINE TEMP-TABLE rmcat-list 
  FIELD zikatnr                 AS INTEGER 
  FIELD anzahl                  AS INTEGER 
  FIELD sleeping                AS LOGICAL INITIAL YES
  FIELD kurzbez                 AS CHAR 
  FIELD bezeich                 AS CHAR FORMAT "x(20)" 
  FIELD zinr                    AS CHAR 
. 

DEFINE TEMP-TABLE room-list 
   FIELD datum                  AS DATE
   FIELD zikatnr                AS INTEGER 
   FIELD sleeping               AS LOGICAL INITIAL YES 
   FIELD bezeich                AS CHAR FORMAT "x(10)" 
   FIELD room                   AS INTEGER FORMAT "->>9" /*available room after allotment*/ 
   FIELD t-avail                AS INTEGER FORMAT ">>9"  /*total available*/
   FIELD t-room                 AS INTEGER FORMAT ">>9" 
   FIELD t-ooo                  AS INTEGER FORMAT ">>9"
   FIELD t-occ                  AS INTEGER FORMAT ">>9"
   FIELD t-alot                 AS INTEGER FORMAT ">>9"
   FIELD t-lnight               AS INTEGER FORMAT ">>>9" 
   FIELD t-arrival              AS INTEGER FORMAT ">>>9" 
   FIELD t-depart               AS INTEGER FORMAT ">>>9"
   FIELD resnr                  AS CHAR FORMAT "x(7)" 
   FIELD name                   AS CHAR FORMAT "x(24)" 
   FIELD groupname              AS CHAR FORMAT "x(24)" 
   FIELD rmno                   LIKE zimmer.zinr
   FIELD depart                 AS DATE 
   FIELD arrival                AS DATE 
   FIELD rmcat                  AS CHAR FORMAT "x(6)" 
   FIELD kurzbez                AS CHAR 
   FIELD pax                    AS INTEGER FORMAT ">>9"
   FIELD qty                    AS INTEGER FORMAT ">>9"
   FIELD Adult                  AS INTEGER FORMAT ">>9" 
   FIELD ch1                    AS INTEGER FORMAT ">>9" 
   FIELD ch2                    AS INTEGER FORMAT ">>9" 
   FIELD compli                 AS INTEGER FORMAT ">>9" 
   FIELD nat                    AS CHAR FORMAT "x(3)" 
   FIELD argt                   AS CHAR FORMAT "x(7)" 
   FIELD company                AS CHAR FORMAT "x(18)" 
   FIELD currency               AS CHAR FORMAT "x(4)"
   FIELD segment                AS CHAR FORMAT "x(4)"
   FIELD nights                 AS INTEGER FORMAT ">>>>>9"
   FIELD alot                   AS INTEGER
   FIELD pocc                   AS DECIMAL
   FIELD rentable               AS INTEGER
.

DEF INPUT PARAMETER case-type       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER incl-tentative  AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER mi-inactive     AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER datum           AS DATE    NO-UNDO.
DEF INPUT PARAMETER TABLE FOR rmcat-list.
DEF OUTPUT PARAMETER TABLE FOR room-list.

DEF VARIABLE vhp-limited AS LOGICAL NO-UNDO INIT NO.
DEF VARIABLE do-it       AS LOGICAL NO-UNDO.
DEF VARIABLE tot-room    AS INTEGER NO-UNDO INIT 0. 
DEF BUFFER rline1 FOR res-line.
RUN run-main.

PROCEDURE run-main :
DEFINE VARIABLE tot-actroom         AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-occrm           AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-ooo             AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-alot            AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-avail           AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-avail2          AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-rent            AS INTEGER NO-UNDO INITIAL 0.
   
    RUN count-rmcateg.
    
    FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES 
        NO-LOCK BY zimkateg.zikatnr: 
      FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimkateg.zikatnr 
        AND rmcat-list.sleeping NO-ERROR. 
      IF AVAILABLE rmcat-list THEN 
      DO: 
        create room-list. 
        ASSIGN
          room-list.room            = rmcat-list.anzahl
          room-list.t-avail         = rmcat-list.anzahl
          room-list.t-room          = rmcat-list.anzahl
          room-list.zikatnr         = zimkateg.zikatnr
          room-list.bezeich         = STRING(zimkateg.kurzbez,"x(6)") 
          room-list.datum           = datum
        .
        ASSIGN room-list.rentable = room-list.t-room.
      END.
    END.
    FOR EACH rmcat-list WHERE NOT rmcat-list.sleeping, 
          FIRST zimkateg WHERE zimkateg.zikatnr = rmcat-list.zikatnr NO-LOCK 
          BY zimkateg.zikatnr: 
          create room-list.
          ASSIGN
          room-list.sleeping        = NO
          room-list.room            = rmcat-list.anzahl
          room-list.t-avail         = rmcat-list.anzahl
          room-list.t-room          = rmcat-list.anzahl
          room-list.zikatnr         = zimkateg.zikatnr
          room-list.bezeich         = STRING(zimkateg.kurzbez,"x(6)") 
          room-list.datum           = datum
          .
          ASSIGN room-list.rentable = room-list.t-room.
    END.

    FOR EACH res-line WHERE res-line.active-flag LE 1 AND 
          res-line.resstatus LE 6 AND res-line.ankunft LE datum 
          AND res-line.abreise GT datum AND res-line.zikatnr = room-list.zikatnr 
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
              IF do-it THEN 
                  ASSIGN room-list.room     = room-list.room - 1
                         room-list.t-avail  = room-list.t-avail - 1.
    END. 
    
    IF case-type = 1 THEN
    DO:
        FOR EACH room-list WHERE room-list.sleeping: 
            FOR EACH res-line WHERE res-line.active-flag LE 1 
              AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
              AND res-line.resstatus NE 4 
              AND res-line.zikatnr = room-list.zikatnr 
              AND res-line.ankunft LE datum AND res-line.abreise GT datum 
              AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
              do-it = YES. 
              IF res-line.zinr NE "" THEN 
              DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
              END. 
    
              IF res-line.resstatus = 3 AND NOT incl-tentative THEN
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
                  room-list.t-occ       = room-list.t-occ + res-line.zimmeranz 
                  room-list.room        = room-list.room - res-line.zimmeranz
                  room-list.t-avail     =  room-list.t-avail - res-line.zimmeranz
                  .
            END.
        END. /*occupied room*/
    END.
    ELSE IF case-type = 9 THEN
    DO:
        FOR EACH room-list WHERE room-list.sleeping: 
            FOR EACH res-line WHERE res-line.resstatus = 6 
            AND active-flag = 1 AND res-line.zikatnr = room-list.zikatnr 
            AND res-line.abreise GT datum AND res-line.active-flag = 1
            AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
              do-it = YES. 
              IF res-line.zinr NE "" THEN 
              DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
              END. 
    
              IF res-line.resstatus = 3 AND NOT incl-tentative THEN
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
                  room-list.t-occ       = room-list.t-occ + res-line.zimmeranz 
                  room-list.room        = room-list.room - res-line.zimmeranz
                  room-list.t-avail     =  room-list.t-avail - res-line.zimmeranz
                  room-list.rentable    =  room-list.t-room - room-list.t-occ 
                  .
            END.
        END. /*occupied room*/
    END.


    FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
          FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
          AND zimmer.sleeping = YES NO-LOCK. 
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
          FIND FIRST room-list WHERE room-list.zikatnr = zimmer.zikatnr 
            AND room-list.sleeping. 
          IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
           ASSIGN
                room-list.t-ooo     = room-list.t-ooo + 1
                room-list.rentable  =   room-list.rentable - 1
                room-list.room      = room-list.room - 1
                room-list.t-avail     = room-list.t-avail  - 1
                
                .
    END. /*OOO*/
    
    FOR EACH kontline WHERE kontline.betriebsnr = 1 
          AND kontline.ankunft LE datum AND kontline.abreise GE datum 
          AND kontline.zikatnr = room-list.zikatnr 
          AND kontline.kontstatus = 1 NO-LOCK:                                      /* CR 05/04/24 | Fix for Serverless */
          ASSIGN
          room-list.t-alot  = room-list.t-alot + kontline.zimmeranz
          room-list.t-avail = room-list.room
          room-list.room    = room-list.room - kontline.zimmeranz
          . 
    END. /*allotment*/

    FOR EACH room-list WHERE room-list.sleeping: 
         FOR EACH res-line WHERE res-line.active-flag LE 1 
            AND res-line.resstatus LE 13 
            AND res-line.resstatus NE 4 
            AND res-line.resstatus NE 12
            AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
            NO-LOCK :
            IF res-line.abreise = datum AND res-line.resstatus NE 3 AND res-line.zikatnr = room-list.zikatnr THEN 
                ASSIGN room-list.t-depart = room-list.t-depart + res-line.zimmeranz.
            IF res-line.ankunft = datum AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tentative))  THEN
                ASSIGN room-list.t-arrival = room-list.t-arrival + res-line.zimmeranz.
        END.
        ASSIGN
          tot-actroom               =  tot-actroom + room-list.t-room
          tot-occrm                 =  tot-occrm + room-list.t-occ
          tot-ooo                   =  tot-ooo + room-list.t-ooo
          tot-alot                  =  tot-alot +  room-list.t-alot
          tot-avail                 =  tot-avail + room-list.t-avail
          tot-avail2                =  tot-avail2 + room-list.room
          tot-rent                  =  tot-rent   +  room-list.rentable
        .
    END.


    IF tot-actroom NE 0 THEN
    DO:
        CREATE room-list.
        ASSIGN 
              room-list.bezeich      = "TOTAL" 
              room-list.room         = tot-avail2
              room-list.t-avail      = tot-avail
              room-list.t-room       = tot-actroom
              room-list.t-ooo        = tot-ooo
              room-list.t-occ        = tot-occrm
              room-list.t-alot       = tot-alot   
              room-list.rentable   = tot-rent
              
             .
     END.
END.

PROCEDURE count-rmcateg: 
DEFINE VARIABLE zikatnr AS INTEGER NO-UNDO INITIAL 0. 
  FOR EACH rmcat-list: 
    delete rmcat-list. 
  END. 
  tot-room = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK BY zimmer.zikatnr: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimkateg.verfuegbarkeit THEN 
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
/* %%% */ 
  IF NOT mi-inactive THEN RETURN. 
  zikatnr = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = NO NO-LOCK BY zimmer.zikatnr: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimkateg.verfuegbarkeit THEN 
    DO: 
      IF zikatnr NE zimkateg.zikatnr THEN 
      DO: 
        create rmcat-list. 
        rmcat-list.zikatnr = zimkateg.zikatnr. 
        rmcat-list.anzahl = 1. 
        rmcat-list.sleeping = NO. 
        zikatnr = zimkateg.zikatnr. 
      END. 
      ELSE rmcat-list.anzahl = rmcat-list.anzahl + 1. 
    END. 
  END. 
/* %%% */ 
END. 
