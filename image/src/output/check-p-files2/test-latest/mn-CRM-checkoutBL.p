

RUN CRM-checkout.

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
