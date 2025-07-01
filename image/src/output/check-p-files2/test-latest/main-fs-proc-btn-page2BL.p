
DEF TEMP-TABLE tt-grund
    FIELD curr-i AS INTEGER
    FIELD grund  AS CHAR.

DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER b1-resline     AS INT.
DEF INPUT  PARAMETER curr-gastnr    AS INT.
DEF OUTPUT PARAMETER avail-b-storno AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR tt-grund.

DEF VAR i AS INT.
FIND FIRST b-storno WHERE b-storno.bankettnr = b1-resnr AND
    b-storno.breslinnr = b1-resline AND b-storno.gastnr = curr-gastnr NO-ERROR.
IF AVAILABLE b-storno THEN
DO:
    avail-b-storno = YES.
    DO i = 1 TO 10:
        CREATE tt-grund.
        ASSIGN 
            tt-grund.curr-i = i
            tt-grund.grund  = b-storno.grund[i].
    END.
END.
