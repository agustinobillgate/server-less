
DEF INPUT  PARAMETER rec-id      AS INT.
DEF INPUT  PARAMETER dept        AS INT.
DEF OUTPUT PARAMETER it-exist    AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER selected-nr AS INT.
DEF OUTPUT PARAMETER anzahl      AS INT.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
RUN check-discArt.

FOR EACH vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
    AND vhp.h-artikel.artart = 12 NO-LOCK:
    selected-nr = vhp.h-artikel.artnr.
    anzahl = anzahl + 1.
END.

PROCEDURE check-discArt:
DEF VARIABLE disc-art AS INTEGER.
DEF VARIABLE disc-val AS DECIMAL INITIAL 0.
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 557 NO-LOCK.
  disc-art = vhp.htparam.finteger.
  IF disc-art NE 0 THEN
  DO:
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
      AND vhp.h-bill-line.departement = dept 
      AND vhp.h-bill-line.artnr = disc-art NO-LOCK:
      disc-val = disc-val + vhp.h-bill-line.betrag.
    END.
    IF disc-val GE 1 OR disc-val LE -1 THEN it-exist = YES.
  END.
END.

