DEFINE TEMP-TABLE to-list 
  FIELD gastnr     AS INTEGER 
  FIELD name       AS CHAR FORMAT "x(24)" 
 
  FIELD room       AS INTEGER FORMAT "->>,>>9" INITIAL 0 
  FIELD c-room     AS INTEGER                  INITIAL 0
  FIELD pax        AS INTEGER FORMAT "->>,>>9" INITIAL 0 
  FIELD logis      AS DECIMAL FORMAT /*">>>,>>>,>>9"*/ "->>,>>>,>>>,>>9" INITIAL 0 
  FIELD proz       AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD avrgrate   AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0 
  FIELD ratecode   AS CHAR    FORMAT "x(15)"
 
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
  FIELD y-avrgrate AS DECIMAL FORMAT /*">,>>>,>>9"*/ "->,>>>,>>>,>>9" INITIAL 0
  FIELD revenue    AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0 

  FIELD bfast       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0
  FIELD lunch       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0
  FIELD dinner      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0.

DEFINE TEMP-TABLE output-list2 
  FIELD flag    AS INTEGER 
  FIELD name    AS CHAR 
  FIELD rmnite1 AS INTEGER  /*MTD*/ 
  FIELD rmrev1  AS DECIMAL 
  FIELD rmnite  AS INTEGER   /*YTD*/ 
  FIELD rmrev   AS DECIMAL 
  FIELD str2    AS CHAR
  FIELD rate    AS CHAR.

DEF INPUT PARAMETER disptype    AS INT.
DEF INPUT PARAMETER mi-ftd      AS LOGICAL.
DEF INPUT PARAMETER mi-cust     AS LOGICAL.
DEF INPUT PARAMETER f-date      AS DATE.
DEF INPUT PARAMETER t-date      AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER cardtype    AS INT.
DEF INPUT PARAMETER incl-comp   AS LOGICAL.
DEF INPUT PARAMETER sales-ID    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR output-list2.
DEF OUTPUT PARAMETER TABLE FOR to-list.

DEFINE VARIABLE ind AS INTEGER. 
DEFINE VARIABLE price-decimal AS INTEGER. 
DEFINE VARIABLE othRev       AS DECIMAL.

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
DEFINE VARIABLE sty-revenue AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0.   /*william 99B536*/

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
DEFINE VARIABLE revenue AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9" INITIAL 0.     /*william 99B536*/

DEFINE VARIABLE bfast       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0.
DEFINE VARIABLE lunch       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0.
DEFINE VARIABLE dinner      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0.

RUN create-umsatz1.

PROCEDURE create-umsatz1: 
DEFINE VARIABLE mm          AS INTEGER. 
DEFINE VARIABLE yy          AS INTEGER. 
DEFINE VARIABLE from-date   AS DATE. 
DEFINE VARIABLE datum       AS DATE.
DEFINE VARIABLE tdatum     AS DATE NO-UNDO.     /*william 99B536*/
DEFINE VARIABLE do-dat     AS LOGICAL.          /*william 99B536*/
DEFINE VARIABLE do-it       AS LOGICAL. 
DEFINE VARIABLE do-cust     AS LOGICAL.     /*WN*/ 
DEFINE VARIABLE i           AS INTEGER INITIAL 0.
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
    revenue = 0       /*william 99B536*/
  .
   /*/*wn*/
    bfast   = 0
    lunch   = 0
    dinner  = 0
    . */ 
 
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
  IF mi-cust THEN
  DO:
      from-date = f-date. 
      to-date = t-date. 
      mm = MONTH(to-date). 
      yy = YEAR(to-date). 
  END.
 
  FOR EACH output-list2: 
    DELETE output-list2. 
  END. 
  FOR EACH to-list: 
    DELETE to-list. 
  END. 

  FOR EACH genstat WHERE genstat.datum GE from-date 
      AND genstat.datum LE to-date 
      AND genstat.zinr NE "" 
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ 
      USE-INDEX date_ix NO-LOCK, 
      FIRST guest WHERE guest.gastnr = genstat.gastnr 
      NO-LOCK /*BY guest.name BY guest.gastnr*/:

      PROCESS EVENTS.
      
      IF genstat.datum NE tdatum THEN     /*william do other logic*/
      DO:
          tdatum = genstat.datum.
          do-dat = YES.
      END.
      ELSE do-dat = NO.
   
      IF genstat.res-char[2] MATCHES("*$CODE$*") THEN
      DO:
          s = SUBSTR(genstat.res-char[2],(INDEX(res-char[2],"$CODE$") + 6)).
          curr-code = TRIM(ENTRY(1, s, ";")).
      END.
      /*Alder - Ticket ECA513 - Start*/
      ELSE DO:
          FIND FIRST res-line WHERE res-line.resnr EQ genstat.resnr AND res-line.reslinnr EQ genstat.res-int[1] NO-LOCK NO-ERROR.
          IF AVAILABLE res-line THEN
          DO:
              s = SUBSTR(zimmer-wunsch,(INDEX(zimmer-wunsch,"$CODE$") + 6)).
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

      /*Bily - Ticket 67DF21*/
      IF do-it AND sales-ID NE "ALL" THEN
      do-it = guest.phonetik3 = TRIM(ENTRY(1, sales-ID, "-")).

/*       MESSAGE sales-ID                       */
/*           VIEW-AS ALERT-BOX INFO BUTTONS OK. */

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
                to-list.y-room     = to-list.y-room + 1
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
          DO:
              ASSIGN
                  to-list.y-logis    = to-list.y-logis + genstat.logis
                  y-logis            = y-logis + genstat.logis.
              to-list.revenue = to-list.revenue + genstat.logis.
              revenue = revenue + genstat.logis.
              IF do-dat THEN
              DO:
                  RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william 99B536*/
                  ASSIGN
                      to-list.revenue = to-list.revenue + othRev.
                      revenue = revenue + othRev.
              END.
          END.
          ELSE
          DO:
          
              ASSIGN
                  to-list.y-logis    = to-list.y-logis + genstat.rateLocal
                  y-logis            = y-logis + genstat.rateLocal.
              to-list.revenue = to-list.revenue + genstat.rateLocal.
              revenue = revenue + genstat.rateLocal.
              IF do-dat THEN
              DO:
                  RUN calc-othRev (genstat.datum, OUTPUT othRev).     /*william 99B536*/
                  ASSIGN
                      to-list.revenue = to-list.revenue + othRev.
                      revenue = revenue + othRev.
              END.
          END.
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

      /*
      /*wn*/
      do-cust = YES.
      IF cardtype LT 3 THEN do-cust = guest.karteityp = cardtype.
      IF NOT incl-comp AND genstat.zipreis = 0 THEN
      DO:
        IF (genstat.gratis GT 0) THEN do-cust = NO.
        IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
           AND genstat.resstatus NE 13 THEN do-cust = NO.
      END.

      IF do-cust AND sales-ID NE ? THEN
      do-cust = guest.phonetik3 = TRIM(ENTRY(1, sales-ID, "-")).

      IF do-cust THEN
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
                to-list.name     = guest.name + ", " + guest.vorname1 + " " 
                                   + guest.anrede1 + guest.anredefirma
                to-list.ratecode = curr-code
                to-list.gastnr   = guest.gastnr .
               
          END.
          
          IF genstat.datum = to-date THEN
          DO:
              IF genstat.resstatus NE 13 THEN 
                  ASSIGN
                  to-list.room     = to-list.room + 1
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
                to-list.y-room  = to-list.y-room + 1
                y-room          = y-room  + 1.

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
          ASSIGN
            to-list.bfast    =  genstat.res-deci[2]
            bfast            =  genstat.res-deci[2]
            to-list.lunch    =  genstat.res-deci[3]
            lunch            =  genstat.res-deci[3]
            to-list.dinner   =  genstat.res-deci[4]
            dinner           =  genstat.res-deci[4].
      END. /*end wn*/
      */  

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


  /*RUN INIT-val.*/
  CREATE output-list2. 
  output-list2.flag = 3. 
  DO ind = 1 TO 235: /*195*/
    output-list2.str2 = output-list2.str2 + "-". 
  END. 
  
  CREATE output-list2. 
  output-list2.flag = 4. 
  
  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room). 

  IF price-decimal = 0  THEN 
  DO:
output-list2.str2 = STRING("T o t a l", "x(24)") 
    + STRING(room, "->>,>>9") 
    + STRING(pax, "->>,>>9") 
    + STRING(logis, "->>,>>>,>>>,>>9") 
    + STRING(proz, "->>9.99") 
    + STRING(avrgrate, "->,>>>,>>>,>>9") 
    + STRING(m-room, "->>,>>9") 
    + STRING(m-pax, "->>,>>9") 
    + STRING(m-logis, "->>,>>>,>>>,>>9")
    + STRING(m-proz, "->>9.99") 
    + STRING(m-avrgrate, "->,>>>,>>>,>>9") 
    + STRING(y-room, "->>>,>>9") 
    + STRING(y-pax, "->>>,>>9") 
    + STRING(y-logis, "->,>>>,>>>,>>>,>>9") 
    + STRING(y-proz, "->>9.99") 
    + STRING(y-avrgrate, "->,>>>,>>>,>>9")
    + "                  "                      /*william*/
    + STRING(sty-logis, " ->,>>>,>>>,>>9.99")
    /*+ STRING(bfast, "->,>>>,>>>,>>9") 
    + STRING(lunch, "->,>>>,>>>,>>9")
    + STRING(dinner, "->,>>>,>>>,>>9")*/
    . 
    output-list2.rmrev = revenue. /*william 99B536*/
  END.
  
  ELSE 
  DO:
output-list2.str2 = STRING("T o t a l", "x(24)") 
    + STRING(room, "->>,>>9") 
    + STRING(pax, "->>,>>9") 
    + STRING(logis, " ->>,>>>,>>9.99") 
    + STRING(proz, "->>9.99") 
    + STRING(avrgrate,  "->>,>>>,>>9.99") 
    + STRING(m-room, "->>,>>9") 
    + STRING(m-pax, "->>,>>9") 
    + STRING(m-logis, " ->>,>>>,>>9.99") 
    + STRING(m-proz, "->>9.99") 
    + STRING(m-avrgrate,  "->>,>>>,>>9.99") 
    + STRING(y-room, "->>>,>>9") 
    + STRING(y-pax, "->>>,>>9") 
    + STRING(y-logis, " ->,>>>,>>>,>>9.99") 
    + STRING(y-proz, "->>9.99") 
    + STRING(y-avrgrate,  "->>,>>>,>>9.99")
    /*+ STRING(bfast, "->,>>>,>>>,>>9") 
    + STRING(lunch, "->,>>>,>>>,>>9")
    + STRING(dinner, "->,>>>,>>>,>>9")*/
    . 
    output-list2.rmrev = revenue. /*william 99B536*/
  END.
  
END. 



PROCEDURE create-output:       
    DEFINE BUFFER output-buff FOR output-list2.
    DEFINE VARIABLE i AS INTEGER INITIAL 0.
    DEFINE VARIABLE a AS INTEGER INITIAL 0.
    DEFINE VARIABLE ratecode-bez AS CHAR FORMAT "x(24)".
    DO:
      FOR EACH to-list NO-LOCK BY to-list.ratecode BY to-list.NAME: 
          FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 EQ TRIM(to-list.ratecode) NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN ratecode-bez = queasy.char2.
          ELSE ratecode-bez = "".
        i = i + 1.
        FIND FIRST output-buff WHERE output-buff.rate = to-list.ratecode NO-LOCK NO-ERROR.
        IF NOT AVAILABLE output-buff THEN
        DO:
            IF i NE 1 THEN
            DO: 
                RUN create-sub.
            END.
            create output-list2. 

            IF LENGTH(ratecode-bez) NE 24 THEN 
            DO:
                a = 179 - LENGTH(ratecode-bez).

                ratecode-bez = ratecode-bez + FILL(" ",a).
            END.

            IF price-decimal = 0  THEN 
            DO: 
                output-list2.str2 = ratecode-bez + STRING(to-list.ratecode,"x(18)").    /* "x(15)" Gerald 3645DD extend ratecode*/
                /*output-list2.str2 = fill(" ",179) + STRING(to-list.ratecode,"x(15)").*/
                CREATE output-list2.
                RUN count-sub1.
            END. 
            ELSE 
            DO: 
                output-list2.str2 = ratecode-bez + STRING(to-list.ratecode,"x(18)").    /* "x(15)" Gerald 3645DD extend ratecode*/
                /*output-list2.str2 = fill(" ",179) + STRING(to-list.ratecode,"x(15)").*/
                CREATE output-list2.
                RUN count-sub2.
            END. 
        END.
        ELSE
        DO:
            CREATE output-list2.
            IF price-decimal = 0  THEN 
                RUN count-sub1.
            ELSE
                RUN count-sub2.
        END.                        
      END. 
      RUN create-sub.
    END.
END.

PROCEDURE create-sub:
  create output-list2. 
  output-list2.flag = 1. 
  DO ind = 1 TO 235: /*195*/
    output-list2.str2 = output-list2.str2 + "-". 
  END. 
  create output-list2. 
  output-list2.flag = 2. 
  st-avrgrate = 0. 
  IF (st-room - stc-room) NE 0 THEN st-avrgrate = st-logis / (st-room - stc-room). 
  stm-avrgrate = 0. 
  IF (stm-room - stmc-room) NE 0 THEN stm-avrgrate = stm-logis / (stm-room - stmc-room). 
  sty-avrgrate = 0. 
  IF (sty-room - styc-room) NE 0 THEN sty-avrgrate = sty-logis / (sty-room - styc-room). 
 
  IF price-decimal = 0  THEN 
  DO:
 output-list2.str2 = STRING("S u b T o t a l", "x(24)") 
    + STRING(st-room, "->>,>>9") 
    + STRING(st-pax, "->>,>>9") 
    + STRING(st-logis, "->>,>>>,>>>,>>9") 
    + STRING(st-proz, "->>9.99") 
    + STRING(st-avrgrate, "->,>>>,>>>,>>9") 
    + STRING(stm-room, "->>,>>9") 
    + STRING(stm-pax, "->>,>>9") 
    + STRING(stm-logis, "->>,>>>,>>>,>>9")
    + STRING(stm-proz, "->>9.99") 
    + STRING(stm-avrgrate, "->,>>>,>>>,>>9") 
    + STRING(sty-room, "->>>,>>9") 
    + STRING(sty-pax, "->>>,>>9") 
    + STRING(sty-logis, "->,>>>,>>>,>>>,>>9") 
    + STRING(sty-proz, "->>9.99") 
    + STRING(sty-avrgrate, "->,>>>,>>>,>>9")
    /*+ STRING(bfast, "->,>>>,>>>,>>9") 
    + STRING(lunch, "->,>>>,>>>,>>9")
    + STRING(dinner, "->,>>>,>>>,>>9")*/
    .
      output-list2.rmrev = sty-revenue. /*william 99B536*/
  END.
   
  ELSE
  DO:
 output-list2.str2 = STRING("S u b T o t a l", "x(24)") 
    + STRING(st-room, "->>,>>9") 
    + STRING(st-pax, "->>,>>9") 
    + STRING(st-logis, " ->>,>>>,>>9.99") 
    + STRING(st-proz, "->>9.99") 
    + STRING(st-avrgrate,  "->>,>>>,>>9.99") 
    + STRING(stm-room, "->>,>>9") 
    + STRING(stm-pax, "->>,>>9") 
    + STRING(stm-logis, " ->>,>>>,>>9.99")
    + STRING(stm-proz, "->>9.99") 
    + STRING(stm-avrgrate,  "->>,>>>,>>9.99") 
    + STRING(sty-room, "->>>,>>9") 
    + STRING(sty-pax, "->>>,>>9") 
    + STRING(sty-logis, " ->,>>>,>>>,>>9.99") 
    + STRING(sty-proz, "->>9.99") 
    + STRING(sty-avrgrate,  "->>,>>>,>>9.99")
    /*+ STRING(bfast, "->,>>>,>>>,>>9") 
    + STRING(lunch, "->,>>>,>>>,>>9")
    + STRING(dinner, "->,>>>,>>>,>>9")*/
    .
    output-list2.rmrev = sty-revenue. /*william 99B536*/
  END.
 

  create output-list2. 
  output-list2.str2 = FILL (" ",30).
  RUN init-val.
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
  sty-revenue = 0.      /*william 99B536*/
 /* bfast = 0.
  lunch = 0.
  dinner = 0.*/
  
END.  

PROCEDURE count-sub2:
  output-list2.str2 = STRING(to-list.name, "x(24)") 
        + STRING(to-list.room, "->>,>>9") 
        + STRING(to-list.pax, "->>,>>9") 
        + STRING(to-list.logis, " ->>,>>>,>>9.99") 
        + STRING(to-list.proz, "->>9.99")      
        + STRING(to-list.avrgrate, "->>,>>>,>>9.99")  
        + STRING(to-list.m-room, "->>,>>9") 
        + STRING(to-list.m-pax, "->>,>>9") 
        + STRING(to-list.m-logis, " ->>,>>>,>>9.99")  
        + STRING(to-list.m-proz, "->>9.99")            
        + STRING(to-list.m-avrgrate, "->>,>>>,>>9.99")   
        + STRING(to-list.y-room, "->>>,>>9") 
        + STRING(to-list.y-pax, "->>>,>>9") 
        + STRING(to-list.y-logis, " ->,>>>,>>>,>>9.99")  
        + STRING(to-list.y-proz, "->>9.99")         
        + STRING(to-list.y-avrgrate, "->>,>>>,>>9.99")
        /*+ STRING(to-list.y-logis, " ->,>>>,>>>,>>9.99") */
        /*+ STRING(to-list.bfast, "->,>>>,>>>,>>9") 
        + STRING(to-list.lunch, "->,>>>,>>>,>>9")
        + STRING(to-list.dinner, "->,>>>,>>>,>>9")*/
      .
      output-list2.rate = to-list.ratecode.
      output-list2.name = STRING(to-list.name, "x(24)"). 
      output-list2.rmnite = to-list.y-room. 
      output-list2.rmrev = to-list.revenue.         /*william 99B536*/
      output-list2.rmnite1 = to-list.m-room. 
      output-list2.rmrev1 = to-list.m-logis. 
   proz = proz + to-list.proz.
   m-proz = m-proz + to-list.m-proz.
   y-proz = y-proz + to-list.y-proz.
   st-room = st-room + TO-list.room.
   st-pax = st-pax  + to-list.pax.
   st-proz = st-proz + to-list.proz.
   st-logis = st-logis + to-list.logis.
   st-avrgrate = st-avrgrate + to-list.avrgrate.
   stm-room = stm-room + to-list.m-room.        
   stm-pax = stm-pax  + to-list.m-pax.
   stm-proz = stm-proz + to-list.m-proz.
   stm-logis = stm-logis + to-list.m-logis.
   stm-avrgrate = stm-avrgrate + to-list.m-avrgrate.
   sty-room = sty-room + to-list.y-room.        
   sty-pax = sty-pax  + to-list.y-pax.
   sty-proz = sty-proz + to-list.y-proz.
   sty-logis = sty-logis + to-list.y-logis.
   sty-avrgrate = sty-avrgrate + to-list.y-avrgrate.
   sty-revenue = sty-revenue + to-list.revenue.       /*william 99B536*/
END.

PROCEDURE count-sub1:
   output-list2.str2 = STRING(to-list.name, "x(24)") 
        + STRING(to-list.room, "->>,>>9") 
        + STRING(to-list.pax, "->>,>>9") 
        + STRING(to-list.logis, "->>,>>>,>>>,>>9")   
        + STRING(to-list.proz, "->>9.99") 
        + STRING(to-list.avrgrate, "->,>>>,>>>,>>9") 
        + STRING(to-list.m-room, "->>,>>9") 
        + STRING(to-list.m-pax, "->>,>>9") 
        + STRING(to-list.m-logis, "->>,>>>,>>>,>>9") 
        + STRING(to-list.m-proz, "->>9.99") 
        + STRING(to-list.m-avrgrate, "->,>>>,>>>,>>9") 
        + STRING(to-list.y-room, "->>>,>>9") 
        + STRING(to-list.y-pax, "->>>,>>9") 
        + STRING(to-list.y-logis, "->,>>>,>>>,>>>,>>9") 
        + STRING(to-list.y-proz, "->>9.99") 
        + STRING(to-list.y-avrgrate, "->,>>>,>>>,>>9")
        /*+ STRING(to-list.y-logis, " ->,>>>,>>>,>>9.99")*/
        /*+ STRING(to-list.bfast, "->,>>>,>>>,>>9") 
        + STRING(to-list.lunch, "->,>>>,>>>,>>9")
        + STRING(to-list.dinner, "->,>>>,>>>,>>9")*/
      .
      output-list2.name = STRING(to-list.name, "x(24)"). 
      output-list2.rmnite = to-list.y-room. 
      output-list2.rmrev = to-list.revenue.         /*william 99B536*/
      output-list2.rmnite1 = to-list.m-room. 
      output-list2.rmrev1 = to-list.m-logis. 
      output-list2.rate = to-list.ratecode.
      proz = proz + to-list.proz.
    m-proz = m-proz + to-list.m-proz.
    y-proz = y-proz + to-list.y-proz.
    st-room = st-room + TO-list.room.
    st-pax = st-pax  + to-list.pax.
    st-proz = st-proz + to-list.proz.
    st-logis = st-logis + to-list.logis.
    st-avrgrate = st-avrgrate + to-list.avrgrate.
    stm-room = stm-room + to-list.m-room.        
    stm-pax = stm-pax  + to-list.m-pax.
    stm-proz = stm-proz + to-list.m-proz.
    stm-logis = stm-logis + to-list.m-logis.
    stm-avrgrate = stm-avrgrate + to-list.m-avrgrate.
    sty-room = sty-room + to-list.y-room.        
    sty-pax = sty-pax  + to-list.y-pax.
    sty-proz = sty-proz + to-list.y-proz.
    sty-logis = sty-logis + to-list.y-logis.
    sty-avrgrate = sty-avrgrate + to-list.y-avrgrate.
    sty-revenue = sty-revenue + to-list.revenue.          /*william 99B536*/
END.

PROCEDURE calc-othRev:
DEFINE INPUT PARAMETER datum AS DATE.
DEFINE OUTPUT PARAMETER othRev AS DECIMAL.

DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE max-i       AS INTEGER INITIAL 0.
DEFINE VARIABLE art-list    AS INTEGER EXTENT 200. 
DEFINE VARIABLE serv-vat    AS LOGICAL. 
DEFINE VARIABLE fact        AS DECIMAL. 
DEFINE VARIABLE serv        AS DECIMAL. 
DEFINE VARIABLE vat         AS DECIMAL.


FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
serv-vat = htparam.flogical. 

FOR EACH artikel WHERE artikel.departement = 0
    AND artikel.artart = 0 AND artikel.umsatzart = 1 NO-LOCK 
    BY artikel.artnr:
    max-i = max-i + 1.
    art-list[max-i] = artikel.artnr.
END.
    
    DO i = 1 TO max-i: 
        FIND FIRST artikel WHERE artikel.artnr = art-list[i] 
            AND artikel.departement = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN 
        DO: 
            serv = 0. 
            vat = 0. 
            FOR EACH umsatz WHERE umsatz.artnr = artikel.artnr 
                AND umsatz.departement = artikel.departement 
                AND umsatz.datum EQ datum NO-LOCK: 
                RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                                   artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                
                fact = 1.00 + serv + vat. 
                othRev = othRev + umsatz.betrag / fact.
            END. 
        END.
    END.
END.


