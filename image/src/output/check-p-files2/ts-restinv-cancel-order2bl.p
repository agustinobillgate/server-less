DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT PARAMETER rec-id-h-art AS INT.
DEF INPUT PARAMETER rec-id-hbline AS INT.
DEF OUTPUT PARAMETER answer AS LOGICAL.
DEF OUTPUT PARAMETER cancel-flag AS LOGICAL.
DEF OUTPUT PARAMETER billart AS INT.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER price AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

FIND FIRST h-bill-line WHERE RECID(h-bill-line) = rec-id-hbline.
answer = NO. 
cancel-flag = YES. 
DO: 
    FIND FIRST vhp.h-artikel WHERE RECID(vhp.h-artikel) = rec-id-h-art NO-LOCK. 
    billart = vhp.h-bill-line.artnr. 
    description = vhp.h-bill-line.bezeich. 
    price = vhp.h-bill-line.epreis. 
    /*MTRUN return-qty.*/
END.
CREATE t-h-artikel.
BUFFER-COPY h-artikel TO t-h-artikel.
ASSIGN t-h-artikel.rec-id = RECID(h-artikel).
