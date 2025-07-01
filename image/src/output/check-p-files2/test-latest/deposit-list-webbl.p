  
DEFINE TEMP-TABLE output-list 
  FIELD gname AS CHAR
  FIELD resno AS INT
  FIELD deposit AS DECIMAL
  FIELD payment AS DECIMAL
  FIELD limit AS DATE. 

DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE INPUT PARAMETER sorttype AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  FOR EACH bk-veran WHERE bk-veran.limit-date GE from-date AND bk-veran.limit-date LE to-date 
    USE-INDEX limitdate_ix NO-LOCK, 
    FIRST guest WHERE guest.gastnr = bk-veran.gastnr USE-INDEX gastnr_index NO-LOCK : 
    IF sorttype = 0 THEN 
    DO: 
      IF bk-veran.total-paid LT bk-veran.deposit THEN 
      DO: 
        RUN create-output-list. 
      END. 
    END. 
    ELSE IF sorttype = 1 THEN 
    DO: 
      IF bk-veran.total-paid GE bk-veran.deposit THEN 
      DO: 
        RUN create-output-list. 
      END. 
    END. 
  END. 
 
PROCEDURE create-output-list: 
  CREATE output-list. 
  ASSIGN
      output-list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
      output-list.resno = bk-veran.veran-nr
      output-list.deposit = bk-veran.deposit
      output-list.payment = bk-veran.total-paid
      output-list.limit = bk-veran.limit-date.
END. 
 
