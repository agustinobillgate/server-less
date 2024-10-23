
DEFINE TEMP-TABLE setup-list 
    FIELD nr   AS INTEGER 
    FIELD CHAR AS CHAR FORMAT "x(1)". 

DEF TEMP-TABLE t-guest
    FIELD firmen-nr LIKE guest.firmen-nr
    FIELD steuernr  LIKE guest.steuernr.

DEF INPUT  PARAMETER inp-resname            AS CHAR.
DEF INPUT  PARAMETER user-init              AS CHAR.

DEF OUTPUT PARAMETER ext-char               AS CHAR.
DEF OUTPUT PARAMETER long-stay              AS INT.
DEF OUTPUT PARAMETER ci-date                AS DATE.
DEF OUTPUT PARAMETER fdate1                 AS DATE.
DEF OUTPUT PARAMETER fdate2                 AS DATE.
DEF OUTPUT PARAMETER lname                  AS CHAR.
DEF OUTPUT PARAMETER show-rate              AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER bediener-permissions   AS CHAR.
DEF OUTPUT PARAMETER feldtype-336           AS INT.
DEF OUTPUT PARAMETER flogical-336           AS LOGICAL.
DEF OUTPUT PARAMETER finteger-337           AS INT.
DEF OUTPUT PARAMETER finteger-338           AS INT.
DEF OUTPUT PARAMETER flogical-1111          AS LOGICAL.
DEF OUTPUT PARAMETER p-297                  AS INT.
DEF OUTPUT PARAMETER p-437                  AS LOGICAL.
DEF OUTPUT PARAMETER l-param472             AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER vipnr1                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr2                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr3                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr4                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr5                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr6                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr7                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr8                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER vipnr9                 AS INTEGER INITIAL 999999999. 
DEF OUTPUT PARAMETER TABLE FOR t-guest.
DEF OUTPUT PARAMETER TABLE FOR setup-list.


RUN htpint.p   (297, OUTPUT p-297).
RUN htplogic.p (437, OUTPUT p-437).

FIND FIRST htparam WHERE htparam.paramnr = 472 NO-LOCK. 
IF htparam.paramgruppe = 99 AND htparam.feldtyp = 4 THEN            /* Rulita 140324| Fixing for Serverless */
ASSIGN l-param472 = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 148 NO-LOCK. 
/* Extended CHAR FOR GCF Prog */ 
ext-char = htparam.fchar. 

FIND FIRST htparam WHERE htparam.paramnr = 139 NO-LOCK. 
long-stay = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
fdate1 = ci-date. 
fdate2 = ci-date. 
lname = inp-resname. 

FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
vipnr1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
vipnr2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
vipnr3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
vipnr4 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
vipnr5 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
vipnr6 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
vipnr7 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
vipnr8 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
vipnr9 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
IF SUBSTR(bediener.permissions, 35, 1) NE "0" THEN show-rate = YES. 
bediener-permissions = bediener.permissions.

FIND FIRST guest WHERE guest.karteityp GE 1 AND guest.gastnr GT 0 AND guest.firmen-nr GT 0 AND guest.steuernr NE "" NO-LOCK NO-ERROR.
DO WHILE AVAILABLE guest:
    CREATE t-guest.
    ASSIGN
        t-guest.firmen-nr = guest.firmen-nr
        t-guest.steuernr  = guest.steuernr.

    FIND NEXT guest WHERE guest.karteityp GE 1 AND guest.gastnr GT 0 AND guest.firmen-nr GT 0 AND guest.steuernr NE "" NO-LOCK NO-ERROR.
END.
/*
FOR EACH guest WHERE guest.karteityp GE 1 
    AND guest.gastnr GT 0 
    AND guest.firmen-nr GT 0 
    AND guest.steuernr NE "" NO-LOCK:
    CREATE t-guest.
    ASSIGN
        t-guest.firmen-nr = guest.firmen-nr
        t-guest.steuernr  = guest.steuernr.
END.
*/

FIND FIRST htparam WHERE paramnr = 336 NO-LOCK.
feldtype-336 = htparam.feldtyp.
flogical-336 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 337 NO-LOCK. 
finteger-337 = htparam.finteger.
FIND FIRST htparam WHERE paramnr = 338 NO-LOCK. 
finteger-338 = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 1111 NO-LOCK.
flogical-1111 = htparam.flogical.

RUN bed-setup.

PROCEDURE bed-setup: 
DEFINE VARIABLE it-exist AS LOGICAL INITIAL NO. 
/*  this record must exist !!! */ 
  CREATE setup-list. 
  setup-list.nr = 1. 
  setup-list.char = " ". 
 
  FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
    AND paramtext.txtnr LE 9299 NO-LOCK: 
    CREATE setup-list. 
    setup-list.nr = paramtext.txtnr - 9199. 
    setup-list.char = SUBSTR(paramtext.notes,1,1). 
    it-exist = YES. 
  END. 
END.
