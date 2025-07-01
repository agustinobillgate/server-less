DEF TEMP-TABLE t-res-voucherNo  
    FIELD NAME          LIKE reservation.NAME
    FIELD vesrdepot     LIKE reservation.vesrdepot
    FIELD resnr         LIKE reservation.resnr
    FIELD activeflag    LIKE reservation.activeflag.

DEF TEMP-TABLE t-part-resline
    FIELD zimmer-wunsch     LIKE res-line.zimmer-wunsch
    FIELD gastnr            LIKE res-line.gastnr
    FIELD NAME              LIKE res-line.NAME
    FIELD resnr             LIKE res-line.resnr.


DEF TEMP-TABLE r-list
    FIELD ta-name AS CHAR FORMAT "x(24)" COLUMN-LABEL "Travel Agent Name"
    FIELD gname   AS CHAR FORMAT "x(24)" COLUMN-LABEL "Guest Name"
    FIELD resnr   LIKE reservation.resnr FORMAT ">>>>>>>>9"
    FIELD voucher AS CHAR FORMAT "x(20)" COLUMN-LABEL "Voucher"
    INITIAL ""
.

DEFINE TEMP-TABLE t-guest       LIKE guest.
DEFINE TEMP-TABLE t-reservation LIKE reservation.
DEFINE TEMP-TABLE t-voucherNo   LIKE t-res-voucherNo.

DEFINE INPUT PARAMETER voucher-no   AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER fname        AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE       FOR t-res-voucherNo.
DEFINE OUTPUT PARAMETER TABLE       FOR t-part-resline.
DEFINE OUTPUT PARAMETER TABLE       FOR r-list.   

DEFINE VARIABLE tname AS CHAR    NO-UNDO.
DEFINE VARIABLE i     AS INTEGER NO-UNDO.
DEFINE VARIABLE str   AS CHAR    NO-UNDO.

RUN read-reservationbl.p (3, 0, 0, voucher-no, OUTPUT TABLE t-reservation).
FIND FIRST t-reservation NO-LOCK NO-ERROR. 
IF AVAILABLE t-reservation THEN 
DO: 
    RUN res-vouchernobl.p (1, voucher-no, "", "",
                           OUTPUT TABLE t-res-voucherNo,
                           OUTPUT TABLE t-part-resline).
END.
ELSE
DO:
    IF fname NE "" THEN 
    DO: 
        tname = SUBSTR(fname,1,1) + "ZZZ". 
        RUN res-vouchernobl.p (2, voucher-no, fname, tname,
                               OUTPUT TABLE t-res-voucherNo,
                               OUTPUT TABLE t-part-resline).
    END. 
    ELSE 
    DO: 
        RUN res-vouchernobl.p (3, voucher-no, "", "",
                               OUTPUT TABLE t-res-voucherNo,
                               OUTPUT TABLE t-part-resline).
    END.
END.

FOR EACH r-list:
    DELETE r-list.
END.

RUN res-vouchernobl.p (4, "", "", "", 
                       OUTPUT TABLE t-voucherNo, 
                       OUTPUT TABLE t-part-resline).

FOR EACH t-part-resline NO-LOCK:
    DO i = 1 TO NUM-ENTRIES(t-part-resline.zimmer-wunsch,";") - 1:
        str = ENTRY(i, t-part-resline.zimmer-wunsch, ";").
        IF SUBSTR(str,1,7) = "voucher" 
            AND SUBSTR(str,8) MATCHES ("*" + voucher-no + "*") THEN 
        DO:
            i = 999.
            RUN read-guestbl.p (1, t-part-resline.gastnr, "", "",
                                OUTPUT TABLE t-guest).
            FIND FIRST t-guest NO-LOCK.
            CREATE r-list.
            ASSIGN
                r-list.ta-name = t-guest.NAME
                r-list.gname   = t-part-resline.NAME
                r-list.resnr   = t-part-resline.resnr
                r-list.voucher = SUBSTR(str,8)
                .
        END.
    END.
END.
