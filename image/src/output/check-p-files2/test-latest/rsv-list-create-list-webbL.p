DEFINE TEMP-TABLE output-list
  FIELD bk-stat   AS CHAR
  FIELD bk-datum  AS DATE
  FIELD engager   AS CHAR
  FIELD contact   AS CHAR
  FIELD bk-event  AS CHAR
  FIELD venue     AS CHAR
  FIELD bk-time   AS CHAR
  FIELD pax       AS INTEGER
  FIELD tablesetup  AS CHAR 
  FIELD room-rev  AS DECIMAL
  FIELD fb-rev    AS DECIMAL
  FIELD other-rev AS DECIMAL
  FIELD total-rev AS DECIMAL
  FIELD cm-id     AS CHAR
  FIELD sales     AS CHAR
  FIELD crdate    AS DATE
  FIELD cutOff    AS DATE
  FIELD segment   AS CHAR
  FIELD sob       AS CHAR
  FIELD resnr     AS INTEGER 
  FIELD reslinnr  AS INTEGER 
  FIELD remark    AS CHAR
  FIELD resstatus AS INTEGER 
  FIELD datum     AS DATE
  FIELD gastnr    AS INTEGER
.  

DEF INPUT  PARAMETER from-date          AS DATE.
DEF INPUT  PARAMETER to-date            AS DATE.
DEF INPUT  PARAMETER inp-room           AS CHARACTER.
DEF INPUT  PARAMETER stat-screen-value  AS CHAR.
DEF INPUT  PARAMETER mi-created-chk     AS LOGICAL.
DEF INPUT  PARAMETER mi-event-chk       AS LOGICAL.
DEF INPUT  PARAMETER mi-engager-chk     AS LOGICAL.
DEF INPUT  PARAMETER mi-room-chk        AS LOGICAL.
DEF INPUT  PARAMETER mi-sales-chk       AS LOGICAL.
DEF INPUT  PARAMETER mi-segment-chk     AS LOGICAL.
DEF INPUT  PARAMETER mi-cutoff-chk      AS LOGICAL.
DEF OUTPUT PARAMETER gastnr             AS INT.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE total-estrev AS DECIMAL INITIAL 0. 
DEFINE VARIABLE total-paid  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE troomrev    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE tfbrev      AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE tothrev     AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE ttrev       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".

DEFINE VARIABLE do-it AS LOGICAL INIT NO.

RUN create-list.

PROCEDURE create-list: 
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
          IF AVAILABLE bk-veran THEN 
          DO:
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.                     
          END. 
        END. 
     ELSE IF mi-event-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bis-datum: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END. 
     ELSE IF mi-engager-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bestellt_durch: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END. 
     ELSE IF mi-room-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.raeume[1]: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END.
     ELSE IF mi-sales-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.vgeschrieben:
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END.
     ELSE IF mi-segment-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-veran.segmentcode: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END.
     ELSE IF mi-cutoff-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK,  
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-veran.segmentcode: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
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
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END. 
    ELSE IF mi-event-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bis-datum: 
          IF AVAILABLE bk-veran THEN 
          DO:
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END. 
     ELSE IF mi-engager-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bestellt_durch: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END. 
     ELSE IF mi-room-chk = TRUE THEN
        FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus = int(stat-screen-value) NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.raeume[1]: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END. 
     ELSE IF mi-sales-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.vgeschrieben: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END.
     ELSE IF mi-segment-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK, 
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-veran.segmentcode: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END.
     ELSE IF mi-cutoff-chk = TRUE THEN
         FOR EACH bk-func WHERE bk-func.bis-datum GE from-date AND bk-func.bis-datum LE to-date AND 
          bk-func.resstatus LE 3 NO-LOCK,  
          FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-veran.segmentcode: 
          IF AVAILABLE bk-veran THEN 
          DO: 
            IF inp-room NE "" AND bk-func.raeume[1] = inp-room THEN do-it = YES.
            ELSE IF inp-room = "" THEN do-it = YES.
            ELSE do-it = NO.
            other-rev = 0.
            IF do-it THEN
            DO:
              FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-rev = other-rev + (bk-rart.preis * anzahl).
              END.
              RUN create-output-list.
            END.
          END. 
        END.
  END. 
END. 

PROCEDURE create-output-list:

  CREATE output-list. 
  ASSIGN 
    output-list.bk-datum = bk-func.bis-datum
    output-list.engager = bk-func.bestellt_durch
    output-list.contact = bk-func.v-kontaktperson[1]
    output-list.bk-event = bk-func.zweck[1]
    output-list.venue = bk-func.raeume[1]
    output-list.bk-time = bk-func.uhrzeit
    output-list.pax = bk-func.personen
    output-list.room-rev = bk-func.rpreis[1]
    output-list.fb-rev = bk-func.rpreis[7] * bk-func.rpersonen[1]
    output-list.other-rev = other-rev
    output-list.total-rev = bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-rev
    output-list.bk-stat = bk-func.c-resstatus[1]
    output-list.resnr         = bk-func.veran-nr 
    output-list.reslinnr      = bk-func.veran-seite 
    output-list.resstatus     = bk-func.resstatus 
    output-list.datum         = bk-func.datum 
    output-list.sob           = bk-func.technik[2]
    output-list.crdate        = bk-veran.kontaktfirst
    output-list.tablesetup    = bk-func.tischform[1]  /*ITA 240314*/
    output-list.remark        = bk-veran.bemerkung  /*ITA 240314*/
    gastnr = bk-veran.gastnr
    output-list.gastnr = bk-veran.gastnr
  . 
  FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
  IF AVAILABLE bk-reser THEN output-list.cutOff = bk-reser.limitdate. 

  FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK NO-ERROR.
  IF AVAILABLE guest THEN
    ASSIGN
      output-list.cm-id = guest.phonetik2
      output-list.sales = guest.phonetik3.

  FIND FIRST queasy WHERE queasy.KEY = 146 
    AND queasy.char1 = STRING(bk-veran.segmentcode) NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN output-list.segment = char3.

  ASSIGN
    total-estrev = total-estrev + bk-veran.deposit
    total-paid   = total-paid   + bk-veran.total-paid
    troomrev     = troomrev     + bk-func.rpreis[1]
    tfbrev       = tfbrev       + (bk-func.rpreis[7] * bk-func.rpersonen[1])
    tothrev      = tothrev      + other-rev
    ttrev        = ttrev        + (bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) 
                  + other-rev).
END.

 
