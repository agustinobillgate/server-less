
DEF INPUT  PARAMETER bill-gastnr AS INT.
DEF OUTPUT PARAMETER kreditlimit AS DECIMAL.

FIND FIRST guest WHERE guest.gastnr = bill-gastnr NO-LOCK. 

IF guest.kreditlimit NE 0 THEN kreditlimit = guest.kreditlimit. 
ELSE 
DO: 
  FIND FIRST htparam WHERE paramnr = 68 NO-LOCK. 
  IF htparam.fdecimal NE 0 THEN kreditlimit = htparam.fdecimal. 
  ELSE kreditlimit = htparam.finteger. 
END. 
