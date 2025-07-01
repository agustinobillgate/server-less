DEFINE TEMP-TABLE print-rc-list
    FIELD gastno          AS CHARACTER
    FIELD cr-usr          AS CHARACTER
    FIELD last-name       AS CHARACTER
    FIELD first-name      AS CHARACTER
    FIELD guest-title     AS CHARACTER
    FIELD room            AS CHARACTER
    FIELD room-no         AS CHARACTER
    FIELD room-price      AS CHARACTER
    FIELD arrival         AS CHARACTER
    FIELD departure       AS CHARACTER
    FIELD eta-flight      AS CHARACTER
    FIELD eta-time        AS CHARACTER
    FIELD etd-flight      AS CHARACTER
    FIELD etd-time        AS CHARACTER
    FIELD no-guest        AS CHARACTER
    FIELD purpose-stay    AS CHARACTER
    FIELD guest-address1  AS CHARACTER
    FIELD guest-address2  AS CHARACTER
    FIELD guest-address3  AS CHARACTER
    FIELD guest-country   AS CHARACTER
    FIELD guest-zip       AS CHARACTER
    FIELD guest-city      AS CHARACTER
    FIELD guest-nation    AS CHARACTER
    FIELD guest-province  AS CHARACTER
    FIELD guest-id        AS CHARACTER
    FIELD guest-email     AS CHARACTER
    FIELD birth-date      AS CHARACTER   
    FIELD company-name    AS CHARACTER
    FIELD rsv-addr1       AS CHARACTER
    FIELD rsv-addr2       AS CHARACTER
    FIELD rsv-addr3       AS CHARACTER
    FIELD rsv-country     AS CHARACTER
    FIELD rsv-city        AS CHARACTER
    FIELD rsv-zip         AS CHARACTER
    FIELD ccard           AS CHARACTER
    FIELD mobile-no       AS CHARACTER
    FIELD bill-instruct   AS CHARACTER
    FIELD birth-place     AS CHARACTER
    FIELD expired-id      AS CHARACTER
    FIELD resnr           AS CHARACTER
.

DEFINE TEMP-TABLE output-list   
  FIELD flag AS INTEGER INITIAL 0   
  FIELD STR AS CHAR FORMAT "x(68)"   
  FIELD str1 AS CHAR.  
  

DEFINE INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.  
DEFINE INPUT PARAMETER resno           AS INT  NO-UNDO.
DEFINE INPUT PARAMETER reslino         AS INT  NO-UNDO.
DEFINE INPUT PARAMETER gastno          AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER ct             AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER term-condition AS CHAR.
DEFINE OUTPUT PARAMETER gdpractivated  AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER newsactivated  AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER gdpr-flag      AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER euro-flag      AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER member-flag    AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER marketing-flag AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER newsletter-flag AS LOGICAL INIT NO.

DEFINE OUTPUT PARAMETER TABLE FOR print-rc-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.  


/*
DEFINE VARIABLE pvILanguage AS INTEGER.
DEFINE VARIABLE resno    AS INT  NO-UNDO INIT 21.
DEFINE VARIABLE reslino  AS INT  NO-UNDO INIT 1.
DEFINE VARIABLE gastno   AS INT  NO-UNDO INIT 12538.
DEFINE VARIABLE ct      AS CHAR NO-UNDO.
DEFINE VARIABLE term-condition AS CHAR.
*/

DEFINE VARIABLE temp-zimmerwusch    AS CHAR     NO-UNDO.
DEFINE VARIABLE zimmerwunsch        AS CHAR     NO-UNDO.
DEFINE VARIABLE anz                 AS INTEGER  NO-UNDO.
DEFINE VARIABLE WI-gastnr           AS INTEGER  NO-UNDO.
DEFINE VARIABLE IND-gastnr          AS INTEGER  NO-UNDO.
DEFINE VARIABLE cc-str              AS CHAR     NO-UNDO.
DEFINE VARIABLE cc-nr               AS CHAR     INITIAL ""  NO-UNDO.
DEFINE VARIABLE mm                  AS INTEGER  INITIAL 0   NO-UNDO.
DEFINE VARIABLE yy                  AS INTEGER  INITIAL 0   NO-UNDO.
DEFINE VARIABLE cc-valid            AS LOGICAL  INITIAL YES NO-UNDO.

DEFINE VARIABLE contcode        AS CHAR NO-UNDO.  
DEFINE VARIABLE tmp-str AS CHAR NO-UNDO.


DEFINE BUFFER rsvguest     FOR guest.

DEFINE VARIABLE bb          AS MEMPTR.
DEFINE VARIABLE image-data  AS CHAR.


/*
MESSAGE 
"pvILanguage " + string(pvILanguage) skip   
"resno       " + string(resno      ) skip   
"reslino     " + string(reslino    ) skip   
"gastno      " + string(gastno     ) VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
/* Get the signature */
FIND FIRST archieve WHERE archieve.KEY = "send-sign-rc" AND
    archieve.num1 = resno AND archieve.num2 = reslino AND
    archieve.num3 = gastno NO-LOCK NO-ERROR.
IF AVAILABLE archieve AND archieve.CHAR[2] NE "" THEN
    image-data = archieve.CHAR[2].

IF LENGTH(image-data) > 0 THEN
DO:
    SET-SIZE(bb) = 0.
    SET-SIZE(bb) = LENGTH(image-data).
    PUT-STRING(bb,1,LENGTH(image-data)) = image-data.

    ct = BASE64-ENCODE(bb).
END.

/* Get the data */
FIND FIRST res-line WHERE res-line.resnr = resno AND res-line.reslinnr = reslino NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    zimmerwunsch = res-line.zimmer-wunsch.
    CREATE print-rc-list.
    ASSIGN  print-rc-list.room-no       = STRING(res-line.zinr)
            print-rc-list.arrival       = STRING(res-line.ankunft, "99/99/9999")
            print-rc-list.departure     = STRING(res-line.abreise, "99/99/9999") + " " + STRING(res-line.abreisezeit,"HH:MM")
            print-rc-list.eta-flight    = SUBSTR(res-line.flight-nr, 1, 6)
            print-rc-list.eta-time      = SUBSTR(res-line.flight-nr,7,2) + ":" + SUBSTR(res-line.flight-nr,9,2)
            print-rc-list.etd-flight    = SUBSTR(res-line.flight-nr, 12, 6)
            print-rc-list.etd-time      = SUBSTR(res-line.flight-nr,18,2) + ":" + SUBSTR(res-line.flight-nr,20,2)
            print-rc-list.no-guest      = STRING(res-line.erwachs + res-line.gratis)
            print-rc-list.gastno        = STRING(res-line.gastnrmember).
            .
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
    IF AVAILABLE reservation AND reservation.useridanlage NE "" THEN
        cr-usr = reservation.useridanlage.

    print-rc-list.resnr = STRING(res-line.resnr).

    DO anz = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        temp-zimmerwusch = ENTRY(anz, res-line.zimmer-wunsch, ";").
        IF SUBSTR(temp-zimmerwusch,1,8) = "segm_pur" THEN 
        DO:
            print-rc-list.purpose-stay = SUBSTR(temp-zimmerwusch,9).
            FIND FIRST queasy WHERE queasy.KEY = 143 
                AND queasy.number1 = INTEGER(print-rc-list.purpose-stay) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy AND queasy.char3 NE "" THEN 
                print-rc-list.purpose-stay = queasy.char3.
            LEAVE.
        END.
    END.
    
    FIND FIRST queasy WHERE queasy.key = 9 AND 
        queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.char1 NE "" THEN 
        print-rc-list.bill-instruct = queasy.char1.  

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR. 
    IF AVAILABLE zimkateg THEN
        print-rc-list.room = zimkateg.kurzbez + " / " + STRING(vhp.res-line.zimmeranz). 

    /* guest detail */
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        ASSIGN  print-rc-list.last-name         = guest.NAME
                print-rc-list.first-name        = guest.vorname1 
                print-rc-list.guest-title       = guest.anrede1
                print-rc-list.guest-address1    = TRIM(guest.adresse1)
                print-rc-list.guest-address2    = TRIM(guest.adresse2)
                print-rc-list.guest-address3    = TRIM(guest.adresse3)
                print-rc-list.guest-country     = TRIM(guest.land)
                print-rc-list.guest-zip         = STRING(guest.plz)
                print-rc-list.guest-city        = TRIM(guest.wohnort)
                print-rc-list.guest-nation      = TRIM(guest.nation1)
                print-rc-list.guest-province    = TRIM(guest.geburt-ort2)
                print-rc-list.guest-id          = TRIM(guest.ausweis-nr1)
                print-rc-list.guest-email       = TRIM(guest.email-adr)
                print-rc-list.mobile-no         = STRING(guest.mobil-telefon,"x(16)")
                print-rc-list.birth-place       = STRING(guest.telex,"x(24)")
        .                              
        IF guest.geburtdatum1 NE ? THEN 
            print-rc-list.birth-date = STRING(guest.geburtdatum1,"99/99/9999").
        IF guest.geburtdatum2 NE ? THEN 
            print-rc-list.expired-id = STRING(guest.geburtdatum2,"99/99/9999").
            
        ASSIGN  cc-str = ENTRY(1, guest.ausweis-nr2, "|")
                cc-nr  = ENTRY(2, cc-str, "\")
                mm     = INTEGER(SUBSTR(ENTRY(3, cc-str, "\"),1,2)) 
                yy     = INTEGER(SUBSTR(ENTRY(3, cc-str, "\"),3)) 
                cc-nr  = cc-nr + ", " + SUBSTR(ENTRY(3, cc-str, "\"),1,2) + "/"
                        + SUBSTR(ENTRY(3, cc-str, "\"),3) NO-ERROR.

        IF cc-nr = "" THEN cc-valid = NO.
        IF cc-valid THEN 
            IF yy LT YEAR(TODAY) THEN cc-valid = NO.
        IF cc-valid THEN 
            IF (yy = YEAR(TODAY) AND mm LT MONTH(TODAY)) THEN cc-valid = NO.
        IF cc-valid THEN print-rc-list.ccard = cc-nr.
    END.

    /* reserve detail */
    FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK.
    WI-gastnr = htparam.finteger.
    FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK.
    IND-gastnr = htparam.finteger.
    FIND FIRST rsvguest WHERE rsvguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE rsvguest THEN
    DO:
        ASSIGN  print-rc-list.company-name      = STRING((rsvguest.NAME + ", " + rsvguest.anredefirma),"x(24)")
                print-rc-list.rsv-addr1         = TRIM(rsvguest.adresse1)
                print-rc-list.rsv-addr2         = TRIM(rsvguest.adresse2)
                print-rc-list.rsv-addr3         = TRIM(rsvguest.adresse3)
                print-rc-list.rsv-city          = TRIM(rsvguest.wohnort)
                print-rc-list.rsv-zip           = TRIM(rsvguest.plz)
                print-rc-list.rsv-country       = TRIM(rsvguest.land)
            .

        IF rsvguest.karteityp = 0 OR (rsvguest.gastnr = WI-gastnr OR rsvguest.gastnr = IND-gastnr) THEN 
            print-rc-list.room-price = TRIM(STRING(res-line.zipreis, ">>>,>>>,>>9.99")). 
        /*ELSE IF res-line.gastnrmember = res-line.gastnrpay THEN
            print-rc-list.room-price = TRIM(STRING(res-line.zipreis, ">>>,>>>,>>9.99")). 
*/
    END.

    /*FT serverless masukkan ke dalam if avaiable resline*/
        /* Get Term and Condition */    
    FIND FIRST htparam WHERE htparam.paramnr = 51 AND htparam.paramgr = 15 
        AND htparam.reihenfolge = 136 NO-LOCK NO-ERROR.
    
    IF AVAILABLE htparam THEN
    DO:
      FIND FIRST briefzei WHERE briefzei.briefnr = htparam.finteger NO-LOCK NO-ERROR.
      IF AVAILABLE briefzei THEN
      term-condition = briefzei.texte.
    END.
    
    
    /* Get stay cost*/
    contcode = "".  
    FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.   
    IF AVAILABLE guest-pr THEN   
    DO:  
        contcode = guest-pr.CODE.  
        tmp-str = res-line.zimmer-wunsch.  
        IF tmp-str MATCHES("*$CODE$*") THEN  
        DO:  
            tmp-str = SUBSTR(tmp-str,INDEX(tmp-str,"$CODE$") + 6).  
            contcode = SUBSTR(tmp-str, 1, INDEX(tmp-str,";") - 1).  
        END.  
    END.  
    
    /*Get MEMBER Flag*/
    FIND FIRST mc-guest WHERE mc-guest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN member-flag = YES.
    ELSE member-flag = NO.
    
    /*Get GDPR Flag*/
    DEFINE VARIABLE i        AS INT.
    DEFINE VARIABLE str      AS CHAR.
    DEFINE VARIABLE strgdpr  AS CHAR.
    DEFINE VARIABLE strmark  AS CHAR.
    DEFINE VARIABLE strnews  AS CHAR.
    DEFINE VARIABLE err-flag AS INT.
    
    FIND FIRST htparam WHERE paramnr = 346 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam AND htparam.bezeich NE "Not Used" THEN gdpractivated = htparam.flogical.
    ELSE gdpractivated = NO.
    
    IF gdpractivated THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(zimmerwunsch,";") - 1:
            str = ENTRY(i, zimmerwunsch, ";").
            IF SUBSTR(str,1,4) EQ "GDPR" THEN strgdpr = SUBSTR(str,5).
            /*IF SUBSTR(str,1,9) EQ "MARKETING" THEN strmark = SUBSTR(str,10).
            IF SUBSTR(str,1,10) EQ "NEWSLETTER" THEN strnews = SUBSTR(str,11).*/
        END.
    
    
        IF strgdpr = "YES" THEN gdpr-flag = YES.
        ELSE gdpr-flag = NO.
        /*IF strmark = "YES" THEN marketing-flag  = YES.
        ELSE marketing-flag  = NO.
        IF strnews = "YES" THEN newsletter-flag = YES.
        ELSE  newsletter-flag = NO.*/
    
        IF gdpr-flag EQ NO THEN
        DO:
            RUN checkin-gdprbl.p (gastno, OUTPUT err-flag).
            IF err-flag = 1 THEN 
            ASSIGN
                gdpr-flag = YES
                euro-flag = YES.
        END.
        IF gdpr-flag EQ YES THEN
        DO:
            euro-flag = YES.
            FIND FIRST res-line WHERE res-line.resnr EQ resno 
                AND res-line.reslinnr EQ reslino 
                AND res-line.gastnrmember EQ gastno EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN
            DO:
                IF NOT res-line.zimmer-wunsch MATCHES "*GDPR*" THEN 
                res-line.zimmer-wunsch = res-line.zimmer-wunsch + "GDPRyes;".
            END.
        END.
    END.
    ELSE
    DO:
        gdpr-flag = NO.
    END.
    
    FIND FIRST htparam WHERE paramnr = 477 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam AND htparam.bezeich NE "Not Used" THEN newsactivated = htparam.flogical.
    ELSE newsactivated = NO.
    
    IF newsactivated THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(zimmerwunsch,";") - 1:
            str = ENTRY(i, zimmerwunsch, ";").
            IF SUBSTR(str,1,9) EQ "MARKETING" THEN strmark = SUBSTR(str,10).
            IF SUBSTR(str,1,10) EQ "NEWSLETTER" THEN strnews = SUBSTR(str,11).
        END.
        IF strmark = "YES" THEN marketing-flag  = YES.
        ELSE marketing-flag  = NO.
        IF strnews = "YES" THEN newsletter-flag = YES.
        ELSE  newsletter-flag = NO.
    END.
    
    
    RUN view-staycostbl.p  
        (pvILanguage, resno, reslino, contcode, OUTPUT TABLE output-list).  
END.                                                     

