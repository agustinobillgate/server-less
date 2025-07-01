
DEFINE TEMP-TABLE p-list LIKE gc-pitype.

DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER active-flag AS LOGICAL.
DEF INPUT PARAMETER TABLE FOR p-list.
DEF OUTPUT PARAMETER return-it    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST p-list.
RUN chek-p-list.
IF return-it THEN RETURN.
IF case-type = 1 THEN   /* add */
DO :
    CREATE gc-pitype. 
    RUN fill-new-gc-pitype. 
    success-flag = YES.
END.
ELSE IF case-type = 2 THEN   /* add */
DO:
    FIND FIRST gc-pitype WHERE gc-pitype.nr = p-list.nr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE gc-pitype THEN
    DO:
        RUN fill-new-gc-pitype.
        success-flag = YES.
    END.
END.


PROCEDURE chek-p-list:
  DEFINE buffer gc-pitype1 FOR gc-pitype. 
  FIND FIRST gc-pitype1 WHERE gc-pitype1.bezeich = p-list.bezeich 
      AND gc-pitype1.nr NE p-list.nr NO-LOCK NO-ERROR. 
  IF AVAILABLE gc-pitype1 AND gc-pitype1.bezeich NE "" THEN 
  DO:
    return-it = YES.
    RETURN.
    /*MTp-list.bezeich = gc-pitype1.bezeich. 
    DISP p-list.bezeich WITH FRAME frame1. 
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Description already exists.",lvCAREA,"") 
      VIEW-AS ALERT-BOX INFORMATION. */
  END.
END.

PROCEDURE fill-new-gc-pitype: 
  ASSIGN
    gc-pitype.nr = p-list.nr
    gc-pitype.bezeich     = p-list.bezeich
    gc-pitype.activeflag  = INTEGER(NOT active-flag) 
  . 
  RELEASE gc-pitype. 
END. 
 
