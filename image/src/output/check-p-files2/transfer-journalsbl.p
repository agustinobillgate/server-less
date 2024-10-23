
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER depttype AS INT.

RUN transfer-journals.

PROCEDURE transfer-journals:
DEFINE buffer gl-jouhdr1 FOR gl-jouhdr. 
DEFINE VARIABLE date1 AS DATE. 
DEFINE VARIABLE date2 AS DATE. 
  FIND FIRST htparam WHERE paramnr = 558 no-lock.    /* LAST Accounting Period */ 
  date1 = htparam.fdate + 1. 
  FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
  date2 = htparam.fdate. 
  IF from-date GT date1 THEN date1 = from-date. 
  IF to-date LT date2 THEN date2 = to-date. 
  FOR EACH gl-jouhdr1 WHERE gl-jouhdr1.activeflag = 0 
    AND gl-jouhdr1.datum GE date1 AND gl-jouhdr1.datum LE date2 
    AND gl-jouhdr1.jtype = depttype AND gl-jouhdr1.batch = YES: 
    gl-jouhdr1.batch = NO. 
  END. 
END. 
