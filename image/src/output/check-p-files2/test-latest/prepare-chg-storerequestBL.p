
DEF INPUT  PARAMETER user-init  AS CHAR.
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER req-flag   AS LOGICAL.
DEF OUTPUT PARAMETER p-220      AS INT.

FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN show-price = htparam.flogical. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. 
IF AVAILABLE bediener THEN /*FT serverless*/
DO:
  IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
END.

FIND FIRST htparam WHERE paramnr = 475 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN req-flag = NOT htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 220 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN p-220 = htparam.finteger.
