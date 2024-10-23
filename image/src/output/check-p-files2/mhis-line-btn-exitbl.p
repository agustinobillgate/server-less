
DEF INPUT PARAMETER curr-nr AS INT.
DEF INPUT PARAMETER m-list-datum AS DATE.
DEF INPUT PARAMETER m-list-cost AS DECIMAL.
DEF INPUT PARAMETER remark-screen-value AS CHAR.
DEF OUTPUT PARAMETER rec-id AS INT.

create mhis-line.
mhis-line.nr = curr-nr. 
mhis-line.datum = m-list-datum. 
mhis-line.cost = m-list-cost. 
mhis-line.remark = remark-screen-value. 
FIND CURRENT mhis-line NO-LOCK.
rec-id = RECID(mhis-line).
