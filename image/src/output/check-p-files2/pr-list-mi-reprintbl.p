
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER list-str0      AS CHAR.
DEF OUTPUT PARAMETER briefnr        AS INT.
DEF OUTPUT PARAMETER printer-nr     AS INT.
DEF OUTPUT PARAMETER l-od-docu-nr   AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER avail-l-od     AS LOGICAL INIT NO.

DEFINE buffer l-od FOR l-order.

RUN htpint.p(687, OUTPUT briefnr).
{supertransBL.i} 

DEF VAR lvCAREA AS CHAR INITIAL "prepare-fo-parxls".
FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE brief THEN
DO:
    msg-str = msg-str + translateExtended ("Letter Number not found : ",lvCAREA,"")
            + STRING(briefnr) + ".".
    RETURN NO-APPLY.
END.
FIND FIRST l-od WHERE l-od.docu-nr = TRIM(list-str0) NO-LOCK NO-ERROR. 
IF AVAILABLE l-od THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 220 NO-LOCK. 
    printer-nr = htparam.finteger.
    l-od-docu-nr = l-od.docu-nr.
    avail-l-od = YES.
END. 
