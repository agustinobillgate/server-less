DEF TEMP-TABLE t-reservation    LIKE reservation.

DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rsvNo      AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gastNo     AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER voucherNo  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE      FOR t-reservation.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST reservation WHERE reservation.resnr = rsvNo NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
          CREATE t-reservation.
          BUFFER-COPY reservation TO t-reservation.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST reservation WHERE reservation.resnr = rsvNo and
            reservation.gastnr = gastNo NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
          CREATE t-reservation.
          BUFFER-COPY reservation TO t-reservation.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST reservation WHERE reservation.activeflag = 0
            AND reservation.vesrdepot = voucherNo NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
          CREATE t-reservation.
          BUFFER-COPY reservation TO t-reservation.
        END.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST reservation WHERE reservation.activeflag = 0
            AND reservation.gastnr GT 0 NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
          CREATE t-reservation.
          BUFFER-COPY reservation TO t-reservation.
        END.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH reservation WHERE reservation.name = voucherNo
            AND reservation.gastnr = gastNo 
            AND reservation.activeflag = 0 NO-LOCK :
            CREATE t-reservation.
            BUFFER-COPY reservation TO t-reservation.
        END.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST reservation WHERE reservation.resart = rsvNo
            NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
          CREATE t-reservation.
          BUFFER-COPY reservation TO t-reservation.
        END.
    END.
    WHEN 7 THEN
    DO:
        FIND FIRST reservation WHERE reservation.activeflag = rsvNo
            AND reservation.guestnrcom[2] = gastNo NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
          CREATE t-reservation.
          BUFFER-COPY reservation TO t-reservation.
        END.
    END.
END CASE.

