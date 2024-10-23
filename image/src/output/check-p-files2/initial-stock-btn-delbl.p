
DEF INPUT PARAMETER best-list-artnr AS INT.
DEF INPUT PARAMETER best-list-lager-nr AS INT.
DEF INPUT PARAMETER best-list-anz-anf-best LIKE l-bestand.anz-anf-best.
DEF INPUT PARAMETER best-list-val-anf-best LIKE l-bestand.val-anf-best.

FIND FIRST l-bestand WHERE l-bestand.artnr = best-list-artnr 
  AND l-bestand.lager-nr = 0 EXCLUSIVE-LOCK. 
ASSIGN 
  l-bestand.anz-anf-best = l-bestand.anz-anf-best - 
    best-list-anz-anf-best 
  l-bestand.val-anf-best = l-bestand.val-anf-best - 
    best-list-val-anf-best. 
FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
  EXCLUSIVE-LOCK. 
IF l-bestand.anz-anf-best NE 0 THEN 
DO: 
 l-artikel.vk-preis = l-bestand.val-anf-best / l-bestand.anz-anf-best. 
END. 
ELSE l-artikel.vk-preis = 0. 
FIND CURRENT l-artikel NO-LOCK. 
FIND FIRST l-bestand WHERE l-bestand.artnr = best-list-artnr 
AND l-bestand.lager-nr = best-list-lager-nr EXCLUSIVE-LOCK. 
DELETE l-bestand.
