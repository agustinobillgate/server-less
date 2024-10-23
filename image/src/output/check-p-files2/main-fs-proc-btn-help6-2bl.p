
DEF INPUT  PARAMETER fsl-veran-nr AS INT.
DEF INPUT  PARAMETER fsl-veran-seite AS INT.
DEF INPUT  PARAMETER zwkum-zknr AS INT.
DEF OUTPUT PARAMETER STR AS CHAR.

FOR EACH bk-rart WHERE bk-rart.veran-nr = fsl-veran-nr AND bk-rart.veran-seite = fsl-veran-seite 
    AND bk-rart.zwkum = zwkum-zknr USE-INDEX nr-pg-ug-ix NO-LOCK: 
    RUN create-p2-str(INPUT-OUTPUT STR). 
END. 


PROCEDURE create-p2-str: 
DEFINE INPUT-OUTPUT PARAMETER STR AS CHAR FORMAT "x(400)". 
  IF STR = "" THEN 
  DO: 
    IF bk-rart.preis = 0 THEN 
      STR = STRING(bk-rart.anzahl) + " " + bk-rart.bezeich. 
    ELSE 
      STR = STRING(bk-rart.anzahl) + " " + bk-rart.bezeich + " " + STRING(bk-rart.preis,">,>>>,>>>"). 
  END. 
  ELSE 
  DO: 
    IF bk-rart.preis = 0 THEN 
      STR = STR + ", " + STRING(bk-rart.anzahl) + " " + bk-rart.bezeich. 
    ELSE 
      STR = STR + ", " + STRING(bk-rart.anzahl) + " " + bk-rart.bezeich + " " + STRING(bk-rart.preis,">,>>>,>>>"). 
  END. 
END. 
