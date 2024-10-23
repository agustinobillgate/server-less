DEFINE TEMP-TABLE g-list LIKE gl-department.

DEFINE INPUT  PARAMETER TABLE FOR g-list.
DEFINE INPUT  PARAMETER case-type AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST g-list.
IF case-type = 1 THEN   /* add */
DO :
    CREATE gl-department.
    RUN fill-gl-department.
    RELEASE gl-department.
    success-flag = YES.
END.
ELSE IF case-type = 2 THEN   /* chg */
DO:
    FIND FIRST gl-department WHERE gl-department.nr = g-list.nr EXCLUSIVE-LOCK.
    IF AVAILABLE gl-department THEN RUN fill-gl-department.
    FIND CURRENT gl-department.
    RELEASE gl-department.
    success-flag = YES.
END.



PROCEDURE fill-gl-department:
  ASSIGN
    gl-department.nr      = g-list.nr
    gl-department.bezeich = g-list.bezeich
    gl-department.fodept  = g-list.fodept.
END.
