DEFINE TEMP-TABLE room-list 
  FIELD wd           AS INTEGER 
  FIELD datum        AS DATE 
  FIELD bezeich      AS CHAR FORMAT "x(15)"
  FIELD room         AS DECIMAL FORMAT " >>9.99" EXTENT 17 INITIAL 0 
  FIELD coom         AS CHAR EXTENT /*21*/ 17 FORMAT "x(7)" INITIAL "" 
  FIELD k-pax        AS INTEGER INITIAL 0
  FIELD t-pax        AS INTEGER INITIAL 0
  FIELD lodg         AS DECIMAL EXTENT 7 FORMAT "->>>,>>>,>>>,>>9.99"
  FIELD avrglodg     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
  FIELD avrglodg2    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
  FIELD avrgrmrev    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" /*MT 17/10/13 */
  FIELD avrgrmrev2   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" /*FONT 2*/ 
  FIELD others       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" EXTENT 8
  FIELD ly-fcast     AS CHAR    FORMAT "x(7)"
  FIELD ly-actual    AS CHAR    FORMAT "x(7)"
  FIELD ly-avlodge   AS CHAR    FORMAT "x(13)"
  FIELD room-excComp AS INT INIT 0
  FIELD room-comp    AS INT INIT 0
  FIELD fixleist     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" /*Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9 */
  FIELD fixleist2    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" /*Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9 */
  FIELD rmrate      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
  FIELD rmrate2     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
  FIELD revpar      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
  FIELD revpar2     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
.

DEFINE TEMP-TABLE segm-list 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD segm AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE argt-list 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD argtnr AS INTEGER
  FIELD argt AS CHAR 
  FIELD bezeich AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE zikat-list 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD zikatnr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEF INPUT PARAMETER curr-from-date  AS DATE       NO-UNDO.
DEF INPUT PARAMETER curr-to-date    AS DATE       NO-UNDO.
DEF INPUT PARAMETER all-segm        AS LOGICAL    NO-UNDO. 
DEF INPUT PARAMETER all-argt        AS LOGICAL    NO-UNDO.
DEF INPUT PARAMETER all-zikat       AS LOGICAL    NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE FOR room-list.
DEF INPUT PARAMETER TABLE FOR segm-list.
DEF INPUT PARAMETER TABLE FOR argt-list.
DEF INPUT PARAMETER TABLE FOR zikat-list.

DEF TEMP-TABLE s-list
    FIELD datum     AS DATE
    FIELD ly-fcast  AS INTEGER INIT 0
    FIELD ly-actual AS INTEGER INIT 0
    FIELD ly-logis  AS DECIMAL INIT 0
.

DEF VARIABLE date-1         AS DATE NO-UNDO.
DEF VARIABLE date-2         AS DATE NO-UNDO.

DEF VARIABLE curr-ci-date   AS DATE NO-UNDO.
DEF VARIABLE ci-date        AS DATE NO-UNDO.
DEF VARIABLE from-date      AS DATE NO-UNDO.
DEF VARIABLE to-date        AS DATE NO-UNDO.
DEF VARIABLE exchg-rate     AS DECIMAL NO-UNDO.
DEF VARIABLE tot-fcast      AS DECIMAL NO-UNDO.
DEF VARIABLE tot-actual     AS DECIMAL NO-UNDO.
DEF VARIABLE tot-logis      AS DECIMAL NO-UNDO.

/* Add by Michael @ 30/11/2018 for Nihiwatu Resort - ticket no 36774F */
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
ELSE exchg-rate = 1. 
/* End of add */

RUN htpdate.p (87, OUTPUT curr-ci-date).

ASSIGN
    ci-date   = DATE(2, 28, YEAR(curr-ci-date) - 1)
    from-date = ci-date
    to-date   = ci-date
.

ASSIGN ci-date = DATE(MONTH(curr-ci-date), DAY(curr-ci-date),
  YEAR(curr-ci-date) - 1) NO-ERROR.

ASSIGN from-date = DATE(MONTH(curr-from-date), DAY(curr-from-date),
  YEAR(curr-from-date) - 1) NO-ERROR.

ASSIGN to-date = DATE(MONTH(curr-to-date), DAY(curr-to-date),
  YEAR(curr-to-date) - 1) NO-ERROR.

/*IF from-date LT ci-date THEN
DO:
  ASSIGN
    date-1 = from-date
    date-2 = ci-date - 1
  .
  IF to-date LT ci-date THEN date-2 = to-date.
  RUN calculate-2.
END.

IF to-date GE ci-date THEN
DO:
  ASSIGN
    date-1 = ci-date
    date-2 = to-date
  .
  IF from-date GT ci-date THEN ASSIGN date-1 = from-date.
  RUN calculate-2.
  RUN calculate-3.
END.*/

ASSIGN
    date-1 = from-date
    date-2 = to-date
  .
RUN calculate-2.


FIND FIRST room-list WHERE room-list.wd = 0 NO-ERROR.
ASSIGN room-list.ly-fcast   = STRING(tot-fcast,">>>>>>9")
       room-list.ly-actual  = STRING(tot-actual,">>>>>>9")
       room-list.ly-avlodge = STRING(tot-logis / tot-actual,"->,>>>,>>9.99")
 .

PROCEDURE calculate-1:
DEF VAR do-it       AS LOGICAL  NO-UNDO.
DEF VAR rmsharer    AS LOGICAL  NO-UNDO.
DEF VAR datum1      AS DATE     NO-UNDO.

  FOR EACH genstat WHERE genstat.datum GE date-1 
      AND genstat.datum LE date-2
      AND genstat.zinr NE "" 
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ NO-LOCK:
      ASSIGN
        rmsharer = (genstat.resstatus = 13)
        do-it    = NOT rmsharer
      .

      IF do-it THEN
      DO:
          IF genstat.res-date[1] LT genstat.datum
              AND genstat.res-date[2] = genstat.datum 
              AND genstat.resstatus = 8 THEN do-it = NO.
      END.

      IF do-it THEN
      DO:
           FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
      END.

      IF do-it AND NOT all-segm THEN 
      DO: 
        FIND FIRST segm-list WHERE segm-list.segm = genstat.segmentcode 
          AND segm-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE segm-list. 
      END. 
      
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST argt-list WHERE argt-list.argt = genstat.argt 
          AND argt-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE argt-list. 
      END. 
      
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST zikat-list WHERE zikat-list.zikatnr = genstat.zikatnr 
         AND zikat-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE zikat-list. 
      END. 

      IF do-it THEN
      DO: 
          FIND FIRST s-list WHERE s-list.datum = genstat.datum NO-ERROR.
          IF NOT AVAILABLE s-list THEN
          DO:
            CREATE s-list.
            ASSIGN s-list.datum = genstat.datum.
          END.
          ASSIGN
            s-list.ly-fcast  = s-list.ly-fcast   + 1
            s-list.ly-actual = s-list.ly-actual  + 1
            s-list.ly-logis  = s-list.ly-logis + genstat.logis
          .

          /* Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9
          FIND FIRST fixleist WHERE fixleist.resnr EQ genstat.resnr NO-LOCK NO-ERROR.
          IF AVAILABLE fixleist THEN ASSIGN room-list.fixleist = room-list.fixleist + fixleist.betrag.
          End of add */
      END.
  END.

  FOR EACH s-list:
    ASSIGN 
      datum1 = s-list.datum
      datum1 = DATE(MONTH(datum1), DAY(datum1), YEAR(datum1) + 1)
    .
    FIND FIRST room-list WHERE room-list.datum = datum1 NO-ERROR.

    IF AVAILABLE room-list THEN
    ASSIGN
      tot-logis            = tot-logis + s-list.ly-logis
      s-list.ly-logis      = s-list.ly-logis / s-list.ly-actual
      room-list.ly-fcast   = STRING(s-list.ly-fcast,">>>>>>9")
      room-list.ly-actual  = STRING(s-list.ly-actual,">>>>>>9")
      room-list.ly-avlodge = STRING(s-list.ly-logis,"->,>>>,>>9.99")
      tot-fcast            = tot-fcast + s-list.ly-fcast
      tot-actual           = tot-actual + s-list.ly-actual
    .
  END.
END.

PROCEDURE calculate-2:
DEF VAR do-it       AS LOGICAL  NO-UNDO.
DEF VAR rmsharer    AS LOGICAL  NO-UNDO.
DEF VAR datum1      AS DATE     NO-UNDO.

  FOR EACH s-list:
      DELETE s-list.
  END.


  FOR EACH genstat WHERE genstat.datum GE date-1 
      AND genstat.datum LE date-2
      AND genstat.zinr NE "" 
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ NO-LOCK: 
      
      ASSIGN
        rmsharer = (genstat.resstatus = 13)
        do-it    = NOT rmsharer
      .
      IF do-it THEN
      DO:
          IF genstat.res-date[1] LT genstat.datum
              AND genstat.res-date[2] = genstat.datum 
              AND genstat.resstatus = 8 THEN do-it = NO.
      END.

      IF do-it THEN
      DO:
           FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
      END.

      IF do-it THEN
      DO:
           FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
      END.

      IF do-it AND NOT all-segm THEN 
      DO: 
        FIND FIRST segm-list WHERE segm-list.segm = genstat.segmentcode 
          AND segm-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE segm-list. 
      END. 
      
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST argt-list WHERE argt-list.argt = genstat.argt 
          AND argt-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE argt-list. 
      END. 
      
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST zikat-list WHERE zikat-list.zikatnr = genstat.zikatnr 
         AND zikat-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE zikat-list. 
      END. 

      IF do-it THEN
      DO: 
          FIND FIRST s-list WHERE s-list.datum = genstat.datum NO-ERROR.
          IF NOT AVAILABLE s-list THEN
          DO:
            CREATE s-list.
            ASSIGN s-list.datum = genstat.datum.
          END.
          ASSIGN
            s-list.ly-fcast  = s-list.ly-fcast   + 1
            s-list.ly-actual = s-list.ly-actual  + 1
            s-list.ly-logis  = s-list.ly-logis + genstat.logis
          .

          /* Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9
          FIND FIRST fixleist WHERE fixleist.resnr EQ genstat.resnr NO-LOCK NO-ERROR.
          IF AVAILABLE fixleist THEN ASSIGN room-list.fixleist = room-list.fixleist + fixleist.betrag.
          End of add */
      END.
  END.

  FOR EACH s-list:
    ASSIGN 
      datum1 = s-list.datum
      datum1 = DATE(MONTH(datum1), DAY(datum1), YEAR(datum1) + 1) NO-ERROR
    .
    FIND FIRST room-list WHERE room-list.datum = datum1 NO-ERROR.
    IF AVAILABLE room-list THEN
    ASSIGN
      tot-logis            = tot-logis + s-list.ly-logis
      s-list.ly-logis      = s-list.ly-logis / s-list.ly-actual
      room-list.ly-fcast   = STRING(s-list.ly-fcast,">>>>>>9")
      room-list.ly-actual  = STRING(s-list.ly-actual,">>>>>>9")
      room-list.ly-avlodge = STRING(s-list.ly-logis,"->,>>>,>>9.99")
      tot-fcast            = tot-fcast + s-list.ly-fcast
      tot-actual           = tot-actual + s-list.ly-actual
    .
  END.
END.


PROCEDURE calculate-3:
DEF VAR curr-date           AS DATE     NO-UNDO.
DEF VAR do-it               AS LOGICAL  NO-UNDO.
DEFINE VARIABLE datum3      AS DATE     NO-UNDO.
DEFINE VARIABLE datum1      AS DATE. 
DEFINE VARIABLE datum2      AS DATE. 

  FOR EACH s-list:
      DELETE s-list.
  END.

  FOR EACH res-line WHERE (res-line.active-flag = 2
    AND res-line.resstatus LE 13 
    AND res-line.resstatus NE 4 
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 9 
    AND res-line.resstatus NE 10 
    AND NOT (res-line.ankunft GT date-2) 
    AND NOT (res-line.abreise LT date-1)) 
    AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0
    USE-INDEX gnrank_ix NO-LOCK,
    FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK
    BY res-line.gastnr BY res-line.resnr: /*MT 13/08/12 */

      ASSIGN do-it = YES.

      IF do-it THEN
      DO:
        FIND FIRST segment WHERE segment.segmentcode = genfcast.segmentcode
          NO-LOCK NO-ERROR.
        do-it = AVAILABLE segment AND segment.vip-level = 0.
      END.
    
      IF do-it AND NOT all-segm THEN 
      DO: 
        FIND FIRST segm-list WHERE segm-list.segm = genfcast.segmentcode 
          AND segm-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE segm-list. 
      END. 
      
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST argt-list WHERE argt-list.argt = genfcast.argt 
          AND argt-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE argt-list. 
      END. 
      
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST zikat-list WHERE zikat-list.zikatnr = genfcast.zikatnr 
         AND zikat-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE zikat-list. 
      END. 

      datum1 = date-1. 
      IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
      datum2 = date-2. 
      IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.
      
      DO curr-date = datum1 TO datum2:
        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
            AND NOT res-line.zimmerfix THEN DO:
            FIND FIRST s-list WHERE s-list.datum = curr-date NO-ERROR.
            IF NOT AVAILABLE s-list THEN
            DO:
              CREATE s-list.
              ASSIGN s-list.datum = curr-date.
            END.
            s-list.ly-fcast = s-list.ly-fcast  + res-line.zimmeranz.        
        END.
      END.
  END.
    
    
  /*
  DO curr-date = date-1 TO date-2:
    FOR EACH genfcast WHERE genfcast.ankunft LE curr-date
      AND genfcast.abreise GT curr-date
      AND genfcast.datum LE ci-date 
      AND genfcast.resstatus NE 11 NO-LOCK:

      do-it = genfcast.CANCELLED EQ ? OR NOT genfcast.CANCELLED LE ci-date.
      
      IF do-it THEN
      DO:
        FIND FIRST segment WHERE segment.segmentcode = genfcast.segmentcode
          NO-LOCK NO-ERROR.
        do-it = AVAILABLE segment AND segment.vip-level = 0.
      END.

      IF do-it AND NOT all-segm THEN 
      DO: 
        FIND FIRST segm-list WHERE segm-list.segm = genfcast.segmentcode 
          AND segm-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE segm-list. 
      END. 
      
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST argt-list WHERE argt-list.argt = genfcast.argt 
          AND argt-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE argt-list. 
      END. 
      
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST zikat-list WHERE zikat-list.zikatnr = genfcast.zikatnr 
         AND zikat-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE zikat-list. 
      END. 

      IF do-it THEN
      DO: 
        FIND FIRST s-list WHERE s-list.datum = curr-date NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN s-list.datum = curr-date.
        END.
        s-list.ly-fcast = s-list.ly-fcast  + genfcast.zimmeranz.

        /* Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9
        FIND FIRST fixleist WHERE fixleist.resnr EQ genstat.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE fixleist THEN ASSIGN room-list.fixleist = room-list.fixleist + fixleist.betrag.
        End of add */
      END.
    END.
  END.*/

  FOR EACH s-list:
    ASSIGN 
      datum3 = s-list.datum
      datum3 = DATE(MONTH(datum3), DAY(datum3), YEAR(datum3) + 1) NO-ERROR
    .
    FIND FIRST room-list WHERE room-list.datum = datum3 NO-ERROR.
    IF AVAILABLE room-list THEN
    ASSIGN room-list.ly-fcast = STRING(s-list.ly-fcast,">>>>>>9")
           tot-fcast            = tot-fcast + s-list.ly-fcast
       .
  END.

END.

