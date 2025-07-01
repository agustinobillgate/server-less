DEF TEMP-TABLE t-paramtext LIKE paramtext.

DEF INPUT  PARAMETER case-type AS INTEGER       NO-UNDO.
DEF INPUT  PARAMETER int1       AS INT.
DEF INPUT  PARAMETER int2       AS INT.
DEF INPUT  PARAMETER int3       AS INT.
DEF INPUT  PARAMETER char1      AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-paramtext.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST paramtext WHERE paramtext.ptexte = char1
            AND paramtext.sprachcode NE int1 NO-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN RUN assign-it.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH paramtext WHERE paramtext.txtnr GE int1
            AND paramtext.txtnr LE int2 NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST paramtext WHERE paramtext.ptexte = char1
            AND paramtext.txtnr NE int1
            AND paramtext.txtnr GT int2 NO-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN RUN assign-it.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST htparam WHERE paramnr = 987 NO-LOCK.
        int1 = 600 + htparam.finteger.
        FIND FIRST htparam WHERE paramnr = 433 NO-LOCK.
        int2 = 600 + htparam.finteger.
        FOR EACH paramtext WHERE  paramtext.txtnr GE 601
            AND paramtext.txtnr LE 699 AND paramtext.ptexte NE ""
            AND paramtext.txtnr NE int1 AND paramtext.txtnr NE int2 NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH paramtext WHERE  paramtext.txtnr GE 601
            AND paramtext.txtnr LE 699 AND paramtext.ptexte NE "" NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST paramtext WHERE paramtext.ptexte = char1
            AND paramtext.txtnr NE int1 NO-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN RUN assign-it.
    END.
    WHEN 7 THEN
    DO:
        FIND FIRST paramtext WHERE paramtext.txtnr = int1
            NO-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN RUN assign-it.
    END.
    WHEN 8 THEN
    DO:
        FIND FIRST paramtext WHERE paramtext.txtnr = int1 AND 
            paramtext.sprachcode = int2 NO-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN RUN assign-it.
    END.
    WHEN 9 THEN
    DO:
        FOR EACH paramtext WHERE paramtext.txtnr GE int1
            AND paramtext.txtnr LE int2 AND paramtext.ptexte NE "" NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 10 THEN
    DO:
        FOR EACH paramtext WHERE paramtext.txtnr GE int1
            AND paramtext.txtnr LE int2 AND paramtext.ptexte NE "" NO-LOCK:
            RUN assign-it.
        END.
        RUN filter-it.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-paramtext.
    BUFFER-COPY paramtext TO t-paramtext.
END.

PROCEDURE filter-it:
    FIND FIRST zimkateg WHERE zimkateg.kurzbez = ENTRY(1, char1, ";")
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE zimkateg THEN RETURN.
    FOR EACH t-paramtext:
        FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr
            AND zimmer.setup = t-paramtext.txtnr - 9200
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE zimmer THEN DELETE t-paramtext.
    END.
END.
