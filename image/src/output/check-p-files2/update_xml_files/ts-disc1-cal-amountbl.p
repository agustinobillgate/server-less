
DEF TEMP-TABLE t-h-artikel
    FIELD mwst          LIKE h-artikel.mwst
    FIELD service       LIKE h-artikel.service
    FIELD artnr         LIKE h-artikel.artnr
    FIELD bezeich       LIKE h-artikel.bezeich
    FIELD service-code  LIKE h-artikel.service-code
    FIELD mwst-code     LIKE h-artikel.mwst-code.

DEF TEMP-TABLE t-artikel
    FIELD umsatzart     LIKE artikel.umsatzart.

DEF INPUT PARAMETER menu-artnr AS INT.
DEF INPUT PARAMETER menu-departement AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = menu-artnr 
  AND vhp.h-artikel.departement = menu-departement NO-LOCK.  
FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront 
  AND vhp.artikel.departement = vhp.h-artikel.departement NO-LOCK.
CREATE t-h-artikel.
ASSIGN
    t-h-artikel.mwst          = h-artikel.mwst-code                        /* Rulita 040225 | Fixing serverless issue git 518 */
    t-h-artikel.service       = h-artikel.service-code                     /* Rulita 040225 | Fixing serverless issue git 518 */
    t-h-artikel.artnr         = h-artikel.artnr
    t-h-artikel.bezeich       = h-artikel.bezeich
    t-h-artikel.service-code  = h-artikel.service-code
    t-h-artikel.mwst-code     = h-artikel.mwst-code.

CREATE t-artikel.
ASSIGN t-artikel.umsatzart    = artikel.umsatzart.
