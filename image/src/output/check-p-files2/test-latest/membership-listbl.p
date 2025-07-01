DEFINE TEMP-TABLE member-list
    FIELD guest-number      AS INT
    FIELD member-number     AS CHAR
    FIELD member-type       AS CHAR
    FIELD member-from-date  AS DATE
    FIELD member-to-date    AS DATE
    FIELD member-sales-id   AS CHAR
    FIELD member-sales-name AS CHAR
    FIELD member-actiflag   AS LOGICAL
    FIELD guest-title       AS CHAR
    FIELD first-name        AS CHAR
    FIELD last-name         AS CHAR
    FIELD country           AS CHAR
    FIELD address           AS CHAR
    FIELD city              AS CHAR
    FIELD phone             AS CHAR
    FIELD mobile-phone      AS CHAR
    FIELD email             AS CHAR
    FIELD sex               AS CHAR
    FIELD idcard-number     AS CHAR
    FIELD birthday          AS DATE
    FIELD bemerk            AS CHAR
    FIELD member-name       AS CHAR.

DEFINE TEMP-TABLE non-member
    FIELD activeflag AS LOGICAL.

DEFINE INPUT PARAMETER member-number AS CHAR.
DEFINE INPUT PARAMETER member-type AS INT.
DEFINE OUTPUT PARAMETER result-str AS CHAR.

DEFINE OUTPUT PARAMETER TABLE FOR member-list.
DEFINE VARIABLE salesname AS CHAR.

IF member-type EQ 0 THEN
DO:
    IF member-number EQ "" THEN
    DO:     
       FOR EACH mc-guest NO-LOCK:
           FIND FIRST guest WHERE guest.gastnr EQ mc-guest.gastnr NO-LOCK NO-ERROR.
          /* FIND FIRST nation WHERE nation.kurzbez EQ guest.wohnort NO-LOCK NO-ERROR.*/
           FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
           salesname = "".
           IF mc-guest.sales-id NE "" THEN
           DO:
               FIND FIRST bediener WHERE bediener.flag EQ 0 AND bediener.userinit EQ mc-guest.sales-id NO-LOCK NO-ERROR.
               IF AVAILABLE bediener THEN salesname = bediener.username.
               ELSE salesname = "".
           END.
           
           IF AVAILABLE guest THEN RUN create-list.

       END.       
    END.
    ELSE
    DO:
        FIND FIRST mc-guest WHERE mc-guest.cardnum EQ member-number NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr EQ mc-guest.gastnr NO-LOCK NO-ERROR.
            /* FIND FIRST nation WHERE nation.kurzbez EQ guest.wohnort NO-LOCK NO-ERROR. */
            FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
            salesname = "".
            IF mc-guest.sales-id NE "" THEN
            DO:
                FIND FIRST bediener WHERE bediener.flag EQ 0 AND bediener.userinit EQ mc-guest.sales-id NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN salesname = bediener.username.
                ELSE salesname = "".
            END.
            RUN create-list.
        END.
    END.
END.
ELSE
DO:
    IF member-number EQ "" THEN
    DO:
        FOR EACH mc-guest WHERE mc-guest.nr EQ member-type NO-LOCK:
            FIND FIRST guest WHERE guest.gastnr EQ mc-guest.gastnr NO-LOCK NO-ERROR.
           /* FIND FIRST nation WHERE nation.kurzbez EQ guest.wohnort NO-LOCK NO-ERROR.*/
            FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
            salesname = "".
            IF mc-guest.sales-id NE "" THEN
            DO:
                FIND FIRST bediener WHERE bediener.flag EQ 0 AND bediener.userinit EQ mc-guest.sales-id NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN salesname = bediener.username.
                ELSE salesname = "".
            END.
            RUN create-list.
        END.
    END.
    ELSE
    DO:
        FIND FIRST mc-guest WHERE mc-guest.nr EQ member-type 
            AND mc-guest.cardnum EQ member-number NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr EQ mc-guest.gastnr NO-LOCK NO-ERROR.
           /* FIND FIRST nation WHERE nation.kurzbez EQ guest.wohnort NO-LOCK NO-ERROR.*/
            FIND FIRST mc-types WHERE mc-types.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
            salesname = "".
            IF mc-guest.sales-id NE "" THEN
            DO:
                FIND FIRST bediener WHERE bediener.flag EQ 0 AND bediener.userinit EQ mc-guest.sales-id NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN salesname = bediener.username.
                ELSE salesname = "".
            END.
            RUN create-list.
        END.
    END.
END.

PROCEDURE create-list:    
         CREATE member-list.
            ASSIGN 
              member-list.guest-number      = guest.gastnr
              member-list.member-number     = mc-guest.cardnum
              member-list.member-type       = mc-types.bezeich
              member-list.member-from-date  = mc-guest.fdate
              member-list.member-to-date    = mc-guest.tdate
              member-list.member-sales-id   = mc-guest.sales-id
              member-list.member-sales-name = salesname
              member-list.member-actiflag   = mc-guest.activeflag
              member-list.first-name        = guest.vorname1
              member-list.last-name         = guest.NAME
              member-list.guest-title       = guest.anrede1
              member-list.country           = guest.land
              member-list.address           = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
              member-list.city              = guest.wohnort
              member-list.phone             = guest.telefon
              member-list.mobile-phone      = guest.mobil-telefon
              member-list.email             = guest.email-adr
              member-list.sex               = guest.geschlecht
              member-list.idcard-number     = guest.ausweis-nr1
              member-list.birthday          = guest.geburtdatum1
              member-list.bemerk            = REPLACE(member-list.address, CHR(10), "")
              member-list.member-name       = REPLACE(guest.vorname1 + " " +  guest.NAME, CHR(10), "").
          
         IF AVAILABLE mc-types THEN ASSIGN member-list.member-type = mc-types.bezeich.
END.

/*
DEFINE BROWSE b1 QUERY q1 DISPLAY 
  /* Frans: Edit sesuai kebutuhan ticket, type data dan width browse nya */
  SUBSTRING(STR,1,8)            FORMAT "x(8)"           LABEL "Member Code" 
  SUBSTRING(STR,29,6)           FORMAT "x(6)"           LABEL "Member Name" 
  INTEGER(SUBSTRING(STR,35,9))  FORMAT ">>>>>>>>>"      LABEL "Member Type" 
  INTEGER(SUBSTRING(STR,44,12)) FORMAT ">>>>>>>>>>>>"   LABEL "Valid From" 
  SUBSTRING(STR,56, 18)         FORMAT "x(18)"          LABEL "Valid Until" 
  SUBSTRING(STR,74, 22)         FORMAT "x(22)"          LABEL "Active Member" 
  INTEGER(SUBSTRING(STR,96,5))  FORMAT "->>>9"          LABEL "Country" 
  SUBSTRING(STR,101,19)         FORMAT "x(19)"          LABEL "Address" 
  SUBSTRING(STR,9, 20)          FORMAT "x(20)"          LABEL "City" 
  SUBSTRING(STR,120, 8)         FORMAT "x(8)"           LABEL "Phone" 
  SUBSTRING(STR,128, 16)        FORMAT "x(16)"          LABEL "Mobile Phone"
  SUBSTRING(STR,128, 16)        FORMAT "x(16)"          LABEL "Email"
  SUBSTRING(STR,128, 16)        FORMAT "x(16)"          LABEL "ID Card Number"
  SUBSTRING(STR,128, 16)        FORMAT "x(16)"          LABEL "Birthday"
  SUBSTRING(STR,128, 16)        FORMAT "x(16)"          LABEL "Gender"
  WITH 27 DOWN WIDTH 144.5 FONT 12 FIT-LAST-COLUMN 
/*  label-bgcolor 7 label-fgcolor 15  */ 
  SEPARATORS TITLE "Membership List". 
*/
