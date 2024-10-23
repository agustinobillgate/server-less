DEFINE TEMP-TABLE birth-list 
  FIELD company     AS CHAR FORMAT "x(30)"
  FIELD NAME        AS CHAR FORMAT "x(36)" 
  FIELD geburtdatum AS DATE FORMAT "99/99/9999" 
  FIELD geburt-ort1 AS CHAR FORMAT "x(28)"
  FIELD telephone   AS CHAR FORMAT "x(25)"
  FIELD email       AS CHAR FORMAT "x(40)"
.

DEFINE INPUT PARAMETER from-mm AS INTEGER.
DEFINE INPUT PARAMETER from-dd AS INTEGER.
DEFINE INPUT PARAMETER to-mm AS INTEGER.
DEFINE INPUT PARAMETER to-dd AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR birth-list.


DEFINE VARIABLE from-date AS INTEGER. 
DEFINE VARIABLE to-date AS INTEGER. 
DEFINE VARIABLE count AS INTEGER INITIAL 0. 
DEFINE VARIABLE stopped AS LOGICAL INITIAL NO. 
  from-date = from-mm * 100 + from-dd. 
  IF from-mm LE to-mm THEN to-date = to-mm * 100 + to-dd. 
  ELSE to-date = (to-mm + 12) * 100 + to-dd. 
  FOR EACH birth-list: 
    DELETE birth-list. 
  END. 
  
  FOR EACH guest WHERE karteityp = 1 NO-LOCK USE-INDEX ganame_index,
      FIRST bk-veran WHERE bk-veran.gastnr = guest.gastnr NO-LOCK,
      FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr :
      
      IF (month(akt-kont.geburtdatum1) * 100 + day(akt-kont.geburtdatum1)) GE from-date 
          AND (month(akt-kont.geburtdatum1) * 100 + day(akt-kont.geburtdatum1)) LE to-date THEN 
        DO: 
          create birth-list. 
          ASSIGN
          birth-list.company = guest.NAME
          birth-list.name = akt-kont.name + ", " + akt-kont.vorname 
                  + " " + akt-kont.anrede 
          birth-list.geburtdatum = akt-kont.geburtdatum1
          birth-list.geburt-ort1 = akt-kont.geburt-ort1
          birth-list.telephone   = akt-kont.telefon
          birth-list.email       = akt-kont.email-adr.
        END. 
  END.
