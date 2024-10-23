
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER nr AS INT.

FIND FIRST prtable WHERE RECID(prtable) = rec-id EXCLUSIVE-LOCK.
DELETE prtable.

FOR EACH queasy WHERE queasy.key = 18 
    AND queasy.number1 = nr EXCLUSIVE-LOCK: 
    DELETE queasy. 
END.

FIND FIRST prmarket WHERE prmarket.nr = nr EXCLUSIVE-LOCK.
delete prmarket.
