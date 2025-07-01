DEF INPUT PARAMETER t-refno     AS CHAR.
DEF INPUT PARAMETER t-bezeich   AS CHAR.
DEF INPUT PARAMETER t-recid     AS INT.
DEF INPUT PARAMETER user-init   AS CHAR.    /*naufal - add parameter for logfile*/

DEF VAR refno   LIKE gl-jouhdr.refno.       /*naufal - add variable for logfile*/            
DEF VAR bez     LIKE gl-jouhdr.bezeich.     /*naufal - add variable for logfile*/        
DEF VAR datum   LIKE gl-jouhdr.datum.       /*naufal - add variable for logfile*/

FIND FIRST gl-jouhdr WHERE RECID(gl-jouhdr) = t-recid.
/*naufal - assign variable for logfile*/
ASSIGN
    refno = gl-jouhdr.refno
    bez   = gl-jouhdr.bezeich
    datum = gl-jouhdr.datum.
/*end*/
IF t-refno NE "" THEN 
DO: 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    ASSIGN gl-jouhdr.refno = t-refno. 
    FIND CURRENT gl-jouhdr NO-LOCK. 
END. 
IF t-bezeich NE "" THEN 
DO: 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    ASSIGN gl-jouhdr.bezeich = t-bezeich. 
    FIND CURRENT gl-jouhdr NO-LOCK. 
END.
/*naufal - validation log file*/
IF gl-jouhdr.refno NE refno THEN
DO:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Modify Journal, Date: " + STRING(datum) + ", RefNo From: " + refno + " To: " + gl-jouhdr.refno
            res-history.action      = "G/L".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END.

IF gl-jouhdr.bezeich NE bez THEN
DO:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Modify Journal, Date: " + STRING(datum) + ", Desc From: " + bez + " To: " + gl-jouhdr.bezeich
            res-history.action      = "G/L".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END.
/*end*/
