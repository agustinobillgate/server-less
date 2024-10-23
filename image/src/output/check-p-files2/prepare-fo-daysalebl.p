DEFINE TEMP-TABLE bline-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD userinit LIKE bediener.userinit 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD name LIKE bediener.username 
  FIELD bl-recid AS INTEGER INITIAL 0. 

DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.
DEF OUTPUT PARAMETER curr-local AS CHAR.
DEF OUTPUT PARAMETER curr-foreign AS CHAR.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER h-art-coupon AS INT.
DEF OUTPUT PARAMETER p-240 AS LOGICAL.
DEF OUTPUT PARAMETER p-110 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR bline-list.

DEFINE BUFFER usr1 FOR bediener.
find first htparam where htparam.paramnr = 144 no-lock. 
find first waehrung where waehrung.wabkurz = htparam.fchar no-lock no-error. 
if available waehrung then exchg-rate = waehrung.ankauf / 
waehrung.einheit. 
else exchg-rate = 1. 
 
find first htparam where paramnr = 152 no-lock. 
curr-local = fchar. 
find first htparam where paramnr = 144 no-lock. 
curr-foreign = fchar. 
find first htparam where paramnr = 110 no-lock.  /*Invoicing Date */ 
from-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 1001 NO-LOCK.
h-art-coupon = htparam.finteger.


FOR EACH usr1 WHERE usr1.username NE "" NO-LOCK BY usr1.username: 
    create bline-list. 
    bline-list.userinit = usr1.userinit. 
    bline-list.name = usr1.username. 
    bline-list.bl-recid = RECID(usr1). 
    bline-list.SELECTED = YES.
    IF SUBSTR(usr1.perm,8,1) GE "2" THEN bline-list.flag = 1. 
END. 

RUN htplogic.p(240, OUTPUT p-240).
RUN htpdate.p (110, OUTPUT p-110).
