
DEF TEMP-TABLE t-artikel LIKE artikel
    FIELD zk-bezeich LIKE zwkum.bezeich
    FIELD ek-bezeich LIKE ekum.bezeich
    FIELD argt-bez   LIKE arrangement.argt-bez
    FIELD rec-id     AS INT.

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER case-type   AS INT.
DEFINE INPUT  PARAMETER dept        AS INT.
DEFINE INPUT  PARAMETER artNo       AS INT.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "artikel-admin".

IF case-type = 2 THEN 
DO:
    RUN check-argt.
    RETURN.
END.

FOR EACH artikel WHERE artikel.departement = dept NO-LOCK:
    RUN assign-it.
END.


PROCEDURE assign-it:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.

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


PROCEDURE check-argt:
  FIND FIRST argt-line WHERE argt-line.departement = dept
      AND argt-line.argt-artnr = artNo NO-LOCK NO-ERROR.
  IF AVAILABLE argt-line THEN
  DO:
    FIND FIRST arrangement WHERE arrangement.argtnr = argt-line.argtnr
        NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement THEN
    msg-str = msg-str + CHR(2)
            + translateExtended ("Wrong Article type as arrangement found using this article",lvCAREA,"")
            + " " + arrangement.arrangement.
    ELSE 
    msg-str = msg-str + CHR(2)
            + translateExtended ("argt-line record exists for this article number!",lvCAREA,"").
    RETURN NO-APPLY. 
  END.
END.
