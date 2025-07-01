DEF TEMP-TABLE t-printer
  FIELD nr AS INTEGER
  FIELD path AS CHARACTER
  FIELD copies AS INTEGER
  FIELD make AS CHARACTER
  FIELD emu AS CHARACTER
  FIELD position AS CHARACTER
  FIELD pglen AS INTEGER
  FIELD spooled AS LOGICAL
  FIELD bondrucker AS LOGICAL
  FIELD opsysname AS CHARACTER
.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER recid-emu AS INTEGER.
DEF INPUT PARAMETER TABLE FOR t-printer.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-printer NO-LOCK NO-ERROR.
IF NOT AVAILABLE t-printer THEN RETURN NO-APPLY.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE printer.
        BUFFER-COPY t-printer TO printer.
        FIND FIRST printcod WHERE RECID(printcod) = recid-emu.
        IF AVAILABLE printcod THEN PRINTER.emu = printcod.emu.
        RELEASE printer.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST printer WHERE printer.nr = t-printer.nr
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE printer THEN
        DO:
            BUFFER-COPY t-printer EXCEPT emu TO PRINTER.
            FIND FIRST printcod WHERE RECID(printcod) = recid-emu.
            IF AVAILABLE printcod THEN PRINTER.emu = printcod.emu.
            RELEASE printer.
            success-flag = YES.
        END.
    END.
END CASE.
