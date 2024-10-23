DEF TEMP-TABLE p-list LIKE gc-piacct.

DEF INPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER active-flag AS LOGICAL.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER flag2 AS INT INIT 0.

FIND FIRST p-list NO-LOCK NO-ERROR.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = p-list.fibukonto
    NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN
DO:
  flag = 1.
  IF p-list.bezeich = "" THEN 
  DO:
      flag2 = 1.
      RETURN NO-APPLY.
  END.
END.

IF case-type = 1 THEN
DO:
    CREATE gc-piacct. 
    RUN fill-new-gc-piacct. 
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST gc-piacct WHERE gc-piacct.nr = p-list.nr NO-LOCK NO-ERROR.
    IF AVAILABLE gc-piacct THEN
    DO:
        FIND CURRENT gc-piacct EXCLUSIVE-LOCK.
        ASSIGN
          gc-piacct.fibukonto = p-list.fibukonto
          gc-piacct.bezeich = p-list.bezeich
          gc-piacct.activeflag = INTEGER(NOT active-flag).
        FIND CURRENT gc-piacct NO-LOCK.
        RELEASE gc-piacct.
    END.
END.
PROCEDURE fill-new-gc-piacct:
  ASSIGN
    gc-piacct.nr          = p-list.nr
    gc-piacct.fibukonto   = p-list.fibukonto
    gc-piacct.bezeich     = p-list.bezeich
    gc-piacct.activeflag  = INTEGER(NOT active-flag) 
  . 
  RELEASE gc-piacct. 
END. 
