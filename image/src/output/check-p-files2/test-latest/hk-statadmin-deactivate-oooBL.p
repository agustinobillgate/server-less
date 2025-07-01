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

DEF INPUT-OUTPUT PARAMETER TABLE FOR bline-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR om-list.
DEF INPUT PARAMETER ci-date AS DATE.
DEF INPUT PARAMETER user-nr AS INT.
DEF INPUT PARAMETER chgsort AS INT.
DEF OUTPUT PARAMETER TABLE FOR z-list.

DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE cat-flag AS LOGICAL INIT NO.
DEFINE VARIABLE roomnr   AS INT INIT 0.
DEFINE BUFFER zbuff FOR zimkateg.
DEFINE BUFFER qsy   FOR queasy.


RUN deactivate-ooo.

PROCEDURE deactivate-ooo:
  DEFINE VARIABLE answer AS LOGICAL. 
  DEFINE VARIABLE result AS LOGICAL. 
  DEF VAR oos-flag AS LOGICAL INITIAL NO NO-UNDO. 
  DEF VAR ooo-flag AS LOGICAL INITIAL NO NO-UNDO. /*MT 01/11/12 */
 
  FOR EACH bline-list WHERE bline-list.selected = YES: 
      FIND FIRST zimmer WHERE zimmer.zinr = bline-list.zinr NO-LOCK. 

      FOR EACH outorder WHERE outorder.zinr = bline-list.zinr EXCLUSIVE-LOCK: 
          oos-flag = (outorder.betriebsnr = 3 OR outorder.betriebsnr = 4).
          /*MT 01/11/12 */
          ooo-flag = (outorder.betriebsnr LE 1 AND 
                      ci-date GE outorder.gespstart AND 
                      ci-date LE outorder.gespende).

          IF oos-flag AND (outorder.gespstart = outorder.gespende) THEN 
          DO: 
            FIND FIRST zinrstat WHERE zinrstat.zinr = "oos" 
              AND zinrstat.datum = ci-date NO-ERROR. 
            IF NOT AVAILABLE zinrstat THEN 
            DO: 
              CREATE zinrstat. 
              ASSIGN 
                zinrstat.datum = ci-date 
                zinrstat.zinr = "oos". 
            END. 
            zinrstat.zimmeranz = zinrstat.zimmeranz + 1. 
            delete outorder.
            RELEASE outorder.
          END. 
          /*MT 01/11/12 */
          ELSE IF ooo-flag THEN 
          DO:
              FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN cat-flag = YES.
            
              FIND FIRST zbuff WHERE zbuff.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
              IF AVAILABLE zbuff THEN
              DO:
                IF cat-flag THEN roomnr = zbuff.typ.
                ELSE roomnr = zbuff.zikatnr.
              END.

              DO datum = outorder.gespstart TO outorder.gespende:
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
              CREATE res-history. 
              ASSIGN 
                res-history.nr = user-nr 
                res-history.datum = TODAY 
                res-history.zeit = TIME 
                res-history.aenderung = "Remove O-O-O Record of Room " + outorder.zinr 
                   + " " + STRING(outorder.gespstart) + "-" + STRING(outorder.gespende)
                res-history.action = "HouseKeeping". 
              FIND CURRENT res-history NO-LOCK. 
              RELEASE res-history. 

              /*ITA 260525 Log Availability*/
                CREATE res-history. 
                ASSIGN 
                  res-history.nr        = user-nr
                  res-history.datum     = TODAY 
                  res-history.zeit      = TIME 
                  res-history.aenderung = "Remove O-O-O Record of Room " + outorder.zinr 
                                          + " " + STRING(outorder.gespstart) + "-" + STRING(outorder.gespende)
                  res-history.action    = "Log Availability"
                . 
                FIND CURRENT res-history NO-LOCK. 
                RELEASE res-history. 


              delete outorder.
              RELEASE outorder.
          END.
          /*MT 01/11/12 */

          /*MT 01/11/12 delete outorder. */
      END. 

      FIND CURRENT zimmer EXCLUSIVE-LOCK. 
      zimmer.bediener-nr-stat = user-nr. 
      IF zimmer.zistatus GE 6 THEN 
      DO: 
        zimmer.zistatus = chgsort - 1. 
        FIND FIRST om-list WHERE om-list.zinr = zimmer.zinr. 
        om-list.ind = zimmer.zistatus + 1. 
      END. 
      FIND CURRENT zimmer NO-LOCK. 
      bline-list.selected = NO. 
  END.

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
END. 
