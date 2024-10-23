
DEF TEMP-TABLE t-outorder         LIKE outorder.
DEF INPUT  PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rmNo         AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER resNo        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER ci-date      AS DATE    NO-UNDO.
DEF INPUT  PARAMETER to-date      AS DATE    NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-outorder.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = rmNo
            AND outorder.betriebsnr = resNo NO-LOCK NO-ERROR.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = rmNo NO-LOCK NO-ERROR.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = rmNo 
            AND outorder.gespstart GE ci-date
            AND outorder.gespende LE ci-date NO-LOCK NO-ERROR.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = rmNo 
            AND outorder.gespende GE ci-date NO-LOCK NO-ERROR.
    END.
    WHEN 5 THEN
    DO:
        FIND FIRST outorder WHERE RECID(outorder) = resNo NO-LOCK NO-ERROR.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = rmNo
            AND outorder.gespstart LE ci-date AND outorder.gespende GE ci-date
            AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.
    END.
    WHEN 7 THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = rmNo
            AND outorder.betriebsnr = resNo
            AND outorder.gespstart GT to-date
            AND outorder.gespende LT ci-date NO-LOCK NO-ERROR.
    END.

    WHEN 99 THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = rmNo
            AND outorder.betriebsnr = resNo EXCLUSIVE-LOCK NO-ERROR.
    END.
END CASE.


IF AVAILABLE outorder THEN
DO:
  CREATE t-outorder.
  BUFFER-COPY outorder TO t-outorder.
END.

