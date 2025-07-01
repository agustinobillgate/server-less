DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.
DEF TEMP-TABLE t-parameters
    FIELD varname LIKE parameters.varname
    FIELD vstring LIKE parameters.vstring.
DEF TEMP-TABLE t-l-bestand LIKE l-bestand. /*FD, July 27, 2020*/

DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER nextdate AS DATE.
DEF OUTPUT PARAMETER selected-date AS DATE.
DEF OUTPUT PARAMETER fl-eknr AS INT.
DEF OUTPUT PARAMETER bl-eknr AS INT.
DEF OUTPUT PARAMETER auto-approve AS LOGICAL. /*naufal 241219 - add flag for parameter auto approve*/
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.
DEF OUTPUT PARAMETER TABLE FOR t-l-bestand.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
nextdate = billdate + 1. 
selected-date = nextdate. 
 
FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
fl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
bl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
/*naufal 241219 - add parameter for auto approve*/
FIND FIRST htparam WHERE paramnr = 390 NO-LOCK.
auto-approve = htparam.flogical.
/*end*/
FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

FOR EACH parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" :
    CREATE t-parameters.
    BUFFER-COPY parameters TO t-parameters.
END.

FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK.
    CREATE t-l-bestand.
    BUFFER-COPY l-bestand TO t-l-bestand.
END.