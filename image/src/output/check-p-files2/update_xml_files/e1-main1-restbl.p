DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER pos-dept AS INT.
DEF INPUT PARAMETER bediener-username AS CHAR.
DEF OUTPUT PARAMETER do-it AS LOGICAL INIT NO.

FIND FIRST hoteldpt WHERE hoteldpt.num = pos-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN
DO :
    FIND FIRST kellner WHERE STRING(kellner.kellner-nr,"99") = user-init 
      AND kellner.departement = pos-dept NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE kellner THEN 
    FIND FIRST kellner WHERE kellner.kellnername = bediener-username 
      AND kellner.departement = pos-dept NO-LOCK NO-ERROR. 
    IF AVAILABLE kellner THEN 
    DO: 
        do-it = YES.
    END.
END.
