
DEF INPUT PARAMETER t-recid AS INT.

FIND FIRST l-order WHERE RECID(l-order) = t-recid NO-LOCK NO-ERROR.
DO transaction: 
    FIND CURRENT l-order EXCLUSIVE-LOCK.
    delete l-order. 
    RELEASE l-order.
END. 
