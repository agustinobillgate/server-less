
DEF INPUT PARAMETER location-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

DEF BUFFER egReq FOR eg-property.
DEF BUFFER egPro FOR eg-request.

FIND FIRST egReq WHERE egReq.location = location-nr NO-LOCK NO-ERROR.
FIND FIRST egPro WHERE egPro.location = location-nr  NO-LOCK NO-ERROR.

IF AVAILABLE egReq OR AVAILABLE egPro THEN
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

FIND FIRST eg-location WHERE RECID(eg-location) = rec-id.
FIND CURRENT eg-location EXCLUSIVE-LOCK.  
DELETE eg-location.  
RELEASE eg-location.
