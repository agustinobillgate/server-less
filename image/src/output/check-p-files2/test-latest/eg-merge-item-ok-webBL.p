
DEFINE INPUT PARAMETER item-nr  AS INTEGER.
DEFINE INPUT PARAMETER merge-nr AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag1 AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER success-flag2 AS LOGICAL INIT NO.

DEFINE BUFFER buf-eg-request FOR eg-request.

/*Replace Item at Work Order with Item Merge*/
FOR EACH eg-request NO-LOCK: 
    FIND FIRST buf-eg-request WHERE buf-eg-request.reqnr = eg-request.reqnr
        AND buf-eg-request.propertynr = item-nr NO-LOCK NO-ERROR.
    IF AVAILABLE buf-eg-request THEN
    DO:
        FIND CURRENT buf-eg-request EXCLUSIVE-LOCK. 
        buf-eg-request.propertynr = merge-nr.
        FIND CURRENT buf-eg-request NO-LOCK.
        RELEASE buf-eg-request.
        success-flag1 = YES.
    END.        
END.

/*Delete Selected Merge Item*/
FIND FIRST eg-property WHERE eg-property.nr = item-nr NO-LOCK NO-ERROR.
IF AVAILABLE eg-property THEN
DO:
    FIND CURRENT eg-property EXCLUSIVE-LOCK.  
    DELETE eg-property.  
    RELEASE eg-property.
    success-flag2 = YES.
END.

