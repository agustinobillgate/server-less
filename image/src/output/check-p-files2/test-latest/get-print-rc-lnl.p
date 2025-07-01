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
    FIELD province        AS CHARACTER
    FIELD phone           AS CHARACTER
    FIELD telefax         AS CHARACTER
    FIELD occupation      AS CHARACTER
    FIELD child1          AS CHARACTER
    FIELD child2          AS CHARACTER
    FIELD main-comment    AS CHARACTER
    FIELD member-comment  AS CHARACTER
    FIELD depositgef      AS CHARACTER
    FIELD depositbez      AS CHARACTER
    FIELD segment         AS CHARACTER
.

DEFINE TEMP-TABLE variable-list
    FIELD varKey    AS CHAR
    FIELD varValue  AS CHAR.

DEFINE INPUT PARAMETER resNo    AS INTEGER.
DEFINE INPUT PARAMETER reslinNo AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR variable-list.

RUN get-print-rc-lnlbl.p (resNo, reslinNo, OUTPUT TABLE print-rc-list). 

FIND FIRST print-rc-list NO-LOCK NO-ERROR.   
IF AVAILABLE print-rc-list THEN
DO:
    CREATE variable-list.
    ASSIGN 
        varKey   = "$GASTNO"
        varValue = print-rc-list.gastno.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$CR-USR"
        varValue = print-rc-list.cr-usr.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$FIRSTNAME"
        varValue = print-rc-list.first-name.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$TITLE1"
        varValue = print-rc-list.guest-title.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ROOM"
        varValue = print-rc-list.room.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ROOM-NO"
        varValue = print-rc-list.room-no.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ROOM-PRICE"
        varValue = print-rc-list.room-price.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ARRIVAL"
        varValue = print-rc-list.arrival.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ETAFL"
        varValue = print-rc-list.eta-flight.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ETATIME"
        varValue = print-rc-list.eta-time.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$DEPARTURE"
        varValue = print-rc-list.departure.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$DEPARTURE0"
        varValue = SUBSTR(print-rc-list.departure, 1, 10).
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ETDFL"
        varValue = print-rc-list.etd-flight.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ETDTIME"
        varValue = print-rc-list.etd-time.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ACC"
        varValue = print-rc-list.no-guest.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ADDRESS1"
        varValue = print-rc-list.guest-address1.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ADDRESS1"
        varValue = print-rc-list.guest-address2.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ADDRESS1"
        varValue = print-rc-list.guest-address3.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RESIDENT"
        varValue = print-rc-list.guest-city.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ZIP"
        varValue = print-rc-list.guest-zip.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$COUNTRY"
        varValue = print-rc-list.guest-country.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$GCOMPANY"
        varValue = print-rc-list.company-name.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RSV-ADDR1"
        varValue = print-rc-list.rsv-addr1.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RSV-ADDR2"
        varValue = print-rc-list.rsv-addr2.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RSV-ADDR3"
        varValue = print-rc-list.rsv-addr3.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RSV-CITY"
        varValue = print-rc-list.rsv-city.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RSV-ZIP"
        varValue = print-rc-list.rsv-zip.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RSV-COUNTRY"
        varValue = print-rc-list.rsv-country.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$CCARD"
        varValue = print-rc-list.ccard.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$BIRTHPLACE"
        varValue = print-rc-list.birth-place.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$BIRTDATE"
        varValue = print-rc-list.birth-date.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ID-No"
        varValue = print-rc-list.guest-id.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$ID-EXPIRED"
        varValue = print-rc-list.expired-id.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$NATION1"
        varValue = print-rc-list.guest-nation.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$PURPOSE"
        varValue = print-rc-list.purpose-stay.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$BL-INSTRUCT"
        varValue = print-rc-list.bill-instruct.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$EMAIL"
        varValue = print-rc-list.guest-email.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$RESNO"
        varValue = print-rc-list.resnr.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$PROVINCE"
        varValue = print-rc-list.province.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$PHONE"
        varValue = print-rc-list.phone.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$OCCUPATION"
        varValue = print-rc-list.occupation.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$CHILD1"
        varValue = print-rc-list.child1.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$CHILD2"
        varValue = print-rc-list.child2.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$MAIN-COMMENT"
        varValue = print-rc-list.main-comment.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$MEMBER-COMMENT"
        varValue = print-rc-list.member-comment.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$DEPOSITGEF"
        varValue = print-rc-list.depositgef.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$DEPOSITBEZ"
        varValue = print-rc-list.depositbez.
    CREATE variable-list.
    ASSIGN 
        varKey   = "$SEGMENT"
        varValue = print-rc-list.segment.

    IF NUM-ENTRIES(print-rc-list.last-name,"-") GT 1 THEN 
    DO:
        CREATE variable-list.
        ASSIGN 
            varKey   = "$Name1"
            varValue = ENTRY(1,print-rc-list.last-name,"-").
        CREATE variable-list.
        ASSIGN 
            varKey   = "$MC-TYPE"
            varValue = ENTRY(2,print-rc-list.last-name,"-").
    END.
    ELSE
    DO:
        CREATE variable-list.
        ASSIGN 
            varKey   = "$Name1"
            varValue = print-rc-list.last-name.
    END.

    IF NUM-ENTRIES(print-rc-list.telefax,";") GT 1 THEN 
    DO:
        CREATE variable-list.
        ASSIGN 
            varKey   = "$TELEFAX"
            varValue = ENTRY(1,print-rc-list.telefax,";").
        CREATE variable-list.
        ASSIGN 
            varKey   = "$CARD-NUM"
            varValue = ENTRY(2,print-rc-list.telefax,";").
    END.
    ELSE
    DO:
        CREATE variable-list.
        ASSIGN 
            varKey   = "$TELEFAX"
            varValue = print-rc-list.telefax.
    END.

    IF NUM-ENTRIES(print-rc-list.mobile-no,";") GT 1 THEN 
    DO:
        CREATE variable-list.
        ASSIGN 
            varKey   = "$MOBILE"
            varValue = ENTRY(1,print-rc-list.mobile-no,";").
        CREATE variable-list.
        ASSIGN 
            varKey   = "$SOURCE"
            varValue = ENTRY(2,print-rc-list.mobile-no,";").
    END.
    ELSE
    DO:
        CREATE variable-list.
        ASSIGN 
            varKey   = "$MOBILE"
            varValue = print-rc-list.mobile-no.
    END.
END.
