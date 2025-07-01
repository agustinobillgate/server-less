/*FT 151214 bonus night*/

DEFINE WORKFILE cl-list 
  FIELD flag       AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD segm       AS INTEGER FORMAT ">>9" 
  FIELD betriebsnr AS INTEGER 
  FIELD compli     AS LOGICAL INITIAL NO 
  FIELD bezeich    AS CHAR FORMAT "x(16)" 
  FIELD droom      AS INTEGER FORMAT "->9" 
  FIELD proz1      AS DECIMAL FORMAT "->,>>,>>9.9"
  FIELD mroom      AS INTEGER FORMAT ">>,>>9" 
  FIELD proz2      AS DECIMAL FORMAT "->,>>,>>9.9" 
  FIELD dpax       AS INTEGER FORMAT ">>9" 
  FIELD mpax       AS INTEGER FORMAT ">,>>9" 
  FIELD drate      AS DECIMAL FORMAT ">,>>>,>>9.99" 
  FIELD mrate      AS DECIMAL FORMAT ">,>>>,>>9.99" 
  FIELD drev       AS DECIMAL FORMAT "->,>>>,>>9.99" 
  FIELD mrev       AS DECIMAL FORMAT "->>,>>>,>>9.99"
  FIELD yroom      AS INTEGER FORMAT "->,>>,>>9"
  FIELD proz3      AS DECIMAL FORMAT "->,>>9.9"
  FIELD ypax       AS INTEGER FORMAT "->,>>,>>9"
  FIELD yrate      AS DECIMAL FORMAT ">,>>>,>>9.99"
  FIELD yrev       AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" . 

DEFINE TEMP-TABLE output-list 
  FIELD segNo      AS INTEGER INITIAL 0
  FIELD flag       AS CHAR 
  FIELD STR        AS CHAR
  FIELD yroom      AS CHAR FORMAT "x(6)"
  FIELD proz3      AS CHAR FORMAT "x(6)"
  FIELD ypax       AS CHAR FORMAT "x(6)"
  FIELD yrate      AS CHAR FORMAT "x(13)" 
  FIELD yrev       AS CHAR FORMAT "x(22)"
  FIELD zero-flag  AS LOGICAL INIT NO.

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

DEF OUTPUT PARAMETER TABLE FOR output-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rm-drecap2".

DEFINE VARIABLE do-it AS LOGICAL INITIAL NO.

DEFINE VARIABLE droomRev AS INTEGER FORMAT ">>9".
DEFINE VARIABLE mroomRev AS INTEGER FORMAT ">>,>>9".
DEFINE VARIABLE yroomRev AS INTEGER FORMAT ">>,>>9".

DEFINE VARIABLE droomExc AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mroomExc AS INTEGER FORMAT "->,>>>,>>9".
DEFINE VARIABLE yroomExc AS INTEGER FORMAT "->,>>>,>>9".

DEFINE VARIABLE tot-room AS INTEGER INITIAL 0. /*active room*/
DEFINE VARIABLE all-room AS INTEGER INITIAL 0.
DEFINE VARIABLE dvacant AS INTEGER. 
DEFINE VARIABLE dooo AS INTEGER. 
DEFINE VARIABLE mvacant AS INTEGER. 
DEFINE VARIABLE mooo AS INTEGER. 
DEFINE VARIABLE yvacant AS INTEGER. 
DEFINE VARIABLE yooo AS INTEGER. 
DEFINE VARIABLE dnoshow AS INTEGER. 
DEFINE VARIABLE dcancel AS INTEGER. 
DEFINE VARIABLE mnoshow AS INTEGER. 
DEFINE VARIABLE mcancel AS INTEGER. 
DEFINE VARIABLE ynoshow AS INTEGER. 
DEFINE VARIABLE ycancel AS INTEGER. 

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

DEFINE VARIABLE from-bez AS CHAR FORMAT "x(22)". 
DEFINE VARIABLE to-bez AS CHAR FORMAT "x(22)". 
 
DEFINE VARIABLE inactive     AS INTEGER. 
DEFINE VARIABLE mtd-act      AS INTEGER.
DEFINE VARIABLE mtd-totrm    AS INTEGER.

DEFINE VARIABLE ytd-act      AS INTEGER.
DEFINE VARIABLE ytd-totrm    AS INTEGER.

DEFINE VARIABLE ncompli AS INTEGER FORMAT ">>9".
DEFINE VARIABLE mtd-ncompli AS INTEGER FORMAT ">>9".
DEFINE VARIABLE ytd-ncompli AS INTEGER FORMAT ">>9".

DEFINE VARIABLE dcompli AS INTEGER .
DEFINE VARIABLE mcompli AS INTEGER .
DEFINE VARIABLE ycompli AS INTEGER .

DEFINE VARIABLE dHU AS INTEGER .
DEFINE VARIABLE mHU AS INTEGER .
DEFINE VARIABLE yHU AS INTEGER .


FIND FIRST htparam WHERE paramnr = 186.
opening-date = htparam.fdate.
IF MONTH(to-date) = MONTH(opening-date) 
    AND YEAR(to-date) = YEAR(opening-date)THEN
    from-date = opening-date.

RUN create-umsatz.

PROCEDURE create-umsatz: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE black-list AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
  black-list = htparam.finteger. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
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
  
  FOR EACH zimmer WHERE NOT sleeping NO-LOCK: 
    inactive = inactive + 1. 
  END. 

  FOR EACH zkstat WHERE zkstat.datum = to-date NO-LOCK:
      tot-room = tot-room + zkstat.anz100.
  END.

  RUN create-lbl.
  RUN count-mtd-totrm.

  IF NOT segmtype-exist THEN 
  DO: 
    RUN cal-umsatz1(1, 12, 15, 49, translateExtended ("Room Revenue",lvCAREA,""), "", YES).
    RUN cal-umsatz1(13,14, 0, 0, translateExtended ("Total Room Occ",lvCAREA,""),
        translateExtended ("Double Occupancy",lvCAREA,""), NO).
  END. 
  ELSE 
  DO: 
    RUN cal-umsatz1a(0, 0, translateExtended ("Room Revenue",lvCAREA,""), "", YES). 
    RUN cal-umsatz1b(1, 2, translateExtended ("Total Room Occ",lvCAREA,""), 
        translateExtended ("Double Occupancy",lvCAREA,""), NO).
  END. 

  RUN cal-umsatz2. 
  RUN cal-umsatz3. 
  RUN no-show.
END. 

PROCEDURE create-lbl:
    DEF VAR n AS INTEGER NO-UNDO.

    CREATE output-list.
    ASSIGN
        output-list.flag    = "header"
        output-list.str     = FILL("=", 165)
        output-list.yroom   = FILL("=", 10)
        output-list.proz3   = FILL("=", 6)
        output-list.ypax    = FILL("=", 10)
        output-list.yrate   = FILL("=", 13)
        output-list.yrev    = FILL("=", 19).

    CREATE output-list.
    ASSIGN output-list.flag  = "header".
    
    IF mi-mtd-chk THEN
    DO:     
        output-list.str = translateExtended ("SNoGuest Segment   #Rm    (%)   MTD   (%) Pax   MTD    Avrg-Rate MTD-AvrgRate  Room-Revenue      MTD-RmRevenue",lvCAREA,""). 
    END.                                                                                                                                                                 
    ELSE
    DO:
        output-list.str = translateExtended ("SNoGuest Segment   #Rm    (%)   FTD   (%) Pax   FTD    Avrg-Rate FTD-AvrgRate  Room-Revenue      FTD-RmRevenue",lvCAREA,""). 
    END.
        
    ASSIGN
        output-list.yroom   = translateExtended("       YTD", lvCAREA, "")
        output-list.proz3   = translateExtended("   (%)", lvCAREA, "")
        output-list.ypax    = translateExtended("    YTDPax", lvCAREA, "")
        output-list.yrate   = translateExtended(" YTD-AvrgRate", lvCAREA, "")
        output-list.yrev    = translateExtended("   YTDRoomRevenue", lvCAREA, "").
    
    CREATE output-list.
    ASSIGN
        output-list.flag = "header"
        output-list.str = FILL("=", 165)
        output-list.str     = FILL("=", 165)
        output-list.yroom   = FILL("=", 10)
        output-list.proz3   = FILL("=", 6)
        output-list.ypax    = FILL("=", 10)
        output-list.yrate   = FILL("=", 13)
        output-list.yrev    = FILL("=", 19).
       
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
DEFINE BUFFER bgenstat FOR genstat.
  
  FOR EACH segment WHERE 
       ((segment.segmentcode GE i1 AND segment.segmentcode LE i2) OR 
       (segment.segmentcode GE i3 AND segment.segmentcode LE i4)) 
      NO-LOCK BY segment.segmentcode: 
        
      FIND FIRST bgenstat WHERE bgenstat.segmentcode = segment.segmentcode 
          AND bgenstat.datum GE from-date 
          AND bgenstat.datum LE to-date 
          AND bgenstat.resstatus NE 13 
          AND bgenstat.gratis EQ 0 
          AND bgenstat.segmentcode NE 0 
          AND bgenstat.nationnr NE 0
          AND bgenstat.zinr NE ""
          AND bgenstat.res-logic[2] NO-LOCK NO-ERROR.
      IF AVAILABLE bgenstat THEN ASSIGN do-it1 = YES.
      ELSE DO: 
          IF segment.bezeich MATCHES "*$$0" THEN ASSIGN do-it1 = NO.
          ELSE do-it1 = YES.
      END.

      IF do-it1 THEN DO:
          CREATE cl-list. 
          cl-list.segm = segment.segmentcode. 
          cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0").
    
          FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode 
              AND genstat.datum GE from-date 
              AND genstat.datum LE to-date 
              AND genstat.resstatus NE 13 
              /*MTAND genstat.zipreis NE 0*/
              AND genstat.gratis EQ 0 
              AND genstat.segmentcode NE 0 
              AND genstat.nationnr NE 0
              AND genstat.zinr NE ""
              AND genstat.res-logic[2] EQ YES /*27032012 genstat.res-logic[2] MU */
              USE-INDEX segm_ix NO-LOCK:
              
              IF genstat.res-date[1] LT genstat.datum AND genstat.res-date[2] = genstat.datum 
                AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
              ELSE
              DO:
                IF genstat.datum = to-date THEN 
                DO: 
                    droom         = droom + 1. 
                    cl-list.droom = cl-list.droom + 1. 
                    /*cl-list.dpax  = cl-list.dpax + genstat.gratis. */
                    cl-list.dpax  = cl-list.dpax + genstat.erwachs + genstat.kind1 
                                      + genstat.kind2 + genstat.gratis. 
                    cl-list.drev  = cl-list.drev + genstat.logis. 
                    /*M dpax          = dpax + genstat.erwachs + genstat.kind1 
                                    + genstat.kind2 + genstat.gratis.  */
                    drev          = drev + genstat.logis.
                END.
                IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                    OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                DO:
                    cl-list.mroom   = cl-list.mroom + 1. 
                    cl-list.mpax    = cl-list.mpax + genstat.erwachs + genstat.kind1 
                                      + genstat.kind2 + genstat.gratis. 
                    cl-list.mrev    = cl-list.mrev + genstat.logis. 
                    mroom           = mroom + 1. 
                    mpax            = mpax + genstat.erwachs + genstat.kind1 
                                      + genstat.kind2 + genstat.gratis. 
                    mrev            = mrev + genstat.logis. 
                END.
             
                ASSIGN
                    cl-list.yroom   = cl-list.yroom + 1
                    cl-list.ypax    = cl-list.ypax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 + genstat.gratis
                    cl-list.yrev    = cl-list.yrev + genstat.logis
                    yroom           = yroom + 1
                    ypax            = ypax + genstat.gratis
                    yrev            = yrev + genstat.logis. 
              END.              
          END.
      END.
     
      /*MT 01/02/13
      DO datum = from-date TO to-date: 

        FIND FIRST genstat WHERE genstat.segmentcode = segment.segmentcode 
          AND genstat.datum EQ datum AND genstat.resstatus NE 13
          /* AND segmentstat.betriebsnr = 0 */ 
          USE-INDEX segm_ix NO-LOCK NO-ERROR. 
        IF AVAILABLE genstat THEN 
        DO: 
          IF datum = to-date THEN 
          DO: 
            droom         = droom + 1. 
            cl-list.droom = cl-list.droom + 1. 
            cl-list.dpax  = cl-list.dpax + genstat.gratis. 
            cl-list.drev  = cl-list.drev + genstat.logis. 
            /*M dpax          = dpax + genstat.erwachs + genstat.kind1 
                            + genstat.kind2 + genstat.gratis.  */
            drev          = drev + genstat.logis.
          END.
          IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
              OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
          DO:
              cl-list.mroom   = cl-list.mroom + 1. 
              cl-list.mpax    = cl-list.mpax + genstat.erwachs + genstat.kind1 
                                + genstat.kind2 + genstat.gratis. 
              cl-list.mrev    = cl-list.mrev + genstat.logis. 
              mroom           = mroom + 1. 
              mpax            = mpax + genstat.erwachs + genstat.kind1 
                                + genstat.kind2 + genstat.gratis. 
              mrev            = mrev + genstat.logis. 
          END.

          ASSIGN
              cl-list.yroom   = cl-list.yroom + 1
              cl-list.ypax    = cl-list.ypax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis
              cl-list.yrev    = cl-list.yrev + genstat.logis
              yroom           = yroom + 1
              ypax            = ypax + genstat.gratis
              yrev            = yrev + genstat.logis. 
        END. 
      END. 
      */

  END. 
  
  IF do-it THEN
  DO:
      FOR EACH genstat WHERE genstat.datum GE from-date 
          AND genstat.datum LE to-date  
          AND genstat.segmentcode NE 0 
          AND genstat.nationnr NE 0
          AND genstat.zinr NE ""
          AND genstat.resstatus NE 13 
          AND genstat.res-logic[2] EQ YES NO-LOCK: /*27032012 genstat.res-logic[2] MU */
        FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-ERROR.
        IF AVAILABLE segment THEN       /*kl segment ada*/
        DO:
            FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                IF genstat.datum = to-date THEN 
                DO: 
                    cl-list.drev = cl-list.drev + genstat.res-deci[1].
                    drev = drev + genstat.logis.
                END.

                IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                    OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                DO:
                    cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
                    mrev = mrev + genstat.logis.
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
                            drev = drev + genstat.logis.
                        END.

                        IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                            OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                        DO:
                            cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
                            mrev = mrev + genstat.logis.
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
                                drev = drev + genstat.logis.
                            END.

                            IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                                OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                            DO:
                                cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
                                mrev = mrev + genstat.logis.
                            END.
                        END.
                    END.
                END.
            END.
            ELSE
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

                        IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                            OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                        DO:
                            cl-list.mrev = cl-list.mrev + genstat.res-deci[1].
                            mrev = mrev + genstat.logis.
                        END.
                    END.
                END.
            END.
        END.
      END.
  END.


  
  FOR EACH cl-list WHERE ((cl-list.segm GE i1 AND cl-list.segm LE i2) 
    OR (cl-list.segm GE i3 AND cl-list.segm LE i4)): 
    IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
    IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
    cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
    cl-list.proz2 = 100.0 * cl-list.mroom / /*(tot-room * day(to-date))*/ mtd-act. 
    cl-list.proz3 = 100.0 * cl-list.yroom / /*(tot-room * day(to-date))*/ ytd-act. 
    IF droom NE 0 THEN drate = drev / droom. 
    IF mroom NE 0 THEN mrate = mrev / mroom. 
    IF yroom NE 0 THEN yrate = yrev / yroom. 
 
    IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
    IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
    IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
 
    dpax = dpax + cl-list.dpax.
    CREATE output-list.
    output-list.segNo = cl-list.segm.

    ASSIGN
        output-list.str = STRING(cl-list.segm, ">>>") 
      + STRING(cl-list.bezeich, "x(16)") 
      + STRING(cl-list.droom, "->9") 
      + STRING(cl-list.proz1, "->>9.99") 
      + STRING(cl-list.mroom, "->>>>9 ") 
      + STRING(cl-list.proz2, "->>9.99") 
      + STRING(cl-list.dpax, "->9") 
      + STRING(cl-list.mpax, "->,>>9") 
      + STRING(cl-list.drate, "->,>>>,>>9.99") 
      + STRING(cl-list.mrate, "->,>>>,>>9.99") 
      + STRING(cl-list.drev, "->>,>>>,>>9.99") 
      + STRING(cl-list.mrev, ">>>,>>>,>>>,>>9.99")
        output-list.yroom = STRING(cl-list.yroom, "->,>>>,>>9") 
        output-list.ypax = STRING(cl-list.ypax, "->,>>>,>>9") 
        output-list.proz3 = STRING(cl-list.proz3, "->>9.99") 
        output-list.yrev = STRING(cl-list.yrev, "->>>,>>>,>>>,>>9.99").
        output-list.yrate = STRING(cl-list.yrate, "->,>>>,>>9.99").
    IF cl-list.drev EQ 0 AND cl-list.mrev EQ 0 AND cl-list.yrev EQ 0 THEN 
        output-list.zero-flag = YES.
  END. 
  CREATE output-list. 
  ASSIGN
      output-list.str = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 19).
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
 
  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(rev-title,"x(16)") 
      + STRING(droom, "->9") 
      + STRING(droom / tot-room * 100, "->>9.99") 
      + STRING(mroom, "->>>>9") 
      + STRING(mroom / /*(tot-room * day(to-date))*/ mtd-act * 100, "->>9.99") 
      + STRING(dpax, "->9") 
      + STRING(mpax, "->,>>9")
      output-list.yroom = STRING(yroom, "->,>>>,>>9")
      output-list.ypax  = STRING(ypax, "->,>>>,>>9")
      output-list.proz3 = STRING(ytd-act * 100 , "->,>>9").
  IF show-avrg THEN 
  DO: 
    IF droom NE 0 THEN output-list.str = output-list.str 
      + STRING(drev / droom, "->,>>>,>>9.99"). 
    ELSE output-list.str = output-list.str + STRING(0, ">,>>>,>>9.99"). 
   IF mroom NE 0 THEN output-list.str = output-list.str 
     + STRING(mrev / mroom, "->,>>>,>>9.99"). 
    ELSE output-list.str = output-list.str + STRING(0, ">,>>>,>>9.99"). 
    IF yroom NE 0 THEN output-list.yrate = 
      STRING(yrev / yroom, "->,>>>,>>9.99"). 
    ELSE output-list.yrate = STRING(0, "->,>>>,>>9.99"). 
  END. 
  ELSE output-list.str 
    = output-list.str + STRING(0, ">>>>>>>>>>>>>") + STRING(0, ">>>>>>>>>>>>>"). 
  ASSIGN
      output-list.str = output-list.str 
      + STRING(drev, ">>>,>>>,>>9.99") 
      + STRING(mrev, ">>>,>>>,>>>,>>9.99")
      output-list.yrev = STRING(yrev, "->>>,>>>,>>>,>>9.99"). 
 
  IF rev-title1 NE "" THEN 
  DO: 
    CREATE output-list. 
    output-list.str = "   " + STRING(rev-title1,"x(16)") 
      + STRING(0, ">>>"). 
    IF droom NE 0 THEN output-list.str = output-list.str 
      + STRING((dpax - droom) / droom * 100, "->>9.99") /*M*/ + STRING(0,">,>>>"). 
    ELSE output-list.str = output-list.str 
      + STRING(0, "->>9.99") /*M*/ + STRING(0, ">,>>>"). 
    IF mroom NE 0 THEN output-list.str = output-list.str 
      + STRING((mpax - mroom) / mroom * 100, "->>9.99").  /*M*/
    ELSE output-list.str = output-list.str + STRING(0, "->>9.99").  /*M*/
    output-list.str = output-list.str + STRING(0, ">>>") + STRING(0, ">>,>>>"). 
    IF yroom NE 0 THEN output-list.proz3 =
       STRING((ypax - yroom) / yroom * 100, "->>9.99").  /*M*/
    ELSE output-list.proz3 = STRING(0, "->>9.99").  /*M*/
  END. 
 
  CREATE output-list. 
  ASSIGN
      output-list.str = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 19).
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
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

DEFINE BUFFER bgenstat FOR genstat.

/*DEFINE VARIABLE datum AS DATE. */

  FOR EACH segment WHERE segment.betriebsnr = 0 NO-LOCK BY segment.segmentcode: 
    FIND FIRST bgenstat WHERE bgenstat.segmentcode = segment.segmentcode 
          AND bgenstat.datum GE from-date 
          AND bgenstat.datum LE to-date 
          AND bgenstat.resstatus NE 13 
          AND bgenstat.gratis EQ 0 
          AND bgenstat.segmentcode NE 0 
          AND bgenstat.nationnr NE 0
          AND bgenstat.zinr NE ""
          AND bgenstat.res-logic[2] NO-LOCK NO-ERROR.
    IF AVAILABLE bgenstat THEN ASSIGN do-it1 = YES.
    ELSE DO: 
          IF segment.bezeich MATCHES "*$$0" THEN ASSIGN do-it1 = NO.
          ELSE do-it1 = YES.
      END.

    IF do-it1 THEN DO:
        CREATE cl-list. 
        cl-list.segm = segment.segmentcode. 
        cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0"). 
        cl-list.betriebsnr = segment.betriebsnr. 
        cl-list.drev = 0.
        /*DO datum = from-date TO to-date: */
        
        FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode 
            AND genstat.datum GE from-date 
            AND genstat.datum LE to-date 
            AND genstat.resstatus NE 13 
            /*FT 151214AND genstat.zipreis NE 0*/
            AND genstat.gratis EQ 0
            AND genstat.segmentcode NE 0 
            AND genstat.nationnr NE 0
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] EQ YES /*27032012 genstat.res-logic[2] MU */
            USE-INDEX segm_ix NO-LOCK:
            
            inact = YES.
            IF genstat.res-date[1] LT genstat.datum AND genstat.res-date[2] = genstat.datum 
                AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
            ELSE
            DO:
              IF genstat.datum = to-date THEN 
              DO: 
                  droom             = droom + 1. 
                  cl-list.droom     = cl-list.droom + 1. 
                  cl-list.dpax      = cl-list.dpax + genstat.erwachs + genstat.kind1 
                                      + genstat.kind2. 
                  cl-list.drev      = cl-list.drev + genstat.logis. 
                  /*M dpax              = dpax + genstat.erwachs + genstat.kind1 
                                      + genstat.kind2. */
                  drev              = drev + genstat.logis. 
              END. 
             
              IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                  OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
              DO:
                  cl-list.mroom   = cl-list.mroom + 1. 
                  cl-list.mpax    = cl-list.mpax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2. 
                  cl-list.mrev    = cl-list.mrev + genstat.logis. 
                  mroom           = mroom + 1. 
                  mpax            = mpax + genstat.erwachs + genstat.kind1 
                                    + genstat.kind2. 
                  mrev            = mrev + genstat.logis. 
              END.
              ASSIGN
                  cl-list.yroom   = cl-list.yroom + 1. 
                  cl-list.ypax    = cl-list.ypax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2. 
                  cl-list.yrev    = cl-list.yrev + genstat.logis. 
                  yroom           = yroom + 1. 
                  ypax            = ypax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2. 
                  yrev            = yrev + genstat.logis.
            END.
             
        END. /*each genstat*/
    END.    
  END.  /*each segment*/
  
/********merge other room revenue*********/
  IF do-it THEN
  DO:
      FOR EACH genstat WHERE genstat.datum GE from-date 
          AND genstat.datum LE to-date  
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
                      ASSIGN cl-list.drev = cl-list.drev + genstat.res-deci[1]
                      drev = drev + genstat.res-deci[1].
                  END.

                  IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                      OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                  DO:
                      ASSIGN cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                                  mrev = mrev + genstat.res-deci[1].
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
                              ASSIGN cl-list.drev = cl-list.drev + genstat.res-deci[1]
                              drev = drev + genstat.res-deci[1].
                          END.

                          IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                              OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                          DO:
                              ASSIGN cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                              mrev = mrev + genstat.res-deci[1].
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
                                  ASSIGN cl-list.drev = cl-list.drev + genstat.res-deci[1]
                                  drev = drev + genstat.res-deci[1].
                              END.

                              IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                                  OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                              DO:
                                  ASSIGN cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                                  mrev = mrev + genstat.res-deci[1].
                              END.
                          END.
                      END.
                  END.
              END.
              ELSE
              DO: 
                  FIND FIRST segment NO-ERROR. 
                  IF AVAILABLE segment THEN
                  DO:
                      FIND FIRST cl-list WHERE cl-list.segm EQ segment.segmentcode NO-ERROR.
                      IF AVAILABLE cl-list THEN
                      DO:
                          IF genstat.datum = to-date THEN 
                          DO: 
                              ASSIGN cl-list.drev = cl-list.drev + genstat.res-deci[1]
                              drev = drev + genstat.res-deci[1].
                          END.

                          IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                              OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                          DO:
                              ASSIGN cl-list.mrev = cl-list.mrev + genstat.res-deci[1]
                              mrev = mrev + genstat.res-deci[1].
                          END.
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
        IF droom NE 0 THEN drate = drev / droom. 
        IF mroom NE 0 THEN mrate = mrev / mroom. 
        IF yroom NE 0 THEN yrate = yrev / yroom. 
    
        IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
        IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
        IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
     
        ASSIGN tot-proz3 = tot-proz3 + cl-list.proz3 /*ROUND(cl-list.proz3, 2).    */.
    
        /*M */
        dpax = dpax + cl-list.dpax.
        CREATE output-list. 
        output-list.segNo = cl-list.segm.
        
        IF NOT long-digit THEN 
        DO:
            ASSIGN
            output-list.str = STRING(cl-list.segm, ">>>") 
              + STRING(cl-list.bezeich, "x(16)") 
              + STRING(cl-list.droom, "->9") 
              + STRING(cl-list.proz1, "->>9.99") 
              + STRING(cl-list.mroom, "->>>>9") 
              + STRING(cl-list.proz2, "->>9.99") 
              + STRING(cl-list.dpax, "->9") 
              + STRING(cl-list.mpax, "->,>>9") 
              + STRING(cl-list.drate, "->,>>>,>>9.99") 
              + STRING(cl-list.mrate, "->,>>>,>>9.99") 
              + STRING(cl-list.drev, "->>,>>>,>>9.99") 
              + STRING(cl-list.mrev, ">>>,>>>,>>>,>>9.99")  /*lalala*/
              output-list.yroom = STRING(cl-list.yroom, "->,>>>,>>9")
              output-list.ypax  = STRING(cl-list.ypax, "->,>>>,>>9") /*SIS 29/11/12 */
              output-list.yrate = STRING(cl-list.yrate, "->,>>>,>>9.99")
              output-list.yrev  = STRING(cl-list.yrev, "->>>,>>>,>>>,>>9.99")
              output-list.proz3 = STRING(cl-list.proz3, "->>9.99").
        END.
        ELSE
        DO:
            ASSIGN
            output-list.str = STRING(cl-list.segm, ">>>") 
              + STRING(cl-list.bezeich, "x(16)") 
              + STRING(cl-list.droom, "->9") 
              + STRING(cl-list.proz1, "->>9.99") 
              + STRING(cl-list.mroom, "->>>>9") 
              + STRING(cl-list.proz2, "->>9.99") 
              + STRING(cl-list.dpax, "->9") 
              + STRING(cl-list.mpax, "->,>>9") 
              + STRING(cl-list.drate, "->>>,>>>,>>9") 
              + STRING(cl-list.mrate, "->>>,>>>,>>9") 
              + STRING(cl-list.drev, "->,>>>,>>>,>>9") 
              + STRING(cl-list.mrev, "->>>,>>>,>>>,>>9")
              output-list.yroom = STRING(cl-list.yroom, "->,>>>,>>9")
              output-list.ypax  = STRING(cl-list.ypax, "->>>>9")
              output-list.yrate = STRING(cl-list.yrate, "->>>,>>>,>>9")
              output-list.yrev  = STRING(cl-list.yrev, "->>>>,>>>,>>>,>>9")
              output-list.proz3 = STRING(cl-list.proz3, "->>9.99").
        END.

        IF cl-list.drev EQ 0 AND cl-list.mrev EQ 0 AND cl-list.yrev EQ 0 THEN 
            output-list.zero-flag = YES.
      END. 
    
      CREATE output-list. 
      ASSIGN
          output-list.str = "   "
          output-list.yroom = FILL("-", 10)
          output-list.proz3 = FILL("-", 6)
          output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
          output-list.yrate = FILL("-", 13)
          output-list.yrev  = FILL("-", 19).
      DO i = 1 TO 96: 
        output-list.str = output-list.str + "----". 
      END. 
  END.
  
  droomExc = droom.
  mroomExc = mroom.
  yroomExc = yroom.
  
  ASSIGN
      droomRev = droomExc
      mroomRev = mroomExc
      yroomRev = yroomExc.
  CREATE output-list.
  ASSIGN
      output-list.str = "   " + STRING(rev-title,"x(16)") 
      + STRING(droom, "->9") 
      + STRING(droom / tot-room * 100, "->>9.99") 
      + STRING(mroom, "->>>>9") 
      + STRING(mroom / /*(tot-room * day(to-date))*/ mtd-act * 100, "->>9.99") /*M*/
      + STRING(dpax, "->9") 
      + STRING(mpax, "->,>>9").
  ASSIGN
      output-list.yroom = STRING(yroom, "->,>>>,>>9")
      output-list.ypax  = STRING(ypax, "->,>>>,>>9")
      output-list.proz3 = STRING(tot-proz3,"->>9.99") /*M*/
      .
  
  IF show-avrg THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      IF droom NE 0 THEN output-list.str = output-list.str 
        + STRING(drev / droom, "->,>>>,>>9.99"). 
      ELSE output-list.str = output-list.str + STRING(0, "->,>>>,>>9.99"). 
      IF mroom NE 0 THEN output-list.str = output-list.str 
        + STRING(mrev / mroom, "->,>>>,>>9.99"). 
      ELSE output-list.str = output-list.str + STRING(0, "->,>>>,>>9.99"). 
      IF yroom NE 0 THEN output-list.yrate = 
         STRING(yrev / yroom, "->,>>>,>>9.99"). 
      ELSE output-list.yrate = STRING(0, "->,>>>,>>9.99"). 
    END. 
    ELSE 
    DO: 
      IF droom NE 0 THEN output-list.str = output-list.str 
        + STRING(drev / droom, "->>>,>>>,>>9"). 
      ELSE output-list.str = output-list.str + STRING(0, "->>>,>>>,>>9"). 
      IF mroom NE 0 THEN output-list.str = output-list.str 
        + STRING(mrev / mroom, "->>>,>>>,>>9"). 
      ELSE output-list.str = output-list.str + STRING(0, "->>>,>>>,>>9"). 
      IF yroom NE 0 THEN output-list.yrate =
         STRING(yrev / yroom, "->>>,>>>,>>9"). 
      ELSE output-list.yrate = STRING(0, "->,>>>,>>>,>>9"). 
    END. 
  END. 
  ELSE output-list.str 
    = output-list.str + STRING(0, ">>>>>>>>>>>>>") + STRING(0, ">>>>>>>>>>>>>"). 
  IF NOT long-digit THEN 
      ASSIGN
      output-list.str = output-list.str 
      + STRING(drev, ">>>,>>>,>>9.99") 
      + STRING(mrev, ">>>,>>>,>>>,>>9.99")
      output-list.yrev = STRING(yrev, "->>>,>>>,>>>,>>9.99"). 
  ELSE 
      ASSIGN
          output-list.str = output-list.str 
            + STRING(drev, ">>,>>>,>>>,>>9") 
            + STRING(mrev, ">>>>,>>>,>>>,>>9")
          output-list.yrev = STRING(yrev, "->>>,>>>,>>>,>>9.99").
  
  IF rev-title1 NE "" THEN 
  DO: 
    CREATE output-list. 
    output-list.str = "   " + STRING(rev-title1,"x(16)") 
      + STRING(0, ">>>"). 
    IF droom NE 0 THEN output-list.str = output-list.str 
      + STRING((dpax - droom) / droom * 100, "->>9.99") /*M*/ + STRING(0,">,>>>"). 
    ELSE output-list.str = output-list.str 
      + STRING(0, "->>9.99") /*M*/ + STRING(0, ">,>>>"). 
    IF mroom NE 0 THEN output-list.str = output-list.str 
      + STRING((mpax - mroom) / mroom * 100, "->>9.99").  /*M*/
    ELSE output-list.str = output-list.str + STRING(0, "->>9.99"). /*M*/
    output-list.str = output-list.str + STRING(0, ">>>") + STRING(0, ">>,>>>"). 
    IF yroom NE 0 THEN output-list.proz3 =
       STRING((ypax - yroom) / yroom * 100, "->>9.99"). /*M*/
    ELSE output-list.proz3 = STRING(0, "->>9.99"). /*M*/
  END. 
 
  CREATE output-list. 
  ASSIGN
      output-list.str = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 19).
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
END. 


PROCEDURE cal-umsatz1b: 
    
DEFINE INPUT PARAMETER i1 AS INTEGER. 
DEFINE INPUT PARAMETER i2 AS INTEGER. 
DEFINE INPUT PARAMETER rev-title AS CHAR. 
DEFINE INPUT PARAMETER rev-title1 AS CHAR. 
DEFINE INPUT PARAMETER show-avrg AS LOGICAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE inact AS LOGICAL INITIAL NO.

DEFINE VARIABLE do-it1 AS LOGICAL.
DEFINE BUFFER bgenstat FOR genstat.

  FOR EACH segment NO-LOCK BY segment.segmentcode :      
    FIND FIRST bgenstat WHERE bgenstat.segmentcode = segment.segmentcode 
          AND bgenstat.datum GE from-date 
          AND bgenstat.datum LE to-date 
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

    IF do-it1 THEN DO:
        FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode  /*House Use*/
              AND genstat.datum GE from-date AND genstat.datum LE to-date 
              AND genstat.resstatus NE 13 
              AND genstat.gratis NE 0 /*FT 151214*/
              AND genstat.segmentcode NE 0 
              AND genstat.nationnr NE 0
              AND genstat.zinr NE ""
              AND genstat.res-logic[2] EQ YES /*27032012 genstat.res-logic[2] MU */
              USE-INDEX segm_ix NO-LOCK : 
              inact = YES.
              FIND FIRST cl-list WHERE cl-list.segm = segment.segmentcode 
                AND cl-list.compli = YES NO-LOCK NO-ERROR. 
              IF NOT AVAILABLE cl-list THEN 
              DO: 
                CREATE cl-list. 
                cl-list.compli = YES. 
                cl-list.segm = segment.segmentcode. 
                cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0"). 
                cl-list.betriebsnr = segment.betriebsnr. 
              END. 
    
              IF genstat.res-date[1] LT genstat.datum AND genstat.res-date[2] = genstat.datum 
                AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
              ELSE
              DO:
                IF genstat.datum = to-date THEN 
                DO:
                  droom = droom + 1.
                  cl-list.droom = cl-list.droom + 1.
                  cl-list.dpax  = cl-list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
                  /*M dpax          = dpax + genstat.gratis + genstat.erwachs 
                                  + genstat.kind1 + genstat.kind2.  */
                END. 
               
                IF (mi-mtd-chk AND MONTH(genstat.datum) = MONTH(to-date))
                    OR (mi-ftd-chk AND genstat.datum GE fdate AND genstat.datum LE tdate) THEN
                DO:
                    mroom           = mroom + 1.
                    cl-list.mroom   = cl-list.mroom + 1. 
                    cl-list.mpax    = cl-list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis. 
                    mpax            = mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                END.
                ASSIGN
                    yroom           = yroom + 1
                    cl-list.yroom   = cl-list.yroom + 1  /*House use*/
                    cl-list.ypax    = cl-list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    ypax            = ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
              END.
              
        END.
    END.       
  END. 
  

  IF inact THEN
  DO:
  
      FOR EACH cl-list WHERE cl-list.compli = YES : 
        IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
        IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
        IF cl-list.yroom NE 0 THEN cl-list.yrate = cl-list.yrev / cl-list.yroom. 
        cl-list.proz1 = 100.0 * cl-list.droom / tot-room. 
        cl-list.proz2 = 100.0 * cl-list.mroom / /*(tot-room * day(to-date))*/ mtd-act. 
        cl-list.proz3 = 100.0 * cl-list.yroom / /*(tot-room * day(to-date))*/ ytd-act. 
        IF droom NE 0 THEN drate = drev / droom. 
        IF mroom NE 0 THEN mrate = mrev / mroom. 
        IF yroom NE 0 THEN yrate = yrev / yroom. 
    
        IF cl-list.proz1 = ? THEN cl-list.proz1 = 0.
        IF cl-list.proz2 = ? THEN cl-list.proz2 = 0.
        IF cl-list.proz3 = ? THEN cl-list.proz3 = 0.
     
        /*M */
        dpax = dpax + cl-list.dpax.
        CREATE output-list.
        output-list.segNo = cl-list.segm.
    
        IF NOT long-digit THEN 
            ASSIGN
            output-list.str = STRING(cl-list.segm, ">>>") 
              + STRING(cl-list.bezeich, "x(16)") 
              + STRING(cl-list.droom, "->9") 
              + STRING(cl-list.proz1, "->>9.99") 
              + STRING(cl-list.mroom, "->>>>9") 
              + STRING(cl-list.proz2, "->>9.99") 
              + STRING(cl-list.dpax, "->9") 
              + STRING(cl-list.mpax, "->,>>9") 
              + STRING(cl-list.drate, "->,>>>,>>9.99") 
              + STRING(cl-list.mrate, "->,>>>,>>9.99") 
              + STRING(cl-list.drev, "->>,>>>,>>9.99") 
              + STRING(cl-list.mrev, ">>>,>>>,>>>,>>9.99")
                output-list.yroom = STRING(cl-list.yroom, "->,>>>,>>9")
                output-list.ypax  = STRING(cl-list.ypax, "->,>>>,>>9")
                output-list.yrate = STRING(cl-list.yrate, "->,>>>,>>9.99")
                output-list.yrev  = STRING(cl-list.yrev, "->>>,>>>,>>>,>>9.99")
                output-list.proz3 = STRING(cl-list.proz3, "->>9.99")
            .
        ELSE 
            ASSIGN
            output-list.str = STRING(cl-list.segm, ">>>") 
              + STRING(cl-list.bezeich, "x(16)") 
              + STRING(cl-list.droom, "->9") 
              + STRING(cl-list.proz1, "->>9.99") 
              + STRING(cl-list.mroom, "->>>>9") 
              + STRING(cl-list.proz2, "->>9.99") /*M*/
              + STRING(cl-list.dpax, "->9") 
              + STRING(cl-list.mpax, "->,>>9") 
              + STRING(cl-list.drate, "->>>,>>>,>>9") 
              + STRING(cl-list.mrate, "->>>,>>>,>>9") 
              + STRING(cl-list.drev, "->,>>>,>>>,>>9") 
              + STRING(cl-list.mrev, "->>>,>>>,>>>,>>9")
                output-list.yroom = STRING(cl-list.yroom, "->,>>>,>>9")
                output-list.ypax  = STRING(cl-list.ypax, "->,>>>,>>9")
                output-list.yrate = STRING(cl-list.yrate, "->>>,>>>,>>9")
                output-list.yrev  = STRING(cl-list.yrev, " ->>>,>>>,>>>,>>9")
                output-list.proz3 = STRING(cl-list.proz3, "->>9.99")
            .
            /*mpax = mpax + cl-list.mpax.*/
      END. 
      CREATE output-list. 
          ASSIGN
          output-list.str = "   "
          output-list.yroom = FILL("-", 10)
          output-list.proz3 = FILL("-", 6)
          output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
          output-list.yrate = FILL("-", 13)
          output-list.yrev  = FILL("-", 19). 
      DO i = 1 TO 96: 
        output-list.str = output-list.str + "----". 
      END.
  END.
  

  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(rev-title,"x(16)") 
      + STRING(droom, "->9") 
      + STRING(droom / tot-room * 100, "->>9.99") 
      + STRING(mroom, "->>>>9") 
      + STRING(mroom / /*(tot-room * day(to-date))*/ mtd-act * 100, "->>9.99") 
      + STRING(dpax, "->9") 
      + STRING(mpax, "->,>>9")
      output-list.yroom = STRING(yroom, "->,>>>,>>9")
      output-list.ypax  = STRING(ypax, "->,>>>,>>9")
      output-list.proz3 = STRING(yroom / ytd-act * 100, "->>9.99").
  IF show-avrg THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      IF droom NE 0 THEN output-list.str = output-list.str 
        + STRING(drev / droom, "->,>>>,>>9.99"). 
      ELSE output-list.str = output-list.str + STRING(0, "->,>>>,>>9.99"). 
      IF mroom NE 0 THEN output-list.str = output-list.str 
        + STRING(mrev / mroom, "->,>>>,>>9.99"). 
      ELSE output-list.str = output-list.str + STRING(0, "->,>>>,>>9.99"). 
      IF yroom NE 0 THEN output-list.yrate = 
         STRING(yrev / yroom, "->,>>>,>>9.99"). 
      ELSE output-list.yrate =  STRING(0, "->,>>>,>>9.99"). 
    END. 
    ELSE 
    DO: 
      IF droom NE 0 THEN output-list.str = output-list.str 
        + STRING(drev / droom, "->>>,>>>,>>9"). 
      ELSE output-list.str = output-list.str + STRING(0, "->>>,>>>,>>9"). 
      IF mroom NE 0 THEN output-list.str = output-list.str 
        + STRING(mrev / mroom, "->>>,>>>,>>9"). 
      ELSE output-list.str = output-list.str + STRING(0, "->>>,>>>,>>9"). 
      IF yroom NE 0 THEN output-list.yrate =
         STRING(yrev / yroom, "->>>,>>>,>>9"). 
      ELSE output-list.yrate = STRING(0, "->,>>>,>>>,>>9"). 
    END. 
  END. 
  ELSE output-list.str 
    = output-list.str + STRING(" ", "x(13)") + STRING(" ", "x(13)").
  IF NOT long-digit THEN 
  ASSIGN
      output-list.str = output-list.str 
      + STRING(drev, "->>,>>>,>>9.99") 
      + STRING(mrev, ">>>,>>>,>>>,>>9.99")
      output-list.yrev = STRING(yrev, "->>>,>>>,>>>,>>9.99"). 
  ELSE
      ASSIGN
          output-list.str = output-list.str 
            + STRING(drev, "->>>,>>>,>>9") 
            + STRING(mrev, "->>>,>>>,>>>,>>9")
          output-list.yrev = STRING(yrev, "->>>>,>>>,>>>,>>9")
      . 
 
  IF rev-title1 NE "" THEN 
  DO: 
    CREATE output-list. 
    output-list.str = "   " + STRING(rev-title1,"x(16)") 
      + STRING(0, ">>>"). 
    IF droom NE 0 THEN output-list.str = output-list.str 
      + STRING((dpax - droom) / droom * 100, "->>9.99") + STRING(0,">,>>>"). 
    ELSE output-list.str = output-list.str 
      + STRING(0, "->>9.99") /*M*/ + STRING(0, ">,>>>"). 
    IF mroom NE 0 THEN output-list.str = output-list.str 
      + STRING((mpax - mroom) / mroom * 100, "->>9.99"). 
    ELSE output-list.str = output-list.str + STRING(0, "->>9.99"). 
    output-list.str = output-list.str + STRING(0, ">>>") + STRING(0, ">>,>>>"). 
    IF yroom NE 0 THEN output-list.proz3
      = STRING((ypax - yroom) / yroom * 100, "->>9.99"). 
    ELSE output-list.proz3 = STRING(0, "->>9.99").  /*M*/
  END. 
 
  CREATE output-list. 
  ASSIGN
      output-list.str   = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 17)
      .
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
END. 


PROCEDURE cal-umsatz2: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 

  dooo = 0. 
  mooo = 0.
  yooo = 0.
  DO datum = from-date TO to-date: 
    FIND FIRST zinrstat WHERE zinrstat.datum = datum 
      AND zinrstat.zinr = "ooo" NO-LOCK NO-ERROR. 
    IF AVAILABLE zinrstat THEN 
    DO: 
      IF datum = to-date THEN dooo = zinrstat.zimmeranz. 
      /*IF MONTH(datum) = month(to-date) THEN mooo = mooo + zinrstat.zimmeranz. */
      IF (mi-mtd-chk AND MONTH(zinrstat.datum) = MONTH(to-date))
          OR (mi-ftd-chk AND zinrstat.datum GE fdate AND zinrstat.datum LE tdate) THEN
          mooo = mooo + zinrstat.zimmeranz.
      yooo = yooo + zinrstat.zimmeranz.
    END. 
  END. 
  
  dvacant = tot-room - dooo - droom.
  mvacant = mtd-act - mooo - mroom.
  yvacant = ytd-act - yooo - yroom.
  
  IF to-date = opening-date THEN 
  DO:
      mvacant = dvacant.
      yvacant = dvacant.
      mooo = dooo.
      yooo = dooo.
  END.
  
  CREATE output-list. 
  ASSIGN
  output-list.str = "   " + STRING(translateExtended ("V A C A N T",lvCAREA,""),"x(16)") 
      + STRING(dvacant, "->9") 
      + STRING(dvacant / tot-room * 100, "->>9.99") 
      + STRING(mvacant, "->,>>9") /**/
      + STRING(mvacant / /*(tot-room * day(to-date))*/ mtd-act * 100, "->>9.99") 
      + STRING(0, ">>>") 
      + STRING(0, ">>>>>>") 
      + STRING("", "x(13)") 
      + STRING("", "x(13)") 
      + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>>>")
      output-list.yroom = STRING(yvacant, "->,>>>,>>9")
      output-list.proz3 = STRING(yvacant / ytd-act * 100, "->>9.99")
      .
  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(translateExtended ("Out Of Order",lvCAREA,""),"x(16)") 
      + STRING(dooo, ">>9") 
      + STRING(dooo / tot-room * 100, "->>9.99") 
      + STRING(mooo, ">>,>>9") 
      + STRING(mooo / /*(tot-room * day(to-date))*/ mtd-act * 100, "->>9.99")  /*M*/
      + STRING(0, ">>>") 
      + STRING(0, ">>>>>>") 
      + STRING("", "x(13)") 
      + STRING("", "x(13)") 
      + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>>>")
      output-list.yroom = STRING(yooo, "->,>>>,>>9")
      output-list.proz3 = STRING(yooo / ytd-act * 100, "->>9.99").
  CREATE output-list. 
  ASSIGN
      output-list.str = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 19).
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
  
  FIND FIRST zinrstat WHERE zinrstat.zinr = "tot-rm" AND zinrstat.datum = to-date
      NO-LOCK NO-ERROR.
  IF AVAILABLE zinrstat THEN all-room = zinrstat.zimmeranz.
  
  /*MTIF MONTH(to-date) = MONTH(opening-date) THEN
  DO:
      mtd-totrm = all-room.
      ytd-totrm = all-room.
  END.*/

  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(translateExtended ("# Active Rooms",lvCAREA,""),"x(16)") 
      + STRING(tot-room, ">>9") 
      + STRING(100, "->>9.99")  /*M*/
      + STRING(mtd-act, ">>,>>9") 
      + STRING(100, "->>9.99")  /*M*/
      + STRING(0, ">>>") 
      + STRING(0, ">>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>>>")
      output-list.yroom = STRING(ytd-act, "->,>>>,>>9")
      . 
  
  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(translateExtended ("Inactive Rooms",lvCAREA,""),"x(16)") 
      /* + STRING(inactive, ">>9") */ /*20 Feb 09 */
     + STRING(all-room - tot-room, ">>9")
      + STRING("", ">>>>>>") 
      + STRING((mtd-totrm - mtd-act), ">>>>>>") 
      + STRING("", ">>>>>>") 
      + STRING(0, ">>>") 
      + STRING(0, ">>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>>>")
      output-list.yroom = STRING(ytd-totrm - ytd-act, "->,>>>,>>9")
      . 
 
  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(translateExtended ("Total Rooms",lvCAREA,""),"x(16)") 
      /* + STRING(tot-room + inactive, ">>9") */ 
      + STRING(all-room, ">>9")
      + STRING("", ">>>>>>") 
      + STRING(mtd-totrm, ">>>>>>") 
      + STRING("", ">>>>>>") 
      + STRING(0, ">>>") 
      + STRING(0, ">>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>>>>")
      output-list.yroom = STRING(ytd-totrm , "->,>>>,>>9")
      .
 
  CREATE output-list. 
  ASSIGN
      output-list.str = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 17).
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
END. 
 

PROCEDURE cal-umsatz3: 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE max-i       AS INTEGER INITIAL 0.
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE art-list    AS INTEGER EXTENT 150. 
DEFINE VARIABLE serv-vat    AS LOGICAL. 
DEFINE VARIABLE fact        AS DECIMAL. 
DEFINE VARIABLE serv        AS DECIMAL. 
DEFINE VARIABLE vat         AS DECIMAL.
DEFINE VARIABLE drev-droom  AS DECIMAL.
DEFINE VARIABLE mrev-mroom  AS DECIMAL.
/*MT 31/05/13 */
DEFINE VARIABLE drev-droom1 AS DECIMAL.
DEFINE VARIABLE mrev-mroom1 AS DECIMAL.


  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH artikel WHERE artikel.departement = 0
      AND artikel.artart = 0 AND artikel.umsatzart = 1 NO-LOCK 
      BY artikel.artnr:
      max-i = max-i + 1.
      art-list[max-i] = artikel.artnr.
  END.


  IF do-it THEN
  DO:
  END.
  ELSE
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
                drev = drev + umsatz.betrag / fact. 
                cl-list.drev = umsatz.betrag / fact. 
              END. 
              
              IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
                OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
    
              DO:
                  mrev = mrev + umsatz.betrag / fact. 
                  cl-list.mrev = cl-list.mrev + umsatz.betrag / fact. 
              END.
              ASSIGN
                  yrev = yrev + umsatz.betrag / fact. 
                  cl-list.yrev = cl-list.yrev + umsatz.betrag / fact. 
            END. 
          END. 
          IF cl-list.mrev NE 0 THEN 
          DO: 
            CREATE output-list. 
            IF NOT long-digit THEN 
            output-list.str = "   " + STRING(cl-list.bezeich,"x(16)") 
              + STRING(0, ">>>") 
              + STRING(0, ">>>>>>") 
              + STRING(0, ">>>>>>")  /*FT 23/08/12 */
              + STRING(0, ">>>>>>") 
              + STRING(0, ">>>") 
              + STRING(0, ">>>>>>") 
              + STRING("", "x(13)") 
              + STRING("", "x(13)") 
              + STRING(cl-list.drev, "->>,>>>,>>9.99") 
              + STRING(cl-list.mrev, "->>>>,>>>,>>9.99"). 
            ELSE 
            output-list.str = "   " + STRING(cl-list.bezeich,"x(16)") 
              + STRING(0, ">>>") 
              + STRING(0, ">>>>>>") 
              + STRING(0, ">>>>>>") /*FT 23/08/12 */
              + STRING(0, ">>>>>>") 
              + STRING(0, ">>>") 
              + STRING(0, ">>>>>>") 
              + STRING(0, ">>>>>>>>>>>>>") 
              + STRING(0, ">>>>>>>>>>>>>") 
              + STRING(cl-list.drev, ">>,>>>,>>>,>>9") 
              + STRING(cl-list.mrev, ">>>>,>>>,>>>,>>9"). 
          END.
        END. 
      END. 
      
      CREATE output-list. 
      ASSIGN
          output-list.str = "   "
          output-list.yroom = FILL("-", 10)
          output-list.proz3 = FILL("-", 6)
          output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
          output-list.yrate = FILL("-", 13)
          output-list.yrev  = FILL("-", 17).
      DO i = 1 TO 96: 
        output-list.str = output-list.str + "----". 
      END. 
  END.
 
 
  IF mi-excHU-chk = TRUE THEN
      ASSIGN
      ncompli = ncompli - dHU
      mtd-ncompli = mtd-ncompli - mHU
      ytd-ncompli = ytd-ncompli - yHU.

  IF mi-excComp-chk = TRUE THEN
      ASSIGN
      ncompli = ncompli - dCompli
      mtd-ncompli = mtd-ncompli - mCompli
      ytd-ncompli = ytd-ncompli - yCompli.
  
  drev-droom  = drev / droom.
  drev-droom1 = drev / droomRev.        /*MT 31/05/13 */
  IF drev-droom EQ ? THEN drev-droom = 0.
  IF drev-droom1 EQ ? THEN drev-droom1 = 0.
  
  mrev-mroom  = mrev / mroom.
  mrev-mroom1 = mrev / mroomRev.        /*MT 31/05/13 */
  IF mrev-mroom EQ ? THEN mrev-mroom = 0.
  IF mrev-mroom1 EQ ? THEN mrev-mroom1 = 0.
  
  IF NOT long-digit THEN 
  DO: 
      /*MT 31/05/13 */
      CREATE output-list. 
      ASSIGN
          output-list.str = "   " + STRING(translateExtended ("RmRev Inc Comp",lvCAREA,""),"x(16)") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>>>>") /*FT 23/08/12 */
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(drev-droom, "->,>>>,>>9.99") 
            + STRING(mrev-mroom, "->,>>>,>>9.99") 
            + STRING(drev, ">>>,>>>,>>9.99") 
            + STRING(mrev, ">>>,>>>,>>>,>>9.99")
          output-list.yrev = STRING(yrev, "->>>,>>>,>>>,>>9.99").
          IF yroom NE 0 THEN
            output-list.yrate = STRING(yrev / Yroom, "->,>>>,>>9.99"). 

      CREATE output-list. 
      ASSIGN
          output-list.str = "   " + STRING(translateExtended ("RmRev Exc Comp",lvCAREA,""),"x(16)") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>>>>") /*FT 23/08/12 */
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(drev-droom1, "->,>>>,>>9.99") 
            + STRING(mrev-mroom1, "->,>>>,>>9.99") 
            + STRING(drev, ">>>,>>>,>>9.99") 
            + STRING(mrev, ">>>,>>>,>>>,>>9.99")
          output-list.yrev = STRING(yrev, "->>>,>>>,>>>,>>9.99").
          IF yroomrev NE 0 THEN
            output-list.yrate = STRING(yrev / Yroomrev, "->,>>>,>>9.99"). /*FT 28/02/14*/
  END.
  ELSE 
  DO:
      /*MT 31/05/13 */
      CREATE output-list. 
      ASSIGN
          output-list.str = "   " + STRING(translateExtended ("Total RmRevenue (comp guest)",lvCAREA,""),"x(30)") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>>>>") /*FT 23/08/12 */
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(drev-droom, "->>>,>>>,>>>") 
            + STRING(mrev-mroom, "->>>,>>>,>>>") 
            + STRING(drev, ">>,>>>,>>>,>>9") 
            + STRING(mrev, ">>>>,>>>,>>>,>>9")
          output-list.yrev = STRING(yrev, "->>>,>>>,>>>,>>>,>>9") .

      CREATE output-list. 
      ASSIGN
          output-list.str = "   " + STRING(translateExtended ("Total RmRevenue (paying guest)",lvCAREA,""),"x(30)") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>>>>") /*FT 23/08/12 */
            + STRING(0, ">>>>>>") 
            + STRING(0, ">>>") 
            + STRING(0, ">>>>>>") 
            + STRING(drev-droom1, "->>>,>>>,>>>") 
            + STRING(mrev-mroom1, "->>>,>>>,>>>") 
            + STRING(drev, ">>,>>>,>>>,>>9") 
            + STRING(mrev, ">>>>,>>>,>>>,>>9")
          output-list.yrev = STRING(yrev, "->>>>,>>>,>>>,>>9") .
  END.
  /*FT 28/02/14IF yroom NE 0 THEN
      output-list.yrate = STRING(yrev / Yroom, "->>>,>>>,>>>"). */
  CREATE output-list. 
  ASSIGN
      output-list.str = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 19).
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
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
    
    IF (mi-mtd-chk AND MONTH(datum) = MONTH(to-date))
            OR (mi-ftd-chk AND datum GE fdate AND datum LE tdate) THEN
        mnoshow = mnoshow + zinrstat.zimmeranz.
    ynoshow = ynoshow + zinrstat.zimmeranz.
  END.
  FOR EACH zinrstat NO-LOCK WHERE 
    zinrstat.zinr = "CancRes"   AND 
    zinrstat.datum GE from-date AND
    zinrstat.datum LE to-date:
    IF zinrstat.datum = to-date THEN dcancel = dcancel + zinrstat.zimmeranz.
    IF MONTH(datum) = MONTH(to-date) THEN ASSIGN mcancel = mcancel + zinrstat.zimmeranz.
    ycancel = ycancel + zinrstat.zimmeranz.
  END.

  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(translateExtended ("NO SHOW",lvCAREA,""),"x(16)") 
      + STRING(dnoshow, ">>9") 
      + STRING(0, "->>9.99")  /*M*/
      + STRING(mnoshow, ">>,>>9") 
      + STRING(0, ">>>>>>") 
      + STRING(0, ">>>") 
      + STRING(0, ">>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>>>")
      output-list.yroom = STRING(ynoshow, "->,>>>,>>9").
  CREATE output-list. 
  ASSIGN
      output-list.str = "   " + STRING(translateExtended ("C A N C E L",lvCAREA,""),"x(16)") 
      + STRING(dcancel, ">>9") 
      + STRING(0, "->>9.99")  /*M*/
      + STRING(mcancel, ">>,>>9") 
      + STRING(0, ">>>>>>") 
      + STRING(0, ">>>") 
      + STRING(0, ">>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>") 
      + STRING(0, ">>>>>>>>>>>>>>>>")
      output-list.yroom = STRING(ycancel, "->,>>>,>>9").
  CREATE output-list. 
  ASSIGN
      output-list.str = "   "
      output-list.yroom = FILL("-", 10)
      output-list.proz3 = FILL("-", 6)
      output-list.ypax  = FILL("-", 10) /*SIS 29/11/12 */
      output-list.yrate = FILL("-", 13)
      output-list.yrev  = FILL("-", 17).
  DO i = 1 TO 96: 
    output-list.str = output-list.str + "----". 
  END. 
END. 
