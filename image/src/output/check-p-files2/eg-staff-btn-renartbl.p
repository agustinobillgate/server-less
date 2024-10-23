
DEF INPUT PARAMETER staff-nr AS INT.
DEF OUTPUT PARAMETER avail-table AS LOGICAL INIT NO.

DEF BUFFER main FOR eg-mdetail.
DEF BUFFER req  FOR eg-request.

FIND FIRST main WHERE main.KEY = 2 AND main.nr = staff-nr NO-LOCK NO-ERROR.
FIND FIRST req WHERE req.assign-to = staff-nr NO-LOCK NO-ERROR.
IF AVAILABLE req AND AVAILABLE main THEN
    avail-table = YES.
