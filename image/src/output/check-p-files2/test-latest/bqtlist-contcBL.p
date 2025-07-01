 
DEFINE TEMP-TABLE t-out
     FIELD gastnr       LIKE akt-kont.gastnr
     FIELD company      AS CHAR FORMAT "x(30)"      COLUMN-LABEL "Company"
     FIELD anrede       LIKE akt-kont.anrede        FORMAT "x(5)"
     FIELD vorname      LIKE akt-kont.vorname       FORMAT "x(15)"
     FIELD NAME         LIKE akt-kont.NAME          FORMAT "x(20)"
     FIELD abteilung    LIKE akt-kont.abteilung     COLUMN-LABEL "Department"
     FIELD religion      AS CHAR FORMAT "x(10)"     COLUMN-LABEL "Religion"
     FIELD geburtdatum1 LIKE akt-kont.geburtdatum1  
     FIELD telefon      LIKE akt-kont.telefon       COLUMN-LABEL "Telephone"
     FIELD durchwahl    LIKE akt-kont.durchwahl     COLUMN-LABEL "Ext"
     FIELD email-adr    LIKE akt-kont.email-adr     COLUMN-LABEL "Email Address"
     .
 
DEFINE OUTPUT PARAMETER TABLE FOR t-out.


  FOR EACH  t-out: 
    DELETE  t-out. 
  END. 

  FOR EACH guest WHERE karteityp = 1 NO-LOCK USE-INDEX ganame_index,
      FIRST bk-veran WHERE bk-veran.gastnr = guest.gastnr NO-LOCK,
      FIRST akt-kont WHERE guest.gastnr = akt-kont.gastnr NO-LOCK:
      IF AVAILABLE guest THEN
      DO:
          CREATE t-out.
          ASSIGN
          t-out.gastnr          = akt-kont.gastnr
          t-out.company         = guest.NAME
          t-out.anrede          = akt-kont.anrede
          t-out.vorname         = akt-kont.vorname
          t-out.NAME            = akt-kont.NAME
          t-out.abteilung       = akt-kont.abteilung
          t-out.geburtdatum1    = akt-kont.geburtdatum1 
          t-out.telefon         = akt-kont.telefon
          t-out.durchwahl       = akt-kont.durchwahl
          t-out.email-adr       = akt-kont.email-adr
            .
      END.
      FIND FIRST queasy WHERE queasy.KEY = 149 AND INT(queasy.char1) = akt-kont.pers-bez NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
          t-out.religion        = queasy.char3.
      END.
  END.
