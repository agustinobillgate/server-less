DEF INPUT PARAMETER t-refno     AS CHAR.
DEF INPUT PARAMETER t-bezeich   AS CHAR.
DEF INPUT PARAMETER t-recid     AS INT.

FIND FIRST gl-jouhdr WHERE RECID(gl-jouhdr) = t-recid.

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
