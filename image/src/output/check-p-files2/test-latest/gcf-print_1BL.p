DEFINE TEMP-TABLE output-list 
  FIELD STR AS CHAR. 

DEFINE TEMP-TABLE gcf-print2 LIKE guest
    FIELD rateCode      AS CHAR FORMAT "x(64)"
    FIELD memberno      AS CHAR FORMAT "x(24)"
    FIELD membertype    AS CHAR FORMAT "x(24)"
    FIELD count-num     AS INTEGER
    FIELD segment       AS CHAR FORMAT "X(16)". /*william*/


DEFINE INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fl-list     AS LOGICAL.
DEFINE INPUT PARAMETER city        AS CHAR.
DEFINE INPUT PARAMETER sorttype    AS INTEGER.
DEFINE INPUT PARAMETER from-name   AS CHAR.
DEFINE INPUT PARAMETER to-name     AS CHAR.
DEFINE INPUT PARAMETER segm-all    AS LOGICAL.
DEFINE INPUT PARAMETER paytype     AS INTEGER.
DEFINE INPUT PARAMETER PRtype      AS INTEGER.
DEFINE INPUT PARAMETER fl-email    AS LOGICAL.
DEFINE INPUT PARAMETER segmentcode AS INTEGER.
DEFINE INPUT PARAMETER fdate       AS DATE.     /*FD September 18, 2020*/
DEFINE INPUT PARAMETER tdate       AS DATE.     /*FD September 18, 2020*/
DEFINE INPUT PARAMETER fl-mcid     AS LOGICAL.  /*FD April 26, 2021*/
DEFINE INPUT PARAMETER prov        AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR gcf-print2.
DEFINE OUTPUT PARAMETER anzahl      AS INTEGER NO-UNDO INITIAL 0.
    
{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "gcf-print".

/************** MAIN LOGIC **************/
IF fl-list THEN RUN create-gcflist1.
ELSE RUN create-gcflist.

/************** PROCEDURE **************/
PROCEDURE create-gcflist: 
DEFINE VARIABLE str1 AS CHAR FORMAT "x(110)". 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE buffer guest1 FOR guest. 
DEFINE VARIABLE to-city AS CHAR INITIAL "zzz". 
 
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
 
  IF city NE "" THEN 
  DO: 
    to-city = city. 
  END. 
 
  FOR EACH guest WHERE gastnr GT 0 AND karteityp = sorttype 
    AND guest.name GE from-name AND guest.name LE to-name 
    AND guest.wohnort GE city AND guest.wohnort LE to-city 
    AND guest.anlage-datum GE fdate AND guest.anlage-datum LE tdate 
    NO-LOCK BY guest.name:
    
    do-it = YES.
    IF NOT segm-all THEN
    DO: 
      FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
        AND guestseg.segmentcode = segmentcode NO-LOCK NO-ERROR. 
      do-it =  AVAILABLE guestseg.
    END.

    IF do-it AND payType GT 0 THEN 
    DO:   
        IF paytype = 1 THEN do-it = (guest.zahlungsart NE 0).
        ELSE do-it = (guest.zahlungsart EQ 0).
    END.
    
    IF do-it AND PRtype GT 0 THEN
    DO:
      FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr
          NO-LOCK NO-ERROR.
      IF PRtype = 1 THEN do-it = AVAILABLE guest-pr.
      ELSE do-it = NOT AVAILABLE guest-pr.
    END.

    IF do-it AND fl-email THEN
    DO:
        IF guest.email-adr = "" THEN
            do-it = NO.
    END.

    IF do-it AND fl-mcid THEN
    DO:
        FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE mc-guest THEN do-it = NO.
    END.

    IF do-it THEN 
    DO: 
      anzahl = anzahl + 1. 
      IF sorttype = 0 THEN 
      DO: 
        create output-list. 
        output-list.str = STRING((translateExtended ("Name :",lvCAREA,"") + " " + guest.name + ", " 
          + guest.vorname1 + " " + guest.anrede1), "x(64)") 
          + translateExtended ("CardNo :",lvCAREA,"") + " " + STRING(guest.gastnr). 
 
        create output-list. 
        output-list.str = translateExtended ("Address :",lvCAREA,"") + " " + guest.adresse1 + "  " + guest.adresse2. 
 
        IF guest.adresse3 NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = "         " + guest.adresse3. 
        END. 
 
        create output-list. 
        output-list.str = translateExtended ("City :",lvCAREA,"") + " " + guest.land + " - " 
          + STRING(guest.plz) + " " + guest.wohnort.

        IF prov THEN    /*william 5CF606*/
        DO:
            CREATE output-list.
            output-list.str = translateExtended ("Province :",lvCAREA,"") + " " + guest.geburt-ort2 .
        END.
 
        create output-list. 
        output-list.str = translateExtended ("Telephone :",lvCAREA,"") + " " + STRING(guest.telefon) 
          + "   " + translateExtended ("Telefax :",lvCAREA,"") + " " + STRING(guest.fax). 
        IF guest.email-adr NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("E-mail :",lvCAREA,"") + " " + guest.email-adr. 
        END. 
 
        create output-list. 
        IF guest.geburtdatum1 NE ? THEN 
          output-list.str = translateExtended ("Birthdate :",lvCAREA,"") + " " + STRING(guest.geburtdatum1) 
            + "   " + translateExtended ("Credit Limit :",lvCAREA,"") + " " + STRING(guest.kreditlimit). 
        ELSE output-list.str = translateExtended ("Birthdate :",lvCAREA,"") + " " + "          " 
            + "   " + translateExtended ("Credit Limit :",lvCAREA,"") + " " + STRING(guest.kreditlimit). 
        IF guest.zahlungsart NE 0 THEN 
        output-list.str = output-list.str + "   " + translateExtended ("Payment :",lvCAREA,"") + " " 
          + STRING(guest.zahlungsart). 
 
        IF guest.master-gastnr NE 0 THEN 
        DO: 
          FIND FIRST guest1 WHERE guest1.gastnr = guest.master-gastnr NO-LOCK. 
          create output-list. 
          output-list.str = translateExtended ("Master Company :",lvCAREA,"") + " " 
            + guest1.name + " " + guest.anredefirma. 
        END. 

        IF fl-mcid THEN
        DO:
            FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                create output-list.
                output-list.str = translateExtended ("Membership No :",lvCAREA,"")
                    + " " + mc-guest.cardnum.

                FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN
                DO:
                    create output-list.
                    output-list.str = translateExtended ("Membership Type :",lvCAREA,"")
                        + " " + mc-types.bezeich.
                END.                    
            END.
        END.

        IF PRtype EQ 1 THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("Rate Codes :",lvCAREA,"").
          FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr 
            NO-LOCK BY guest-pr.CODE:
            output-list.str = output-list.str + " " + guest-pr.CODE + ";".
          END. 
        END.

        IF guest.bemerk NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("Comments :",lvCAREA,"") + " " + STRING(guest.bemerk, "x(80)"). 
        END. 
 
        create output-list. 
        output-list.str = chr(10). 
      END. 
      
      ELSE IF sorttype = 1 THEN 
      DO: 
        create output-list. 
        output-list.str = STRING((translateExtended ("Name :",lvCAREA,"") + " " + guest.name + " " 
          + guest.anredefirma), "x(64)") 
          + translateExtended ("CardNo :",lvCAREA,"") + " " + STRING(guest.gastnr). 
 
        create output-list. 
        output-list.str = translateExtended ("Address :",lvCAREA,"") + " " + guest.adresse1 + "  " + guest.adresse2. 
        IF guest.adresse3 NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = "         " + guest.adresse3. 
        END. 
 
        create output-list. 
        output-list.str = translateExtended ("City :",lvCAREA,"") + " " + guest.land + " - " 
          + STRING(guest.plz) + " " + guest.wohnort. 

        IF prov THEN    /*william 5CF606*/
        DO:
            CREATE output-list.
            output-list.str = translateExtended ("Province :",lvCAREA,"") + " " + guest.geburt-ort2 .
        END.
 
        create output-list. 
        output-list.str = translateExtended ("Telephone :",lvCAREA,"") + " " + STRING(guest.telefon) 
          + "   " + translateExtended ("Telefax :",lvCAREA,"") + " " + STRING(guest.fax). 
        IF guest.email-adr NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("E-mail :",lvCAREA,"") + " " + guest.email-adr. 
        END. 
 
        create output-list. 
        output-list.str = translateExtended ("Credit Limit :",lvCAREA,"") + " " + STRING(guest.kreditlimit). 
        IF guest.zahlungsart NE 0 THEN 
        output-list.str = output-list.str + "   " + translateExtended ("Payment :",lvCAREA,"") + " " 
          + STRING(guest.zahlungsart). 

        IF guest.namekontakt NE "" THEN
        DO:
            CREATE output-list.
            output-list.str = translateExtended("Contact Name :", lvCAREA, "") + " " + 
                guest.namekontakt.
        END.
 
        IF guest.master-gastnr NE 0 THEN 
        DO: 
          FIND FIRST guest1 WHERE guest1.gastnr = guest.master-gastnr NO-LOCK. 
          create output-list. 
          output-list.str = translateExtended ("Master Company :",lvCAREA,"") + " " 
            + guest1.name + " " + guest.anredefirma. 
        END. 
 
        IF fl-mcid THEN
        DO:
            FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                create output-list.
                output-list.str = translateExtended ("Membership No :",lvCAREA,"")
                    + " " + mc-guest.cardnum.

                FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN
                DO:
                    create output-list.
                    output-list.str = translateExtended ("Membership Type :",lvCAREA,"")
                        + " " + mc-types.bezeich.
                END.
            END.
        END.

        IF PRtype EQ 1 THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("Rate Codes :",lvCAREA,"").
          FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr 
            NO-LOCK BY guest-pr.CODE:
            output-list.str = output-list.str + " " + guest-pr.CODE + ";".
          END. 
        END.

        IF guest.bemerk NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("Comments :",lvCAREA,"") + " " + STRING(guest.bemerk, "x(80)"). 
        END. 
        create output-list. 
        output-list.str = chr(10). 
      END. 
 
      ELSE IF sorttype = 2 THEN 
      DO: 
        create output-list. 
        output-list.str = STRING((translateExtended ("Name :",lvCAREA,"") + " " + guest.name + " " 
          + guest.anredefirma), "x(64)") 
          + translateExtended ("CardNo :",lvCAREA,"") + " " + STRING(guest.gastnr). 
 
        create output-list. 
        output-list.str = translateExtended ("Address :",lvCAREA,"") + " " + guest.adresse1 + "  " + guest.adresse2. 
        IF guest.adresse3 NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = "         " + guest.adresse3. 
        END. 
 
        create output-list. 
        output-list.str = translateExtended ("City :",lvCAREA,"") + " " + guest.land + " - " 
          + STRING(guest.plz) + " " + guest.wohnort.

        IF prov THEN    /*william 5CF606*/
        DO:
            CREATE output-list.
            output-list.str = translateExtended ("Province :",lvCAREA,"") + " " + guest.geburt-ort2 .
        END.
 
        create output-list. 
        output-list.str = translateExtended ("Telephone :",lvCAREA,"") + " " + STRING(guest.telefon) 
          + "   " + translateExtended ("Telefax :",lvCAREA,"") + " " + STRING(guest.fax). 
        IF guest.email-adr NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("E-mail :",lvCAREA,"") + " " + guest.email-adr. 
        END. 
 
        create output-list. 
        output-list.str = translateExtended ("Credit Limit :",lvCAREA,"") + " " + STRING(guest.kreditlimit). 
        IF guest.zahlungsart NE 0 THEN 
        output-list.str = output-list.str + "   " + translateExtended ("Payment :",lvCAREA,"") + " " 
          + STRING(guest.zahlungsart). 

        IF guest.namekontakt NE "" THEN 
        DO:
            CREATE output-list.
            output-list.str = translateExtended("Contact Name :", lvCAREA, "") + " " + 
                guest.namekontakt.
        END.
 
        IF guest.master-gastnr NE 0 THEN 
        DO: 
          FIND FIRST guest1 WHERE guest1.gastnr = guest.master-gastnr NO-LOCK. 
          create output-list. 
          output-list.str = translateExtended ("Master Company :",lvCAREA,"") + " " 
            + guest1.name + " " + guest.anredefirma. 
        END. 
 
        IF fl-mcid THEN
        DO:
            FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                create output-list.
                output-list.str = translateExtended ("Membership No :",lvCAREA,"")
                    + " " + mc-guest.cardnum.

                FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN
                DO:
                    create output-list.
                    output-list.str = translateExtended ("Membership Type :",lvCAREA,"")
                        + " " + mc-types.bezeich.
                END.
            END.
        END.

        IF PRtype EQ 1 THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("Rate Codes :",lvCAREA,"").
          FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr
            NO-LOCK BY guest-pr.CODE:
            output-list.str = output-list.str + " " + guest-pr.CODE + ";".
          END. 
        END.

        IF guest.bemerk NE "" THEN 
        DO: 
          create output-list. 
          output-list.str = translateExtended ("Comments :",lvCAREA,"") + " " + STRING(guest.bemerk, "x(80)"). 
        END. 
        create output-list. 
        output-list.str = chr(10).
      END.
    END.
  END.
END. 


PROCEDURE create-gcflist1: 
DEFINE VARIABLE str1 AS CHAR FORMAT "x(110)". 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE buffer guest1 FOR guest. 
DEFINE VARIABLE to-city AS CHAR INITIAL "zzz". 
 
  FOR EACH gcf-print2: 
    delete gcf-print2. 
  END. 
 
  IF city NE "" THEN 
  DO: 
    to-city = city. 
  END. 

  FOR EACH guest WHERE guest.gastnr GT 0 AND guest.karteityp = sorttype 
    AND guest.name GE from-name AND guest.name LE to-name 
    AND guest.wohnort GE city AND guest.wohnort LE to-city 
    AND guest.anlage-datum GE fdate AND guest.anlage-datum LE tdate
    NO-LOCK BY guest.name:

    do-it = YES.
    IF NOT segm-all = YES THEN 
    DO: 
      FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
        AND guestseg.segmentcode = segmentcode NO-LOCK NO-ERROR. 
      do-it = AVAILABLE guestseg. 
    END. 
    

    IF do-it AND payType GT 0 THEN 
    DO: 
        IF paytype = 1 THEN do-it = (guest.zahlungsart NE 0). 
        ELSE do-it = (guest.zahlungsart EQ 0).
    END.
    
    IF do-it AND PRtype GT 0 THEN
    DO:
      FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr
          NO-LOCK NO-ERROR.
      IF PRtype = 1 THEN do-it = AVAILABLE guest-pr.
      ELSE do-it = NOT AVAILABLE guest-pr.
    END.

    IF do-it AND fl-email THEN
    DO:
        IF guest.email-adr = "" THEN
            do-it = NO.
    END.

    IF do-it AND fl-mcid THEN
    DO:
        FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE mc-guest THEN do-it = NO.
    END.

    IF do-it THEN 
    DO: 
      anzahl = anzahl + 1. 
      CREATE gcf-print2.
      gcf-print2.count-num = anzahl.

      BUFFER-COPY guest TO gcf-print2.
      FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE mc-guest THEN 
      DO:
          gcf-print2.memberno = mc-guest.cardnum . /*wen 08/29/18*/
          FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
          IF AVAILABLE mc-types THEN gcf-print2.membertype = mc-types.bezeich.
      END.
          

      IF PRtype = 1 THEN
        FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr
            NO-LOCK BY guest-pr.CODE:
            gcf-print2.ratecode = gcf-print2.ratecode + guest-pr.CODE + ";".
            
        END.
      
      IF segm-all THEN FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK NO-ERROR. /*william*/
      FIND FIRST segment WHERE segment.segmentcode EQ guestseg.segmentcode NO-LOCK NO-ERROR.
      IF AVAILABLE segment THEN
        gcf-print2.segment = segment.bezeich.
      ELSE
        gcf-print2.segment = "".
    END. 
  END. 
END. 

