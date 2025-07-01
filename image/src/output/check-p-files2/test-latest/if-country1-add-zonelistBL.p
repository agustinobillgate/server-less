
DEF INPUT PARAMETER ifname AS CHAR.
DEF INPUT PARAMETER cost-list-zone AS CHAR.
DEF INPUT PARAMETER s AS CHAR.
DEF OUTPUT PARAMETER rec-id AS INT INIT 0 NO-UNDO.

RUN add-zonelist.

PROCEDURE add-zonelist:

    create parameters. 
    ASSIGN 
    parameters.progname = ifname 
    parameters.section = "Dcode" 
    parameters.varname = cost-list-zone 
    parameters.vtype = 1 
    parameters.vstring = s. 

    FIND CURRENT parameters.
    rec-id = RECID(parameters).

END.
