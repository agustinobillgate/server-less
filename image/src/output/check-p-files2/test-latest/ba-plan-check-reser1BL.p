
DEF TEMP-TABLE t-bk-reser
    FIELD resstatus LIKE bk-reser.resstatus
    FIELD veran-nr  LIKE bk-reser.veran-nr.

DEF INPUT  PARAMETER rml-raum    LIKE bk-reser.raum.
DEF INPUT  PARAMETER rsv-date    AS DATE.
DEF INPUT  PARAMETER rsv-i       AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-bk-reser.

FOR EACH bk-reser WHERE bk-reser.raum = rml-raum
    AND bk-reser.datum = rsv-date
    AND rsv-i GE bk-reser.von-i AND rsv-i LE bk-reser.bis-i 
    AND bk-reser.resstatus LE 2 
    USE-INDEX raumdat_ix NO-LOCK:
    CREATE t-bk-reser.
    ASSIGN
        t-bk-reser.resstatus = bk-reser.resstatus
        t-bk-reser.veran-nr  = bk-reser.veran-nr.
END.
