DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER cost-list-rec-id AS INT.
DEF INPUT PARAMETER last-zone AS CHAR.

IF case-type = 1 THEN
DO:
    FIND FIRST parameters WHERE RECID(parameters) EQ cost-list-rec-id NO-LOCK NO-ERROR. 
	IF AVAILABLE parameters THEN 
    DO:
        FIND CURRENT parameters EXCLUSIVE-LOCK.
	    DELETE parameters.
	END.
END.
ELSE IF case-type = 2 THEN
DO:
    FOR EACH parameters WHERE parameters.progname EQ "if-internal" 
        AND parameters.section EQ "zone" 
        AND parameters.varname EQ last-zone EXCLUSIVE-LOCK: 
        DELETE parameters.
    END. 
END.
