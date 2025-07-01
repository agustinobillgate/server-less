
DEF INPUT  PARAMETER inp-rechnr AS INT.
DEF OUTPUT PARAMETER username       AS CHAR.
DEF OUTPUT PARAMETER gremark      AS CHAR.


DEF BUFFER rline FOR res-line. 
DEF BUFFER gbuff FOR guest. 
 
FIND FIRST bill WHERE bill.rechnr = inp-rechnr NO-LOCK. 

FIND FIRST rline WHERE rline.resnr = bill.resnr 
    AND rline.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE rline THEN 
DO:
	FIND FIRST gbuff WHERE gbuff.gastnr EQ rline.gastnrmember NO-LOCK NO-ERROR.
	IF AVAILABLE gbuff THEN
	gremark = gbuff.bemerkung.
	
	FIND FIRST bediener WHERE bediener.userinit EQ rline.changed-id NO-LOCK NO-ERROR.
	IF AVAILABLE bediener THEN
	username = bediener.username.
END.

