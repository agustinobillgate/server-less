DEFINE INPUT PARAMETER location-nr AS INTEGER.
DEFINE INPUT PARAMETER rec-id AS INTEGER.
DEFINE OUTPUT PARAMETER err-code AS INTEGER INITIAL 0.

DEFINE BUFFER eg-pro FOR eg-property.
DEFINE BUFFER eg-req FOR eg-request.

FIND FIRST eg-req WHERE eg-req.location = location-nr NO-LOCK NO-ERROR.
FIND FIRST eg-pro WHERE eg-pro.location = location-nr  NO-LOCK NO-ERROR.
IF AVAILABLE eg-req OR AVAILABLE eg-pro THEN
DO:
    err-code = 1.
    /*MTHIDE MESSAGE NO-PAUSE.  
    MESSAGE translateExtended ("Object Item/Request exists for this location.",lvCAREA,"")   
        SKIP
        translateExtended ("Deleting not posibble",lvCAREA,"")   
    VIEW-AS ALERT-BOX INFORMATION.  

    SELECTED = YES.

    APPLY "entry" TO b1.*/
    RETURN NO-APPLY.  
END.

/*Alder - Serverless - Issue 775 - Start*/
FIND FIRST eg-location WHERE RECID(eg-location) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE eg-location THEN
DO:
    FIND CURRENT eg-location EXCLUSIVE-LOCK.  
    DELETE eg-location.  
    RELEASE eg-location.
END.
/*Alder - Serverless - Issue 775 - End*/

