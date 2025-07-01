DEFINE TEMP-TABLE best-list LIKE l-bestand
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER s-artnr    AS INT.
DEF INPUT  PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER error-code AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER fl-code    AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER TABLE FOR best-list.

FIND FIRST l-bestand WHERE l-bestand.artnr = s-artnr 
    AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR. 
IF AVAILABLE l-bestand THEN 
DO: 
    FIND FIRST l-op WHERE l-op.artnr = s-artnr 
      AND l-op.lager-nr = curr-lager NO-LOCK NO-ERROR. 
    IF AVAILABLE l-op THEN 
    DO: 
        fl-code = 1.
        error-code = 2.
        RETURN. 
    END. 
    FIND FIRST l-ophis WHERE l-ophis.artnr = s-artnr 
      AND l-ophis.lager-nr = curr-lager NO-LOCK NO-ERROR. 
    IF AVAILABLE l-ophis THEN 
    DO:
      fl-code = 2.
      error-code = 2. 
      RETURN. 
    END.

    fl-code = 3.
    CREATE best-list. 
    best-list.artnr = s-artnr. 
    best-list.anf-best-dat = l-bestand.anf-best-dat. 
    best-list.lager-nr = curr-lager. 
    best-list.anz-anf-best = l-bestand.anz-anf-best. 
    best-list.val-anf-best = l-bestand.val-anf-best. 
    best-list.betriebsnr = 1. 
    best-list.rec-id = RECID(l-bestand).
END.
