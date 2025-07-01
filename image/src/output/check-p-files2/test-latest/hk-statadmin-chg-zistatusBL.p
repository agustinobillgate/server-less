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
DEF INPUT  PARAMETER ci-date AS DATE.
DEF INPUT  PARAMETER chgsort AS INT.
DEF INPUT  PARAMETER t-zinr AS CHAR.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF INPUT  PARAMETER user-nr AS INT.

DEF OUTPUT PARAMETER curr-zinr AS CHAR.
DEF OUTPUT PARAMETER curr-stat AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR z-list.

DEF VARIABLE from-stat AS CHAR FORMAT "x(100)".
DEF VARIABLE to-stat   AS CHAR FORMAT "x(100)".

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-statadmin".
DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(23)" NO-UNDO. 
stat-list[1] = translateExtended ("Vacant Clean Checked", lvCAREA,""). 
stat-list[2] = translateExtended ("Vacant Clean Unchecked", lvCAREA,""). 
stat-list[3] = translateExtended ("Vacant Dirty", lvCAREA,""). 
stat-list[4] = translateExtended ("Expected Departure", lvCAREA,""). 
stat-list[5] = translateExtended ("Occupied Dirty", lvCAREA,""). 
stat-list[6] = translateExtended ("Occupied Cleaned", lvCAREA,""). 
stat-list[7] = translateExtended ("Out-of-Order", lvCAREA,""). 
stat-list[8] = translateExtended ("Off-Market", lvCAREA,""). 
stat-list[9] = translateExtended ("Do not Disturb", lvCAREA,""). 
stat-list[10] = translateExtended ("Out-of-Service",lvCAREA,""). 

FIND FIRST zimmer WHERE zimmer.zinr = t-zinr NO-LOCK NO-ERROR.

RUN chg-zistatus.

PROCEDURE chg-zistatus:
  DEFINE VARIABLE result AS LOGICAL. 
  FOR EACH bline-list WHERE bline-list.selected = YES: 
    DO TRANSACTION: 
      FIND FIRST zimmer WHERE zimmer.zinr = bline-list.zinr EXCLUSIVE-LOCK. 
      from-stat = STRING(zimmer.zistatus) + " " + stat-list[zimmer.zistatus + 1]. 
      IF chgsort = 8 THEN zimmer.zistatus = 8. 
      ELSE 
      DO: 
        IF chgsort = 3 AND (zimmer.zistatus LE 1 OR zimmer.zistatus = 5) AND zimmer.personal = YES THEN zimmer.personal = NO.

        IF (zimmer.zistatus = 0 OR zimmer.zistatus = 1 OR zimmer.zistatus = 2) 
        THEN 
        DO: 
            zimmer.zistatus = chgsort - 1. 
        END. 
        ELSE IF zimmer.zistatus = 4 AND chgsort = 1 THEN zimmer.zistatus = 5. 
        ELSE IF zimmer.zistatus = 5 AND chgsort = 3 THEN zimmer.zistatus = 4. 
        ELSE IF zimmer.zistatus = 8 THEN zimmer.zistatus = 4. 

        to-stat = STRING(zimmer.zistatus) + " " + stat-list[zimmer.zistatus + 1]. 

        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
        CREATE res-history. 
        ASSIGN 
          res-history.nr = bediener.nr 
          res-history.datum = TODAY 
          res-history.zeit = TIME 
          res-history.aenderung = "Room " + zimmer.zinr 
             + " Status Changed From " 
             + FROM-stat + " to " + to-stat
          res-history.action = "HouseKeeping". 
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history.

      END. 
      zimmer.bediener-nr-stat = user-nr.
      FIND CURRENT zimmer NO-LOCK.
      
      IF zimmer.zistatus = 0 THEN
      DO: /* set queuing room as done */
          FIND FIRST queasy WHERE queasy.KEY = 162
              AND queasy.char1 = zimmer.zinr NO-ERROR.
          IF AVAILABLE queasy THEN 
          DO:    
              ASSIGN 
                  queasy.number1 = 1
                  queasy.char3   = user-init
                  queasy.number3 = TIME
                  queasy.date3   = TODAY
              .
              FIND CURRENT queasy NO-LOCK.
          END.
      END.
    END. 
      

    
    FIND FIRST om-list WHERE om-list.zinr = zimmer.zinr. 
    IF om-list.ind NE 8 THEN om-list.ind = zimmer.zistatus + 1. 
    FIND CURRENT zimmer NO-LOCK. 
    curr-zinr = zimmer.zinr. 
    curr-stat = stat-list[zimmer.zistatus + 1]. /* Malik Serverless : stat-list[zistatus + 1] -> stat-list[zimmer.zistatus + 1] */
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
