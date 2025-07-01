
DEF INPUT PARAMETER v-vendor-nr AS INT.
DEF OUTPUT PARAMETER avail-ven AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER ven-bezeich AS CHAR.

DEF BUFFER ven FOR eg-vendor.
FIND FIRST ven WHERE ven.vendor-nr = v-vendor-nr NO-LOCK NO-ERROR.
IF AVAILABLE ven THEN
DO:
    ven-bezeich = ven.bezeich.
    avail-ven = YES.
END.

