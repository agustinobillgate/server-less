
DEF INPUT PARAMETER paramno AS INT.
DEF INPUT PARAMETER bezeich AS CHAR.
DEF INPUT PARAMETER fdecimal AS DECIMAL.
DEF INPUT PARAMETER fchar AS CHAR.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST htparam WHERE htparam.paramnr = paramno EXCLUSIVE-LOCK.
IF AVAILABLE htparam THEN
DO:
    ASSIGN 
        htparam.bezeich = bezeich
        htparam.fdecimal = fdecimal
        htparam.fchar = fchar
        .
    success-flag = YES.
    RELEASE htparam.
END.

