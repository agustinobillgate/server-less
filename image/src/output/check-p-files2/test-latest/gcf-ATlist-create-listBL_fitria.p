DEFINE TEMP-TABLE s-list 
  FIELD ktype   AS INTEGER 
  FIELD gastnr  AS INTEGER 
  FIELD segm    AS INTEGER FORMAT ">>>9" COLUMN-LABEL "Main!Segm" 
  FIELD code    AS CHAR FORMAT "x(15)"   LABEL "Segm" 
  FIELD name    AS CHAR FORMAT "x(30)"   LABEL "Company Name" 
  FIELD kname   AS CHAR FORMAT "x(24)"   LABEL "Contact Person" 
  FIELD phone   AS CHAR FORMAT "x(16)"   LABEL "Phone" 
  FIELD fax     AS CHAR FORMAT "x(16)"   LABEL "Fax" 
  FIELD adresse AS CHAR FORMAT "x(44)"   LABEL "Address" 
  FIELD city    AS CHAR FORMAT "x(16)"   LABEL "City" 
  FIELD land    AS CHAR FORMAT "x(3)"    LABEL "Ctry" 
  FIELD zip     AS CHAR FORMAT "x(7)"    COLUMN-LABEL "ZipCode" 
  FIELD sales   AS CHAR FORMAT "x(12)"   COLUMN-LABEL "Sales!In Charge" 
  FIELD email   AS CHAR FORMAT "x(32)"   COLUMN-LABEL "Email Address" 

  FIELD guest-pr-code  LIKE guest-pr.code
  FIELD avail-guest-pr AS LOGICAL INIT NO
  FIELD flag           AS INT INIT 0
  FIELD segmbez AS CHAR FORMAT "x(20)"   LABEL "Segmgrup description" /*william 20/02/24 543114*/
.            

DEFINE VARIABLE sflag AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR s-list.
FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK NO-ERROR.
IF htparam.feldtyp = 4 AND htparam.flogical THEN sflag = 1.
ELSE sflag = 2.

RUN create-list.

PROCEDURE create-list: 
DEFINE buffer bediener1 FOR bediener. 
  FOR EACH guest WHERE guest.karteityp GE 1 AND guest.gastnr GT 0 
      NO-LOCK BY guest.name: 
      

      CREATE s-list.
      ASSIGN
        s-list.ktype = guest.karteityp
        s-list.gastnr = guest.gastnr
        s-list.name = guest.NAME
        s-list.phone = guest.telefon 
        s-list.fax = guest.fax
        s-list.adresse = guest.adresse1 
        s-list.city = guest.wohnort
        s-list.land = guest.land
        s-list.zip = guest.plz
      . 
      FOR EACH akt-kont WHERE akt-kont.gastnr = guest.gastnr 
        AND SUBSTR(akt-kont.abteilung,1,3) NE "Acc" BY akt-kont.hauptkontakt DESC:
        s-list.kname = akt-kont.name. 
        IF akt-kont.vorname NE "" THEN 
        DO: 
          IF s-list.kname = "" THEN s-list.kname = akt-kont.vorname. 
          ELSE s-list.kname = s-list.kname + ", " + akt-kont.vorname. 
        END. 
        LEAVE.
      END.
      IF s-list.kname = "" THEN
      DO:
        FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
        IF AVAILABLE akt-kont THEN 
        DO: 
          s-list.kname = akt-kont.name. 
          IF akt-kont.vorname NE "" THEN 
          DO: 
            IF s-list.kname = "" THEN s-list.kname = akt-kont.vorname. 
            ELSE s-list.kname = s-list.kname + ", " + akt-kont.vorname. 
          END. 
        END. 
      END.

      FOR EACH guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK BY guestseg.reihenfolge DESC:
        FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK. 
        s-list.segm = segment.segmentgrup. 
        s-list.code = ENTRY(1, segment.bezeich, "$$0"). 
        FIND FIRST queasy WHERE queasy.key = 26 AND queasy.number1 EQ s-list.segm NO-LOCK NO-ERROR.
        s-list.segmbez = queasy.char3.
        LEAVE.
      END.

      /*FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr 
        AND SUBSTR(akt-kont.abteilung,1,3) NE "Acc" 
        AND akt-kont.hauptkontakt NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE akt-kont THEN 
      FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr 
        AND SUBSTR(akt-kont.abteilung,1,3) NE "Acc" NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE akt-kont THEN 
      FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr NO-LOCK NO-ERROR. 

      IF AVAILABLE akt-kont THEN 
      DO: 
        s-list.kname = akt-kont.name. 
        IF akt-kont.vorname NE "" THEN 
        DO: 
          IF s-list.kname = "" THEN s-list.kname = akt-kont.vorname. 
          ELSE s-list.kname = s-list.kname + ", " + akt-kont.vorname. 
        END. 
      END. 
      FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
      AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE guestseg THEN 
      FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
      IF AVAILABLE guestseg THEN 
      DO: 
        FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
          NO-LOCK. 
        s-list.segm = segment.segmentgrup. 
        s-list.code = ENTRY(1, segment.bezeich, "$$0"). 
        FIND FIRST queasy WHERE queasy.key = 26 AND queasy.number1 EQ s-list.segm NO-LOCK NO-ERROR.
        s-list.segmbez = queasy.char3. /*william 20/02/24 543114*/
      END. */
      IF guest.adresse2 NE "" THEN s-list.adresse 
        = s-list.adresse + " " + guest.adresse2. 
      IF guest.phonetik3 NE "" THEN 
      DO: 
        FIND FIRST bediener1 WHERE bediener1.userinit = guest.phonetik3 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener1 THEN s-list.sales = bediener1.username. 
      END. 
      s-list.email = guest.email-adr.                                         /* Rulita 170225 | Fixing serverless from guest.email to guest.email-adr issue git 604 */

      FIND FIRST guest-pr WHERE guest-pr.gastnr = s-list.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest-pr THEN
      DO:
          ASSIGN
          s-list.guest-pr-code  = guest-pr.code
          s-list.avail-guest-pr = YES
          s-list.flag = sflag.
      END.
  END. 
END. 
