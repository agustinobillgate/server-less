
DEF TEMP-TABLE t-parameters
    FIELD varname   LIKE parameters.varname
    FIELD vstring   LIKE parameters.vstring.

DEF TEMP-TABLE t-l-hauptgrp LIKE l-hauptgrp.

DEF INPUT-OUTPUT PARAMETER LnL-filepath      AS CHAR.
DEF INPUT        PARAMETER LnL-prog          AS CHAR.
DEF OUTPUT       PARAMETER long-digit        AS LOGICAL.
DEF OUTPUT       PARAMETER avail-l-untergrup AS LOGICAL INIT NO.
DEF OUTPUT       PARAMETER TABLE FOR t-l-hauptgrp.
DEF OUTPUT       PARAMETER TABLE FOR t-parameters.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST l-untergrup WHERE l-untergrup.betriebsnr = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE l-untergrup THEN avail-l-untergrup = YES.

FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
    LnL-filepath = htparam.fchar. 
    IF SUBSTR(LnL-filepath, LENGTH(LnL-filepath), 1) NE "\" THEN 
        LnL-filepath = LnL-filepath + "\". 
    LnL-filepath = LnL-filepath + LnL-prog.
END.

FOR EACH parameters NO-LOCK WHERE 
    parameters.progname = "CostCenter"  AND 
    parameters.section = "Name" :
    CREATE t-parameters.
    ASSIGN
      t-parameters.varname   = parameters.varname
      t-parameters.vstring   = parameters.vstring.
END.

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
END.
