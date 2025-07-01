DEFINE TEMP-TABLE gl-jouhdr-list
    FIELD refno LIKE gl-jouhdr.refno.

DEF OUTPUT PARAMETER f-int          AS INTEGER.
DEF OUTPUT PARAMETER last-acctdate  AS DATE.
DEF OUTPUT PARAMETER acct-date      AS DATE.
DEF OUTPUT PARAMETER close-year     AS DATE.
DEF OUTPUT PARAMETER msg-str        AS CHARACTER.
DEF OUTPUT PARAMETER TABLE FOR gl-jouhdr-list.

DEFINE VARIABLE last-acct-period AS DATE.
DEFINE VARIABLE tmpDate AS DATE.

FIND FIRST htparam WHERE htparam.paramnr = 1012 NO-LOCK.
IF htparam.paramgr = 38 AND htparam.feldtyp = 1 AND htparam.finteger GT 0 THEN
    f-int = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 1118 no-lock.    /* LAST A/P Transfer DATE */ 
last-acctdate = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* CURRENT Accounting Period */ 
acct-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 795 NO-LOCK. 
close-year = htparam.fdate.

FOR EACH gl-jouhdr WHERE gl-jouhdr.jtype = 4 NO-LOCK :
    CREATE gl-jouhdr-list.
    ASSIGN gl-jouhdr-list.refno = gl-jouhdr.refno.
END.

FIND FIRST htparam WHERE paramnr = 558 no-lock.   /* LAST Accounting Period */ 
last-acct-period = htparam.fdate.

ASSIGN
    tmpDate = last-acctdate + 1.

/*FDL Dec 22, 2023 => Ticket 221A85*/
/*IF (last-acctdate + 1) LE last-acct-period THEN FT serverless */
IF tmpDate LE last-acct-period THEN
DO:
    msg-str = "Last AP transfer to GL (Param 1118) lower then last accounting closing period (Param 558)."
        + CHR(10)    
        + "Transfer to GL not possible."
        .
    RETURN.
END.
