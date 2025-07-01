DEF TEMP-TABLE z-list
    FIELD zinr              LIKE zimmer.zinr
    FIELD setup             LIKE zimmer.setup
    FIELD zikatnr           LIKE zimmer.zikatnr
    FIELD etage             LIKE zimmer.etage
    FIELD zistatus          LIKE zimmer.zistatus
    FIELD CODE              LIKE zimmer.CODE
    FIELD bediener-nr-stat  LIKE zimmer.bediener-nr-stat
    FIELD checkout          AS LOGICAL INITIAL NO
    FIELD str-reason        AS CHAR.
  

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD ind AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE bline-list 
  FIELD zinr AS CHAR 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD bl-recid AS INTEGER. 

DEF INPUT-OUTPUT  PARAMETER TABLE FOR bline-list.
DEF INPUT-OUTPUT  PARAMETER TABLE FOR om-list.
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER ci-date AS DATE.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER reason AS CHAR.
DEF INPUT PARAMETER service-flag AS LOGICAL.
DEF INPUT PARAMETER user-nr AS INT.

DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR z-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-statadmin".

DEF BUFFER obuff FOR outorder.

DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE cat-flag AS LOGICAL INIT NO.
DEFINE VARIABLE roomnr   AS INT INIT 0.
DEFINE BUFFER zbuff FOR zimkateg.
DEFINE BUFFER qsy FOR queasy.

FOR EACH bline-list WHERE bline-list.SELECTED:
    FIND FIRST obuff WHERE obuff.zinr = bline-list.zinr
        AND ((obuff.gespstart GE from-date AND obuff.gespstart LE to-date)
          OR (obuff.gespende GE from-date AND obuff.gespende LE to-date)
          OR (from-date GE obuff.gespstart AND from-date LE obuff.gespende)
          OR (to-date GE obuff.gespstart AND to-date LE obuff.gespende))
         NO-LOCK NO-ERROR.
    IF AVAILABLE obuff THEN
    DO:
        /* Dzikri 1C80AD - error data pop-up */
        ASSIGN
          msg-str = translateExtended ("Overlapping O-O-O or O-M record found!",lvCAREA,"") + " " + STRING(bline-list.zinr)
          flag = 1
        .
        /* Dzikri 1C80AD - END */
        LEAVE.
    END.
END.

IF flag = 1 THEN RETURN.

FOR EACH bline-list WHERE bline-list.selected = YES: 
    FIND FIRST zimmer WHERE zimmer.zinr = bline-list.zinr NO-LOCK. 
    FIND FIRST res-line WHERE res-line.active-flag LE 1 AND 
        ((res-line.ankunft GE from-date AND res-line.ankunft LE to-date) OR 
         (res-line.abreise GT from-date AND res-line.abreise LE to-date) OR 
         (from-date GE res-line.ankunft AND from-date LT res-line.abreise)) 
        AND res-line.zinr EQ bline-list.zinr NO-LOCK NO-ERROR.

    IF AVAILABLE res-line THEN 
    DO: 
        msg-str = translateExtended ("Attention: Room Number",lvCAREA,"") + 
                " " + STRING(bline-list.zinr) + CHR(10) +
                translateExtended ("Reservation exists under ResNo",lvCAREA,"") + 
                " = " + STRING(res-line.resnr) + CHR(10) +
                translateExtended ("Guest Name",lvCAREA,"") + 
                " = " + res-line.name + CHR(10) +
                translateExtended ("Arrival :",lvCAREA,"") + 
                " " + STRING(res-line.ankunft) + "   " + 
                translateExtended ("Departure :",lvCAREA,"") + 
                " " + STRING(res-line.abreise).
        flag = 2.
        LEAVE. 
    END. 
    ELSE 
    DO: 
        DO TRANSACTION: 
          CREATE outorder. 
          outorder.zinr = bline-list.zinr. 
          outorder.gespstart = from-date. 
          outorder.gespende  = to-date. 
          outorder.betriebsnr = dept. 
          outorder.gespgrund = reason + "$" + STRING(user-nr). 
 
          IF service-flag THEN outorder.betriebsnr = 
              outorder.betriebsnr + 3. 
 
          FIND CURRENT outorder NO-LOCK. 

          FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN cat-flag = YES.
    
          FIND FIRST zbuff WHERE zbuff.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
          IF AVAILABLE zbuff THEN
          DO:
            IF cat-flag THEN roomnr = zbuff.typ.
            ELSE roomnr = zbuff.zikatnr.
          END.

          DO datum = from-date TO to-date:
            FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
              AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
            IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
            DO:
              FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
              IF AVAILABLE qsy THEN
              DO:
                  qsy.logi2 = YES.
                  FIND CURRENT qsy NO-LOCK.
                  RELEASE qsy.
              END.
            END.                            
          END.

           /*ITA 260525 Log Availability*/
            CREATE res-history. 
            ASSIGN 
              res-history.nr        = user-nr
              res-history.datum     = TODAY
              res-history.zeit      = TIME 
              res-history.aenderung = "Change to OOO - Room : " + bline-list.zinr
              res-history.action    = "Log Availability"
            . 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 

          IF NOT service-flag THEN
          DO:
              CREATE res-history. 
              ASSIGN 
                res-history.nr = user-nr 
                res-history.datum = TODAY 
                res-history.zeit = TIME 
                res-history.aenderung = "Set O-O-O to Room " + bline-list.zinr 
                   + " " + STRING(from-date) + " - " + STRING(to-date)
                   + "; " + reason
                res-history.action = "HouseKeeping". 
              FIND CURRENT res-history NO-LOCK. 
              RELEASE res-history. 
          END.


          IF from-date EQ ci-date THEN
          DO:
            FIND CURRENT zimmer EXCLUSIVE-LOCK. 
            zimmer.bediener-nr-stat = user-nr. 
            FIND FIRST res-line WHERE res-line.active-flag = 1
              AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE res-line THEN
            DO:
              zimmer.zistatus = 6. 
              FIND FIRST om-list WHERE om-list.zinr = zimmer.zinr. 
              IF outorder.betriebsnr = 3 OR outorder.betriebsnr = 4 THEN
                  om-list.ind = 10.
              ELSE om-list.ind = 7. 
            END.
            FIND CURRENT zimmer NO-LOCK. 
          END.
          bline-list.selected = NO. 
          RELEASE outorder.
        END. 
    END. 
END.

IF flag = 2 THEN RETURN.

FOR EACH z-list:
    DELETE z-list.
END.

FOR EACH zimmer NO-LOCK:
    CREATE z-list.
    BUFFER-COPY zimmer TO z-list.
    IF zimmer.zistatus = 2 THEN 
    DO:
      FIND FIRST res-line WHERE res-line.resstatus = 8 
          AND res-line.zinr = zimmer.zinr
          AND res-line.abreise = ci-date NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN z-list.checkout = YES.
    END.

    /*ITA 030717*/
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
        AND outorder.betriebsnr LE 2 
        AND outorder.gespstart LE ci-date 
        AND outorder.gespende GE ci-date NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN 
        ASSIGN z-list.str-reason = ENTRY(1, outorder.gespgrund, "$").
    ELSE ASSIGN z-list.str-reason = " ".
END.

