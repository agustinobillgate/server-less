
DEF INPUT PARAMETER rec-id              AS INT.
DEF INPUT PARAMETER potype              AS INT.
DEF INPUT PARAMETER cost-acct           AS CHAR.
DEF INPUT PARAMETER bez                 AS CHAR.
DEF INPUT PARAMETER billdate            AS DATE.
DEF INPUT PARAMETER bediener-username   AS CHAR.

FIND FIRST l-order WHERE RECID(l-order) = rec-id.
FIND CURRENT l-order EXCLUSIVE-LOCK. 
IF potype = 2 THEN l-order.stornogrund = STRING(cost-acct, "x(12)") + bez. 
l-order.lieferdatum = billdate. 
l-order.lief-fax[2] = bediener-username. 

FIND CURRENT l-order NO-LOCK.
