DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE INPUT PARAMETER pos-dept AS INTEGER.
DEFINE INPUT PARAMETER bediener-username AS CHARACTER.
DEFINE OUTPUT PARAMETER active-waiter AS LOGICAL INITIAL NO.

FIND FIRST hoteldpt WHERE hoteldpt.num = pos-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN
DO:
    FIND FIRST kellner WHERE kellner.kellner-nr = INT(user-init) 
        AND kellner.departement = hoteldpt.num NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE kellner THEN
    DO:
        FIND FIRST kellner WHERE kellner.kellnername = bediener-username 
            AND kellner.departement = hoteldpt.num NO-LOCK NO-ERROR. 
    END.
    
    IF AVAILABLE kellner THEN 
    DO: 
        active-waiter = YES.
        RETURN.
    END.
END.
