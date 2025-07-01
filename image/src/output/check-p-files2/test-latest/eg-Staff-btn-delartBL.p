
DEF BUFFER egmain FOR eg-maintain. /*Alder - Serverless - Issue 800*/ /*egMain -> egmain*/
DEF BUFFER egreq  FOR eg-request.

DEF INPUT PARAMETER staff-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST egmain WHERE /*egmain.KEY = 2 AND*/ egmain.pic = staff-nr AND egmain.TYPE NE 3 NO-LOCK NO-ERROR.
FIND FIRST egreq WHERE egreq.assign-to = staff-nr AND egreq.reqstatus NE 5 NO-LOCK NO-ERROR.

IF AVAILABLE egmain OR AVAILABLE egreq THEN
DO:
    fl-code = 1.
    /*MTHIDE MESSAGE NO-PAUSE.  
    MESSAGE translateExtended ("Work exists for this Person in Charge.",lvCAREA,"")   
        SKIP
        translateExtended ("Deleting not posibble",lvCAREA,"")   
    VIEW-AS ALERT-BOX INFORMATION.  
    APPLY "entry" TO b1.*/
    RETURN NO-APPLY.  
END.

/*Alder - Serverless - Issue 800 - Start*/
FIND FIRST eg-staff WHERE RECID(eg-staff) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE eg-staff THEN
DO:
    FIND CURRENT eg-staff EXCLUSIVE-LOCK. 
    ASSIGN eg-staff.activeflag = NO.
    /*DELETE eg-staff.  */
    FIND CURRENT eg-staff NO-LOCK.
    RELEASE eg-staff.
    fl-code = 2.
END.
/*Alder - Serverless - Issue 800* - End*/

   /*MTOPEN QUERY q1 FOR EACH eg-staff NO-LOCK, 
    FIRST dept WHERE dept.dept-nr = eg-staff.usergroup NO-LOCK
    /*, FIRST Vuser WHERE Vuser.usr-nr = eg-staff.vhpuser NO-LOCK*/
    BY eg-staff.nr.

/*b1:REFRESH().*/

answer = NO.  
RUN init-staff. */
