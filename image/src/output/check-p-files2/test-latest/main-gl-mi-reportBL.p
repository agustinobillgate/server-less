
DEF TEMP-TABLE t-brief LIKE brief.

DEF INPUT  PARAMETER reportnr           AS INT.
DEF OUTPUT PARAMETER avail-parameters   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-brief.

FIND FIRST brief WHERE brief.briefnr = reportnr NO-LOCK.
CREATE t-brief.
BUFFER-COPY brief TO t-brief.

FIND FIRST parameters WHERE progname = "GL-macro"
    AND parameters.SECTION = STRING(reportnr) NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN
    avail-parameters = YES.
