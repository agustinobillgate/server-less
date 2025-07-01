DEFINE TEMP-TABLE b1-list LIKE gl-jouhdr
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER sorttype   AS INT.
DEF INPUT  PARAMETER from-refno AS CHAR.
DEF INPUT  PARAMETER depttype   AS INT.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF OUTPUT  PARAMETER TABLE FOR b1-list.

RUN display-it.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR):
DEF VAR n AS INTEGER.
DEF VAR s1 AS CHAR.
  n = INDEX(bemerk, ";&&").
  IF n > 0 THEN RETURN SUBSTR(bemerk, 1, n - 1).
  ELSE RETURN bemerk.
END.

PROCEDURE display-it:
DEFINE VARIABLE b-flag AS LOGICAL INITIAL NO.
  IF sorttype = 0 THEN b-flag = YES.
  
  IF from-refno = "" THEN 
  DO:
    IF depttype = 0 THEN 
    FOR EACH gl-jouhdr
        WHERE gl-jouhdr.activeflag = sorttype AND gl-jouhdr.jtype GT 0 
        AND gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date 
        AND gl-jouhdr.batch = b-flag NO-LOCK 
        BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
        RUN assign-b1.
    END.
    ELSE
    FOR EACH gl-jouhdr 
        WHERE gl-jouhdr.activeflag = sorttype 
        AND gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date 
        AND gl-jouhdr.jtype = depttype AND gl-jouhdr.batch = b-flag NO-LOCK 
        BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
        RUN assign-b1.
    END.
 
    IF AVAILABLE gl-jouhdr THEN 
    DO: 
      /*MTdebits = gl-jouhdr.debit.
      credits = gl-jouhdr.credit.
      /*MTDISP debits credits WITH FRAME frame1. */*/
    END. 
  END. 
  ELSE 
  DO: 
    IF depttype = 0 THEN
    FOR EACH gl-jouhdr 
        WHERE gl-jouhdr.activeflag = sorttype AND gl-jouhdr.jtype GT 0 
        AND gl-jouhdr.refno EQ from-refno AND gl-jouhdr.datum GE from-date 
        AND gl-jouhdr.datum LE to-date AND gl-jouhdr.batch = b-flag NO-LOCK 
        BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
        RUN assign-b1.
    END.
    ELSE
    FOR EACH gl-jouhdr 
        WHERE gl-jouhdr.activeflag = sorttype AND gl-jouhdr.batch = b-flag 
        AND gl-jouhdr.refno EQ from-refno AND gl-jouhdr.datum GE from-date 
        AND gl-jouhdr.datum LE to-date AND gl-jouhdr.jtype = depttype 
        AND gl-jouhdr.batch = b-flag NO-LOCK 
        BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
        RUN assign-b1.
    END.
 
    IF AVAILABLE gl-jouhdr THEN 
    DO: 
      /*MTdebits = gl-jouhdr.debit. 
      credits = gl-jouhdr.credit. 
      /*MTDISP debits credits WITH FRAME frame1. */*/
    END. 
  END. 
END. 

PROCEDURE assign-b1:
    CREATE b1-list.
    BUFFER-COPY gl-jouhdr TO b1-list.
    b1-list.rec-id = RECID(gl-jouhdr).
END.
