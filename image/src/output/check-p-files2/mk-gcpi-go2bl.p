DEF INPUT PARAMETER pi-number AS CHAR.
DEF INPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER pbuff-docu-nr2 AS CHAR.
DEF OUTPUT PARAMETER printed2 AS LOGICAL.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = pi-number NO-LOCK NO-ERROR.  /*sis 050613*/
FIND FIRST counters WHERE counters.counter-no = 43 EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE counters THEN
DO:
    CREATE counters.
    ASSIGN
      counters.counter-no = 43
      counters.counter-bez = "GC Proforma Invoice SETTLEMENT Counter No"
    .
END.
ASSIGN counters.counter = counters.counter + 1.
IF counters.counter GT 9999 THEN counters.counter = 1.

FIND CURRENT counters NO-LOCK.
ASSIGN pbuff-docu-nr2 = "IS" + STRING(MONTH(billdate),"99")
                 + STRING(YEAR(billdate),"9999") + "-"
                 + STRING(counters.counter,"9999"). /* Malik Serverless : STRING(counters.counter,"9999") -> STRING(counter.counter,"9999") */

FIND CURRENT gc-pi EXCLUSIVE-LOCK.
ASSIGN gc-pi.docu-nr2 = pbuff-docu-nr2.
FIND CURRENT gc-pi NO-LOCK.
printed2 = gc-pi.printed2.
