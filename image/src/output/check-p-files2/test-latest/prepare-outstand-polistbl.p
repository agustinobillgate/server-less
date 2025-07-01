DEFINE INPUT PARAMETER user-init        AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER show-price      AS LOG  NO-UNDO.
/****************************************************************************/

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
