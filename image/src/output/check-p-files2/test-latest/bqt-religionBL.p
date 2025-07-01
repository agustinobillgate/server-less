DEFINE TEMP-TABLE religion 
  FIELD gastnr      AS INT
  FIELD company     AS CHAR FORMAT "x(30)" COLUMN-LABEL "Company Name"
  FIELD NAME        AS CHAR FORMAT "x(40)" COLUMN-LABEL "Name, First Name, Title"
  FIELD pers-bez    AS CHAR FORMAT "x(24)" COLUMN-LABEL "Religion"
  FIELD telephone   AS CHAR FORMAT "x(30)" COLUMN-LABEL "Telephone"
  FIELD email       AS CHAR FORMAT "x(45)" COLUMN-LABEL "Email"
.

DEFINE INPUT PARAMETER INT AS INTEGER.
DEFINE INPUT PARAMETER from-mm AS INTEGER.
DEFINE INPUT PARAMETER from-dd AS INTEGER.
DEFINE INPUT PARAMETER to-mm AS INTEGER.
DEFINE INPUT PARAMETER to-dd AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR religion.

DEFINE VARIABLE from-date AS INTEGER. 
DEFINE VARIABLE to-date AS INTEGER. 
DEFINE VARIABLE count AS INTEGER INITIAL 0. 
DEFINE VARIABLE stopped AS LOGICAL INITIAL NO. 
  from-date = from-mm * 100 + from-dd. 
  IF from-mm LE to-mm THEN to-date = to-mm * 100 + to-dd. 
  ELSE to-date = (to-mm + 12) * 100 + to-dd. 
  FOR EACH religion: 
    DELETE religion. 
  END. 
 
IF INT NE 0 THEN
DO:
    FOR EACH guest WHERE karteityp = 1 NO-LOCK USE-INDEX ganame_index,
      FIRST bk-veran WHERE bk-veran.gastnr =  guest.gastnr  NO-LOCK:
      DO:
          FOR EACH akt-kont WHERE akt-kont.gastnr = guest.gastnr 
              AND akt-kont.pers-bez = INT NO-LOCK:
             
                CREATE religion. 
                ASSIGN
                religion.gastnr      = guest.gastnr
                religion.company     = guest.NAME 
                religion.name        = akt-kont.name + ", " + akt-kont.vorname 
                                   + " " + akt-kont.anrede 
                religion.telephone   = akt-kont.telefon
                religion.email       = akt-kont.email-adr.
            
                FIND FIRST queasy WHERE queasy.KEY = 149 AND queasy.char1 = STRING(akt-kont.pers-bez) NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                    religion.pers-bez = queasy.char3.
                ELSE.

          END.
     END. 
  END.
END.
ELSE
DO:
    FOR EACH guest WHERE karteityp = 1 NO-LOCK USE-INDEX ganame_index,
      FIRST bk-veran WHERE bk-veran.gastnr =  guest.gastnr  NO-LOCK:
      DO:
          FOR EACH akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK:
             
                CREATE religion. 
                ASSIGN
                religion.gastnr      = guest.gastnr
                religion.company     = guest.NAME 
                religion.name        = akt-kont.name + ", " + akt-kont.vorname 
                                   + " " + akt-kont.anrede 
                religion.telephone   = akt-kont.telefon
                religion.email       = akt-kont.email-adr.
            
                FIND FIRST queasy WHERE queasy.KEY = 149 AND queasy.char1 = STRING(akt-kont.pers-bez) NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                    religion.pers-bez = queasy.char3.
                ELSE.

          END.
     END. 
  END.
END.
