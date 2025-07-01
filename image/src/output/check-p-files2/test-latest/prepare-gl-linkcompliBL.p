DEF TEMP-TABLE gl-jouhdr-list
    FIELD refno LIKE gl-jouhdr.refno.

DEF OUTPUT PARAMETER f-int           AS INTEGER.
DEF OUTPUT PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER foreign-nr      AS INTEGER.
DEF OUTPUT PARAMETER exchg-rate      AS DECIMAL.
DEF OUTPUT PARAMETER last-acctdate   AS DATE.
DEF OUTPUT PARAMETER acct-date       AS DATE.
DEF OUTPUT PARAMETER close-year      AS DATE.
DEF OUTPUT PARAMETER TABLE FOR gl-jouhdr-list.

FIND FIRST htparam WHERE htparam.paramnr = 1012 NO-LOCK.
IF htparam.paramgr = 38 AND htparam.feldtyp = 1 AND htparam.finteger GT 0 THEN
    f-int = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency flag */ 
double-currency = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    foreign-nr = waehrung.waehrungsnr. 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE exchg-rate = 1. 
END. 

FIND FIRST htparam WHERE paramnr = 1123 no-lock.   /* LAST Transfer DATE */ 
last-acctdate = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* CURRENT Accounting Period */ 
acct-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 795 NO-LOCK. 
close-year = htparam.fdate. 

FOR EACH gl-jouhdr WHERE gl-jouhdr.jtype = 3:
    CREATE gl-jouhdr-list.
    ASSIGN gl-jouhdr-list.refno = gl-jouhdr.refno.
END.
