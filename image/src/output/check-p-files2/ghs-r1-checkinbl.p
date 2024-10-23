DEFINE TEMP-TABLE r-list
    FIELD email         AS CHARACTER
    FIELD g-title       AS CHARACTER
    FIELD firstname     AS CHARACTER
    FIELD lastname      AS CHARACTER
    FIELD cardname      AS CHARACTER
    FIELD mobile        AS CHARACTER
    FIELD phone         AS CHARACTER
    FIELD postcode      AS CHARACTER
    FIELD fax           AS CHARACTER
    FIELD address1      AS CHARACTER
    FIELD address2      AS CHARACTER
    FIELD city          AS CHARACTER
    FIELD state         AS CHARACTER
    FIELD country       AS CHARACTER
    FIELD nationality   AS CHARACTER
    FIELD memberno      AS CHARACTER
    FIELD propID        AS CHARACTER
    FIELD profile       AS CHARACTER
    FIELD confno        AS CHARACTER
    FIELD note          AS CHARACTER
    FIELD passport      AS CHARACTER
    FIELD idcard        AS CHARACTER
    FIELD birthdate     AS CHARACTER
    FIELD gender        AS CHARACTER
    FIELD comp          AS CHARACTER
    FIELD compno        AS CHARACTER.

/*Irfan 21/02/18 add mapping country
DEFINE TEMP-TABLE nation 
    FIELD nr AS INTEGER
    FIELD nation-code AS CHAR
    FIELD nation-name AS CHAR
    FIELD nation-iso2 AS CHAR
    FIELD nation-iso3 AS CHAR.
*/
DEFINE INPUT PARAMETER datum AS DATE.
DEFINE INPUT PARAMETER propID AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR r-list.


FIND FIRST htparam WHERE paramnr = 87 NO-LOCK NO-ERROR.
/*DEFINE VARIABLE datum AS DATE.
datum = fdate - 1.
DEFINE VARIABLE propID AS CHAR INIT "A1".*/

DEFINE VARIABLE birthdate AS CHARACTER.

DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gcomp FOR guest.   

DEFINE STREAM s1.

/*
IF SEARCH("countrymapping.xml") NE ? THEN
    TEMP-TABLE nation:READ-XML("file",SEARCH("countrymapping.xml"),?,?,?).
*/

FOR EACH res-line WHERE 
    ((res-line.resstatus = 6 OR res-line.resstatus = 13) AND res-line.ankunft = datum) OR
    (res-line.resstatus = 8 AND res-line.active-flag = 2
    AND res-line.ankunft = datum AND res-line.abreise = datum) OR
    (res-line.resstatus NE 9 AND res-line.resstatus NE 99 AND res-line.resstatus NE 12
     AND res-line.resstatus NE 10 AND res-line.ankunft = datum AND datum LT htparam.fdate) NO-LOCK,
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK:
    IF AVAILABLE gmember THEN
    DO:
        CREATE r-list.
        ASSIGN
            r-list.email = gmember.email-adr
            r-list.g-title = gmember.anrede1
            r-list.firstname = gmember.vorname1
            r-list.lastname = gmember.NAME
            r-list.cardname = gmember.vorname1 + " " + gmember.NAME
            r-list.mobile = gmember.mobil-telefon
            r-list.phone = gmember.telefon
            r-list.postcode  = gmember.plz
            r-list.fax = gmember.fax
            r-list.address1 = gmember.adresse1
            r-list.address2 = gmember.adresse2
            r-list.city = gmember.wohnort
            r-list.state = gmember.geburt-ort2
            r-list.country = gmember.land
            r-list.nationality = gmember.nation1
            r-list.memberno = ""
            r-list.propID = propID
            r-list.profile = propID + "-" + STRING(gmember.gastnr)
            r-list.confno = propID + "-" + STRING(res-line.resnr) + STRING(res-line.reslinnr,"999")
            r-list.note = gmember.bemerkung.
            
        IF gmember.geburt-ort1 = "Passport" THEN
            r-list.passport = gmember.ausweis-nr1.
        ELSE r-list.idcard = gmember.ausweis-nr1.
        IF gmember.geburtdatum1 EQ ? THEN
          birthdate = "".
        ELSE
          birthdate = STRING(YEAR(gmember.geburtdatum1),"9999") + "-" +
                      STRING(MONTH(gmember.geburtdatum1),"99") + "-" +
                      STRING(DAY(gmember.geburtdatum1),"99").
        r-list.birthdate = birthdate.
        IF gmember.geschlecht = "M" THEN
            r-list.gender = "Male".
        ELSE IF gmember.geschlecht = "F" THEN
            r-list.gender = "Female".
        FIND FIRST gcomp WHERE gcomp.gastnr = gmember.master-gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE gcomp THEN
            ASSIGN
                r-list.comp = gcomp.name + ", " + gcomp.anredefirma
                r-list.compno = gcomp.telefon.

        /*
        FIND FIRST nation WHERE nation.nation-code EQ gmember.nation1 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN
        DO:
            ASSIGN
                nation-code         = nation.nation-iso2
                r-list.nationality  = nation-code
                r-list.country      = nation-code.
        END.
        */
    END.
END.
/*
DEFINE VARIABLE filenm AS CHARACTER INIT "c:\source10\GHS\r1_checkin_data.csv".

OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.
PUT STREAM s1 UNFORMATTED 
    "EMAIL,TITLE,GENDER,FIRSTNAME,LASTNAME,CARDNAME,BIRTHDAY,COMPANY,"
    "MOBILE_NUMBER,HOME_NUMBER,OFFICE_NUMBER,POST_CODE,FAX,ADDRESS1,"
    "ADDRESS2,CITY,STATE,COUNTRY,NATIONALITY,PASSPORT_ID,IDCARD_NUMBER,"
    "MEMBERSHIP_NO,PROPERTY_CODE,PROFILE_NO,CONFIRMATION_NO,NOTE" SKIP.
OUTPUT STREAM s1 CLOSE.

OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.  
    FOR EACH r-list:
        ASSIGN
            r-list.cardname = REPLACE(r-list.cardname,","," ")
            r-list.comp = REPLACE(r-list.comp,","," ")
            r-list.address1 = REPLACE(r-list.address1,","," ")
            r-list.address2 = REPLACE(r-list.address2,","," ").

        PUT STREAM s1 UNFORMATTED 
            r-list.email "," r-list.g-title "," r-list.gender "," r-list.firstname "," 
            r-list.lastname "," r-list.cardname "," r-list.birthdate "," r-list.comp ","
            r-list.mobile "," r-list.phone "," r-list.compno "," r-list.postcode "," 
            r-list.fax "," r-list.address1 "," r-list.address2 "," r-list.city ","
            r-list.state "," r-list.country "," r-list.nationality "," r-list.passport ","
            r-list.idcard "," r-list.memberno "," r-list.propId "," r-list.profile ","
            r-list.confno "," r-list.note SKIP.
  END.
OUTPUT STREAM s1 CLOSE.*/





