
DEF INPUT  PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT PARAMETER nr AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR INIT "".
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fstype-admin".

FIND FIRST gl-acct WHERE gl-acct.fs-type = nr NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct  THEN 
DO: 
 msg-str = msg-str + CHR(2)
         + translateExtended ("Chart of account exists, deleting not possible.",lvCAREA,"").
END. 
ELSE 
DO: 
 FIND FIRST gl-fstype WHERE gl-fstype.nr = nr EXCLUSIVE-LOCK. 
 delete gl-fstype.
 success-flag = YES.
 /*MTOPEN QUERY q1 FOR EACH gl-fstype NO-LOCK BY gl-fstype.nr. 
 IF AVAILABLE gl-fstype THEN 
 DO: 
    selected = YES. 
    RUN fill-g-list. 
    RUN disp-g-list. 
 END. 
 ELSE 
 DO: 
   selected = NO. 
   RUN init-g-list. 
   RUN disp-g-list. 
 END. 
 */
END. 
