DEFINE TEMP-TABLE cl-list 
  FIELD segm       AS INTEGER FORMAT ">>9" 
  FIELD betriebsnr AS INTEGER 
  FIELD compli     AS LOGICAL INITIAL NO 
  FIELD bezeich    AS CHAR FORMAT "x(18)" 
  FIELD droom      AS INTEGER FORMAT "->9" 
  FIELD proz1      AS DECIMAL FORMAT "->>9.99"
  FIELD mroom      AS INTEGER FORMAT ">>,>>9" 
  FIELD proz2      AS DECIMAL FORMAT "->>9.99" 
  FIELD dpax       AS INTEGER FORMAT ">>9" 
  FIELD mpax       AS INTEGER FORMAT ">,>>9" 
  FIELD drate      AS DECIMAL FORMAT ">,>>>,>>9.99" 
  FIELD mrate      AS DECIMAL FORMAT ">,>>>,>>9.99" 
  FIELD drev       AS DECIMAL FORMAT "->,>>>,>>9.99" 
  FIELD mrev       AS DECIMAL FORMAT "->>,>>>,>>9.99"
  FIELD yroom      AS INTEGER FORMAT "->,>>,>>9"
  FIELD proz3      AS DECIMAL FORMAT "->>9.99"
  FIELD ypax       AS INTEGER FORMAT "->,>>,>>9"
  FIELD yrate      AS DECIMAL FORMAT ">,>>>,>>9.99"
  FIELD yrev       AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" 
  FIELD zero-flag  AS LOGICAL. 

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID" 
  FIELD ind AS INTEGER INITIAL 0
  FIELD reason      AS CHAR     /*MT 11/12/12 */
  FIELD gespstart   AS DATE     /*MT 11/12/12 */
  FIELD gespende    AS DATE.    /*MT 11/12/12 */


DEF INPUT PARAMETER pvILanguage     AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER opening-date    AS DATE.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER fdate           AS DATE.
DEF INPUT PARAMETER tdate           AS DATE.
DEF INPUT PARAMETER segmtype-exist  AS LOGICAL.
DEF INPUT PARAMETER mi-mtd-chk      AS LOGICAL.
DEF INPUT PARAMETER mi-ftd-chk      AS LOGICAL.
DEF INPUT PARAMETER mi-excHU-chk    AS LOGICAL.
DEF INPUT PARAMETER mi-excComp-chk  AS LOGICAL.
DEF INPUT PARAMETER long-digit      AS LOGICAL. 

DEF OUTPUT PARAMETER TABLE FOR cl-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rm-drecap2".

DEFINE VARIABLE do-it AS LOGICAL.

DEFINE VARIABLE droomRev AS INTEGER FORMAT ">>9".
DEFINE VARIABLE mroomRev AS INTEGER FORMAT ">>,>>9".
DEFINE VARIABLE yroomRev AS INTEGER FORMAT ">>,>>9".

/* Start - Oscar (28/01/25) - FD7927 - Adjust variable */

DEFINE VARIABLE drevRev  AS DECIMAL FORMAT ">>,>>>,>>9.99". 
DEFINE VARIABLE mrevRev  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE yrevRev  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".

DEFINE VARIABLE dpaxRev  AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mpaxRev  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE ypaxRev  AS INTEGER FORMAT "->,>>,>>9".

DEFINE VARIABLE drateRev AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE mrateRev AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE yrateRev AS DECIMAL FORMAT ">,>>>,>>9.99".

DEFINE VARIABLE droomComp AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mroomComp AS INTEGER FORMAT "->,>>>,>>9".
DEFINE VARIABLE yroomComp AS INTEGER FORMAT "->,>>>,>>9".

DEFINE VARIABLE dpaxComp  AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mpaxComp  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE ypaxComp  AS INTEGER FORMAT "->,>>,>>9".

DEFINE VARIABLE droomHU AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mroomHU AS INTEGER FORMAT "->,>>>,>>9".
DEFINE VARIABLE yroomHU AS INTEGER FORMAT "->,>>>,>>9".

DEFINE VARIABLE dpaxHU  AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mpaxHU  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE ypaxHU  AS INTEGER FORMAT "->,>>,>>9".

/* 
DEFINE VARIABLE droomExc AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mroomExc AS INTEGER FORMAT "->,>>>,>>9".
DEFINE VARIABLE yroomExc AS INTEGER FORMAT "->,>>>,>>9". */

DEFINE VARIABLE tot-room AS INTEGER INITIAL 0. /*active room*/
DEFINE VARIABLE all-room AS INTEGER INITIAL 0.

DEFINE VARIABLE dvacant AS INTEGER. 
DEFINE VARIABLE mvacant AS INTEGER. 
DEFINE VARIABLE yvacant AS INTEGER. 

DEFINE VARIABLE dooo AS INTEGER. 
DEFINE VARIABLE mooo AS INTEGER. 
DEFINE VARIABLE yooo AS INTEGER. 

DEFINE VARIABLE dnoshow AS INTEGER. 
DEFINE VARIABLE mnoshow AS INTEGER. 
DEFINE VARIABLE ynoshow AS INTEGER. 

DEFINE VARIABLE dcancel AS INTEGER. 
DEFINE VARIABLE mcancel AS INTEGER. 
DEFINE VARIABLE ycancel AS INTEGER. 

DEFINE VARIABLE cal-umsatz1-called AS LOGICAL INITIAL NO. /* Oscar (28/01/25) - FD7927 - variable to check if function already called or not to prevent duplicate */
DEFINE VARIABLE cal-umsatz4-called AS LOGICAL INITIAL NO. /* Oscar (28/01/25) - FD7927 - variable to check if function already called or not to prevent duplicate */

/* End - Oscar (28/01/25) - FD7927 - Adjust variable */

DEFINE VARIABLE droom AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE proz1 AS DECIMAL FORMAT ">>9.9". 
DEFINE VARIABLE mroom AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE proz2 AS INTEGER FORMAT ">>9.9". 
DEFINE VARIABLE dpax  AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mpax  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE drate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE mrate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE drev  AS DECIMAL FORMAT ">>,>>>,>>9.99". 
DEFINE VARIABLE mrev  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE yroom AS INTEGER FORMAT "->,>>,>>9".
DEFINE VARIABLE ypax  AS INTEGER FORMAT "->,>>,>>9".
DEFINE VARIABLE yrate AS DECIMAL FORMAT ">,>>>,>>9.99".
DEFINE VARIABLE yrev  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 

/* DEFINE VARIABLE from-bez AS CHAR FORMAT "x(22)". 
DEFINE VARIABLE to-bez AS CHAR FORMAT "x(22)".  */
 
DEFINE VARIABLE inactive     AS INTEGER.

DEFINE VARIABLE mtd-act      AS INTEGER.
DEFINE VARIABLE mtd-totrm    AS INTEGER.

DEFINE VARIABLE ytd-act      AS INTEGER.
DEFINE VARIABLE ytd-totrm    AS INTEGER.

/* DEFINE VARIABLE ncompli AS INTEGER FORMAT ">>9".
DEFINE VARIABLE mtd-ncompli AS INTEGER FORMAT ">>9".
DEFINE VARIABLE ytd-ncompli AS INTEGER FORMAT ">>9". */

/* DEFINE VARIABLE dcompli AS INTEGER .
DEFINE VARIABLE mcompli AS INTEGER .
DEFINE VARIABLE ycompli AS INTEGER . */

/* DEFINE VARIABLE dHU AS INTEGER .
DEFINE VARIABLE mHU AS INTEGER .
DEFINE VARIABLE yHU AS INTEGER . */

DEFINE VARIABLE ci-date AS DATE. 


FIND FIRST htparam WHERE paramnr = 186.
opening-date = htparam.fdate.
IF MONTH(to-date) = MONTH(opening-date) 
    AND YEAR(to-date) = YEAR(opening-date)THEN
    from-date = opening-date.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

IF from-date LT ci-date THEN RUN create-umsatz.
ELSE RUN create-umsatz1.

FOR EACH cl-list WHERE cl-list.bezeich = "Deleted":
  DELETE cl-list.
END.
/*
FOR EACH cl-list:
    DISP cl-list.segm cl-list.bezeich cl-list.droom cl-list.proz1 cl-list.drev.
END.
*/

PROCEDURE create-umsatz1: 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE black-list AS INTEGER. 

  FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
  black-list = htparam.finteger. 

  FOR EACH cl-list: 
    delete cl-list. 
  END.

  ASSIGN
      droom     = 0
      mroom     = 0
      yroom     = 0
      dpax      = 0
      mpax      = 0
      ypax      = 0
      drev      = 0
      mrev      = 0
      yrev      = 0
      tot-room  = 0
      inactive  = 0
      mtd-act   = 0
      ytd-act   = 0
      mtd-totrm = 0
      ytd-totrm = 0
    .
  
  FOR EACH zimmer WHERE NOT zimmer.sleeping NO-LOCK: 
    inactive = inactive + 1. 
  END. 
    
  FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK: 
    tot-room = tot-room + 1.
  END.
  
  RUN count-mtd-totrm1.

  IF NOT segmtype-exist THEN 
  DO: 
    RUN cal-umsatz4(1, 12, 15, 49, translateExtended ("Room Revenue",lvCAREA,""), "", YES).
    RUN cal-umsatz4(13, 14, 0, 0, translateExtended ("Total Room Occ",lvCAREA,""),
        translateExtended ("  Double Occupancy",lvCAREA,""), NO).
  END. 
  ELSE 
  DO: 
    RUN cal-umsatz4a(0, 0, translateExtended ("Room Revenue",lvCAREA,""), "", YES). 
    RUN cal-umsatz4b(1, 2, translateExtended ("Total Room Occ",lvCAREA,""), 
        translateExtended ("  Double Occupancy",lvCAREA,""), NO).
  END. 

  RUN cal-umsatz5. 
  RUN cal-umsatz6. 

END. 


PROCEDURE create-umsatz: 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE black-list AS INTEGER. 

  FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
  black-list = htparam.finteger. 

  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  ASSIGN
      droom     = 0
      mroom     = 0
      yroom     = 0
      dpax      = 0
      mpax      = 0
      ypax      = 0
      drev      = 0
      mrev      = 0
      yrev      = 0
      tot-room  = 0
      inactive  = 0
      mtd-act   = 0
      ytd-act   = 0
      mtd-totrm = 0
      ytd-totrm = 0
      .
  
  FOR EACH zimmer WHERE NOT zimmer.sleeping NO-LOCK: 
    inactive = inactive + 1. 
  END. 
    
  IF to-date LT ci-date THEN DO:
    FOR EACH zkstat WHERE zkstat.datum = to-date NO-LOCK:
      tot-room = tot-room + zkstat.anz100.
    END.
  END.
  ELSE DO:
    FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK: 
      tot-room = tot-room + 1.
    END. 
  END.
  
  RUN count-mtd-totrm.

  IF NOT segmtype-exist THEN 
  DO: 
    RUN cal-umsatz1(1, 12, 15, 49, translateExtended ("Room Revenue",lvCAREA,""), "", YES).
    RUN cal-umsatz1(13, 14, 0, 0, translateExtended ("Total Room Occ",lvCAREA,""),
        translateExtended ("  Double Occupancy",lvCAREA,""), NO).
  END. 
  ELSE 
  DO: 
    RUN cal-umsatz1a(0, 0, translateExtended ("Room Revenue",lvCAREA,""), "", YES). 
    RUN cal-umsatz1b(1, 2, translateExtended ("Total Room Occ",lvCAREA,""), 
        translateExtended ("  Double Occupancy",lvCAREA,""), NO).
  END. 

  RUN cal-umsatz2. 
  RUN cal-umsatz3. 
  RUN no-show.
END.


PROCEDURE count-mtd-totrm1:
  DEF VAR datum AS DATE NO-UNDO.
  DEF VAR tot1  AS INTEGER.
  DEF VAR glob-tot  AS INTEGER.
  
  ASSIGN mtd-totrm = 0 mtd-act = 0 ytd-act = 0 ytd-totrm = 0.

  FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
      glob-tot = glob-tot + 1.
  END.


  DO datum = from-date TO to-date:
      ASSIGN tot1 = 0 .

      FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
          tot1 = tot1 + 1.
      END.

      IF tot1 = 0 THEN tot1 = glob-tot.

      IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date)) 
      OR (mi-ftd-chk AND (datum GE fdate AND datum LE tdate)) 
      THEN mtd-act = mtd-act + tot1.
      ytd-act = ytd-act + tot1.

      FOR EACH zimmer NO-LOCK:
          IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
              OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
              mtd-totrm = mtd-totrm + 1.
          ytd-totrm = ytd-totrm + 1.
      END.        
  END.
END.

PROCEDURE count-mtd-totrm:
  DEF VAR datum AS DATE NO-UNDO.
  DEF VAR tot1  AS INTEGER.
  DEF VAR glob-tot  AS INTEGER.
  ASSIGN mtd-totrm = 0 mtd-act = 0 ytd-act = 0 ytd-totrm = 0.
  
  FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
      glob-tot = glob-tot + 1.
  END.
  
  DO datum = from-date TO to-date:
      ASSIGN tot1 = 0 .
      FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
          tot1 = tot1  + zkstat.anz100.
      END.
      IF tot1 = 0 THEN 
          tot1 = glob-tot.
          
      IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
          OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
          mtd-act = mtd-act + tot1.
      ytd-act = ytd-act + tot1.

      FIND FIRST zinrstat WHERE zinrstat.zinr =  "tot-rm" AND 
          zinrstat.datum = datum NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN
      DO:
          IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
          OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
              mtd-totrm = mtd-totrm + zinrstat.zimmeranz.

          ytd-totrm = ytd-totrm + zinrstat.zimmeranz.
      END.
      ELSE
      DO:
          IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
              OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
              mtd-totrm = mtd-totrm + glob-tot + inactive.
          ytd-totrm = ytd-totrm + glob-tot + inactive.
      END.
      
  END.
END.

PROCEDURE cal-umsatz1: 
  DEFINE INPUT PARAMETER i1 AS INTEGER. 
  DEFINE INPUT PARAMETER i2 AS INTEGER. 
  DEFINE INPUT PARAMETER i3 AS INTEGER. 
  DEFINE INPUT PARAMETER i4 AS INTEGER. 
  DEFINE INPUT PARAMETER rev-title AS CHAR. 
  DEFINE INPUT PARAMETER rev-title1 AS CHAR. 
  DEFINE INPUT PARAMETER show-avrg AS LOGICAL. 

  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE datum  AS DATE. 
  DEFINE VARIABLE do-it1 AS LOGICAL.
  DEFINE VARIABLE d1 AS DATE.
  DEFINE VARIABLE d2 AS DATE.
  DEFINE VARIABLE datum0 AS DATE.
  DEFINE VARIABLE datum1 AS DATE.
  DEFINE VARIABLE datum2 AS DATE.
  DEFINE VARIABLE curr-i AS INTEGER.
  DEFINE VARIABLE net-lodg    AS DECIMAL.
  DEFINE VARIABLE Fnet-lodg   AS DECIMAL.
  DEFINE VARIABLE tot-breakfast   AS DECIMAL.
  DEFINE VARIABLE tot-Lunch       AS DECIMAL.
  DEFINE VARIABLE tot-dinner      AS DECIMAL.
  DEFINE VARIABLE tot-Other       AS DECIMAL.
  DEFINE VARIABLE tot-rmrev       AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-vat         AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-service     AS DECIMAL INITIAL 0.
  

  DEFINE BUFFER bgenstat FOR genstat.

  d1 = from-date.
  IF to-date LT (ci-date - 1) THEN d2 = to-date.
  ELSE d2 = ci-date - 1.
  
  FOR EACH segment WHERE 
    ((segment.segmentcode GE i1 AND segment.segmentcode LE i2) 
    OR (segment.segmentcode GE i3 AND segment.segmentcode LE i4)) 
    NO-LOCK BY segment.segmentcode: 
        
      FIND FIRST bgenstat WHERE bgenstat.segmentcode = segment.segmentcode 
        AND bgenstat.datum GE d1 
        AND bgenstat.datum LE d2 
        AND bgenstat.resstatus NE 13 
        AND bgenstat.gratis EQ 0 
        AND bgenstat.segmentcode NE 0 
        AND bgenstat.nationnr NE 0
        AND bgenstat.zinr NE ""
        AND bgenstat.res-logic[2] NO-LOCK NO-ERROR.
      IF AVAILABLE bgenstat THEN ASSIGN do-it1 = YES.
      ELSE 
      DO: 
        IF segment.bezeich MATCHES "*$$0" THEN ASSIGN do-it1 = NO.
        ELSE do-it1 = YES.
      END.

      IF do-it1 THEN
      DO:
        CREATE cl-list. 
        cl-list.segm = segment.segmentcode. 
        cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0").
      
        FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode 
          AND genstat.datum GE d1 
          AND genstat.datum LE d2 
          AND genstat.resstatus NE 13 
          AND genstat.gratis EQ 0 
          AND genstat.segmentcode NE 0 
          AND genstat.nationnr NE 0
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] EQ YES /*27032012 genstat.res-logic[2] MU */
          USE-INDEX segm_ix NO-LOCK:
                
            /* Start - Oscar (28/01/25) - FD7927 - Adjust to e1 desktop version */
            /*IF genstat.res-date[1] LT genstat.datum AND genstat.res-date[2] = genstat.datum 
            AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
            ELSE*/
            DO:
              IF genstat.datum = to-date THEN 
              DO: 
                cl-list.droom = cl-list.droom + 1. 
                cl-list.dpax  = cl-list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
                cl-list.drev  = cl-list.drev + genstat.logis. 
                
                droomRev      = droomRev + 1.
                dpaxRev       = dpaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. /* Oscar (07/03/25) - 89D27E - fix duplicate count on pax */
                drevRev       = drevRev + genstat.logis.
              END.
              IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                  OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
              DO:
                  cl-list.mroom   = cl-list.mroom + 1. 
                  cl-list.mpax    = cl-list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
                  cl-list.mrev    = cl-list.mrev + genstat.logis. 
                  
                  mroomRev        = mroomRev + 1. 
                  mpaxRev         = mpaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
                  mrevRev         = mrevRev + genstat.logis. 
              END.
                
              ASSIGN
                cl-list.yroom   = cl-list.yroom + 1
                cl-list.ypax    = cl-list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                cl-list.yrev    = cl-list.yrev + genstat.logis

                yroomRev        = yroomRev + 1
                ypaxRev         = ypaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. /* Oscar (07/03/25) - 89D27E - fix wrong count */
                yrevRev         = yrevRev + genstat.logis. 
            END.  
            /* End - Oscar (28/01/25) - FD7927 - Adjust to e1 desktop version */            
        END.
      END.           
  END. 
  
  IF do-it THEN
  DO:
    FOR EACH genstat WHERE genstat.datum GE d1 
      AND genstat.datum LE d2  
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.resstatus NE 13 
      AND genstat.res-logic[2] EQ YES 
      NO-LOCK: /*27032012 genstat.res-logic[2] MU */
        FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-ERROR.
        IF AVAILABLE segment THEN       /*kl segment ada*/
        DO:
          FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
          IF AVAILABLE cl-list THEN
          DO:
            IF genstat.datum = to-date THEN 
            DO: 
              cl-list.drev = cl-list.drev + genstat.res-deci[1].
              drevRev = drevRev + genstat.logis.
            END.

            IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
            DO:
              cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
              mrevRev = mrevRev + genstat.logis.
            END.
          END.
        END.
        ELSE    /*klo gada*/
        DO:
          FIND FIRST guestseg WHERE guestseg.gastnr EQ genstat.gastnr NO-ERROR.
          IF AVAILABLE guestseg THEN
          DO:
            IF guestseg.reihenfolge EQ 1 THEN
            DO:
              FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
              IF AVAILABLE cl-list THEN
              DO:
                IF genstat.datum = to-date THEN 
                DO: 
                    cl-list.drev = cl-list.drev + genstat.res-deci[1].
                    drevRev = drevRev + genstat.logis.
                END.

                IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
                DO:
                    cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
                    mrevRev = mrevRev + genstat.logis.
                END.
              END.
            END.
            ELSE
            DO:
              FIND FIRST guestseg WHERE guestseg.reihenfolge EQ 0 NO-ERROR.
              IF AVAILABLE guestseg THEN
              DO:
                FIND FIRST cl-list WHERE cl-list.segm EQ guestseg.segmentcode NO-ERROR.
                IF AVAILABLE cl-list THEN
                DO:
                  IF genstat.datum = to-date THEN 
                  DO: 
                      cl-list.drev = cl-list.drev + genstat.res-deci[1].
                      drevRev = drevRev + genstat.logis.
                  END.

                  IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                  OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
                  DO:
                      cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
                      mrevRev = mrevRev + genstat.logis.
                  END.
                END.
              END.
            END.
          END.
          /* Oscar (28/01/25) - FD7927 - Adjust to e1 desktop version */
          /* ELSE
          DO:
            FIND FIRST segment NO-ERROR. 
            IF AVAILABLE segment THEN
            DO:
              FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
              IF AVAILABLE cl-list THEN
              DO:
                IF genstat.datum = to-date THEN 
                DO: 
                  cl-list.drev = cl-list.drev + genstat.res-deci[1].
                  drev = drev + genstat.logis.
                END.

                IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                    OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
                DO:
                  cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
                  mrev = mrev + genstat.logis.
                END.
              END.
            END.
          END. */
        END.
    END.
  END.
  
  /* Oscar (28/01/25) - FD7927 - Adjust to e1 desktop version */
  IF (NOT cal-umsatz1-called) AND (to-date GE ci-date) THEN 
  DO:
    ASSIGN d2 = d2 + 1.

    FOR EACH res-line WHERE ((res-line.resstatus LE 13 
      AND res-line.resstatus NE 4
      AND res-line.resstatus NE 8
      AND res-line.resstatus NE 9 
      AND res-line.resstatus NE 10 
      AND res-line.resstatus NE 12 
      AND res-line.active-flag LE 1 
      AND NOT (res-line.ankunft GT to-date) 
      AND NOT (res-line.abreise LT d2))) OR
      (res-line.resstatus = 8 AND res-line.active-flag = 2
      AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
      AND res-line.gastnr GT 0 
      AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
      FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
      BY res-line.resnr BY res-line.reslinnr descending: 

        ASSIGN curr-i = 0.

        IF res-line.kontignr LT 0 THEN 
        DO:
          ASSIGN do-it1 = YES.
          FIND FIRST cl-list WHERE cl-list.segm EQ reservation.segmentcode NO-ERROR.

          IF NOT AVAILABLE cl-list THEN 
          DO:
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment AND NOT segment.bezeich MATCHES "*$$0" THEN 
            DO:
              IF segment.betriebsnr NE 1 AND segment.betriebsnr NE 2 THEN
              DO:
                CREATE cl-list.
                cl-list.compli     = NO. 
                cl-list.segm       = segment.segmentcode. 
                cl-list.bezeich    = segment.bezeich.
                cl-list.betriebsnr = segment.betriebsnr.
              END.
              ELSE
              DO:
                CREATE cl-list.
                cl-list.compli     = YES. 
                cl-list.segm       = segment.segmentcode. 
                cl-list.bezeich    = segment.bezeich.
                cl-list.betriebsnr = segment.betriebsnr.
              END.
            END.    
            ELSE ASSIGN do-it1 = NO.
          END.

          IF do-it1 = YES THEN
          DO:
            datum1 = d2.
            IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
            datum2 = to-date. 
            IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.
        
            DO datum0 = datum1 TO datum2:
              ASSIGN curr-i = curr-i + 1.
              IF datum0 = res-line.abreise THEN .
              ELSE
              DO:
                ASSIGN 
                  net-lodg      = 0
                  tot-breakfast = 0
                  tot-lunch     = 0
                  tot-dinner    = 0
                  tot-other     = 0
                . 
            
                RUN get-room-breakdown.p(RECID(res-line), datum0, curr-i, from-date,
                                        OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                        OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                        OUTPUT tot-dinner, OUTPUT tot-other,
                                        OUTPUT tot-rmrev, OUTPUT tot-vat,
                                        OUTPUT tot-service).    
                
                /* Start - Oscar (28/01/25) - FD7927 - Adjust to e1 desktop version */
                IF datum0 = to-date THEN 
                DO:
                  cl-list.droom = cl-list.droom + res-line.zimmeranz. 
                  cl-list.dpax  = cl-list.dpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                  cl-list.drev  = cl-list.drev + net-lodg. 

                  IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                  DO:
                    droomRev = droomRev + res-line.zimmeranz. 
                    dpaxRev  = dpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                    drevRev  = drevRev + net-lodg.
                  END.

                  IF cl-list.betriebsnr EQ 1 THEN
                  DO:
                    droomComp = droomComp + res-line.zimmeranz.
                    dpaxComp  = dpaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                  IF cl-list.betriebsnr EQ 2 THEN
                  DO:
                    droomHU = droomHU + res-line.zimmeranz.
                    dpaxHU  = dpaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                END.

                IF (mi-mtd-chk AND MONTH(datum0) = MONTH(to-date))
                  OR (mi-ftd-chk AND datum0 GE d2 AND datum0 LE tdate) THEN
                DO:
                  cl-list.mroom   = cl-list.mroom + res-line.zimmeranz. 
                  cl-list.mpax    = cl-list.mpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                  cl-list.mrev    = cl-list.mrev + net-lodg. 
                  
                  IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                  DO:
                    mroomRev           = mroomRev + res-line.zimmeranz. 
                    mpaxRev            = mpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                    mrevRev            = mrevRev + net-lodg.
                  END.
                  
                  IF cl-list.betriebsnr EQ 1 THEN
                  DO:
                    mroomComp = mroomComp + res-line.zimmeranz.
                    mpaxComp  = mpaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                  IF cl-list.betriebsnr EQ 2 THEN
                  DO:
                    mroomHU = mroomHU + res-line.zimmeranz.
                    mpaxHU  = mpaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                END.

                ASSIGN
                  cl-list.yroom   = cl-list.yroom + res-line.zimmeranz
                  cl-list.ypax    = cl-list.ypax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis
                  cl-list.yrev    = cl-list.yrev + net-lodg.

                IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                DO:
                  yroomRev           = yroomRev + res-line.zimmeranz.
                  ypaxRev            = ypaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                  yrevRev            = yrevRev + net-lodg.
                END.

                IF cl-list.betriebsnr EQ 1 THEN
                DO:
                  yroomComp = yroomComp + res-line.zimmeranz.
                  ypaxComp  = ypaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                END.
                IF cl-list.betriebsnr EQ 2 THEN
                DO:
                  yroomHU = yroomHU + res-line.zimmeranz.
                  ypaxHU  = ypaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                END. 

                /* End - Oscar (28/01/25) - FD7927 - Adjust to e1 desktop version */
              END.                                        
            END.
          END.
        END.
    END.  /*do for each*/

    cal-umsatz1-called = YES.
  END. /*do if 1*/
  
  
  FOR EACH cl-list WHERE ((cl-list.segm GE i1 AND cl-list.segm LE i2) 
        OR (cl-list.segm GE i3 AND cl-list.segm LE i4)): 

        IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
        IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
        cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
        cl-list.proz2 = 100.0 * cl-list.mroom / /*(tot-room * day(to-date))*/ mtd-act. 
        cl-list.proz3 = 100.0 * cl-list.yroom / /*(tot-room * day(to-date))*/ ytd-act. 
        IF droomRev NE 0 THEN drateRev = drevRev / droomRev. 
        IF mroomRev NE 0 THEN mrateRev = mrevRev / mroomRev. 
        IF yroomRev NE 0 THEN yrateRev = yrevRev / yroomRev. 
    
        IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
        IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
        IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
    
        /* dpaxRev = dpaxRev + cl-list.dpax. */ /* Oscar (07/03/25) - 89D27E - fix duplicate count on pax */
        IF cl-list.drev EQ 0 AND cl-list.mrev EQ 0 AND cl-list.yrev EQ 0 THEN 
            cl-list.zero-flag = YES.
  END. 

  CREATE cl-list.
  
  /*Start - Oscar (28/01/25) - FD7927 - Adjust variable */
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = rev-title
    cl-list.droom = droomRev
    cl-list.proz1 = droomRev / tot-room * 100
    cl-list.mroom = mroomRev
    cl-list.proz2 = mroomRev / mtd-act * 100
    cl-list.dpax = dpaxRev
    cl-list.mpax = mpaxRev
    cl-list.yroom = yroomRev
    cl-list.ypax = ypaxRev
    cl-list.proz3 = ytd-act * 100
    cl-list.drev = drevRev
    cl-list.mrev = mrevRev
    cl-list.yrev = yrevRev
  .
  /* End - Oscar (28/01/25) - FD7927 - Adjust variable */

  IF show-avrg THEN 
  DO: 
    IF droomRev NE 0 THEN cl-list.drate = drevRev / droomRev.
    ELSE cl-list.drate = 0. 
    IF mroomRev NE 0 THEN cl-list.mrate = mrevRev / mroomRev.
    ELSE cl-list.mrate = 0.
    IF yroomRev NE 0 THEN cl-list.yrate = yrevRev / yroomRev.
    ELSE cl-list.yrate = 0.
  END. 

  IF rev-title1 NE "" THEN 
  DO:
    CREATE cl-list.
    cl-list.bezeich = rev-title1.
    IF droomRev NE 0 THEN cl-list.proz1 = (dpaxRev - droomRev) / droomRev * 100.
    ELSE cl-list.proz1 = 0.
    IF mroomRev NE 0 THEN cl-list.proz2 = (mpaxRev - mroomRev) / mroomRev * 100.
    ELSE cl-list.proz2 = 0.
    IF yroomRev NE 0 THEN cl-list.proz3 = (ypaxRev - yroomRev) / yroomRev * 100.
    ELSE cl-list.proz3 = 0.
  END. 
  CREATE cl-list.
END. 
 

PROCEDURE cal-umsatz1a: 
  DEFINE INPUT PARAMETER i1 AS INTEGER. 
  DEFINE INPUT PARAMETER i2 AS INTEGER. 
  DEFINE INPUT PARAMETER rev-title AS CHAR. 
  DEFINE INPUT PARAMETER rev-title1 AS CHAR. 
  DEFINE INPUT PARAMETER show-avrg AS LOGICAL. 

  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE tot-proz3   AS DECIMAL INITIAL 0 NO-UNDO.
  DEFINE VARIABLE inact       AS LOGICAL INITIAL NO.
  DEFINE VARIABLE do-it1      AS LOGICAL.

  DEFINE VARIABLE d1 AS DATE.
  DEFINE VARIABLE d2 AS DATE.
  DEFINE VARIABLE datum0 AS DATE.
  DEFINE VARIABLE datum1 AS DATE.
  DEFINE VARIABLE datum2 AS DATE.
  DEFINE VARIABLE curr-i AS INTEGER.
  DEFINE VARIABLE net-lodg    AS DECIMAL.
  DEFINE VARIABLE Fnet-lodg   AS DECIMAL.
  DEFINE VARIABLE tot-breakfast   AS DECIMAL.
  DEFINE VARIABLE tot-Lunch       AS DECIMAL.
  DEFINE VARIABLE tot-dinner      AS DECIMAL.
  DEFINE VARIABLE tot-Other       AS DECIMAL.
  DEFINE VARIABLE tot-rmrev       AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-vat         AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-service     AS DECIMAL INITIAL 0.

  DEFINE BUFFER bgenstat FOR genstat.

  d1 = from-date.
  IF to-date LT (ci-date - 1) THEN d2 = to-date.
  ELSE d2 = ci-date - 1.

  FOR EACH segment WHERE segment.betriebsnr = 0 NO-LOCK BY segment.segmentcode: 
    FIND FIRST bgenstat WHERE bgenstat.segmentcode = segment.segmentcode 
      AND bgenstat.datum GE d1 
      AND bgenstat.datum LE d2 
      AND bgenstat.resstatus NE 13 
      /* AND bgenstat.zipreis NE 0 */ /* Oscar (11/03/25) - F7C9FB - fix decrepancy with DRR because different queary */
      AND bgenstat.gratis EQ 0 
      AND bgenstat.segmentcode NE 0 
      AND bgenstat.nationnr NE 0
      AND bgenstat.zinr NE ""
      AND bgenstat.res-logic[2] NO-LOCK NO-ERROR.

    IF AVAILABLE bgenstat THEN ASSIGN do-it1 = YES.
    ELSE
    DO: 
      IF segment.bezeich MATCHES "*$$0" THEN ASSIGN do-it1 = NO.
      ELSE do-it1 = YES.
    END.

    IF do-it1 THEN
    DO:
      CREATE cl-list. 
      ASSIGN
        cl-list.segm = segment.segmentcode
        cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0")
        cl-list.betriebsnr = segment.betriebsnr
        cl-list.drev = 0
      .  
        
      FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode 
        AND genstat.datum GE d1 
        AND genstat.datum LE d2 
        AND genstat.resstatus NE 13 
        /* AND genstat.zipreis NE 0 */ /* Oscar (11/03/25) - F7C9FB - fix decrepancy with DRR because different queary */
        AND genstat.gratis EQ 0
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES /*27032012 genstat.res-logic[2] MU */
        USE-INDEX segm_ix NO-LOCK:
            
          inact = YES.

          /* Start - Oscar (28/01/25) - FD7927 - Adjust to e1-desktop */
          /*IF genstat.res-date[1] LT genstat.datum AND genstat.res-date[2] = genstat.datum 
            AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
          ELSE*/
          DO:
            IF genstat.datum = to-date THEN 
            DO:
              ASSIGN
                cl-list.droom     = cl-list.droom + 1
                cl-list.dpax      = cl-list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                cl-list.drev      = cl-list.drev + genstat.logis

                droomRev          = droomRev + 1
                dpaxRev           = dpaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. /* Oscar (07/03/25) - 89D27E - fix duplicate count on pax */
                drevRev           = drevRev + genstat.logis
              . 
            END. 
              
            IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
              OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
            DO:
              ASSIGN
                cl-list.mroom   = cl-list.mroom + 1
                cl-list.mpax    = cl-list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2. 
                cl-list.mrev    = cl-list.mrev + genstat.logis. 

                mroomRev        = mroomRev + 1. 
                mpaxRev         = mpaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2. 
                mrevRev         = mrevRev + genstat.logis. 
            END.

            ASSIGN
              cl-list.yroom   = cl-list.yroom + 1. 
              cl-list.ypax    = cl-list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2. 
              cl-list.yrev    = cl-list.yrev + genstat.logis. 
              
              yroomRev        = yroomRev + 1. 
              ypaxRev         = ypaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2. 
              yrevRev         = yrevRev + genstat.logis.
          END.
          /* End - Oscar (28/01/25) - FD7927 - Adjust to e1-desktop */
      END. /*each genstat*/
    END.    
  END.  /*each segment*/
  
  /********merge other room revenue*********/
  IF do-it THEN
  DO:
    FOR EACH genstat WHERE genstat.datum GE d1 
      AND genstat.datum LE d2  
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.resstatus NE 13
      AND genstat.res-logic[2] EQ YES /*27032012 genstat.res-logic[2] MU */
      NO-LOCK:
        FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-ERROR.
        IF AVAILABLE segment THEN   /*kl segment ada*/
        DO:
          FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
          IF AVAILABLE cl-list THEN
          DO:
            IF genstat.datum = to-date THEN 
            DO: 
              ASSIGN 
                cl-list.drev = cl-list.drev + genstat.res-deci[1]
                drevRev      = drevRev + genstat.res-deci[1]. /* Oscar (28/01/25) - FD7927 - Adjust variable */
            END.

            IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
            DO:
              ASSIGN 
                cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                mrevRev      = mrevRev + genstat.res-deci[1]. /* Oscar (28/01/25) - FD7927 - Adjust variable */
            END.
          END.
        END.
        ELSE    /*klo gada segment*/
        DO:
          FIND FIRST guestseg WHERE guestseg.gastnr EQ genstat.gastnr NO-ERROR.
          IF AVAILABLE guestseg THEN
          DO:
            IF guestseg.reihenfolge EQ 1 THEN
            DO:
              FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
              IF AVAILABLE cl-list THEN
              DO:
                IF genstat.datum = to-date THEN 
                DO: 
                  ASSIGN 
                    cl-list.drev = cl-list.drev + genstat.res-deci[1]
                    drevRev      = drevRev + genstat.res-deci[1]. /* Oscar (28/01/25) - FD7927 - Adjust variable */
                END.

                IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                  OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
                DO:
                  ASSIGN 
                    cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                    mrevRev      = mrevRev + genstat.res-deci[1]. /* Oscar (28/01/25) - FD7927 - Adjust variable */
                END.
              END.
            END.
            ELSE /* if reihenfolge ne 1*/
            DO:
              FIND FIRST guestseg WHERE guestseg.reihenfolge EQ 0 NO-ERROR.
              IF AVAILABLE guestseg THEN
              DO:
                FIND FIRST cl-list WHERE cl-list.segm EQ guestseg.segmentcode NO-ERROR.
                IF AVAILABLE cl-list THEN
                DO:
                  IF genstat.datum = to-date THEN 
                  DO: 
                    ASSIGN 
                      cl-list.drev = cl-list.drev + genstat.res-deci[1]
                      drevRev      = drevRev + genstat.res-deci[1]. /* Oscar (28/01/25) - FD7927 - Adjust variable */
                  END.

                  IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                      OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
                  DO:
                    ASSIGN 
                      cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                      mrevRev      = mrevRev + genstat.res-deci[1]. /* Oscar (28/01/25) - FD7927 - Adjust variable */
                  END.
                END.
              END.
            END.
          END.
          /* Start - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */
          /* ELSE /* not available guestseg*/
          DO: 
            FIND FIRST segment NO-ERROR. 
            IF AVAILABLE segment THEN
            DO:
              FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
              IF AVAILABLE cl-list THEN
              DO:
                IF genstat.datum = to-date THEN 
                DO: 
                  ASSIGN 
                    cl-list.drev = cl-list.drev + genstat.res-deci[1]
                    drev = drev + genstat.res-deci[1].
                  END.

                  IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                      OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
                  DO:
                    ASSIGN
                      cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                      mrev = mrev + genstat.res-deci[1].
                  END.
                END.
              END.
            END.
          END. */
          /* End - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */
        END.
    END. /* for each */

    /* Start - Oscar - (05/02/25) - FD7927-2 - Move to outside to adjust to desktop */
    /* IF to-date GE ci-date THEN 
    DO:
      ASSIGN d2 = d2 + 1.

      FOR EACH res-line WHERE ((res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        AND res-line.resstatus NE 8
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT d2))) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
        BY res-line.resnr BY res-line.reslinnr descending: 

          ASSIGN curr-i = 0.

          IF res-line.kontignr LT 0 THEN 
          DO:
            ASSIGN do-it1 = YES.
            FIND FIRST cl-list WHERE cl-list.segm EQ reservation.segmentcode NO-ERROR.
            IF NOT AVAILABLE cl-list THEN 
            DO:
              FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
              IF AVAILABLE segment AND NOT segment.bezeich MATCHES "*$$0" THEN 
              DO:
                  IF segment.betriebsnr NE 1 AND segment.betriebsnr NE 2 THEN
                  DO:
                    inact = YES.
                    
                    CREATE cl-list.
                    cl-list.compli     = NO. 
                    cl-list.segm       = segment.segmentcode. 
                    cl-list.bezeich    = segment.bezeich.
                    cl-list.betriebsnr = segment.betriebsnr.
                  END.
                  ELSE
                  DO:
                    CREATE cl-list.
                    cl-list.compli     = YES. 
                    cl-list.segm       = segment.segmentcode. 
                    cl-list.bezeich    = segment.bezeich.
                    cl-list.betriebsnr = segment.betriebsnr.
                  END.
              END.    
              ELSE ASSIGN do-it1 = NO.
            END.

            IF do-it1 = YES THEN 
            DO:
              datum1 = d2.
              IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
              datum2 = to-date. 
              IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

              DO datum0 = datum1 TO datum2:
                ASSIGN curr-i = curr-i + 1.

                IF datum0 NE res-line.abreise THEN 
                DO:
                  ASSIGN  net-lodg      = 0
                        tot-breakfast = 0
                        tot-lunch     = 0
                        tot-dinner    = 0
                        tot-other     = 0
                  . 

                  RUN get-room-breakdown.p( RECID(res-line), datum0, curr-i, from-date,
                                            OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                            OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                            OUTPUT tot-dinner, OUTPUT tot-other,
                                            OUTPUT tot-rmrev, OUTPUT tot-vat,
                                            OUTPUT tot-service).
                  
                  /* Start - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */                          
                  IF datum0 = to-date THEN 
                  DO:
                    cl-list.droom = cl-list.droom + res-line.zimmeranz. 
                    cl-list.dpax  = cl-list.dpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                    cl-list.drev  = cl-list.drev + net-lodg. 

                    IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                    DO:
                      droomRev         = droomRev + res-line.zimmeranz. 
                      drevRev          = drevRev + net-lodg.
                    END.

                    IF cl-list.betriebsnr EQ 1 THEN
                    DO:
                      droomComp = droomComp + res-line.zimmeranz.
                      dpaxComp  = dpaxComp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    END.
                    IF cl-list.betriebsnr EQ 2 THEN
                    DO:
                      droomHU = droomHU + res-line.zimmeranz.
                      dpaxHU  = dpaxHU + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    END.
                  END.

                  IF (mi-mtd-chk AND MONTH(datum0) = MONTH(to-date))
                  OR (mi-ftd-chk AND datum0 GE d2 AND datum0 LE tdate) THEN 
                  DO:
                    cl-list.mroom   = cl-list.mroom + res-line.zimmeranz. 
                    cl-list.mpax    = cl-list.mpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                    cl-list.mrev    = cl-list.mrev + net-lodg. 
                    
                    IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                    DO:
                      mroomRev           = mroomRev + res-line.zimmeranz. 
                      mpaxRev            = mpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                      mrevRev            = mrevRev + net-lodg.
                    END.
                    
                    IF cl-list.betriebsnr EQ 1 THEN
                    DO:
                      mroomComp = mroomComp + res-line.zimmeranz.
                      mpaxComp  = mpaxComp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    END.
                    IF cl-list.betriebsnr EQ 2 THEN
                    DO:
                      mroomHU = mroomHU + res-line.zimmeranz.
                      mpaxHU  = mpaxHU + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    END.
                  END.

                  ASSIGN
                    cl-list.yroom   = cl-list.yroom + res-line.zimmeranz.
                    cl-list.ypax    = cl-list.ypax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                    cl-list.yrev    = cl-list.yrev + net-lodg.
                  
                  IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                  DO:
                    yroomRev           = yroomRev + res-line.zimmeranz.
                    ypaxRev            = ypaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                    yrevRev            = yrevRev + net-lodg.
                  END.

                  IF cl-list.betriebsnr EQ 1 THEN
                  DO:
                    yroomComp = yroomComp + res-line.zimmeranz.
                    ypaxComp  = ypaxComp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  END.
                  IF cl-list.betriebsnr EQ 2 THEN
                  DO:
                    yroomHU = yroomHU + res-line.zimmeranz.
                    ypaxHU  = ypaxHU + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  END.

                  /* End - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */
                END.                                        
              END.
            END.
          END.
      END.
    END.

    /* Start - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */
    IF inact THEN
    DO:
      FOR EACH cl-list WHERE (cl-list.betriebsnr GE i1 AND cl-list.betriebsnr LE i2): 
        IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
        IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
        IF cl-list.yroom NE 0 THEN cl-list.yrate = cl-list.yrev / cl-list.yroom. 
        cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
        cl-list.proz2 = 100.0 * cl-list.mroom / mtd-act. 
        cl-list.proz3 = 100.0 * cl-list.yroom / ytd-act. 
        IF droomRev NE 0 THEN drateRev = drevRev / droomRev. 
        IF mroomRev NE 0 THEN mrateRev = mrevRev / mroomRev. 
        IF yroomRev NE 0 THEN yrateRev = yrevRev / yroomRev. 
    
        IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
        IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
        IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
     
        ASSIGN tot-proz3 = tot-proz3 + cl-list.proz3 /*ROUND(cl-list.proz3, 2).    */.
    
        /*M */
        dpaxRev = dpaxRev + cl-list.dpax.

        IF cl-list.drev EQ 0 AND cl-list.mrev EQ 0 AND cl-list.yrev EQ 0 THEN 
          cl-list.zero-flag = YES.
      END.
      CREATE cl-list.
    END.
    /* End - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */

    /* ASSIGN
      droomExc = droom
      mroomExc = mroom
      yroomExc = yroom
      droomRev = droomExc
      mroomRev = mroomExc
      yroomRev = yroomExc. */

    CREATE cl-list.

    /* Start - Oscar (28/01/25) - FD7927 - Adjust variable */ 
    CREATE cl-list.
    ASSIGN
      cl-list.bezeich = rev-title
      cl-list.droom   = droomRev
      cl-list.proz1   = droomRev / tot-room * 100
      cl-list.mroom   = mroomRev
      cl-list.proz2   = mroomRev / mtd-act * 100
      cl-list.dpax    = dpaxRev
      cl-list.mpax    = mpaxRev
      cl-list.yroom   = yroomRev
      cl-list.ypax    = ypaxRev
      cl-list.proz3   = tot-proz3
      cl-list.drev    = drevRev
      cl-list.mrev    = mrevRev
      cl-list.yrev    = yrevRev
    .

    IF show-avrg THEN 
    DO:
      IF droomRev NE 0 THEN cl-list.drate = drevRev / droomRev.
      ELSE cl-list.drate = 0.
      IF mroomRev NE 0 THEN cl-list.mrate = mrevRev / mroomRev.
      ELSE cl-list.mrate = 0.
      IF yroomRev NE 0 THEN cl-list.yrate = yrevRev / yroomRev.
      ELSE cl-list.yrate = 0.
    END.

    IF rev-title1 NE "" THEN 
    DO:
      CREATE cl-list.
      ASSIGN cl-list.bezeich = rev-title1.
      IF droomRev NE 0 THEN cl-list.proz1 = (dpaxRev - droomRev) / droomRev * 100.
      ELSE cl-list.proz1 = 0.
      IF mroomRev NE 0 THEN cl-list.proz2 = (mpaxRev - mroomRev) / mroomRev * 100.
      ELSE cl-list.proz2 = 0.
      IF yroomRev NE 0 THEN cl-list.proz3 = (ypaxRev - yroomRev) / yroomRev * 100.
      ELSE cl-list.proz3 = 0.
    END. 
    CREATE cl-list.
    /* End - Oscar (28/01/25) - FD7927 - Adjust variable */ 
    */
    /* End - Oscar - (05/02/25) - FD7927-2 - Move to outside to adjust to desktop */
  END.

  /* Start - Oscar - (05/02/25) - FD7927-2 - Move to outside to adjust to desktop */
  IF to-date GE ci-date THEN 
  DO:
    ASSIGN d2 = d2 + 1.

    FOR EACH res-line WHERE ((res-line.resstatus LE 13 
      AND res-line.resstatus NE 4
      AND res-line.resstatus NE 8
      AND res-line.resstatus NE 9 
      AND res-line.resstatus NE 10 
      AND res-line.resstatus NE 12 
      AND res-line.active-flag LE 1 
      AND NOT (res-line.ankunft GT to-date) 
      AND NOT (res-line.abreise LT d2))) OR
      (res-line.resstatus = 8 AND res-line.active-flag = 2
      AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
      AND res-line.gastnr GT 0 
      AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
      FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
      BY res-line.resnr BY res-line.reslinnr descending: 

        ASSIGN curr-i = 0.

        IF res-line.kontignr LT 0 THEN 
        DO:
          ASSIGN do-it1 = YES.
          FIND FIRST cl-list WHERE cl-list.segm EQ reservation.segmentcode NO-ERROR.
          IF NOT AVAILABLE cl-list THEN 
          DO:
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment AND NOT segment.bezeich MATCHES "*$$0" THEN 
            DO:
                IF segment.betriebsnr NE 1 AND segment.betriebsnr NE 2 THEN
                DO:
                  inact = YES.
                  
                  CREATE cl-list.
                  cl-list.compli     = NO. 
                  cl-list.segm       = segment.segmentcode. 
                  cl-list.bezeich    = segment.bezeich.
                  cl-list.betriebsnr = segment.betriebsnr.
                END.
                ELSE
                DO:
                  CREATE cl-list.
                  cl-list.compli     = YES. 
                  cl-list.segm       = segment.segmentcode. 
                  cl-list.bezeich    = segment.bezeich.
                  cl-list.betriebsnr = segment.betriebsnr.
                END.
            END.    
            ELSE ASSIGN do-it1 = NO.
          END.

          IF do-it1 = YES THEN 
          DO:
            datum1 = d2.
            IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
            datum2 = to-date. 
            IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

            DO datum0 = datum1 TO datum2:
              ASSIGN curr-i = curr-i + 1.

              IF datum0 NE res-line.abreise THEN 
              DO:
                ASSIGN  net-lodg      = 0
                      tot-breakfast = 0
                      tot-lunch     = 0
                      tot-dinner    = 0
                      tot-other     = 0
                . 

                RUN get-room-breakdown.p( RECID(res-line), datum0, curr-i, from-date,
                                          OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                          OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                          OUTPUT tot-dinner, OUTPUT tot-other,
                                          OUTPUT tot-rmrev, OUTPUT tot-vat,
                                          OUTPUT tot-service).
                
                /* Start - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */                          
                IF datum0 = to-date THEN 
                DO:
                  cl-list.droom = cl-list.droom + res-line.zimmeranz. 
                  cl-list.dpax  = cl-list.dpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                  cl-list.drev  = cl-list.drev + net-lodg. 

                  IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                  DO:
                    droomRev         = droomRev + res-line.zimmeranz. 
                    dpaxRev          = dpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix duplicate count on pax */
                    drevRev          = drevRev + net-lodg.
                  END.

                  IF cl-list.betriebsnr EQ 1 THEN
                  DO:
                    droomComp = droomComp + res-line.zimmeranz.
                    dpaxComp  = dpaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                  IF cl-list.betriebsnr EQ 2 THEN
                  DO:
                    droomHU = droomHU + res-line.zimmeranz.
                    dpaxHU  = dpaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                END.

                IF (mi-mtd-chk AND MONTH(datum0) = MONTH(to-date))
                OR (mi-ftd-chk AND datum0 GE d2 AND datum0 LE tdate) THEN 
                DO:
                  cl-list.mroom   = cl-list.mroom + res-line.zimmeranz. 
                  cl-list.mpax    = cl-list.mpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                  cl-list.mrev    = cl-list.mrev + net-lodg. 
                  
                  IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                  DO:
                    mroomRev           = mroomRev + res-line.zimmeranz. 
                    mpaxRev            = mpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                    mrevRev            = mrevRev + net-lodg.
                  END.
                  
                  IF cl-list.betriebsnr EQ 1 THEN
                  DO:
                    mroomComp = mroomComp + res-line.zimmeranz.
                    mpaxComp  = mpaxComp +  res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                  IF cl-list.betriebsnr EQ 2 THEN
                  DO:
                    mroomHU = mroomHU + res-line.zimmeranz.
                    mpaxHU  = mpaxHU +  res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                  END.
                END.

                ASSIGN
                  cl-list.yroom   = cl-list.yroom + res-line.zimmeranz.
                  cl-list.ypax    = cl-list.ypax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                  cl-list.yrev    = cl-list.yrev + net-lodg.
                
                IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                DO:
                  yroomRev           = yroomRev + res-line.zimmeranz.
                  ypaxRev            = ypaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                  yrevRev            = yrevRev + net-lodg.
                END.

                IF cl-list.betriebsnr EQ 1 THEN
                DO:
                  yroomComp = yroomComp + res-line.zimmeranz.
                  ypaxComp  = ypaxComp +  res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                END.
                IF cl-list.betriebsnr EQ 2 THEN
                DO:
                  yroomHU = yroomHU + res-line.zimmeranz.
                  ypaxHU  = ypaxHU +  res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                END.

                /* End - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */
              END.                                        
            END.
          END.
        END.
    END.
  END.

  /* Start - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */
  IF inact THEN
  DO:
    FOR EACH cl-list WHERE (cl-list.betriebsnr GE i1 AND cl-list.betriebsnr LE i2): 
      IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
      IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
      IF cl-list.yroom NE 0 THEN cl-list.yrate = cl-list.yrev / cl-list.yroom. 
      cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
      cl-list.proz2 = 100.0 * cl-list.mroom / mtd-act. 
      cl-list.proz3 = 100.0 * cl-list.yroom / ytd-act. 
      IF droomRev NE 0 THEN drateRev = drevRev / droomRev. 
      IF mroomRev NE 0 THEN mrateRev = mrevRev / mroomRev. 
      IF yroomRev NE 0 THEN yrateRev = yrevRev / yroomRev. 
  
      IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
      IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
      IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
    
      ASSIGN tot-proz3 = tot-proz3 + cl-list.proz3 /*ROUND(cl-list.proz3, 2).    */.
  
      /*M */
      /* dpaxRev = dpaxRev + cl-list.dpax. */

      IF cl-list.drev EQ 0 AND cl-list.mrev EQ 0 AND cl-list.yrev EQ 0 THEN 
        cl-list.zero-flag = YES.
    END.
    CREATE cl-list.
  END.
  /* End - Oscar (28/01/25) - FD7927 - Adjust e1-desktop */

  /* ASSIGN
    droomExc = droom
    mroomExc = mroom
    yroomExc = yroom
    droomRev = droomExc
    mroomRev = mroomExc
    yroomRev = yroomExc. */

  CREATE cl-list.

  /* Start - Oscar (28/01/25) - FD7927 - Adjust variable */ 
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = rev-title
    cl-list.droom   = droomRev
    cl-list.proz1   = droomRev / tot-room * 100
    cl-list.mroom   = mroomRev
    cl-list.proz2   = mroomRev / mtd-act * 100
    cl-list.dpax    = dpaxRev
    cl-list.mpax    = mpaxRev
    cl-list.yroom   = yroomRev
    cl-list.ypax    = ypaxRev
    cl-list.proz3   = tot-proz3
    cl-list.drev    = drevRev
    cl-list.mrev    = mrevRev
    cl-list.yrev    = yrevRev
  .

  IF show-avrg THEN 
  DO:
    IF droomRev NE 0 THEN cl-list.drate = drevRev / droomRev.
    ELSE cl-list.drate = 0.
    IF mroomRev NE 0 THEN cl-list.mrate = mrevRev / mroomRev.
    ELSE cl-list.mrate = 0.
    IF yroomRev NE 0 THEN cl-list.yrate = yrevRev / yroomRev.
    ELSE cl-list.yrate = 0.
  END.

  IF rev-title1 NE "" THEN 
  DO:
    CREATE cl-list.
    ASSIGN cl-list.bezeich = rev-title1.
    IF droomRev NE 0 THEN cl-list.proz1 = (dpaxRev - droomRev) / droomRev * 100.
    ELSE cl-list.proz1 = 0.
    IF mroomRev NE 0 THEN cl-list.proz2 = (mpaxRev - mroomRev) / mroomRev * 100.
    ELSE cl-list.proz2 = 0.
    IF yroomRev NE 0 THEN cl-list.proz3 = (ypaxRev - yroomRev) / yroomRev * 100.
    ELSE cl-list.proz3 = 0.
  END. 
  CREATE cl-list.
  /* End - Oscar (28/01/25) - FD7927 - Adjust variable */ 
  /* End - Oscar - (05/02/25) - FD7927-2 - Move to outside to adjust to desktop */
END. 


PROCEDURE cal-umsatz1b: 
  DEFINE INPUT PARAMETER i1 AS INTEGER. 
  DEFINE INPUT PARAMETER i2 AS INTEGER. 
  DEFINE INPUT PARAMETER rev-title AS CHAR. 
  DEFINE INPUT PARAMETER rev-title1 AS CHAR. 
  DEFINE INPUT PARAMETER show-avrg AS LOGICAL. 

  DEFINE VARIABLE i             AS INTEGER. 
  DEFINE VARIABLE datum         AS DATE. 
  DEFINE VARIABLE inact         AS LOGICAL INITIAL NO.
  DEFINE VARIABLE do-it1        AS LOGICAL.
  DEFINE VARIABLE d1            AS DATE.
  DEFINE VARIABLE d2            AS DATE.
  DEFINE VARIABLE datum0        AS DATE.
  DEFINE VARIABLE datum1        AS DATE.
  DEFINE VARIABLE datum2        AS DATE.
  DEFINE VARIABLE curr-i        AS INTEGER.
  DEFINE VARIABLE net-lodg      AS DECIMAL.
  DEFINE VARIABLE Fnet-lodg     AS DECIMAL.
  DEFINE VARIABLE tot-breakfast AS DECIMAL.
  DEFINE VARIABLE tot-Lunch     AS DECIMAL.
  DEFINE VARIABLE tot-dinner    AS DECIMAL.
  DEFINE VARIABLE tot-Other     AS DECIMAL.
  DEFINE VARIABLE tot-rmrev     AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-vat       AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-service   AS DECIMAL INITIAL 0.

  DEFINE BUFFER bgenstat FOR genstat.

  d1 = from-date.
  IF to-date LT (ci-date - 1) THEN d2 = to-date.
  ELSE d2 = ci-date - 1.

  FOR EACH segment NO-LOCK BY segment.segmentcode:      
    FIND FIRST bgenstat WHERE bgenstat.segmentcode = segment.segmentcode 
        AND bgenstat.datum GE d1 
        AND bgenstat.datum LE d2 
        AND bgenstat.resstatus NE 13 
        AND bgenstat.gratis NE 0 
        AND bgenstat.segmentcode NE 0 
        AND bgenstat.nationnr NE 0
        AND bgenstat.zinr NE ""
        AND bgenstat.res-logic[2] NO-LOCK NO-ERROR.
    IF AVAILABLE bgenstat THEN ASSIGN do-it1 = YES.
    ELSE DO: 
        IF segment.bezeich MATCHES "*$$0" THEN ASSIGN do-it1 = NO.
        ELSE do-it1 = YES.
    END.

    IF do-it1 THEN 
    DO:
        FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode  /*House Use*/
            AND genstat.datum GE d1 
            AND genstat.datum LE d2 
            AND genstat.resstatus NE 13 
            AND genstat.gratis NE 0 /*FT 151214*/
            AND genstat.segmentcode NE 0 
            AND genstat.nationnr NE 0
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] EQ YES /*27032012 genstat.res-logic[2] MU */
            USE-INDEX segm_ix NO-LOCK : 

              inact = YES.
              FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode 
                AND cl-list.compli = YES NO-LOCK NO-ERROR. 
              IF NOT AVAILABLE cl-list THEN 
              DO: 
                CREATE cl-list. 
                cl-list.compli = YES. 
                cl-list.segm = segment.segmentcode. 
                cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0"). 
                cl-list.betriebsnr = segment.betriebsnr. 
              END. 
    
              /* Start - Oscar (28/01/25) - FD7927 - Adjust to e1-desktop version */ 
              /*IF genstat.res-date[1] LT genstat.datum AND genstat.res-date[2] = genstat.datum 
                AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
              ELSE*/
              DO:
                IF genstat.datum = to-date THEN 
                DO:
                  cl-list.droom = cl-list.droom + 1.
                  cl-list.dpax  = cl-list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  
                  IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                  DO:
                    droomRev = droomRev + 1. 
                    dpaxRev = dpaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. /* Oscar (07/03/25) - 89D27E - fix duplicate count on pax */
                  END.

                  IF cl-list.betriebsnr EQ 1 THEN
                  DO:
                    droomComp = droomComp + 1.
                    dpaxComp  = dpaxComp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  END.
                  IF cl-list.betriebsnr EQ 2 THEN
                  DO:
                    droomHU = droomHU + 1.
                    dpaxHU  = dpaxHU + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  END.
                  /*M dpax          = dpax + genstat.gratis + genstat.erwachs 
                                  + genstat.kind1 + genstat.kind2.  */
                END. 
               
                IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(d2))
                    OR (mi-ftd-chk AND genstat.datum GE d1 AND genstat.datum LE d2) THEN
                DO:
                    cl-list.mroom   = cl-list.mroom + 1. 
                    cl-list.mpax    = cl-list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
      
                    IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                    DO:
                      mroomRev = mroomRev + 1. 
                      mpaxRev  = mpaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
                    END.
                    
                    IF cl-list.betriebsnr EQ 1 THEN
                    DO:
                      mroomComp = mroomComp + 1.
                      mpaxComp  = mpaxComp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    END.
                    IF cl-list.betriebsnr EQ 2 THEN
                    DO:
                      mroomHU = mroomHU + 1.
                      mpaxHU  = mpaxHU + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    END.
                END.
                ASSIGN
                    cl-list.yroom   = cl-list.yroom + 1  /*House use*/
                    cl-list.ypax    = cl-list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                
                IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                DO:
                  yroomRev = yroomRev + 1. 
                  ypaxRev  = ypaxRev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
                END.

                IF cl-list.betriebsnr EQ 1 THEN
                DO:
                  yroomComp = yroomComp + 1.
                  ypaxComp  = ypaxComp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                END.
                IF cl-list.betriebsnr EQ 2 THEN
                DO:
                  yroomHU = yroomHU + 1.
                  ypaxHU  = ypaxHU + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                END.
                /* End - Oscar (28/01/25) - FD7927 - Adjust to e1-desktop version */ 
              END.
        END.
    END.       
  END. 

  /* Start - Oscar (28/01/25) - FD7927 - comment because already done in cal-umsatz1a to prevent duplicate */ 
  /* 
  IF to-date GE ci-date THEN 
  DO:
      ASSIGN d2 = d2 + 1.

      FOR EACH res-line WHERE ((res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        AND res-line.resstatus NE 8
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT d2))) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
        BY res-line.resnr BY res-line.reslinnr descending: 

        ASSIGN curr-i = 0.

        IF res-line.kontignr LT 0 THEN DO:
            ASSIGN do-it1 = YES.
            FIND FIRST cl-list WHERE cl-list.segm EQ reservation.segmentcode NO-ERROR.
            IF NOT AVAILABLE cl-list THEN DO:
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode 
                    NO-LOCK NO-ERROR.
                IF AVAILABLE segment AND NOT segment.bezeich MATCHES "*$$0" THEN DO:
                    CREATE cl-list. 
                    cl-list.segm    = segment.segmentcode. 
                    cl-list.bezeich = segment.bezeich.
                END.    
                ELSE ASSIGN do-it1 = NO.
            END.

            IF do-it1 = YES THEN DO:
                datum1 = d2.
                IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
                datum2 = to-date. 
                IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

                DO datum0 = datum1 TO datum2:
                    ASSIGN curr-i = curr-i + 1.

                    IF datum0 = res-line.abreise THEN .
                    ELSE DO:

                        ASSIGN net-lodg      = 0
                               tot-breakfast = 0
                               tot-lunch     = 0
                               tot-dinner    = 0
                               tot-other     = 0
                         . 

                        RUN get-room-breakdown.p(RECID(res-line), datum0, curr-i, from-date,
                                                 OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                 OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                 OUTPUT tot-dinner, OUTPUT tot-other,
                                                 OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                 OUTPUT tot-service).    

                        IF datum0 = to-date THEN DO:
                            droom         = droom + res-line.zimmeranz. 
                            cl-list.droom = cl-list.droom + res-line.zimmeranz. 
                            cl-list.dpax  = cl-list.dpax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis. 
                            cl-list.drev  = cl-list.drev + net-lodg. 
                            drev          = drev + net-lodg.
                        END.

                        IF (mi-mtd-chk AND MONTH(datum0) = MONTH(to-date))
                            OR (mi-ftd-chk AND datum0 GE d2 AND datum0 LE tdate) THEN DO:

                            cl-list.mroom   = cl-list.mroom + res-line.zimmeranz. 
                            cl-list.mpax    = cl-list.mpax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis. 
                            cl-list.mrev    = cl-list.mrev + net-lodg. 
                            mroom           = mroom + res-line.zimmeranz. 
                            mpax            = mpax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis. 
                            mrev            = mrev + net-lodg.                            
                        END.

                        ASSIGN
                            cl-list.yroom   = cl-list.yroom + res-line.zimmeranz
                            cl-list.ypax    = cl-list.ypax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis
                            cl-list.yrev    = cl-list.yrev + net-lodg
                            yroom           = yroom + res-line.zimmeranz
                            ypax            = ypax + res-line.erwachs + res-line.kind1 
                                              + res-line.kind2 + res-line.gratis
                            yrev            = yrev + net-lodg. 
                    END.                                        
                END.
            END.
        END.
      END.
  END.
  */
  /* End - Oscar (28/01/25) - FD7927 - comment because already done in cal-umsatz1a to prevent duplicate */

  /* Start - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
  IF inact THEN
  DO:
  
      FOR EACH cl-list WHERE cl-list.compli = YES : 
        IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
        IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
        IF cl-list.yroom NE 0 THEN cl-list.yrate = cl-list.yrev / cl-list.yroom. 
        cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
        cl-list.proz2 = 100.0 * cl-list.mroom / /*(tot-room * day(to-date))*/ mtd-act. 
        cl-list.proz3 = 100.0 * cl-list.yroom / /*(tot-room * day(to-date))*/ ytd-act. 
        /* IF droom NE 0 THEN drate = drev / droom. 
        IF mroom NE 0 THEN mrate = mrev / mroom. 
        IF yroom NE 0 THEN yrate = yrev / yroom. */
    
        IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
        IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
        IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
     
        /*M */
        /* dpaxRev = dpaxRev + cl-list.dpax. */
      END. 

      CREATE cl-list.
  END.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = rev-title
    cl-list.droom = droomRev + droomComp + droomHU
    cl-list.proz1 = (droomRev + droomComp + droomHU) / tot-room * 100
    cl-list.mroom = mroomRev + mroomComp + mroomHU
    cl-list.proz2 = (mroomRev + mroomComp + mroomHU) / mtd-act * 100
    cl-list.dpax = dpaxRev + dpaxComp + dpaxHU
    cl-list.mpax = mpaxRev + mpaxComp + mpaxHU
    cl-list.yroom = yroomRev + yroomComp + yroomHU
    cl-list.ypax = ypaxRev + ypaxComp + ypaxHU
    cl-list.proz3 = (yroomRev + yroomComp + yroomHU) / ytd-act * 100
    cl-list.drev = drevRev
    cl-list.mrev = mrevRev
    cl-list.yrev = yrevRev
  .

  IF show-avrg THEN 
  DO:
    IF (droomRev + droomComp + droomHU) NE 0 THEN cl-list.drate = drevRev / (droomRev + droomComp + droomHU).
    ELSE cl-list.drate = 0.
    IF (mroomRev + mroomComp + mroomHU) NE 0 THEN cl-list.mrate = mrevRev / (mroomRev + mroomComp + mroomHU).
    ELSE cl-list.mrate = 0.
    IF (yroomRev + yroomComp + yroomHU) NE 0 THEN cl-list.yrate = yrevRev / (yroomRev + yroomComp + yroomHU).
    ELSE cl-list.yrate = 0.
  END.

  IF rev-title1 NE "" THEN 
  DO: 
    CREATE cl-list.
    ASSIGN
      cl-list.bezeich = rev-title1.
    IF (droomRev + droomComp + droomHU) NE 0 THEN cl-list.proz1 = ((dpaxRev + dpaxComp + dpaxHU) - (droomRev + droomComp + droomHU)) / (droomRev + droomComp + droomHU) * 100.
    ELSE cl-list.proz1 = 0.
    IF (mroomRev + mroomComp + mroomHU) NE 0 THEN cl-list.proz2 = ((mpaxRev + mpaxComp + mpaxHU) - (mroomRev + mroomComp + mroomHU)) / (mroomRev + mroomComp + mroomHU) * 100.
    ELSE cl-list.proz2 = 0.
    IF (yroomRev + yroomComp + yroomHU) NE 0 THEN cl-list.proz3 = ((ypaxRev + ypaxComp + ypaxHU) - (yroomRev + yroomComp + yroomHU)) / (yroomRev + yroomComp + yroomHU) * 100.
    ELSE cl-list.proz3 = 0.
  END. 
  CREATE cl-list.

  /* End - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
END. 


PROCEDURE cal-umsatz2: 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE datum1 AS DATE.

  dooo = 0. 
  mooo = 0.
  yooo = 0.

  DO datum = from-date TO to-date: 
    IF to-date LT ci-date THEN ASSIGN datum1 = to-date.
    ELSE ASSIGN datum1 = (ci-date - 1).

    FIND FIRST zinrstat WHERE zinrstat.datum = datum 
      AND zinrstat.zinr = "ooo" NO-LOCK NO-ERROR. 
    IF AVAILABLE zinrstat THEN 
    DO: 
      IF datum = to-date THEN dooo = zinrstat.zimmeranz. 
      IF (mi-mtd-chk AND MONTH(zinrstat.datum) = MONTH(datum1))
          OR (mi-ftd-chk AND zinrstat.datum GE fdate AND zinrstat.datum LE datum1) THEN
              mooo = mooo + zinrstat.zimmeranz.
      yooo = yooo + zinrstat.zimmeranz.
    END. 

    /* Start - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
    /* 
    IF datum GE ci-date THEN 
    DO:
        FOR EACH outorder WHERE (outorder.gespstart GE datum AND outorder.gespstart LE datum) 
            OR (outorder.gespstart LE datum AND outorder.gespende GE datum) NO-LOCK,
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK:

              IF datum = to-date THEN dooo = dooo + 1. 
              IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date)) THEN 
                  mooo = mooo + 1.
              yooo = yooo + 1.

        END.
    END.
    */

    IF datum GE ci-date THEN
    DO:
      FOR EACH outorder WHERE 
        (outorder.gespstart GE datum AND outorder.gespstart LE datum AND outorder.betriebsnr LE 1) 
        OR (outorder.gespstart LE datum AND outorder.gespende GE datum AND outorder.betriebsnr LE 1) 
        NO-LOCK,
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK:
      
        IF datum = to-date THEN dooo = dooo + 1. 
        
        FIND FIRST om-list WHERE om-list.zinr EQ outorder.zinr 
            AND om-list.gespstart EQ outorder.gespstart
            AND om-list.gespende EQ outorder.gespende NO-LOCK NO-ERROR.
        IF NOT AVAILABLE om-list THEN
        DO:
            CREATE om-list.
            om-list.zinr = outorder.zinr.           
            om-list.gespstart = outorder.gespstart.      
            om-list.gespende = outorder.gespende.
        
            mooo = mooo + 1.
            yooo = yooo + 1.
        END.  
      END.
    END.

    /* End - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
  END. 
  
  dvacant = tot-room - dooo - (droomRev + droomComp + droomHU).
  mvacant = mtd-act - mooo - (mroomRev + mroomComp + mroomHU).
  yvacant = ytd-act - yooo - (yroomRev + yroomComp + yroomHU).
  
  IF to-date = opening-date THEN 
  DO:
      mvacant = dvacant.
      yvacant = dvacant.
      mooo = dooo.
      yooo = dooo.
  END.
  
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "V A C A N T"
    cl-list.droom = dvacant
    cl-list.proz1 = dvacant / tot-room * 100
    cl-list.mroom = mvacant
    cl-list.proz2 = mvacant / mtd-act * 100
    cl-list.yroom = yvacant
    cl-list.proz3 = yvacant / ytd-act * 100.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "Out Of Order"
    cl-list.droom = dooo
    cl-list.proz1 = dooo / tot-room * 100
    cl-list.mroom = mooo
    cl-list.proz2 = mooo / mtd-act * 100
    cl-list.yroom = yooo
    cl-list.proz3 = yooo / ytd-act * 100.

  CREATE cl-list.

  IF to-date LT ci-date THEN DO:
    FIND FIRST zinrstat WHERE zinrstat.zinr = "tot-rm" AND zinrstat.datum = to-date NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN all-room = zinrstat.zimmeranz.
  END.
  ELSE DO:
    FOR EACH zimmer NO-LOCK:
      ASSIGN all-room = all-room + 1.
    END.
  END.
  
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "# Active Rooms"
    cl-list.droom = tot-room
    cl-list.proz1 = 100
    cl-list.mroom = mtd-act
    cl-list.proz2 = 100
    cl-list.yroom = ytd-act
    cl-list.proz3 = 100.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "Inactive Rooms"
    cl-list.droom = all-room - tot-room
    cl-list.mroom = mtd-totrm - mtd-act
    cl-list.yroom = ytd-totrm - ytd-act.
      
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "Total Rooms"
    cl-list.droom = all-room
    cl-list.mroom = mtd-totrm
    cl-list.yroom = ytd-totrm
  .
  CREATE cl-list.
END. 
 

PROCEDURE cal-umsatz3: 
  DEFINE VARIABLE i            AS INTEGER. 
  DEFINE VARIABLE max-i        AS INTEGER INITIAL 0.
  DEFINE VARIABLE datum        AS DATE. 
  DEFINE VARIABLE art-list     AS INTEGER EXTENT 150. 
  DEFINE VARIABLE serv-vat     AS LOGICAL. 
  DEFINE VARIABLE fact         AS DECIMAL. 
  DEFINE VARIABLE serv         AS DECIMAL. 
  DEFINE VARIABLE vat          AS DECIMAL.
  DEFINE VARIABLE drev-droom   AS DECIMAL.
  DEFINE VARIABLE mrev-mroom   AS DECIMAL.
  DEFINE VARIABLE yrev-yroom   AS DECIMAL.
  /*MT 31/05/13 */ 
  DEFINE VARIABLE drev-droom1  AS DECIMAL.
  DEFINE VARIABLE mrev-mroom1  AS DECIMAL.
  DEFINE VARIABLE yrev-yroom1  AS DECIMAL.
  DEFINE VARIABLE compli-count AS DECIMAL.
  DEFINE VARIABLE state-str    AS CHARACTER.


  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH artikel WHERE artikel.departement = 0
      AND artikel.artart = 0 AND artikel.umsatzart = 1 NO-LOCK 
      BY artikel.artnr:
          max-i = max-i + 1.
          art-list[max-i] = artikel.artnr.
  END.

  do-it = YES.

  IF do-it THEN
  DO:
      DO i = 1 TO max-i: 
        FIND FIRST artikel WHERE artikel.artnr = art-list[i] 
          AND artikel.departement = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN 
        DO: 
          CREATE cl-list. 
          cl-list.segm = artikel.artnr. 
          IF i GE 10 THEN /*M give limitation 15.09.10*/
              cl-list.bezeich = translateExtended ("Other RmRev",lvCAREA,"").  
          ELSE 
              cl-list.bezeich = artikel.bezeich. 
         
          DO datum = from-date TO to-date: 
          serv = 0. 
          vat = 0. 
            FOR EACH umsatz WHERE umsatz.artnr = artikel.artnr 
              AND umsatz.departement = artikel.departement 
              AND umsatz.datum EQ datum NO-LOCK: 
    
              RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                 artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                fact = 1.00 + serv + vat. 
    
              IF datum = to-date THEN 
              DO: 
                drevRev = drevRev + umsatz.betrag / fact. 
                cl-list.drev = umsatz.betrag / fact. 
              END. 
              
              IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
                OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
    
              DO:
                  mrevRev = mrevRev + umsatz.betrag / fact. 
                  cl-list.mrev = cl-list.mrev + umsatz.betrag / fact. 
              END.
              ASSIGN
                  yrevRev = yrevRev + umsatz.betrag / fact. 
                  cl-list.yrev = cl-list.yrev + umsatz.betrag / fact. 
            END. 
          END. 
          IF cl-list.mrev = 0 THEN 
          DO:
              cl-list.bezeich = "Deleted".
          END.
        END. 
      END. 
      CREATE cl-list.
  END.
 
  /* Start - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
  drev-droom  = drevRev / (droomRev + droomHU + droomComp).
  IF drev-droom EQ ? THEN drev-droom = 0.

  mrev-mroom  = mrevRev / (mroomRev + mroomHU + mroomComp).        /*MT 31/05/13 */
  IF mrev-mroom EQ ? THEN mrev-mroom = 0.

  yrev-yroom  = yrevRev / (yroomRev + yroomHU + yroomComp).
  IF yrev-yroom EQ ? THEN yrev-yroom = 0.

  IF NOT mi-excHU-chk THEN
    ASSIGN
      droomRev = droomRev + droomHU
      mroomRev = mroomRev + mroomHU
      yroomRev = yroomRev + yroomHU.

  IF NOT mi-excComp-chk THEN
    ASSIGN
      droomRev = droomRev + droomComp
      mroomRev = mroomRev + mroomComp
      yroomRev = yroomRev + yroomComp.
  
  drev-droom1  = drevRev / droomRev.        /*MT 31/05/13 */
  IF drev-droom1 EQ ? THEN drev-droom1 = 0.
  
  mrev-mroom1  = mrevRev / mroomRev.        /*MT 31/05/13 */
  IF mrev-mroom1 EQ ? THEN mrev-mroom1 = 0.

  yrev-yroom1  = yrevRev / yroomRev.
  IF yrev-yroom1 EQ ? THEN yrev-yroom1 = 0.

  IF mi-excHU-chk AND mi-excComp-chk THEN
    state-str = translateExtended ("RmRev Exc Comp&HU",lvCAREA,"").
  ELSE IF mi-excHU-chk THEN
    state-str = translateExtended ("RmRev Exc HU",lvCAREA,"").
  ELSE IF mi-excComp-chk THEN
    state-str = translateExtended ("RmRev Exc Comp",lvCAREA,"").
  ELSE
    state-str = "".
  
  IF NOT long-digit THEN
  DO:
    CREATE cl-list.
    ASSIGN
      cl-list.bezeich = "RmRev Inc All"
      cl-list.drate   = drev-droom
      cl-list.mrate   = mrev-mroom
      cl-list.drev    = drevRev
      cl-list.mrev    = mrevRev
      cl-list.yrev    = yrevRev
      cl-list.yrate   = yrev-yroom.

    CREATE cl-list.
    IF mi-excHU-chk OR mi-excComp-chk THEN
    DO:
      ASSIGN
        cl-list.bezeich = state-str
        cl-list.drate = drev-droom1
        cl-list.mrate = mrev-mroom1
        cl-list.drev  = drevRev
        cl-list.mrev  = mrevRev
        cl-list.yrev  = yrevRev
        cl-list.yrate = yrev-yroom1.
    END.
  END.
  ELSE
  DO:
    CREATE cl-list.
    ASSIGN
      cl-list.bezeich = "RmRev Inc All"
      cl-list.drate   = drev-droom
      cl-list.mrate   = mrev-mroom
      cl-list.drev    = drevRev
      cl-list.mrev    = mrevRev
      cl-list.yrev    = yrevRev
      cl-list.yrate   = yrev-yroom.

    CREATE cl-list.
    IF mi-excHU-chk OR mi-excComp-chk THEN
    DO:
      ASSIGN
        cl-list.bezeich = state-str
        cl-list.drate = drev-droom1
        cl-list.mrate = mrev-mroom1
        cl-list.drev  = drevRev
        cl-list.mrev  = mrevRev
        cl-list.yrev  = yrevRev
        cl-list.yrate = yrev-yroom1.
    END.
  END.

  /* End - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */

  CREATE cl-list.
END. 
 

PROCEDURE no-show: 
  DEFINE VARIABLE i AS INTEGER. 
  dnoshow = 0. 
  dcancel = 0. 
  mnoshow = 0. 
  mcancel = 0. 
  FOR EACH zinrstat NO-LOCK WHERE 
    zinrstat.zinr = "No-Show"   AND 
    zinrstat.datum GE from-date AND
    zinrstat.datum LE to-date:
    IF zinrstat.datum = to-date THEN dnoshow = dnoshow + zinrstat.zimmeranz.
    
    IF (mi-mtd-chk AND MONTH(zinrstat.datum) = MONTH(to-date))
            OR (mi-ftd-chk AND zinrstat.datum GE fdate AND zinrstat.datum LE tdate) THEN
        mnoshow = mnoshow + zinrstat.zimmeranz.
    ynoshow = ynoshow + zinrstat.zimmeranz.
  END.
  FOR EACH zinrstat NO-LOCK WHERE 
    zinrstat.zinr = "CancRes"   AND 
    zinrstat.datum GE from-date AND
    zinrstat.datum LE to-date:
    IF zinrstat.datum = to-date THEN dcancel = dcancel + zinrstat.zimmeranz.
    IF MONTH(zinrstat.datum) = MONTH(to-date) THEN ASSIGN mcancel = mcancel + zinrstat.zimmeranz. /* Malik serverless : MONTH(datum) -> MONTH(zinrstat.datum) */
    ycancel = ycancel + zinrstat.zimmeranz.
  END.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "NO SHOW"
    cl-list.droom = dnoshow
    cl-list.mroom = mnoshow
    cl-list.yroom = ynoshow.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "C A N C E L"
    cl-list.droom = dcancel
    cl-list.mroom = mcancel
    cl-list.yroom = ycancel.  
  
  CREATE cl-list.
END. 

PROCEDURE cal-umsatz4: 
  DEFINE INPUT PARAMETER i1 AS INTEGER. 
  DEFINE INPUT PARAMETER i2 AS INTEGER. 
  DEFINE INPUT PARAMETER i3 AS INTEGER. 
  DEFINE INPUT PARAMETER i4 AS INTEGER. 
  DEFINE INPUT PARAMETER rev-title AS CHAR. 
  DEFINE INPUT PARAMETER rev-title1 AS CHAR. 
  DEFINE INPUT PARAMETER show-avrg AS LOGICAL. 

  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE datum  AS DATE. 
  DEFINE VARIABLE do-it1 AS LOGICAL.
  DEFINE VARIABLE d1 AS DATE.
  DEFINE VARIABLE d2 AS DATE.
  DEFINE VARIABLE datum0 AS DATE.
  DEFINE VARIABLE datum1 AS DATE.
  DEFINE VARIABLE datum2 AS DATE.
  DEFINE VARIABLE curr-i AS INTEGER.
  DEFINE VARIABLE net-lodg    AS DECIMAL.
  DEFINE VARIABLE Fnet-lodg   AS DECIMAL.
  DEFINE VARIABLE tot-breakfast   AS DECIMAL.
  DEFINE VARIABLE tot-Lunch       AS DECIMAL.
  DEFINE VARIABLE tot-dinner      AS DECIMAL.
  DEFINE VARIABLE tot-Other       AS DECIMAL.
  DEFINE VARIABLE tot-rmrev       AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-vat         AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-service     AS DECIMAL INITIAL 0.

  DEFINE BUFFER bgenstat FOR genstat.

  IF NOT cal-umsatz4-called THEN
  DO:
      ASSIGN d2 = from-date.

      FOR EACH res-line WHERE ((res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        AND res-line.resstatus NE 8
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT d2))) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
        BY res-line.resnr BY res-line.reslinnr descending: 

          ASSIGN curr-i = 0.

          IF res-line.kontignr LT 0 THEN 
          DO:
              ASSIGN do-it1 = YES.
              FIND FIRST cl-list WHERE cl-list.segm EQ reservation.segmentcode NO-ERROR.
              IF NOT AVAILABLE cl-list THEN 
              DO:
                  FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                  IF AVAILABLE segment AND NOT segment.bezeich MATCHES "*$$0" THEN 
                  DO:
                    IF segment.betriebsnr NE 1 AND segment.betriebsnr NE 2 THEN
                    DO:
                      CREATE cl-list.
                      cl-list.compli     = NO. 
                      cl-list.segm       = segment.segmentcode. 
                      cl-list.bezeich    = segment.bezeich.
                      cl-list.betriebsnr = segment.betriebsnr.
                    END.
                    ELSE
                    DO:
                      CREATE cl-list.
                      cl-list.compli     = YES. 
                      cl-list.segm       = segment.segmentcode. 
                      cl-list.bezeich    = segment.bezeich.
                      cl-list.betriebsnr = segment.betriebsnr.
                    END.
                  END.    
                  ELSE ASSIGN do-it1 = NO.
              END.

              IF do-it1 = YES THEN DO:
                  datum1 = d2.
                  IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
                  datum2 = to-date. 
                  IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

                  DO datum0 = datum1 TO datum2:
                      ASSIGN curr-i = curr-i + 1.

                      IF datum0 = res-line.abreise THEN .
                      ELSE DO:

                          ASSIGN net-lodg      = 0
                                tot-breakfast = 0
                                tot-lunch     = 0
                                tot-dinner    = 0
                                tot-other     = 0
                          . 

                          RUN get-room-breakdown.p(RECID(res-line), datum0, curr-i, from-date,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).    

                          /* Start - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
                          IF datum0 = to-date THEN 
                          DO:
                            cl-list.droom = cl-list.droom + res-line.zimmeranz. 
                            cl-list.dpax  = cl-list.dpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                            cl-list.drev  = cl-list.drev + net-lodg. 
          
                            IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                            DO:
                              droomRev         = droomRev + res-line.zimmeranz. 
                              dpaxRev          = dpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix duplicate count on pax */
                              drevRev          = drevRev + net-lodg.
                            END.
          
                            IF cl-list.betriebsnr EQ 1 THEN
                            DO:
                              droomComp = droomComp + res-line.zimmeranz.
                              dpaxComp  = dpaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                            IF cl-list.betriebsnr EQ 2 THEN
                            DO:
                              droomHU = droomHU + res-line.zimmeranz.
                              dpaxHU  = dpaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                          END.

                          IF (mi-mtd-chk AND MONTH(datum0) = MONTH(to-date))
                            OR (mi-ftd-chk AND datum0 GE d2 AND datum0 LE tdate) THEN 
                          DO:
                            cl-list.mroom   = cl-list.mroom + res-line.zimmeranz. 
                            cl-list.mpax    = cl-list.mpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                            cl-list.mrev    = cl-list.mrev + net-lodg. 
                            
                            IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                            DO:
                              mroomRev           = mroomRev + res-line.zimmeranz. 
                              mpaxRev            = mpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                              mrevRev            = mrevRev + net-lodg.
                            END.
                            
                            IF cl-list.betriebsnr EQ 1 THEN
                            DO:
                              mroomComp = mroomComp + res-line.zimmeranz.
                              mpaxComp  = mpaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                            IF cl-list.betriebsnr EQ 2 THEN
                            DO:
                              mroomHU = mroomHU + res-line.zimmeranz.
                              mpaxHU  = mpaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                          END.

                          ASSIGN
                            cl-list.yroom   = cl-list.yroom + res-line.zimmeranz.
                            cl-list.ypax    = cl-list.ypax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                            cl-list.yrev    = cl-list.yrev + net-lodg.
                          
                          IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                          DO:
                            yroomRev           = yroomRev + res-line.zimmeranz.
                            ypaxRev            = ypaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                            yrevRev            = yrevRev + net-lodg.
                          END.
          
                          IF cl-list.betriebsnr EQ 1 THEN
                          DO:
                            yroomComp = yroomComp + res-line.zimmeranz.
                            ypaxComp  = ypaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                          END.
                          IF cl-list.betriebsnr EQ 2 THEN
                          DO:
                            yroomHU = yroomHU + res-line.zimmeranz.
                            ypaxHU  = ypaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                          END. 

                          /* End - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
                      END.                                        
                  END.
              END.
          END.
      END.

      cal-umsatz4-called = YES.
  END.

  FOR EACH cl-list WHERE ((cl-list.segm GE i1 AND cl-list.segm LE i2) 
    OR (cl-list.segm GE i3 AND cl-list.segm LE i4)): 
      IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
      IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
      cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
      cl-list.proz2 = 100.0 * cl-list.mroom / /*(tot-room * day(to-date))*/ mtd-act. 
      cl-list.proz3 = 100.0 * cl-list.yroom / /*(tot-room * day(to-date))*/ ytd-act. 
      IF droomRev NE 0 THEN drateRev = drevRev / droomRev. 
      IF mroomRev NE 0 THEN mrateRev = mrevRev / mroomRev. 
      IF yroomRev NE 0 THEN yrateRev = yrevRev / yroomRev. 
  
      IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
      IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
      IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
 
      /* dpaxRev = dpaxRev + cl-list.dpax. */
    IF cl-list.drev EQ 0 AND cl-list.mrev EQ 0 AND cl-list.yrev EQ 0 THEN 
      cl-list.zero-flag = YES.
  END. 

  CREATE cl-list.
  
  /* Start - Oscar (28/01/25) - FD7927 - adjust variable */
  CREATE cl-list.
  ASSIGN 
    cl-list.bezeich = STRING(rev-title,"x(16)")
    cl-list.droom = droomRev
    cl-list.proz1 = droomRev / tot-room * 100
    cl-list.mroom = mroomRev
    cl-list.proz2 = mroomRev / mtd-act * 100
    cl-list.dpax = dpaxRev
    cl-list.mpax = mpaxRev
    cl-list.yroom = yroomRev
    cl-list.ypax = ypaxRev
    cl-list.proz3 = ytd-act * 100
    cl-list.drev = drevRev
    cl-list.mrev = mrevRev
    cl-list.yrev = yrevRev
  .
  
  IF show-avrg THEN 
  DO: 
    IF droomRev NE 0 THEN cl-list.drate = drevRev / droomRev.
    ELSE cl-list.drate = 0.
    IF mroomRev NE 0 THEN cl-list.mrate = mrevRev / mroomRev.
    ELSE cl-list.mrate = 0.
    IF yroomRev NE 0 THEN cl-list.yrate = yrevRev / yroomRev.
    ELSE cl-list.yrate = 0.
  END. 

  IF rev-title1 NE "" THEN 
  DO: 
    CREATE cl-list.
    ASSIGN cl-list.bezeich = rev-title1.
    IF droomRev NE 0 THEN cl-list.proz1 = (dpaxRev - droomRev) / droomRev * 100.
    ELSE cl-list.proz1 = 0.
    IF mroomRev NE 0 THEN cl-list.proz2 = (mpaxRev - mroomRev) / mroomRev * 100.
    ELSE cl-list.proz2 = 0.
    IF yroomRev NE 0 THEN cl-list.proz3 = (ypaxRev - yroomRev) / yroomRev * 100.
    ELSE cl-list.proz3 = 0.
  END. 

  CREATE cl-list.
  /* Start - Oscar (28/01/25) - FD7927 - adjust variable */
END. 
 

PROCEDURE cal-umsatz4a: 
  DEFINE INPUT PARAMETER i1 AS INTEGER. 
  DEFINE INPUT PARAMETER i2 AS INTEGER. 
  DEFINE INPUT PARAMETER rev-title AS CHAR. 
  DEFINE INPUT PARAMETER rev-title1 AS CHAR. 
  DEFINE INPUT PARAMETER show-avrg AS LOGICAL. 

  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE tot-proz3   AS DECIMAL INITIAL 0 NO-UNDO.
  DEFINE VARIABLE inact       AS LOGICAL INITIAL NO.
  DEFINE VARIABLE do-it1      AS LOGICAL.

  DEFINE VARIABLE d1            AS DATE.
  DEFINE VARIABLE d2            AS DATE.
  DEFINE VARIABLE datum0        AS DATE.
  DEFINE VARIABLE datum1        AS DATE.
  DEFINE VARIABLE datum2        AS DATE.
  DEFINE VARIABLE curr-i        AS INTEGER.
  DEFINE VARIABLE net-lodg      AS DECIMAL.
  DEFINE VARIABLE Fnet-lodg     AS DECIMAL.
  DEFINE VARIABLE tot-breakfast AS DECIMAL.
  DEFINE VARIABLE tot-Lunch     AS DECIMAL.
  DEFINE VARIABLE tot-dinner    AS DECIMAL.
  DEFINE VARIABLE tot-Other     AS DECIMAL.
  DEFINE VARIABLE tot-rmrev     AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-vat       AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-service   AS DECIMAL INITIAL 0.

  DEFINE BUFFER bgenstat FOR genstat.

  /*DEFINE VARIABLE datum AS DATE. */

  DO:
      ASSIGN d2 = from-date.
      FOR EACH res-line WHERE ((res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        AND res-line.resstatus NE 8
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT d2))) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
        BY res-line.resnr BY res-line.reslinnr descending: 

          ASSIGN curr-i = 0.

          IF res-line.kontignr LT 0 THEN 
          DO:
              ASSIGN do-it1 = YES.
              FIND FIRST cl-list WHERE cl-list.segm EQ reservation.segmentcode NO-ERROR.

              IF NOT AVAILABLE cl-list THEN 
              DO:
                  FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                  IF AVAILABLE segment AND NOT segment.bezeich MATCHES "*$$0" THEN 
                  DO:
                    IF segment.betriebsnr NE 1 AND segment.betriebsnr NE 2 THEN
                    DO:
                      CREATE cl-list.
                      cl-list.compli     = NO. 
                      cl-list.segm       = segment.segmentcode. 
                      cl-list.bezeich    = segment.bezeich.
                      cl-list.betriebsnr = segment.betriebsnr.
                    END.
                    ELSE
                    DO:
                      CREATE cl-list.
                      cl-list.compli     = YES. 
                      cl-list.segm       = segment.segmentcode. 
                      cl-list.bezeich    = segment.bezeich.
                      cl-list.betriebsnr = segment.betriebsnr.
                    END.
                  END.    
                  ELSE ASSIGN do-it1 = NO.
              END.

              IF do-it1 = YES THEN 
              DO:
                  datum1 = d2.
                  IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
                  datum2 = to-date. 
                  IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

                  DO datum0 = datum1 TO datum2:
                      ASSIGN curr-i = curr-i + 1.

                      IF datum0 NE res-line.abreise THEN
                      DO:
                          ASSIGN net-lodg      = 0
                                tot-breakfast = 0
                                tot-lunch     = 0
                                tot-dinner    = 0
                                tot-other     = 0
                          . 

                          RUN get-room-breakdown.p(RECID(res-line), datum0, curr-i, from-date,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).    

                          /* Start - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
                          IF datum0 = to-date THEN 
                          DO:
                            cl-list.droom = cl-list.droom + res-line.zimmeranz. 
                            cl-list.dpax  = cl-list.dpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                            cl-list.drev  = cl-list.drev + net-lodg. 
          
                            IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                            DO:
                              droomRev         = droomRev + res-line.zimmeranz. 
                              dpaxRev          = dpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix duplicate count on pax */
                              drevRev          = drevRev + net-lodg.
                            END.
          
                            IF cl-list.betriebsnr EQ 1 THEN
                            DO:
                              droomComp = droomComp + res-line.zimmeranz.
                              dpaxComp  = dpaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                            IF cl-list.betriebsnr EQ 2 THEN
                            DO:
                              droomHU = droomHU + res-line.zimmeranz.
                              dpaxHU  = dpaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                          END.
          
                          IF (mi-mtd-chk AND MONTH(datum0) = MONTH(to-date))
                          OR (mi-ftd-chk AND datum0 GE d2 AND datum0 LE tdate) THEN 
                          DO:
                            cl-list.mroom   = cl-list.mroom + res-line.zimmeranz. 
                            cl-list.mpax    = cl-list.mpax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                            cl-list.mrev    = cl-list.mrev + net-lodg. 
                            
                            IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                            DO:
                              mroomRev           = mroomRev + res-line.zimmeranz. 
                              mpaxRev            = mpaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. 
                              mrevRev            = mrevRev + net-lodg.
                            END.
                            
                            IF cl-list.betriebsnr EQ 1 THEN
                            DO:
                              mroomComp = mroomComp + res-line.zimmeranz.
                              mpaxComp  = mpaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                            IF cl-list.betriebsnr EQ 2 THEN
                            DO:
                              mroomHU = mroomHU + res-line.zimmeranz.
                              mpaxHU  = mpaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                            END.
                          END.
          
                          ASSIGN
                            cl-list.yroom   = cl-list.yroom + res-line.zimmeranz.
                            cl-list.ypax    = cl-list.ypax + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                            cl-list.yrev    = cl-list.yrev + net-lodg.
                          
                          IF cl-list.betriebsnr NE 1 AND cl-list.betriebsnr NE 2 THEN
                          DO:
                            yroomRev           = yroomRev + res-line.zimmeranz.
                            ypaxRev            = ypaxRev + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis.
                            yrevRev            = yrevRev + net-lodg.
                          END.
          
                          IF cl-list.betriebsnr EQ 1 THEN
                          DO:
                            yroomComp = yroomComp + res-line.zimmeranz.
                            ypaxComp  = ypaxComp + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                          END.
                          IF cl-list.betriebsnr EQ 2 THEN
                          DO:
                            yroomHU = yroomHU + res-line.zimmeranz.
                            ypaxHU  = ypaxHU + res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis. /* Oscar (07/03/25) - 89D27E - fix called wrong table */
                          END.
                          /* End - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
                      END.                                        
                  END.
              END.
          END.
      END.
  END.

  IF inact THEN
  DO:
      FOR EACH cl-list WHERE (cl-list.betriebsnr GE i1 AND cl-list.betriebsnr LE i2): 
        IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
        IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
        IF cl-list.yroom NE 0 THEN cl-list.yrate = cl-list.yrev / cl-list.yroom. 
        cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
        cl-list.proz2 = 100.0 * cl-list.mroom / /*(tot-room * day(to-date))*/ mtd-act. 
        cl-list.proz3 = 100.0 * cl-list.yroom / ytd-act. 
        IF droomRev NE 0 THEN drateRev = drevRev / droomRev. 
        IF mroomRev NE 0 THEN mrateRev = mrevRev / mroomRev. 
        IF yroomRev NE 0 THEN yrateRev = yrevRev / yroomRev.
    
        IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
        IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
        IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
     
        ASSIGN tot-proz3 = tot-proz3 + cl-list.proz3 /*ROUND(cl-list.proz3, 2).    */.
    
        /*M */
        /* dpaxRev = dpaxRev + cl-list.dpax. */

        IF cl-list.drev EQ 0 AND cl-list.mrev EQ 0 AND cl-list.yrev EQ 0 THEN 
          cl-list.zero-flag = YES.
      END. 
      CREATE cl-list.
  END.
  
  /* 
  droomExc = droom.
  mroomExc = mroom.
  yroomExc = yroom.
  
  ASSIGN
      droomRev = droomExc
      mroomRev = mroomExc
      yroomRev = yroomExc. */

  /* Start - Oscar (28/01/25) - FD7927 - adjust variable */
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = rev-title
    cl-list.droom = droomRev
    cl-list.proz1 = droomRev / tot-room * 100
    cl-list.mroom = mroomRev
    cl-list.proz2 = mroomRev / mtd-act * 100
    cl-list.dpax = dpaxRev
    cl-list.mpax = mpaxRev
    cl-list.yroom = yroomRev
    cl-list.ypax = ypaxRev
    cl-list.proz3 = tot-proz3
    cl-list.drev = drevRev
    cl-list.mrev = mrevRev
    cl-list.yrev = yrevRev 
  .

  IF show-avrg THEN 
  DO: 
    IF droomRev NE 0 THEN cl-list.drate = drevRev / droomRev.
    ELSE cl-list.drate = 0.
    IF mroomRev NE 0 THEN cl-list.mrate = mrevRev / mroomRev.
    ELSE cl-list.mrate = 0.
    IF yroomRev NE 0 THEN cl-list.yrate = yrevRev / yroomRev.
    ELSE cl-list.yrate = 0.
  END.

  /* IF rev-title1 NE "" THEN 
  DO: 
    CREATE cl-list.
    ASSIGN cl-list.bezeich = rev-title1.
    IF droomRev NE 0 THEN cl-list.proz1 = (dpaxRev - droomRev) / droomRev * 100.
    ELSE cl-list.proz1 = 0.
    IF mroomRev NE 0 THEN cl-list.proz2 = (mpaxRev - mroomRev) / mroomRev * 100.
    ELSE cl-list.proz2 = 0.
    IF yroomRev NE 0 THEN cl-list.proz3 = (ypaxRev - yroomRev) / yroomRev * 100.
    ELSE cl-list.proz3 = 0.
  END.  */
  CREATE cl-list.

  /* End - Oscar (28/01/25) - FD7927 - adjust variable */
END. 


PROCEDURE cal-umsatz4b: 
  DEFINE INPUT PARAMETER i1 AS INTEGER. 
  DEFINE INPUT PARAMETER i2 AS INTEGER. 
  DEFINE INPUT PARAMETER rev-title AS CHAR. 
  DEFINE INPUT PARAMETER rev-title1 AS CHAR. 
  DEFINE INPUT PARAMETER show-avrg AS LOGICAL. 

  DEFINE VARIABLE i             AS INTEGER. 
  DEFINE VARIABLE datum         AS DATE. 
  DEFINE VARIABLE inact         AS LOGICAL INITIAL NO.
  DEFINE VARIABLE do-it1        AS LOGICAL.
  DEFINE VARIABLE d1            AS DATE.
  DEFINE VARIABLE d2            AS DATE.
  DEFINE VARIABLE datum0        AS DATE.
  DEFINE VARIABLE datum1        AS DATE.
  DEFINE VARIABLE datum2        AS DATE.
  DEFINE VARIABLE curr-i        AS INTEGER.
  DEFINE VARIABLE net-lodg      AS DECIMAL.
  DEFINE VARIABLE Fnet-lodg     AS DECIMAL.
  DEFINE VARIABLE tot-breakfast AS DECIMAL.
  DEFINE VARIABLE tot-Lunch     AS DECIMAL.
  DEFINE VARIABLE tot-dinner    AS DECIMAL.
  DEFINE VARIABLE tot-Other     AS DECIMAL.
  DEFINE VARIABLE tot-rmrev     AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-vat       AS DECIMAL INITIAL 0.
  DEFINE VARIABLE tot-service   AS DECIMAL INITIAL 0.

  DEFINE BUFFER bgenstat FOR genstat.
  
  /* Start - Oscar (28/01/25) - FD7927 - comment to prevent duplicate because already done in cal-umsatz4a */
  /* DO:
      ASSIGN d2 = from-date.
      FOR EACH res-line WHERE ((res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        AND res-line.resstatus NE 8
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT d2))) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
        BY res-line.resnr BY res-line.reslinnr descending: 

        ASSIGN curr-i = 0.

        IF res-line.kontignr LT 0 THEN DO:
            ASSIGN do-it1 = YES.
            FIND FIRST cl-list WHERE cl-list.segm EQ reservation.segmentcode NO-ERROR.
            IF NOT AVAILABLE cl-list THEN DO:
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode 
                    NO-LOCK NO-ERROR.
                IF AVAILABLE segment AND NOT segment.bezeich MATCHES "*$$0" THEN DO:
                    CREATE cl-list. 
                    cl-list.segm    = segment.segmentcode. 
                    cl-list.bezeich = segment.bezeich.
                END.    
                ELSE ASSIGN do-it1 = NO.
            END.

            IF do-it1 = YES THEN DO:
                datum1 = d2.
                IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
                datum2 = to-date. 
                IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

                DO datum0 = datum1 TO datum2:
                    ASSIGN curr-i = curr-i + 1.

                    IF datum0 = res-line.abreise THEN .
                    ELSE DO:

                        ASSIGN net-lodg      = 0
                               tot-breakfast = 0
                               tot-lunch     = 0
                               tot-dinner    = 0
                               tot-other     = 0
                         . 

                        RUN get-room-breakdown.p(RECID(res-line), datum0, curr-i, from-date,
                                                 OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                 OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                 OUTPUT tot-dinner, OUTPUT tot-other,
                                                 OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                 OUTPUT tot-service).    

                        IF datum0 = to-date THEN DO:
                            droom         = droom + res-line.zimmeranz. 
                            cl-list.droom = cl-list.droom + res-line.zimmeranz. 
                            cl-list.dpax  = cl-list.dpax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis. 
                            cl-list.drev  = cl-list.drev + net-lodg. 
                            drev          = drev + net-lodg.
                        END.

                        IF (mi-mtd-chk AND MONTH(datum0) = MONTH(to-date))
                            OR (mi-ftd-chk AND datum0 GE d2 AND datum0 LE tdate) THEN DO:

                            cl-list.mroom   = cl-list.mroom + res-line.zimmeranz. 
                            cl-list.mpax    = cl-list.mpax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis. 
                            cl-list.mrev    = cl-list.mrev + net-lodg. 
                            mroom           = mroom + res-line.zimmeranz. 
                            mpax            = mpax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis. 
                            mrev            = mrev + net-lodg.                            
                        END.

                        ASSIGN
                            cl-list.yroom   = cl-list.yroom + res-line.zimmeranz
                            cl-list.ypax    = cl-list.ypax + res-line.erwachs + res-line.kind1 
                                            + res-line.kind2 + res-line.gratis
                            cl-list.yrev    = cl-list.yrev + net-lodg
                            yroom           = yroom + res-line.zimmeranz
                            ypax            = ypax + res-line.erwachs + res-line.kind1 
                                              + res-line.kind2 + res-line.gratis
                            yrev            = yrev + net-lodg. 
                    END.                                        
                END.
            END.
        END.
      END.
  END. */
  /* End - Oscar (28/01/25) - FD7927 - comment to prevent duplicate because already done in cal-umsatz4a */
  
  IF inact THEN
  DO:
      FOR EACH cl-list WHERE cl-list.compli = YES : 
        IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
        IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
        IF cl-list.yroom NE 0 THEN cl-list.yrate = cl-list.yrev / cl-list.yroom. 
        cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
        cl-list.proz2 = 100.0 * cl-list.mroom / /*(tot-room * day(to-date))*/ mtd-act. 
        cl-list.proz3 = 100.0 * cl-list.yroom / /*(tot-room * day(to-date))*/ ytd-act. 
        /* IF droom NE 0 THEN drate = drev / droom. 
        IF mroom NE 0 THEN mrate = mrev / mroom. 
        IF yroom NE 0 THEN yrate = yrev / yroom.  */
    
        IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
        IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
        IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
     
        /* dpax = dpax + cl-list.dpax. */
      END. 
      CREATE cl-list.
  END.

  /* Start - Oscar (28/01/25) - FD7927 - adjust variable */
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = rev-title
    cl-list.droom = droomRev + droomComp + droomHU
    cl-list.proz1 = (droomRev + droomComp + droomHU) / tot-room * 100
    cl-list.mroom = mroomRev + mroomComp + mroomHU
    cl-list.proz2 = (mroomRev + mroomComp + mroomHU) / mtd-act * 100
    cl-list.dpax = dpaxRev + dpaxComp + dpaxHU
    cl-list.mpax = mpaxRev + mpaxComp + mpaxHU
    cl-list.yroom = yroomRev + yroomComp + yroomHU
    cl-list.ypax = ypaxRev + ypaxComp + ypaxHU
    cl-list.proz3 = (yroomRev + yroomComp + yroomHU) / ytd-act * 100
    cl-list.drev = drevRev
    cl-list.mrev = mrevRev
    cl-list.yrev = yrevRev
  .
  
  IF show-avrg THEN 
  DO: 
    IF (droomRev + droomComp + droomHU) NE 0 THEN cl-list.drate = drevRev / (droomRev + droomComp + droomHU).
    ELSE cl-list.drate = 0.
    IF (mroomRev + mroomComp + mroomHU) NE 0 THEN cl-list.mrate = mrevRev / (mroomRev + mroomComp + mroomHU).
    ELSE cl-list.mrate = 0.
    IF (yroomRev + yroomComp + yroomHU) NE 0 THEN cl-list.yrate = yrevRev / (yroomRev + yroomComp + yroomHU).
    ELSE cl-list.yrate = 0.
  END.

  IF rev-title1 NE "" THEN 
  DO: 
    CREATE cl-list.
    ASSIGN cl-list.bezeich = rev-title1.
    
    IF (droomRev + droomComp + droomHU) NE 0 THEN cl-list.proz1 = ((dpaxRev + dpaxComp + dpaxHU) - (droomRev + droomComp + droomHU)) / (droomRev + droomComp + droomHU) * 100.
    ELSE cl-list.proz1 = 0.
    IF (mroomRev + mroomComp + mroomHU) NE 0 THEN cl-list.proz2 = ((mpaxRev + mpaxComp + mpaxHU) - (mroomRev + mroomComp + mroomHU)) / (mroomRev + mroomComp + mroomHU) * 100.
    ELSE cl-list.proz2 = 0.
    IF (yroomRev + yroomComp + yroomHU) NE 0 THEN cl-list.proz3 = ((ypaxRev + ypaxComp + ypaxHU) - (yroomRev + yroomComp + yroomHU)) / (yroomRev + yroomComp + yroomHU) * 100.
    ELSE cl-list.proz3 = 0.
  END.

  CREATE cl-list.

  /* End - Oscar (28/01/25) - FD7927 - adjust variable */
END.

PROCEDURE cal-umsatz5: 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE datum AS DATE. 
  DEFINE VARIABLE datum1 AS DATE.

  dooo = 0. 
  mooo = 0.
  yooo = 0.
  
  DO datum = from-date TO to-date: 
    FOR EACH outorder WHERE (outorder.gespstart GE datum AND outorder.gespstart LE datum) 
        OR (outorder.gespstart LE datum AND outorder.gespende GE datum) NO-LOCK,
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK:

          IF datum = to-date THEN dooo = dooo + 1. 
          
          /* Start - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
          FIND FIRST om-list WHERE om-list.zinr EQ outorder.zinr 
            AND om-list.gespstart EQ outorder.gespstart
            AND om-list.gespende EQ outorder.gespende NO-LOCK NO-ERROR.
          IF NOT AVAILABLE om-list THEN
          DO:
              CREATE om-list.
              om-list.zinr = outorder.zinr.           
              om-list.gespstart = outorder.gespstart.      
              om-list.gespende = outorder.gespende.

              mooo = mooo + 1.
          END.
          /* IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date)) THEN 
             mooo = mooo + 1. 
          */
          /* End - Oscar (28/01/25) - FD7927 - adjust to e1-desktop */
          yooo = yooo + 1.

    END.    
  END. 
  
  /* Oscar (28/01/25) - FD7927 - adjust calculation to e1-desktop */
  dvacant = tot-room - dooo - (droomRev + droomComp + droomHU).
  mvacant = mtd-act - mooo - (mroomRev + mroomComp + mroomHU).
  yvacant = ytd-act - yooo - (yroomRev + yroomComp + yroomHU).
  
  IF to-date = opening-date THEN 
  DO:
      mvacant = dvacant.
      yvacant = dvacant.
      mooo = dooo.
      yooo = dooo.
  END.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "V A C A N T"
    cl-list.droom = dvacant
    cl-list.proz1 = dvacant / tot-room * 100
    cl-list.mroom = mvacant
    cl-list.proz2 = mvacant / mtd-act * 100
    cl-list.yroom = yvacant
    cl-list.proz3 = yvacant / ytd-act * 100.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "Out Of Order"
    cl-list.droom = dooo
    cl-list.proz1 = dooo / tot-room * 100
    cl-list.mroom = mooo
    cl-list.proz2 = mooo / mtd-act * 100
    cl-list.yroom = yooo
    cl-list.proz3 = yooo / ytd-act * 100.

  CREATE cl-list.

  IF to-date LT ci-date THEN DO:
    FIND FIRST zinrstat WHERE zinrstat.zinr = "tot-rm" AND zinrstat.datum = to-date NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN all-room = zinrstat.zimmeranz.
  END.
  ELSE DO:
    FOR EACH zimmer NO-LOCK:
      ASSIGN all-room = all-room + 1.
    END.
  END.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "# Active Rooms"
    cl-list.droom = tot-room
    cl-list.proz1 = 100
    cl-list.mroom = mtd-act
    cl-list.proz2 = 100
    cl-list.yroom = ytd-act
    cl-list.proz3 = 100.

  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "Inactive Rooms"
    cl-list.droom = all-room - tot-room
    cl-list.mroom = mtd-totrm - mtd-act
    cl-list.yroom = ytd-totrm - ytd-act.
      
  CREATE cl-list.
  ASSIGN
    cl-list.bezeich = "Total Rooms"
    cl-list.droom = all-room
    cl-list.mroom = mtd-totrm
    cl-list.yroom = ytd-totrm
  .

  CREATE cl-list.
END. 
 

PROCEDURE cal-umsatz6: 
  DEFINE VARIABLE i            AS INTEGER. 
  DEFINE VARIABLE max-i        AS INTEGER INITIAL 0.
  DEFINE VARIABLE datum        AS DATE. 
  DEFINE VARIABLE art-list     AS INTEGER EXTENT 150. 
  DEFINE VARIABLE serv-vat     AS LOGICAL. 
  DEFINE VARIABLE fact         AS DECIMAL. 
  DEFINE VARIABLE serv         AS DECIMAL. 
  DEFINE VARIABLE vat          AS DECIMAL.
  DEFINE VARIABLE drev-droom   AS DECIMAL.
  DEFINE VARIABLE mrev-mroom   AS DECIMAL.
  DEFINE VARIABLE yrev-yroom   AS DECIMAL.
  /*MT 31/05/13 */ 
  DEFINE VARIABLE drev-droom1  AS DECIMAL.
  DEFINE VARIABLE mrev-mroom1  AS DECIMAL.
  DEFINE VARIABLE yrev-yroom1  AS DECIMAL.
  DEFINE VARIABLE compli-count AS DECIMAL.
  DEFINE VARIABLE state-str    AS CHARACTER.


  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH artikel WHERE artikel.departement = 0
      AND artikel.artart = 0 AND artikel.umsatzart = 1 NO-LOCK 
      BY artikel.artnr:
        max-i = max-i + 1.
        art-list[max-i] = artikel.artnr.
  END.

  do-it = YES.

  IF do-it THEN
  DO:
      DO i = 1 TO max-i: 
        FIND FIRST artikel WHERE artikel.artnr = art-list[i] 
          AND artikel.departement = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN 
        DO: 
          CREATE cl-list. 
          cl-list.segm = artikel.artnr. 
          IF i GE 10 THEN /*M give limitation 15.09.10*/
              cl-list.bezeich = translateExtended ("Other RmRev",lvCAREA,"").  
          ELSE 
              cl-list.bezeich = artikel.bezeich. 
         
          DO datum = from-date TO to-date: 
          serv = 0. 
          vat = 0. 
            FOR EACH umsatz WHERE umsatz.artnr = artikel.artnr 
              AND umsatz.departement = artikel.departement 
              AND umsatz.datum EQ datum NO-LOCK: 
    
              RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                 artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                fact = 1.00 + serv + vat. 
    
              IF datum = to-date THEN 
              DO: 
                drevRev = drevRev + umsatz.betrag / fact. 
                cl-list.drev = umsatz.betrag / fact. 
              END. 
              
              IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
                OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
              DO:
                  mrevRev = mrevRev + umsatz.betrag / fact. 
                  cl-list.mrev = cl-list.mrev + umsatz.betrag / fact. 
              END.
              ASSIGN
                  yrevRev = yrevRev + umsatz.betrag / fact. 
                  cl-list.yrev = cl-list.yrev + umsatz.betrag / fact. 
            END. 
          END. 
          IF cl-list.mrev = 0 THEN 
          DO: 
              cl-list.bezeich = "Deleted".
          END.
        END. 
      END. 
      CREATE cl-list.
  END.
  
  /* Start - Oscar (28/01/25) - FD7927 - adjust variable and calculation to e1-desktop */
 
  drev-droom  = drevRev / (droomRev + droomHU + droomComp).
  IF drev-droom EQ ? THEN drev-droom = 0.

  mrev-mroom  = mrevRev / (mroomRev + mroomHU + mroomComp).        /*MT 31/05/13 */
  IF mrev-mroom EQ ? THEN mrev-mroom = 0.

  yrev-yroom  = yrevRev / (yroomRev + yroomHU + yroomComp).
  IF yrev-yroom EQ ? THEN yrev-yroom = 0.

  IF NOT mi-excHU-chk THEN
    ASSIGN
      droomRev = droomRev + droomHU
      mroomRev = mroomRev + mroomHU
      yroomRev = yroomRev + yroomHU.

  IF NOT mi-excComp-chk THEN
    ASSIGN
      droomRev = droomRev + droomComp
      mroomRev = mroomRev + mroomComp
      yroomRev = yroomRev + yroomComp.
  
  drev-droom1  = drevRev / droomRev.        /*MT 31/05/13 */
  IF drev-droom1 EQ ? THEN drev-droom1 = 0.
  
  mrev-mroom1  = mrevRev / mroomRev.        /*MT 31/05/13 */
  IF mrev-mroom1 EQ ? THEN mrev-mroom1 = 0.

  yrev-yroom1  = yrevRev / yroomRev.
  IF yrev-yroom1 EQ ? THEN yrev-yroom1 = 0.

  IF mi-excHU-chk AND mi-excComp-chk THEN
    state-str = translateExtended ("RmRev Exc Comp&HU",lvCAREA,"").
  ELSE IF mi-excHU-chk THEN
    state-str = translateExtended ("RmRev Exc HU",lvCAREA,"").
  ELSE IF mi-excComp-chk THEN
    state-str = translateExtended ("RmRev Exc Comp",lvCAREA,"").
  ELSE
    state-str = "".

  /* End - Oscar (28/01/25) - FD7927 - adjust variable and calculation to e1-desktop */
  
  IF NOT long-digit THEN 
  DO: 
    CREATE cl-list.
    ASSIGN
      cl-list.bezeich = "RmRev Inc All"
      cl-list.drate = drev-droom
      cl-list.mrate = mrev-mroom
      cl-list.drev = drevRev
      cl-list.mrev = mrevRev
      cl-list.yrev = yrevRev
      cl-list.yrate = yrev-yroom.

    IF mi-excHU-chk OR mi-excComp-chk THEN
    DO:
      CREATE cl-list.
      ASSIGN
        cl-list.bezeich = state-str
        cl-list.drate = drev-droom1
        cl-list.mrate = mrev-mroom1
        cl-list.drev = drevRev
        cl-list.mrev = mrevRev
        cl-list.yrev = yrevRev
        cl-list.yrate = yrev-yroom1.
    END.
  END.
  ELSE 
  DO:
    CREATE cl-list.
    ASSIGN
      cl-list.bezeich = "RmRev Inc All"
      cl-list.drate = drev-droom
      cl-list.mrate = mrev-mroom
      cl-list.drev = drevRev
      cl-list.mrev = mrevRev
      cl-list.yrev = yrevRev
      cl-list.yrate = yrev-yroom.

    IF mi-excHU-chk OR mi-excComp-chk THEN
    DO:
      CREATE cl-list.
      ASSIGN
        cl-list.bezeich = state-str
        cl-list.drate = drev-droom1
        cl-list.mrate = mrev-mroom1
        cl-list.drev = drevRev
        cl-list.mrev = mrevRev
        cl-list.yrev = yrevRev
        cl-list.yrate = yrev-yroom1.
    END.
  END.
END. 
