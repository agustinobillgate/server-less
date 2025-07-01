DEFINE TEMP-TABLE output-list 
    FIELD from-time AS CHAR
    FIELD to-time AS CHAR
    FIELD room AS CHAR
    FIELD rsv-no AS INTEGER
    FIELD bezeich AS CHAR
    FIELD qty AS INTEGER
    FIELD price AS DECIMAL
    FIELD ba-status AS CHAR
    FIELD id AS CHAR.

DEFINE INPUT PARAMETER from-cr      LIKE bk-raum.raum.
DEFINE INPUT PARAMETER to-cr        LIKE bk-raum.raum.
DEFINE INPUT PARAMETER curr-date    AS DATE.
DEFINE OUTPUT PARAMETER from-i      AS INTEGER.
DEFINE OUTPUT PARAMETER to-i        AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE       FOR output-list.



FOR EACH output-list: 
  DELETE output-list. 
END. 

FOR EACH bk-rart WHERE bk-rart.raum GE from-cr AND bk-rart.raum LE to-cr 
  AND bk-rart.resstatus LE 2 NO-LOCK, 
  FIRST bk-reser WHERE bk-reser.veran-nr = bk-rart.veran-nr 
  AND bk-reser.veran-resnr = bk-rart.veran-resnr 
  AND bk-reser.datum = curr-date AND bk-reser.resstatus LE 2 
  USE-INDEX vernr-ix NO-LOCK: 
  from-i = bk-reser.von-i. 
  to-i = bk-reser.bis-i. 
  RUN create-string. 
END. 

PROCEDURE create-string: 
DEFINE VARIABLE status-chr AS CHAR FORMAT "x(10)". 
DEFINE BUFFER usrbuff FOR bediener. 
  IF bk-rart.resstatus = 1 THEN 
  DO: 
    status-chr = "Fix". 
  END. 
  ELSE 
  DO: 
    status-chr = "Tentative". 
  END. 
  FIND FIRST usrbuff WHERE usrbuff.nr = bk-rart.setup-id NO-LOCK NO-ERROR. 
  CREATE output-list. 
  ASSIGN
      output-list.from-time = STRING(bk-reser.von-zeit, "99:99")
      output-list.to-time = STRING(bk-reser.bis-zeit, "99:99")
      output-list.room = bk-rart.raum
      output-list.rsv-no = bk-rart.veran-nr
      output-list.bezeich = bk-rart.bezeich
      output-list.qty = bk-rart.anzahl
      output-list.price = bk-rart.preis
      output-list.ba-status = status-chr
      output-list.id = usrbuff.userinit.
END. 
