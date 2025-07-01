
DEFINE TEMP-TABLE room-list 
  FIELD wd            AS INTEGER 
  FIELD datum         AS DATE 
  FIELD bezeich       AS CHAR FORMAT "x(15)" FONT 2 
  FIELD room          AS DECIMAL FORMAT " >>9.99" EXTENT 17 
    INITIAL [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
  FIELD coom          AS CHAR EXTENT /*21*/ 17 FORMAT "x(7)" FONT 2 INITIAL "" 
  FIELD k-pax         AS INTEGER INITIAL 0
  FIELD t-pax         AS INTEGER INITIAL 0
  /*FIELD lodg         AS DECIMAL EXTENT 5 FORMAT "->>>,>>>,>>>,>>9.99" */
  FIELD lodg          AS DECIMAL EXTENT 7 FORMAT "->>>,>>>,>>>,>>>,>>9.99" /*will*/
  FIELD avrglodg      AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99"
  FIELD avrglodg2     AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99"
  FIELD avrgrmrev     AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" FONT 2 /*MT 17/10/13 */
  FIELD avrgrmrev2    AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" FONT 2 
  /*FIELD others       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" EXTENT 4 */
  FIELD others        AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" EXTENT 8 FONT 2
  FIELD ly-fcast      AS CHAR    FORMAT "x(7)"  FONT 2
  FIELD ly-actual     AS CHAR    FORMAT "x(7)"  FONT 2
  FIELD ly-avlodge    AS CHAR    FORMAT "x(13)" FONT 2
  FIELD room-excComp  AS INT INIT 0
  FIELD room-comp     AS INT INIT 0
  FIELD fixleist      AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" /* Add by Michael @ 16/11/2018 for Quest San Hotel - ticket no EE3EC9 */
  FIELD fixleist2     AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" /*Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9 */
  FIELD rmrate        AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99"
  FIELD rmrate2       AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" 
  FIELD revpar        AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99"
  FIELD revpar2       AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99"
/*MG A2A1B4*/
  FIELD avrglodg-inclcomp AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99"
  FIELD avrglodg-exclcomp AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99"
  FIELD rmocc-exclcomp    AS DECIMAL FORMAT ">>9.99".


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

/*ITA 290318*/
DEFINE TEMP-TABLE outlook-list
    FIELD SELECTED   AS LOGICAL INITIAL NO
    FIELD outlook-nr AS INTEGER
    FIELD bezeich    AS CHAR FORMAT "x(16)".

DEFINE TEMP-TABLE print-list
    FIELD code-name AS CHAR FORMAT "x(80)".

DEFINE TEMP-TABLE print-list2
    FIELD argm AS CHAR FORMAT "x(80)".

DEFINE TEMP-TABLE print-list3
    FIELD room AS CHAR FORMAT "x(80)".

DEFINE INPUT  PARAMETER TABLE FOR segm-list.
DEFINE INPUT  PARAMETER TABLE FOR argt-list.
DEFINE INPUT  PARAMETER TABLE FOR zikat-list.
DEFINE INPUT  PARAMETER TABLE FOR outlook-list.
DEFINE INPUT  PARAMETER pvILanguage      AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER op-type          AS INTEGER.
DEFINE INPUT  PARAMETER flag-i           AS INT.
DEFINE INPUT  PARAMETER curr-date        AS DATE.
DEFINE INPUT  PARAMETER to-date          AS DATE.
DEFINE INPUT  PARAMETER all-segm         AS LOGICAL. 
DEFINE INPUT  PARAMETER all-argt         AS LOGICAL.
DEFINE INPUT  PARAMETER all-zikat        AS LOGICAL.
DEFINE INPUT  PARAMETER exclOOO          AS LOGICAL.
DEFINE INPUT  PARAMETER incl-tent        AS LOGICAL. 
DEFINE INPUT  PARAMETER show-rev         AS INTEGER. 
DEFINE INPUT  PARAMETER vhp-limited      AS LOGICAL.
DEFINE INPUT  PARAMETER excl-compl       AS LOGICAL.
DEFINE INPUT  PARAMETER all-outlook      AS LOGICAL.
DEFINE INPUT  PARAMETER incl-oth         AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "occ-fcast1".

DEFINE BUFFER rline1 FOR res-line. 

DEF VAR tot-rmrev AS DECIMAL INITIAL 0.
DEFINE TEMP-TABLE active-rm-list
    FIELD datum     AS DATE
    FIELD zimmeranz AS INTEGER INIT 0
.

DEFINE TEMP-TABLE dayuse-list
    FIELD datum     AS DATE
    FIELD zimmeranz AS INTEGER INIT 0
    FIELD pax       AS INTEGER INIT 0
.

DEFINE VARIABLE bonus-array         AS LOGICAL EXTENT 999 INITIAL NO. 

DEFINE VARIABLE week-list AS CHAR EXTENT 7 FORMAT "x(3)" 
  INITIAL ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]. 

DEFINE VARIABLE tent-pers       AS INTEGER NO-UNDO.
DEFINE VARIABLE datum           AS DATE.
DEFINE VARIABLE tot-room        AS INTEGER. 
DEFINE VARIABLE mtd-tot-room    AS INTEGER. 
DEFINE VARIABLE accum-tot-room  AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE actual-tot-room AS INTEGER. 

DEFINE VARIABLE segm-name       AS CHAR FORMAT "x(500)".
DEFINE VARIABLE argm-name       AS CHAR FORMAT "x(500)".
DEFINE VARIABLE room-name       AS CHAR FORMAT "x(500)".

DEFINE VARIABLE ci-date         AS DATE. 
DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 
DEFINE VARIABLE t-lodg          AS DECIMAL FORMAT "->>>,>>>,>>9.99" EXTENT 7.
DEFINE VARIABLE jml-date        AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE tot-avrg        AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-rmrate        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". /*willi*/
DEFINE VARIABLE t-rmrate2       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE t-revpar        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE t-revpar2       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".

DEFINE VARIABLE price           AS INTEGER NO-UNDO. /* Dzikri 796D85 - arrangement fixcost */

DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE new-contrate    AS LOGICAL INITIAL NO     NO-UNDO. 
/*DEFINE VARIABLE exchg-rate      AS DECIMAL.*/
DEFINE VARIABLE rm-vat          AS LOGICAL.
DEFINE VARIABLE rm-serv         AS LOGICAL.
DEFINE VARIABLE rm-array        AS INTEGER EXTENT 18.  /* FOR calculation OF TOTAL */ 
DEFINE VARIABLE exchg-rate      AS DECIMAL NO-UNDO.
DEFINE VARIABLE sum-comp        AS DECIMAL NO-UNDO.
DEFINE VARIABLE post-it         AS LOGICAL NO-UNDO.
DEFINE VARIABLE fcost           AS DECIMAL NO-UNDO.

DEFINE STREAM s1.
 
/**********MAIN LOGIC********/
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
ELSE exchg-rate = 1. 
FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
rm-vat = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
rm-serv = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 

DEFINE VARIABLE curr-time AS INTEGER.
DEFINE VARIABLE tmpInt    AS INTEGER NO-UNDO.

ASSIGN
  tmpInt = to-date - curr-date
  tmpInt = tmpInt + 1.

CASE op-type:
    WHEN 0 THEN
    DO: 
       IF curr-date LT ci-date THEN RUN create-browse. 
       ELSE RUN create-browse1.
       RUN segm-code-name.      
       RUN room-code-name.
       RUN argt-code-name.       
    END.
END CASE.

/**********PROCEDURE********/
/*FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs AS INTEGER, 
     INPUT kind1 AS INTEGER, 
     INPUT kind2 AS INTEGER). 
  DEF VAR rate AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN 
      rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. FT serverless*/

PROCEDURE create-browse:  /*history*/
DEFINE VARIABLE curr-i      AS INTEGER.
DEFINE VARIABLE net-lodg    AS DECIMAL.
DEFINE VARIABLE Fnet-lodg   AS DECIMAL.
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE datum1      AS DATE. 
DEFINE VARIABLE datum2      AS DATE. 
DEFINE VARIABLE d2          AS DATE. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE wd          AS INTEGER. 
DEFINE VARIABLE p-room      AS INTEGER. 
DEFINE VARIABLE prev-room   AS INTEGER. 
DEFINE VARIABLE p-pax       AS INTEGER. 
DEFINE VARIABLE avrg-rate   AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL. 
DEFINE VARIABLE consider-it AS LOGICAL. 
DEFINE VARIABLE dayuse-flag AS LOGICAL. 

DEFINE VARIABLE kont-doit   AS LOGICAL.
DEFINE VARIABLE allot-doit  AS LOGICAL.
DEFINE VARIABLE mtd-occ     AS DECIMAL NO-UNDO.
DEFINE VARIABLE rmsharer    AS LOGICAL INITIAL NO.
DEFINE VARIABLE othRev      AS DECIMAL.

DEFINE VARIABLE tavg-rmrev    AS DECIMAL.
DEFINE VARIABLE tavg-rmrev2   AS DECIMAL.

DEFINE VARIABLE troom-excComp AS INT.

DEFINE VARIABLE rsvStat         AS CHAR    NO-UNDO.
DEFINE VARIABLE avrg-lodging    AS DECIMAL NO-UNDO.
DEFINE VARIABLE avrg-rmrate     AS DECIMAL NO-UNDO.
DEFINE VARIABLE avrg-lodging2   AS DECIMAL NO-UNDO.
DEFINE VARIABLE avrg-rmrate2    AS DECIMAL NO-UNDO.

DEFINE VARIABLE anzahl-dayuse AS INTEGER NO-UNDO.

DEFINE BUFFER s-list FOR segm-list. 
DEFINE BUFFER a-list FOR argt-list. 
DEFINE BUFFER z-list FOR zikat-list. 
DEFINE BUFFER kline  FOR kontline.
DEFINE BUFFER o-list FOR outlook-list.

DEFINE VAR tot-breakfast    AS DECIMAL.
DEFINE VAR tot-Lunch        AS DECIMAL.
DEFINE VAR tot-dinner       AS DECIMAL.
DEFINE VAR tot-Other        AS DECIMAL.
DEFINE VAR tot-fixcost      AS DECIMAL.
DEFINE VAR tot-fixcost2     AS DECIMAL.

DEFINE VAR sum-breakfast    AS DECIMAL.
DEFINE VAR sum-Lunch        AS DECIMAL.
DEFINE VAR sum-dinner       AS DECIMAL.
DEFINE VAR sum-Other        AS DECIMAL.
DEFINE VAR sum-breakfast-usd    AS DECIMAL.
DEFINE VAR sum-Lunch-usd        AS DECIMAL.
DEFINE VAR sum-dinner-usd       AS DECIMAL.
DEFINE VAR sum-Other-usd        AS DECIMAL.
DEFINE VAR tot-vat          AS DECIMAL INITIAL 0.
DEFINE VAR tot-service      AS DECIMAL INITIAL 0.
DEFINE VAR service          AS DECIMAL INITIAL 0.
DEFINE VAR vat              AS DECIMAL INITIAL 0.

DEFINE VAR rmrate           AS DECIMAL INITIAL 0.
DEFINE VAR room-excComp     AS INT.
DEFINE VAR bfast-art        AS INT.
DEFINE VARIABLE curr-zinr   AS CHAR    NO-UNDO.
DEFINE VARIABLE pax         AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-date1  AS DATE    NO-UNDO.

DEFINE VARIABLE t-avrglodg-inclcomp AS DECIMAL.
DEFINE VARIABLE t-avrglodg-exclcomp AS DECIMAL.
DEFINE VARIABLE t-rmocc-exclcomp    AS DECIMAL.
DEFINE VARIABLE t-room-comp         AS INTEGER.
DEFINE VARIABLE tmp-date AS DATE. 


  FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
  bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 

  room-excComp = 0.
  DO i = 1 TO 18: 
    rm-array[i] = 0. 
  END. 
 
  DO i = 1 TO 4: 
    t-lodg[i] = 0. 
  END. 

  tent-pers = 0.
  FOR EACH room-list: 
    delete room-list. 
  END. 
 
  actual-tot-room = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK: 
    IF all-zikat THEN actual-tot-room = actual-tot-room + 1. 
    ELSE 
    DO: 
      FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
        AND z-list.selected NO-LOCK NO-ERROR. 
      IF AVAILABLE z-list THEN actual-tot-room = actual-tot-room + 1. 
    END. 
  END. 
  
  RUN create-active-room-list.

  datum = curr-date - 1. 
  
  DO i = 1 TO tmpInt: /* FT Serverless : (to-date - curr-date + 1) */
    datum = datum + 1. 
    wd = WEEKDAY(datum) - 1. 
    IF wd = 0 THEN wd = 7. 
    RUN rsv-closeout(datum, OUTPUT rsvstat).
    CREATE room-list. 
    ASSIGN
      room-list.wd      = wd 
      room-list.datum   = datum 
      room-list.bezeich = " " + week-list[wd] + " " + STRING(datum) + rsvStat. 
  
    FOR EACH kontline WHERE kontline.ankunft LE datum AND kontline.abreise GE datum
      AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK:
      allot-doit = YES.
      IF kontline.zikatnr NE 0 AND NOT all-zikat THEN
      DO:
        FIND FIRST z-list WHERE z-list.zikatnr = kontline.zikatnr 
          AND z-list.selected NO-LOCK NO-ERROR. 
        allot-doit = AVAILABLE z-list. 
      END.
      IF allot-doit AND (datum GE (ci-date + kontline.ruecktage)) THEN
      DO:
        room-list.room[14] = room-list.room[14] + kontline.zimmeranz. 
        rm-array[14] = rm-array[14] + kontline.zimmeranz. 
      END.
    END.
  END. 
  
  /*CREATE room-list. 
  room-list.bezeich = " TOTAL".*/

  datum1 = curr-date. 
  IF to-date LT (ci-date - 1) THEN d2 = to-date. 
  ELSE d2 = ci-date - 1. 
 
  /*
  IF NOT vhp-limited THEN
  DO datum = datum1 TO d2:

    FIND FIRST zinrstat WHERE zinrstat.zinr = "Arrival"
      AND zinrstat.datum = datum NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN
    DO:
        FIND FIRST room-list WHERE room-list.datum = datum. 
        ASSIGN
          room-list.room[3] = room-list.room[3] + zinrstat.zimmeranz
          room-list.room[4] = room-list.room[4] + zinrstat.personen
                              + zinrstat.betriebsnr
          rm-array[3]       = rm-array[3] + zinrstat.zimmeranz
          rm-array[4]       = rm-array[4] + zinrstat.personen
                              + zinrstat.betriebsnr
        .
    END.
    FIND FIRST zinrstat WHERE zinrstat.zinr = "Departure"
      AND zinrstat.datum = datum NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN
    DO:
        FIND FIRST room-list WHERE room-list.datum = datum. 
        ASSIGN
          room-list.room[5] = room-list.room[5] + zinrstat.zimmeranz
          room-list.room[6] = room-list.room[6] + zinrstat.personen
                              + zinrstat.betriebsnr
          rm-array[5]       = rm-array[5] + zinrstat.zimmeranz
          rm-array[6]       = rm-array[6] + zinrstat.personen
                              + zinrstat.betriebsnr
        .
    END.   
  END.*/

  
  /*expected depart*/
  FOR EACH genstat WHERE genstat.res-date[2] GE datum1
    AND genstat.res-date[2] LE d2 
    AND genstat.resstatus NE 13 
    AND genstat.segmentcode NE 0 
    AND genstat.res-logic[2] EQ YES 
    AND genstat.zinr NE " "
    USE-INDEX gastnrmember_ix NO-LOCK,
    FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK,
    FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK,
    FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr NO-LOCK,
    FIRST segment WHERE segment.segmentcode = genstat.segmentcode 
      BY genstat.res-date[2] BY genstat.zinr BY genstat.datum:

      IF curr-zinr NE genstat.zinr THEN 
      DO:
        ASSIGN do-it = YES.
        IF do-it AND NOT all-segm THEN 
        DO: 
           FIND FIRST s-list WHERE s-list.segm = genstat.segmentcode 
             AND s-list.selected NO-LOCK NO-ERROR. 
           do-it = AVAILABLE s-list. 
        END. 
        IF do-it AND NOT all-argt THEN 
        DO: 
          FIND FIRST a-list WHERE a-list.argt = genstat.argt 
            AND a-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE a-list. 
        END. 
        IF do-it AND NOT all-zikat THEN 
        DO: 
          FIND FIRST z-list WHERE z-list.zikatnr = genstat.zikatnr 
            AND z-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE z-list. 
        END. 

            
        IF do-it THEN 
        DO:  
          ASSIGN pax = genstat.erwachs + genstat.kind1 + genstat.kind2 +  genstat.gratis.
          FIND FIRST room-list WHERE room-list.datum = genstat.res-date[2] NO-ERROR. 
          IF AVAILABLE room-list THEN
          DO:
            ASSIGN
              room-list.room[5] = room-list.room[5] + 1
              room-list.room[6] = room-list.room[6] + pax
              rm-array[5]       = rm-array[5] + 1
              rm-array[6]       = rm-array[6] + pax.
          END.
          
        END.
      END.
      ASSIGN curr-zinr  = genstat.zinr.
  END.
    
    
  /*New 11 agustus 2009*/
  FOR EACH genstat WHERE genstat.datum GE datum1 AND genstat.datum LE d2
    AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */
    AND genstat.zinr NE "" 
    USE-INDEX date_ix NO-LOCK: /*MT 13/08/12 */
    IF NOT vhp-limited THEN do-it = YES.
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
      
    rmsharer = (genstat.resstatus = 13).
     
    IF do-it AND NOT all-segm THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.segm = genstat.segmentcode 
        AND s-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE s-list. 
    END. 
    IF do-it AND NOT all-argt THEN 
    DO: 
      FIND FIRST a-list WHERE a-list.argt = genstat.argt 
        AND a-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE a-list. 
    END. 
    IF do-it AND NOT all-zikat THEN 
    DO: 
      FIND FIRST z-list WHERE z-list.zikatnr = genstat.zikatnr 
        AND z-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE z-list. 
    END. 

    /*ITA 200318*/
    IF excl-compl AND do-it THEN 
    DO:
      FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
        AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
      IF AVAILABLE segment THEN ASSIGN do-it = NO.
      ELSE
      DO:
        IF genstat.zipreis = 0 AND genstat.gratis NE 0
          AND genstat.resstatus = 6
          AND genstat.res-logic[2] EQ YES THEN ASSIGN do-it = NO.
      END.
    END.

    /*ITA 290318*/
    IF do-it AND NOT all-outlook THEN 
    DO:
      FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN 
      DO:
        FIND FIRST o-list WHERE o-list.SELECTED = YES 
          AND o-list.outlook-nr = zimmer.typ NO-LOCK NO-ERROR.
          ASSIGN do-it = AVAILABLE o-list.
      END.
    END.
        
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK NO-ERROR. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
    DO:
      FIND FIRST exrate WHERE exrate.datum = genstat.datum 
        AND exrate.artnr = waehrung.waehrungsnr NO-LOCK NO-ERROR. 
      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
    END.
      
    IF do-it THEN
    DO: 
      FIND FIRST room-list WHERE room-list.datum = genstat.datum NO-ERROR.
      IF AVAILABLE room-list THEN
      DO:
          IF genstat.res-date[1] = genstat.datum AND genstat.resstatus NE 13 THEN 
          DO:
            ASSIGN
              room-list.room[3] = room-list.room[3] + 1
              room-list.room[4] = room-list.room[4] + genstat.erwachs + genstat.kind1 
                                      + genstat.kind2 +  genstat.gratis
              rm-array[3]       = rm-array[3] + 1
              rm-array[4]       = rm-array[4] + genstat.erwachs + genstat.kind1 
                                      + genstat.kind2 +  genstat.gratis
              .
          END.
    
          IF NOT rmSharer THEN
          DO:
            ASSIGN
              room-list.room[7] = room-list.room[7] + 1
              rm-array[7] = rm-array[7] + 1.
    
            IF genstat.gratis EQ 0 THEN
              ASSIGN
                room-list.room-excComp = room-list.room-excComp + 1
                room-excComp           = room-excComp + 1.
    
            IF genstat.gratis NE 0 THEN
              ASSIGN room-list.room-comp    = room-list.room-comp + 1
                t-room-comp            = t-room-comp + 1.
          END.
    
    
    
          IF show-rev EQ 1 THEN 
          DO:
            ASSIGN room-list.lodg[4] = room-list.lodg[4] + genstat.logis
                   t-lodg[4]         = t-lodg[4]         + genstat.logis
                   room-list.lodg[5] = room-list.lodg[5] + genstat.logis  /*+ genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]*/
                   t-lodg[5]         = t-lodg[5]         + genstat.logis  /*+ genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]*/
                   room-list.rmrate  = room-list.rmrate + genstat.rateLocal. /* bily - genstat.zipreis */
          END.
          ELSE IF show-rev EQ 2 THEN
            ASSIGN room-list.lodg[4] = room-list.lodg[4] + genstat.logis
                   t-lodg[4]         = t-lodg[4]         + genstat.logis
                   room-list.lodg[5] = room-list.lodg[5] + genstat.logis  
                   t-lodg[5]         = t-lodg[5]         + genstat.logis 
                   room-list.lodg[6] = room-list.lodg[4] / exchg-rate
                   t-lodg[6]         = t-lodg[6] + (genstat.logis / exchg-rate)
                   room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                   t-lodg[7]         = t-lodg[7] + (genstat.logis / exchg-rate)
                   room-list.rmrate  = room-list.rmrate + genstat.rateLocal /* bily - genstat.zipreis */
                   room-list.rmrate2 = room-list.rmrate / exchg-rate .
          ELSE
            ASSIGN room-list.lodg[4] = 0
                   t-lodg[4]         = 0
                   room-list.lodg[5] = 0
                   t-lodg[5]         = 0
                   room-list.lodg[6] = 0
                   t-lodg[6]         = 0
                   room-list.lodg[7] = 0
                   t-lodg[7]         = 0
                   room-list.rmrate  = 0
                   room-list.rmrate2 = 0.
        
          ASSIGN
            room-list.room[8] = room-list.room[8] + genstat.erwachs + genstat.kind1
                                + genstat.kind2 + genstat.gratis + genstat.kind3
            /*room-list.lodg[4] = room-list.lodg[4] + genstat.logis*/
            rm-array[8]       = rm-array[8]       + genstat.erwachs + genstat.kind1
                                + genstat.kind2 + genstat.gratis    + genstat.kind3
            /*t-lodg[4]         = t-lodg[4]         + genstat.logis*/.
              
              
              /*FIND FIRST artikel WHERE artikel.zwkum = bfast-art NO-LOCK NO-ERROR.
              IF AVAILABLE artikel THEN
                  RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
                       artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).*/
              
              /*MT breakfast lunch dinner other */
          ASSIGN
            room-list.others[1] = room-list.others[1] + genstat.res-deci[2] 
            room-list.others[2] = room-list.others[2] + genstat.res-deci[3]
            room-list.others[3] = room-list.others[3] + genstat.res-deci[4]
            room-list.others[4] = room-list.others[4] + genstat.res-deci[5] + genstat.res-deci[6]
            room-list.others[5] = room-list.others[1] / exchg-rate
            room-list.others[6] = room-list.others[2] / exchg-rate
            room-list.others[7] = room-list.others[3] / exchg-rate
            room-list.others[8] = room-list.others[4] / exchg-rate
          .
              
          IF genstat.res-date[1] = genstat.res-date[2] /* day use */
            AND NOT rmSharer 
            AND genstat.res-logic[2] EQ YES THEN /* of active-room */
          DO:
            FIND FIRST dayuse-list WHERE dayuse-list.datum = genstat.datum NO-ERROR.
            IF NOT AVAILABLE dayuse-list THEN
            DO:
              CREATE dayuse-list.
              ASSIGN dayuse-list.datum = genstat.datum.
            END.
            dayuse-list.zimmeranz = dayuse-list.zimmeranz + 1.
          END.
    
              /* Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9*/
          FOR EACH fixleist WHERE fixleist.resnr = genstat.resnr
            AND fixleist.reslinnr = genstat.res-int[1] NO-LOCK: 
          
            FIND FIRST res-line WHERE res-line.resnr = genstat.resnr 
              AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
    
            RUN check-fixleist-posted(genstat.datum , fixleist.artnr, fixleist.departement, 
                                      fixleist.sequenz, fixleist.dekade, 
                                      fixleist.lfakt, genstat.res-date[1], genstat.res-date[2], 
                                      OUTPUT post-it). 
            ASSIGN 
              service = 0
              vat     = 0
              fcost   = 0.
    
            IF post-it THEN 
            DO:
              FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr
                AND artikel.departement = fixleist.departement NO-LOCK NO-ERROR.
              IF AVAILABLE artikel THEN
                RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
                                   artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
    
              ASSIGN fcost = fixleist.betrag * fixleist.number
                     fcost = fcost / (1 + service + vat).
    
              IF show-rev EQ 1 THEN
                ASSIGN room-list.fixleist = room-list.fixleist + fcost
                      /*tot-fixcost        = tot-fixcost + room-list.fixleist*/
                       tot-fixcost        = tot-fixcost + fcost.
              ELSE IF show-rev EQ 2 THEN
                ASSIGN room-list.fixleist = room-list.fixleist + fcost                           
                       room-list.fixleist2 = room-list.fixleist2 + (fcost / exchg-rate)
                               /*tot-fixcost         = tot-fixcost + room-list.fixleist
                       tot-fixcost2        = tot-fixcost2 + room-list.fixleist2*/
                       tot-fixcost         = tot-fixcost + fcost
                       tot-fixcost2        = tot-fixcost2 + (fcost / exchg-rate).
            END.                
          END.
              /*FIND FIRST fixleist WHERE fixleist.resnr EQ genstat.resnr NO-LOCK NO-ERROR.
              IF AVAILABLE fixleist THEN ASSIGN room-list.fixleist = room-list.fixleist + fixleist.betrag.*/
              /*End of add */
      END.
    END.
  END.

  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  ELSE exchg-rate = 1. 

  d2 = d2 + 1. 
  IF to-date GE ci-date THEN 
  FOR EACH res-line WHERE ((res-line.resstatus LE 13 
    AND res-line.resstatus NE 4
    AND res-line.resstatus NE 8
    AND res-line.resstatus NE 9 
    AND res-line.resstatus NE 10 
    AND res-line.resstatus NE 12 
    AND res-line.active-flag LE 1 
    /*AND NOT (res-line.ankunft GT to-date) FT serverless*/
    AND res-line.ankunft LE to-date
    /*AND NOT (res-line.abreise LT d2)FT serverless*/
    AND res-line.abreise GE d2)) OR
    ((res-line.active-flag = 2 AND res-line.resstatus = 8
    AND res-line.ankunft = ci-date AND res-line.abreise = ci-date) OR 
    (res-line.active-flag = 2 AND res-line.resstatus = 8 
    AND res-line.abreise = ci-date))
    AND res-line.gastnr GT 0 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK 
    USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
      NO-ERROR.
    ASSIGN
      curr-i      = 0
      dayuse-flag = NO
    .

    
    IF NOT vhp-limited THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
    END.
    
    IF do-it AND res-line.resstatus = 8
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date THEN
    DO:
      dayuse-flag = YES.     
      FIND FIRST arrangement WHERE arrangement.arrangement 
        =  res-line.arrangement NO-LOCK. 
      FIND FIRST bill-line WHERE bill-line.departement = 0
        AND bill-line.artnr = arrangement.argt-artikelnr
        AND bill-line.bill-datum = ci-date
        AND bill-line.massnr = res-line.resnr
        AND bill-line.billin-nr = res-line.reslinnr
        USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
      do-it = AVAILABLE bill-line.
    END.

    IF do-it AND NOT all-segm THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
        AND s-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE s-list. 
    END. 
    IF do-it AND NOT all-argt THEN 
    DO: 
      FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
        AND a-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE a-list. 
    END. 
    IF do-it AND NOT all-zikat THEN 
    DO: 
      FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
        AND z-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE z-list. 
    END. 
 
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
    IF do-it AND AVAILABLE zimmer THEN 
    DO: 
      FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
        AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
      IF zimmer.sleeping THEN 
      DO: 
        IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
          do-it = NO. 
      END. 
      ELSE 
      DO: 
        IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
        ELSE do-it = NO. 
      END. 
    END. 
 
    kont-doit = YES. 
    IF do-it AND (NOT all-segm) AND (res-line.kontignr LT 0) THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
        AND s-list.selected NO-LOCK NO-ERROR. 
      kont-doit = AVAILABLE s-list. 
    END. 

    /*ITA 200318*/
    IF excl-compl AND do-it THEN 
    DO:
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
      IF AVAILABLE segment THEN ASSIGN do-it = NO.
      ELSE
      DO:
        IF res-line.zipreis = 0 AND res-line.gratis NE 0
              /* SY Oct 10, 2021  
                  AND res-line.resstatus = 6 
              */
        THEN ASSIGN do-it = NO.
      END.
    END.

    /*ITA 290318*/
    IF do-it AND NOT all-outlook THEN DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer THEN DO:
              FIND FIRST o-list WHERE o-list.SELECTED = YES 
                  AND o-list.outlook-nr = zimmer.typ NO-LOCK NO-ERROR.
               ASSIGN do-it = AVAILABLE o-list.
          END.
    END.
    
    IF do-it THEN 
    DO: 
      
      IF dayuse-flag THEN
      DO:
        FIND FIRST dayuse-list WHERE dayuse-list.datum = datum
            NO-ERROR.
        IF NOT AVAILABLE dayuse-list THEN
        DO:
          CREATE dayuse-list.
          ASSIGN dayuse-list.datum = res-line.ankunft.
        END.
        IF NOT res-line.zimmerfix THEN 
          dayuse-list.zimmeranz = dayuse-list.zimmeranz + 1.
        dayuse-list.pax = dayuse-list.pax + res-line.erwachs
          + res-line.kind1.
      END.

      datum1 = d2. 
      IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
      datum2 = to-date. 
      IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.
       /*IF res-line.abreise LE datum2 THEN datum2 = res-line.abreise - 1.*/

      DO datum = datum1 TO datum2: 
        pax = res-line.erwachs. 
        net-lodg = 0.
        curr-i = curr-i + 1.
    
        IF res-line.zipreis NE 0 THEN DO:
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
              AND reslin-queasy.resnr = res-line.resnr 
              AND reslin-queasy.reslinnr = res-line.reslinnr 
              AND reslin-queasy.date1 LE datum 
              AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
              pax = reslin-queasy.number3. 
        END.

        FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
        IF AVAILABLE room-list THEN /*FT serverless*/
        DO:
            consider-it = YES. 
            IF res-line.zimmerfix /*AND datum LT ci-date*/ THEN 
            DO: 
              FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                AND rline1.reslinnr NE res-line.reslinnr 
                AND rline1.resstatus EQ 8 /*AND rline1.erwachs GT 0 */
                AND rline1.abreise GE datum NO-LOCK NO-ERROR. 
              IF AVAILABLE rline1 THEN consider-it = NO. 
            END. 
            
            IF datum = res-line.abreise THEN .
            ELSE DO:
                /* START Breakfast lunch Dinner other From Room Rev*/
                ASSIGN net-lodg      = 0
                       tot-breakfast = 0
                       tot-lunch     = 0
                       tot-dinner    = 0
                       tot-other     = 0
                       tot-rmrev     = 0
                    . 
        
                IF (show-rev EQ 1 OR show-rev EQ 2) AND res-line.zipreis GT 0 THEN DO:
                    IF incl-tent = NO THEN DO:
                        IF res-line.resstatus NE 3 THEN DO:
                            RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                     OUTPUT tot-service).                              
                        END.       
                    END.
                    ELSE RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                     OUTPUT tot-service).                      
                END.
    
                IF net-lodg = ? THEN ASSIGN net-lodg = 0.
                IF tot-rmrev = ? THEN ASSIGN tot-rmrev = 0.
                
                /* END Breakfast lunch Dinner other From Room Rev*/
                ASSIGN room-list.others[1] = room-list.others[1] + tot-breakfast
                       room-list.others[2] = room-list.others[2] + tot-lunch
                       room-list.others[3] = room-list.others[3] + tot-dinner
                       room-list.others[4] = room-list.others[4] + tot-other
                       room-list.others[5] = room-list.others[1] / exchg-rate
                       room-list.others[6] = room-list.others[2] / exchg-rate    
                       room-list.others[7] = room-list.others[3] / exchg-rate   
                       room-list.others[8] = room-list.others[4] / exchg-rate . 
    
             
    
             /* Add by Michael # 16/11/2018 for Quest San Hotel - ticket no EE3EC9*/
                FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
                    AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
                        
                    RUN check-fixleist-posted(datum , fixleist.artnr, fixleist.departement, 
                                              fixleist.sequenz, fixleist.dekade, 
                                              fixleist.lfakt, res-line.ankunft, res-line.abreise, 
                                              OUTPUT post-it). 
                    ASSIGN 
                        service = 0
                        vat     = 0
                        fcost   = 0.
        
                    IF post-it THEN DO:
    
                        FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr
                            AND artikel.departement = fixleist.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE artikel THEN
                            RUN calc-servvat.p(artikel.departement, artikel.artnr, datum, 
                                               artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
    
                        ASSIGN fcost = fixleist.betrag * fixleist.number
                               fcost = fcost / (1 + service + vat).
    
    
                        IF show-rev EQ 1 THEN
                            ASSIGN room-list.fixleist = room-list.fixleist + fcost
                                   /*tot-fixcost        = tot-fixcost + room-list.fixleist*/
                                   tot-fixcost        = tot-fixcost + fcost
                                    .
                        ELSE IF show-rev EQ 2 THEN
                            ASSIGN room-list.fixleist  = room-list.fixleist + fcost                               
                                   room-list.fixleist2 = room-list.fixleist2 + (fcost / exchg-rate)
                                   /*tot-fixcost2        = tot-fixcost2 + room-list.fixleist2
                                   tot-fixcost         = tot-fixcost + room-list.fixleist*/
                                   tot-fixcost2        = tot-fixcost2 + (fcost / exchg-rate)
                                   tot-fixcost         = tot-fixcost + fcost.
                    END.         
                END.
             /*End of add */
             /* Dzikri 796D85 - arrangement fixcost */
              FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK.
              IF AVAILABLE arrangement THEN
              DO:
                FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
                    AND argt-line.kind2 NO-LOCK: 
                      
                    RUN check-fixargt-posted(argt-line.argt-artnr, argt-line.departement, 
                            argt-line.fakt-modus, argt-line.intervall, res-line.ankunft, res-line.abreise, 
                            OUTPUT post-it).
                            
                    ASSIGN 
                        service = 0
                        vat     = 0
                        fcost   = 0.
                    
                    IF post-it THEN DO:
    
                        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr
                            AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE artikel THEN
                            RUN calc-servvat.p(artikel.departement, artikel.artnr, datum, 
                                               artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
                        IF argt-line.vt-percnt = 0 THEN 
                        DO: 
                          IF argt-line.betriebsnr = 0 THEN pax = res-line.erwachs. 
                          ELSE pax = argt-line.betriebsnr. 
                        END. 
                        ELSE IF argt-line.vt-percnt = 1 THEN pax = res-line.kind1. 
                        ELSE IF argt-line.vt-percnt = 2 THEN pax = res-line.kind2.
                        ELSE pax = 0.
                        price = 0.
                        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                            AND reslin-queasy.char1    = "" 
                            AND reslin-queasy.number1  = argt-line.departement 
                            AND reslin-queasy.number2  = argt-line.argtnr 
                            AND reslin-queasy.resnr    = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr 
                            AND reslin-queasy.number3  = argt-line.argt-artnr 
                            AND curr-date GE reslin-queasy.date1 
                            AND curr-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO:
                          FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                            AND reslin-queasy.char1    = "" 
                            AND reslin-queasy.number1  = argt-line.departement 
                            AND reslin-queasy.number2  = argt-line.argtnr 
                            AND reslin-queasy.resnr    = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr 
                            AND reslin-queasy.number3  = argt-line.argt-artnr 
                            AND curr-date GE reslin-queasy.date1 
                            AND curr-date LE reslin-queasy.date2 NO-LOCK:
                              IF reslin-queasy.deci1 NE 0 THEN price = reslin-queasy.deci1.
                              ELSE IF reslin-queasy.deci2 NE 0 THEN price = reslin-queasy.deci2.
                              ELSE IF reslin-queasy.deci3 NE 0 THEN price = reslin-queasy.deci3.
                              IF price NE 0 THEN                            
                              ASSIGN fcost = price * pax
                                     fcost = fcost / (1 + service + vat).
                              .
                          END.
                        END.
                        IF price EQ 0 THEN
                        ASSIGN fcost = argt-line.betrag * pax
                               fcost = fcost / (1 + service + vat).
                        IF show-rev EQ 1 THEN
                            ASSIGN room-list.fixleist = room-list.fixleist + fcost
                                   /*tot-fixcost        = tot-fixcost + room-list.fixleist*/
                                   tot-fixcost        = tot-fixcost + fcost
                                    .
                        ELSE IF show-rev EQ 2 THEN
                            ASSIGN room-list.fixleist  = room-list.fixleist + fcost                               
                                   room-list.fixleist2 = room-list.fixleist2 + (fcost / exchg-rate)
                                   /*tot-fixcost2        = tot-fixcost2 + room-list.fixleist2
                                   tot-fixcost         = tot-fixcost + room-list.fixleist*/
                                   tot-fixcost2        = tot-fixcost2 + (fcost / exchg-rate)
                                   tot-fixcost         = tot-fixcost + fcost.
                    END.         
                END.
              END.
             /* Dzikri 796D85 - END */
            END.
                    
            IF datum = res-line.ankunft AND (res-line.resstatus NE 3 
                OR (res-line.resstatus = 3 AND incl-tent)) AND consider-it THEN 
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND NOT res-line.zimmerfix THEN DO:
                  ASSIGN
                    room-list.room[3] = room-list.room[3] + res-line.zimmeranz
                    room-list.lodg[2] = room-list.lodg[2] + net-lodg
                    rm-array[3] = rm-array[3] + res-line.zimmeranz
                    t-lodg[2]   = t-lodg[2] + net-lodg
                  . 
    
                  IF (res-line.kontignr LT 0) AND kont-doit THEN 
                  DO: 
                      room-list.room[16] = room-list.room[16] - res-line.zimmeranz. 
                      rm-array[16] = rm-array[16] - res-line.zimmeranz. 
                  END. 
              END.
              
              ASSIGN
                room-list.room[4] = room-list.room[4] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz 
                rm-array[4] = rm-array[4] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
              . 
              IF (res-line.kontignr LT 0) AND kont-doit THEN 
              DO: 
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                  AND NOT res-line.zimmerfix THEN
                ASSIGN
                  room-list.room[16] = room-list.room[16] - res-line.zimmeranz
                  rm-array[16] = rm-array[16] - res-line.zimmeranz
                .
                ASSIGN
                  room-list.room[17] = room-list.room[17] 
                    - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                       + res-line.gratis) * res-line.zimmeranz 
                  rm-array[17] = rm-array[17] 
                    - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                       + res-line.gratis) * res-line.zimmeranz
                . 
     
                FIND FIRST kontline WHERE kontline.gastnr = res-line.gastnr 
                  AND kontline.ankunft EQ datum 
                  AND kontline.zikatnr = res-line.zikatnr 
                  AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 
                  NO-LOCK NO-ERROR. 
                IF AVAILABLE kontline THEN 
                ASSIGN
                  room-list.k-pax = room-list.k-pax 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                    - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                    * res-line.zimmeranz
                  rm-array[18] = rm-array[18] 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                       + res-line.gratis) * res-line.zimmeranz 
                    - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                    * res-line.zimmeranz
                . 
              END. 
     
              IF /*res-line.ankunft LT res-line.abreise OR dayuse-flag*/
                 res-line.ankunft LE res-line.abreise OR dayuse-flag THEN 
              DO: 
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                  AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent))
                  AND NOT res-line.zimmerfix THEN
                DO:
    
                    ASSIGN
                      room-list.room[7] = room-list.room[7] + res-line.zimmeranz 
                      room-list.lodg[4] = room-list.lodg[4] + net-lodg
                      room-list.lodg[6] = room-list.lodg[4] / exchg-rate
                      t-lodg[4]   = t-lodg[4] + net-lodg
                      t-lodg[6]   = t-lodg[6] + (net-lodg / exchg-rate)
                      rm-array[7] = rm-array[7] + res-line.zimmeranz
                    .
                    
                    /*RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                     OUTPUT tot-service).*/ /*tutup dulu*/       
                    
                    /*ft 26/11/13*/
                    IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN DO:
                      room-list.room-comp = room-list.room-comp + res-line.zimmeranz .
                      t-room-comp         = t-room-comp + res-line.zimmeranz.
                    END.
                    ELSE DO:
                        room-list.lodg[5] = room-list.lodg[5] + net-lodg.
                        t-lodg[5]         = t-lodg[5]         + net-lodg.
                        /*room-list.rmrate  = room-list.rmrate + res-line.zipreis.*/
                        room-list.rmrate  = room-list.rmrate + tot-rmrev.
                    END.
                    ASSIGN
                      room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                      room-list.room-excComp = room-list.room[7] - room-list.room-comp
                      t-lodg[7]         = t-lodg[7] + (net-lodg / exchg-rate)
                      room-list.rmrate2 = room-list.rmrate / exchg-rate.
    
                  /*
                    ASSIGN room-list.others[1] = room-list.others[1] + tot-breakfast
                           room-list.others[2] = room-list.others[2] + tot-lunch
                           room-list.others[3] = room-list.others[3] + tot-dinner
                           room-list.others[4] = room-list.others[4] + tot-other .
                  */
                    /*IF datum NE curr-date THEN
                     room-list.lodg[1] = room-list.lodg[1] + net-lodg.*/
                END. 
                 IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND res-line.resstatus NE 3 THEN
                        ASSIGN
                          room-list.room[8] = room-list.room[8] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                               + res-line.gratis) * res-line.zimmeranz 
                          rm-array[8] = rm-array[8] 
                            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                               + res-line.gratis) * res-line.zimmeranz . 
              END. 
            END. 
    
            
     
            IF datum = res-line.abreise 
              AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent))
              AND consider-it THEN 
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND NOT res-line.zimmerfix THEN
              DO:
                  ASSIGN
                    room-list.room[5] = room-list.room[5] + res-line.zimmeranz
                    room-list.lodg[3] = room-list.lodg[3] + net-lodg
                    t-lodg[3]   = t-lodg[3] + net-lodg
                    rm-array[5] = rm-array[5] + res-line.zimmeranz
                  . 
                  IF datum NE curr-date THEN
                  room-list.lodg[1] = room-list.lodg[1] + net-lodg.
              END.
    
              ASSIGN
                room-list.room[6] = room-list.room[6] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz 
                rm-array[6] = rm-array[6] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz 
              . 
    
            END. 
     
            /*IF res-line.resstatus NE 3 AND consider-it 
              AND res-line.ankunft LT res-line.abreise THEN 
            DO:*/
            IF (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent)) 
              AND res-line.resstatus NE 4 
              AND consider-it 
              AND (res-line.abreise GT res-line.ankunft 
                AND res-line.ankunft NE datum
                AND res-line.abreise NE datum) THEN 
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent))
                AND NOT res-line.zimmerfix THEN
              DO:
                  ASSIGN  
                    room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                    room-list.lodg[4] = room-list.lodg[4] + net-lodg
                    room-list.lodg[6] = room-list.lodg[4] / exchg-rate
                    rm-array[7] = rm-array[7] + res-line.zimmeranz
                    t-lodg[4]   = t-lodg[4] + net-lodg.
                    t-lodg[6]   = t-lodg[6] + (net-lodg / exchg-rate).
                    
                  
                  /*ft 26/11/13*/
                  IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN DO:
                    room-list.room-comp = room-list.room-comp + res-line.zimmeranz .
                    t-room-comp         = t-room-comp + res-line.zimmeranz.
                  END.
                  ELSE 
                   ASSIGN
                    room-list.lodg[5] = room-list.lodg[5] + net-lodg
                    t-lodg[5]         = t-lodg[5]         + net-lodg
                    room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                    t-lodg[7]         = t-lodg[7] + (net-lodg / exchg-rate)
                    room-list.room-excComp = room-list.room[7] - room-list.room-comp
                   /* room-list.rmrate  = room-list.rmrate + res-line.zipreis.*/
                    room-list.rmrate   = room-list.rmrate + tot-rmrev
                    room-list.rmrate2  = room-list.rmrate / exchg-rate
                    .
                    
                  IF datum NE curr-date THEN room-list.lodg[1] = room-list.lodg[1] + net-lodg.
              END.
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                  AND res-line.resstatus NE 3 THEN
              ASSIGN
                room-list.room[8] = room-list.room[8] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz 
                rm-array[8] = rm-array[8] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz 
              . 
              IF (res-line.kontignr LT 0) AND kont-doit THEN 
              DO: 
                /*IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                  AND NOT res-line.zimmerfix THEN*/
                ASSIGN  
                  room-list.room[16] = room-list.room[16] - res-line.zimmeranz
                  rm-array[16] = rm-array[16] - res-line.zimmeranz
                .
                ASSIGN
                  room-list.room[17] = room-list.room[17] 
                    - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                       + res-line.gratis) * res-line.zimmeranz 
                  rm-array[17] = rm-array[17] 
                    - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                       + res-line.gratis) * res-line.zimmeranz 
                . 
     
                FIND FIRST kontline WHERE kontline.gastnr = res-line.gastnr 
                  AND kontline.ankunft EQ datum 
                  AND kontline.zikatnr = res-line.zikatnr 
                  AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 
                  NO-LOCK NO-ERROR. 
                IF AVAILABLE kontline THEN 
                ASSIGN 
                  room-list.k-pax = room-list.k-pax 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                    - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                    * res-line.zimmeranz
                  rm-array[18] = rm-array[18] 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                    - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                    * res-line.zimmeranz
                . 
              END. 
            END.
    
            /*IF datum = curr-date AND res-line.ankunft LE (datum - 1) THEN 
            DO: 
              consider-it = YES. 
              IF res-line.zimmerfix AND datum LT ci-date THEN 
              DO: 
                FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                  AND rline1.reslinnr NE res-line.reslinnr 
                  AND rline1.resstatus EQ 8 AND rline1.erwachs GT 0 
                  AND rline1.abreise GT (datum - 1) NO-LOCK NO-ERROR. 
                IF AVAILABLE rline1 THEN consider-it = NO. 
              END. 
              IF consider-it THEN 
              DO: 
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND
                 NOT res-line.zimmerfix THEN
                ASSIGN  
                  room-list.room[1] = room-list.room[1] + res-line.zimmeranz
                  room-list.lodg[1] = room-list.lodg[1] + net-lodg
                  /*MT 07/06/12 */
                  rm-array[1] = rm-array[1] + res-line.zimmeranz
                .
    
                ASSIGN
                  room-list.room[2] = room-list.room[2] 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz
                  rm-array[2] = rm-array[2] + room-list.room[2]
                .
              END. 
            END. */
            IF res-line.resstatus = 3 AND datum LT res-line.abreise THEN DO:
                   ASSIGN 
                      room-list.room[13] = room-list.room[13] + res-line.zimmeranz
                      rm-array[13] = rm-array[13] + res-line.zimmeranz
                      room-list.t-pax = room-list.t-pax + (res-line.erwachs * res-line.zimmeranz)
                      tent-pers = tent-pers + (res-line.erwachs * res-line.zimmeranz)
                      room-list.lodg[4] = room-list.lodg[4] + net-lodg. 
                      room-list.lodg[6] = room-list.lodg[4] / exchg-rate. 
    
                      IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN DO:
                          room-list.room-comp = room-list.room-comp + res-line.zimmeranz.
                          t-room-comp         = t-room-comp + res-line.zimmeranz.
                      END.
                      ELSE 
                          ASSIGN
                            room-list.lodg[5] = room-list.lodg[5] + net-lodg
                            t-lodg[5]         = t-lodg[5]         + net-lodg
                            room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                            t-lodg[7]         = t-lodg[7] + (net-lodg / exchg-rate)
                            /*room-list.rmrate  = room-list.rmrate + res-line.zipreis*/
                            room-list.rmrate   = room-list.rmrate + tot-rmrev
                            room-list.rmrate2  = room-list.rmrate / exchg-rate.
                            
            END.        
            
            IF res-line.kontignr > 0 /* AND NOT res-line.zimmerfix */
              AND res-line.active-flag LE 1 AND res-line.resstatus LE 6
              AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
              AND res-line.abreise GT datum THEN 
            DO: 
              FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
                AND kline.kontstat = 1 NO-LOCK NO-ERROR.
              IF AVAILABLE kline THEN DO:
                  FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
                    AND kontline.ankunft LE datum AND kontline.abreise GE datum
                    AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 
                    NO-LOCK NO-ERROR.
                  IF AVAILABLE kontline AND datum GE (ci-date + kontline.ruecktage) THEN
                  DO:
                    room-list.room[14] = room-list.room[14] - res-line.zimmeranz. 
                    rm-array[14] = rm-array[14] - res-line.zimmeranz. 
                  END.
              END.          
            END.
        END.
        
      END. 
    END. 
    PROCESS EVENTS. 
  END. 
 
  DO datum = d2 TO to-date: 
    FOR EACH kontline WHERE kontline.ankunft LE datum 
      AND kontline.abreise GE datum AND kontline.betriebsnr = 1 
      AND kontline.kontstat = 1 NO-LOCK: 
      do-it = YES. 
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST a-list WHERE a-list.argt = kontline.arrangement 
          AND a-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE a-list. 
      END. 
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST z-list WHERE z-list.zikatnr = kontline.zikatnr 
          AND z-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE z-list. 
      END. 
      IF do-it AND NOT all-segm THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = kontline.gastnr NO-LOCK. 
        FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
          AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE guestseg THEN 
          FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.segm = guestseg.segmentcode 
            AND s-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE s-list. 
        END. 
      END. 

      /*ITA 13/01/22*/
      IF excl-compl AND do-it THEN DO:
          FIND FIRST guest WHERE guest.gastnr = kontline.gastnr NO-LOCK. 
          FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
              AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE guestseg THEN 
              FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                NO-LOCK NO-ERROR. 
          IF AVAILABLE guestseg THEN DO:
              FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
                  AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
              IF AVAILABLE segment THEN ASSIGN do-it = NO.          
          END.

      END.
 
      IF do-it THEN 
      DO: 
        FIND FIRST room-list WHERE room-list.datum = datum. 
        room-list.room[16] = room-list.room[16] + kontline.zimmeranz. 
        room-list.room[17] = room-list.room[17] 
          + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
          * kontline.zimmeranz. 
        rm-array[16] = rm-array[16] + kontline.zimmeranz. 
        rm-array[17] = rm-array[17] 
          + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
          * kontline.zimmeranz. 
      END. 
    END. 
    PROCESS EVENTS. 
  END. 

  FOR EACH room-list: 
    IF room-list.room[16] GT 0 THEN
        ASSIGN
        room-list.room[7] = room-list.room[7] + room-list.room[16]
        room-list.room[8] = room-list.room[8] + room-list.room[17] + room-list.k-pax. 

    IF incl-tent THEN
        ASSIGN
        /*room-list.room[7] = room-list.room[7] + room-list.room[13]*/
        room-list.room[8] = room-list.room[8] + room-list.t-pax
        /*room-list.room-excComp = room-list.room-excComp + room-list.room[13]*/. 
  END. 

  IF rm-array[16] GT 0 THEN
      ASSIGN
      rm-array[7] = rm-array[7] + rm-array[16] 
      rm-array[8] = rm-array[8] + rm-array[17] + rm-array[18]. 
  
  IF incl-tent THEN
      ASSIGN 
        /*rm-array[7] = rm-array[7] + rm-array[13]*/
        rm-array[8] = rm-array[8] + tent-pers.
 
  datum = curr-date - 1. 
  DO i = 1 TO tmpInt: /* FT Serverless : (to-date - curr-date + 1)*/
    datum = datum + 1. 
    FIND FIRST room-list WHERE room-list.datum = datum. 
    FOR EACH queasy WHERE queasy.key = 14 AND 
      queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK, 
      FIRST zimmer WHERE zimmer.zinr = queasy.char1 AND zimmer.sleeping NO-LOCK: 
      FIND FIRST guestseg WHERE guestseg.gastnr = queasy.number3 
        AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE guestseg THEN 
      FIND FIRST guestseg WHERE guestseg.gastnr = queasy.number3 
        NO-LOCK NO-ERROR. 
      do-it = AVAILABLE guestseg. 
      IF NOT all-segm AND do-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.segm = guestseg.segmentcode 
          AND s-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE s-list. 
      END. 
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST a-list WHERE a-list.argt = queasy.char2 
          AND a-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE a-list. 
      END. 
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
          AND z-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE z-list. 
      END. 
      IF do-it THEN 
      DO:
        room-list.room[7] = room-list.room[7] + 1. 
        room-list.room[8] = room-list.room[8] + queasy.number1. 
        rm-array[7] = rm-array[7] + 1. 
        rm-array[8] = rm-array[8] + queasy.number1. 
      END. 
    END. 
  END. 
  
  RUN cal-lastday-occ. 
  ASSIGN
    p-room    = 0 
    p-pax     = 0 
    prev-room = 0 
    datum     = curr-date - 1
  . 
  
  DO i = 1 TO tmpInt: /*FT Serverless */
    ASSIGN
      datum         = datum + 1
      anzahl-dayuse = 0
    . 
    RUN get-active-room(datum, OUTPUT tot-room).
    ASSIGN accum-tot-room = accum-tot-room + tot-room.

    FIND FIRST dayuse-list WHERE dayuse-list.datum = datum NO-ERROR.
    IF AVAILABLE dayuse-list THEN 
      anzahl-dayuse = dayuse-list.zimmeranz.

    FIND FIRST room-list WHERE room-list.datum = datum. 
    IF tot-room NE 0 THEN
    DO:
      room-list.room[9] = room-list.room[7] / tot-room * 100. 
      prev-room = prev-room + room-list.room[7]. 
      room-list.room[10] = prev-room / accum-tot-room * 100. 

      room-list.rmocc-exclcomp = (room-list.room[7] - room-list.room-comp ) / tot-room * 100.
    END.
    
    IF (room-list.room[7] - anzahl-dayuse) LT tot-room THEN 
    DO: 
      room-list.room[11] = tot-room - room-list.room[7] + anzahl-dayuse. 
      rm-array[11] = rm-array[11] + tot-room - room-list.room[7] + anzahl-dayuse. 
    END. 
    ELSE 
    DO: 
      room-list.room[12] = room-list.room[7] - tot-room - anzahl-dayuse. 
      rm-array[12] = rm-array[12] + room-list.room[7] - tot-room - anzahl-dayuse. 
    END. 
    
    IF i GT 1 THEN 
    DO:
      ASSIGN
          room-list.room[1] = p-room
          room-list.room[2] = p-pax
          /*MT 07/06/12 */
          rm-array[1] = rm-array[1] + p-room
          rm-array[2] = rm-array[2] + p-pax
          .     
    END.
    ASSIGN
        p-room = room-list.room[7]
        p-pax = room-list.room[8].
  END. 
 
  FOR EACH room-list WHERE room-list.wd NE 0: 

    IF room-list.datum LT ci-date THEN 
    DO: 
      FIND FIRST zinrstat WHERE zinrstat.zinr = "ooo" 
        AND zinr.datum = room-list.datum NO-LOCK NO-ERROR. 
      IF AVAILABLE zinrstat THEN 
      DO: 
        /*MT 31/05/12 */
        IF NOT all-zikat THEN 
        DO:
            FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
              AND z-list.selected NO-LOCK NO-ERROR. 
            IF AVAILABLE z-list THEN
                ASSIGN
                room-list.room[15] = zinrstat.zimmeranz
                rm-array[15] = rm-array[15] + zinrstat.zimmeranz. 
        END.
        ELSE
            ASSIGN
            room-list.room[15] = zinrstat.zimmeranz
            rm-array[15] = rm-array[15] + zinrstat.zimmeranz. 
      END. 
    END. 
    ELSE 
    DO: 
      FOR EACH outorder WHERE outorder.gespstart LE room-list.datum 
        AND outorder.gespende GE room-list.datum AND outorder.betriebsnr LE 1 
        NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping 
        NO-LOCK: 
        /*MT 31/05/12 */
        IF NOT all-zikat THEN 
        DO: 
            FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
              AND z-list.selected NO-LOCK NO-ERROR. 
            IF AVAILABLE z-list THEN
            ASSIGN
               room-list.room[15] = room-list.room[15] + 1
               rm-array[15] = rm-array[15] + 1. 
        END. 
        ELSE
        DO:
            room-list.room[15] = room-list.room[15] + 1. 
            rm-array[15] = rm-array[15] + 1. 
        END.
      END. 
    END. 
    
    IF exclOOO THEN
    ASSIGN
        room-list.room[11] = room-list.room[11] - room-list.room[15]
        rm-array[11] = rm-array[11] - room-list.room[15]
    .
  END. 
  
  FOR EACH room-list WHERE room-list.wd NE 0: 
    DO i = 1 TO 8: 
      room-list.coom[i] = STRING(room-list.room[i],">>>>>>9"). 
    END. 
    DO i = 9 TO 10: 
      room-list.coom[i] = STRING(room-list.room[i]," >>9.99"). 
    END. 
    DO i = 11 TO 15: 
      room-list.coom[i] = STRING(room-list.room[i], "->>>>>9"). 
    END. 
    DO i = 16 TO 17: 
      room-list.coom[i] = STRING(room-list.room[i],">>>>>>9"). 
    END. 
  END. 

  ASSIGN
    jml-date = to-date - curr-date
    jml-date = jml-date + 1.

  ASSIGN do-it = YES.
  IF show-rev EQ 1 OR show-rev EQ 2 THEN DO:
       /*ITA 201016*/
      DEFINE VARIABLE tmax    AS INTEGER NO-UNDO INIT 0.
      DEFINE VARIABLE tmin    AS INTEGER NO-UNDO INIT 0.
      DEFINE VARIABLE counter AS INTEGER NO-UNDO INIT 0.
    
      FOR EACH s-list WHERE s-list.SELECTED = YES:
          ASSIGN counter = counter + 1.
          FIND FIRST segment WHERE segment.segmentcode = s-list.segm
              NO-LOCK NO-ERROR.
          IF AVAILABLE segment THEN DO:
              IF tmin = 0 AND counter = 1 THEN DO:
                  IF segment.betriebsnr = 0 THEN
                      ASSIGN tmin = 0.
                  ELSE ASSIGN tmin = segment.betriebsnr.
              END.
              
              IF segment.betriebsnr GT tmax THEN
                  ASSIGN tmax = segment.betriebsnr.
    
              IF segment.betriebsnr LT tmin THEN
                  ASSIGN tmin = segment.betriebsnr.
          END.
      END.
        
      IF tmax LE 2 AND tmin GE 1 THEN ASSIGN do-it = NO.
      ELSE ASSIGN do-it = YES.
  END.


  IF do-it THEN DO:
      /*FT 25/10/13 --> add othRev for rmRev*/
      /*t-lodg[5] = 0.*/
      IF incl-oth THEN DO:
          FOR EACH room-list:
              RUN calc-othRev (room-list.datum, OUTPUT othRev).
              IF room-list.datum NE ? THEN /*FT serverless*/
              DO:
                IF room-list.datum LT ci-date THEN DO:
                  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK NO-ERROR. 
                  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN DO:
                      FIND FIRST exrate WHERE exrate.datum = room-list.datum 
                          AND exrate.artnr = waehrung.waehrungsnr NO-LOCK NO-ERROR. 
                      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
                  END.
                END.
                ELSE DO:
                  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
                  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
                  ELSE exchg-rate = 1. 
                END.
              END.

              ASSIGN
                  room-list.lodg[5] = room-list.lodg[5] + othRev
                  room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                  .
    
              IF room-list.wd NE 0 THEN 
                  ASSIGN 
                    t-lodg[5] = t-lodg[5] + othRev.
                    t-lodg[7] = t-lodg[7] + (othRev / exchg-rate).
          END.
      END.      
  END. /*end*/
  CREATE room-list. 
  room-list.bezeich = " TOTAL".
  FOR EACH room-list:
      tot-avrg = tot-avrg + room-list.room[9].
      IF (room-list.room[7] - room-list.room[16]) NE 0 THEN
          room-list.avrglodg  = room-list.lodg[4] / (room-list.room[7] - room-list.room[16]).
          room-list.avrglodg2 = room-list.avrglodg / exchg-rate.
      IF (room-list.room-excComp - room-list.room[16]) NE 0 THEN DO:
          ASSIGN
              room-list.avrgrmrev  = room-list.lodg[5] / (room-list.room[7] - room-list.room[16])
              room-list.avrgrmrev2 = room-list.avrgrmrev / exchg-rate
              .

          /*room-list.avrgrmrev  = room-list.lodg[5] / (room-list.room-excComp - room-list.room[16]).
          room-list.avrgrmrev2 = room-list.avrgrmrev / exchg-rate.*/
      END.
      IF room-list.wd NE 0 THEN
          /*troom-excComp = troom-excComp + (room-list.room-excComp - room-list.room[16]).*/
          troom-excComp = troom-excComp + (room-list.room[7] - room-list.room[16]).

      IF ((DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100) NE 0 THEN DO:
          ASSIGN
            room-list.revpar = (DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100
            room-list.revpar2 = room-list.revpar / exchg-rate.
      END.

      room-list.avrglodg-inclcomp = room-list.lodg[5] / room-list.room[7].
      room-list.avrglodg-exclcomp = room-list.lodg[5] / (room-list.room[7] - room-list.room-comp).
  END.

  tavg-rmrev = t-lodg[5] / troom-excComp.
  tavg-rmrev2 = tavg-rmrev / exchg-rate.

  t-avrglodg-inclcomp = t-lodg[5] / rm-array[7].
  t-avrglodg-exclcomp = t-lodg[5] / (rm-array[7] - t-room-comp).
 
  avrg-rate = tot-avrg / jml-date.

  RUN get-mtd-active-room(OUTPUT mtd-tot-room).
  ASSIGN mtd-occ = 0.
  IF mtd-tot-room NE 0 THEN DO:
    mtd-occ = rm-array[7] / mtd-tot-room * 100.
    t-rmocc-exclcomp = (rm-array[7] - t-room-comp ) / mtd-tot-room * 100.
  END.

  FIND FIRST room-list WHERE room-list.wd = 0. /* total */ 
  DO i = 1 TO 8: 
    room-list.room[i] = rm-array[i]. 
  END. 
  DO i = 11 TO 17: 
    room-list.room[i] = rm-array[i]. 
  END. 
  
  DO i = 1 TO 8: 
    room-list.coom[i] = STRING(room-list.room[i],">>>>>>9"). 
  END. 
  DO i = 11 TO 12: 
    room-list.coom[i] = STRING(room-list.room[i],">>>>>>>"). 
  END. 
  ASSIGN
      room-list.room[09] = mtd-occ
      room-list.coom[09] = STRING(mtd-occ, " >>9.99")

      room-list.coom[10] = STRING(avrg-rate," >>9.99") 
      room-list.coom[13] = STRING(rm-array[13], ">>>>>>>") 
      room-list.coom[14] = STRING(rm-array[14], ">>>>>>>") 
      room-list.coom[15] = STRING(rm-array[15], ">>>>>>>")
      room-list.lodg[2]  = t-lodg[2]
      room-list.lodg[3]  = t-lodg[3]
      room-list.lodg[4]  = t-lodg[4]
      room-list.lodg[5]  = t-lodg[5]
      room-list.lodg[6]  = t-lodg[6]
      room-list.lodg[7]  = t-lodg[7]    
  .
  DO i = 16 TO 17: 
    room-list.coom[i] = STRING(room-list.room[i],"->>>>>9"). 
  END. 
 
  ASSIGN
      mtd-occ      = 0
      avrg-lodging = 0
      avrg-rmrate  = 0
  .
  FOR EACH room-list WHERE room-list.wd NE 0:
      avrg-lodging  = avrg-lodging + room-list.avrglodg.
      avrg-rmrate   = avrg-rmrate + room-list.avrgrmrev.
      avrg-lodging2 = avrg-lodging2 + room-list.avrglodg2.
      avrg-rmrate2  = avrg-rmrate2 + room-list.avrgrmrev2.
      mtd-occ       = mtd-occ + room-list.room[9].

      sum-breakfast = sum-breakfast + room-list.others[1].
      sum-lunch     = sum-lunch + room-list.others[2].
      sum-dinner    = sum-dinner + room-list.others[3].
      sum-other     = sum-other + room-list.others[4].

      sum-breakfast-usd = sum-breakfast-usd + room-list.others[5].
      sum-lunch-usd     = sum-lunch-usd + room-list.others[6].
      sum-dinner-usd    = sum-dinner-usd + room-list.others[7].
      sum-other-usd     = sum-other-usd + room-list.others[8].
      sum-comp          = sum-comp + room-list.room-comp.
      t-revpar          = t-revpar + room-list.revpar.
      t-revpar2         = t-revpar2 + room-list.revpar2.
      t-rmrate          = t-rmrate + room-list.rmrate.
      t-rmrate2         = t-rmrate2 + room-list.rmrate2.

  END.
  
  FIND FIRST room-list WHERE room-list.wd = 0. /* total */
  IF tavg-rmrev = ? THEN tavg-rmrev = 0.
  IF tavg-rmrev2 = ? THEN tavg-rmrev2 = 0.
  ASSIGN
      /*MT 07/06/12
      room-list.coom[9]  = STRING("","x(6)")*/
      /*room-list.avrglodg   = avrg-lodging / (to-date - curr-date + 1)
      room-list.avrglodg2  = avrg-lodging2 / (to-date - curr-date + 1)FT serverless*/
      room-list.avrglodg   = avrg-lodging / tmpInt
      room-list.avrglodg2  = avrg-lodging2 / tmpInt
      room-list.avrgrmrev  = tavg-rmrev  /*(to-date - curr-date + 1)*/
      room-list.avrgrmrev2 = tavg-rmrev2
      room-list.others[1]   = sum-breakfast 
      room-list.others[2]   = sum-lunch   
      room-list.others[3]   = sum-dinner
      room-list.others[4]   = sum-other 
      room-list.others[5]   = sum-breakfast-usd 
      room-list.others[6]   = sum-lunch-usd   
      room-list.others[7]   = sum-dinner-usd
      room-list.others[8]   = sum-other-usd 
      room-list.room-comp  = sum-comp
      /*room-list.revpar     = t-revpar
      room-list.revpar2    = t-revpar2*/
      room-list.rmrate     = t-rmrate
      room-list.rmrate2    = t-rmrate2
      room-list.fixleist   = tot-fixcost
      room-list.fixleist2  = tot-fixcost2

      room-list.avrglodg-inclcomp = t-avrglodg-inclcomp
      room-list.avrglodg-exclcomp = t-avrglodg-exclcomp
      room-list.rmocc-exclcomp    = t-rmocc-exclcomp.

  IF ((DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100) NE 0 THEN DO:
      ASSIGN
        room-list.revpar = (DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100
        room-list.revpar2 = room-list.revpar / exchg-rate.
  END.

  IF room-list.room[7] NE 0 THEN
      ASSIGN
      room-list.avrglodg  = room-list.lodg[4] / room-list.room[7].
      room-list.avrglodg2 = room-list.avrglodg / exchg-rate.
      /*room-list.avrgrmrev = room-list.lodg[5] / room-list.room[7].*/
END. 
 
PROCEDURE segm-code-name:
    DEFINE BUFFER bsegm FOR segm-list.
    DEFINE VARIABLE a AS INTEGER.
    DEFINE VARIABLE d AS INTEGER INITIAL 79.
    DEFINE VARIABLE e AS INTEGER INITIAL 0.
    DEFINE VARIABLE r AS INTEGER INITIAL 1.
    DEFINE VARIABLE counter AS INTEGER.
    segm-name = "".
    
    FOR EACH print-list:
        DELETE print-list.
    END.

    IF all-segm /*:SCREEN-VALUE IN FRAME FRAME1= "Yes"*/ THEN
        segm-name = "ALL".
    ELSE IF NOT all-segm /*:SCREEN-VALUE IN FRAME FRAME1= "No"*/ THEN
    DO:                  
        FOR EACH bsegm WHERE bsegm.SELECTED EQ YES :
            IF LENGTH(bsegm.bezeich) GE 0 THEN
                    segm-name = segm-name + SUBSTRING(bsegm.bezeich,5, LENGTH(bsegm.bezeich) - 3) + "; ".           
        END. 

        IF LENGTH(segm-name) GE 0 THEN
                segm-name = SUBSTRING(segm-name,1, LENGTH(segm-name) - 2).
    END.                                                 
   
      a = LENGTH(segm-name).
      /*REPEAT WHILE a GT 80:
        IF a GT 80 THEN
        DO:
            IF SUBSTRING(segm-name,d + 1 , 1) NE ";" /*AND a - e GT LENGTH(segm-name) */THEN
            REPEAT r = e + 1 TO 80 + e:
                   r = r + d.
                   IF SUBSTRING(segm-name,r,1) EQ ";" THEN
                   DO: 
                       a = LENGTH(segm-name).
                        CREATE print-list.
                        code-name =  SUBSTRING(segm-name,e + 1,r - e).
                        IF SUBSTRING(code-name, 1, 1) = " " THEN
                           code-name = SUBSTRING(code-name, 2, (LENGTH(code-name) - 1)). /*
                        str5[c] = SUBSTRING(segm-name,e + 1,r - e ).
                        c =  c + 1.                                 */
                        a = a - r.
                        e = r.
                        d = 79.
                        LEAVE.
                   END.
                   ELSE       
                   DO:
                      r = r - d.
                      d = d - 2.
                   END.   
            END.                   
        END.
        /*ELSE IF a LT 80 THEN
        DO:              
            
           /*CREATE print-list.
           code-name = SUBSTRING(segm-name,r + 1,a).*/
           /*str5[c] =  SUBSTRING(segm-name,r + 1,a).
           c =  c + 1.                               */
           
        END.*/   
      END.
    IF a LT 80 THEN*/
    DO:              
        a = LENGTH(segm-name).
        IF a > 80  THEN
        DO:
           DO e = 1 TO a:
               counter = counter + 1.
               CREATE print-list.

               IF LENGTH(segm-name) GE 0 THEN
                    print-list.code-name = SUBSTRING(segm-name,e,80). 
               e = (counter * 80) + 1.
           END.
           /*CREATE print-list.
           code-name = SUBSTRING(segm-name,r + 1,a). 
           IF SUBSTRING(code-name, 1, 1) = " " THEN
               code-name = SUBSTRING(code-name, 2, (LENGTH(code-name) - 1)).*/
        END.
        ELSE
        DO:
           CREATE print-list.
           IF LENGTH(segm-name) GE 0 THEN         
             print-list.code-name = SUBSTRING(segm-name,r,a). 
            
           /*
           IF SUBSTRING(code-name, 1, 1) = " " THEN
               print-list.code-name = SUBSTRING(code-name, 2, (LENGTH(code-name) - 1)).*/

           IF LENGTH(print-list.code-name) GT 0 THEN
               print-list.code-name = SUBSTRING(print-list.code-name, 2, (LENGTH(print-list.code-name) - 1)).
        END.
    END.       
         
END.

PROCEDURE argt-code-name:
     DEFINE BUFFER bargt FOR argt-list.

    DEFINE VARIABLE a AS INTEGER.
    DEFINE VARIABLE d AS INTEGER INITIAL 79.
    DEFINE VARIABLE e AS INTEGER INITIAL 0.
    DEFINE VARIABLE r AS INTEGER INITIAL 1.
    DEFINE VARIABLE str-cut AS CHAR.
    argm-name = "".

    FOR EACH print-list2:
        DELETE print-list2.
    END.                    

    IF all-argt /*:SCREEN-VALUE IN FRAME FRAME1= "Yes"*/ THEN
            argm-name = "ALL".
    ELSE IF NOT all-argt /*:SCREEN-VALUE IN FRAME FRAME1= "No"*/ THEN
    DO:                  
        FOR EACH bargt WHERE bargt.SELECTED EQ YES :
            argm-name = argm-name + bargt.bezeich + "; ".           
        END.

        IF LENGTH(argm-name) GT 0 THEN
          argm-name = SUBSTRING(argm-name,1, LENGTH(argm-name) - 2).
    END.         
     a = LENGTH(argm-name).
     /*REPEAT WHILE a GT 80:
        IF a GT 80 THEN
        DO:
            /*ITA 081216*/
            IF SUBSTRING(argm-name,d + 1 , 1) = ";" THEN 
                ASSIGN str-cut = SUBSTRING(argm-name,d + 3 , 1).
            ELSE ASSIGN str-cut = SUBSTRING(argm-name,d + 1 , 1).

            IF str-cut NE ";" THEN
            REPEAT r = e + 1 TO 80 + e:
                   r = r + d.
                   IF SUBSTRING(argm-name,r,1) EQ ";" THEN
                   DO: 
                       a = LENGTH(argm-name).
                        CREATE print-list2.
                        argm =  SUBSTRING(argm-name,e + 1,r - e). 
                        IF SUBSTRING(argm, 1, 1) = " " THEN
                            argm = SUBSTRING(argm, 2, (LENGTH(argm) - 1)).
                        a = a - r.
                        e = r.
                        d = 79.
                        LEAVE.
                   END.
                   ELSE       
                   DO:
                      r = r - d.
                      d = d - 2.
                   END.   
            END.                   
        END.
      /*  ELSE IF a LT 80 THEN
        DO:              
           CREATE print-list2.
           argm = SUBSTRING(argm-name,r ,a).
        END.   */
      END.
    IF a LT 80 THEN*/
    DO:              
        a = LENGTH(argm-name).
        IF a > 80  THEN
        DO:
           CREATE print-list2.
           IF a GT 0 THEN argm = SUBSTRING(argm-name,r + 1,a). 
            
           /*
           IF SUBSTRING(argm, 1, 1) = " " THEN
               argm = SUBSTRING(argm, 2, (LENGTH(argm) - 1)).*/

           IF LENGTH(argm) GT 0 THEN argm = SUBSTRING(argm, 2, (LENGTH(argm) - 1)).

        END.
        ELSE
        DO:
           CREATE print-list2.

           IF a GT 0 THEN argm = SUBSTRING(argm-name,r,a).

           IF LENGTH(argm) GT 0 THEN
               argm = SUBSTRING(argm, 2, (LENGTH(argm) - 1)).
            
           /*
           IF SUBSTRING(argm, 1, 1) = " " THEN
               argm = SUBSTRING(argm, 2, (LENGTH(argm) - 1)).*/
        END.
    END.         
    
 END.


 PROCEDURE room-code-name:
    DEFINE BUFFER broom FOR zikat-list.

    DEFINE VARIABLE a AS INTEGER.
    DEFINE VARIABLE d AS INTEGER INITIAL 79.
    DEFINE VARIABLE e AS INTEGER INITIAL 0.
    DEFINE VARIABLE r AS INTEGER INITIAL 1.
    room-name = "".

    FOR EACH print-list3:
       DELETE print-list3.
    END.

   IF all-zikat /*:SCREEN-VALUE IN FRAME FRAME1= "Yes"*/ THEN
        room-name = "ALL".
    ELSE IF NOT all-zikat /*:SCREEN-VALUE IN FRAME FRAME1= "No"*/ THEN
    DO:                  
        DEFINE VARIABLE curr-time AS INTEGER.
        ASSIGN curr-time = TIME.

        FOR EACH broom WHERE broom.SELECTED EQ YES :
            room-name = room-name + broom.bezeich  + "; ".           
        END. 

        IF LENGTH(room-name) GT 0 THEN
            room-name = SUBSTRING(room-name,1, LENGTH(room-name) - 2).
    END. 

    
    ASSIGN curr-time = TIME.
    a = LENGTH(room-name).
    /*REPEAT WHILE a GT 80:
        IF a GT 80 THEN
        DO:
            IF SUBSTRING(room-name,d + 1 , 1) NE ";" /*AND a - e GT LENGTH(segm-name) */THEN
            REPEAT r = e + 1 TO 80 + e:
                   r = r + d.
                   IF SUBSTRING(room-name,r,1) EQ ";" THEN
                   DO: 
                       a = LENGTH(room-name).
                        CREATE print-list3.
                        room =  SUBSTRING(room-name,e + 1,r - e). 
                        IF SUBSTRING(room, 1, 1) = " " THEN
                            room = SUBSTRING(room, 2, (LENGTH(room) - 1)). /*
                        str5[c] = SUBSTRING(segm-name,e + 1,r - e ).
                        c =  c + 1.                                 */
                        a = a - r.
                        e = r.
                        d = 79.
                        LEAVE.
                   END.
                   ELSE       
                   DO:
                      r = r - d.
                      d = d - 2.
                   END.   
            END.                   
        END.
        /*ELSE IF a LT 80 THEN
        DO:              
           CREATE print-list3.
           room = SUBSTRING(room-name,r ,a + 1).
           /*str5[c] =  SUBSTRING(segm-name,r + 1,a).
           c =  c + 1.                               */
           
        END.   */
    END.
    IF a LT 80 THEN*/
    DO:              
        a = LENGTH(room-name).
        IF a > 80  THEN
        DO:
           CREATE print-list3.
           IF a GT 0 THEN room = SUBSTRING(room-name,r + 1,a). 

           IF LENGTH(room) GT 0 THEN
              room = SUBSTRING(room, 2, (LENGTH(room) - 1)).
        END.
        ELSE
        DO:
           CREATE print-list3.
           IF a GT 0 THEN room = SUBSTRING(room-name,r,a). 

           IF LENGTH(room) GT 0 THEN
                room = SUBSTRING(room, 2, (LENGTH(room) - 1)).
            
           /*
           IF SUBSTRING(room, 1, 1) = " " THEN
                room = SUBSTRING(room, 2, (LENGTH(room) - 1)).*/
        END.           .
    END.                
END.

PROCEDURE create-browse1: /*forecast*/
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE datum1      AS DATE. 
DEFINE VARIABLE datum2      AS DATE. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE wd          AS INTEGER. 
DEFINE VARIABLE p-room      AS INTEGER. 
DEFINE VARIABLE p-lodg      AS DECIMAL.
DEFINE VARIABLE prev-room   AS INTEGER. 
DEFINE VARIABLE p-pax       AS INTEGER. 
DEFINE VARIABLE avrg-rate   AS DECIMAL. 
DEFINE VARIABLE do-it       AS LOGICAL. 
DEFINE VARIABLE consider-it AS LOGICAL. 
DEFINE VARIABLE dayuse-flag AS LOGICAL. 

/*MT 07/06/12 
DEFINE VARIABLE rm-array    AS INTEGER EXTENT 18. 
*/
DEFINE VARIABLE n           AS INTEGER INITIAL 0. 
DEFINE VARIABLE kont-doit   AS LOGICAL. 
DEFINE VARIABLE allot-doit  AS LOGICAL.
DEFINE VARIABLE mtd-occ     AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-lodg    AS DECIMAL NO-UNDO.
DEFINE VARIABLE Fnet-lodg   AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-i      AS INTEGER.

DEFINE VARIABLE rsvStat      AS CHAR    NO-UNDO.
DEFINE VARIABLE avrg-lodging AS DECIMAL NO-UNDO.

DEFINE VARIABLE anzahl-dayuse AS INTEGER NO-UNDO.

DEFINE BUFFER s-list FOR segm-list. 
DEFINE BUFFER a-list FOR argt-list. 
DEFINE BUFFER z-list FOR zikat-list. 
DEFINE BUFFER kline  FOR kontline.
DEFINE BUFFER o-list FOR outlook-list.

DEFINE VAR tot-breakfast    AS DECIMAL.
DEFINE VAR tot-Lunch        AS DECIMAL.
DEFINE VAR tot-dinner       AS DECIMAL.
DEFINE VAR tot-Other        AS DECIMAL.
DEFINE VAR tot-fixcost      AS DECIMAL.
DEFINE VAR tot-fixcost2     AS DECIMAL.

DEFINE VAR sum-breakfast    AS DECIMAL.
DEFINE VAR sum-Lunch        AS DECIMAL.
DEFINE VAR sum-dinner       AS DECIMAL.
DEFINE VAR sum-Other        AS DECIMAL.
DEFINE VAR sum-breakfast-usd    AS DECIMAL.
DEFINE VAR sum-Lunch-usd        AS DECIMAL.
DEFINE VAR sum-dinner-usd       AS DECIMAL.
DEFINE VAR sum-Other-usd        AS DECIMAL.
DEFINE VAR tot-vat              AS DECIMAL INITIAL 0.
DEFINE VAR tot-service          AS DECIMAL INITIAL 0.
DEFINE VAR service              AS DECIMAL INITIAL 0.
DEFINE VAR vat                  AS DECIMAL INITIAL 0.

DEFINE VARIABLE tavg-rmrev    AS DECIMAL.
DEFINE VARIABLE tavg-rmrev2   AS DECIMAL.
DEFINE VARIABLE troom-excComp AS INT.
DEFINE VARIABLE othRev        AS DECIMAL.

DEFINE VARIABLE t-avrglodg-inclcomp AS DECIMAL.
DEFINE VARIABLE t-avrglodg-exclcomp AS DECIMAL.
DEFINE VARIABLE t-rmocc-exclcomp    AS DECIMAL.
DEFINE VARIABLE t-room-comp         AS INTEGER.

DEFINE VARIABLE curr-resnr AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-segm  AS INTEGER NO-UNDO.

tent-pers = 0.
  DO i = 1 TO 18: 
    rm-array[i] = 0. 
    IF i < 5 THEN
        t-lodg[i] = 0.
  END. 
  
  FOR EACH room-list: 
    delete room-list. 
  END. 
 
  tot-room = 0. 
  FOR EACH zimmer WHERE sleeping NO-LOCK: 
    IF all-zikat THEN tot-room = tot-room + 1. 
    ELSE 
    DO: 
      FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
        AND z-list.selected NO-LOCK NO-ERROR. 
      IF AVAILABLE z-list THEN tot-room = tot-room + 1. 
    END. 
  END. 
  datum = curr-date - 1.
  DO i = 1 TO tmpInt: /* FT Serverless */ 
      datum = datum + 1. 
      wd = WEEKDAY(datum) - 1. 
      IF wd = 0 THEN wd = 7. 
      RUN rsv-closeout(datum, OUTPUT rsvstat).
      CREATE room-list. 
      ASSIGN
        room-list.wd      = wd 
        room-list.datum   = datum 
        room-list.bezeich = " " + week-list[wd] + " " + STRING(datum) + rsvStat. 
    
      FOR EACH kontline WHERE kontline.ankunft LE datum 
        AND kontline.abreise GE datum AND kontline.betriebsnr = 0 
        AND kontline.kontstat = 1 NO-LOCK:
        allot-doit = YES.
        IF kontline.zikatnr NE 0 AND NOT all-zikat THEN
        DO:
          FIND FIRST z-list WHERE z-list.zikatnr = kontline.zikatnr 
            AND z-list.selected NO-LOCK NO-ERROR. 
          allot-doit = AVAILABLE z-list. 
        END.
        IF allot-doit AND (datum GE (ci-date + kontline.ruecktage)) THEN
        DO:
          room-list.room[14] = room-list.room[14] + kontline.zimmeranz. 
          rm-array[14] = rm-array[14] + kontline.zimmeranz. 
        END.
      END.
  END.


  
  /*CREATE room-list. 
  room-list.bezeich = " TOTAL".FT serverless*/
    
  /** %%% **/ 
  /* NOTES: Tentative reservatio is needed here TO GET the sum, but does NOT 
          effect TO the occupancy statistic*/ 
  /* 18 Feb 08 Requested by SB BayVIew, there is an option to consider tentative in 
  occupancy statistic */

  curr-time = TIME.
  
  FOR EACH res-line WHERE (res-line.active-flag LE 1 
    AND res-line.resstatus LE 13 
    AND res-line.resstatus NE 4
    /*AND res-line.resstatus NE 9 
    AND res-line.resstatus NE 10 FT serverless*/
    AND res-line.resstatus NE 12
    /*AND NOT (res-line.ankunft GT to-date) FT serverless*/
    AND res-line.ankunft LE to-date
    /*AND NOT (res-line.abreise LT curr-date)) OR FT serverless*/
    AND res-line.abreise GE curr-date) OR
    ((res-line.active-flag = 2 AND res-line.resstatus = 8
    AND res-line.ankunft = ci-date AND res-line.abreise = ci-date) OR 
    (res-line.active-flag = 2 AND res-line.resstatus = 8 
    AND res-line.abreise = ci-date))
    AND res-line.gastnr GT 0
    AND res-line.l-zuordnung[3] = 0
    USE-INDEX gnrank_ix NO-LOCK
    /*FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK ,
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
    BY res-line.gastnr*/ BY res-line.resnr: /*MT 13/08/12 */
    
     
    /*FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
        NO-ERROR. FT serverless*/

     ASSIGN
     curr-i        = 0
     tot-breakfast = 0
     tot-lunch     = 0
     tot-dinner    = 0
     tot-other     = 0
     dayuse-flag   = NO
   .

    IF curr-resnr NE res-line.resnr THEN
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
      curr-resnr = res-line.resnr.
      curr-segm = reservation.segmentcode.
    END.
    
    IF NOT vhp-limited THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST segment WHERE segment.segmentcode = /*reservation.segmentcode*/ curr-segm
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
    END.

    FIND FIRST room-list WHERE room-list.datum GE res-line.ankunft AND room-list.datum LE res-line.abreise NO-ERROR.
    IF NOT AVAILABLE room-list THEN do-it = NO. /*FT serverless*/


    IF do-it AND res-line.resstatus = 8 
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date THEN
    DO:
      dayuse-flag = YES.     
      FIND FIRST arrangement WHERE arrangement.arrangement 
        =  res-line.arrangement NO-LOCK NO-ERROR. 
      FIND FIRST bill-line WHERE bill-line.departement = 0
        AND bill-line.artnr = arrangement.argt-artikelnr
        AND bill-line.bill-datum = ci-date
        AND bill-line.massnr = res-line.resnr
        AND bill-line.billin-nr = res-line.reslinnr
        USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
      do-it = AVAILABLE bill-line.
    END.
    
    IF do-it AND NOT all-segm THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.segm = reservation.segmentcode 
        AND s-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE s-list. 
    END. 
    IF do-it AND NOT all-argt THEN 
    DO: 
      FIND FIRST a-list WHERE a-list.argt = res-line.arrangement 
        AND a-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE a-list. 
    END. 
    IF do-it AND NOT all-zikat THEN 
    DO: 
      FIND FIRST z-list WHERE z-list.zikatnr = res-line.zikatnr 
        AND z-list.selected NO-LOCK NO-ERROR. 
      do-it = AVAILABLE z-list. 
    END. 
 
    kont-doit = YES. 
    IF do-it AND (NOT all-segm) AND (res-line.kontignr LT 0) THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.segm = /*reservation.segmentcode */ curr-segm
        AND s-list.selected NO-LOCK NO-ERROR. 
      kont-doit = AVAILABLE s-list. 
    END. 

    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
    IF do-it AND AVAILABLE zimmer THEN 
    DO: 
      FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
        AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
      IF zimmer.sleeping THEN 
      DO: 
          IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
            do-it = NO. 
      END. 
      ELSE 
      DO: 
        IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
        ELSE do-it = NO. 
      END. 
    END. 
    
    /*ITA 200318*/
    IF excl-compl AND do-it THEN DO:
          FIND FIRST segment WHERE segment.segmentcode = /*reservation.segmentcode*/ curr-segm
              AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
          IF AVAILABLE segment THEN ASSIGN do-it = NO.
          ELSE DO:
              IF res-line.zipreis = 0 AND res-line.gratis NE 0
                /*AND res-line.resstatus = 6*/ THEN ASSIGN do-it = NO.
          END.
    END.

    /*ITA 290318*/
    IF do-it AND NOT all-outlook THEN DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer THEN DO:
              FIND FIRST o-list WHERE o-list.SELECTED = YES 
                  AND o-list.outlook-nr = zimmer.typ NO-LOCK NO-ERROR.
               ASSIGN do-it = AVAILABLE o-list.
          END.
    END.

    /*IF do-it AND res-line.ankunft NE ? AND res-line.abreise NE ? THEN /*FT serverless*/
    DO:
        FIND FIRST room-list WHERE room-list.datum GE res-line.ankunft AND room-list.datum LE res-line.abreise NO-LOCK NO-ERROR.
        IF NOT AVAILABLE room-list THEN do-it = NO. 
    END.*/

    IF do-it THEN 
    DO: 
      IF dayuse-flag THEN
      DO:
        FIND FIRST dayuse-list WHERE dayuse-list.datum = ci-date
            NO-ERROR.
        IF NOT AVAILABLE dayuse-list THEN
        DO:
          CREATE dayuse-list.
          ASSIGN dayuse-list.datum = res-line.ankunft.
        END.
        IF NOT res-line.zimmerfix THEN 
          dayuse-list.zimmeranz = dayuse-list.zimmeranz + 1.
        dayuse-list.pax = dayuse-list.pax + res-line.erwachs
          + res-line.kind1.
      END.
    
      datum1 = curr-date. 
      IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
      datum2 = to-date. 
      IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.
      /*IF res-line.abreise LE datum2 THEN datum2 = res-line.abreise - 1.*/
      
      
      DO datum = datum1 TO datum2: 
        pax = res-line.erwachs. 
        curr-i = curr-i + 1.
        net-lodg = 0.    

        /*ITA 291217*/
        IF res-line.zipreis NE 0 THEN DO:
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
              AND reslin-queasy.resnr = res-line.resnr 
              AND reslin-queasy.reslinnr = res-line.reslinnr 
              AND reslin-queasy.date1 LE datum 
              AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
              pax = reslin-queasy.number3. 
        END.
        
        FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
        IF AVAILABLE room-list THEN /*FT serverless*/
        DO:
            consider-it = YES. 
            IF res-line.zimmerfix THEN 
            DO: 
              FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr 
                AND rline1.reslinnr NE res-line.reslinnr 
                AND rline1.resstatus EQ 8 /*and rline1.erwachs GT 0*/ 
                AND rline1.abreise GT datum NO-LOCK NO-ERROR. 
              IF AVAILABLE rline1 THEN consider-it = NO. 
            END. 
    
            IF datum = res-line.abreise THEN .
            ELSE DO:
    
                FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
                    AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
        
                    RUN check-fixleist-posted(datum , fixleist.artnr, fixleist.departement, 
                                              fixleist.sequenz, fixleist.dekade, 
                                              fixleist.lfakt, res-line.ankunft, res-line.abreise,
                                              OUTPUT post-it). 
                    ASSIGN 
                        service = 0
                        vat     = 0
                        fcost   = 0.
        
                    IF post-it THEN DO:
                        FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr
                            AND artikel.departement = fixleist.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE artikel THEN
                            RUN calc-servvat.p(artikel.departement, artikel.artnr, datum, 
                                               artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
                        
                        ASSIGN fcost = fixleist.betrag * fixleist.number
                               fcost = fcost / (1 + service + vat).
                        
    
                        
                        IF show-rev EQ 1 THEN
                            ASSIGN room-list.fixleist = room-list.fixleist + fcost
                                   /*tot-fixcost        = tot-fixcost + room-list.fixleist*/
                                   tot-fixcost        = tot-fixcost + fcost.
                        ELSE IF show-rev EQ 2 THEN
                             ASSIGN room-list.fixleist  = room-list.fixleist + fcost                               
                                   room-list.fixleist2 = room-list.fixleist2 + (fcost / exchg-rate)
                                   /*tot-fixcost2        = tot-fixcost2 + room-list.fixleist2
                                   tot-fixcost         = tot-fixcost + room-list.fixleist*/
                                   tot-fixcost2        = tot-fixcost2 + (fcost / exchg-rate)
                                   tot-fixcost         = tot-fixcost + fcost.
                    END.   
                END.
    
                /* Dzikri 796D85 - arrangement fixcost */
                FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK.
                IF AVAILABLE arrangement THEN
                DO:
                  FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
                      AND argt-line.kind2 NO-LOCK: 
    
                      RUN check-fixargt-posted(argt-line.argt-artnr, argt-line.departement, 
                              argt-line.fakt-modus, argt-line.intervall, res-line.ankunft, res-line.abreise, 
                              OUTPUT post-it).
    
                      ASSIGN 
                          service = 0
                          vat     = 0
                          fcost   = 0.
                      
                      IF post-it THEN DO:
                          FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr
                              AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR.
                          IF AVAILABLE artikel THEN do:
                              RUN calc-servvat.p(artikel.departement, artikel.artnr, datum, 
                                                 artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
                          end.
    
                          IF argt-line.vt-percnt = 0 THEN 
                          DO: 
                            IF argt-line.betriebsnr = 0 THEN pax = res-line.erwachs. 
                            ELSE pax = argt-line.betriebsnr. 
                          END. 
                          ELSE IF argt-line.vt-percnt = 1 THEN pax = res-line.kind1. 
                          ELSE IF argt-line.vt-percnt = 2 THEN pax = res-line.kind2.
                          ELSE pax = 0.
    
                          price = 0.
                          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                              AND reslin-queasy.char1    = "" 
                              AND reslin-queasy.number1  = argt-line.departement 
                              AND reslin-queasy.number2  = argt-line.argtnr 
                              AND reslin-queasy.resnr    = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.number3  = argt-line.argt-artnr 
                              AND curr-date GE reslin-queasy.date1 
                              AND curr-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
                          IF AVAILABLE reslin-queasy THEN 
                          DO:
                            FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                              AND reslin-queasy.char1    = "" 
                              AND reslin-queasy.number1  = argt-line.departement 
                              AND reslin-queasy.number2  = argt-line.argtnr 
                              AND reslin-queasy.resnr    = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.number3  = argt-line.argt-artnr 
                              AND curr-date GE reslin-queasy.date1 
                              AND curr-date LE reslin-queasy.date2 NO-LOCK:
                                IF reslin-queasy.deci1 NE 0 THEN price = reslin-queasy.deci1.
                                ELSE IF reslin-queasy.deci2 NE 0 THEN price = reslin-queasy.deci2.
                                ELSE IF reslin-queasy.deci3 NE 0 THEN price = reslin-queasy.deci3.
                                IF price NE 0 THEN                            
                                ASSIGN fcost = price * pax
                                       fcost = fcost / (1 + service + vat).
                                .
                            END.
                          END.
                          IF price EQ 0 THEN
                          ASSIGN fcost = argt-line.betrag * pax
                                 fcost = fcost / (1 + service + vat).
    
                          IF show-rev EQ 1 THEN
                              ASSIGN room-list.fixleist = room-list.fixleist + fcost
                                     /*tot-fixcost        = tot-fixcost + room-list.fixleist*/
                                     tot-fixcost        = tot-fixcost + fcost
                                      .
                          ELSE IF show-rev EQ 2 THEN
                              ASSIGN room-list.fixleist  = room-list.fixleist + fcost                               
                                     room-list.fixleist2 = room-list.fixleist2 + (fcost / exchg-rate)
                                     /*tot-fixcost2        = tot-fixcost2 + room-list.fixleist2
                                     tot-fixcost         = tot-fixcost + room-list.fixleist*/
                                     tot-fixcost2        = tot-fixcost2 + (fcost / exchg-rate)
                                     tot-fixcost         = tot-fixcost + fcost.
                          
                      END.         
                  END.
                END.
               /* Dzikri 796D85 - END */
                
                
                /* START Breakfast lunch Dinner other From Room Rev*/
                ASSIGN net-lodg   = 0
                    tot-breakfast = 0
                    tot-lunch     = 0
                    tot-dinner    = 0
                    tot-other     = 0
                    tot-rmrev     = 0
                . 
    
                
                IF (show-rev EQ 1 OR show-rev EQ 2) AND res-line.zipreis GT 0 THEN
                DO:             
                    IF incl-tent = NO THEN DO:
                        IF res-line.resstatus NE 3 THEN DO:
                            RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                     OUTPUT tot-service).      
                        END.       
                    END.
                    ELSE RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                     OUTPUT tot-service).                
                END.
    
                IF net-lodg = ? THEN ASSIGN net-lodg = 0.
                IF tot-rmrev = ? THEN ASSIGN tot-rmrev = 0.
                                                                                    
                /* END Breakfast lunch Dinner other From Room Rev*/                 
                ASSIGN room-list.others[1] = room-list.others[1] + tot-breakfast
                       room-list.others[2] = room-list.others[2] + tot-lunch
                       room-list.others[3] = room-list.others[3] + tot-dinner
                       room-list.others[4] = room-list.others[4] + tot-other 
                       room-list.others[5] = room-list.others[1] / exchg-rate 
                       room-list.others[6] = room-list.others[2] / exchg-rate 
                       room-list.others[7] = room-list.others[3] / exchg-rate 
                       room-list.others[8] = room-list.others[4] / exchg-rate .
            END.
    
                     
            IF datum = res-line.ankunft AND consider-it 
                AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent)) THEN
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND NOT res-line.zimmerfix THEN 
              DO: 
                room-list.lodg[2] = room-list.lodg[2] + net-lodg.
                room-list.room[3] = room-list.room[3] + res-line.zimmeranz. 
                rm-array[3] = rm-array[3] + res-line.zimmeranz. 
                t-lodg[2]   = t-lodg[2] + net-lodg.
    
                IF (res-line.kontignr LT 0) AND kont-doit THEN 
                DO: 
                  room-list.room[16] = room-list.room[16] - res-line.zimmeranz. 
                  rm-array[16] = rm-array[16] - res-line.zimmeranz. 
                END. 
    
                 ASSIGN
                    room-list.room[4] = room-list.room[4] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz
                    rm-array[4] = rm-array[4] 
                      + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                      + res-line.gratis) * res-line.zimmeranz.             
              END.  
                
             
              IF (res-line.kontignr LT 0) AND kont-doit THEN 
              DO: 
                 ASSIGN
                   room-list.room[17] = room-list.room[17] 
                     - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz
                   rm-array[17] = rm-array[17] 
                     - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz
                 . 
                 FIND FIRST kontline WHERE kontline.gastnr = res-line.gastnr 
                   AND kontline.ankunft = datum 
                   AND kontline.zikatnr = res-line.zikatnr 
                   AND kontline.betriebsnr = 1 
                   AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
                 IF AVAILABLE kontline THEN 
                 ASSIGN
                   room-list.k-pax = room-list.k-pax 
                     + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz 
                     - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                     * res-line.zimmeranz 
                   rm-array[18] = rm-array[18] 
                     + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                     + res-line.gratis) * res-line.zimmeranz 
                     - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                     * res-line.zimmeranz
                 . 
              END. 
    
              IF /*res-line.ankunft LT res-line.abreise OR dayuse-flag*/
                 res-line.ankunft LE res-line.abreise OR dayuse-flag THEN 
              DO: 
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                  AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent))
                  AND NOT res-line.zimmerfix THEN DO:
                    ASSIGN
                      room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                      room-list.lodg[4] = room-list.lodg[4] + net-lodg
                      room-list.lodg[6] = room-list.lodg[4] / exchg-rate
                      rm-array[7] = rm-array[7] + res-line.zimmeranz 
                      t-lodg[4]   = t-lodg[4] + net-lodg.               
                      t-lodg[6]   = t-lodg[6] + (net-lodg / exchg-rate).
                END.                                                            
    
                /*ft 26/11/13*/
                IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN
                DO:
                  room-list.room-comp = room-list.room-comp + res-line.zimmeranz .
                  t-room-comp         = room-list.room-comp + res-line.zimmeranz .
                END.
                ELSE 
                  ASSIGN
                    room-list.lodg[5] = room-list.lodg[5] + net-lodg
                    t-lodg[5]         = t-lodg[5]         + net-lodg
                    room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                    t-lodg[7]         = t-lodg[7] + (net-lodg / exchg-rate).
                
                room-list.room-excComp = room-list.room[7] - room-list.room-comp.
                /*room-list.rmrate  = room-list.rmrate + res-line.zipreis.*/
                room-list.rmrate  = room-list.rmrate + tot-rmrev.
                room-list.rmrate2 = room-list.rmrate / exchg-rate.
    
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                    AND res-line.resstatus NE 3 THEN
                ASSIGN
                  room-list.room[8] = room-list.room[8] 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                  rm-array[8] = rm-array[8] 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                .
              END. 
            END. /*  Arrival */ 
            
            IF datum = res-line.abreise AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent)) 
              AND consider-it THEN 
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND NOT res-line.zimmerfix THEN DO:
                  ASSIGN
                    room-list.room[5] = room-list.room[5] + res-line.zimmeranz
                    room-list.lodg[3] = room-list.lodg[3] + net-lodg
                    rm-array[5] = rm-array[5] + res-line.zimmeranz
                    t-lodg[3] = t-lodg[3] + net-lodg. 
              END.
    
              
              IF datum NE curr-date THEN
                  room-list.lodg[1] = room-list.lodg[1] + net-lodg.
              ASSIGN
                room-list.room[6] = room-list.room[6] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                  + res-line.gratis) * res-line.zimmeranz 
                rm-array[6] = rm-array[6] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                  + res-line.gratis) * res-line.zimmeranz 
                 
              .
            END. /* Departure */ 
    
            /*ITA 080818*/
            IF (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent)) 
              AND res-line.resstatus NE 4 
              AND consider-it 
              AND (res-line.abreise GT res-line.ankunft 
                AND res-line.ankunft NE datum
                AND res-line.abreise NE datum) THEN 
            DO: 
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                AND (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND incl-tent))
                AND NOT res-line.zimmerfix THEN DO:
    
                  ASSIGN
                    room-list.room[7] = room-list.room[7] + res-line.zimmeranz
                    room-list.lodg[4] = room-list.lodg[4] + net-lodg
                    room-list.lodg[6] = room-list.lodg[4] / exchg-rate
                    rm-array[7] = rm-array[7]   + res-line.zimmeranz
                    t-lodg[4]   = t-lodg[4]     + net-lodg.
                    t-lodg[6]   = t-lodg[6] + (net-lodg / exchg-rate).        
                    room-list.room-excComp = room-list.room[7] - room-list.room-comp.
              END.
                
              /*ft 26/11/13*/
              IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN
              DO:
                room-list.room-comp = room-list.room-comp + res-line.zimmeranz .
                t-room-comp         = room-list.room-comp + res-line.zimmeranz .
              END.
              ELSE 
                ASSIGN
                  room-list.lodg[5] = room-list.lodg[5] + net-lodg
                  t-lodg[5]         = t-lodg[5]         + net-lodg
                  room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                  t-lodg[7]         = t-lodg[7] + (net-lodg / exchg-rate).
    
              /*room-list.rmrate  = room-list.rmrate + res-line.zipreis.*/
              room-list.rmrate  = room-list.rmrate + tot-rmrev.
              room-list.rmrate2 = room-list.rmrate / exchg-rate.
             
              IF datum NE curr-date THEN
                  room-list.lodg[1] = room-list.lodg[1] + net-lodg.
    
              IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                  AND res-line.resstatus NE 3 THEN
              ASSIGN
                room-list.room[8] = room-list.room[8] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                  + res-line.gratis) * res-line.zimmeranz 
                rm-array[8] = rm-array[8] 
                  + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                  + res-line.gratis) * res-line.zimmeranz 
              .
              
              IF (res-line.kontignr LT 0) AND kont-doit THEN 
              DO: 
                ASSIGN
                  room-list.room[16] = room-list.room[16] - res-line.zimmeranz
                  room-list.room[17] = room-list.room[17] 
                    - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                  rm-array[16] = rm-array[16] - res-line.zimmeranz
                  rm-array[17] = rm-array[17] 
                    - (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                .
                FIND FIRST kontline WHERE kontline.gastnr = res-line.gastnr 
                  AND kontline.ankunft EQ datum 
                  AND kontline.zikatnr = res-line.zikatnr 
                  AND kontline.betriebsnr = 1 
                  AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
                IF AVAILABLE kontline THEN  
                ASSIGN
                  room-list.k-pax = room-list.k-pax 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                    - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                    * res-line.zimmeranz
                  rm-array[18] = rm-array[18] 
                    + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                    + res-line.gratis) * res-line.zimmeranz 
                    - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
                    * res-line.zimmeranz
                .  
              END. 
            END. /* Inhouse */ 
            
            /*tentative*/
            IF res-line.resstatus = 3 AND datum LT res-line.abreise THEN DO:
                   ASSIGN 
                      room-list.room[13] = room-list.room[13] + res-line.zimmeranz
                      rm-array[13] = rm-array[13] + res-line.zimmeranz
                      room-list.t-pax = room-list.t-pax + (res-line.erwachs * res-line.zimmeranz)
                      tent-pers = tent-pers + (res-line.erwachs * res-line.zimmeranz).
                      /*room-list.lodg[4] = room-list.lodg[4] + net-lodg. 
                      room-list.lodg[6] = room-list.lodg[4] / exchg-rate. 
    
                      IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN
                          room-list.room-comp = room-list.room-comp + res-line.zimmeranz.
                      ELSE 
                          ASSIGN
                            room-list.lodg[5] = room-list.lodg[5] + net-lodg
                            t-lodg[5]         = t-lodg[5]         + net-lodg
                            room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                            t-lodg[7]         = t-lodg[5]         / exchg-rate.
                   room-list.rmrate  = room-list.rmrate + res-line.zipreis.
                   room-list.rmrate2 = room-list.rmrate / exchg-rate.*/
                    
            END.        
            
            IF res-line.kontignr > 0 /* AND NOT res-line.zimmerfix */
              AND res-line.active-flag LE 1 AND res-line.resstatus LE 6
              AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
              AND res-line.abreise GT datum THEN 
            DO: 
              FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
                AND kline.kontstat = 1 NO-LOCK NO-ERROR.
              IF AVAILABLE kline THEN DO:
                  FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
                    AND kontline.ankunft LE datum AND kontline.abreise GE datum
                    AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 
                    NO-LOCK NO-ERROR.
                  IF AVAILABLE kontline AND datum GE (ci-date + kontline.ruecktage) THEN
                  ASSIGN
                    room-list.room[14] = room-list.room[14] - res-line.zimmeranz
                    rm-array[14] = rm-array[14] - res-line.zimmeranz.
              END.         
            END.         
        END.
        
        
      END. 
    END. 
    PROCESS EVENTS. 
  END. 
  
 /*OUTPUT STREAM s1 CLOSE.*/
  DO datum = curr-date TO to-date: 
    FOR EACH kontline WHERE kontline.ankunft LE datum 
      AND kontline.abreise GE datum AND kontline.betriebsnr = 1 
      AND kontline.kontstat = 1 NO-LOCK: 
      do-it = YES. 
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST a-list WHERE a-list.argt = kontline.arrangement 
          AND a-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE a-list. 
      END. 
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST z-list WHERE z-list.zikatnr = kontline.zikatnr 
          AND z-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE z-list. 
      END. 
      IF do-it AND NOT all-segm THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = kontline.gastnr NO-LOCK. 
        FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
          AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE guestseg THEN 
          FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.segm = guestseg.segmentcode 
            AND s-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE s-list. 
        END. 
      END. 

      /*ITA 13/01/22*/
      IF excl-compl AND do-it THEN DO:
          FIND FIRST guest WHERE guest.gastnr = kontline.gastnr NO-LOCK. 
          FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
              AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE guestseg THEN 
              FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                NO-LOCK NO-ERROR. 
          IF AVAILABLE guestseg THEN DO:
              FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
                  AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
              IF AVAILABLE segment THEN ASSIGN do-it = NO.          
          END.
      END.
 
      IF do-it THEN 
      DO: 
        FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
        ASSIGN
          room-list.room[16] = room-list.room[16] + kontline.zimmeranz
          room-list.room[17] = room-list.room[17] 
            + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
            * kontline.zimmeranz
          rm-array[16] = rm-array[16] + kontline.zimmeranz
          rm-array[17] = rm-array[17] 
            + (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
            * kontline.zimmeranz
        . 
      END. 
    END. 
    PROCESS EVENTS. 
  END. 
    
  /*DEFINE VARIABLE curr-time AS INTEGER.*/
  curr-time = TIME.  

  CREATE room-list. 
  room-list.bezeich = " TOTAL".
    
  FOR EACH room-list:      
    IF room-list.room[16] GT 0 THEN
        ASSIGN
            room-list.room[7] = room-list.room[7] + room-list.room[16]
            room-list.room[8] = room-list.room[8] + room-list.room[17] + room-list.k-pax. 
    
    IF incl-tent THEN
        ASSIGN
            /*room-list.room[7] = room-list.room[7] + room-list.room[13]*/
            room-list.room[8] = room-list.room[8] + room-list.t-pax
            /*room-list.room-excComp = room-list.room-excComp + room-list.room[13]*/.
  END. 

  IF rm-array[16] GT 0 THEN
      ASSIGN
      rm-array[7] = rm-array[7] + rm-array[16]
      rm-array[8] = rm-array[8] + rm-array[17] + rm-array[18].
  IF incl-tent THEN
      ASSIGN
          /*rm-array[7] = rm-array[7]  + rm-array[13]*/
          rm-array[8] = rm-array[8]  + tent-pers.
 
  datum = curr-date - 1. 
  
  DO i = 1 TO tmpInt: /* FT Serverless */
    datum = datum + 1. 
    
    FIND FIRST room-list WHERE room-list.datum = datum NO-ERROR. 
 
    FOR EACH queasy WHERE queasy.key = 14 AND 
      queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK, 
      FIRST zimmer WHERE zimmer.zinr = queasy.char1 AND zimmer.sleeping NO-LOCK: 
      FIND FIRST guestseg WHERE guestseg.gastnr = queasy.number3 
        AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE guestseg THEN 
      FIND FIRST guestseg WHERE guestseg.gastnr = queasy.number3 
        NO-LOCK NO-ERROR. 
      do-it = AVAILABLE guestseg. 
      IF NOT all-segm AND do-it THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.segm = guestseg.segmentcode 
          AND s-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE s-list. 
      END. 
      IF do-it AND NOT all-argt THEN 
      DO: 
        FIND FIRST a-list WHERE a-list.argt = queasy.char2 
          AND a-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE a-list. 
      END. 
      IF do-it AND NOT all-zikat THEN 
      DO: 
        FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
          AND z-list.selected NO-LOCK NO-ERROR. 
        do-it = AVAILABLE z-list. 
      END. 
      IF do-it THEN 
      ASSIGN
        room-list.room[7] = room-list.room[7] + 1
        room-list.room[8] = room-list.room[8] + queasy.number1 
        rm-array[7] = rm-array[7] + 1
        rm-array[8] = rm-array[8] + queasy.number1 
      . 
    END. 
  END. 
   
  RUN cal-lastday-occ. 
  ASSIGN
    p-room    = 0 
    p-pax     = 0 
    prev-room = 0 
    datum     = curr-date - 1.
  
    
  DO i = 1 TO tmpInt: /* FT Serverless */
    ASSIGN
      datum         = datum + 1
      anzahl-dayuse = 0
    . 
    
    FIND FIRST dayuse-list WHERE dayuse-list.datum = datum NO-ERROR.
    IF AVAILABLE dayuse-list THEN 
      anzahl-dayuse = dayuse-list.zimmeranz.

    FIND FIRST room-list WHERE room-list.datum = datum. 
    room-list.room[9] = room-list.room[7] / tot-room * 100. 
    prev-room = prev-room + room-list.room[7]. 
    room-list.room[10] = prev-room / (tot-room * i) * 100. 
    room-list.rmocc-exclcomp = (room-list.room[7] - room-list.room-comp ) / tot-room * 100.
    
    IF (room-list.room[7] - anzahl-dayuse) LT tot-room THEN 
    DO: 
      room-list.room[11] = tot-room - room-list.room[7] + anzahl-dayuse. 
      rm-array[11] = rm-array[11] + tot-room - room-list.room[7] + anzahl-dayuse. 
    END. 
    ELSE 
    DO: 
      room-list.room[12] = room-list.room[7] - tot-room - anzahl-dayuse. 
      rm-array[12] = rm-array[12] + room-list.room[7] - tot-room - anzahl-dayuse. 
    END. 
    
    IF i GT 1 THEN 
    ASSIGN 
      room-list.room[1] = p-room
      room-list.room[2] = p-pax
      /*room-list.lodg[1] = p-lodg*/
      /*MT 07/06/12 */
      rm-array[1] = rm-array[1] + p-room
      rm-array[2] = rm-array[2] + p-pax
    .
    
    p-room = room-list.room[7]. 
    p-lodg = room-list.lodg[4].
    p-pax = room-list.room[8].
  END. 

  FOR EACH room-list WHERE room-list.wd NE 0: 
      
    IF room-list.datum LT ci-date THEN 
    DO: 
      FIND FIRST zinrstat WHERE zinrstat.zinr = "ooo" 
        AND zinr.datum = room-list.datum NO-LOCK NO-ERROR. 
      IF AVAILABLE zinrstat THEN 
      ASSIGN
        room-list.room[15] = zinrstat.zimmeranz
        rm-array[15] = rm-array[15] + zinrstat.zimmeranz
      . 
    END. 
    ELSE 
    DO: 
      FOR EACH outorder WHERE outorder.gespstart LE room-list.datum 
        AND outorder.gespende GE room-list.datum AND outorder.betriebsnr LE 1 
        NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping 
        NO-LOCK: 
        IF NOT all-zikat THEN 
        DO: 
            FIND FIRST z-list WHERE z-list.zikatnr = zimmer.zikatnr 
              AND z-list.selected NO-LOCK NO-ERROR. 
            IF AVAILABLE z-list THEN
            ASSIGN
               room-list.room[15] = room-list.room[15] + 1
               rm-array[15] = rm-array[15] + 1. 
        END. 
        ELSE
        DO:
            room-list.room[15] = room-list.room[15] + 1. 
            rm-array[15] = rm-array[15] + 1. 
        END.
      END. 
      IF exclOOO THEN
      ASSIGN
          room-list.room[11] = room-list.room[11] - room-list.room[15]
          rm-array[11] = rm-array[11] - room-list.room[15]
      .
    END. 
  END. 

  FOR EACH room-list WHERE room-list.wd NE 0: 
    DO i = 1 TO 8: 
      room-list.coom[i] = STRING(room-list.room[i],"->>>>>9").
    END. 
    DO i = 9 TO 10: 
      room-list.coom[i] = STRING(room-list.room[i],"->>9.99"). 
    END. 
    DO i = 11 TO 15: 
      room-list.coom[i] = STRING(room-list.room[i], "->>>>>>"). 
    END. 
    DO i = 16 TO 17: 
      room-list.coom[i] = STRING(room-list.room[i],"->>>>>9"). 
    END. 
  END. 
    
  /*jml-date = to-date - curr-date + 1.FT serverless*/
  ASSIGN
    jml-date = to-date - curr-date
    jml-date = jml-date + 1.

  ASSIGN do-it = YES.
  IF show-rev EQ 1 OR show-rev EQ 2 THEN DO:
       /*ITA 201016*/
      DEFINE VARIABLE tmax    AS INTEGER NO-UNDO INIT 0.
      DEFINE VARIABLE tmin    AS INTEGER NO-UNDO INIT 0.
      DEFINE VARIABLE counter AS INTEGER NO-UNDO INIT 0.
    
      FOR EACH s-list WHERE s-list.SELECTED = YES:
          ASSIGN counter = counter + 1.
          FIND FIRST segment WHERE segment.segmentcode = s-list.segm
              NO-LOCK NO-ERROR.
          IF AVAILABLE segment THEN DO:
              IF tmin = 0 AND counter = 1 THEN DO:
                  IF segment.betriebsnr = 0 THEN
                      ASSIGN tmin = 0.
                  ELSE ASSIGN tmin = segment.betriebsnr.
              END.
              
              IF segment.betriebsnr GT tmax THEN
                  ASSIGN tmax = segment.betriebsnr.
    
              IF segment.betriebsnr LT tmin THEN
                  ASSIGN tmin = segment.betriebsnr.
          END.
      END.
        
      IF tmax LE 2 AND tmin GE 1 THEN ASSIGN do-it = NO.
      ELSE ASSIGN do-it = YES.
  END.
    
  
  /*IF do-it THEN DO:
      /*FT 25/10/13 --> add othRev for rmRev*/
      /*t-lodg[5] = 0.*/
      FOR EACH room-list:
          RUN calc-othRev (room-list.datum, OUTPUT othRev).
          ASSIGN
              room-list.lodg[5] = room-list.lodg[5] + othRev
              room-list.lodg[7] = room-list.lodg[5] / exchg-rate.

          IF room-list.wd NE 0 THEN 
              ASSIGN 
                    t-lodg[5] = t-lodg[5] + othRev.
                    t-lodg[7] = t-lodg[7] + (othRev / exchg-rate).
      END.
  END.*/ /*end*/


  IF do-it THEN DO:
      /*FT 25/10/13 --> add othRev for rmRev*/
      /*t-lodg[5] = 0.*/
      IF incl-oth THEN DO:
          FOR EACH room-list:
              RUN calc-othRev (room-list.datum, OUTPUT othRev).
              IF room-list.datum NE ? THEN
              DO:
                IF room-list.datum LT ci-date THEN DO:
                  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK NO-ERROR. 
                  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN DO:
                      FIND FIRST exrate WHERE exrate.datum = room-list.datum 
                          AND exrate.artnr = waehrung.waehrungsnr NO-LOCK NO-ERROR. 
                      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
                  END.
                END.
                ELSE DO:
                  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
                  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
                  ELSE exchg-rate = 1. 
                END.
              END.  
                
              ASSIGN
                  room-list.lodg[5] = room-list.lodg[5] + othRev
                  room-list.lodg[7] = room-list.lodg[5] / exchg-rate
                  .
    
              IF room-list.wd NE 0 THEN 
                  ASSIGN 
                    t-lodg[5] = t-lodg[5] + othRev.
                    t-lodg[7] = t-lodg[7] + (othRev / exchg-rate).
          END.
      END.      
  END. /*end*/

  FOR EACH room-list:
      tot-avrg = tot-avrg + room-list.room[9].

      IF (room-list.room[7] - room-list.room[16]) NE 0 THEN
        room-list.avrglodg  = room-list.lodg[4] / (room-list.room[7] - room-list.room[16]).
        room-list.avrglodg2 = room-list.avrglodg / exchg-rate.
      
      IF (room-list.room-excComp - room-list.room[16]) NE 0 THEN DO:  /*FT121114*/
          room-list.avrgrmrev = room-list.lodg[5] / (room-list.room[7] - room-list.room[16]).
          room-list.avrgrmrev2 = room-list.avrgrmrev / exchg-rate.
          /*
          room-list.avrgrmrev = room-list.lodg[5] / (room-list.room-excComp - room-list.room[16]).
          room-list.avrgrmrev2 = room-list.avrgrmrev / exchg-rate.*/
      END.
      IF room-list.wd NE 0 THEN
          /*troom-excComp = troom-excComp + (room-list.room-excComp - room-list.room[16]).*/
          troom-excComp = troom-excComp + (room-list.room[7] - room-list.room[16]).

      IF ((DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100) NE 0 THEN DO:
          ASSIGN
            room-list.revpar = (DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100
            room-list.revpar2 = room-list.revpar / exchg-rate.
      END.

      room-list.avrglodg-inclcomp = room-list.lodg[5] / room-list.room[7].
      room-list.avrglodg-exclcomp = room-list.lodg[5] / (room-list.room[7] - room-list.room-comp).  
  END.
  
  IF troom-excComp NE 0 THEN
    tavg-rmrev = t-lodg[5] / troom-excComp.
    tavg-rmrev2 = tavg-rmrev / exchg-rate.
    avrg-rate = tot-avrg / jml-date.

  t-avrglodg-inclcomp = t-lodg[5] / rm-array[7].
  t-avrglodg-exclcomp = t-lodg[5] / (rm-array[7] - t-room-comp).  

  /*F
  FIND FIRST room-list WHERE room-list.datum = to-date. 
  avrg-rate = room-list.room[10]. 
  F*/

  DEF VAR jml1 AS INTEGER.
  DEF VAR jml2 AS DECIMAL FORMAT "->>9.99".
  DEF VAR jml3 AS DECIMAL FORMAT "->>9.99".

  /*mtd-occ = rm-array[7] / (tot-room * (to-date - curr-date + 1)) * 100.
  t-rmocc-exclcomp = (rm-array[7] - t-room-comp) / (tot-room * (to-date - curr-date + 1)) * 100. FT serverless*/
  ASSIGN
    mtd-occ = rm-array[7] / (tot-room * tmpInt) * 100
    t-rmocc-exclcomp = (rm-array[7] - t-room-comp) / (tot-room * tmpInt) * 100.
  
  
  
  FIND FIRST room-list WHERE room-list.wd = 0. /* total */
  DO i = 1 TO 8:   
    room-list.room[i] = rm-array[i]. 
  END. 

  DO i = 11 TO 17: 
    room-list.room[i] = rm-array[i]. 
  END. 

  DO i = 1 TO 8: 
    room-list.coom[i] = STRING(room-list.room[i],"->>>>>9"). 
  END. 

  DO i = 11 TO 12: 
    room-list.coom[i] = STRING(room-list.room[i],"->>>>>>"). 
  END. 

  ASSIGN
    room-list.room[9]  = mtd-occ
    room-list.coom[9]  = STRING(mtd-occ, " >>9.99")
    room-list.coom[10] = STRING(avrg-rate,"->>9.99")
    room-list.coom[13] = STRING(rm-array[13], "->>>>>>") 
    room-list.coom[14] = STRING(rm-array[14], "->>>>>>") 
    room-list.coom[15] = STRING(rm-array[15], "->>>>>>")
    room-list.lodg[2]  = t-lodg[2]
    room-list.lodg[3]  = t-lodg[3]
    room-list.lodg[4]  = t-lodg[4]
    room-list.lodg[5]  = t-lodg[5] /*FT 230914*/
    room-list.lodg[6]  = t-lodg[6]
    room-list.lodg[7]  = t-lodg[7]   
    room-list.rmocc-exclcomp    = t-rmocc-exclcomp.
    room-list.avrglodg-inclcomp = t-avrglodg-inclcomp.
    room-list.avrglodg-exclcomp = t-avrglodg-exclcomp.
  .
  
  DO i = 16 TO 17: 
    room-list.coom[i] = STRING(room-list.room[i],"->>>>>9"). 
  END.

  ASSIGN
      mtd-occ      = 0
      avrg-lodging = 0
  .
  FOR EACH room-list WHERE room-list.wd NE 0:
      ASSIGN
          avrg-lodging = avrg-lodging + room-list.avrglodg
          mtd-occ      = mtd-occ + room-list.room[9]
          
          sum-breakfast = sum-breakfast + room-list.others[1]
          sum-lunch     = sum-lunch + room-list.others[2]
          sum-dinner    = sum-dinner + room-list.others[3]
          sum-other     = sum-other + room-list.others[4].
          sum-breakfast-usd = sum-breakfast-usd + room-list.others[5].
          sum-lunch-usd     = sum-lunch-usd + room-list.others[6].
          sum-dinner-usd    = sum-dinner-usd + room-list.others[7].
          sum-other-usd     = sum-other-usd + room-list.others[8].
          sum-comp          = sum-comp + room-list.room-comp.
          t-revpar          = t-revpar + room-list.revpar.
          t-revpar2         = t-revpar2 + room-list.revpar2.
          t-rmrate          = t-rmrate + room-list.rmrate.
          t-rmrate2         = t-rmrate2 + room-list.rmrate2.
  END.
  
  FIND FIRST room-list WHERE room-list.wd = 0. /* total */
  IF tavg-rmrev = ? THEN tavg-rmrev = 0.
  IF tavg-rmrev2 = ? THEN tavg-rmrev2 = 0.

  ASSIGN
      /*MT 07/06/12
      room-list.coom[9]  = STRING("","x(6)")*/
      /*room-list.avrglodg    = avrg-lodging / (to-date - curr-date + 1)FT serverless*/
      room-list.avrglodg    = avrg-lodging / tmpInt
      room-list.avrgrmrev   = tavg-rmrev
      room-list.avrgrmrev2  = tavg-rmrev2
      room-list.others[1]    = sum-breakfast 
      room-list.others[2]    = sum-lunch   
      room-list.others[3]    = sum-dinner
      room-list.others[4]    = sum-other 
      room-list.others[5]    = sum-breakfast-usd 
      room-list.others[6]    = sum-lunch-usd   
      room-list.others[7]    = sum-dinner-usd
      room-list.others[8]    = sum-other-usd 
      room-list.room-comp   = sum-comp
      /*room-list.revpar = t-revpar
      room-list.revpar2 = t-revpar2*/
      room-list.rmrate   = t-rmrate
      room-list.rmrate2  = t-rmrate2
      room-list.fixleist = tot-fixcost
      room-list.fixleist2 = tot-fixcost2.
  IF ((DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100) NE 0 THEN DO:
      ASSIGN
        room-list.revpar = (DECIMAL(room-list.coom[9]) * room-list.avrgrmrev) / 100
        room-list.revpar2 = room-list.revpar / exchg-rate.
  END.

  IF room-list.room[7] NE 0 THEN
      room-list.avrglodg  = room-list.lodg[4] / room-list.room[7].
      room-list.avrglodg2 = room-list.avrglodg / exchg-rate.
END. 

PROCEDURE cal-lastday-occ: 
DEFINE VARIABLE do-it AS LOGICAL NO-UNDO. 
DEFINE BUFFER s-list FOR segm-list. 
  FIND FIRST room-list WHERE room-list.datum = curr-date. 
  
  IF curr-date LE ci-date THEN DO:
      /*FOR EACH segmentstat WHERE segmentstat.datum = (curr-date - 1) NO-LOCK: 
        IF NOT vhp-limited THEN do-it = YES.
        ELSE
        DO:
          FIND FIRST segment WHERE segment.segmentcode = segmentstat.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
        
        IF do-it AND NOT all-segm THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.segm = segmentstat.segmentcode 
            AND s-list.selected NO-LOCK NO-ERROR. 
          do-it = AVAILABLE s-list. 
        END. 
    
        IF do-it THEN 
        ASSIGN 
          room-list.room[1] = room-list.room[1] + segmentstat.zimmeranz
          /*MT 07/06/12 */
          rm-array[1] = rm-array[1] + segmentstat.zimmeranz
          /*room-list.lodg[1] = room-list.lodg[1] + segmentstat.logis*/
          room-list.room[2] = room-list.room[2] + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis 
          /*MT 07/06/12 */
          rm-array[2] = rm-array[2] + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis 
        .     
      END.*/
    
      /*ITA 16/09/21 NEW CONCEPT*/
      FOR EACH genstat WHERE genstat.datum = curr-date - 1
          AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */
          AND genstat.zinr NE ""
          AND genstat.resstatus NE 13
          USE-INDEX date_ix NO-LOCK: /*MT 13/08/12 */

            ASSIGN do-it = YES.

            IF do-it AND NOT all-segm THEN 
            DO: 
              FIND FIRST s-list WHERE s-list.segm = genstat.segmentcode 
                AND s-list.selected NO-LOCK NO-ERROR. 
              do-it = AVAILABLE s-list. 
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

            IF do-it THEN DO:
                ASSIGN 
                  room-list.room[1] = room-list.room[1] + 1
                  rm-array[1] = rm-array[1] + 1
                  room-list.room[2] = room-list.room[2] + genstat.erwachs + genstat.kind1 
                    + genstat.kind2 + genstat.kind3 + genstat.gratis 
                  rm-array[2] = rm-array[2] + genstat.erwachs + genstat.kind1 
                    + genstat.kind2 + genstat.kind3 + genstat.gratis 
                .     
            END.
      END.
  END.  
  ELSE
  ASSIGN
      room-list.room[1] = room-list.room[7] - room-list.room[3] 
                        + room-list.room[5]
      /*MT 07/06/12 */
      rm-array[1] = rm-array[1] + room-list.room[1]
      /*room-list.lodg[1] = room-list.lodg[4] - room-list.lodg[2]
                        + room-list.lodg[3]*/
      room-list.room[2] = room-list.room[8] - room-list.room[4] 
                    + room-list.room[6]
      /*MT 07/06/12 */
      rm-array[2] = rm-array[2] + room-list.room[2].

      room-list.lodg[1] = room-list.lodg[4] - room-list.lodg[2]
            + room-list.lodg[3].

END.

PROCEDURE rsv-closeout:
DEF INPUT    PARAMETER datum    AS DATE.
DEF OUTPUT   PARAMETER rsvStat  AS CHAR INITIAL "".
DEF VARIABLE curr-anz           AS INTEGER NO-UNDO.
DEF VARIABLE curr-date          AS DATE    NO-UNDO.
DEF VARIABLE start-date         AS DATE    NO-UNDO.
  FIND FIRST queasy WHERE queasy.KEY = 37
      AND queasy.number1 = YEAR(datum) NO-LOCK NO-ERROR.
  IF NOT AVAILABLE queasy THEN RETURN.
  ASSIGN 
      start-date = DATE(1, 1, YEAR(datum))
      curr-anz   = 0
  .
  DO curr-date = start-date TO datum:
      curr-anz = curr-anz + 1.
  END.
  rsvStat = " " + SUBSTR(queasy.char3, curr-anz, 1).
END.


PROCEDURE check-bonus: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE stay AS INTEGER. 
DEFINE VARIABLE pay AS INTEGER. 
DEFINE VARIABLE num-bonus AS INTEGER INITIAL 0. 
 
  j = 1. 
  DO i = 1 TO 4: 
    stay = INTEGER(SUBSTR(arrangement.options, j, 2)). 
    pay  = INTEGER(SUBSTR(arrangement.options, j + 2, 2)). 
    IF (stay - pay) GT 0 THEN 
    DO: 
      n = num-bonus + pay  + 1. 
      DO k = n TO stay: 
        bonus-array[k] = YES. 
      END. 
      num-bonus = stay - pay. 
    END. 
     j = j + 4. 
  END. 
END. 

/*MTe1
PROCEDURE usr-prog1: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog" 
    AND reslin-queasy.number1 = resnr 
    AND reslin-queasy.number2 = 0 AND reslin-queasy.char1 = "" 
    AND reslin-queasy.reslinnr = 1 USE-INDEX argt_ix NO-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy THEN prog-str = reslin-queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, res-line.resnr, res-line.reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 
 
PROCEDURE usr-prog2: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST queasy WHERE queasy.key = 2 
    AND queasy.char1 = guest-pr.code NO-LOCK NO-ERROR. 
  IF AVAILABLE queasy THEN prog-str = queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, res-line.resnr, res-line.reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 

*/

PROCEDURE create-active-room-list:
DEF VAR end-date    AS DATE NO-UNDO.
DEF VAR actual-date AS DATE NO-UNDO INIT ?.
DEFINE BUFFER z-list FOR zikat-list.
  IF to-date LT ci-date THEN end-date = to-date.
  ELSE end-date = ci-date - 1.
  /*MT 31/05/12 */
  IF all-zikat THEN
    FOR EACH zkstat WHERE zkstat.datum GE curr-date
      AND zkstat.datum LE end-date NO-LOCK BY zkstat.datum:
      IF actual-date NE zkstat.datum THEN
      DO:
        CREATE active-rm-list.
        ASSIGN 
          active-rm-list.datum     = zkstat.datum
          actual-date              = zkstat.datum
        .
      END.
      active-rm-list.zimmeranz = active-rm-list.zimmeranz
        + zkstat.anz100.
    END.
  ELSE
    FOR EACH zkstat WHERE zkstat.datum GE curr-date
       AND zkstat.datum LE end-date NO-LOCK BY zkstat.datum:

      FIND FIRST z-list WHERE z-list.zikatnr = zkstat.zikatnr 
        AND z-list.selected NO-LOCK NO-ERROR.
      IF AVAILABLE z-list THEN
      DO:
        IF actual-date NE zkstat.datum THEN
        DO:
          CREATE active-rm-list.
          ASSIGN 
            active-rm-list.datum     = zkstat.datum
            actual-date              = zkstat.datum
          .
        END.
        active-rm-list.zimmeranz = active-rm-list.zimmeranz
            + zkstat.anz100.
      END.
    END.
END.

PROCEDURE get-active-room:
DEFINE INPUT  PARAMETER curr-datum  AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER active-room AS INTEGER NO-UNDO INIT 0.
  IF curr-datum GE ci-date THEN
  DO:
    active-room = actual-tot-room.
    RETURN.
  END.
  FIND FIRST active-rm-list WHERE active-rm-list.datum = curr-datum
      NO-ERROR.
  IF AVAILABLE active-rm-list THEN active-room = active-rm-list.zimmeranz.
END.

PROCEDURE get-mtd-active-room:
DEF OUTPUT PARAMETER mtd-room AS INTEGER NO-UNDO INIT 0.
DEF VAR datum AS DATE    NO-UNDO.
DEF VAR anz   AS INTEGER NO-UNDO.
  DO datum = curr-date TO to-date:
      RUN get-active-room(datum, OUTPUT anz).
      mtd-room = mtd-room + anz.
  END.
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

PROCEDURE check-fixleist-posted: 
DEFINE INPUT PARAMETER curr-date    AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER artnr        AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER dept         AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER fakt-modus   AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER intervall    AS INTEGER  NO-UNDO. 
DEFINE INPUT PARAMETER lfakt        AS DATE     NO-UNDO. 
DEFINE INPUT PARAMETER cidate       AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER codate       AS DATE     NO-UNDO.
DEFINE OUTPUT PARAMETER post-it     AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE delta AS INTEGER. 
DEFINE VARIABLE start-date AS DATE. 
DEFINE VARIABLE tmpInt1 AS INTEGER.
DEFINE VARIABLE tmpDate AS DATE.
 
/* ITA 07/03/25
  IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF res-line.ankunft = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (res-line.ankunft + 1) = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF day(curr-date) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF day(curr-date + 1) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 6 THEN 
  DO: 
    IF lfakt = ? THEN delta = 0. 
    ELSE 
    DO: 
      delta = lfakt - res-line.ankunft. 
      IF delta LT 0 THEN delta = 0. 
    END. 
    ASSIGN
      start-date = res-line.ankunft + delta
      tmpInt1 = res-line.abreise - start-date.
    /*IF (res-line.abreise - start-date) LT intervall FT serverless*/
    IF tmpInt1 LT intervall
      THEN start-date = res-line.ankunft. 
    ASSIGN
      tmpInt1 = intervall - 1
      tmpDate = start-date + tmpInt1.
    /*IF curr-date LE (start-date + (intervall - 1)) FT serverless*/
    IF curr-date LE tmpDate
      THEN post-it = YES. 
    IF curr-date LT start-date THEN post-it = no. /* may NOT post !! */ 
  END. */

IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF cidate = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (cidate + 1) = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF day(curr-date) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF day(curr-date + 1) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 6 THEN 
  DO: 
    IF lfakt = ? THEN delta = 0. 
    ELSE 
    DO: 
      delta = lfakt - cidate. 
      IF delta LT 0 THEN delta = 0. 
    END. 
    ASSIGN
      start-date = cidate + delta
      tmpInt1 = codate - start-date.
    /*IF (res-line.abreise - start-date) LT intervall FT serverless*/
    IF tmpInt1 LT intervall
      THEN start-date = cidate. 
    ASSIGN
      tmpInt1 = intervall - 1
      tmpDate = start-date + tmpInt1.
    /*IF curr-date LE (start-date + (intervall - 1)) FT serverless*/
    IF curr-date LE tmpDate
      THEN post-it = YES. 
    IF curr-date LT start-date THEN post-it = no. /* may NOT post !! */ 
  END.
END. 

/* Dzikri 796D85 - arrangment fixed cost appear in forcast */
PROCEDURE check-fixargt-posted: 
DEFINE INPUT PARAMETER artnr AS INTEGER. 
DEFINE INPUT PARAMETER dept AS INTEGER. 
DEFINE INPUT PARAMETER fakt-modus AS INTEGER. 
DEFINE INPUT PARAMETER intervall AS INTEGER.  
DEFINE INPUT PARAMETER cidate       AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER codate       AS DATE     NO-UNDO.
DEFINE OUTPUT PARAMETER post-it AS LOGICAL INITIAL NO. 
 
  /*IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF res-line.ankunft = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (res-line.ankunft + 1) = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF day(curr-date) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF day(curr-date + 1) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 6 THEN 
  DO: 
    IF curr-date LE (res-line.ankunft + (intervall - 1)) 
    THEN post-it = YES. 
  END. */

  IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF cidate = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (cidate + 1) = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF day(curr-date) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF day(curr-date + 1) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 6 THEN 
  DO: 
    IF curr-date LE (cidate + (intervall - 1)) 
    THEN post-it = YES. 
  END.
END. 
/* Dzikri 796D85 - END */

