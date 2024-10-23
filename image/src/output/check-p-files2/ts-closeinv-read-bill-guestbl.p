
DEFINE TEMP-TABLE t-h-bill  LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER guestnr        AS INT.
DEF INPUT  PARAMETER rec-h-bill     AS INT.
DEF OUTPUT PARAMETER rec-bill-guest AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

DEFINE buffer   bill-guest  FOR vhp.guest. 

FIND FIRST bill-guest WHERE bill-guest.gastnr = guestnr NO-LOCK.
rec-bill-guest = RECID(bill-guest).

FIND FIRST vhp.h-bill WHERE RECID(h-bill) = rec-h-bill EXCLUSIVE-LOCK.
vhp.h-bill.bilname = bill-guest.NAME + ", " + bill-guest.vorname1
                    + " " + bill-guest.anrede1.
FIND CURRENT vhp.h-bill NO-LOCK.
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).
