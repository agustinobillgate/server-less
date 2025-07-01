
DEF INPUT PARAMETER inp-gastnr AS INT.
DEF INPUT PARAMETER email-str  AS CHAR.

FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK.
FIND CURRENT guest EXCLUSIVE-LOCK.
guest.email-adr = email-str.
FIND CURRENT guest NO-LOCK.
