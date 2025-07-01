
DEF INPUT PARAMETER c-list-rechnr AS INT.
DEF INPUT PARAMETER c-list-dept AS INT.
DEF INPUT PARAMETER gname AS CHAR.

FIND FIRST h-bill WHERE h-bill.rechnr = c-list-rechnr
  AND h-bill.departement = c-list-dept NO-LOCK NO-ERROR. 
IF AVAILABLE h-bill THEN 
DO: 
  FIND CURRENT h-bill EXCLUSIVE-LOCK. 
  h-bill.bilname = gname.
  FIND CURRENT h-bill NO-LOCK. 
END. 
