
DEF INPUT  PARAMETER l-artikel-artnr AS INT.
DEF INPUT  PARAMETER curr-lager      AS INT.

DEF OUTPUT PARAMETER do-it           AS LOGICAL INIT NO.

FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel-artnr 
  AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR. 
IF AVAILABLE l-bestand AND (l-bestand.anz-anf-best NE 0 
OR l-bestand.anz-eingang NE 0 OR l-bestand.anz-ausgang NE 0) THEN 
    do-it = YES.
