
DEF INPUT  PARAMETER rechnr      AS INT.
DEF OUTPUT PARAMETER bill-resnr  AS INT.
DEF OUTPUT PARAMETER bill-rechnr AS INT.

FIND FIRST bill WHERE bill.rechnr = rechnr NO-LOCK NO-ERROR. 
bill-resnr  = bill.resnr.
bill-rechnr = bill.rechnr.
