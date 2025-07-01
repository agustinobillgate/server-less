
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER nr AS INT.

FIND FIRST eg-property WHERE eg-property.nr = nr.
IF case-type = 1 THEN
DO:
    FIND CURRENT eg-property EXCLUSIVE-LOCK.  
    ASSIGN eg-property.activeflag = NO.
    RELEASE eg-property.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND CURRENT eg-property EXCLUSIVE-LOCK.  
    DELETE eg-property.
END.
