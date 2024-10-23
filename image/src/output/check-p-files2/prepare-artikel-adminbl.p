
DEF TEMP-TABLE t-artikel LIKE artikel
    FIELD zk-bezeich LIKE zwkum.bezeich
    FIELD ek-bezeich LIKE ekum.bezeich
    FIELD argt-bez   LIKE arrangement.argt-bez
    FIELD rec-id     AS INT.

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER from-bez    AS CHAR.
DEFINE INPUT  PARAMETER dept        AS INT.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR.
DEFINE OUTPUT PARAMETER msg-str2    AS CHAR.
DEFINE OUTPUT PARAMETER local-nr    AS INT.
DEFINE OUTPUT PARAMETER foreign-nr  AS INT.
DEFINE OUTPUT PARAMETER d-bezeich   AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "artikel-admin". 

DEFINE VARIABLE p121 AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7).",lvCAREA,"").
  RETURN. 
END. 
local-nr = waehrung.waehrungsnr. 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar 
  NO-LOCK NO-ERROR. 
IF (NOT AVAILABLE waehrung) THEN 
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)",lvCAREA,"").
  RETURN. 
END. 
foreign-nr = waehrung.waehrungsnr.


FIND FIRST hoteldpt WHERE hoteldpt.num = dept NO-LOCK. 
d-bezeich = hoteldpt.depart. 

FIND FIRST htparam WHERE htparam.paramnr = 121 NO-LOCK NO-ERROR.
ASSIGN p121 = htparam.finteger.

ASSIGN d-bezeich = d-bezeich + ";" + STRING(p121).

FOR EACH artikel WHERE artikel.departement = dept NO-LOCK:
    RUN assign-it.
END.

RUN artikel-admin-check-btn-exitbl.p
    (pvILanguage, OUTPUT msg-str2).


PROCEDURE assign-it:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
    ASSIGN t-artikel.rec-id = RECID(artikel).
    FIND FIRST zwkum WHERE zwkum.zknr = artikel.zwkum 
      AND zwkum.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE zwkum THEN ASSIGN t-artikel.zk-bezeich = zwkum.bezeich. 
    FIND FIRST ekum WHERE ekum.eknr = artikel.endkum NO-LOCK NO-ERROR. 
    IF AVAILABLE ekum THEN t-artikel.ek-bezeich = ekum.bezeich. 
    FIND FIRST arrangement WHERE arrangement.argtnr = artikel.artgrp 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE arrangement THEN t-artikel.argt-bez = arrangement.argt-bez. 
    ELSE t-artikel.argt-bez = "None".
END.
