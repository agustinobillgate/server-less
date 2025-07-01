
DEFINE BUFFER sub FOR eg-vendor.

DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER vendor-vendor-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER avail-sub AS LOGICAL INIT NO.

FIND FIRST eg-vendor WHERE RECID(eg-vendor) = rec-id.
IF curr-select = "chg" THEN
    find first sub where sub.vendor-nr = vendor-vendor-nr
        AND ROWID(sub) NE ROWID(eg-vendor) no-lock no-error.

ELSE IF curr-select = "add" THEN
    find first sub where sub.vendor-nr = vendor-vendor-nr no-lock no-error.

if available sub then
    avail-sub = YES.

