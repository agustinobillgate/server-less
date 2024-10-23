
DEF TEMP-TABLE t-h-artikel
    FIELD bezaendern    LIKE h-artikel.bezaendern
    FIELD epreis1       LIKE h-artikel.epreis1
    FIELD departement   LIKE h-artikel.departement
    FIELD aenderwunsch  LIKE h-artikel.aenderwunsch
    FIELD bondruckernr  LIKE h-artikel.bondruckernr
    FIELD betriebsnr    LIKE h-artikel.betriebsnr.

DEF INPUT  PARAMETER art-list-artnr AS INT.
DEF INPUT  PARAMETER dept           AS INT.
DEF OUTPUT PARAMETER param-172      AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

DEF VAR i AS INT.

FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = art-list-artnr 
    AND vhp.h-artikel.departement = dept NO-LOCK.
CREATE t-h-artikel.
ASSIGN
    t-h-artikel.bezaendern    = h-artikel.bezaendern
    t-h-artikel.epreis1       = h-artikel.epreis1
    t-h-artikel.departement   = h-artikel.departement
    t-h-artikel.aenderwunsch  = h-artikel.aenderwunsch
    t-h-artikel.betriebsnr    = h-artikel.betriebsnr.
DO i = 1 TO 4:
    t-h-artikel.bondruckernr[i]  = h-artikel.bondruckernr[i].
    i = i + 1.
END.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 172 NO-LOCK.
param-172 = htparam.fchar.
