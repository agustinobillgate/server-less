DEFINE TEMP-TABLE output-list 
  FIELD datum AS DATE
  FIELD engager AS CHAR
  FIELD contact-person AS CHAR
  FIELD ba-event AS CHAR
  FIELD venue AS CHAR
  FIELD ba-time AS CHAR
  FIELD pax AS INTEGER
  FIELD room-rev AS DECIMAL
  FIELD fb-rev AS DECIMAL
  FIELD other-rev AS DECIMAL
  FIELD total-rev AS DECIMAL
  FIELD salesId AS CHAR
  FIELD cmid AS CHAR
  FIELD resnr AS INTEGER 
  FIELD resline AS INTEGER
  FIELD tablesetup  AS CHAR
  FIELD remark      AS CHAR
  FIELD ba-status AS CHAR
. 

DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER troomrev    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEF OUTPUT PARAMETER tfbrev      AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEF OUTPUT PARAMETER tothrev     AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEF OUTPUT PARAMETER ttrev       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE total-rev AS DECIMAL INITIAL 0.

RUN journal-list.

PROCEDURE journal-list: 
  DEF VAR other-rev AS DECIMAL FORMAT "->>>,>>>,>>9.99".

  ASSIGN
        troomrev = 0
        tfbrev   = 0
        tothrev  = 0
        ttrev    = 0.

  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  FOR EACH b-history WHERE b-history.datum GE from-date AND b-history.datum LE to-date AND 
    b-history.resstatus NE 5 NO-LOCK: 
      other-rev = 0.
      FOR EACH bk-rart WHERE bk-rart.veran-nr = b-history.veran-nr AND
            bk-rart.veran-seite = b-history.veran-seite NO-LOCK:
            other-rev = other-rev + (bk-rart.preis * anzahl).
      END.
      CREATE output-list. 
      ASSIGN
          output-list.datum = b-history.datum
          output-list.engager = b-history.bestellt_durch
          output-list.contact-person = b-history.v-kontaktperson[1]
          output-list.ba-event = b-history.anlass[1]
          output-list.venue = b-history.raeume[1]
          output-list.ba-time = b-history.uhrzeit
          output-list.pax = b-history.personen.
      
      FIND FIRST bk-stat WHERE bk-stat.resnr = b-history.veran-nr
          NO-LOCK NO-ERROR.
      IF AVAILABLE bk-stat AND bk-stat.salesID NE "" THEN output-list.salesId = bk-stat.salesID.
      ELSE
      DO:
        FIND FIRST bk-veran WHERE bk-veran.veran-nr = b-history.veran-nr
            NO-LOCK NO-ERROR.
        IF AVAILABLE bk-veran THEN
        DO:
          IF bk-veran.betrieb-gast GT 0 THEN
          FIND FIRST bediener WHERE bediener.nr = bk-veran.betrieb-gast
             NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN output-list.salesId = bediener.userinit.
          ELSE
          DO:
            FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK.
            IF guest.phonetik3 NE "" THEN output-list.salesId = guest.phonetik3.
            ELSE output-list.salesId = "**".
            IF guest.phonetik2 NE "" THEN output-list.cmid 
              = STRING(guest.phonetik2, "x(2)").
            ELSE output-list.cmid = "**".
          END.
        END.
        ELSE output-list.salesId = "**".
      END.

      ASSIGN
          output-list.tablesetup = b-history.tischform[1]
          output-list.remark     = b-history.bemerkung
          output-list.resnr = b-history.veran-nr
          output-list.resline = b-history.veran-seite
          output-list.ba-status = b-history.c-resstatus[1]
          output-list.room-rev = b-history.rpreis[1]
          output-list.fb-rev = b-history.rpreis[7] * b-history.rpersonen[1]
          output-list.other-rev = other-rev
          output-list.total-rev = b-history.rpreis[1] + (b-history.rpreis[7] * b-history.rpersonen[1]) +
                                 other-rev
          total-rev = total-rev + b-history.deposit
          troomrev     = troomrev     + b-history.rpreis[1]
          tfbrev       = tfbrev       + (b-history.rpreis[7] * b-history.rpersonen[1])
          tothrev      = tothrev      + other-rev
          ttrev        = ttrev        + (b-history.rpreis[1] + (b-history.rpreis[7] * b-history.rpersonen[1]) 
                                       + other-rev).
  END. 
END. 
