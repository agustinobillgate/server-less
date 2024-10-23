
DEF INPUT PARAMETER bill-gastnr AS INT.
DEF OUTPUT PARAMETER klimit AS DECIMAL.

FIND FIRST vhp.htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
FIND FIRST vhp.guest WHERE vhp.guest.gastnr = bill-gastnr NO-LOCK. 
IF vhp.guest.kreditlimit NE 0 THEN klimit = vhp.guest.kreditlimit. 
ELSE 
DO: 
    IF vhp.htparam.fdecimal NE 0 THEN klimit = vhp.htparam.fdecimal. 
    ELSE klimit = vhp.htparam.finteger. 
END.
