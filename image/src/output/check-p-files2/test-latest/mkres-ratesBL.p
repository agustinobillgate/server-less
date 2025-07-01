
DEFINE TEMP-TABLE reslin-list LIKE res-line.

DEFINE TEMP-TABLE Res-Dynarate
    FIELD date1  AS DATE
    FIELD date2  AS DATE
    FIELD rate   AS DECIMAL
    FIELD rmCat  AS CHAR
    FIELD argt   AS CHAR
    FIELD prcode AS CHAR
    FIELD rCode  AS CHAR
    FIELD markNo AS INTEGER
    FIELD setup  AS INTEGER
    FIELD adult  AS INTEGER
    FIELD child  AS INTEGER
    INDEX date1_ix date1
  .

DEFINE TEMP-TABLE room-list 
  FIELD avail-flag  AS LOGICAL INITIAL NO
  FIELD allot-flag  AS LOGICAL INITIAL NO
  FIELD zikatnr     AS INTEGER 
  FIELD i-typ       AS INTEGER
  FIELD sleeping    AS LOGICAL INITIAL YES 
  FIELD allotment   AS INTEGER EXTENT 30 
  FIELD bezeich     AS CHAR FORMAT "x(19)"
  FIELD room        AS INTEGER EXTENT 30 
  FIELD coom        AS CHAR EXTENT 30 FORMAT "x(12)"

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
  FIELD minadvance    AS INTEGER INIT 0
  FIELD maxadvance    AS INTEGER INIT 0    
  FIELD frdate        AS DATE INIT ?
  FIELD todate        AS DATE INIT ?
  FIELD marknr      AS INTEGER INIT 0
  FIELD datum       AS DATE EXTENT 30
. 

DEFINE TEMP-TABLE t-rqy LIKE reslin-queasy
    FIELD count-i AS INTEGER.
    .

DEF INPUT PARAMETER from-date   AS DATE    NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR    NO-UNDO.
DEF INPUT PARAMETER chg-zikat   AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER chg-flag    AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER TABLE FOR reslin-list.
DEF INPUT PARAMETER TABLE FOR room-list.
DEF OUTPUT PARAMETER ratecode-bez  AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER new-segm      AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER fixed-rate    AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER room-rate     AS DECIMAL NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE FOR Res-Dynarate. 
    
DEF VARIABLE resno       AS INTEGER NO-UNDO.
DEF VARIABLE reslinno    AS INTEGER NO-UNDO.
DEF VARIABLE ankunft     AS DATE    NO-UNDO.
DEF VARIABLE abreise     AS DATE    NO-UNDO.
DEF VARIABLE curr-argt   AS CHAR    NO-UNDO.
DEF VARIABLE ractive     AS LOGICAL NO-UNDO.

DEF VARIABLE curr-i         AS INTEGER NO-UNDO.
DEF VARIABLE fr-date        AS DATE    NO-UNDO.
DEF VARIABLE checkin-date   AS DATE    NO-UNDO.
DEF VARIABLE curr-date      AS DATE    NO-UNDO.
DEF VARIABLE to-date        AS DATE    NO-UNDO.
DEF VARIABLE p-493          AS LOGICAL NO-UNDO.
DEF VARIABLE cid            AS CHAR NO-UNDO INIT "".
DEF VARIABLE cdate          AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 
DEF VARIABLE counter        AS INTEGER NO-UNDO.

DEF BUFFER r-qsy FOR reslin-queasy.
DEF BUFFER bqueasy FOR queasy.

FIND FIRST reslin-list.
FIND FIRST room-list.

ASSIGN
    resno     = reslin-list.resnr
    reslinno  = reslin-list.reslinnr
    ankunft   = reslin-list.ankunft
    abreise   = reslin-list.abreise
    curr-argt = reslin-list.arrangement.

IF reslin-list.changed NE ? THEN
ASSIGN
    cid   = reslin-list.changed-id  
    cdate = STRING(reslin-list.changed)
.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN checkin-date = htparam.fdate.

/*ITA 260418 Request Harris Kelapa Gading*/
FIND FIRST htparam WHERE htparam.paramnr = 493 NO-LOCK.
ASSIGN p-493 = htparam.flogical.

counter = 1.
/* IF p-493 = YES THEN DO: Comment Ita Intruction*/
FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
    AND reslin-queasy.resnr    = resno
    AND reslin-queasy.reslinnr = reslinno
    AND ((reslin-queasy.date1 GE from-date
    AND reslin-queasy.date1 LE (abreise - 1)) OR (reslin-queasy.date1 GE from-date
    AND reslin-queasy.date2 LE (abreise - 1))):            
    
    /*FDL June 13, 2024 => Ticket 71CA90*/
    CREATE t-rqy.
    ASSIGN            
        t-rqy.key       = "ResChanges"
        t-rqy.count-i   = counter
        t-rqy.resnr     = resno   
        t-rqy.reslinnr  = reslinno
        t-rqy.date2     = TODAY
        t-rqy.number2   = TIME 
        . 
    t-rqy.char3 = STRING(reslin-list.ankunft) + ";" 
        + STRING(reslin-list.ankunft) + ";" 
        + STRING(reslin-list.abreise) + ";" 
        + STRING(reslin-list.abreise) + ";" 
        + STRING(reslin-list.zimmeranz) + ";" 
        + STRING(reslin-list.zimmeranz) + ";" 
        + STRING(reslin-list.erwachs) + ";" 
        + STRING(reslin-list.erwachs) + ";" 
        + STRING(reslin-list.kind1) + ";" 
        + STRING(reslin-list.kind1) + ";" 
        + STRING(reslin-list.gratis) + ";" 
        + STRING(reslin-list.gratis) + ";" 
        + STRING(reslin-list.zikatnr) + ";" 
        + STRING(reslin-list.zikatnr) + ";" 
        + STRING(reslin-list.zinr) + ";" 
        + STRING(reslin-list.zinr) + ";"
        + STRING(reslin-list.arrangement) + ";" 
        + STRING(reslin-list.arrangement) + ";"
        + STRING(reslin-list.zipreis) + ";" 
        + STRING(reslin-list.zipreis) + ";"
        + STRING(cid) + ";" 
        + STRING(user-init) + ";" 
        + STRING(cdate, "x(8)") + ";" 
        + STRING(TODAY) + ";" 
        + STRING("Modify Fixrate FR:") + ";" 
        + STRING(reslin-queasy.date1) 
        + "-" + STRING(reslin-queasy.deci1) + ";"
        + STRING("YES", "x(3)") + ";" 
        + STRING("YES", "x(3)") + ";" 
    .
    counter = counter + 2.

    DELETE reslin-queasy.
    RELEASE reslin-queasy.
END.
/*END.*/

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = room-list.rcode NO-LOCK.
IF AVAILABLE queasy THEN DO:
    FIND FIRST bqueasy WHERE bqueasy.KEY = 264
        AND bqueasy.char1 = queasy.char1 NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy AND bqueasy.logi1 THEN ASSIGN ratecode-bez = queasy.char1 + " - " + queasy.char2.
    ELSE ASSIGN ratecode-bez = queasy.char1 + " - " + queasy.char2.
END.

DO TRANSACTION:
/* split fixed rates to each single date */
  FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
    AND reslin-queasy.resnr    = resno
    AND reslin-queasy.reslinnr = reslinno
    AND reslin-queasy.date1 LT reslin-queasy.date2:
    DO:
        to-date = reslin-queasy.date2.
        FIND FIRST r-qsy WHERE RECID(r-qsy) = RECID(reslin-queasy).
        ASSIGN r-qsy.date2 = r-qsy.date1.
        FIND CURRENT r-qsy NO-LOCK.
        RELEASE r-qsy.
    END.
    curr-date = reslin-queasy.date1.
    DO curr-i = 2 TO (to-date - reslin-queasy.date1):
        ASSIGN curr-date = curr-date + 1.
      DO:
        CREATE r-qsy.
        BUFFER-COPY reslin-queasy EXCEPT date1 date2 TO r-qsy.
        ASSIGN 
            r-qsy.date1 = curr-date
            r-qsy.date2 = curr-date
        .
        FIND CURRENT r-qsy NO-LOCK.
        RELEASE r-qsy.
      END.
    END.
  END.  

  counter = 2.
/* assign the rates to the date(s) which no rate defined yet */
  ASSIGN
        fixed-rate = YES
        fr-date    = from-date.
  DO curr-i = 1 TO (abreise - from-date):
      FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
          AND reslin-queasy.resnr    = resno
          AND reslin-queasy.reslinnr = reslinno
          AND reslin-queasy.date1    = fr-date
          AND reslin-queasy.date2    = fr-date NO-LOCK NO-ERROR.

/* SY 17 AUG 2015 */
      IF NOT AVAILABLE reslin-queasy THEN
      DO:
        CREATE reslin-queasy.
        ASSIGN
          reslin-queasy.key      = "arrangement"
          reslin-queasy.resnr    = resno 
          reslin-queasy.reslinnr = reslinno
          reslin-queasy.date1    = fr-date 
          reslin-queasy.date2    = fr-date
          reslin-queasy.deci1    = room-list.rmrate[curr-i]
          reslin-queasy.char2    = room-list.prcode[curr-i]
          reslin-queasy.char3    = user-init
        .        

        IF curr-argt NE room-list.argt THEN 
          ASSIGN reslin-queasy.char1 = room-list.argt.     

        /*FDL June 13, 2024 => Ticket 71CA90*/
        CREATE t-rqy.
        ASSIGN            
            t-rqy.key       = "ResChanges"
            t-rqy.count-i   = counter
            t-rqy.resnr     = resno   
            t-rqy.reslinnr  = reslinno
            t-rqy.date2     = TODAY
            t-rqy.number2   = TIME 
            . 
        t-rqy.char3 = STRING(reslin-list.ankunft) + ";" 
            + STRING(reslin-list.ankunft) + ";" 
            + STRING(reslin-list.abreise) + ";" 
            + STRING(reslin-list.abreise) + ";" 
            + STRING(reslin-list.zimmeranz) + ";" 
            + STRING(reslin-list.zimmeranz) + ";" 
            + STRING(reslin-list.erwachs) + ";" 
            + STRING(reslin-list.erwachs) + ";" 
            + STRING(reslin-list.kind1) + ";" 
            + STRING(reslin-list.kind1) + ";" 
            + STRING(reslin-list.gratis) + ";" 
            + STRING(reslin-list.gratis) + ";" 
            + STRING(reslin-list.zikatnr) + ";" 
            + STRING(reslin-list.zikatnr) + ";" 
            + STRING(reslin-list.zinr) + ";" 
            + STRING(reslin-list.zinr) + ";"
            + STRING(reslin-list.arrangement) + ";" 
            + STRING(reslin-list.arrangement) + ";"
            + STRING(reslin-list.zipreis) + ";" 
            + STRING(reslin-list.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + STRING("Modify Fixrate TO:") + ";" 
            + STRING(reslin-queasy.date1) 
            + "-" + STRING(reslin-queasy.deci1) + ";"
            + STRING("YES", "x(3)") + ";" 
            + STRING("YES", "x(3)") + ";" 
        .
        counter = counter + 2.        
      END.
/* SY 17 AUG 2015: create fixed rate only if it does not exist yet,
   eg when the user extends the check-out date.
   Delete the existing fixed rate(s) first if you want to update it 
      ELSE 
      DO:    
        IF NOT chg-flag THEN /* To keep the created rates */
        ASSIGN
          room-list.rmrate[curr-i] = reslin-queasy.deci1
          room-list.prcode[curr-i] = reslin-queasy.char2
        .
        ELSE
        ASSIGN
          reslin-queasy.deci1    = room-list.rmrate[curr-i]
          reslin-queasy.char2    = room-list.prcode[curr-i]
          reslin-queasy.char1    = room-list.argt
        .
      END.*/
      

      IF curr-i = 1 THEN room-rate = reslin-queasy.deci1.
      ASSIGN fr-date = fr-date + 1.
  END.  
  /*FDL June 13, 2024 => Ticket 71CA90*/
  FOR EACH t-rqy NO-LOCK BY t-rqy.count-i:
    CREATE reslin-queasy.
    BUFFER-COPY t-rqy TO reslin-queasy.
  END.

/* SY 19 AUG 2015 deactivate, cleaning up will be done 
   in mk-res-gobl.p
  FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
    AND reslin-queasy.resnr    = resno
    AND reslin-queasy.reslinnr = reslinno NO-LOCK:
    IF reslin-queasy.date2 LT from-date THEN .
    ELSE 
    DO:    
      FIND FIRST r-qsy WHERE RECID(r-qsy) = RECID(reslin-queasy).
      IF reslin-queasy.date1 LT from-date
        AND reslin-queasy.date2 GE from-date THEN
      DO:
        r-qsy.date2 = from-date - 1.
        FIND CURRENT r-qsy NO-LOCK.
      END.
      ELSE IF room-list.dynarate THEN DELETE r-qsy.
      RELEASE r-qsy.
    END.
  END.
*/

  FIND FIRST zimkateg WHERE zimkateg.kurzbez = room-list.rmcat.
  FIND FIRST res-line WHERE res-line.resnr = resno
    AND res-line.reslinnr = reslinno EXCLUSIVE-LOCK.

  RUN update-qsy171.

  ASSIGN
    res-line.zimmer-wunsch  = reslin-list.zimmer-wunsch
    res-line.arrangement    = reslin-list.arrangement
    res-line.betriebsnr     = reslin-list.betriebsnr
    res-line.zipreis        = reslin-list.zipreis
    res-line.reserve-int    = room-list.marknr
    res-line.zikatnr        = zimkateg.zikatnr
    res-line.l-zuordnung[1] = zimkateg.zikatnr
  .

  IF chg-zikat THEN
  ASSIGN
    res-line.zinr  = ""
    res-line.setup = 0
  .
  FIND CURRENT res-line NO-LOCK.
    
  ASSIGN ractive = YES.
  FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = room-list.rcode NO-LOCK.
  FIND FIRST bqueasy WHERE bqueasy.KEY = 264
        AND bqueasy.char1 = queasy.char1 NO-LOCK NO-ERROR.
  IF AVAILABLE bqueasy THEN ASSIGN ractive = NOT bqueasy.logi1.


  IF ENTRY(1, queasy.char3, ";") NE "" AND ractive AND 
    ((reslin-list.active-flag = 0) OR
     (reslin-list.active-flag = 1) AND (from-date = checkin-date))  THEN
  DO:
    FIND FIRST segment WHERE segment.bezeich = ENTRY(1, queasy.char3, ";")
        NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
      FIND FIRST reservation WHERE reservation.resnr = resno
        EXCLUSIVE-LOCK. 
      ASSIGN 
        reservation.segmentcode = segment.segmentcode
        new-segm                = STRING(segment.segmentcode) + " "
                                + segment.bezeich
      .
      FIND CURRENT reservation NO-LOCK.
    END.
  END.

  IF room-list.dynarate THEN
  DO:
    FOR EACH res-dynarate:
      IF res-dynarate.date2 LT from-date THEN .
      ELSE IF res-dynarate.date1 LT checkin-date
        AND res-dynarate.date2 GE checkin-date THEN
        res-dynarate.date2 = checkin-date - 1.
      ELSE DELETE res-dynarate.
    END.
  
    ASSIGN
      fixed-rate = YES
      fr-date    = from-date
    .
    DO curr-i = 1 TO (abreise - from-date):
      CREATE res-dynarate.
      ASSIGN  res-dynarate.date1  = fr-date
            res-dynarate.date2  = fr-date
            res-dynarate.rmcat  = room-list.rmcat
            res-dynarate.argt   = room-list.argt
            res-dynarate.markNo = room-list.marknr
            res-dynarate.adult  = room-list.adult
            res-dynarate.child  = room-list.child
            res-dynarate.rcode  = room-list.rcode
            res-dynarate.prcode = room-list.prcode[curr-i]
            res-dynarate.rate   = room-list.rmrate[curr-i]
      .
      
      FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
          AND reslin-queasy.resnr    = resno
          AND reslin-queasy.reslinnr = reslinno
          AND reslin-queasy.date1    = fr-date
          AND reslin-queasy.date2    = fr-date NO-ERROR.
      IF NOT AVAILABLE reslin-queasy THEN
      DO:
        CREATE reslin-queasy.
        ASSIGN
            reslin-queasy.key      = "arrangement"
            reslin-queasy.resnr    = resno 
            reslin-queasy.reslinnr = reslinno
            reslin-queasy.date1    = fr-date 
            reslin-queasy.date2    = fr-date
            reslin-queasy.deci1    = room-list.rmrate[curr-i]
            reslin-queasy.char2    = room-list.prcode[curr-i]
            reslin-queasy.char3    = user-init
          .
        IF curr-argt NE room-list.argt THEN 
      END.
      IF curr-i = 1 THEN room-rate = reslin-queasy.deci1.      

      ASSIGN 
          fr-date             = fr-date + 1
          res-dynarate.rate   = reslin-queasy.deci1
          reslin-queasy.char1 = room-list.argt
      .

    END.
  END.

  FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
      AND reslin-queasy.resnr    = resno
      AND reslin-queasy.reslinnr = reslinno:
      IF reslin-queasy.date2 LT reslin-list.ankunft THEN
          DELETE reslin-queasy.
      ELSE IF reslin-queasy.date1 GE reslin-list.abreise THEN
          DELETE reslin-queasy.
  END.

END. /* end transaction */

/* SY 22/11/2014 */
IF reslin-list.active-flag = 0 THEN
    RUN check-bonus-nightbl.p(reslin-list.ankunft, 
        reslin-list.abreise, INPUT-OUTPUT TABLE res-dynarate).

PROCEDURE update-qsy171:
    DEFINE BUFFER qsy FOR queasy.
    DEFINE BUFFER zbuff  FOR zimkateg.
    
    DEFINE VARIABLE upto-date   AS DATE.
    DEFINE VARIABLE datum       AS DATE.
    DEFINE VARIABLE start-date  AS DATE.
    
    DEFINE VARIABLE i           AS INT INIT 0.
    DEFINE VARIABLE iftask      AS CHAR INIT "".
    DEFINE VARIABLE origcode    AS CHAR INIT "".
    DEFINE VARIABLE newcode     AS CHAR INIT "".
    DEFINE VARIABLE do-it       AS LOGICAL INIT NO.
    DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.

    DEFINE VARIABLE roomnr      AS INT INIT 0.
    DEFINE VARIABLE roomnr1     AS INT INIT 0.

    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
        IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
        DO:
            origcode  = SUBSTR(iftask,11).
            LEAVE.
        END.
    END. 

    DO i = 1 TO NUM-ENTRIES(reslin-list.zimmer-wunsch,";") - 1:
        iftask = ENTRY(i, reslin-list.zimmer-wunsch, ";").
        IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
        DO:
            newcode  = SUBSTR(iftask,11).
            LEAVE.
        END.
    END. 

    FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN cat-flag = YES.

    FIND FIRST zbuff WHERE zbuff.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    IF cat-flag AND AVAILABLE zbuff THEN
        ASSIGN 
            roomnr = zbuff.typ
            roomnr1 = zimkateg.typ.
    ELSE IF AVAILABLE zbuff THEN
        ASSIGN 
            roomnr = zbuff.zikatnr
            roomnr1 = zimkateg.zikatnr.

    IF origcode = newcode AND res-line.zikatnr = zimkateg.zikatnr THEN.
    ELSE IF origcode NE "" OR newcode NE "" THEN
    DO:
        IF res-line.ankunft = res-line.abreise THEN upto-date = res-line.abreise .
            ELSE upto-date = res-line.abreise  - 1. 
        IF res-line.zikatnr NE zimkateg.zikatnr THEN
        DO:
            DO datum = res-line.ankunft TO upto-date:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND CURRENT queasy EXCLUSIVE-LOCK.
                    queasy.logi2 = YES.
                    FIND CURRENT queasy NO-LOCK.
                    RELEASE queasy.
                END. 
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr1 AND queasy.char1 = newcode NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND CURRENT queasy EXCLUSIVE-LOCK.
                    queasy.logi2 = YES.
                    FIND CURRENT queasy NO-LOCK.
                    RELEASE queasy.
                END. 
            END.
        END.
        ELSE IF res-line.zikatnr = zimkateg.zikatnr AND origcode NE newcode  THEN
        DO:
            DO datum = res-line.ankunft TO upto-date:
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND CURRENT queasy EXCLUSIVE-LOCK.
                    queasy.logi2 = YES.
                    FIND CURRENT queasy NO-LOCK.
                    RELEASE queasy.
                END. 
                FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
                    AND queasy.number1 = roomnr AND queasy.char1 = newcode NO-LOCK NO-ERROR.
                IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
                DO:
                    FIND CURRENT queasy EXCLUSIVE-LOCK.
                    queasy.logi2 = YES.
                    FIND CURRENT queasy NO-LOCK.
                    RELEASE queasy.
                END. 
            END.
        END.
    END.
END.
