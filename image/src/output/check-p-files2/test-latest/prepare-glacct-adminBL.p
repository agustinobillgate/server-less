

DEFINE TEMP-TABLE b1-list LIKE gl-acct
    FIELD main-bezeich   LIKE gl-main.bezeich
    FIELD kurzbez        LIKE gl-fstype.kurzbez
    FIELD dept-bezeich   LIKE gl-department.bezeich
    FIELD fstype-bezeich LIKE gl-fstype.bezeich.

DEF TEMP-TABLE gl-main1 LIKE gl-main.
DEF TEMP-TABLE gl-fstype1 LIKE gl-fstype.
DEF TEMP-TABLE gl-dept1 LIKE gl-department.

DEF OUTPUT PARAMETER from-acct AS CHAR.
DEF OUTPUT PARAMETER gst-flag  AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR b1-list.
DEF OUTPUT PARAMETER TABLE FOR gl-main1.
DEF OUTPUT PARAMETER TABLE FOR gl-fstype1.
DEF OUTPUT PARAMETER TABLE FOR gl-dept1.

FIND FIRST gl-acct WHERE INTEGER(gl-acct.fibukonto) = 0 
  AND gl-acct.bezeich = "" AND gl-acct.main-nr = 0 NO-ERROR. 
IF AVAILABLE gl-acct THEN delete gl-acct. 


FIND FIRST htparam WHERE paramnr = 551 NO-LOCK. 
IF htparam.paramgr = 38 AND htparam.fchar NE "" THEN from-acct = htparam.fchar. 

FOR EACH gl-acct WHERE gl-acct.fibukonto GE from-acct NO-LOCK, 
    FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK, 
    FIRST gl-fstype WHERE gl-fstype.nr = gl-acct.fs-type NO-LOCK, 
    FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK 
    BY gl-acct.fibukonto:
    CREATE b1-list.
    BUFFER-COPY gl-acct TO b1-list.
    ASSIGN
      b1-list.main-bezeich   = gl-main.bezeich
      b1-list.kurzbez        = gl-fstype.kurzbez
      b1-list.dept-bezeich   = gl-department.bezeich
      b1-list.fstype-bezeich = gl-fstype.bezeich.
END.

FOR EACH gl-main:
    CREATE gl-main1.
    BUFFER-COPY gl-main TO gl-main1.
END.
FOR EACH gl-fstype:
    CREATE gl-fstype1.
    BUFFER-COPY gl-fstype TO gl-fstype1.
END.
FOR EACH gl-department:
    CREATE gl-dept1.
    BUFFER-COPY gl-department TO gl-dept1.
END.

/*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.
