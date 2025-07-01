/* Add by Michael @ 28/02/2019 for Sol Beach Benoa request - display by Arrangement */
DEF TEMP-TABLE t-argt
    FIELD CODE  LIKE arrangement.arrangement
    FIELD NAME  LIKE arrangement.argt-bez.
/* End of add */

DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER foreign-nr AS INT. 
DEF OUTPUT PARAMETER f-log AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-argt.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
END. 

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK.
f-log = htparam.flogical.

/* Add by Michael @ 28/02/2019 for Sol Beach Benoa request - display by Arrangement */
FOR EACH arrangement NO-LOCK:
    CREATE t-argt.
    ASSIGN t-argt.CODE = arrangement.arrangement
        t-argt.NAME = arrangement.argt-bez.
END.
/* End of add */

