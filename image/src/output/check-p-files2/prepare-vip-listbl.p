
DEF TEMP-TABLE t-vipnr
    FIELD vip-nr1 AS INT
    FIELD vip-nr2 AS INT
    FIELD vip-nr3 AS INT
    FIELD vip-nr4 AS INT
    FIELD vip-nr5 AS INT
    FIELD vip-nr6 AS INT
    FIELD vip-nr7 AS INT
    FIELD vip-nr8 AS INT
    FIELD vip-nr9 AS INT
    FIELD vip-nr10 AS INT.

DEF INPUT  PARAMETER user-init  AS CHAR.
DEF OUTPUT PARAMETER ci-date    AS DATE.
DEF OUTPUT PARAMETER show-rate  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER p-297      AS INT.
DEF OUTPUT PARAMETER LnL-filepath AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-vipnr.


FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
    LnL-filepath = htparam.fchar. 
    IF SUBSTR(LnL-filepath, LENGTH(LnL-filepath), 1) NE "\" THEN 
        LnL-filepath = LnL-filepath + "\". 
    /*MTLnL-filepath = LnL-filepath + LnL-prog. */
END. 

FIND FIRST htparam WHERE htparam.paramnr = 297 NO-LOCK.
p-297 = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
IF SUBSTR(bediener.permissions, 35, 1) NE "0" THEN show-rate = YES. 

RUN fill-vipnr.

PROCEDURE fill-vipnr: 
  CREATE t-vipnr.
  FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
  t-vipnr.vip-nr1 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
  t-vipnr.vip-nr2 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr =  702 NO-LOCK. 
  t-vipnr.vip-nr3 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
  t-vipnr.vip-nr4 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
  t-vipnr.vip-nr5 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
  t-vipnr.vip-nr6 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
  t-vipnr.vip-nr7 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
  t-vipnr.vip-nr8 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
  t-vipnr.vip-nr9 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 712 NO-LOCK. 
  t-vipnr.vip-nr10 = htparam.finteger. 
END. 
