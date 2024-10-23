
DEF INPUT  PARAMETER reportnr AS INT.
DEF OUTPUT PARAMETER avail-param AS LOGICAL INIT NO.

FIND FIRST parameters WHERE progname = "FO-macro"
    AND parameters.SECTION = STRING(reportnr) NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN avail-param = YES.
