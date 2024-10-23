
DEFINE TEMP-TABLE glodging-turnover
    FIELD cust-name         AS CHARACTER FORMAT "x(24)"       
    FIELD t-o               AS DECIMAL FORMAT ">>,>>>,>>9"      INITIAL 0
    FIELD budget-to         AS DECIMAL FORMAT ">>,>>>,>>9"      INITIAL 0
    FIELD percnt-to         AS DECIMAL FORMAT ">>9.9"           INITIAL 0
    FIELD ytd               AS DECIMAL FORMAT ">,>>>,>>>,>>9"   INITIAL 0
    FIELD budget-ytd        AS DECIMAL FORMAT ">,>>>,>>>,>>9"   INITIAL 0
    FIELD percnt-ytd        AS DECIMAL FORMAT ">>9.9"           INITIAL 0
    FIELD lodg-to           AS DECIMAL FORMAT ">>,>>>,>>9"      INITIAL 0
    FIELD budget-lodg-to    AS DECIMAL FORMAT ">>,>>>,>>9"      INITIAL 0
    FIELD percnt-lodg-to    AS DECIMAL FORMAT ">>9.9"           INITIAL 0
    FIELD lodg-ytd          AS DECIMAL FORMAT ">,>>>,>>>,>>9"   INITIAL 0
    FIELD budget-lodg-ytd   AS DECIMAL FORMAT ">,>>>,>>>,>>9"   INITIAL 0
    FIELD percnt-lodg-ytd   AS DECIMAL FORMAT ">>9.9"           INITIAL 0
    FIELD rmnite            AS DECIMAL FORMAT ">,>>9"           INITIAL 0
    FIELD budget-rmnite     AS DECIMAL FORMAT ">,>>9"           INITIAL 0
    FIELD percnt-rmnite     AS DECIMAL FORMAT ">>9.9"           INITIAL 0
    FIELD rmnite-ytd        AS DECIMAL FORMAT ">>>,>>9"         INITIAL 0
    FIELD budget-rmnite-ytd AS DECIMAL FORMAT ">>>,>>9"         INITIAL 0
    FIELD percnt-rmnite-ytd AS DECIMAL FORMAT ">>9.9"           INITIAL 0
    .  

DEFINE TEMP-TABLE gfb-turnover
    FIELD cust-name     AS CHARACTER FORMAT "x(24)"
    FIELD t-o           AS DECIMAL FORMAT ">>,>>>,>>9"    INITIAL 0
    FIELD fb-to         AS DECIMAL FORMAT ">>,>>>,>>9"    INITIAL 0
    FIELD budget-fb-to  AS DECIMAL FORMAT ">>,>>>,>>9"    INITIAL 0
    FIELD percnt-fb-to  AS DECIMAL FORMAT ">>9.9"         INITIAL 0
    FIELD fb-ytd        AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0
    FIELD budget-fb-ytd AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0
    FIELD percnt-fb-ytd AS DECIMAL FORMAT ">>9.9"         INITIAL 0
    .

DEFINE TEMP-TABLE gother-turnover
    FIELD cust-name        AS CHARACTER FORMAT "x(24)"
    FIELD t-o              AS DECIMAL FORMAT ">>,>>>,>>9"    INITIAL 0
    FIELD other-to         AS DECIMAL FORMAT ">>,>>>,>>9"    INITIAL 0  
    FIELD budget-other-to  AS DECIMAL FORMAT ">>,>>>,>>9"    INITIAL 0  
    FIELD percnt-other-to  AS DECIMAL FORMAT ">>9.9"         INITIAL 0  
    FIELD other-ytd        AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0  
    FIELD budget-other-ytd AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0  
    FIELD percnt-other-ytd AS DECIMAL FORMAT ">>9.9"         INITIAL 0  
    .

DEFINE WORKFILE to-list 
  FIELD gastnr     AS INTEGER 
  FIELD name       AS CHAR FORMAT "x(24)" 
  FIELD flag       AS LOGICAL EXTENT 12 INITIAL YES 
 
  FIELD gesamt     AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD b-gesamt   AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
  FIELD ygesamt    AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD b-ygesamt  AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
 
  FIELD logis      AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD b-logis    AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD proz3      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
  FIELD ylogis     AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD b-ylogis   AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD proz4      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
 
  FIELD fb         AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD b-fb       AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD proz5      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
  FIELD yfb        AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD b-yfb      AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD proz6      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
 
  FIELD sonst      AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD b-sonst    AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0 
  FIELD proz7      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
  FIELD ysonst     AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD b-ysonst   AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0 
  FIELD proz8      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
 
  FIELD room       AS DECIMAL FORMAT ">,>>9" INITIAL 0 
  FIELD b-room     AS DECIMAL FORMAT ">,>>9" INITIAL 0 
  FIELD proz9      AS DECIMAL FORMAT ">>9.9" INITIAL 0 
  FIELD yroom      AS DECIMAL FORMAT ">>>,>>9" INITIAL 0 
  FIELD b-yroom    AS DECIMAL FORMAT ">>>,>>9" INITIAL 0 
  FIELD proz10     AS DECIMAL FORMAT ">>9.9" INITIAL 0.

DEFINE INPUT PARAMETER from-date   AS CHAR.
DEFINE INPUT PARAMETER cardtype    AS INT.
DEFINE INPUT PARAMETER hide-zero   AS LOGICAL.
DEFINE INPUT PARAMETER disptype    AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR glodging-turnover.
DEFINE OUTPUT PARAMETER TABLE FOR gfb-turnover.
DEFINE OUTPUT PARAMETER TABLE FOR gother-turnover.

RUN create-umsatz.

PROCEDURE create-umsatz: 

  DEFINE VARIABLE mm AS INTEGER. 
  DEFINE VARIABLE yy AS INTEGER. 
  FOR EACH glodging-turnover: 
    delete glodging-turnover. 
  END. 
  FOR EACH gfb-turnover: 
    delete gfb-turnover. 
  END. 
  FOR EACH gother-turnover: 
    delete gother-turnover. 
  END. 
  FOR EACH to-list: 
    delete to-list. 
  END. 
 
  mm = INTEGER(SUBSTR(from-date,1,2)). 
  yy = INTEGER(SUBSTR(from-date,3,4)). 
 
  FOR EACH guestat WHERE guestat.jahr = yy AND guestat.monat LE mm 
    AND guestat.betriebsnr = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = guestat.gastnr 
      AND guest.karteityp = cardtype NO-LOCK BY guest.name: 
    FIND FIRST guestbud WHERE guestbud.gastnr = guestat.gastnr 
      AND guestbud.monat = guestat.monat AND guestbud.jahr = guestat.jahr 
      NO-LOCK NO-ERROR. 
    FIND FIRST to-list WHERE to-list.gastnr = guest.gastnr NO-ERROR. 
    IF NOT AVAILABLE to-list THEN 
    DO: 
      create to-list. 
      to-list.gastnr = guest.gastnr. 
      to-list.name = guest.name + ", " + guest.vorname1 + " " 
        + guest.anrede1 + guest.anredefirma. 
    END. 
    to-list.ygesamt = to-list.ygesamt + guestat.gesamtumsatz. 
    to-list.ylogis  = to-list.ylogis + guestat.argtumsatz. 
    to-list.yfb     = to-list.yfb + guestat.f-b-umsatz. 
    to-list.ysonst  = to-list.ysonst + guestat.sonst-umsatz. 
    to-list.yroom   = to-list.yroom + guestat.room-nights. 
    IF guestat.monat = mm THEN 
    DO: 
      to-list.gesamt = to-list.gesamt + guestat.gesamtumsatz. 
      to-list.logis  = to-list.logis + guestat.argtumsatz. 
      to-list.fb     = to-list.fb + guestat.f-b-umsatz. 
      to-list.sonst  = to-list.sonst + guestat.sonst-umsatz. 
      to-list.room   = to-list.room + guestat.room-nights. 
    END. 
 
    IF AVAILABLE guestbud AND to-list.flag[guestbud.monat] THEN 
    DO: 
      to-list.flag[guestbud.monat] = NO. 
      to-list.b-ygesamt  = to-list.b-ygesamt + guestbud.gesamtumsatz. 
      to-list.b-ylogis  = to-list.b-ylogis + guestbud.argtumsatz. 
      to-list.b-yfb     = to-list.b-yfb + guestbud.f-b-umsatz. 
      to-list.b-ysonst  = to-list.b-ysonst + guestbud.sonst-umsatz. 
      to-list.b-yroom   = to-list.b-yroom + guestbud.room-nights. 
      IF guestbud.monat = mm THEN 
      DO: 
        to-list.flag[guestbud.monat] = NO. 
        to-list.b-gesamt  = guestbud.gesamtumsatz. 
        to-list.b-logis  = guestbud.argtumsatz. 
        to-list.b-fb     = guestbud.f-b-umsatz. 
        to-list.b-sonst  = guestbud.sonst-umsatz. 
        to-list.b-room   = guestbud.room-nights. 
      END. 
    END. 
  END. 
 
  FOR EACH to-list: 
    IF to-list.b-gesamt NE 0 THEN 
      to-list.proz1 = to-list.gesamt / to-list.b-gesamt * 100. 
    IF to-list.b-ygesamt NE 0 THEN 
      to-list.proz2 = to-list.ygesamt / to-list.b-ygesamt * 100. 
    IF to-list.b-logis NE 0 THEN 
      to-list.proz3 = to-list.logis / to-list.b-logis * 100. 
    IF to-list.b-ylogis NE 0 THEN 
      to-list.proz4 = to-list.ylogis / to-list.b-ylogis * 100. 
    IF to-list.b-fb NE 0 THEN 
      to-list.proz5 = to-list.fb / to-list.b-fb * 100. 
    IF to-list.b-yfb NE 0 THEN 
      to-list.proz6 = to-list.yfb / to-list.b-yfb * 100. 
    IF to-list.b-sonst NE 0 THEN 
      to-list.proz7 = to-list.sonst / to-list.b-sonst * 100. 
    IF to-list.b-ysonst NE 0 THEN 
      to-list.proz8 = to-list.ysonst / to-list.b-ysonst * 100. 
    IF to-list.b-room NE 0 THEN 
      to-list.proz9 = to-list.room / to-list.b-room * 100. 
    IF to-list.b-yroom NE 0 THEN 
      to-list.proz10 = to-list.yroom / to-list.b-yroom * 100. 
  END. 

  IF hide-zero = YES THEN
  DO:
      FOR EACH to-list WHERE to-list.gesamt NE 0 NO-LOCK: 
          IF disptype = 1 THEN 
          DO: 
            CREATE glodging-turnover.
            ASSIGN                                
              glodging-turnover.cust-name         = to-list.NAME
              glodging-turnover.t-o               = to-list.gesamt
              glodging-turnover.budget-to         = to-list.b-gesamt
              glodging-turnover.percnt-to         = to-list.proz1
              glodging-turnover.ytd               = to-list.ygesamt 
              glodging-turnover.budget-ytd        = to-list.b-ygesamt
              glodging-turnover.percnt-ytd        = to-list.proz2
              glodging-turnover.lodg-to           = to-list.logis
              glodging-turnover.budget-lodg-to    = to-list.b-logis 
              glodging-turnover.percnt-lodg-to    = to-list.proz3
              glodging-turnover.lodg-ytd          = to-list.ylogis
              glodging-turnover.budget-lodg-ytd   = to-list.b-ylogis
              glodging-turnover.percnt-lodg-ytd   = to-list.proz4
              glodging-turnover.rmnite            = to-list.room
              glodging-turnover.budget-rmnite     = to-list.b-room
              glodging-turnover.percnt-rmnite     = to-list.proz9
              glodging-turnover.rmnite-ytd        = to-list.yroom
              glodging-turnover.budget-rmnite-ytd = to-list.b-yroom 
              glodging-turnover.percnt-rmnite-ytd = to-list.proz10
              .          
          END. 
          ELSE IF disptype = 2 THEN 
          DO: 
            CREATE gfb-turnover.
            ASSIGN
              gfb-turnover.cust-name      = to-list.NAME
              gfb-turnover.t-o            = to-list.gesamt
              gfb-turnover.fb-to          = to-list.fb
              gfb-turnover.budget-fb-to   = to-list.b-fb
              gfb-turnover.percnt-fb-to   = to-list.proz5
              gfb-turnover.fb-ytd         = to-list.yfb 
              gfb-turnover.budget-fb-ytd  = to-list.b-fb
              gfb-turnover.percnt-fb-ytd  = to-list.proz6
              .            
          END.
          ELSE IF disptype = 3 THEN 
          DO: 
            CREATE gother-turnover.
            ASSIGN
              gother-turnover.cust-name         = to-list.NAME
              gother-turnover.t-o               = to-list.gesamt
              gother-turnover.other-to          = to-list.sonst
              gother-turnover.budget-other-to   = to-list.b-sonst
              gother-turnover.percnt-other-to   = to-list.proz7
              gother-turnover.other-ytd         = to-list.ysonst
              gother-turnover.budget-other-ytd  = to-list.b-sonst
              gother-turnover.percnt-other-ytd  = to-list.proz8
              .            
          END. 
      END. 
  END.
  ELSE
  DO:
    FOR EACH to-list NO-LOCK: 
        IF disptype = 1 THEN 
        DO: 
          CREATE glodging-turnover.
          ASSIGN                                
            glodging-turnover.cust-name         = to-list.NAME
            glodging-turnover.t-o               = to-list.gesamt
            glodging-turnover.budget-to         = to-list.b-gesamt
            glodging-turnover.percnt-to         = to-list.proz1
            glodging-turnover.ytd               = to-list.ygesamt 
            glodging-turnover.budget-ytd        = to-list.b-ygesamt
            glodging-turnover.percnt-ytd        = to-list.proz2
            glodging-turnover.lodg-to           = to-list.logis
            glodging-turnover.budget-lodg-to    = to-list.b-logis 
            glodging-turnover.percnt-lodg-to    = to-list.proz3
            glodging-turnover.lodg-ytd          = to-list.ylogis
            glodging-turnover.budget-lodg-ytd   = to-list.b-ylogis
            glodging-turnover.percnt-lodg-ytd   = to-list.proz4
            glodging-turnover.rmnite            = to-list.room
            glodging-turnover.budget-rmnite     = to-list.b-room
            glodging-turnover.percnt-rmnite     = to-list.proz9
            glodging-turnover.rmnite-ytd        = to-list.yroom
            glodging-turnover.budget-rmnite-ytd = to-list.b-yroom 
            glodging-turnover.percnt-rmnite-ytd = to-list.proz10
            . 
        END. 
        ELSE IF disptype = 2 THEN 
        DO: 
          CREATE gfb-turnover.
          ASSIGN
            gfb-turnover.cust-name      = to-list.NAME
            gfb-turnover.t-o            = to-list.gesamt
            gfb-turnover.fb-to          = to-list.fb
            gfb-turnover.budget-fb-to   = to-list.b-fb
            gfb-turnover.percnt-fb-to   = to-list.proz5
            gfb-turnover.fb-ytd         = to-list.yfb 
            gfb-turnover.budget-fb-ytd  = to-list.b-fb
            gfb-turnover.percnt-fb-ytd  = to-list.proz6
            .
        END.
        ELSE IF disptype = 3 THEN 
        DO: 
          CREATE gother-turnover.
          ASSIGN
            gother-turnover.cust-name         = to-list.NAME
            gother-turnover.t-o               = to-list.gesamt
            gother-turnover.other-to          = to-list.sonst  
            gother-turnover.budget-other-to   = to-list.b-sonst
            gother-turnover.percnt-other-to   = to-list.proz7  
            gother-turnover.other-ytd         = to-list.ysonst 
            gother-turnover.budget-other-ytd  = to-list.b-sonst
            gother-turnover.percnt-other-ytd  = to-list.proz8  
            . 
        END. 
     END. 
  END.
END.
