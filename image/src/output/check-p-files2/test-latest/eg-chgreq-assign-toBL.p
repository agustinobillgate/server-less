
DEF INPUT PARAMETER request1-deptnum AS INT.
DEF INPUT PARAMETER request1-assign-to AS INT.
DEF OUTPUT PARAMETER avail-usr AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER usr-name AS CHAR.

DEF BUFFER usr1 FOR eg-staff.

FIND FIRST usr1 WHERE 
    usr1.usergroup = request1-deptnum AND 
    usr1.activeflag = YES AND usr1.nr = request1-assign-to NO-LOCK NO-ERROR.
IF AVAILABLE usr1 THEN 
DO:
    avail-usr = YES.
    usr-name = usr1.NAME.
END.
    
