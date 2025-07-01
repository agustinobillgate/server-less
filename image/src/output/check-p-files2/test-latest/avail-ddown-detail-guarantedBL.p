.
DEFINE TEMP-TABLE rlist
    FIELD resnr                 AS CHAR LABEL "ResNo"
    FIELD zinr                  LIKE res-line.zinr
    FIELD ankunft               LIKE res-line.ankunft
    FIELD abreise               LIKE res-line.abreise
    FIELD zimmeranz             LIKE res-line.zimmeranz
    FIELD resstatus             LIKE res-line.resstatus
    FIELD zipreis               LIKE res-line.zipreis
    FIELD erwachs               LIKE res-line.erwachs
    FIELD kind1                 LIKE res-line.kind1
    FIELD gratis                LIKE res-line.gratis
    FIELD NAME                  LIKE res-line.NAME
    FIELD rsvName               AS CHAR FORMAT "x(24)" LABEL "Reserved Name"
    FIELD confirmed             AS LOGICAL INITIAL NO
    FIELD sleeping              AS LOGICAL INITIAL YES
    FIELD bezeich               AS CHAR FORMAT "x(15)"
    FIELD res-status            AS CHAR FORMAT "x(15)"
.

DEF INPUT PARAMETER datum AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rlist.

RUN detail-guaranted.
MESSAGE 3 datum
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
PROCEDURE detail-guaranted :
DEFINE VARIABLE qty             AS INTEGER INITIAL 0.
DEFINE VARIABLE tot-adult       AS INTEGER INITIAL 0.
DEFINE VARIABLE tot-ch          AS INTEGER INITIAL 0.
DEFINE VARIABLE tot-rmrate      AS INTEGER INITIAL 0.
DEFINE VARIABLE do-it           AS LOGICAL NO-UNDO.
DEFINE VARIABLE vhp-limited     AS LOGICAL NO-UNDO INIT NO.

    FOR EACH zimkateg NO-LOCK:
        FOR EACH res-line WHERE res-line.active-flag = 0 
            AND res-line.resstatus = 1 AND res-line.zikatnr = zimkateg.zikatnr 
            AND res-line.ankunft LE datum AND res-line.abreise GT datum 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
            do-it = YES. 
            IF res-line.zinr NE "" THEN 
            DO: 
              FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
              do-it = zimmer.sleeping. 
            END. 
            
            IF do-it AND vhp-limited THEN 
            DO:
              FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                NO-LOCK.
              FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                NO-LOCK NO-ERROR.
              do-it = AVAILABLE segment AND segment.vip-level = 0.
            END.
            
            IF do-it THEN 
            DO:
              CREATE rlist.
              ASSIGN
                  rlist.resnr           = STRING(res-line.resnr)
                  rlist.name            = res-line.name
                  rlist.ankunft         = res-line.ankunft
                  rlist.abreise         = res-line.abreise
                  rlist.zimmeranz       = rlist.zimmeranz
                  rlist.zipreis         = res-line.zipreis
                  rlist.erwachs         = res-line.erwachs
                  rlist.kind1           = res-line.kind1 + res-line.kind2
                  .
            END. 
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
            rlist.rsvName = guest.NAME + ", " + guest.anredefirma. 

            ASSIGN 
                qty = qty + rlist.zimmeranz
                tot-adult = tot-adult + rlist.erwachs
                tot-ch     = tot-ch + rlist.kind1
                tot-rmrate = tot-rmrate + rlist.zipreis. 
        END.  
    END.
    IF qty NE 0 THEN
    DO:
          CREATE rlist.
          ASSIGN
              rlist.rsvName          = "T O T A L"
              rlist.ankunft          = ?
              rlist.abreise          = ?
              rlist.zimmeranz        = qty
              rlist.zipreis          = tot-rmrate
              rlist.erwachs          = tot-adult
              rlist.kind1            = tot-ch
          .
    END.
END.

