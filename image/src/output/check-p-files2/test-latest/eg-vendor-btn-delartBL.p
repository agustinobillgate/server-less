
DEF INPUT PARAMETER vendor-vendor-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egperform FOR eg-vperform. /*Alder - Serverless - Issue 799*/ /*egPerform -> egperform*/
    
FIND FIRST egperform WHERE egperform.vendor-nr = vendor-vendor-nr NO-LOCK NO-ERROR.
IF AVAILABLE egperform THEN
DO:
    fl-code = 1.
    /*MTHIDE MESSAGE NO-PAUSE.  
    MESSAGE translateExtended ("Vendor has been used by other program.",lvCAREA,"")   
        SKIP
        translateExtended ("Deleting not posibble.",lvCAREA,"")   
    VIEW-AS ALERT-BOX INFORMATION.*/
    RETURN NO-APPLY.  
END.

/*Alder - Serverless - Issue 799 - Start*/
FIND FIRST eg-vendor WHERE RECID(eg-vendor) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE eg-vendor THEN
DO:
    FIND CURRENT eg-vendor EXCLUSIVE-LOCK.  
    DELETE eg-vendor.  
    RELEASE eg-vendor.
END.
/*Alder - Serverless - Issue 799 - End*/

/*MTOPEN QUERY q1 FOR EACH eg-vendor NO-LOCK BY eg-vendor.vendor-nr.
answer = NO.  
RUN init-vendor.*/
