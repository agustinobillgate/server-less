DEFINE INPUT PARAMETER gast-no AS INTEGER.
DEFINE OUTPUT PARAMETER email AS CHARACTER.
DEFINE OUTPUT PARAMETER member-exist AS LOGICAL.
DEFINE OUTPUT PARAMETER loyalty-name AS CHARACTER.

FIND FIRST mc-guest WHERE mc-guest.gastnr = gast-no AND mc-guest.activeflag NO-LOCK NO-ERROR.
IF AVAILABLE mc-guest THEN
    member-exist = YES.

FIND FIRST guest WHERE guest.gastnr = gast-no NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
    ASSIGN
        email = guest.email-adr.

FIND FIRST htparam WHERE htparam.paramnr = 787.
IF AVAILABLE htparam THEN
    loyalty-name = ENTRY(1, htparam.fchar, "-").
