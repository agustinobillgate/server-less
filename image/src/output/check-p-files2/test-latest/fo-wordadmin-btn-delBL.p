
DEF INPUT PARAMETER briefnr AS INT.
DEF INPUT PARAMETER int1    AS INT.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST briefzei WHERE briefzei.briefnr = briefnr 
    AND briefzei.briefzeilnr = 1 EXCLUSIVE-LOCK NO-ERROR. 
IF AVAILABLE briefzei THEN delete briefzei.

FIND FIRST brief WHERE brief.briefnr = int1 EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE brief THEN delete brief.

success-flag = YES.
