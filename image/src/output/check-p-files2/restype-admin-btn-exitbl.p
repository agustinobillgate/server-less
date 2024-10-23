
DEF TEMP-TABLE p-list LIKE sourccod.

DEF INPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER case-type     AS INT.
DEF INPUT PARAMETER active-flag   AS LOGICAL.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST p-list.
IF case-type = 1 THEN   /* add */
DO:
    CREATE sourccod.
    RUN fill-new-sourccod.
    success-flag = YES.
END.
ELSE IF case-type = 2 THEN   /* chg */
DO:
    FIND FIRST sourccod WHERE sourccod.source-code = p-list.source-code
        EXCLUSIVE-LOCK.
    IF AVAILABLE sourccod THEN RUN fill-new-sourccod.
    success-flag = YES.
END.



PROCEDURE fill-new-sourccod:
  ASSIGN
    sourccod.source-code = p-list.source-code
    sourccod.bemerk      = p-list.bemerk
    sourccod.bezeich     = p-list.bezeich
    sourccod.betriebsnr  = INTEGER(NOT active-flag)
  .
  RELEASE sourccod. 
END. 

