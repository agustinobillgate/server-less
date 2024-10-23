DEF TEMP-TABLE t-master LIKE master.
DEF INPUT PARAMETER  resnr      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  gastnr     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  invno-flag AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER  user-init  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER gastnrpay  AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-master.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

RUN create-master.

PROCEDURE create-master:

  CREATE master. 
  ASSIGN
    master.resnr        = resnr
    master.gastnr       = gastnr 
    master.gastnrpay    = gastnr 
    master.active       = YES
    master.rechnrstart  = 1 
    master.rechnrend    = 1
    master.umsatzart[1] = YES 
    master.umsatzart[2] = YES
    gastnrpay           = gastnr. 
  . 
  IF invno-flag THEN 
  DO: 
    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
    counters.counter = counters.counter + 1. 
    FIND CURRENT counters NO-LOCK. 
    ASSIGN master.rechnr = counters.counter.
  END. 
    
  FIND CURRENT master.
  CREATE t-master.
  BUFFER-COPY master TO t-master.

  CREATE res-history. 
  ASSIGN 
    res-history.nr = bediener.nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME
    res-history.action = "MASTER BILL"
    res-history.aenderung = "Create Master Bill, ResNo = " + STRING(resnr)
      + " Master BillNo = " + STRING(master.rechnr)
  .
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history. 

END.
