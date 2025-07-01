


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

DEFINE INPUT PARAMETER case-type    AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER voucherNo    AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER fname        AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER tname        AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE       FOR t-res-voucherNo.
DEFINE OUTPUT PARAMETER TABLE       FOR t-part-resline.    

CASE case-type :
    WHEN 1 THEN
    DO:
        FOR EACH reservation WHERE reservation.activeflag = 0
            AND reservation.vesrdepot = voucherNo NO-LOCK :
            CREATE t-res-voucherNo.
            ASSIGN 
                t-res-voucherNo.NAME          = reservation.NAME
                t-res-voucherNo.vesrdepot     = reservation.vesrdepot
                t-res-voucherNo.resnr         = reservation.resnr
                t-res-voucherNo.activeflag    = reservation.activeflag.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH reservation WHERE reservation.activeflag = 0
            AND reservation.NAME GE fname
            AND reservation.NAME LE tname
            AND reservation.vesrdepot MATCHES ("*" + voucherNo + "*") NO-LOCK :
            CREATE t-res-voucherNo.
            ASSIGN 
                t-res-voucherNo.NAME          = reservation.NAME
                t-res-voucherNo.vesrdepot     = reservation.vesrdepot
                t-res-voucherNo.resnr         = reservation.resnr
                t-res-voucherNo.activeflag    = reservation.activeflag.
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH reservation WHERE reservation.activeflag = 0
            AND reservation.vesrdepot MATCHES ("*" + voucherNo + "*") NO-LOCK :
            CREATE t-res-voucherNo.
            ASSIGN 
                t-res-voucherNo.NAME          = reservation.NAME
                t-res-voucherNo.vesrdepot     = reservation.vesrdepot
                t-res-voucherNo.resnr         = reservation.resnr
                t-res-voucherNo.activeflag    = reservation.activeflag.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH res-line WHERE res-line.active-flag LE 1 
            AND res-line.resstatus LE 6
            AND res-line.zimmer-wunsch MATCHES ("*VOUCHER*") NO-LOCK:
            CREATE t-part-resline.
            ASSIGN
                t-part-resline.zimmer-wunsch     = res-line.zimmer-wunsch
                t-part-resline.gastnr            = res-line.gastnr
                t-part-resline.NAME              = res-line.NAME
                t-part-resline.resnr             = res-line.resnr.
        END.
    END.
END CASE.


