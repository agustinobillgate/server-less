DEFINE TEMP-TABLE t-b-storno LIKE b-storno.

DEFINE INPUT PARAMETER resnr AS INTEGER.
DEFINE INPUT PARAMETER resline AS INTEGER.
DEFINE INPUT PARAMETER curr-gastnr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-b-storno.

IF curr-gastnr LT 1 THEN DO:
    FIND FIRST b-storno WHERE b-storno.bankettnr = resnr 
        AND b-storno.breslinnr = resline NO-LOCK NO-ERROR.
    IF AVAILABLE b-storno THEN DO:
        CREATE t-b-storno.
        BUFFER-COPY b-storno TO t-b-storno.
    END.
END.
ELSE DO: 
    FIND FIRST b-storno WHERE b-storno.bankettnr = resnr 
        AND b-storno.breslinnr = resline AND b-storno.gastnr = curr-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE b-storno THEN DO:
        CREATE t-b-storno.
        BUFFER-COPY b-storno TO t-b-storno.
    END.
END.

