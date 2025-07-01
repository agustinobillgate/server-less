
DEF INPUT        PARAMETER dept     AS INT.
DEF INPUT-OUTPUT PARAMETER deptNo   AS INT.
DEF INPUT-OUTPUT PARAMETER deptname AS CHAR.
DEF       OUTPUT PARAMETER flag     AS INT INIT 0.

FIND FIRST parameters WHERE parameters.progname = "CostCenter"
    AND parameters.section = "Name" AND INTEGER(parameters.varname) = deptNo 
    NO-LOCK NO-ERROR. 
IF AVAILABLE parameters THEN 
DO: 
    deptname = parameters.vstring. 
    flag = 1.
END. 
ELSE 
DO: 
    deptNo = dept. 
    flag = 2.
END.
