DEFINE TEMP-TABLE na-list 
  FIELD reihenfolge AS INTEGER 
  FIELD flag        AS INTEGER 
  FIELD bezeich     LIKE nightaudit.bezeichnung 
  FIELD anz         AS INTEGER FORMAT ">>,>>9". 

DEFINE INPUT-OUTPUT  PARAMETER TABLE FOR na-list.
DEFINE INPUT         PARAMETER ci-date  AS DATE.
DEFINE OUTPUT        PARAMETER i        AS INTEGER.


RUN update-rmstatus.

FIND FIRST htparam WHERE htparam.paramnr = 592.
ASSIGN htparam.flogical = NO.
FIND CURRENT htparam NO-LOCK.

PROCEDURE update-rmstatus: 
  FIND FIRST na-list WHERE na-list.reihenfolge = 3. 
  FIND FIRST zimmer NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE zimmer: 
    IF zimmer.zistatus = 0 OR zimmer.zistatus = 1 OR zimmer.zistatus = 2 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO transaction: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        IF res-line.abreise = ci-date THEN zimmer.zistatus = 3. 
        ELSE zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
    END. 
    ELSE IF zimmer.zistatus = 3 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line AND res-line.abreise GT ci-date THEN 
      DO transaction: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
      ELSE IF NOT AVAILABLE res-line THEN 
      DO transaction: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 1. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
    END. 
    ELSE IF zimmer.zistatus = 4 OR zimmer.zistatus = 5 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line AND res-line.abreise EQ ci-date THEN 
      DO transaction: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 3. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
      ELSE IF NOT AVAILABLE res-line THEN 
      DO transaction: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 1. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
    END. 
    IF zimmer.zistatus = 6 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 
        AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO TRANSACTION: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        IF res-line.abreise = ci-date THEN zimmer.zistatus = 3. 
        ELSE zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
          AND outorder.gespstart LT res-line.abreise EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN delete outorder. 
      END. 
      ELSE
      DO TRANSACTION:
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
            AND outorder.gespstart LE ci-date
            AND outorder.gespende GE ci-date
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE outorder THEN
        DO:
          FIND CURRENT zimmer EXCLUSIVE-LOCK.
          ASSIGN
            zimmer.bediener-nr-stat = 0
            zimmer.zistatus = 2
          .
          FIND CURRENT zimmer NO-LOCK.
        END.
      END.
    END. 
    FIND NEXT zimmer NO-LOCK NO-ERROR. 
  END. 
 
  FOR EACH zimkateg: 
    i = 0. 
    FOR EACH zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr NO-LOCK: 
      i = i + 1. 
    END. 
    zimkateg.maxzimanz = i. 
  END. 
 
  PAUSE 0. 
END.
