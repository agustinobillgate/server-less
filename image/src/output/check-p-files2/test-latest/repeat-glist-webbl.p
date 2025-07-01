
DEFINE TEMP-TABLE input-list
    FIELD pvILanguage      AS INTEGER
    FIELD from-date        AS DATE
    FIELD to-date          AS DATE
    FIELD ci-date          AS DATE
    FIELD create-inhouse   AS LOGICAL
    FIELD sorttype         AS INTEGER
    FIELD modetype         AS INTEGER
    FIELD min-stay         AS INTEGER
. 

DEFINE TEMP-TABLE g-list
    FIELD resnr    LIKE res-line.resnr
    FIELD gastnr   AS INTEGER
    FIELD NAME     AS CHAR FORMAT "x(50)"      LABEL "Guest Name"
    FIELD ankunft  AS DATE LABEL "Check-in"
    FIELD abreise  AS DATE LABEL "Check-out"
    FIELD zinr     LIKE zimmer.zinr
    FIELD reslinnr AS INTEGER
    FIELD zipreis  LIKE res-line.zipreis
    FIELD currency AS CHAR FORMAT "x(5)"
    FIELD argt     AS CHAR FORMAT "x(6)"
    FIELD erwachs  AS INTEGER FORMAT ">9" LABEL "A"
    FIELD kind1    AS INTEGER FORMAT ">9" LABEL "Ch"
    FIELD gratis   AS INTEGER FORMAT ">9" LABEL "CO"
    FIELD arrFlag  AS LOGICAL INITIAL NO
    FIELD resname  AS CHARACTER
    FIELD lodging  AS DECIMAL
    INDEX g_ix resnr reslinnr gastnr
    INDEX s_ix resnr gastnr
.

DEF TEMP-TABLE repeat-list
    FIELD flag      AS INTEGER INITIAL 0 /* 1=arrival 2=inhouse */ 
    FIELD gastnr    AS INTEGER
    FIELD NAME      AS CHAR FORMAT "x(32)"      LABEL "Guest Name"
    FIELD nation    AS CHAR FORMAT "x(16)"      LABEL "Nationality"
    FIELD birthdate AS DATE FORMAT "99/99/9999" LABEL "BirthDate"
    FIELD email     AS CHARACTER FORMAT "x(32)" LABEL "Email"      /*dody 10/10/16 add email&telp*/
    FIELD telefon   AS CHARACTER FORMAT "x(16)" LABEL "Telephone"
    FIELD vip       AS CHAR FORMAT "x(5)"       LABEL "VIP"
    FIELD city      AS CHAR FORMAT "X(16)"      LABEL "City"
    FIELD stay      AS INTEGER FORMAT ">>>9"     LABEL "Stay"    INITIAL 0
    FIELD rmnite    AS INTEGER FORMAT ">>>>9"    LABEL "RmNite"  INITIAL 0
    FIELD ankunft   AS DATE                     LABEL "Arrival" INITIAL ?
    FIELD arrFlag   AS LOGICAL INITIAL NO
    FIELD zinr      LIKE zimmer.zinr
    FIELD remark    AS CHAR FORMAT "x(36)"      LABEL "Guest Remark"
    FIELD resname   AS CHARACTER FORMAT "x(32)" LABEL "Reserve Name"
    FIELD lodging   AS DECIMAL                  LABEL "Lodging"
    FIELD pax       AS INTEGER                  LABEL "Pax"
    FIELD mobil-telefon LIKE guest.mobil-telefon LABEL "Mobile Phone" /*wen 080218*/
.


DEF TEMP-TABLE cur-date
    FIELD curr-date AS DATE FORMAT "99/99/9999".

DEF TEMP-TABLE output-rlist LIKE repeat-list.
DEF TEMP-TABLE output-glist LIKE g-list.

/* Dzikri BF3C85 - Repeat Guest List repair
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER from-date        AS DATE. 
DEFINE INPUT PARAMETER to-date          AS DATE. 
DEFINE INPUT PARAMETER ci-date          AS DATE. 
DEFINE INPUT PARAMETER create-inhouse   AS LOGICAL. 
*/
DEFINE INPUT  PARAMETER TABLE FOR input-list.
/* Dzikri BF3C85 - END */
DEFINE OUTPUT PARAMETER TABLE FOR g-list.
DEFINE OUTPUT PARAMETER TABLE FOR repeat-list.
DEFINE OUTPUT PARAMETER TABLE FOR cur-date.

/**********  DEFINE WIDGETS  **********/ 

DEFINE VARIABLE pvILanguage      AS INTEGER  NO-UNDO.
DEFINE VARIABLE from-date        AS DATE. 
DEFINE VARIABLE to-date          AS DATE. 
DEFINE VARIABLE ci-date          AS DATE. 
DEFINE VARIABLE create-inhouse   AS LOGICAL. 
DEFINE VARIABLE sorttype         AS INTEGER. 
DEFINE VARIABLE modetype         AS INTEGER. 
DEFINE VARIABLE min-stay         AS INTEGER. 

FIND FIRST input-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE input-list THEN 
DO:
    MESSAGE "No input parameters found." VIEW-AS ALERT-BOX ERROR.
    RETURN.
END.
ELSE 
DO:
    ASSIGN
        pvILanguage      = input-list.pvILanguage
        from-date        = input-list.from-date
        to-date          = input-list.to-date
        ci-date          = input-list.ci-date
        create-inhouse   = input-list.create-inhouse
        sorttype         = input-list.sorttype
        modetype         = input-list.modetype
        min-stay         = input-list.min-stay
    .
END.
 
RUN repeat-glist_1bl.p (pvILanguage, from-date, to-date,
                    ci-date, create-inhouse,
                    OUTPUT TABLE output-glist, OUTPUT TABLE output-rlist,
                    OUTPUT TABLE cur-date).

IF modetype EQ 1 THEN RUN disp-repeatList.
ELSE IF modetype EQ 2 THEN RUN disp-guestHistory.
 
PROCEDURE disp-repeatList:
  DEFINE VARIABLE tot-lodging AS DECIMAL NO-UNDO.
  DEFINE VARIABLE tot-stay    AS INTEGER NO-UNDO.
  DEFINE VARIABLE tot-rmnight AS INTEGER NO-UNDO.
  DEFINE VARIABLE tot-pax     AS INTEGER NO-UNDO.

  IF sorttype = 0 THEN 
  DO:
       FOR EACH output-rlist BY output-rlist.stay DESCENDING BY output-rlist.NAME:
          IF (output-rlist.stay GE min-stay) 
              OR (output-rlist.stay GE (min-stay - 1) AND output-rlist.arrFLag) THEN
          DO:
            CREATE repeat-list.
            ASSIGN
                repeat-list.flag          = output-rlist.flag
                repeat-list.gastnr        = output-rlist.gastnr
                repeat-list.NAME          = output-rlist.NAME
                repeat-list.nation        = output-rlist.nation
                repeat-list.birthdate     = output-rlist.birthdate
                repeat-list.email         = output-rlist.email
                repeat-list.telefon       = output-rlist.telefon
                repeat-list.vip           = output-rlist.vip
                repeat-list.city          = output-rlist.city
                repeat-list.stay          = output-rlist.stay
                repeat-list.rmnite        = output-rlist.rmnite
                repeat-list.ankunft       = output-rlist.ankunft
                repeat-list.arrFlag       = output-rlist.arrFlag
                repeat-list.zinr          = output-rlist.zinr
                repeat-list.remark        = output-rlist.remark
                repeat-list.resname       = output-rlist.resname
                repeat-list.lodging       = output-rlist.lodging
                repeat-list.pax           = output-rlist.pax
                repeat-list.mobil-telefon = output-rlist.mobil-telefon

                tot-lodging = tot-lodging + output-rlist.lodging
                tot-stay    = tot-stay + output-rlist.stay
                tot-rmnight = tot-rmnight + output-rlist.rmnite
                tot-pax     = tot-pax + output-rlist.pax.
          END.
       END.

       CREATE repeat-list.
       ASSIGN repeat-list.city    = "T O T A L"
              repeat-list.stay    = tot-stay
              repeat-list.lodging = tot-lodging
              repeat-list.rmnite  = tot-rmnight
              repeat-list.zinr    = " "
              repeat-list.pax     = tot-pax.
  END.
  ELSE 
  DO:
    IF sorttype = 1 THEN
    DO:
      FOR EACH output-rlist BY output-rlist.stay DESCENDING BY output-rlist.NAME:
        IF output-rlist.flag = sorttype 
          AND ((output-rlist.stay GE min-stay) OR (output-rlist.stay GE (min-stay - 1) AND output-rlist.arrFLag))
          AND output-rlist.ankunft GE from-date
          AND output-rlist.ankunft LE to-date THEN
        DO:
          CREATE repeat-list.
          ASSIGN
              repeat-list.flag          = output-rlist.flag
              repeat-list.gastnr        = output-rlist.gastnr
              repeat-list.NAME          = output-rlist.NAME
              repeat-list.nation        = output-rlist.nation
              repeat-list.birthdate     = output-rlist.birthdate
              repeat-list.email         = output-rlist.email
              repeat-list.telefon       = output-rlist.telefon
              repeat-list.vip           = output-rlist.vip
              repeat-list.city          = output-rlist.city
              repeat-list.stay          = output-rlist.stay
              repeat-list.rmnite        = output-rlist.rmnite
              repeat-list.ankunft       = output-rlist.ankunft
              repeat-list.arrFlag       = output-rlist.arrFlag
              repeat-list.zinr          = output-rlist.zinr
              repeat-list.remark        = output-rlist.remark
              repeat-list.resname       = output-rlist.resname
              repeat-list.lodging       = output-rlist.lodging
              repeat-list.pax           = output-rlist.pax
              repeat-list.mobil-telefon = output-rlist.mobil-telefon

              tot-lodging = tot-lodging + output-rlist.lodging
              tot-pax     = tot-pax + output-rlist.pax.
        END.
      END.
      CREATE output-rlist.
      ASSIGN output-rlist.city    = "T O T A L"
             output-rlist.stay    = 999
             output-rlist.lodging = tot-lodging
             output-rlist.zinr    = " "
             output-rlist.pax     = tot-pax.

    END.
    ELSE 
    DO:
      FOR EACH output-rlist BY output-rlist.stay DESCENDING BY output-rlist.NAME:
        IF output-rlist.flag = sorttype 
          AND ((output-rlist.stay GE min-stay) OR (output-rlist.stay GE (min-stay - 1) AND output-rlist.arrFLag)) THEN
        DO:
          CREATE repeat-list.
          ASSIGN
              repeat-list.flag          = output-rlist.flag
              repeat-list.gastnr        = output-rlist.gastnr
              repeat-list.NAME          = output-rlist.NAME
              repeat-list.nation        = output-rlist.nation
              repeat-list.birthdate     = output-rlist.birthdate
              repeat-list.email         = output-rlist.email
              repeat-list.telefon       = output-rlist.telefon
              repeat-list.vip           = output-rlist.vip
              repeat-list.city          = output-rlist.city
              repeat-list.stay          = output-rlist.stay
              repeat-list.rmnite        = output-rlist.rmnite
              repeat-list.ankunft       = output-rlist.ankunft
              repeat-list.arrFlag       = output-rlist.arrFlag
              repeat-list.zinr          = output-rlist.zinr
              repeat-list.remark        = output-rlist.remark
              repeat-list.resname       = output-rlist.resname
              repeat-list.lodging       = output-rlist.lodging
              repeat-list.pax           = output-rlist.pax
              repeat-list.mobil-telefon = output-rlist.mobil-telefon
              
              tot-lodging = tot-lodging + output-rlist.lodging
              tot-pax     = tot-pax + output-rlist.pax.
        END.
      END.
      CREATE output-rlist.
      ASSIGN output-rlist.city    = "T O T A L"
             output-rlist.stay    = 999
             output-rlist.lodging = tot-lodging
             output-rlist.zinr    = " "
             output-rlist.pax     = tot-pax.
    END.
  END.
END PROCEDURE.

PROCEDURE disp-guestHistory:
  FOR EACH output-glist WHERE output-glist.gastnr = sorttype NO-LOCK BY output-glist.ankunft:
      CREATE g-list.
      ASSIGN g-list.resnr    = output-glist.resnr
             g-list.gastnr   = output-glist.gastnr
             g-list.NAME     = output-glist.NAME
             g-list.ankunft  = output-glist.ankunft
             g-list.abreise  = output-glist.abreise
             g-list.zinr     = output-glist.zinr
             g-list.reslinnr = output-glist.reslinnr
             g-list.zipreis  = output-glist.zipreis
             g-list.currency = output-glist.currency
             g-list.argt     = output-glist.argt
             g-list.erwachs  = output-glist.erwachs
             g-list.kind1    = output-glist.kind1
             g-list.gratis   = output-glist.gratis
             g-list.arrFlag  = output-glist.arrFlag
             g-list.resname  = output-glist.resname
             g-list.lodging  = output-glist.lodging
      .
  END.

END PROCEDURE.

