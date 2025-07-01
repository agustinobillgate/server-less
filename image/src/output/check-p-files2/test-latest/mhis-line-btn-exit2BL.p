DEFINE buffer mhis-line1 FOR mhis-line.

DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER m-list-datum AS DATE.
DEF INPUT PARAMETER m-list-cost AS DECIMAL.
DEF INPUT PARAMETER remark-screen-value AS CHAR.

FIND FIRST mhis-line1 WHERE RECID(mhis-line1) = rec-id EXCLUSIVE-LOCK. 
mhis-line1.datum = m-list-datum. 
mhis-line1.cost = m-list-cost. 
mhis-line1.remark = remark-screen-value. 
FIND CURRENT mhis-line1 NO-LOCK.
