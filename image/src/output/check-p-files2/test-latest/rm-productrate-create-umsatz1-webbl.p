
DEFINE TEMP-TABLE to-list 
  FIELD flag       AS INTEGER
  FIELD counter    AS INTEGER
  FIELD gastnr     AS INTEGER 
  FIELD name       AS CHAR FORMAT "x(24)" 
 
  FIELD room       AS INTEGER FORMAT "->>,>>9" INITIAL 0 
  FIELD c-room     AS INTEGER                  INITIAL 0
  FIELD pax        AS INTEGER FORMAT "->>,>>9" INITIAL 0 
  FIELD logis      AS DECIMAL FORMAT /*">>>,>>>,>>9"*/ "->>,>>>,>>>,>>9" INITIAL 0 
  FIELD proz       AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD avrgrate   AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0 
  FIELD ratecode   AS CHAR    FORMAT "x(15)"
  /*FIELD ratename   AS CHAR    FORMAT "x(15)"*/
 
  FIELD m-room     AS INTEGER FORMAT "->>,>>9" INITIAL 0 
  FIELD mc-room    AS INTEGER                  INITIAL 0
  FIELD m-pax      AS INTEGER FORMAT "->>,>>9" INITIAL 0 
  FIELD m-logis    AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 
  FIELD m-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD m-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0 
 
  FIELD y-room     AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
  FIELD yc-room    AS INTEGER                   INITIAL 0
  FIELD y-pax      AS INTEGER FORMAT "->>>,>>9" INITIAL 0 
  FIELD y-logis    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0 
  FIELD y-proz     AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD y-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0. 

DEF INPUT PARAMETER disptype AS INT.
DEF INPUT PARAMETER mi-ftd AS LOGICAL.
DEF INPUT PARAMETER f-date AS DATE.
DEF INPUT PARAMETER t-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER cardtype AS INT.
DEF INPUT PARAMETER incl-comp AS LOGICAL.
DEF INPUT PARAMETER sales-ID AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR to-list.

/*
DEF VAR disptype AS INT INIT 0.
DEF VAR mi-ftd AS LOGICAL INIT TRUE.
DEF VAR f-date AS DATE INIT 12/01/18.
DEF VAR t-date AS DATE INIT 12/31/18.
DEF VAR to-date AS DATE.
DEF VAR cardtype AS INT INIT 1.
DEF VAR incl-comp AS LOGICAL INIT FALSE.
DEF VAR sales-ID AS CHAR.
*/
DEFINE VARIABLE ind AS INTEGER. 
DEFINE VARIABLE price-decimal AS INTEGER. 

DEFINE VARIABLE st-room  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stc-room AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE st-pax   AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE st-logis AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE st-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE st-proz  AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEFINE VARIABLE stm-room  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stmc-room  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-pax   AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-logis AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE stm-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9".
DEFINE VARIABLE stm-proz  AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE sty-room  AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE styc-room  AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-pax   AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-logis AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE sty-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE sty-proz  AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEFINE VARIABLE room  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE c-room AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE pax   AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE logis AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE rmrate AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
dEFINE VARIABLE proz  AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE m-room  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE mc-room  AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-pax   AS INTEGER FORMAT "->>,>>9" INITIAL 0. 
DEFINE VARIABLE m-logis AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE m-rmrate AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE m-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE m-proz  AS DECIMAL FORMAT "->>9.99" INITIAL 0 .
 
DEFINE VARIABLE y-room  AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE yc-room  AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-pax   AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-logis AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-rmrate AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-avrgrate AS DECIMAL FORMAT "->,>>>,>>>,>>9". 
DEFINE VARIABLE y-proz  AS DECIMAL FORMAT "->>9.99" INITIAL 0 .

DEFINE VARIABLE i AS INTEGER INIT 0.
DEFINE VARIABLE exist-rate AS LOGICAL.

IF sales-ID EQ ? OR sales-ID EQ " " THEN sales-ID = "".

RUN create-umsatz1.

PROCEDURE create-umsatz1: 
DEFINE VARIABLE mm          AS INTEGER. 
DEFINE VARIABLE yy          AS INTEGER. 
DEFINE VARIABLE from-date   AS DATE. 
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE do-it       AS LOGICAL. 

DEF VAR s                   AS CHAR.
DEF VAR curr-code           AS CHAR.
DEF VAR curr-userID         AS CHAR.

  ASSIGN
    room    = 0     
    c-room  = 0 
    pax     = 0 
    logis   = 0
    proz    = 0

    m-room  = 0 
    mc-room = 0 
    m-pax   = 0 
    m-logis = 0
    m-proz  = 0
  
    y-room  = 0 
    yc-room = 0 
    y-pax   = 0 
    y-logis = 0
    y-proz  = 0
  . 
 
  IF mi-ftd THEN 
  DO: 
    from-date = f-date. 
    to-date = t-date. 
    mm = MONTH(to-date). 
    yy = YEAR(to-date). 
  END. 
  ELSE 
  DO: 
    mm = MONTH(to-date). 
    yy = YEAR(to-date). 
    from-date = DATE(1,1,yy). 
  END. 
 
  FOR EACH to-list: 
    DELETE to-list. 
  END. 

  FOR EACH genstat WHERE genstat.datum GE from-date 
      AND genstat.datum LE to-date 
      AND genstat.zinr NE "" 
      AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */ 
      USE-INDEX date_ix NO-LOCK, 
      FIRST guest WHERE guest.gastnr = genstat.gastnr 
      NO-LOCK /*BY guest.name BY guest.gastnr*/: 
      
      PROCESS EVENTS.
      
      IF genstat.res-char[2] MATCHES("*$CODE$*") THEN
      DO:
          s = SUBSTR(genstat.res-char[2],(INDEX(genstat.res-char[2],"$CODE$") + 6)).                    /* Rulita 140225 | Fixing serverless from res-char to genstat.res-char[2] issue git 602 */
          curr-code = TRIM(ENTRY(1, s, ";")).
      END.
      /*Alder - Ticket ECA513 - Start*/
      ELSE DO:
          FIND FIRST res-line WHERE res-line.resnr EQ genstat.resnr AND res-line.reslinnr EQ genstat.res-int[1] NO-LOCK NO-ERROR.
          IF AVAILABLE res-line THEN
          DO:
              s = SUBSTR(res-line.zimmer-wunsch,(INDEX(res-line.zimmer-wunsch,"$CODE$") + 6)).          /* Rulita 140225 | Fixing serverless from zimmer-wunsch to res-line.zimmer-wunsch] issue git 602 */
              curr-code = TRIM(ENTRY(1, s, ";")).
          END.
          ELSE curr-code = "UNKNOWN".
      END.
      /*Alder - Ticket ECA513 - End*/
      datum = genstat.datum.

      do-it = YES.
      IF cardtype LT 3 THEN do-it = guest.karteityp = cardtype.
      IF NOT incl-comp AND genstat.zipreis = 0 THEN
      DO:
        IF (genstat.gratis GT 0) THEN do-it = NO.
        IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
           AND genstat.resstatus NE 13 THEN do-it = NO.
      END.

      IF do-it AND sales-ID NE "" THEN
      do-it = guest.phonetik3 = TRIM(ENTRY(1, sales-ID, "-")).

      /*FDL Oct 29, 2024: Ticket A526DC*/      
      IF curr-code NE "UNKNOWN" THEN
      DO:          
        exist-rate = NO.
        /*FOR EACH ratecode WHERE ratecode.code EQ curr-code 
            AND ratecode.endperiode GT to-date NO-LOCK:
            exist-rate = YES.
            LEAVE.
        END.*/
        FIND FIRST ratecode WHERE ratecode.CODE EQ curr-code AND ratecode.endperiode GT to-date NO-LOCK NO-ERROR.
        IF AVAILABLE ratecode THEN exist-rate = YES.
        IF NOT exist-rate THEN do-it = NO.
    END.        

      IF do-it THEN
      DO:
          IF genstat.zipreis = 0 THEN
          DO:
            IF (genstat.gratis GT 0) 
                OR ((genstat.erwachs + genstat.kind1 + genstat.kind2 
                + genstat.gratis = 0) AND genstat.resstatus NE 13) THEN 
            DO:
              IF genstat.datum = to-date THEN c-room = c-room + 1.
              IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
               mc-room = mc-room + 1.
              yc-room = yc-room + 1.
            END.
          END.
          FIND FIRST to-list WHERE to-list.gastnr = genstat.gastnr
             AND to-list.ratecode = curr-code NO-LOCK NO-ERROR.
          IF NOT AVAILABLE to-list THEN
          DO:
            CREATE to-list.
            ASSIGN
                to-list.ratecode = curr-code
                to-list.gastnr = guest.gastnr
                to-list.name = guest.name + ", " + guest.vorname1 + " " 
                  + guest.anrede1 + guest.anredefirma
            . 
          END.
          IF genstat.datum = to-date THEN
          DO:
              IF genstat.resstatus NE 13 THEN 
                  ASSIGN
                  to-list.room = to-list.room + 1
                  room             = room  + 1.
              IF genstat.gratis GT 0 THEN
                  ASSIGN
                      to-list.pax      = to-list.pax   + genstat.gratis
                      pax              = pax   + genstat.gratis
                      avrgrate         = avrgrate + genstat.rateLocal.
              ELSE
                  ASSIGN
                      to-list.pax      = to-list.pax   + genstat.erwachs
                                       /*MT 280512*/
                                       + genstat.kind1 + genstat.kind2
                      pax              = pax   + genstat.erwachs
                                       /*MT 280512*/
                                       + genstat.kind1 + genstat.kind2
                      avrgrate         = avrgrate + genstat.rateLocal.

              IF disptype = 0 THEN
                  ASSIGN
                    to-list.logis    = to-list.logis + genstat.logis
                    logis            = logis + genstat.logis.
              ELSE
                  ASSIGN
                  to-list.logis    = to-list.logis + genstat.rateLocal
                  logis            = logis + genstat.rateLocal.

          END.

          /*DISP genstat.datum genstat.resstatus to-list.m-room guest.phonetik3.*/
          IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
          DO:
              IF genstat.resstatus NE 13 THEN 
                  ASSIGN
                  to-list.m-room = to-list.m-room + 1
                  m-room         = m-room + 1.

              IF genstat.gratis GT 0 THEN 
                  ASSIGN
                      to-list.m-pax      = to-list.m-pax + genstat.gratis
                      m-pax              = m-pax   + genstat.gratis
                      m-avrgrate         = m-avrgrate + genstat.rateLocal.             
              ELSE 
                  ASSIGN
                      to-list.m-pax      = to-list.m-pax   + genstat.erwachs
                                         /*MT 280512*/
                                         + genstat.kind1 + genstat.kind2
                      m-pax              = m-pax   + genstat.erwachs
                                         /*MT 280512*/
                                         + genstat.kind1 + genstat.kind2
                      m-avrgrate         = m-avrgrate + genstat.rateLocal.

              IF disptype = 0 THEN
                  ASSIGN
                  to-list.m-logis    = to-list.m-logis + genstat.logis
                  m-logis            = m-logis + genstat.logis.
              ELSE
                  ASSIGN
                  to-list.m-logis    = to-list.m-logis + genstat.rateLocal
                  m-logis            = m-logis + genstat.rateLocal.
          END.
          IF genstat.resstatus NE 13 THEN 
              ASSIGN 
                to-list.y-room = to-list.y-room + 1
                y-room             = y-room  + 1.

          IF genstat.gratis GT 0 THEN
              ASSIGN
                  to-list.y-pax      = to-list.y-pax   + genstat.gratis
                  y-pax              = y-pax   + genstat.gratis
                  y-avrgrate         = y-avrgrate + genstat.rateLocal.
          ELSE
              ASSIGN
                  to-list.y-pax      = to-list.y-pax   + genstat.erwachs 
                                     /*MT 280512*/
                                     + genstat.kind1 + genstat.kind2
                  y-pax              = y-pax   + genstat.erwachs 
                                     /*MT 280512*/
                                     + genstat.kind1 + genstat.kind2
                  y-avrgrate         = y-avrgrate + genstat.rateLocal.

          IF disptype = 0 THEN
              ASSIGN
              to-list.y-logis    = to-list.y-logis + genstat.logis
              y-logis            = y-logis + genstat.logis.
          ELSE
              ASSIGN
                  to-list.y-logis    = to-list.y-logis + genstat.rateLocal
                  y-logis            = y-logis + genstat.rateLocal.
          IF genstat.zipreis = 0 AND
            (genstat.gratis GT 0 OR (genstat.erwachs + genstat.kind1
            + genstat.kind2 + genstat.gratis = 0) 
             AND genstat.resstatus NE 13) THEN /*M 250512 -> fix read as room sharer */
          DO:
            IF genstat.datum = to-date THEN 
              to-list.c-room = to-list.c-room + 1.
            IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN 
               to-list.mc-room = to-list.mc-room + 1.
            to-list.yc-room = to-list.yc-room + 1.
          END.
      
      END.
  END.
                
  FOR EACH to-list:   
    
    IF (to-list.room - to-list.c-room) NE 0 THEN 
      to-list.avrgrate = to-list.logis / (to-list.room - to-list.c-room). 
    IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
      to-list.m-avrgrate = to-list.m-logis / (to-list.m-room - to-list.mc-room). 
    IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
      to-list.y-avrgrate = to-list.y-logis / (to-list.y-room - to-list.yc-room). 
    IF logis NE 0 THEN 
      to-list.proz = to-list.logis / logis * 100. 
    IF m-logis NE 0 THEN 
      to-list.m-proz = to-list.m-logis / m-logis * 100. 
    IF y-logis NE 0 THEN 
      to-list.y-proz = to-list.y-logis / y-logis * 100. 
  END.

  RUN create-output.

  i = i + 1.
  CREATE to-list.
  ASSIGN to-list.counter = i.

  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room). 

  i = i + 1.
  CREATE to-list.
  ASSIGN 
    to-list.counter = i
    to-list.flag = 1
    to-list.NAME = "T O T A L"
    to-list.room = room
    to-list.pax = pax
    to-list.logis = logis
    to-list.proz = proz
    to-list.avrgrate = avrgrate
    to-list.m-room = m-room
    to-list.m-pax = m-pax
    to-list.m-logis = m-logis
    to-list.m-proz = m-proz
    to-list.m-avrgrate = m-avrgrate
    to-list.y-room = y-room
    to-list.y-pax = y-pax
    to-list.y-logis = y-logis
    to-list.y-proz = y-proz
    to-list.y-avrgrate = y-avrgrate.
END. 



PROCEDURE create-output:       
    DEFINE VARIABLE curr-code AS CHARACTER.
    DEFINE BUFFER buff-list FOR to-list.
    DO:
      /* FOR EACH to-list NO-LOCK BY to-list.ratecode BY to-list.NAME: */
      FOR EACH to-list WHERE to-list.ratecode NE "" NO-LOCK BY to-list.ratecode BY to-list.NAME:
          FIND FIRST queasy WHERE queasy.KEY EQ 2 AND queasy.char1 EQ to-list.ratecode NO-LOCK NO-ERROR.
        IF to-list.ratecode NE curr-code AND curr-code NE "" THEN
        DO:
            i = i + 1.
            CREATE buff-list.
            ASSIGN 
                buff-list.counter = i.
            i = i + 1.

            st-avrgrate = 0. 
            IF (st-room - stc-room) NE 0 THEN st-avrgrate = st-logis / (st-room - stc-room). 
            stm-avrgrate = 0. 
            IF (stm-room - stmc-room) NE 0 THEN stm-avrgrate = stm-logis / (stm-room - stmc-room). 
            sty-avrgrate = 0. 
            IF (sty-room - styc-room) NE 0 THEN sty-avrgrate = sty-logis / (sty-room - styc-room). 
            CREATE buff-list.
            ASSIGN
                buff-list.counter = i
                buff-list.flag = 1
                buff-list.NAME = "S u b T o t a l"
                buff-list.room = st-room
                buff-list.pax = st-pax
                buff-list.logis = st-logis
                buff-list.proz = st-proz
                buff-list.avrgrate = st-avrgrate
                buff-list.m-room = stm-room
                buff-list.m-pax = stm-pax
                buff-list.m-logis = stm-logis
                buff-list.m-proz = stm-proz
                buff-list.m-avrgrate = stm-avrgrate
                buff-list.y-room = sty-room
                buff-list.y-pax = sty-pax
                buff-list.y-logis = sty-logis
                buff-list.y-proz = sty-proz
                buff-list.y-avrgrate = sty-avrgrate.
            RUN init-val.
            i = i + 1.
            CREATE buff-list.
            ASSIGN 
                buff-list.counter = i.
        END.
        
        DO:
            IF curr-code = "" OR curr-code NE to-list.ratecode THEN
            DO:
                i = i + 1.
                CREATE buff-list.
                ASSIGN
                    buff-list.counter = i
                    buff-list.ratecode = to-list.ratecode.
                IF to-list.ratecode EQ "UNKNOWN" THEN
                    buff-list.NAME = "UNKNOWN".
                ELSE IF AVAILABLE queasy THEN 
                    buff-list.NAME = queasy.char2.
            END.

            curr-code = to-list.ratecode.
            
            IF curr-code = "" OR curr-code = to-list.ratecode THEN
            DO:
              ASSIGN
                i = i + 1
                to-list.counter = i
                to-list.ratecode = ""
                to-list.flag = 1
                proz = proz + to-list.proz
                m-proz = m-proz + to-list.m-proz
                y-proz = y-proz + to-list.y-proz
                st-room = st-room + to-list.room
                st-pax = st-pax  + to-list.pax
                st-proz = st-proz + to-list.proz
                st-logis = st-logis + to-list.logis
                st-avrgrate = st-avrgrate + to-list.avrgrate
                stm-room = stm-room + to-list.m-room        
                stm-pax = stm-pax  + to-list.m-pax
                stm-proz = stm-proz + to-list.m-proz
                stm-logis = stm-logis + to-list.m-logis
                stm-avrgrate = stm-avrgrate + to-list.m-avrgrate
                sty-room = sty-room + to-list.y-room        
                sty-pax = sty-pax  + to-list.y-pax
                sty-proz = sty-proz + to-list.y-proz
                sty-logis = sty-logis + to-list.y-logis
                sty-avrgrate = sty-avrgrate + to-list.y-avrgrate.
            END.
        END.
      END. 
    END.
END.

PROCEDURE init-val:
  st-room = 0.
  st-pax = 0.
  st-proz = 0.
  st-logis = 0.
  st-avrgrate = 0.
  stm-room = 0.        
  stm-pax = 0.
  stm-proz = 0.
  stm-logis = 0.
  stm-avrgrate = 0.
  sty-room = 0.   
  sty-pax = 0.
  sty-proz = 0.
  sty-logis = 0.
  sty-avrgrate = 0.
END.
