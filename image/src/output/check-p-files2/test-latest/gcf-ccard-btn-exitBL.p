

DEF INPUT PARAMETER gastnr AS INT.
DEF INPUT PARAMETER ausweis-nr2 AS CHAR.

FIND FIRST guest WHERE guest.gastnr = gastnr EXCLUSIVE-LOCK.
ASSIGN guest.ausweis-nr2 = ausweis-nr2.
FIND CURRENT guest NO-LOCK.
