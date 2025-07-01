
DEFINE TEMP-TABLE sum-list 
  FIELD allot-flag  AS LOGICAL INITIAL NO
  FIELD bezeich     AS CHAR FORMAT "x(19)" 
  FIELD summe       AS INTEGER EXTENT 30 FORMAT "       ->>>9"
. 

DEFINE TEMP-TABLE room-avail-list 
  FIELD avail-flag  AS LOGICAL INITIAL NO
  FIELD allot-flag  AS LOGICAL INITIAL NO
  FIELD zikatnr     AS INTEGER 
  FIELD i-typ       AS INTEGER
  FIELD sleeping    AS LOGICAL INITIAL YES 
  FIELD allotment   AS INTEGER EXTENT 30 
  FIELD bezeich     AS CHAR FORMAT "x(19)" FONT 1 
  FIELD room        AS INTEGER EXTENT 30 
  FIELD coom        AS CHAR EXTENT 30 FORMAT "x(15)"
  FIELD sort-prior  AS INTEGER
. 

DEFINE TEMP-TABLE date-list
  FIELD datum       AS DATE
  FIELD counter     AS INT 
.

DEFINE TEMP-TABLE room-list 
  FIELD avail-flag  AS LOGICAL INITIAL NO
  FIELD allot-flag  AS LOGICAL INITIAL NO
  FIELD zikatnr     AS INTEGER 
  FIELD i-typ       AS INTEGER
  FIELD sleeping    AS LOGICAL INITIAL YES 
  FIELD allotment   AS INTEGER EXTENT 30 
  FIELD bezeich     AS CHAR FORMAT "x(19)" FONT 1 
  FIELD room        AS INTEGER EXTENT 30 
  FIELD coom        AS CHAR EXTENT 30 FORMAT "x(15)"

  FIELD rmrate      AS DECIMAL EXTENT 30
  FIELD currency    AS INTEGER
  FIELD wabkurz     AS CHAR
  
  FIELD i-counter   AS INTEGER
  FIELD rateflag    AS LOGICAL INIT NO
  FIELD adult       AS INTEGER
  FIELD child       AS INTEGER
  FIELD prcode      AS CHAR EXTENT 30
  FIELD rmcat       AS CHAR
  FIELD argt        AS CHAR
  FIELD rcode       AS CHAR
  FIELD segmentcode AS CHAR
  FIELD dynarate    AS LOGICAL INIT NO
  FIELD expired     AS LOGICAL INIT NO
  FIELD argt-remark AS CHAR
  FIELD minstay     AS INTEGER INIT 0
  FIELD maxstay     AS INTEGER INIT 0
  FIELD minadvance  AS INTEGER INIT 0
  FIELD maxadvance  AS INTEGER INIT 0    
  FIELD frdate      AS DATE INIT ?
  FIELD todate      AS DATE INIT ?
  FIELD marknr      AS INTEGER INIT 0
  FIELD datum       AS DATE EXTENT 30
. 
DEFINE TEMP-TABLE rate-list
    FIELD rateCode      AS CHARACTER
    FIELD segmentcode   AS CHAR
    FIELD dynaflag      AS LOGICAL INIT NO
    FIELD expired       AS LOGICAL INIT NO
    FIELD room-type     AS INTEGER
    FIELD argtno        AS INTEGER
    FIELD statCode      AS CHARACTER EXTENT 30
    FIELD rmRate        AS DECIMAL   EXTENT 30 
      INIT [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    FIELD minstay       AS INTEGER INIT 0
    FIELD maxstay       AS INTEGER INIT 0
    FIELD minadvance    AS INTEGER INIT 0
    FIELD maxadvance    AS INTEGER INIT 0    
    FIELD frdate        AS DATE INIT ?
    FIELD todate        AS DATE INIT ?
    FIELD adult         AS INTEGER
    FIELD child         AS INTEGER    
    FIELD currency      AS INTEGER
    FIELD wabkurz       AS CHAR
    FIELD occ-rooms     AS INTEGER INIT 0
    FIELD marknr        AS INTEGER INIT 0
    FIELD i-counter     AS INTEGER
.

DEFINE TEMP-TABLE created-list
    FIELD rateCode      AS CHARACTER
    FIELD marknr        AS INTEGER INIT 0
    FIELD rmcateg       AS INTEGER
    FIELD argtno        AS INTEGER
    FIELD statCode      AS CHARACTER EXTENT 30
    FIELD rmRate        AS DECIMAL   EXTENT 30 
      INIT [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
.

/*DODY 291223 enhance stuck trace*/
DEFINE TEMP-TABLE t-kontline LIKE kontline.


DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER vhp-limited AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER op-type          AS INTEGER NO-UNDO.
/*0 create list, 1 design lnl, 2 print lnl, 3 print txt*/
DEFINE INPUT PARAMETER printer-nr       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER call-from        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER adult-child-str         AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER statsort         AS INTEGER NO-UNDO.
/* "Room &Category", 1, "Booking &Status", 2. */
DEFINE INPUT PARAMETER dispsort         AS INTEGER NO-UNDO.
/*"&Before Allotment", 1, "&After Allotment", 2. */
DEFINE INPUT PARAMETER curr-date        AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER incl-tentative   AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER mi-inactive      AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER show-rate        AS LOGICAL NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER indGastnr AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER qci-zinr         AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.
DEFINE OUTPUT PARAMETER TABLE FOR sum-list.

/*
DEFINE VARIABLE qci-zinr         AS CHAR.
DEFINE VARIABLE pvILanguage      AS INTEGER NO-UNDO INIT 1.
DEFINE VARIABLE vhp-limited      AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE op-type          AS INTEGER INIT 0.
DEFINE VARIABLE printer-nr       AS INTEGER INIT 0.
DEFINE VARIABLE call-from        AS INTEGER INIT 0.
DEFINE VARIABLE adult-child-str  AS CHAR    INIT "$A1,0,11022024,1,0,0".
DEFINE VARIABLE statsort         AS INTEGER INIT 1.
DEFINE VARIABLE dispsort         AS INTEGER INIT 1.
DEFINE VARIABLE curr-date        AS DATE INIT 11/02/23.
DEFINE VARIABLE incl-tentative   AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE mi-inactive      AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE show-rate        AS LOGICAL INIT YES.
DEFINE VARIABLE indGastnr        AS INTEGER NO-UNDO INIT 4.
*/

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "availability". 

DEFINE VARIABLE logid  AS INT.
DEFINE VARIABLE logstr AS CHAR.
DEFINE VARIABLE cdstr AS CHAR.
logid = RANDOM(1,99999).
IF curr-date EQ ? THEN cdstr = "NULL".
ELSE cdstr = STRING(curr-date).
logstr = "LOGID=" + STRING(logid) + "|ACS=" + adult-child-str + "|CD=" + cdstr. 

/***************TEMP-TABLE**********/
DEFINE TEMP-TABLE rmcat-list 
  FIELD zikatnr AS INTEGER 
  FIELD anzahl AS INTEGER 
  FIELD sleeping AS LOGICAL INITIAL YES. 

/* START for extra article in general param setting No 2999 */
DEFINE TEMP-TABLE tmp-resline LIKE res-line.

DEFINE TEMP-TABLE tmp-extra 
    FIELD art       AS INTEGER
    FIELD typ-pos   AS CHAR
    FIELD pos-from  AS CHAR
    FIELD cdate     AS DATE
    FIELD room      AS CHAR
    FIELD qty       AS INTEGER.

DEFINE TEMP-TABLE temp-art 
    FIELD art-nr    AS INTEGER
    FIELD art-nm    AS CHAR FORMAT "x(50)".
/* END for extra article in general param setting No 2999 */

/* Dzikri 1156B1 -  wrong number after allotment */
DEFINE TEMP-TABLE tmp-allotment
    FIELD zikatnr     AS INTEGER
    FIELD res-allot   AS INTEGER EXTENT 30
. 
/* Dzikri 1156B1 -  END */

DEFINE BUFFER qci-zimmer FOR zimmer.

/***********VARIABLE*********/
DEFINE VARIABLE col-label AS CHAR EXTENT 31.
DEFINE VARIABLE curr-day  AS INTEGER. 

DEFINE STREAM s1.

DEFINE VARIABLE datum       AS DATE.
DEFINE VARIABLE tot-room    AS INTEGER. 
DEFINE VARIABLE i           AS INTEGER NO-UNDO.
DEFINE VARIABLE ci-date     AS DATE. 
DEFINE VARIABLE co-date     AS DATE INIT ?. 
DEFINE VARIABLE from-date   AS DATE. 
DEFINE VARIABLE to-date     AS DATE. 
DEFINE VARIABLE last-option AS LOGICAL INITIAL NO. 

DEFINE VARIABLE wlist AS CHAR FORMAT "x(133)". 
DEFINE VARIABLE dlist AS CHAR FORMAT "x(133)". 

DEFINE VARIABLE j                   AS INTEGER  NO-UNDO. 
DEFINE VARIABLE dd                  AS INTEGER  NO-UNDO.
DEFINE VARIABLE mm                  AS INTEGER  NO-UNDO.
DEFINE VARIABLE yyyy                AS INTEGER  NO-UNDO.
DEFINE VARIABLE num-day             AS INTEGER  NO-UNDO INIT 29.
DEFINE STREAM s1.


DEFINE VARIABLE htl-name AS CHARACTER FORMAT "x(40)". 
DEFINE VARIABLE htl-adr  AS CHARACTER FORMAT "x(40)". 
DEFINE VARIABLE htl-tel  AS CHARACTER FORMAT "x(24)". 
FIND FIRST paramtext WHERE txtnr = 200 NO-ERROR. 
htl-name = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 201 NO-ERROR. 
htl-adr  = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 204 NO-ERROR. 
htl-tel  = paramtext.ptexte. 
DEFINE VARIABLE res-allot AS INTEGER EXTENT 30. 


DEFINE VARIABLE week-list AS CHAR EXTENT 7 FORMAT "x(19)". 
week-list[1] = translateExtended ("Monday    ", lvCAREA,""). 
week-list[2] = translateExtended ("Tuesday   ", lvCAREA,""). 
week-list[3] = translateExtended ("Wednesday ", lvCAREA,""). 
week-list[4] = translateExtended ("Thursday  ", lvCAREA,""). 
week-list[5] = translateExtended ("Friday    ", lvCAREA,""). 
week-list[6] = translateExtended ("Saturday  ", lvCAREA,""). 
week-list[7] = translateExtended ("Sunday    ", lvCAREA,""). 

DEFINE VARIABLE rpt-title AS CHAR NO-UNDO.

DEFINE VARIABLE occ-room                AS INTEGER EXTENT 30 NO-UNDO. /* Dzikri BEED96 - Add new summarry */

/**********MAIN LOGIC********/
/*DODY 281223 validate curr-date eq ? */
IF curr-date EQ ? THEN
DO:
    MESSAGE logstr VIEW-AS ALERT-BOX INFO BUTTONS OK.
    RETURN.
END.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate.

IF NUM-ENTRIES(adult-child-str,",") GT 2 THEN
DO:
  ASSIGN
    mm      = INTEGER(SUBSTR(ENTRY(3, adult-child-str, ","),1,2))
    dd      = INTEGER(SUBSTR(ENTRY(3, adult-child-str, ","),3,2))
    yyyy    = INTEGER(SUBSTR(ENTRY(3, adult-child-str, ","),5,4))
    co-date = DATE(mm, dd, yyyy) + 1
  .
  IF (curr-date + 29) GT co-date THEN 
      num-day = co-date - curr-date. 
END.


IF qci-zinr NE "" THEN FIND FIRST qci-zimmer WHERE 
    qci-zimmer.zinr = qci-zinr NO-LOCK.

i = 1.
DO WHILE i LE (num-day + 1): 
    CREATE date-list.
    ASSIGN
        date-list.counter = i
        date-list.datum = curr-date + i - 1
        i = i + 1.

END.
       
/*DODY 291223 capture log for stuck trace*/
MESSAGE "LOGID=" STRING(logid) + "|" + STRING(TIME,"HH:MM:SS") + "|START" VIEW-AS ALERT-BOX INFO BUTTONS OK.
MESSAGE logstr VIEW-AS ALERT-BOX INFO BUTTONS OK.



CASE op-type:
    WHEN 0 THEN
    DO:
        RUN create-browse.
        IF statsort = 1 THEN RUN calc-extra (curr-date).

        FOR EACH room-avail-list NO-LOCK:
          FIND FIRST queasy WHERE queasy.KEY = 325
            AND queasy.number1 = room-avail-list.zikatnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN 
                ASSIGN room-avail-list.sort-prior = queasy.number2.
        END.

        IF NOT show-rate THEN RUN create-room-list.
        ELSE RUN create-rate-list.
    END.
    WHEN 1 THEN
        RUN design-lnl.
    WHEN 2 THEN
        RUN print-lnl.
    WHEN 3 THEN
    DO:
        RUN print-txt.
    END.
    WHEN 4 THEN
        RUN clear-it.
END CASE.
MESSAGE "LOGID=" STRING(logid) + "|" + STRING(TIME,"HH:MM:SS") + "|END" VIEW-AS ALERT-BOX INFO BUTTONS OK.

/********PROCEDURE******/


PROCEDURE create-room-list:
DEF VAR curr-i AS INTEGER NO-UNDO INIT 0.
DEF VAR i AS INTEGER NO-UNDO.
  
  FOR EACH room-avail-list BY room-avail-list.sort-prior:      
      curr-i = curr-i + 1.
      CREATE room-list.
      BUFFER-COPY room-avail-list TO room-list.
      ASSIGN 
          room-list.i-counter = curr-i.
  END.

END.

PROCEDURE create-rate-list:
DEFINE VARIABLE curr-i   AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE i        AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE loopRate AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE fdate    AS DATE. 
DEFINE VARIABLE tdate    AS DATE.
DEFINE VARIABLE str-argt AS CHAR    NO-UNDO.
DEFINE VARIABLE room-cat AS CHAR    NO-UNDO.
DEFINE VARIABLE adult    AS INTEGER NO-UNDO.

DEFINE VARIABLE argt-code       AS CHAR NO-UNDO.
DEFINE VARIABLE argt-intervall  AS INTEGER NO-UNDO.
DEFINE VARIABLE argt-zuordnung  AS CHAR NO-UNDO.

DEFINE BUFFER buff-ratelist FOR rate-list.

  fdate = curr-date. 
  tdate = curr-date + num-day.
  IF tdate GT co-date THEN tdate = co-date.


  FOR EACH room-avail-list BY room-avail-list.sort-prior:
      curr-i = curr-i + 1.
      CREATE room-list.
      BUFFER-COPY room-avail-list TO room-list.
      ASSIGN room-list.i-counter = curr-i * 100.  
      RUN available-ratesbl.p(fdate, tdate, room-avail-list.zikatnr,
         curr-i, adult-child-str, INPUT-OUTPUT indGastnr, 
         INPUT-OUTPUT TABLE created-list, OUTPUT TABLE rate-list).

      
      FOR EACH rate-list BY rate-list.i-counter:
        FIND FIRST arrangement WHERE arrangement.argtnr = rate-list.argtno NO-LOCK NO-ERROR.        
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = room-avail-list.zikatnr NO-LOCK NO-ERROR.      

        IF AVAILABLE arrangement THEN
        DO:
            argt-code       = arrangement.arrangement.
            argt-intervall  = arrangement.intervall.
            argt-zuordnung  = arrangement.zuordnung.
        END.

        IF NOT AVAILABLE qci-zimmer OR 
          (AVAILABLE qci-zimmer AND qci-zimmer.zikatnr = room-avail-list.zikatnr) THEN        
        DO:
          
          CREATE room-list.
          BUFFER-COPY room-avail-list TO room-list.

          ASSIGN 
              room-list.i-counter   = rate-list.i-counter
              room-list.rateflag    = YES
              room-list.rcode       = rate-list.rateCode
              room-list.segmentcode = rate-list.segmentcode
              room-list.dynarate    = rate-list.dynaflag
              room-list.expired     = rate-list.expired
              room-list.marknr      = rate-list.marknr
              room-list.adult       = rate-list.adult
              room-list.child       = rate-list.child
              room-list.minstay     = rate-list.minstay
              room-list.maxstay     = rate-list.maxstay
              room-list.minadvance  = rate-list.minadvance
              room-list.maxadvance  = rate-list.maxadvance
              room-list.frdate      = rate-list.frdate
              room-list.todate      = rate-list.todate
              room-list.currency    = rate-list.currency
              room-list.rmcat       = zimkateg.kurzbez
              room-list.argt        = /*arrangement.arrangement*/ argt-code
              room-list.bezeich     = rate-list.rateCode + "/" 
                                    + /*arrangement.arrangement*/ argt-code + "/" 
                                    + STRING(room-list.adult) + "/"
                                    + STRING(room-list.child) + ";".

          IF NUM-ENTRIES(rate-list.wabkurz, ";") GE 2 THEN DO:
              ASSIGN  
                  room-list.wabkurz     = ENTRY(1, rate-list.wabkurz, ";")
                  room-list.bezeich     = room-list.bezeich + ENTRY(2, rate-list.wabkurz, ";").
          END.
          ELSE ASSIGN room-list.wabkurz = rate-list.wabkurz.

          IF room-list.minstay LT /*arrangement.intervall*/ argt-intervall THEN
              room-list.minstay = /*arrangement.intervall*/ argt-intervall.

          FIND FIRST queasy WHERE queasy.KEY = 2
              AND queasy.char1 = rate-list.rateCode NO-LOCK.
          room-list.argt-remark = queasy.char2 + CHR(10).
                    
          IF room-list.frdate NE ? THEN
          room-list.argt-remark = room-list.argt-remark 
              + translateExtended ("Begin Sell Date:",lvCAREA,"") 
              + " " + STRING(room-list.frdate) + "; ".

          IF room-list.todate NE ? THEN
          room-list.argt-remark = room-list.argt-remark 
              + translateExtended ("End Sell Date:",lvCAREA,"") 
              + " " + STRING(room-list.todate) + "; ".

          IF room-list.minstay GT 0 THEN
          room-list.argt-remark = room-list.argt-remark 
              + translateExtended ("Minimum Stay (in nights):",lvCAREA,"") 
              + " " + STRING(room-list.minstay) + "; ".
          
          IF room-list.maxstay GT 0 THEN
          room-list.argt-remark = room-list.argt-remark 
              + translateExtended ("Maximum Stay (in nights):",lvCAREA,"") 
              + " " + STRING(room-list.maxstay) + "; ".
          
          IF room-list.minadvance GT 0 THEN
          room-list.argt-remark = room-list.argt-remark 
              + translateExtended ("Min Advance Booking (in days):",lvCAREA,"") 
              + " " + STRING(room-list.minadvance) + "; ".
          
          IF room-list.maxadvance GT 0 THEN
          room-list.argt-remark = room-list.argt-remark 
              + translateExtended ("Max Advance Booking (in days):",lvCAREA,"") 
              + " " + STRING(room-list.maxadvance) + "; ".

          IF /*arrangement.zuordnung*/ argt-zuordnung NE "" THEN
          room-list.argt-remark = room-list.argt-remark
              + /*arrangement.zuordnung*/ argt-zuordnung + ";".

          loopRate = 0.
          DO datum = fdate TO tdate:
              
              loopRate = loopRate + 1.
              ASSIGN 
                 room-list.datum[loopRate]  = datum
                 room-list.prcode[loopRate] = rate-list.statCode[loopRate]
                 room-list.rmrate[loopRate] = rate-list.rmrate[loopRate]
              .
              IF room-list.rmrate[loopRate] LE 99999 THEN
                room-list.coom[loopRate]   = STRING(room-list.rmrate[loopRate], ">,>>>,>>9.99").
              ELSE
                room-list.coom[loopRate]   = STRING(room-list.rmrate[loopRate], " >>>,>>>,>>9").
          END.
        END.
      END.
  END.
END.


PROCEDURE create-tentative :
  DEFINE VARIABLE datum-t AS DATE.
  DEFINE VARIABLE loop-t AS INT.

  create sum-list. 
  sum-list.bezeich = translateExtended ("Tentative",lvCAREA,""). 
  datum = curr-date.
  
  i = 1.

  DO WHILE i LE (num-day + 1):
      FIND FIRST date-list WHERE date-list.counter = i NO-LOCK NO-ERROR.
      FOR EACH res-line WHERE res-line.active-flag LE 1 
          AND res-line.resstatus EQ 3 
          /*AND res-line.ankunft LE date-list.datum
          AND res-line.abreise GT date-list.datum */
          AND ((res-line.ankunft LE date-list.datum AND res-line.abreise GT date-list.datum)
          OR  (res-line.ankunft EQ date-list.datum AND res-line.abreise EQ date-list.datum))
          /*AND res-line.zikatnr = room-avail-list.zikatnr 
          AND res-line.zinr NE "" */
          AND res-line.l-zuordnung[3] = 0 NO-LOCK /*, 
          FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND 
          NOT zimmer.sleeping NO-LOCK*/ : 
          sum-list.summe[date-list.counter] = sum-list.summe[date-list.counter] + res-line.zimmeranz.
      END.
      i = i + 1.
  END.

  /*FOR EACH zimkateg NO-LOCK: 
      FOR EACH res-line WHERE res-line.active-flag LE 1 
          AND res-line.resstatus EQ 3 
          AND res-line.ankunft LE datum
          AND res-line.abreise GT datum 
          /*AND res-line.zikatnr = room-avail-list.zikatnr 
          AND res-line.zinr NE "" */
          AND res-line.l-zuordnung[3] = 0 NO-LOCK /*, 
          FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND 
          NOT zimmer.sleeping NO-LOCK*/ : 
          i = 1.
          DO WHILE i LE (num-day + 1): 
              sum-list.summe[i] = sum-list.summe[i] + 1.
              i = i + 1.
          END.
      END.
*/
      /*
      DO WHILE i LE (num-day + 1): 
        FOR EACH resplan WHERE resplan.datum = datum 
            AND resplan.zikatnr = zimkateg.zikatnr  NO-LOCK: 
          sum-list.summe[i] = sum-list.summe[i] + resplan.anzzim[3]. 
        END. 
        i = i + 1. 
        datum = datum + 1. 
      END. 
      */
  /*END. */
END.

PROCEDURE create-tmpExtra:
DEFINE INPUT PARAMETER art-nr      AS INTEGER.
DEFINE INPUT PARAMETER typ-pos  AS CHAR.
DEFINE INPUT PARAMETER pos-from AS CHAR.
DEFINE INPUT PARAMETER cdate    AS DATE.
DEFINE INPUT PARAMETER room     AS  CHAR.
DEFINE INPUT PARAMETER qty      AS INTEGER.

CREATE tmp-extra. 
ASSIGN tmp-extra.art        = art-nr
       tmp-extra.typ-pos    = typ-pos
       tmp-extra.pos-from   = pos-from
       tmp-extra.cdate      = cdate
       tmp-extra.room       = room
       tmp-extra.qty        = qty.
END.

PROCEDURE calc-extra:
DEFINE INPUT PARAMETER fdate AS DATE.

    DEF VAR tdate       AS DATE.
    DEF VAR art-nr      AS INTEGER.
    DEF VAR int-art     AS CHAR.
    DEF VAR bdate       AS DATE.
    DEF VAR edate       AS DATE.
    DEF VAR eposdate    AS DATE.
    DEF VAR ndate       AS DATE.
    DEF VAR art-qty     AS INTEGER.
    DEF VAR art-rem     AS INTEGER.
    DEF VAR tot-used    AS INTEGER.
    DEF VAR argtnr      AS INTEGER.

    DEFINE BUFFER bargt FOR arrangement.

    tdate = fdate + num-day.
    IF tdate GT co-date THEN tdate = co-date.

    FOR EACH tmp-resline :
        DELETE tmp-resline.
    END.
    FOR EACH tmp-extra :
        DELETE tmp-extra.
    END.
    FOR EACH temp-art :
        DELETE temp-art.
    END.

    /*ITA*/
    /*FOR EACH res-line WHERE (res-line.ankunft >= fdate AND res-line.ankunft <= tdate) 
        OR (res-line.abreise > fdate + 1 AND res-line.abreise < tdate)
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
        AND res-line.resstatus NE 99   NO-LOCK BY res-line.resnr :*/
    FOR EACH res-line WHERE NOT (res-line.abreise LT fdate) AND NOT (res-line.ankunft GT tdate) 
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 99
        AND res-line.l-zuordnung[3] = 0 NO-LOCK BY res-line.resnr :
        FIND FIRST tmp-resline WHERE tmp-resline.resnr = res-line.resnr
            AND tmp-resline.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tmp-resline THEN
        DO:
            CREATE tmp-resline.
            BUFFER-COPY res-line TO tmp-resline.
        END.
    END.

    FIND FIRST htparam WHERE htparam.paramgr = 5 AND htparam.paramnr = 2999 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(htparam.fchar , ";" ) :
            int-art  = ENTRY(i,htparam.fchar,";").

            IF int-art NE "" THEN
            DO:
                FIND FIRST artikel WHERE artikel.artnr = int(int-art) AND artikel.departement = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    CREATE temp-art.
                    ASSIGN temp-art.art-nr = int(int-art)
                           temp-art.art-nm = artikel.bezeich.

                    art-nr = int(int-art).
                    FOR EACH tmp-resline BY tmp-resline.resnr :
                        FOR EACH fixleist WHERE fixleist.resnr = tmp-resline.resnr 
                            AND fixleist.reslinnr = tmp-resline.reslinnr
                            AND fixleist.artnr = art-nr 
                            AND fixleist.departement = 0 NO-LOCK :
                            
                            IF tmp-resline.ankunft = tmp-resline.abreise THEN
                            DO:
                                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 6 THEN
                                    RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).   
                                ELSE IF fixleist.sequenz = 4 THEN
                                    IF DAY(tmp-resline.ankunft) = 1 THEN 
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
                                ELSE IF fixleist.sequenz = 5 THEN
                                    IF DAY(tmp-resline.ankunft + 1) = 1 THEN 
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
                            END.
                            ELSE
                            DO:
                                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 4 OR fixleist.sequenz = 5 THEN
                                DO:
                                    IF tmp-resline.ankunft < fdate THEN
                                        bdate = fdate.
                                    ELSE
                                        bdate = tmp-resline.ankunft.

                                    IF tmp-resline.abreise > tdate THEN /* IF tmp-resline.abreise > tdate THEN */
                                        edate = tdate + 1.
                                    ELSE IF tmp-resline.abreise <= tdate THEN
                                        edate = tmp-resline.abreise.
                                END.

                                IF fixleist.sequenz = 1 THEN
                                DO:
                                    DO WHILE bdate LT edate :
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).
                                        bdate = bdate + 1.
                                    END.
                                END.
                                ELSE IF fixleist.sequenz = 2 THEN
                                DO:
                                    RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).
                                END.
                                ELSE IF fixleist.sequenz = 4 THEN
                                DO:
                                    DO WHILE bdate LT edate :
                                        IF DAY(bdate) = 1 THEN 
                                             RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).    
                                        bdate = bdate + 1.
                                    END.
                                END.
                                ELSE IF fixleist.sequenz = 5 THEN
                                DO:
                                    DO WHILE bdate LT edate :
                                        IF DAY(bdate + 1) = 1 THEN 
                                            RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number). 
                                        bdate = bdate + 1.
                                    END.
                                END.
                                ELSE IF fixleist.sequenz = 6 THEN
                                DO:
                                    eposdate = (fixleist.lfakt + fixleist.dekade).
        
                                    IF fixleist.lfakt < fdate THEN
                                        bdate = fdate.
                                    ELSE
                                        bdate = fixleist.lfakt.
        
                                    IF eposdate > tdate THEN
                                        edate = tdate + 1.
                                    ELSE IF eposdate <= tdate THEN
                                    DO:
                                        IF eposdate > tmp-resline.abreise THEN
                                            edate = tmp-resline.abreise .
                                        ELSE IF eposdate <= tmp-resline.abreise  THEN
                                            edate = eposdate.
                                    END.  
        
                                    DO WHILE bdate LT edate :
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).
                                        bdate = bdate + 1.
                                    END.
        
                                END.
                            END.                            
                        END.

                        FIND FIRST bargt WHERE bargt.arrangement = tmp-resline.arrangement NO-LOCK NO-ERROR.
                        IF AVAILABLE bargt THEN ASSIGN argtnr = bargt.argtnr.
    
                        FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" AND reslin-queasy.resnr = tmp-resline.resnr 
                            AND reslin-queasy.reslinnr = tmp-resline.reslinnr
                            AND reslin-queasy.number1 = 0 AND reslin-queasy.number3 = art-nr
                            AND reslin-queasy.number2 = argtnr NO-LOCK :

                            PUT reslin-queasy.number3 tmp-resline.zinr tmp-resline.ankunft tmp-resline.abreise reslin-queasy.date1 reslin-queasy.date2 fdate tdate SKIP.
    
                            IF reslin-queasy.date1 < fdate THEN
                                bdate = fdate.
                            ELSE
                                bdate = reslin-queasy.date1.
    
                            IF reslin-queasy.date2 > tdate THEN
                                edate = tdate + 1.
                            ELSE IF reslin-queasy.date2 <= tdate THEN
                                edate = reslin-queasy.date2.
    
                            DO WHILE bdate LT edate :
                                RUN create-tmpExtra (art-nr, "argt-line", "0", bdate, tmp-resline.zinr, 1).
                                bdate = bdate + 1.
                            END.
                        END.
                    END.
                END.
            END.
        END.
    END.

    ndate = fdate.

    IF NOT incl-tentative THEN
    DO:
        create sum-list. 
        ASSIGN sum-list.bezeich = "" . 
        RUN create-tentative.
        tot-used = 0.

        FOR EACH temp-art :
            FIND FIRST artikel WHERE artikel.artnr = temp-art.art-nr AND artikel.departement = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
            DO:
                art-qty = artikel.anzahl.
                CREATE sum-list. 
                sum-list.bezeich = temp-art.art-nm. 
                ndate = fdate.
                DO i = 1 TO 30:                    
                    FOR EACH tmp-extra WHERE tmp-extra.art = temp-art.art-nr AND tmp-extra.cdate = ndate AND tmp-extra.qty NE 0 :
                        tot-used = tot-used + tmp-extra.qty.
                    END.
                    art-rem = art-qty - tot-used.
                    sum-list.summe[i] =  art-rem . 
                    ndate = fdate + i.
                    tot-used = 0.
                END. 
            END.
        END.
    END.
    /* Dzikri FCD1E9 - also show extra artikel */
    ELSE
    DO:
        create sum-list. 
        ASSIGN sum-list.bezeich = "" . 
        tot-used = 0.

        FOR EACH temp-art :
            FIND FIRST artikel WHERE artikel.artnr = temp-art.art-nr AND artikel.departement = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
            DO:
                art-qty = artikel.anzahl.
                CREATE sum-list. 
                sum-list.bezeich = temp-art.art-nm. 
                ndate = fdate.
                DO i = 1 TO 30:                    
                    FOR EACH tmp-extra WHERE tmp-extra.art = temp-art.art-nr AND tmp-extra.cdate = ndate AND tmp-extra.qty NE 0 :
                        tot-used = tot-used + tmp-extra.qty.
                    END.
                    art-rem = art-qty - tot-used.
                    sum-list.summe[i] =  art-rem . 
                    ndate = fdate + i.
                    tot-used = 0.
                END. 
            END.
        END.
    END.
    /* Dzikri FCD1E9 - END */
END.

PROCEDURE count-rmcateg: 
DEFINE VARIABLE zikatnr AS INTEGER INITIAL 0. 
  FOR EACH rmcat-list: 
    delete rmcat-list. 
  END. 
  tot-room = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK BY zimmer.zikatnr: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimkateg.verfuegbarkeit THEN 
    DO: 
      tot-room = tot-room + 1. 
      IF zikatnr NE zimkateg.zikatnr THEN 
      DO: 
        create rmcat-list. 
        rmcat-list.zikatnr = zimkateg.zikatnr. 
        rmcat-list.anzahl = 1. 
        zikatnr = zimkateg.zikatnr. 
      END. 
      ELSE rmcat-list.anzahl = rmcat-list.anzahl + 1. 
    END. 
  END. 
/* %%% */ 
  IF NOT mi-inactive THEN RETURN. 
  zikatnr = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = NO NO-LOCK BY zimmer.zikatnr: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimkateg.verfuegbarkeit THEN 
    DO: 
      IF zikatnr NE zimkateg.zikatnr THEN 
      DO: 
        create rmcat-list. 
        rmcat-list.zikatnr = zimkateg.zikatnr. 
        rmcat-list.anzahl = 1. 
        rmcat-list.sleeping = NO. 
        /*zikatnr = zimkateg.zikatnr. */
      END. 
      ELSE rmcat-list.anzahl = rmcat-list.anzahl + 1. 
      zikatnr = zimkateg.zikatnr.
    END. 
  END.
/* %%% */ 
END. 

PROCEDURE create-browse: 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE fdate AS DATE. 
DEFINE VARIABLE tdate AS DATE. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE tmp-list AS INTEGER EXTENT 30. 
DEFINE VARIABLE ooo-list AS INTEGER EXTENT 30 
    INITIAL [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]. 
DEFINE VARIABLE om-list AS INTEGER EXTENT 30 
    INITIAL [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]. 
DEFINE VARIABLE om-flag AS LOGICAL INITIAL NO. 
DEF VAR tot-used AS INTEGER.
DEF VAR art-qty AS INTEGER.
DEFINE BUFFER kline FOR kontline.

  /*IF last-option NE MENU-ITEM mi-inactive:CHECKED IN MENU mbar THEN 
  DO: 
    RUN count-rmcateg. 
    last-option = MENU-ITEM mi-inactive:CHECKED IN MENU mbar. 
  END. */

    

  RUN count-rmcateg.
 
  FOR EACH room-avail-list: 
    delete room-avail-list. 
  END. 
  FOR EACH sum-list: 
    delete sum-list. 
  END. 
 
  fdate = curr-date. 
  tdate = curr-date + num-day. 
  IF tdate GT co-date THEN tdate = co-date.
  DO i = 1 TO 30: 
    res-allot[i] = 0. 
  END. 

 
  /*DODY 291223 enhance stuck trace*/
    FOR EACH kontline WHERE kontline.betriebsnr = 0 
        AND kontline.ankunft LE tdate AND kontline.abreise GE fdate 
        AND kontline.kontstat = 1 NO-LOCK:

        CREATE t-kontline.
        BUFFER-COPY kontline TO t-kontline.
    END.

/*** %%% ***/    
  FOR EACH res-line WHERE resstatus LE 6 /*AND resstatus NE 3*/ 
    AND resstatus NE 4 AND active-flag LE 1 AND res-line.kontignr GT 0 
    AND NOT res-line.ankunft GT tdate AND NOT res-line.abreise LE fdate 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK:

    IF NOT vhp-limited THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK.
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
    END.

    IF res-line.resstatus = 3 AND NOT incl-tentative THEN
        do-it = NO.
    
    IF do-it THEN
    DO i = 1 TO 30: 
      datum = curr-date + i - 1. 
      IF datum GE res-line.ankunft AND datum LT res-line.abreise THEN 
      DO: 
        FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
          AND kline.kontstat = 1 NO-LOCK.
        FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
          AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE kontline AND datum GE (ci-date + kontline.ruecktage) THEN 
        /* Dzikri 1156B1 -  wrong number after allotment */
        DO:
          res-allot[i] = res-allot[i] + res-line.zimmeranz. 
          FIND FIRST tmp-allotment WHERE tmp-allotment.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE tmp-allotment THEN
          DO:
              CREATE tmp-allotment.
              tmp-allotment.zikatnr  = res-line.zikatnr.
          END. 
          tmp-allotment.res-allot[i] = tmp-allotment.res-allot[i] + res-line.zimmeranz.
        END.
        /* Dzikri 1156B1 -  END */
      END. 
    END. 
  END. 

 
  IF NOT incl-tentative THEN /**MT not incl tentative **/
  DO:
      
      IF statsort = 1 THEN 
      DO: 
        create sum-list. 
        sum-list.bezeich = translateExtended ("Avail before Allotm",lvCAREA,""). 
        FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES 
            NO-LOCK BY zimkateg.typ BY zimkateg.zikatnr: 
          FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimkateg.zikatnr 
            AND rmcat-list.sleeping NO-ERROR. 
          IF AVAILABLE rmcat-list THEN 
          DO: 
            create room-avail-list. 
            i = 1. 
            DO WHILE i LE (num-day + 1): 
              room-avail-list.room[i] = rmcat-list.anzahl. 
              i = i + 1. 
            END. 
            ASSIGN
                room-avail-list.i-typ   = zimkateg.typ
                room-avail-list.zikatnr = zimkateg.zikatnr 
                room-avail-list.bezeich = zimkateg.kurzbez 
                  + " - " + STRING(zimkateg.overbook,">>9")
            . 
          END. 
        END. 
        

        FOR EACH rmcat-list WHERE NOT rmcat-list.sleeping, 
          FIRST zimkateg WHERE zimkateg.zikatnr = rmcat-list.zikatnr NO-LOCK 
          BY zimkateg.typ BY zimkateg.zikatnr: 
          create room-avail-list. 
          room-avail-list.sleeping = NO. 
          i = 1. 
          DO WHILE i LE (num-day + 1): 
            room-avail-list.room[i] = rmcat-list.anzahl. 
            i = i + 1. 
          END. 
                      
          ASSIGN
              room-avail-list.i-typ   = zimkateg.typ
              room-avail-list.zikatnr = zimkateg.zikatnr 
              room-avail-list.bezeich = zimkateg.kurzbez 
                + " - " + STRING(zimkateg.overbook,">>9").

          datum = curr-date. 

          DO i = 1 TO 30: 
              FOR EACH res-line WHERE res-line.active-flag LE 1 
                  AND res-line.resstatus LE 6 
                  /*AND res-line.ankunft LE datum 
                  AND res-line.abreise GT datum */
                  AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
                  OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
                  AND res-line.zikatnr = room-avail-list.zikatnr 
                  AND res-line.zinr NE "" 
                  AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                  FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND 
                  NOT zimmer.sleeping NO-LOCK:
                  IF NOT vhp-limited THEN do-it = YES.
                  ELSE
                  DO:
                    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                      NO-LOCK.
                    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                      NO-LOCK NO-ERROR.
                    do-it = AVAILABLE segment AND segment.vip-level = 0.
                  END.
                  IF do-it THEN 
                      ASSIGN
                          room-avail-list.room[i] = room-avail-list.room[i] - 1
                          occ-room[i] = occ-room[i] + 1                               /* Dzikri BEED96 - Add new summarry */
                      . 
              END. 
              datum = datum + 1. 
          END. 
        END.


        FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
          FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
          AND zimmer.sleeping = YES NO-LOCK. 
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
          datum = curr-date. 
          FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = zimmer.zikatnr 
            AND room-avail-list.sleeping NO-LOCK NO-ERROR. 
          IF AVAILABLE room-avail-list THEN
          DO:
            DO i = 1 TO 30: 
              IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
              DO: 
                IF outorder.betriebsnr = 2 THEN 
                DO: 
                  om-list[i] = om-list[i] + 1. 
                  om-flag = YES. 
                END. 
                ELSE 
                DO:
                  ooo-list[i] = ooo-list[i] + 1. 
                  room-avail-list.room[i] = room-avail-list.room[i] - 1. 
                END. 
              END. 
              datum = datum + 1. 
            END. 
          END.            
        END. 
        

        i = 1. 
        datum = curr-date.
       
        DO WHILE i LE (num-day + 1): 
            FOR EACH res-line WHERE res-line.active-flag LE 1 
                  AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
                  AND res-line.resstatus NE 4 
                  AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
                  OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
                  AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK:
                  FIND FIRST room-avail-list WHERE room-avail-list.sleeping 
                      AND room-avail-list.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                  IF AVAILABLE room-avail-list THEN DO:
                      do-it = YES. 
                      IF res-line.zinr NE "" THEN 
                      DO: 
                        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                        do-it = zimmer.sleeping. 
                      END. 
        
                      IF res-line.resstatus = 3 AND NOT incl-tentative THEN
                          do-it = NO.
        
                      IF do-it AND vhp-limited THEN
                      DO:
                        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                          NO-LOCK.
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                          NO-LOCK NO-ERROR.
                        do-it = AVAILABLE segment AND segment.vip-level = 0.
                      END.
        
                      IF do-it THEN 
                          ASSIGN
                              room-avail-list.room[i] = room-avail-list.room[i] - res-line.zimmeranz
                              occ-room[i] = occ-room[i] + res-line.zimmeranz                               /* Dzikri BEED96 - Add new summarry */
                          . 
                  END.                                     
            END. 
            

             FOR EACH kontline WHERE kontline.betriebsnr = 1 
                  AND kontline.ankunft LE datum AND kontline.abreise GE datum 
                  AND kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK:
                 FIND FIRST room-avail-list WHERE room-avail-list.sleeping 
                     AND room-avail-list.zikatnr = kontline.zikatnr NO-LOCK NO-ERROR.
                 IF AVAILABLE room-avail-list THEN
                       ASSIGN
                             room-avail-list.room[i] = room-avail-list.room[i] - kontline.zimmeranz
                             occ-room[i] = occ-room[i] + kontline.zimmeranz                               /* Dzikri BEED96 - Add new summarry */
                       . 
            END.    

            i = i + 1. 
            datum = datum + 1. 
        END.

         
        DO i = 1 TO 30: 
          sum-list.summe[i] = 0. 
          FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
            sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 
          END. 
        END. 


        IF mi-inactive THEN 
        DO: 
          i = 1. 
          datum = curr-date. 
          DO WHILE i LE (num-day + 1):  /*MT */
              FOR EACH res-line WHERE res-line.active-flag LE 1
                    AND res-line.resstatus LE 6
                    AND res-line.resstatus NE 4
                    /*AND res-line.zikatnr = room-avail-list.zikatnr*/
                    AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
                    OR (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
                    AND res-line.kontignr GE 0
                    AND res-line.l-zuordnung[3] = 0
                    AND res-line.zinr NE "" USE-INDEX res-zinr_ix NO-LOCK :

                  FIND FIRST room-avail-list WHERE NOT room-avail-list.sleeping
                      AND room-avail-list.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                  IF AVAILABLE room-avail-list THEN DO:

                        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr
                                AND NOT zimmer.sleeping NO-LOCK NO-ERROR.
                        IF AVAILABLE zimmer THEN
                        DO:
                            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                              NO-LOCK.
                            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                              NO-LOCK NO-ERROR.
                            IF AVAILABLE segment AND segment.vip-level = 0 THEN
                                room-avail-list.room[i] = room-avail-list.room[i] - 1.
                        END.
                        
                        /*zz
                        FIND FIRST resplan WHERE resplan.zikatnr = room-avail-list.zikatnr 
                          AND resplan.datum = datum NO-LOCK NO-ERROR. 
                        IF AVAILABLE resplan THEN 
                        DO:
                          room-avail-list.room[i] = room-avail-list.room[i] 
                            - resplan.anzzim[1] - resplan.anzzim[2] - resplan.anzzim[6]. 
                        END. 
                        */
                  END.
              END.


            /*FOR EACH room-avail-list WHERE NOT room-avail-list.sleeping: 
                FOR EACH res-line WHERE res-line.active-flag LE 1
                    AND res-line.resstatus LE 6
                    AND res-line.resstatus NE 4
                    AND res-line.zikatnr = room-avail-list.zikatnr
                    AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
                    OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
                    AND res-line.kontignr GE 0
                    AND res-line.l-zuordnung[3] = 0
                    AND res-line.zinr NE "" NO-LOCK :
                    
                    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr
                        AND NOT zimmer.sleeping NO-LOCK NO-ERROR.
                    IF AVAILABLE zimmer THEN
                    DO:
                        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                          NO-LOCK.
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                          NO-LOCK NO-ERROR.
                        IF AVAILABLE segment AND segment.vip-level = 0 THEN
                            room-avail-list.room[i] = room-avail-list.room[i] - 1.
                    END.
                    
                    /*zz
                    FIND FIRST resplan WHERE resplan.zikatnr = room-avail-list.zikatnr 
                      AND resplan.datum = datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE resplan THEN 
                    DO:
                      room-avail-list.room[i] = room-avail-list.room[i] 
                        - resplan.anzzim[1] - resplan.anzzim[2] - resplan.anzzim[6]. 
                    END. 
                    */
                END.
                i = i + 1.
                datum = datum + 1.
            END.*/
              i = i + 1.
              datum = datum + 1.
          END.

          DO i = 1 TO 30:
            sum-list.summe[i] = 0. 
            FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
              sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 
            END. 
          END. 
        END. 

        create sum-list. 
        ASSIGN
          sum-list.allot-flag = YES
          sum-list.bezeich = translateExtended ("Allotments",lvCAREA,""). 
        from-date = curr-date. 
        to-date = from-date + num-day.
        IF to-date GT co-date THEN to-date = co-date.
       
        i = 1. 
        DO datum = from-date TO to-date: 
          /*dody 291223 enhance stuck trace
          FOR EACH kontline WHERE kontline.betriebsnr = 0 
            AND kontline.ankunft LE datum AND kontline.abreise GE datum 
            AND kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK: 
            IF datum GE (ci-date + kontline.ruecktage) THEN 
            DO: 
              sum-list.summe[i] = sum-list.summe[i] + kontline.zimmeranz. 
              FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = kontline.zikatnr 
                AND room-avail-list.sleeping NO-ERROR. 
              IF NOT AVAILABLE room-avail-list THEN FIND FIRST room-avail-list 
                WHERE room-avail-list.sleeping NO-ERROR. 
              IF AVAILABLE room-avail-list THEN 
              room-avail-list.allotment[i] = room-avail-list.allotment[i] 
                + kontline.zimmeranz. 
            END.
          END.*/

            /*dody 291223 enhance stuck trace*/
            FOR EACH t-kontline WHERE t-kontline.betriebsnr = 0 
                AND t-kontline.ankunft LE datum AND t-kontline.abreise GE datum 
                AND t-kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK: 
                IF datum GE (ci-date + t-kontline.ruecktage) THEN 
                DO: 
                    sum-list.summe[i] = sum-list.summe[i] + t-kontline.zimmeranz. 
                    FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = t-kontline.zikatnr AND room-avail-list.sleeping NO-ERROR. 
                    IF NOT AVAILABLE room-avail-list THEN FIND FIRST room-avail-list WHERE room-avail-list.sleeping NO-ERROR. 
                    IF AVAILABLE room-avail-list THEN 
                    room-avail-list.allotment[i] = room-avail-list.allotment[i] + t-kontline.zimmeranz. 
                END.
            END.
            i = i + 1.  
        END. 

        DO i = 1 TO 30: 
          sum-list.summe[i] = sum-list.summe[i] - res-allot[i]. 
          /* Dzikri 1156B1 -  wrong number after allotment */
          FOR EACH tmp-allotment NO-LOCK:
              FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = tmp-allotment.zikatnr 
                AND room-avail-list.sleeping NO-ERROR. 
              IF AVAILABLE room-avail-list THEN 
                room-avail-list.allotment[i] = room-avail-list.allotment[i] - tmp-allotment.res-allot[i].
          END.
          /* 
          IF AVAILABLE room-avail-list THEN 
            room-avail-list.allotment[i] = room-avail-list.allotment[i] - res-allot[i]. 
            Dzikri 1156B1 -  END*/

        END. 

        DO i = 1 TO 30: 
          tmp-list[i] = sum-list.summe[i]. 
        END. 

        create sum-list. 
        sum-list.bezeich = translateExtended ("Avail After Allotm",lvCAREA,""). 
        DO i = 1 TO 30: 
          FOR EACH room-avail-list: 
            sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 

            IF dispsort = 2 THEN 
            room-avail-list.room[i] = room-avail-list.room[i] - room-avail-list.allotment[i]. 

          END. 
          sum-list.summe[i] = sum-list.summe[i] - tmp-list[i]. 
        END. 
        DO i = 1 TO 30: 
          tmp-list[i] = sum-list.summe[i]. /*save availability after allotment*/ 
        END. 

        /* Dzikri BEED96 - Add new summarry */
        CREATE sum-list.
        sum-list.bezeich = translateExtended("Room Occupied",lvCAREA,"").
        DO i = 1 TO 30:
          sum-list.summe[i] = occ-room[i].
        END.
        
        CREATE sum-list.
        sum-list.bezeich = translateExtended("Total Active Room",lvCAREA,"").
        DO i = 1 TO 30:
          sum-list.summe[i] = tot-room.
        END.
        /* Dzikri BEED96 - END */
      
        create sum-list. 
        sum-list.bezeich = translateExtended ("Total Overbooking",lvCAREA,""). 
        DO i = 1 TO 30: 
          anz = 0. 
          IF dispsort = 2 AND tmp-list[i] LT 0 THEN anz = anz - tmp-list[i]. 
          IF anz LT 0 THEN sum-list.summe[i] = - anz. 
          ELSE sum-list.summe[i] = anz.
        END. 

        create sum-list. 
        sum-list.bezeich = translateExtended ("Out-of-Order",lvCAREA,""). 
        DO i = 1 TO 30: 
          sum-list.summe[i] = ooo-list[i]. 
        END. 

        IF om-flag THEN 
        DO: 
          create sum-list. 
          sum-list.bezeich = translateExtended ("Off-Market",lvCAREA,""). 
          DO i = 1 TO 30: 
            sum-list.summe[i] = om-list[i]. 
          END. 
        END. 

        FOR EACH room-avail-list: 
          DO i = 1 TO 30: 
            room-avail-list.coom[i] = STRING(room-avail-list.room[i], "->>>,>>>,>>9"). 
          END. 
        END. 
      END. 
      ELSE IF statsort = 2 THEN RUN create-browse1. 
  END.

  ELSE /*MT incl tentative */
  DO: 
      /*MTIF statsort = 1 THEN 
      DO:*/
        /*MT !!! */
        create sum-list. 
        sum-list.bezeich = translateExtended ("Avail before Allotm",lvCAREA,""). 
        FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES 
            NO-LOCK BY zimkateg.typ BY zimkateg.zikatnr: 
          FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimkateg.zikatnr 
            AND rmcat-list.sleeping NO-ERROR. 
          IF AVAILABLE rmcat-list THEN 
          DO: 
            create room-avail-list. 
            i = 1. 
            DO WHILE i LE (num-day + 1): 
              room-avail-list.room[i] = rmcat-list.anzahl. 
              i = i + 1. 
            END. 
            ASSIGN
                room-avail-list.i-typ   = zimkateg.typ
                room-avail-list.zikatnr = zimkateg.zikatnr 
                room-avail-list.bezeich = zimkateg.kurzbez 
                  + " - " + STRING(zimkateg.overbook,">>9")
            . 
          END. 
        END. 

        FOR EACH rmcat-list WHERE NOT rmcat-list.sleeping, 
          FIRST zimkateg WHERE zimkateg.zikatnr = rmcat-list.zikatnr NO-LOCK 
          BY zimkateg.typ BY zimkateg.zikatnr: 
          create room-avail-list. 
          room-avail-list.sleeping = NO. 
          i = 1. 
          DO WHILE i LE (num-day + 1): 
            room-avail-list.room[i] = rmcat-list.anzahl. 
            i = i + 1. 
          END. 
          ASSIGN
              room-avail-list.i-typ   = zimkateg.typ
              room-avail-list.zikatnr = zimkateg.zikatnr
              room-avail-list.bezeich = zimkateg.kurzbez 
                + " - " + STRING(zimkateg.overbook,">>9")
          . 

          datum = curr-date. 

          DO i = 1 TO 30: 
            FOR EACH res-line WHERE res-line.active-flag LE 1 
              AND res-line.resstatus LE 6 
              AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
              OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
              AND res-line.zikatnr = room-avail-list.zikatnr 
              AND res-line.zinr NE "" AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK, 
              FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND 
              NOT zimmer.sleeping NO-LOCK: 

              IF NOT vhp-limited THEN do-it = YES.
              ELSE
              DO:
                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                  NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                  NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
              END.

              IF do-it THEN 
                  ASSIGN
                      room-avail-list.room[i] = room-avail-list.room[i] - 1
                      occ-room[i] = occ-room[i] + 1                               /* Dzikri BEED96 - Add new summarry */
                  . 
            END. 
            datum = datum + 1. 
          END.
        END. 

        FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
          FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
          AND zimmer.sleeping = YES NO-LOCK. 
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
          datum = curr-date. 
          FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = zimmer.zikatnr 
            AND room-avail-list.sleeping NO-LOCK NO-ERROR. 
          IF AVAILABLE room-avail-list THEN
          DO:
            DO i = 1 TO 30: 
              IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
              DO: 
                IF outorder.betriebsnr = 2 THEN 
                DO: 
                  om-list[i] = om-list[i] + 1. 
                  om-flag = YES. 
                END. 
                ELSE 
                DO:
                  ooo-list[i] = ooo-list[i] + 1. 
                  room-avail-list.room[i] = room-avail-list.room[i] - 1. 
                END. 
              END. 
              datum = datum + 1. 
            END. 
          END.            
        END. 
        
        i = 1. 
        datum = curr-date. 
        DO WHILE i LE (num-day + 1): 
          /*FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
            FOR EACH res-line WHERE res-line.active-flag LE 1 
              AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
              AND res-line.resstatus NE 4 
              AND res-line.zikatnr = room-avail-list.zikatnr 
              /*AND res-line.ankunft LE datum AND res-line.abreise GT datum */
              AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
              OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
              AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
              do-it = YES. 
              IF res-line.zinr NE "" THEN 
              DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
              END. 

              /*IF res-line.resstatus = 3 /*MTAND NOT incl-tentative*/ THEN
                  do-it = NO.*/

              IF do-it AND vhp-limited THEN
              DO:
                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                  NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                  NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
              END.

              IF do-it THEN 
                  room-avail-list.room[i] = room-avail-list.room[i] - res-line.zimmeranz.
            END. 

            FOR EACH kontline WHERE kontline.betriebsnr = 1 
              AND kontline.ankunft LE datum AND kontline.abreise GE datum 
              AND kontline.zikatnr = room-avail-list.zikatnr 
              AND kontline.kontstat = 1 NO-LOCK:
              room-avail-list.room[i] = room-avail-list.room[i] - kontline.zimmeranz. 
            END.
          END. */

          FOR EACH res-line WHERE res-line.active-flag LE 1 
              AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
              AND res-line.resstatus NE 4 
              /*AND res-line.zikatnr = room-avail-list.zikatnr 
              AND res-line.ankunft LE datum AND res-line.abreise GT datum */
              AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
              OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
              AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 

              FIND FIRST room-avail-list WHERE room-avail-list.sleeping
                  AND room-avail-list.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
              IF AVAILABLE room-avail-list THEN DO:
                  do-it = YES. 
                  IF res-line.zinr NE "" THEN 
                  DO: 
                    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                    do-it = zimmer.sleeping. 
                  END. 
        
                  /*IF res-line.resstatus = 3 /*MTAND NOT incl-tentative*/ THEN
                      do-it = NO.*/
        
                  IF do-it AND vhp-limited THEN
                  DO:
                    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                      NO-LOCK.
                    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                      NO-LOCK NO-ERROR.
                    do-it = AVAILABLE segment AND segment.vip-level = 0.
                  END.
        
                  IF do-it THEN 
                      ASSIGN
                          room-avail-list.room[i] = room-avail-list.room[i] - res-line.zimmeranz
                          occ-room[i] = occ-room[i] + res-line.zimmeranz                               /* Dzikri BEED96 - Add new summarry */
                      . 
              END.              
          END. 

          FOR EACH kontline WHERE kontline.betriebsnr = 1 
              AND kontline.ankunft LE datum AND kontline.abreise GE datum 
              /*AND kontline.zikatnr = room-avail-list.zikatnr */
              AND kontline.kontstat = 1 NO-LOCK:
              FIND FIRST room-avail-list WHERE room-avail-list.sleeping
                  AND room-avail-list.zikatnr = kontline.zikatnr NO-LOCK NO-ERROR.
              IF AVAILABLE room-avail-list THEN DO:
                  room-avail-list.room[i] = room-avail-list.room[i] - kontline.zimmeranz. 
                  occ-room[i] = occ-room[i] + kontline.zimmeranz.                               /* Dzikri BEED96 - Add new summarry */
              END.
          END.

          i = i + 1. 
          datum = datum + 1. 
        END. 

        DO i = 1 TO 30: 
          sum-list.summe[i] = 0. 
          FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
            sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 
          END. 
        END. 

        IF mi-inactive THEN 
        DO: 
          i = 1. 
          datum = curr-date. 
          DO WHILE i LE (num-day + 1): 
             FOR EACH res-line WHERE res-line.active-flag LE 1
                AND res-line.resstatus LE 6
                AND res-line.resstatus NE 4
                /*AND res-line.zikatnr = room-avail-list.zikatnr
                AND res-line.ankunft LE datum
                AND res-line.abreise GT datum*/
                AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
                OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
                AND res-line.kontignr GE 0
                AND res-line.l-zuordnung[3] = 0
                AND res-line.zinr NE "" USE-INDEX res-zinr_ix NO-LOCK :

                 FIND FIRST room-avail-list WHERE NOT room-avail-list.sleeping
                     AND room-avail-list.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                 IF AVAILABLE room-avail-list THEN DO:
                     FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr
                            AND NOT zimmer.sleeping NO-LOCK NO-ERROR.
                    IF AVAILABLE zimmer THEN
                    DO:
                      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                        NO-LOCK.
                      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                        NO-LOCK NO-ERROR.
                      IF AVAILABLE segment AND segment.vip-level = 0 THEN
                        room-avail-list.room[i] = room-avail-list.room[i] - 1.
                    END.
                 END.
             END.

            /*FOR EACH room-avail-list WHERE NOT room-avail-list.sleeping: 
              FOR EACH res-line WHERE res-line.active-flag LE 1
                AND res-line.resstatus LE 6
                AND res-line.resstatus NE 4
                AND res-line.zikatnr = room-avail-list.zikatnr
                /*AND res-line.ankunft LE datum
                AND res-line.abreise GT datum*/
                AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
                OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
                AND res-line.kontignr GE 0
                AND res-line.l-zuordnung[3] = 0
                AND res-line.zinr NE ""
                NO-LOCK :
                FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr
                  AND NOT zimmer.sleeping NO-LOCK NO-ERROR.
                IF AVAILABLE zimmer THEN
                DO:
                  FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                    NO-LOCK.
                  FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                    NO-LOCK NO-ERROR.
                  IF AVAILABLE segment AND segment.vip-level = 0 THEN
                    room-avail-list.room[i] = room-avail-list.room[i] - 1.
                END.
              END.
              /*FIND FIRST resplan WHERE resplan.zikatnr = room-avail-list.zikatnr 
                AND resplan.datum = datum NO-LOCK NO-ERROR. 
              IF AVAILABLE resplan THEN 
              DO: 
                room-avail-list.room[i] = room-avail-list.room[i] 
                  - resplan.anzzim[1] - resplan.anzzim[2] - resplan.anzzim[6]. 
              END.*/ 
            
              i = i + 1. 
              datum = datum + 1. 
            END.*/

             i = i + 1. 
              datum = datum + 1.
          END. 

          DO i = 1 TO 30: 
            sum-list.summe[i] = 0. 
            FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
              sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 
            END. 
          END. 
        END. 

        /*MT !!! */
        RUN create-tentative.
        
        /*MT !!! 
        FOR EACH room-avail-list:
            DELETE room-avail-list.
        END.
        create sum-list. 
        ASSIGN
          sum-list.allot-flag = YES
          sum-list.bezeich = translateExtended ("Avail Incl Tentative",lvCAREA,""). 
*/
        /*FTFOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES 
            NO-LOCK BY zimkateg.typ BY zimkateg.zikatnr: 
          FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimkateg.zikatnr 
            AND rmcat-list.sleeping NO-ERROR. 
          IF AVAILABLE rmcat-list THEN 
          DO: 
            create room-avail-list. 
            i = 1. 
            DO WHILE i LE (num-day + 1): 
              room-avail-list.room[i] = rmcat-list.anzahl. 
              i = i + 1. 
            END. 
            ASSIGN
                room-avail-list.i-typ   = zimkateg.typ
                room-avail-list.zikatnr = zimkateg.zikatnr 
                room-avail-list.bezeich = STRING(zimkateg.kurzbez,"x(6)") 
                  + " - " + STRING(zimkateg.overbook,">>9")
            . 
          END. 
        END.*/ 

        /*FTFOR EACH rmcat-list WHERE NOT rmcat-list.sleeping, 
          FIRST zimkateg WHERE zimkateg.zikatnr = rmcat-list.zikatnr NO-LOCK 
          BY zimkateg.typ BY zimkateg.zikatnr: 
          create room-avail-list. 
          room-avail-list.sleeping = NO. 
          i = 1. 
          DO WHILE i LE (num-day + 1): 
            room-avail-list.room[i] = rmcat-list.anzahl. 
            i = i + 1. 
          END. 
          ASSIGN
              room-avail-list.i-typ   = zimkateg.typ
              room-avail-list.zikatnr = zimkateg.zikatnr 
              room-avail-list.bezeich = STRING(zimkateg.kurzbez,"x(6)") 
                + " - " + STRING(zimkateg.overbook,">>9")
          . 

          datum = curr-date. 

          DO i = 1 TO 30: 
            FOR EACH res-line WHERE res-line.active-flag LE 1 AND 
              res-line.resstatus LE 6 AND res-line.ankunft LE datum 
              AND res-line.abreise GT datum AND res-line.zikatnr = room-avail-list.zikatnr 
              AND res-line.zinr NE "" AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
              FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND 
              NOT zimmer.sleeping NO-LOCK: 

              IF NOT vhp-limited THEN do-it = YES.
              ELSE
              DO:
                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                  NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                  NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
              END.

              IF do-it THEN room-avail-list.room[i] = room-avail-list.room[i] - 1. 
                  
            END. 
            datum = datum + 1. 
          END. 
        END.*/ 

        /*MT
        FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
          FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
          AND zimmer.sleeping = YES NO-LOCK. 
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
          datum = curr-date. 
          FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = zimmer.zikatnr 
            AND room-avail-list.sleeping. 
          DO i = 1 TO 30: 
            IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
            DO: 
              IF outorder.betriebsnr = 2 THEN 
              DO: 
                om-list[i] = om-list[i] + 1. 
                om-flag = YES. 
              END. 
              ELSE 
              DO:
                ooo-list[i] = ooo-list[i] + 1. 
                room-avail-list.room[i] = room-avail-list.room[i] - 1. 
              END. 
            END. 
            datum = datum + 1. 
         END. 
        END. 
        */
        /*
        i = 1. 
        datum = curr-date. 
        DO WHILE i LE (num-day + 1): 
          FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
            FOR EACH res-line WHERE res-line.active-flag LE 1 
              AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
              AND res-line.resstatus NE 4 
              AND res-line.zikatnr = room-avail-list.zikatnr 
              AND res-line.ankunft LE datum AND res-line.abreise GT datum 
              AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
              do-it = YES. 
              IF res-line.zinr NE "" THEN 
              DO: 
                FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
                do-it = zimmer.sleeping. 
              END. 

              IF res-line.resstatus = 3 AND NOT incl-tentative THEN
                  do-it = NO.

              IF do-it AND vhp-limited THEN
              DO:
                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                  NO-LOCK.
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                  NO-LOCK NO-ERROR.
                do-it = AVAILABLE segment AND segment.vip-level = 0.
              END.

              IF do-it THEN 
                  room-avail-list.room[i] = room-avail-list.room[i] - res-line.zimmeranz. 
            END. 

            FOR EACH kontline WHERE kontline.betriebsnr = 1 
              AND kontline.ankunft LE datum AND kontline.abreise GE datum 
              AND kontline.zikatnr = room-avail-list.zikatnr 
              AND kontline.kontstat = 1 NO-LOCK: 
              room-avail-list.room[i] = room-avail-list.room[i] - kontline.zimmeranz. 
            END. 
          END. 
          i = i + 1. 
          datum = datum + 1. 
        END. 
        DO i = 1 TO 30: 
          sum-list.summe[i] = 0. 
          FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
            sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 
          END. 
        END. 

        IF mi-inactive THEN 
        DO: 
          i = 1. 
          datum = curr-date. 
          DO WHILE i LE (num-day + 1): 
            FOR EACH room-avail-list WHERE NOT room-avail-list.sleeping: 
              FIND FIRST resplan WHERE resplan.zikatnr = room-avail-list.zikatnr 
                AND resplan.datum = datum NO-LOCK NO-ERROR. 
              IF AVAILABLE resplan THEN 
              DO: 
                room-avail-list.room[i] = room-avail-list.room[i] 
                  - resplan.anzzim[1] - resplan.anzzim[2] - resplan.anzzim[6]. 
              END. 
            END. 
            i = i + 1. 
            datum = datum + 1. 
          END. 
          DO i = 1 TO 30: 
            sum-list.summe[i] = 0. 
            FOR EACH room-avail-list WHERE room-avail-list.sleeping: 
              sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 
            END. 
          END. 
        END. 
        /*endFT*/*/


        /*MT !!! */
        create sum-list. 
        ASSIGN
          sum-list.allot-flag = YES
          sum-list.bezeich = translateExtended ("Allotments",lvCAREA,""). 
        from-date = curr-date. 
        to-date = from-date + num-day.
        IF to-date GT co-date THEN to-date = co-date.

        i = 1. 
        DO datum = from-date TO to-date: 
            /*dody 291223 enhance stuck trace
          FOR EACH kontline WHERE kontline.betriebsnr = 0 
            AND kontline.ankunft LE datum AND kontline.abreise GE datum 
            AND kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK: 
            IF datum GE (ci-date + kontline.ruecktage) THEN 
            DO: 
              sum-list.summe[i] = sum-list.summe[i] + kontline.zimmeranz. 
              FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = kontline.zikatnr 
                AND room-avail-list.sleeping NO-ERROR. 
              IF NOT AVAILABLE room-avail-list THEN FIND FIRST room-avail-list 
                WHERE room-avail-list.sleeping NO-ERROR. 
              IF AVAILABLE room-avail-list THEN 
              room-avail-list.allotment[i] = room-avail-list.allotment[i] 
                + kontline.zimmeranz. 
            END.
          END.*/

            /*dody 291223 enhance stuck trace*/
            FOR EACH t-kontline WHERE t-kontline.betriebsnr = 0 
                AND t-kontline.ankunft LE datum AND t-kontline.abreise GE datum 
                AND t-kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK: 
                IF datum GE (ci-date + t-kontline.ruecktage) THEN 
                DO: 
                    sum-list.summe[i] = sum-list.summe[i] + t-kontline.zimmeranz. 
                    FIND FIRST room-avail-list WHERE room-avail-list.zikatnr = t-kontline.zikatnr AND room-avail-list.sleeping NO-ERROR. 
                    IF NOT AVAILABLE room-avail-list THEN FIND FIRST room-avail-list WHERE room-avail-list.sleeping NO-ERROR. 
                    IF AVAILABLE room-avail-list THEN 
                    room-avail-list.allotment[i] = room-avail-list.allotment[i] + t-kontline.zimmeranz. 
                END.
            END.
            i = i + 1.  
        END. 

        DO i = 1 TO 30: 
          sum-list.summe[i] = sum-list.summe[i] - res-allot[i]. 
          IF AVAILABLE room-avail-list THEN 
            room-avail-list.allotment[i] = room-avail-list.allotment[i] - res-allot[i]. 
        END. 

        DO i = 1 TO 30: 
          tmp-list[i] = sum-list.summe[i]. 
        END. 

        create sum-list. 
        sum-list.bezeich = translateExtended ("Avail After Allotm",lvCAREA,""). 
        DO i = 1 TO 30: 
          FOR EACH room-avail-list: 
            sum-list.summe[i] = sum-list.summe[i] + room-avail-list.room[i]. 

            IF dispsort = 2 THEN 
            room-avail-list.room[i] = room-avail-list.room[i] - room-avail-list.allotment[i]. 

          END. 
          sum-list.summe[i] = sum-list.summe[i] - tmp-list[i]. 
        END. 
        DO i = 1 TO 30: 
          tmp-list[i] = sum-list.summe[i]. /*save availability after allotment*/ 
        END. 
        
        
        /* Dzikri BEED96 - Add new summarry */
        CREATE sum-list.
        sum-list.bezeich = translateExtended("Room Occupied",lvCAREA,"").
        DO i = 1 TO 30:
          sum-list.summe[i] = occ-room[i].
        END.
        
        CREATE sum-list.
        sum-list.bezeich = translateExtended("Total Active Room",lvCAREA,"").
        DO i = 1 TO 30:
          sum-list.summe[i] = tot-room.
        END.
        /* Dzikri BEED96 - END */
        
        create sum-list. 
        sum-list.bezeich = translateExtended ("Total Overbooking",lvCAREA,""). 
        DO i = 1 TO 30: 
          anz = 0. 
          IF dispsort = 2 AND tmp-list[i] LT 0 THEN anz = anz - tmp-list[i]. 
          IF anz LT 0 THEN sum-list.summe[i] = - anz.
          ELSE sum-list.summe[i] = anz. 
        END. 

        create sum-list. 
        sum-list.bezeich = translateExtended ("Out-of-Order",lvCAREA,""). 
        DO i = 1 TO 30: 
          sum-list.summe[i] = ooo-list[i]. 
        END. 

        IF om-flag THEN 
        DO: 
          create sum-list. 
          sum-list.bezeich = translateExtended ("Off-Market",lvCAREA,""). 
          DO i = 1 TO 30: 
            sum-list.summe[i] = om-list[i]. 
          END. 
        END. 

        FOR EACH room-avail-list: 
          DO i = 1 TO 30: 
            room-avail-list.coom[i] = STRING(room-avail-list.room[i], "->>>,>>>,>>9"). 
          END. 
        END. 
      /*MTEND. 
      ELSE IF statsort = 2 THEN RUN create-browse1.*/
  END.

END. 
/* %%% */ 
PROCEDURE create-browse1: 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE abreise1 AS DATE. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE tmp-list AS INTEGER EXTENT 30. 
DEFINE VARIABLE avail-list AS INTEGER EXTENT 30. 
DEFINE VARIABLE om-flag AS LOGICAL INITIAL NO. 
 
  create room-avail-list. 
  room-avail-list.bezeich = translateExtended ("Total Active Rooms",lvCAREA,""). 
  DO i = 1 TO 30: 
    room-avail-list.room[i] = tot-room. 
    tmp-list[i] = tot-room. 
  END. 
 
  create room-avail-list. 
  room-avail-list.bezeich = translateExtended ("Out-of-order",lvCAREA,""). 
  FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK: 
    FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK. 
    IF zimmer.sleeping THEN 
    DO: 
      datum = curr-date. 
      DO i = 1 TO 30: 
        IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
        DO: 
          room-avail-list.room[i] = room-avail-list.room[i] + 1. 
          tmp-list[i] = tmp-list[i] - 1. 
        END. 
        datum = datum + 1. 
      END. 
    END. 
  END. 
  
  create room-avail-list. 
  room-avail-list.bezeich = translateExtended ("Occupied",lvCAREA,""). 
  DO i = 1 TO 30: 
    avail-list[i] = 0. 
  END. 
  FOR EACH res-line WHERE res-line.resstatus = 6 AND active-flag = 1 
    AND res-line.abreise GE curr-date AND res-line.active-flag = 1
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 

    IF NOT vhp-limited THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK.
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
    END.
    
    IF do-it THEN
    DO:
/*  occupied */ 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
      IF zimmer.sleeping THEN 
      DO: 
        datum1 = curr-date + num-day. 
        IF datum1 GT co-date THEN datum1 = co-date.
        abreise1 = res-line.abreise - 1. 
        IF abreise1 LT datum1 THEN datum1 = abreise1. 
        i = 1. 
        DO datum = curr-date TO datum1: 
          room-avail-list.room[i] = room-avail-list.room[i] + 1. 
          tmp-list[i] = tmp-list[i] - 1. 
          i = i + 1. 
        END. 
/* will be vacant */ 
        i = res-line.abreise - curr-date + 1. 
        IF i GE 1 AND i LE 30 THEN avail-list[i] = avail-list[i] + 1. 
      END.
    END. /* IF do-it */
  END. 
 
  create room-avail-list. 
  create room-avail-list. 
  room-avail-list.bezeich = translateExtended ("Rentable",lvCAREA,""). 
  DO i = 1 TO 30: 
    room-avail-list.room[i] = tmp-list[i]. 
  END. 
 
  create room-avail-list. 
  room-avail-list.bezeich = translateExtended ("Guaranted",lvCAREA,""). 
  FOR EACH zimkateg NO-LOCK: 
    i = 1. 
    datum = curr-date. 
    DO WHILE i LE (num-day + 1): 
      FOR EACH res-line WHERE res-line.active-flag = 0 
        AND res-line.resstatus = 1 AND res-line.zikatnr = zimkateg.zikatnr 
        /*AND res-line.ankunft LE datum AND res-line.abreise GT datum */
        AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
        OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
        AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK: 
        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
          do-it = zimmer.sleeping. 
        END. 
        
        IF do-it AND vhp-limited THEN 
        DO:
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK.
          FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
        
        IF do-it THEN 
        DO: 
          room-avail-list.room[i] = room-avail-list.room[i] + res-line.zimmeranz. 
          tmp-list[i] = tmp-list[i] - res-line.zimmeranz. 
        END. 
      END. 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
 
  CREATE room-avail-list. 
  room-avail-list.bezeich = translateExtended ("6 PM",lvCAREA,""). 
  FIND FIRST htparam WHERE htparam.paramnr = 297 NO-LOCK.
  IF htparam.finteger NE 0 THEN room-avail-list.bezeich = STRING(htparam.finteger) 
    + " " + translateExtended ("PM",lvCAREA,""). 

  FOR EACH zimkateg NO-LOCK: 
    i = 1. 
    datum = curr-date. 
    DO WHILE i LE (num-day + 1): 
      FOR EACH res-line WHERE res-line.active-flag = 0 
        AND res-line.resstatus = 2 AND res-line.zikatnr = zimkateg.zikatnr 
        /*AND res-line.ankunft LE datum AND res-line.abreise GT datum */
        AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
        OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
        AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK: 
        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
          do-it = zimmer.sleeping. 
        END. 
        
        IF do-it AND vhp-limited THEN 
        DO:
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK.
          FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
        
        IF do-it THEN 
        DO: 
          room-avail-list.room[i] = room-avail-list.room[i] + res-line.zimmeranz. 
          tmp-list[i] = tmp-list[i] - res-line.zimmeranz. 
        END. 
      END. 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
 
  CREATE room-avail-list. 
  room-avail-list.bezeich = translateExtended ("Oral Confirmed",lvCAREA,""). 
  FOR EACH zimkateg NO-LOCK: 
    i = 1. 
    datum = curr-date. 
    DO WHILE i LE (num-day + 1): 
      FOR EACH res-line WHERE res-line.active-flag = 0 
        AND res-line.resstatus = 5 AND res-line.zikatnr = zimkateg.zikatnr 
        /*AND res-line.ankunft LE datum AND res-line.abreise GT datum */
        AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
        OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
        AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK: 
        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
          do-it = zimmer.sleeping. 
        END. 
        
        IF do-it AND vhp-limited THEN 
        DO:
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK.
          FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
        
        IF do-it THEN 
        DO: 
          room-avail-list.room[i] = room-avail-list.room[i] + res-line.zimmeranz. 
          tmp-list[i] = tmp-list[i] - res-line.zimmeranz. 
        END. 
      END. 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 

  CREATE room-avail-list. 
  room-avail-list.bezeich = translateExtended ("Global Reservation",lvCAREA,""). 
  FOR EACH zimkateg NO-LOCK: 
    i = 1. 
    datum = curr-date. 
    DO WHILE i LE (num-day + 1): 
      FOR EACH kontline WHERE kontline.kontignr GT 0 
        AND kontline.betriebsnr = 1 
        AND kontline.ankunft LE datum AND kontline.abreise GE datum 
        AND kontline.zikatnr = zimkateg.zikatnr 
        AND kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK: 
        room-avail-list.room[i] = room-avail-list.room[i] + kontline.zimmeranz. 
        tmp-list[i] = tmp-list[i] - kontline.zimmeranz. 
      END. 
 
      FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
        AND res-line.resstatus NE 4 
        AND res-line.zikatnr = zimkateg.zikatnr 
        /*AND res-line.ankunft LE datum AND res-line.abreise GT datum */
        AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
        OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
        AND res-line.kontignr LT 0 AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK: 
        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
          do-it = zimmer.sleeping. 
        END. 

        IF res-line.resstatus = 3 AND NOT incl-tentative THEN
            do-it = NO.

        IF do-it AND vhp-limited THEN
        DO:
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK.
          FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
          do-it = AVAILABLE segment AND segment.vip-level = 0.
        END.
        
        IF do-it THEN 
        DO: 
          room-avail-list.room[i] = room-avail-list.room[i] - res-line.zimmeranz. 
          tmp-list[i] = tmp-list[i] + res-line.zimmeranz. 
        END. 
      END. 
 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
 
  CREATE room-avail-list. 
  CREATE room-avail-list. 
  ASSIGN
    room-avail-list.avail-flag = YES
    room-avail-list.bezeich = translateExtended ("Total Availability",lvCAREA,""). 
  DO i = 1 TO 30: 
    room-avail-list.room[i] = tmp-list[i]. 
  END. 
 
  create room-avail-list. 
  ASSIGN
    room-avail-list.allot-flag = YES
    room-avail-list.bezeich = translateExtended ("Allotments",lvCAREA,""). 
  from-date = curr-date. 
  to-date = from-date + num-day. 
  IF to-date GT co-date THEN to-date = co-date.
  i = 1. 


  DO datum = from-date TO to-date: 
    FOR EACH kontline WHERE kontline.betriebsnr = 0 
      AND kontline.ankunft LE datum AND kontline.abreise GE datum 
      AND kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK: 
      IF datum GE (ci-date + kontline.ruecktage) THEN 
      DO: 
        room-avail-list.room[i] = room-avail-list.room[i] + kontline.zimmeranz. 
        tmp-list[i] = tmp-list[i] - kontline.zimmeranz. 
      END.
    END.
    i = i + 1.  
  END. 
 
  DO i = 1 TO 30: 
    room-avail-list.room[i] = room-avail-list.room[i] - res-allot[i]. 
    tmp-list[i] = tmp-list[i] + res-allot[i]. 
  END. 
 
  create room-avail-list. 
  ASSIGN
    room-avail-list.avail-flag = YES
    room-avail-list.bezeich = translateExtended ("Avail After Allotm",lvCAREA,""). 
  DO i = 1 TO 30: 
    room-avail-list.room[i] = tmp-list[i]. 
  END. 
 
  FOR EACH room-avail-list WHERE room-avail-list.bezeich NE "": 
    DO i = 1 TO 30: 
      coom[i] = STRING(room[i], "->>>,>>>,>>9"). 
    END. 
  END. 
 
  datum = curr-date.
  create sum-list. 
  sum-list.bezeich = translateExtended ("Tentative",lvCAREA,""). 
  /*FOR EACH zimkateg NO-LOCK: */
      FOR EACH res-line WHERE res-line.active-flag LE 1 
          AND res-line.resstatus EQ 3 
          /*AND res-line.ankunft LE datum 
          AND res-line.abreise GT datum */
          AND ((res-line.ankunft LE datum AND res-line.abreise GT datum)
          OR  (res-line.ankunft EQ datum AND res-line.abreise EQ datum))
          /*AND res-line.zikatnr = room-avail-list.zikatnr 
          AND res-line.zinr NE "" */
          AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK /*, 
          FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND 
          NOT zimmer.sleeping NO-LOCK*/ : 
          i = 1.
          DO WHILE i LE (num-day + 1): 
              sum-list.summe[i] = sum-list.summe[i] + 1.
              i = i + 1.
          END.
      END.
  /*END. */
 
  create sum-list. 
  sum-list.bezeich = translateExtended ("Waiting List",lvCAREA,""). 
  FOR EACH zimkateg NO-LOCK: 
    i = 1. 
    datum = curr-date. 
    DO WHILE i LE (num-day + 1): 
      FOR EACH resplan WHERE resplan.datum = datum 
          AND resplan.zikatnr = zimkateg.zikatnr  NO-LOCK: 
        sum-list.summe[i] = sum-list.summe[i] + resplan.anzzim[4]. 
      END. 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
 
  create sum-list. 
  sum-list.bezeich = translateExtended ("Exp.Departure",lvCAREA,""). 
  DO i = 1 TO 30: 
    sum-list.summe[i] = avail-list[i]. 
  END. 
 
  om-flag = NO. 
  create sum-list. 
  sum-list.bezeich = translateExtended ("Off-Market",lvCAREA,""). 
  FOR EACH outorder WHERE outorder.betriebsnr = 2 NO-LOCK: 
    datum = curr-date. 
    DO i = 1 TO 30: 
      IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
      DO: 
        sum-list.summe[i] = sum-list.summe[i] + 1. 
        om-flag = YES. 
      END. 
      datum = datum + 1. 
    END. 
  END. 
  IF NOT om-flag THEN delete sum-list. 
 
END. 


PROCEDURE clear-it:
    FOR EACH sum-list:
        DELETE sum-list.
    END.

    FOR EACH room-avail-list:
        DELETE room-avail-list.
    END.
END.

