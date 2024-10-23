
DEF TEMP-TABLE g-list LIKE gl-fstype.

DEF INPUT-OUTPUT PARAMETER TABLE FOR g-list.

FIND FIRST g-list NO-ERROR.
IF NOT AVAILABLE g-list THEN RETURN.

FIND FIRST gl-fstype WHERE gl-fstype.nr = g-list.nr NO-ERROR.
IF NOT AVAILABLE gl-fstype THEN CREATE gl-fstype.
BUFFER-COPY g-list TO gl-fstype.
