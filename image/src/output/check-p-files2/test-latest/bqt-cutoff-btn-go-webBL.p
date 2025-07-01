
DEFINE TEMP-TABLE output-list
  FIELD bk-stat AS CHAR
  FIELD bk-datum AS DATE
  FIELD engager AS CHAR
  FIELD contact AS CHAR
  FIELD bk-event AS CHAR
  FIELD venue AS CHAR
  FIELD bk-time AS CHAR
  FIELD pax AS INTEGER
  FIELD room-rev AS DECIMAL
  FIELD fb-rev AS DECIMAL
  FIELD other-rev AS DECIMAL
  FIELD total-rev AS DECIMAL
  FIELD sales AS CHAR
  FIELD crdate AS DATE
  FIELD cutOff AS DATE
  FIELD resnr AS INTEGER
  FIELD reslinnr AS INTEGER
  FIELD resstatus AS INTEGER
  FIELD datum AS DATE
.

DEF INPUT  PARAMETER inp-room           AS CHAR.
DEF INPUT  PARAMETER from-date          AS DATE.
DEF INPUT  PARAMETER to-date            AS DATE.
DEF INPUT  PARAMETER stat-screen-value  AS CHAR.
DEF INPUT  PARAMETER mi-created-chk     AS LOGICAL.
DEF INPUT  PARAMETER mi-event-chk       AS LOGICAL.
DEF INPUT  PARAMETER mi-engager-chk     AS LOGICAL.
DEF INPUT  PARAMETER mi-room-chk        AS LOGICAL.
DEF OUTPUT PARAMETER troomrev           AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEF OUTPUT PARAMETER tfbrev             AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEF OUTPUT PARAMETER tothrev            AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEF OUTPUT PARAMETER ttrev              AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE total-estrev AS DECIMAL INITIAL 0. 
DEFINE VARIABLE total-paid AS DECIMAL INITIAL 0. 

IF inp-room = "" THEN RUN create-list. 
ELSE RUN create-list1.

PROCEDURE create-list: 
    ASSIGN
        troomrev = 0
        tfbrev   = 0
        tothrev  = 0
        ttrev    = 0.
    DEF VAR other-rev AS DECIMAL FORMAT "->>>,>>>,>>9.99".
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  IF stat-screen-value = "0" THEN 
  DO: 
    IF mi-created-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.

            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum 
                output-list.crdate    = bk-veran.kontaktfirst
                .
            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
                  */

              
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            . 
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
     ELSE IF mi-event-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bis-datum: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum 
                output-list.crdate    = bk-veran.kontaktfirst
                .

            /* Rulita 160625 | change str to temp-table output-list 
              STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
                 */  
 
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
         ELSE IF mi-engager-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bestellt_durch: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum 
                output-list.crdate    = bk-veran.kontaktfirst
                .
            /* Rulita 160625 | change str to temp-table output-list 
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
                  */  

            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
     ELSE IF mi-room-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.raeume[1]: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum 
                output-list.crdate    = bk-veran.kontaktfirst
                .
            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
                  */

            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
  END. 
  ELSE IF stat-screen-value = "1" OR stat-screen-value = "2" OR stat-screen-value = "3" THEN 
  DO: 
    IF mi-created-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum
                .
            
            /* Rulita 160625 | change str to temp-table output-list
             STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99") */
 
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
    ELSE IF mi-event-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bis-datum: 
          IF AVAILABLE bk-veran THEN 
          DO:
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum             
                . 

            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */

            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
     ELSE IF mi-engager-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bestellt_durch: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum            
                .

            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99") */
               
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid.
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
     ELSE IF mi-room-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.raeume[1]: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum             
                .

            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */

            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
  END. 
END. 
 
PROCEDURE create-list1: 
  DEF VAR other-rev AS DECIMAL FORMAT "->>>,>>>,>>9.99".
  ASSIGN
        troomrev = 0
        tfbrev   = 0
        tothrev  = 0
        ttrev    = 0.

  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  IF stat-screen-value = "0" THEN 
  DO: 
    IF mi-created-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK: 
          IF AVAILABLE bk-veran AND bk-func.raeume[1] = inp-room THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum             
                .
            
            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */
                  
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
    ELSE IF mi-event-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bis-datum: 
          IF AVAILABLE bk-veran AND bk-func.raeume[1] = inp-room THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum             
                .

            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */

            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END.
    ELSE IF mi-engager-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bestellt_durch: 
          IF AVAILABLE bk-veran AND bk-func.raeume[1] = inp-room THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum               
                .
            
            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */
                  
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END.
    ELSE IF mi-room-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.raeume[1]: 
          IF AVAILABLE bk-veran AND bk-func.raeume[1] = inp-room THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum             
                .
            
            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */
                  
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
     
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END.
  END. 
  ELSE IF stat-screen-value = "1" OR stat-screen-value = "2" OR stat-screen-value = "3" THEN 
  DO: 
      IF mi-created-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK: 
          IF AVAILABLE bk-veran THEN 
          DO:
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum             
                .

            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */
                  
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
      ELSE IF mi-event-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bis-datum: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.
            CREATE output-list. 
            ASSIGN
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum             
                .
                 
            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */
                  
            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
      ELSE IF mi-engager-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bestellt_durch: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.

            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum              
                .

            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */

            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
      ELSE IF mi-room-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.raeume[1]: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            other-rev = 0.
            FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
            END.

            CREATE output-list. 
            ASSIGN 
                output-list.bk-stat   = STRING(bk-func.c-resstatus[1])
                output-list.bk-datum  = bk-func.bis-datum
                output-list.engager   = STRING(bk-func.bestellt_durch)
                output-list.contact   = STRING(bk-func.v-kontaktperson[1])
                output-list.bk-event  = STRING(bk-func.zweck[1])
                output-list.venue     = STRING(bk-func.raeume[1])
                output-list.bk-time   = STRING(bk-func.uhrzeit)
                output-list.pax       = bk-func.personen
                output-list.room-rev  = bk-func.rpreis[1]
                output-list.fb-rev    = bk-func.rpreis[7] * bk-func.rpersonen[1]
                output-list.other-rev = other-rev
                output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
                output-list.sales     = bk-func.vgeschrieben
                output-list.resnr     = bk-func.veran-nr 
                output-list.reslinnr  = bk-func.veran-seite 
                output-list.resstatus = bk-func.resstatus 
                output-list.datum     = bk-func.datum              
                .

            /* Rulita 160625 | change str to temp-table output-list
            STR = STRING(bk-func.bis-datum,"99/99/99") + 
                  STRING(bk-func.bestellt_durch,"x(32)") + 
                  STRING(bk-func.v-kontaktperson[1],"x(32)") + 
                  STRING(bk-func.zweck[1],"x(18)") + 
                  STRING(bk-func.raeume[1],"x(12)") + 
                  STRING(bk-func.uhrzeit,"x(13)") + 
                  STRING(bk-func.personen,">,>>>") + 
                  STRING(bk-veran.deposit,">>>,>>>,>>9") + 
                  STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
                  STRING(bk-func.vgeschrieben,"x(2)") + 
                  STRING(bk-func.veran-nr,">>>,>>>") + 
                  STRING(bk-func.veran-seite,">>>") + 
                  STRING(bk-func.c-resstatus[1],"x(1)") +
                  STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
                  STRING(other-rev, "->>>,>>>,>>9.99") + 
                  STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev), "->>>,>>>,>>>,>>9.99")
            */

            FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
            IF AVAILABLE bk-reser THEN
              output-list.cutOff = bk-reser.limitdate
            .
            total-estrev = total-estrev + bk-veran.deposit. 
            total-paid   = total-paid   + bk-veran.total-paid. 
            troomrev     = troomrev     + bk-func.rpreis[1].
            tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1]).
            tothrev      = tothrev      + other-rev.
            ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                                           + other-rev).
          END. 
        END. 
  END. 
END. 

