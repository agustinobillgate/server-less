
DEF BUFFER egMain FOR eg-maintain /*eg-mdetail*/ .
DEF BUFFER egreq  FOR eg-request.

DEF INPUT PARAMETER staff-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST egMain WHERE /*egmain.KEY = 2 AND*/ egMain.pic = staff-nr AND egmain.TYPE NE 3 NO-LOCK NO-ERROR.
FIND FIRST egreq WHERE egreq.assign-to = staff-nr AND egreq.reqstatus NE 5 NO-LOCK NO-ERROR.

IF AVAILABLE egMain OR AVAILABLE egreq THEN
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

FIND FIRST eg-staff WHERE RECID(eg-staff) = rec-id.
FIND CURRENT eg-staff EXCLUSIVE-LOCK. 
ASSIGN eg-staff.activeflag = NO.
/*DELETE eg-staff.  */
RELEASE eg-staff.
fl-code = 2.


   /*MTOPEN QUERY q1 FOR EACH eg-staff NO-LOCK, 
    FIRST dept WHERE dept.dept-nr = eg-staff.usergroup NO-LOCK
    /*, FIRST Vuser WHERE Vuser.usr-nr = eg-staff.vhpuser NO-LOCK*/
    BY eg-staff.nr.

/*b1:REFRESH().*/

answer = NO.  
RUN init-staff. */
