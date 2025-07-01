
DEF TEMP-TABLE t-zimmer LIKE zimmer.

DEF INPUT  PARAMETER r-zinr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.


FIND FIRST zimmer WHERE zimmer.zinr = r-zinr NO-LOCK.
CREATE t-zimmer.
BUFFER-COPY zimmer TO t-zimmer.
