
DEF INPUT PARAMETER rechnr AS INT.
DEF OUTPUT PARAMETER a-resnr AS INT.
DEF OUTPUT PARAMETER a-rechnr AS INT.

FIND FIRST bill WHERE bill.rechnr = rechnr NO-LOCK.
ASSIGN
    a-resnr = bill.resnr
    a-rechnr = bill.rechnr.
