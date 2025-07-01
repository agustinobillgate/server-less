DEFINE TEMP-TABLE out-list
    FIELD fibu              AS CHARACTER
    FIELD fibu-desc         AS CHARACTER
    FIELD costcenter-no     AS INTEGER
    FIELD costcenter-name   AS CHARACTER
    .

DEFINE INPUT PARAMETER account-no AS CHARACTER.
DEFINE OUTPUT PARAMETER vSuccess  AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER result-msg AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR out-list.

DEFINE VARIABLE varcode AS CHARACTER.

FOR EACH out-list:
    DELETE out-list.
END.

FIND FIRST parameters WHERE parameters.progname EQ "CostCenter" 
    AND parameters.section EQ "Alloc" 
    AND parameters.varname GT ""
    AND parameters.vstring EQ account-no NO-LOCK NO-ERROR.
IF NOT AVAILABLE parameters THEN
DO:
    result-msg = "Account Number not found.".
    RETURN.
END.

varcode = parameters.varname.
CREATE out-list.
out-list.fibu = parameters.vstring.

FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ parameters.vstring NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN out-list.fibu-desc = gl-acct.bezeich.

FIND FIRST parameters WHERE parameters.progname EQ "CostCenter" 
    AND parameters.section EQ "Name" 
    AND parameters.varname EQ varcode NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN
DO:
    ASSIGN
        out-list.costcenter-no      = INTEGER(parameters.varname)
        out-list.costcenter-name    = parameters.vstring
        .
END.

FIND FIRST out-list NO-LOCK NO-ERROR.
IF AVAILABLE out-list THEN
DO:
    result-msg = "Account found in Cost Center Code: " + STRING(out-list.costcenter-no)
        + CHR(10) + out-list.fibu + " - " + out-list.fibu-desc.
    vSuccess = YES.
END.
