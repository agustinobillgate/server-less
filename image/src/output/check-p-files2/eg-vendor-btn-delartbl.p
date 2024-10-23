
DEF INPUT PARAMETER vendor-vendor-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egPerform FOR eg-vperform.
    
FIND FIRST egPerform WHERE egperform.vendor-nr = vendor-vendor-nr NO-LOCK NO-ERROR.
IF AVAILABLE egPerform THEN
DO:
    fl-code = 1.
    /*MTHIDE MESSAGE NO-PAUSE.  
    MESSAGE translateExtended ("Vendor has been used by other program.",lvCAREA,"")   
        SKIP
        translateExtended ("Deleting not posibble.",lvCAREA,"")   
    VIEW-AS ALERT-BOX INFORMATION.*/
    RETURN NO-APPLY.  
END.
FIND FIRST eg-vendor WHERE RECID(eg-vendor) = rec-id.
FIND CURRENT eg-vendor EXCLUSIVE-LOCK.  
DELETE eg-vendor.  
RELEASE eg-vendor.

/*MTOPEN QUERY q1 FOR EACH eg-vendor NO-LOCK BY eg-vendor.vendor-nr.
answer = NO.  
RUN init-vendor.*/
