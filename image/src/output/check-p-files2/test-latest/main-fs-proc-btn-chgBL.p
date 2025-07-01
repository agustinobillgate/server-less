
DEF TEMP-TABLE t-b-storno LIKE b-storno.

DEF INPUT  PARAMETER b1-resnr    AS INT.
DEF INPUT  PARAMETER b1-resline  AS INT.
DEF INPUT  PARAMETER curr-gastnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-b-storno.

FOR EACH b-storno WHERE b-storno.bankettnr = b1-resnr 
    AND b-storno.breslinnr = b1-resline 
    AND b-storno.gastnr = curr-gastnr NO-LOCK:
    CREATE t-b-storno.
    BUFFER-COPY b-storno TO t-b-storno.
END.
