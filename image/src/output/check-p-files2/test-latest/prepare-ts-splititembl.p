
DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER h-recid            AS INTEGER.

DEF OUTPUT PARAMETER price-decimal      AS INTEGER.
DEF OUTPUT PARAMETER double-currency    AS LOGICAL.
DEF OUTPUT PARAMETER curr-qty           AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK. 
price-decimal = vhp.htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST vhp.htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = vhp.htparam.flogical. 
 
FIND FIRST vhp.h-bill-line WHERE RECID(vhp.h-bill-line) = h-recid NO-LOCK. 
curr-qty = vhp.h-bill-line.anzahl.
CREATE t-h-bill-line.
BUFFER-COPY h-bill-line TO t-h-bill-line.
ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).
