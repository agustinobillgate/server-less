DEFINE TEMP-TABLE bkrart LIKE bk-rart
    FIELD recid-bk-rart AS INT
    FIELD amount AS DECIMAL.

DEF INPUT  PARAMETER veran-nr           AS INT.
DEF INPUT  PARAMETER veran-seite        AS INT.
DEF INPUT  PARAMETER departement        AS INT.
DEF INPUT  PARAMETER q2-artnr           AS INT.
DEF INPUT  PARAMETER qty                AS INT.
DEF INPUT  PARAMETER bediener-nr        AS INT.
DEF INPUT  PARAMETER unit-price         AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR bkrart.

FIND FIRST artikel WHERE artikel.artnr = q2-artnr 
    AND artikel.departement = departement 
    AND artikel.activeflag = YES
    NO-LOCK.

FIND FIRST bk-reser WHERE bk-reser.veran-nr = veran-nr 
  AND bk-reser.veran-resnr = veran-seite NO-LOCK. 
FIND FIRST bk-func WHERE bk-func.veran-nr = veran-nr 
  AND bk-func.veran-seite = veran-seite 
  USE-INDEX vernr-pg-ix NO-LOCK. 
CREATE bk-rart. 
ASSIGN 
  bk-rart.veran-nr = bk-reser.veran-nr 
  bk-rart.veran-resnr = bk-func.veran-seite 
  bk-rart.veran-seite = bk-func.veran-seite 
  bk-rart.von-zeit = bk-reser.von-zeit 
  bk-rart.raum = bk-reser.raum 
  bk-rart.departement = departement 
  bk-rart.veran-artnr = artikel.artnr 
  bk-rart.bezeich = artikel.bezeich 
  bk-rart.anzahl = qty 
  bk-rart.resstatus = bk-reser.resstatus 
  bk-rart.zwkum = artikel.zwkum 
  bk-rart.setup-id = bediener-nr  
  bk-rart.preis = unit-price
.
FIND CURRENT bk-rart NO-LOCK. 

CREATE bkrart.
BUFFER-COPY bk-rart TO bkrart.
