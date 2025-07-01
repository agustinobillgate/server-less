
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER cost-list-rec-id AS INT.
DEF INPUT PARAMETER last-zone AS CHAR.
DEF INPUT PARAMETER ifname AS CHAR.

IF case-type = 1 THEN
DO:
    FIND FIRST parameters WHERE RECID(parameters) = cost-list-rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE parameters THEN
    DO:
        FIND CURRENT parameters EXCLUSIVE-LOCK.
        DELETE parameters. 
    END.
END.
ELSE IF case-type = 2 THEN
DO:
    FOR EACH parameters WHERE parameters.progname = "interface" 
        AND parameters.section = "zone" AND parameters.varname = last-zone: 
        DELETE parameters. 
    END. 
END.
ELSE IF case-type = 3 THEN
DO:
    FOR EACH parameters WHERE parameters.progname = ifname 
        AND parameters.section = "DCode" AND parameters.varname = last-zone: 
        DELETE parameters. 
    END. 
END.
