
DEF INPUT  PARAMETER user-init  AS CHAR.
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
