

DEF VARIABLE anz-tage  AS INTEGER NO-UNDO INIT 60.
DEF VARIABLE hist-tage AS INTEGER NO-UNDO INIT 180.
DEF VARIABLE ci-date   AS DATE    NO-UNDO.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

/* storage duration for system logfile */
FIND FIRST htparam WHERE paramnr = 371 NO-LOCK.  
IF htparam.paramgr = 9 AND htparam.finteger NE 0 THEN
  ASSIGN anz-tage = htparam.finteger.
IF hist-tage LT anz-tage THEN hist-tage = anz-tage.

RUN update-logfile-records.

PROCEDURE update-logfile-records: 
DEF VARIABLE do-it  AS LOGICAL NO-UNDO.
DEF BUFFER reshis   FOR res-history. 
DEF BUFFER r-queasy FOR reslin-queasy. 
DEF BUFFER qsy      FOR queasy.

/* Nortel temporary calls record if not deleted yet */
  FIND FIRST queasy WHERE queasy.KEY = 39
    AND queasy.date1 LT (ci-date - anz-tage) NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE queasy:
    DO TRANSACTION:
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK.
        DELETE qsy.
        RELEASE qsy.
    END.
    FIND NEXT queasy WHERE queasy.KEY = 39
      AND queasy.date1 LT (ci-date - anz-tage) NO-LOCK NO-ERROR.
  END.

/* remove approval */
  FIND FIRST queasy WHERE queasy.KEY = 36
    AND queasy.date1 LT (ci-date - anz-tage) NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE queasy:
    DO TRANSACTION:
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK.
        DELETE qsy.
        RELEASE qsy.
    END.
    FIND NEXT queasy WHERE queasy.KEY = 36
      AND queasy.date1 LT (ci-date - anz-tage) NO-LOCK NO-ERROR.
  END.
  
  FIND FIRST res-history WHERE res-history.action = "HouseKeeping" 
    AND res-history.datum LT (ci-date - anz-tage) 
    AND res-history.zeit GE 0 
    AND res-history.aenderung MATCHES ("*Status Changed*" )
    USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-history: 
    DO TRANSACTION: 
      FIND FIRST reshis WHERE RECID(reshis) = RECID(res-history) 
        EXCLUSIVE-LOCK. 
      DELETE reshis. 
      RELEASE reshis. 
    END. 
    FIND NEXT res-history WHERE res-history.action = "HouseKeeping" 
      AND res-history.datum LT (ci-date - anz-tage) 
      AND res-history.zeit GE 0 
      AND res-history.aenderung MATCHES ("*Status Changed*" )
      USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  END. 
 
  FIND FIRST res-history WHERE res-history.action = "HouseKeeping" 
    AND res-history.datum LT (ci-date - hist-tage) 
    AND res-history.zeit GE 0 
    USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-history: 
    DO TRANSACTION: 
      FIND FIRST reshis WHERE RECID(reshis) = RECID(res-history) 
        EXCLUSIVE-LOCK. 
      DELETE reshis. 
      RELEASE reshis. 
    END. 
    FIND NEXT res-history WHERE res-history.action = "HouseKeeping" 
      AND res-history.datum LT (ci-date - anz-tage) 
      AND res-history.zeit GE 0 
      USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  END. 

  FIND FIRST res-history WHERE res-history.datum LT (ci-date - hist-tage) 
      AND res-history.zeit GE 0 USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-history: 
    do-it = YES.
    IF res-history.action = "G/L" AND res-history.datum GE (ci-date - 750) 
      THEN do-it = NO.
    ELSE IF res-history.action = "reservation" 
      AND res-history.aenderung MATCHES ("*delete*")
      AND res-history.datum GE (ci-date - 365) THEN do-it = NO.
    IF do-it THEN
    DO TRANSACTION: 
      FIND FIRST reshis WHERE RECID(reshis) = RECID(res-history) 
        EXCLUSIVE-LOCK. 
        DELETE reshis. 
        RELEASE reshis. 
    END. 
    FIND NEXT res-history WHERE res-history.datum LT (ci-date - hist-tage) 
      AND res-history.zeit GE 0 USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  END. 

  /*gerald 040620*/
  FIND FIRST res-history WHERE res-history.action = "G/L" 
    AND res-history.datum LT (ci-date - anz-tage) 
    AND res-history.zeit GE 0 
    USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-history: 
    DO TRANSACTION: 
      FIND FIRST reshis WHERE RECID(reshis) = RECID(res-history) 
        EXCLUSIVE-LOCK. 
      DELETE reshis. 
      RELEASE reshis. 
    END. 
    FIND NEXT res-history WHERE res-history.action = "G/L" 
      AND res-history.datum LT (ci-date - anz-tage) 
      AND res-history.zeit GE 0 
      USE-INDEX date-time_ix NO-LOCK NO-ERROR. 
  END. 
 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "ResChanges" 
    AND reslin-queasy.char1 NE "" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE reslin-queasy THEN RETURN. 
  DO WHILE AVAILABLE reslin-queasy: 
    DO TRANSACTION: 
      FIND FIRST r-queasy WHERE RECID(r-queasy) = RECID(reslin-queasy) 
        EXCLUSIVE-LOCK. 
      r-queasy.char3 = reslin-queasy.char1. 
      r-queasy.char1 = "". 
      FIND CURRENT r-queasy NO-LOCK. 
    END. 
    FIND NEXT reslin-queasy WHERE reslin-queasy.key = "ResChanges" 
      AND reslin-queasy.char1 NE "" NO-LOCK NO-ERROR. 
  END. 
END. 
