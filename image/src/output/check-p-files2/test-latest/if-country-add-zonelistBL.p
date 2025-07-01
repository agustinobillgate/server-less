
DEF INPUT PARAMETER cost-list-zone AS CHAR.
DEF INPUT PARAMETER s AS CHAR.
DEF OUTPUT PARAMETER rec-id AS INT.

create parameters. 
parameters.progname = "interface". 
parameters.section = "Dcode". 
parameters.varname = cost-list-zone. 
parameters.vtype = 1. 
parameters.vstring = s.
FIND CURRENT parameters.
rec-id = RECID(parameters).
