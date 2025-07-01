
DEFINE INPUT PARAMETER case-type AS INTEGER.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

IF case-type = 1 THEN RUN del-interface.
ELSE RUN CRM-checkout.


PROCEDURE del-interface:
DEF BUFFER interf FOR interface. 
DEF BUFFER qsy FOR queasy. 
  FIND FIRST interface WHERE interface.key GE 0 
    AND interface.intdate LE (ci-date - 2) 
    AND interface.int-time GE 0 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE interface: 
      DO TRANSACTION: 
        FIND FIRST interf WHERE RECID(interf) = RECID(interface) 
          EXCLUSIVE-LOCK. 
        DELETE interf.
        RELEASE interf.
      END. 
      FIND NEXT interface WHERE interface.key GE 0 
          AND interface.intdate LE (ci-date - 2) 
          AND interface.int-time GE 0 NO-LOCK NO-ERROR. 
  END. 
 
  FIND FIRST queasy WHERE queasy.key = 35
    AND queasy.date1 LE (ci-date - 2)  NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE queasy: 
      DO TRANSACTION: 
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) 
          EXCLUSIVE-LOCK. 
        DELETE qsy.
        RELEASE qsy.
      END. 
      FIND NEXT queasy WHERE queasy.key = 35  
        AND queasy.date1 LE (ci-date - 2) NO-LOCK NO-ERROR. 
  END. 

  FIND FIRST queasy WHERE queasy.key = 30 AND queasy.betriebsnr = 1 
    AND queasy.date1 LE (ci-date - 2)  NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE queasy: 
      DO TRANSACTION: 
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) 
          EXCLUSIVE-LOCK. 
        DELETE qsy.
        RELEASE qsy.
      END. 
      FIND NEXT queasy WHERE queasy.key = 30 AND queasy.betriebsnr = 1 
          AND queasy.date1 LE (ci-date - 2) NO-LOCK NO-ERROR. 
  END. 
 
  FIND FIRST queasy WHERE queasy.key = 30 AND queasy.betriebsnr = 2 
    AND queasy.date1 LE (ci-date - 2)  NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE queasy: 
      DO TRANSACTION: 
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) 
          EXCLUSIVE-LOCK. 
        DELETE qsy. 
        RELEASE qsy.
      END. 
      FIND NEXT queasy WHERE queasy.key = 30 AND queasy.betriebsnr = 2 
          AND queasy.date1 LE (ci-date - 2) NO-LOCK NO-ERROR. 
  END.

/* SY Micros - PMS IF */
  FIND FIRST queasy WHERE queasy.key = 37 AND queasy.betriebsnr = 1 
    AND queasy.date1 LE (ci-date - 2)  NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE queasy: 
      DO TRANSACTION: 
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) 
          EXCLUSIVE-LOCK. 
        DELETE qsy.
        RELEASE qsy.
      END. 
      FIND NEXT queasy WHERE queasy.key = 37 AND queasy.betriebsnr = 1 
          AND queasy.date1 LE (ci-date - 2) NO-LOCK NO-ERROR. 
  END. 
 
  FIND FIRST queasy WHERE queasy.key = 37 AND queasy.betriebsnr = 2 
    AND queasy.date1 LE (ci-date - 2)  NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE queasy: 
      DO TRANSACTION: 
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) 
          EXCLUSIVE-LOCK. 
        DELETE qsy. 
        RELEASE qsy.
      END. 
      FIND NEXT queasy WHERE queasy.key = 37 AND queasy.betriebsnr = 2 
          AND queasy.date1 LE (ci-date - 2) NO-LOCK NO-ERROR. 
  END.

END. 



PROCEDURE CRM-checkout:
DEF VAR bill-date AS DATE NO-UNDO.
  FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
  ASSIGN bill-date = htparam.fdate.
  FOR EACH res-line NO-LOCK WHERE 
      res-line.resstatus = 8            AND 
      res-line.abreise   = bill-date    AND
      res-line.l-zuordnung[3] = 0       AND
      res-line.erwachs GT 0:
      CREATE interface.
      ASSIGN
          interface.key         = 5
          interface.zinr        = res-line.zinr
          interface.nebenstelle = res-line.zinr
          interface.resnr       = res-line.resnr
          interface.reslinnr    = res-line.reslinnr
          interface.intfield    = 0
          interface.int-time    = TIME
          interface.intdate     = TODAY
          interface.parameters  = "CRM check-out"
      .
      FIND CURRENT interface NO-LOCK.
      RELEASE interface.
  END.
END.
