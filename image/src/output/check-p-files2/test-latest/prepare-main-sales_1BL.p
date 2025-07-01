
DEF OUTPUT PARAMETER new-contrate AS LOGICAL.
DEF OUTPUT PARAMETER p-223 AS LOGICAL.
DEF OUTPUT PARAMETER p-999 AS LOGICAL.
DEF OUTPUT PARAMETER p-1459 AS INT.
DEF OUTPUT PARAMETER pl-1459 AS LOGICAL.
DEF OUTPUT PARAMETER p1109 AS LOGICAL.
DEF OUTPUT PARAMETER htl-city        AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAMETER curr-htl-city   AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAMETER new-setup       AS LOGICAL INIT NO NO-UNDO.

FIND FIRST paramtext WHERE txtnr = 204 NO-ERROR. 
curr-htl-city = paramtext.ptexte.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 223 NO-LOCK. 
p-223 = htparam.flogical.
 
FIND FIRST htparam WHERE paramnr = 999 NO-LOCK.
p-999 = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 1459 NO-LOCK.
p-1459 = htparam.paramgr.
pl-1459 = htparam.flogical.

FIND FIRST paramtext WHERE paramtext.txtnr GE 203.
htl-city = paramtext.ptexte.

RUN htplogic.p(1109, OUTPUT p1109).

FIND FIRST bediener WHERE bediener.username MATCHES "*" + CHR(2) + "*" NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN ASSIGN new-setup = YES.
ELSE ASSIGN new-setup = NO.
