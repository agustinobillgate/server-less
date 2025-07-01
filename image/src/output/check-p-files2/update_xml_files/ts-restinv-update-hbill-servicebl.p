
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER str    AS CHAR.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
ASSIGN vhp.h-bill.service[5] = DECIMAL(str).
