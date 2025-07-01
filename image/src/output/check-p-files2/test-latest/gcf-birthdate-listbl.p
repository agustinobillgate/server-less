DEFINE TEMP-TABLE birth-list 
  FIELD NAME        AS CHAR FORMAT "x(36)" 
  FIELD geburtdatum AS DATE FORMAT "99/99/9999" 
  FIELD ankunft1    AS DATE 
  FIELD abreise1    AS DATE 
  FIELD zinr        LIKE zimmer.zinr
  FIELD adresse     AS CHAR FORMAT "x(40)" 
  FIELD wohnort     AS CHAR FORMAT "x(32)". 

DEFINE TEMP-TABLE birth-list2 
  FIELD NAME           AS CHAR FORMAT "x(36)" 
  FIELD geburtdatum    AS DATE FORMAT "99/99/9999" 
  FIELD ankunft1       AS DATE 
  FIELD abreise1       AS DATE 
  FIELD zinr           LIKE zimmer.zinr
  FIELD adresse        AS CHAR FORMAT "x(40)" 
  FIELD wohnort        AS CHAR FORMAT "x(32)"
  FIELD telefon        AS CHAR FORMAT "x(30)"
  FIELD mobil-telefon  AS CHAR FORMAT "x(30)"
  FIELD email-addr     AS CHAR FORMAT "x(60)".

DEF INPUT PARAMETER from-mm   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-dd   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER to-mm     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER to-dd     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-age  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER to-age    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER sorttype  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR birth-list2.

DEFINE VARIABLE from-date   AS INTEGER NO-UNDO.
DEFINE VARIABLE to-date     AS INTEGER NO-UNDO.

from-date = from-mm * 100 + from-dd. 
IF from-mm LE to-mm THEN to-date = to-mm * 100 + to-dd. 
ELSE to-date = (to-mm + 12) * 100 + to-dd.

RUN gcf-birthdatebl.p(from-date, to-date, from-age, to-age, sorttype, 
                      OUTPUT TABLE birth-list).

FOR EACH birth-list2.
    DELETE birth-list2.
END.

FOR EACH birth-list:
  CREATE birth-list2.
  ASSIGN
      birth-list2.name          = birth-list.name       
      birth-list2.geburtdatum   = birth-list.geburtdatum 
      birth-list2.ankunft1      = birth-list.ankunft1    
      birth-list2.abreise1      = birth-list.abreise1    
      birth-list2.zinr          = birth-list.zinr        
      birth-list2.adresse       = ENTRY(1,birth-list.adresse,CHR(3))     
      birth-list2.wohnort       = birth-list.wohnort.
  IF NUM-ENTRIES(birth-list.adresse,CHR(3)) GT 1 THEN DO:
      birth-list2.email-addr    = ENTRY(2,birth-list.adresse,CHR(3)). 
      IF NUM-ENTRIES(birth-list.adresse,CHR(3)) GT 2 THEN DO:
         birth-list2.telefon    = ENTRY(3,birth-list.adresse,CHR(3)). 
         birth-list2.mobil-telefon = ENTRY(4,birth-list.adresse,CHR(3)). 
      END.
  END.         
END.

