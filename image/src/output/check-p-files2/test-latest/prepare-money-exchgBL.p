
DEFINE TEMP-TABLE t-waehrung    LIKE waehrung.
DEFINE TEMP-TABLE t-hoteldpt    LIKE hoteldpt.
DEFINE TEMP-TABLE art1          LIKE artikel.

DEF OUTPUT PARAMETER local-nr AS INT.
DEF OUTPUT PARAMETER local-code AS CHAR.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR art1.

DEFINE buffer art2 FOR artikel.

FIND FIRST htparam WHERE htparam.paramnr = 112 NO-LOCK. 
FIND FIRST art2 WHERE art2.artnr = htparam.finteger 
  AND art2.departement = 0 AND art2.artart = 6 
  AND NOT art2.pricetab NO-LOCK NO-ERROR. 
IF NOT AVAILABLE art2 THEN 
DO: 
  err-code = 1.
  /*MThide MESSAGE NO-PAUSE. 
  MESSAGE translateExtended ("Local Cash Article not defined! (Param 112 / Grp 5).",lvCAREA,"") 
  VIEW-AS ALERT-BOX INFORMATION.*/
  RETURN. 
END. 
local-nr = art2.artnr. 
CREATE art1.
BUFFER-COPY art2 TO art1.
 
FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
local-code = htparam.fchar. 
FIND FIRST waehrung WHERE waehrung.wabkurz = local-code NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO: 
  err-code = 2.
  /*MThide MESSAGE NO-PAUSE. 
  MESSAGE translateExtended ("Local Currency not defined (Param 152/7).",lvCAREA,"") 
  VIEW-AS ALERT-BOX INFORMATION.*/
  RETURN. 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.

FOR EACH waehrung:
    CREATE t-waehrung.
    BUFFER-COPY waehrung TO t-waehrung.
END.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
