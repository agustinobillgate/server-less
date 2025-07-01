DEF TEMP-TABLE t-zimmer LIKE zimmer.

DEF INPUT  PARAMETER r-zinr AS CHAR.
DEF OUTPUT PARAMETER curr-setup AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.

FIND FIRST zimmer WHERE zimmer.zinr = r-zinr NO-LOCK.
IF zimmer.setup NE 0 THEN
DO :
    FIND FIRST paramtext WHERE paramtext.txtnr = (9200 + zimmer.setup) NO-LOCK.
    curr-setup = SUBSTR(paramtext.notes,1,1).
END.
ELSE curr-setup = "". 

CREATE t-zimmer.
BUFFER-COPY zimmer TO t-zimmer.
