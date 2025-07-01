DEFINE WORKFILE reslist 
   FIELD resnr AS INTEGER. 


DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.
DEFINE OUTPUT PARAMETER j       AS INTEGER INIT 0 NO-UNDO.
DEFINE OUTPUT PARAMETER k       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-res.

PROCEDURE del-old-res: 
DEFINE VARIABLE anz       AS INTEGER. 
DEFINE VARIABLE delete-it AS LOGICAL. 
  FIND FIRST htparam WHERE paramnr = 162 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
  /*MTmess-str = translateExtended ("Deleted old reservations",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST res-line WHERE (res-line.resstatus = 8 OR res-line.resstatus = 12) 
    AND res-line.active-flag = 2 
    AND res-line.abreise LT (ci-date - anz) NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    
    FIND FIRST bill WHERE bill.resnr = res-line.resnr AND bill.reslinnr = 0
        AND bill.flag = 0 NO-LOCK NO-ERROR.
    delete-it = NOT (AVAILABLE bill).

    IF delete-it THEN 
    DO: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Deleted old reservations",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND FIRST reslist WHERE reslist.resnr = res-line.resnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reslist THEN 
      DO: 
        CREATE reslist. 
        reslist.resnr = res-line.resnr. 
      END.

      DO TRANSACTION: 
        FIND FIRST gentable WHERE gentable.key = "reservation" 
          AND gentable.number1 = res-line.resnr 
          AND gentable.number2 = res-line.reslinnr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gentable THEN DELETE gentable.
        
        FIND FIRST archieve WHERE archieve.KEY = "send-sign-rc"
            AND archieve.num1 = res-line.resnr 
            AND archieve.num2 = res-line.reslinnr
            AND archieve.num3 = res-line.gastnrmember NO-ERROR.
        IF AVAILABLE archieve THEN DELETE archieve.

        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
          AND fixleist.reslinnr = res-line.reslinnr: 
            delete fixleist. 
        END. 
        
        FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        
        FOR EACH reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
 
        FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "ResChanges" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
 
            FIND FIRST res-history WHERE res-history.resnr = res-line.resnr 
              AND res-history.reslinnr = res-line.reslinnr 
              AND res-history.datum = reslin-queasy.date2 
              AND res-history.zeit = reslin-queasy.number2 
              EXCLUSIVE-LOCK NO-ERROR. 
            IF AVAILABLE res-history THEN DELETE res-history. 
 
            DELETE reslin-queasy. 
        END. 
 
        FOR EACH res-history WHERE res-history.resnr = res-line.resnr 
            AND res-history.reslinnr = res-line.reslinnr 
            AND res-history.datum GE res-line.ankunft 
            AND res-history.zeit GE 0 USE-INDEX res_ix: 
            DELETE res-history. 
        END. 
 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND reslin-queasy.betriebsnr = 0 EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN delete reslin-queasy. 
        FOR EACH mast-art WHERE mast-art.resnr = res-line.resnr 
          AND mast-art.reslinnr = res-line.reslinnr: 
          delete mast-art. 
        END. 
 
        FOR EACH res-history WHERE res-history.resnr = res-line.resnr 
            AND res-history.reslinnr = res-line.reslinnr 
            AND res-history.datum GE res-line.ankunft 
            AND res-history.datum LE res-line.abreise 
            AND res-history.zeit = 0 
            AND res-history.action = "N/A": 
            DELETE res-history. 
        END. 
 
        FIND CURRENT res-line EXCLUSIVE-LOCK. 
        DELETE res-line. 
      END. 
    END. 
    FIND NEXT res-line WHERE (res-line.resstatus = 8 OR res-line.resstatus = 12) 
      AND res-line.active-flag = 2 
    AND res-line.abreise LT (ci-date - anz) NO-LOCK NO-ERROR. 
  END. 
  FOR EACH reslist: 
    FIND FIRST res-line WHERE res-line.resnr = reslist.resnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN 
    DO: 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog" 
        AND reslin-queasy.number1 = reslist.resnr 
        AND reslin-queasy.number2 = 0 AND reslin-queasy.char1 = "" 
        AND reslin-queasy.reslinnr = 1 USE-INDEX argt_ix 
        EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN delete reslin-queasy. 
      FIND FIRST reservation WHERE reservation.resnr = reslist.resnr 
        EXCLUSIVE-LOCK. 
      delete reservation. 
      FIND FIRST master WHERE master.resnr = reslist.resnr 
        EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE master THEN delete master. 
    END. 
    delete reslist. 
  END. 
  /*RUN del-old-noshow. 
  RUN del-old-cancel.*/
  RUN del-old-resline. /*FT del res-line no-show, cancel n delete*/
  RUN del-mal-mainres. 
  PAUSE 0. 
END. 

PROCEDURE del-old-resline: 
DEFINE VARIABLE anz         AS INTEGER. 
DEFINE VARIABLE anz1        AS INTEGER. 
DEFINE VARIABLE delete-it   AS LOGICAL. 

  FIND FIRST htparam WHERE paramnr = 260 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
 
  /*MTmess-str = translateExtended ("Deleted old no-shows",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST res-line WHERE (res-line.resstatus = 10 OR res-line.resstatus = 9 OR res-line.resstatus = 99)
    AND res-line.active-flag = 2 
    AND res-line.ankunft LT (ci-date - anz) NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 

    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK NO-ERROR.
    delete-it = NOT (AVAILABLE reservation AND reservation.zahldatum NE ?).
 
    IF delete-it THEN 
    DO: 
      IF res-line.resstatus = 10 THEN
        j = j + 1. 
      IF res-line.resstatus = 9 THEN
        k = k + 1. 
      /*MTmess-str = translateExtended ("Deleted old no-shows",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND FIRST reslist WHERE reslist.resnr = res-line.resnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reslist THEN 
      DO: 
        CREATE reslist. 
        reslist.resnr = res-line.resnr. 
      END. 
      DO TRANSACTION: 
        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
          AND fixleist.reslinnr = res-line.reslinnr: 
            delete fixleist. 
        END. 
        FOR EACH reslin-queasy WHERE key = "fargt-line" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FOR EACH reslin-queasy WHERE key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FOR EACH reslin-queasy WHERE key = "ResChanges" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FIND CURRENT res-line EXCLUSIVE-LOCK. 
        delete res-line. 
      END. 
    END. 
    FIND NEXT res-line WHERE (res-line.resstatus = 10 OR res-line.resstatus = 9 OR res-line.resstatus = 99)
      AND res-line.active-flag = 2 
      AND res-line.ankunft LT (ci-date - anz) NO-LOCK NO-ERROR. 
  END. 
  FOR EACH reslist: 
    FIND FIRST res-line WHERE res-line.resnr = reslist.resnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN 
    DO: 
      FIND FIRST reservation WHERE reservation.resnr = reslist.resnr 
        EXCLUSIVE-LOCK. 
      delete reservation. 
    END. 
    delete reslist. 
  END. 
END. 


/*PROCEDURE del-old-noshow: 
DEFINE VARIABLE anz         AS INTEGER. 
DEFINE VARIABLE anz1        AS INTEGER. 
DEFINE VARIABLE delete-it   AS LOGICAL. 

  FIND FIRST htparam WHERE paramnr = 260 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
 
  /*MTmess-str = translateExtended ("Deleted old no-shows",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST res-line WHERE res-line.resstatus = 10 
    AND res-line.active-flag = 2 
    AND res-line.ankunft LT (ci-date - anz) NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 

    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK NO-ERROR.
    delete-it = NOT (AVAILABLE reservation AND reservation.zahldatum NE ?).
 
    IF delete-it THEN 
    DO: 
      j = j + 1. 
      /*MTmess-str = translateExtended ("Deleted old no-shows",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND FIRST reslist WHERE reslist.resnr = res-line.resnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reslist THEN 
      DO: 
        CREATE reslist. 
        reslist.resnr = res-line.resnr. 
      END. 
      DO TRANSACTION: 
        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
          AND fixleist.reslinnr = res-line.reslinnr: 
            delete fixleist. 
        END. 
        FOR EACH reslin-queasy WHERE key = "fargt-line" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FOR EACH reslin-queasy WHERE key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FOR EACH reslin-queasy WHERE key = "ResChanges" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FIND CURRENT res-line EXCLUSIVE-LOCK. 
        delete res-line. 
      END. 
    END. 
    FIND NEXT res-line WHERE res-line.resstatus = 10 
      AND res-line.active-flag = 2 
      AND res-line.ankunft LT (ci-date - anz) NO-LOCK NO-ERROR. 
  END. 
  FOR EACH reslist: 
    FIND FIRST res-line WHERE res-line.resnr = reslist.resnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN 
    DO: 
      FIND FIRST reservation WHERE reservation.resnr = reslist.resnr 
        EXCLUSIVE-LOCK. 
      delete reservation. 
    END. 
    delete reslist. 
  END. 
END. 
 
PROCEDURE del-old-cancel: 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE anz1 AS INTEGER. 
DEFINE VARIABLE delete-it AS LOGICAL. 
 
  FIND FIRST htparam WHERE paramnr = 260 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
 
  /*MTmess-str = translateExtended ("Deleted old cancelled",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST res-line WHERE res-line.resstatus = 9 
    AND res-line.active-flag = 2 
    AND res-line.cancelled LT (ci-date - anz) NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
      NO-LOCK NO-ERROR.
    delete-it = NOT (AVAILABLE reservation AND reservation.zahldatum NE ?). 
 
    IF delete-it THEN 
    DO: 
      k = k + 1. 
      /*MTmess-str = translateExtended ("Deleted old cancelled",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND FIRST reslist WHERE reslist.resnr = res-line.resnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reslist THEN 
      DO: 
        CREATE reslist. 
        reslist.resnr = res-line.resnr. 
      END. 
      DO TRANSACTION: 
        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
          AND fixleist.reslinnr = res-line.reslinnr: 
            delete fixleist. 
        END. 
        FOR EACH reslin-queasy WHERE key = "fargt-line" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FOR EACH reslin-queasy WHERE key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FOR EACH reslin-queasy WHERE key = "ResChanges" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr: 
            delete reslin-queasy. 
        END. 
        FIND CURRENT res-line EXCLUSIVE-LOCK. 
        delete res-line. 
      END. 
    END. 
    FIND NEXT res-line WHERE res-line.resstatus = 9 
    AND res-line.active-flag = 2 
    AND res-line.cancelled LT (ci-date - anz) NO-LOCK NO-ERROR. 
  END. 
  FOR EACH reslist: 
    FIND FIRST res-line WHERE res-line.resnr = reslist.resnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN 
    DO: 
      FIND FIRST reservation WHERE reservation.resnr = reslist.resnr 
        EXCLUSIVE-LOCK. 
      delete reservation. 
    END. 
    delete reslist. 
  END. 
END. */
 
PROCEDURE del-mal-mainres: 

  FIND FIRST reservation WHERE activeflag = 0 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE reservation: 
    FIND FIRST res-line WHERE res-line.resnr = reservation.resnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN 
    DO TRANSACTION: 
      FIND CURRENT reservation EXCLUSIVE-LOCK. 
      delete reservation. 
    END. 
    FIND NEXT reservation WHERE activeflag = 0 NO-LOCK NO-ERROR. 
  END. 
 
  FIND FIRST reservation WHERE activeflag = 1 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE reservation: 
    FIND FIRST res-line WHERE res-line.resnr = reservation.resnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN 
    DO TRANSACTION: 
      FIND CURRENT reservation EXCLUSIVE-LOCK. 
      delete reservation. 
    END. 
    FIND NEXT reservation WHERE activeflag = 1 NO-LOCK NO-ERROR. 
  END. 
END. 
