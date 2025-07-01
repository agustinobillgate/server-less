
DEFINE TEMP-TABLE t-fa-grup    LIKE fa-grup.
DEFINE TEMP-TABLE t-fa-lager   LIKE fa-lager. 
DEFINE TEMP-TABLE lagerBuff LIKE fa-lager.

DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER last-acctdate AS DATE.
DEF OUTPUT PARAMETER mm AS INT.
DEF OUTPUT PARAMETER yy AS INT.
DEF OUTPUT PARAMETER from-month AS CHAR.
DEF OUTPUT PARAMETER maxNr AS INT INIT 0.
DEF OUTPUT PARAMETER p-977 AS CHAR.
DEF OUTPUT PARAMETER p-224 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR lagerBuff.
DEF OUTPUT PARAMETER TABLE FOR t-fa-grup.
DEF OUTPUT PARAMETER TABLE FOR t-fa-lager.

RUN htpdate.p (224, OUTPUT p-224).

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
p-977 = htparam.fchar. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST htparam WHERE paramnr = 881 no-lock.    /* LAST Dep'n DATE */ 
last-acctdate = htparam.fdate. 

mm = MONTH(last-acctdate). 
yy = YEAR(last-acctdate). 
from-month = STRING(mm,"99") + STRING(yy,"9999"). 

RUN load-fa-lager.

FOR EACH fa-grup:
    CREATE t-fa-grup.
    BUFFER-COPY fa-grup TO t-fa-grup.
END.

FOR EACH fa-lager:
    CREATE t-fa-lager.
    BUFFER-COPY fa-lager TO t-fa-lager.
END.

PROCEDURE load-fa-lager:
  FOR EACH fa-lager NO-LOCK BY fa-lager.lager-nr:
      CREATE lagerBuff.
      BUFFER-COPY fa-lager TO lagerBuff.
      maxNr = fa-lager.lager-nr.
  END.
  maxNr = maxNr + 1.
  CREATE lagerBuff.
  ASSIGN lagerBuff.lager-nr = maxNr
          lagerBuff.bezeich = "".
END.
