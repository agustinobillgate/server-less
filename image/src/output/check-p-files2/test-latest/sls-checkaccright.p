DEFINE INPUT PARAMETER gastNo           AS INTEGER.
DEFINE OUTPUT PARAMETER restriction     AS LOGICAL INITIAL NO NO-UNDO.

DEFINE VARIABLE        gcf-restrict     AS LOGICAL NO-UNDO.
DEFINE NEW SHARED VARIABLE user-init        AS CHAR FORMAT "x(2)". 

FIND FIRST htparam WHERE htparam.paramnr = 1202 NO-LOCK.
gcf-restrict = htparam.flogical.

IF NOT gcf-restrict THEN RETURN.
    
FIND FIRST guest WHERE guest.gastnr = gastNo NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest THEN RETURN.

IF guest.phonetik3 = user-init OR guest.phonetik3 = "" THEN RETURN.
ELSE
DO:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
    IF SUBSTR(bediener.permission,32,1) LT "2" THEN restriction = YES.
END.
