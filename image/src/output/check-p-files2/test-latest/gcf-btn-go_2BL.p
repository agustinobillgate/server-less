DEF TEMP-TABLE t-guest LIKE guest.

DEF INPUT PARAMETER icase         AS INTEGER NO-UNDO.
DEF INPUT PARAMETER pvILanguage   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER user-init     AS CHAR    NO-UNDO.
/*DEF INPUT PARAMETER ms-num        AS CHAR    NO-UNDO.*/
DEF INPUT PARAMETER refno4        AS CHAR    NO-UNDO.
DEF INPUT PARAMETER TABLE FOR t-guest.

DEF OUTPUT PARAMETER msg-str      AS CHAR    INIT "" NO-UNDO.
DEF OUTPUT PARAMETER error-number AS INTEGER INIT 0  NO-UNDO.

DEF VARIABLE gastno       AS INTEGER            NO-UNDO.
DEF VARIABLE def-natcode  AS CHAR               NO-UNDO.
DEF VARIABLE name-changed AS LOGICAL INITIAL NO NO-UNDO. 
DEF VARIABLE zugriff      AS LOGICAL. 

DEFINE VARIABLE priscilla-active AS LOGICAL INITIAL YES NO-UNDO.
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "chg-gcf0". 

DEFINE TEMP-TABLE tlist
    FIELD tfield AS CHAR
    FIELD tcount AS INT.

DEFINE VARIABLE i AS INT INIT 0.
DEFINE VARIABLE str AS CHAR INIT "".
DEFINE VARIABLE str1 AS CHAR INIT "".
DEFINE VARIABLE sum-i AS INT INIT 0.

/* validasi untuk vhpcloud CRG 05/02/2024) */
IF refno4 = ? THEN
    refno4 = "".

FIND FIRST htparam WHERE htparam.paramnr = 50 AND htparam.paramgr = 6 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.fchar NE "" THEN
DO i = 1 TO NUM-ENTRIES(htparam.fchar,";"):
    IF ENTRY(i,htparam.fchar,";") NE "" THEN
    DO:
        sum-i = sum-i + 1.
        CREATE tlist.
        ASSIGN 
            tlist.tfield = ENTRY(i,htparam.fchar,";")
            tlist.tcount = sum-i.
    END.  
END.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
FIND FIRST t-guest.
ASSIGN gastno = t-guest.gastnr.

FIND FIRST tlist NO-LOCK NO-ERROR.
IF AVAILABLE tlist AND t-guest.karteityp = 0 THEN
DO:
    FOR EACH tlist NO-LOCK:
        IF (tlist.tfield = "ttl" AND t-guest.anrede1 = "") OR
            (tlist.tfield = "dob" AND t-guest.geburtdatum1 = ?) OR
            (tlist.tfield = "sex" AND t-guest.geschlecht = "") OR
            (tlist.tfield = "adr" AND t-guest.adresse1 = "" AND t-guest.adresse2 = ""
             AND t-guest.adresse3 = "") THEN
        DO:
            error-number = 7.
        END.
        IF tlist.tfield = "ttl" THEN str1 = "Title".
        ELSE IF tlist.tfield = "dob" THEN str1 = "Birthdate".
        ELSE IF tlist.tfield = "sex" THEN str1 = "Sex".
        ELSE IF tlist.tfield = "adr" THEN str1 = "Address".
        IF tlist.tcount NE sum-i THEN
            str = str + str1 + ", ".
        ELSE str = SUBSTR(str,1,LENGTH(str) - 2) + " & "+ str1.
    END.
END.

IF error-number = 7 THEN
DO:
    msg-str = translateExtended( "Please fill all the mandatory fields in parameter number 50 (" + str + ")." , lvCAREA, "":U). 
    RETURN.
END.


IF icase = 2 THEN 
DO:    
   RUN update-record.
   IF name-changed THEN RUN update-gcfname.p(gastno).
   RETURN.
END.
ELSE IF icase = 3 THEN 
DO:    
   RUN new-record.
   RETURN.
END.

FIND FIRST htparam WHERE htparam.paramnr = 153 NO-LOCK. 
FIND FIRST nation WHERE nation.kurzbez = htparam.fchar. 
def-natcode = nation.kurzbez. 

IF icase = 1 THEN
DO: 
  FIND FIRST guestseg WHERE guestseg.gastnr = gastno NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE guestseg OR guestseg.segment = 0 THEN 
  DO: 
    IF AVAILABLE guestseg AND guestseg.segment = 0 THEN 
    DO: 
      FIND CURRENT guestseg EXCLUSIVE-LOCK. 
      DELETE guestseg. 
    END. 
    IF t-guest.karteityp GT 0 THEN
    DO:
      msg-str = translateExtended( "Guest segment not yet defined.", lvCAREA, "":U). 
      error-number = 1.
      RETURN.
    END.
  END.
END.

IF t-guest.NAME = "" THEN 
DO: 
  msg-str = translateExtended( "Name not defined yet.", lvCAREA, "":U). 
  error-number = 2. 
  RETURN.
END. 
  
IF t-guest.karteityp = 0 THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 961 NO-LOCK.
  IF htparam.feldtyp = 4 AND htparam.flogical THEN
  DO:
    IF TRIM(t-guest.anrede1) = "" THEN
    DO:
      msg-str = translateExtended( "Guest Title not yet defined.", lvCAREA, "":U). 
      error-number = 3.
      RETURN. 
    END.
  END.

  FIND FIRST nation WHERE nation.kurzbez = t-guest.nation1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE nation THEN 
  DO: 
    msg-str = translateExtended( "Nationality not yet defined.", lvCAREA, "":U). 
    error-number = 4.
    RETURN.
  END. 

  IF t-guest.land NE def-natcode AND t-guest.nation2 NE "" THEN 
  DO: 
    msg-str = translateExtended( "Local Region for local country only.", lvCAREA, "":U). 
    error-number = 5.
    RETURN.
  END. 
END.

FIND FIRST nation WHERE nation.kurzbez = t-guest.land NO-LOCK NO-ERROR. 
IF NOT AVAILABLE nation THEN 
DO: 
  msg-str = translateExtended( "Country not yet defined.", lvCAREA, "":U). 
  error-number = 6.
  RETURN.
END. 


IF t-guest.phonetik3 NE "" THEN 
DO: 
   FIND FIRST htparam WHERE paramnr = 1002 NO-LOCK. 
   IF htparam.flogical THEN 
   DO: 
     FIND FIRST akt-cust WHERE akt-cust.gastnr = t-guest.gastnr NO-LOCK NO-ERROR.
     IF NOT AVAILABLE akt-cust THEN
     DO:
         CREATE akt-cust. 
         ASSIGN 
             akt-cust.gastnr   = t-guest.gastnr
             akt-cust.c-init   = user-init 
             akt-cust.userinit = t-guest.phonetik3
         .
     END.
     ELSE
     DO:
         IF akt-cust.userinit = t-guest.phonetik3 THEN .
         ELSE
         DO:
            /* IF zugriff THEN          /wenni 22/7/2016/
             DO:*/
                 FIND CURRENT akt-cust EXCLUSIVE-LOCK.
                 ASSIGN
                   akt-cust.c-init   = user-init 
                   akt-cust.userinit = t-guest.phonetik3
                 .
                 FIND CURRENT akt-cust NO-LOCK.
         END.
       END.
    END.
END. 
/*END*/
ELSE 
DO: 
      FIND FIRST akt-cust WHERE akt-cust.gastnr = t-guest.gastnr 
          AND akt-cust.userinit = t-guest.phonetik3 EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE akt-cust THEN 
      DO: 
        DELETE akt-cust. 
        RELEASE akt-cust. 
      END. 
END. 


/*fadly 12/12/2018
IF ms-num NE "" THEN
DO:
    FIND FIRST mc-guest WHERE mc-guest.gastnr = t-guest.gastnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE mc-guest THEN
    CREATE mc-guest.
    ASSIGN
        mc-guest.gastnr  = t-guest.gastnr
        mc-guest.cardnum = ms-num.
END.
*/

/*Alder - Serverless - Issue 584 - Start*/
PROCEDURE update-record:
    FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        IF (t-guest.NAME NE guest.name) 
            OR (t-guest.vorname1 NE guest.vorname1)
            OR (t-guest.anrede1 NE guest.anrede1) 
            OR (t-guest.vornamekind[1] NE guest.vornamekind[1]) 
            OR (t-guest.kreditlimit NE guest.kreditlimit) THEN
        DO:
            name-changed = YES. 
            CREATE res-history. 
            ASSIGN 
              res-history.nr     = bediener.nr 
              res-history.datum  = TODAY 
              res-history.zeit   = TIME 
              res-history.action = "GuestFile".
            IF (t-guest.NAME NE guest.name) 
                OR (t-guest.vorname1 NE t-guest.vorname1)
                OR (t-guest.anrede1 NE guest.anrede1) THEN
                res-history.aenderung = "GuestCard: GastNo " + STRING(guest.gastnr) 
                    + " " + guest.NAME + "," + guest.vorname1 + " changed to " 
                    + t-guest.NAME + "," + t-guest.vorname1.
       
            IF t-guest.vornamekind[1] NE guest.vornamekind[1] THEN
            DO:
                IF res-history.aenderung NE "" THEN
                    res-history.aenderung = res-history.aenderung + "; ". 
                    res-history.aenderung = res-history.aenderung + "Changed Picture file from " + guest.vornamekind[1].
            END.
      
            IF t-guest.kreditlimit NE guest.kreditlimit THEN
            DO:
                IF res-history.aenderung NE "" THEN 
                    res-history.aenderung = res-history.aenderung + "; ".
                    res-history.aenderung = res-history.aenderung + "Credit Limit changed from"
                    + " " + STRING(guest.kreditlimit) + " TO " + STRING(t-guest.kreditlimit).
            END.
      
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.

        IF priscilla-active THEN
        DO:
            IF (t-guest.NAME NE guest.name) 
                OR (t-guest.vorname1 NE guest.vorname1)
                OR (t-guest.anrede1 NE guest.anrede1)     
                OR (t-guest.email-adr NE guest.email-adr) THEN
            DO:
                FOR EACH res-line WHERE res-line.gastnrmember = guest.gastnr
                    AND res-line.active-flag LE 1
                    AND res-line.resstatus NE 12
                    AND res-line.l-zuordnung[3] NE 1 NO-LOCK:
        
                    RUN intevent-1.p(9, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
                END.
            END.
        END.
      

        IF refno4 NE "" THEN DO:
            FIND FIRST queasy WHERE queasy.KEY = 231 AND queasy.number1 = gastno NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN 
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN queasy.char1 = refno4.
                FIND CURRENT queasy NO-LOCK.
            END.
            ELSE 
            DO:
                CREATE queasy.
                ASSIGN 
                    queasy.KEY     = 231
                    queasy.number1 = gastno
                    queasy.char1   = refno4.
            END.
        END.
  
        FIND CURRENT guest EXCLUSIVE-LOCK.
        BUFFER-COPY t-guest TO guest.
        FIND CURRENT guest NO-LOCK.
    END.
END PROCEDURE.
/*Alder - Serverless - Issue 584 - End*/

PROCEDURE new-record:
    FIND FIRST  guest WHERE guest.gastnr = gastno EXCLUSIVE-LOCK. 
    BUFFER-COPY t-guest TO guest.
    FIND CURRENT guest NO-LOCK.

    /* tambahan untuk ChronDigital GuestProfile Salesboard (CRG 14Sep23) */
    FIND FIRST htparam WHERE paramnr = 1023 NO-LOCK NO-ERROR. /* license salesboard */
    IF AVAILABLE htparam AND htparam.flogical = YES THEN
    DO:
        IF guest.karteityp GT 0 THEN RUN intevent-1.p(36, "", "newgcf", guest.gastnr, guest.karteityp).
    END.

    IF refno4 NE "" THEN DO:
        FIND FIRST queasy WHERE queasy.KEY = 231 AND queasy.number1 = gastno NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN 
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN queasy.char1 = refno4.
            FIND CURRENT queasy NO-LOCK.
        END.
        ELSE 
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY     = 231
                queasy.number1 = gastno
                queasy.char1   = refno4.
        END.
    END.
END.
