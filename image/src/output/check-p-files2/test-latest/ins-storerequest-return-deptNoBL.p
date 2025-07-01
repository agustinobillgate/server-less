
DEF INPUT  PARAMETER deptNo             AS INT.
DEF OUTPUT PARAMETER parameters-vstring AS CHAR.
DEF OUTPUT PARAMETER avail-parameters   AS LOGICAL INIT NO.

FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
  AND parameters.section = "Name" AND INTEGER(parameters.varname) = deptNo 
  NO-LOCK NO-ERROR. 
IF AVAILABLE parameters THEN 
    ASSIGN
    avail-parameters  = YES
    parameters-vstring = parameters.vstring.
