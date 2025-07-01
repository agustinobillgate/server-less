DEFINE TEMP-TABLE sum-list
    FIELD datum     AS DATE                 LABEL "Date"
    FIELD gastnr    AS INTEGER
    FIELD firma     AS CHAR FORMAT "x(24)"  LABEL "Company Name"
    FIELD kontcode  AS CHAR FORMAT "x(12)"  LABEL "Code"
    FIELD zikatnr   AS INTEGER
    FIELD kurzbez   AS CHAR FORMAT "x(6)"   LABEL "RmType"
    FIELD erwachs   AS INTEGER FORMAT ">9"  LABEL "A"
    FIELD kind1     AS INTEGER FORMAT ">9"  LABEL "Ch"
    FIELD gloAnz    AS INTEGER FORMAT ">>9" LABEL "Qty"
    FIELD gresAnz   AS INTEGER FORMAT ">>9" LABEL "GRsv"
    FIELD resAnz    AS INTEGER FORMAT ">>9" LABEL "Rsv"
    FIELD resnrStr  AS CHAR FORMAT "x(60)"  LABEL "ResNo Without Codes"
    INDEX idx1 datum gastnr kontcode
    INDEX idx2 datum gastnr zikatnr erwachs
    INDEX idx3 datum gastnr zikatnr
.

DEFINE TEMP-TABLE output-list 
    FIELD STR               AS CHAR FORMAT "x(141)".

DEFINE TEMP-TABLE str-detail
    FIELD company-name      AS CHAR
    FIELD address           AS CHAR
    FIELD city              AS CHAR
    FIELD glorescode        AS CHAR
    FIELD pricecode         AS CHAR
    FIELD start-date        AS CHAR
    FIELD pax               AS CHAR
    FIELD ending-date       AS CHAR
    FIELD rmcat             AS CHAR
    FIELD argt              AS CHAR
    FIELD id                AS CHAR
    FIELD chgID             AS CHAR
    FIELD create-date       AS CHAR
    FIELD comments          AS CHAR
    FIELD dates-period      AS CHAR
    FIELD dates-number      AS CHAR EXTENT 31
    FIELD dates-str         AS CHAR EXTENT 31
    FIELD reserved-room     AS CHAR EXTENT 31 
    FIELD used-reservation  AS CHAR EXTENT 31 
    FIELD not-used          AS CHAR EXTENT 31 
    FIELD avail-room        AS CHAR EXTENT 31 
    FIELD overbooking       AS CHAR EXTENT 31
    FIELD reservations      AS CHAR 
    FIELD residents         AS CHAR 
    FIELD cancel-res        AS CHAR 
    . 
DEFINE TEMP-TABLE str-summary
    FIELD total-reserve     AS CHAR EXTENT 31 
    FIELD used-reserve      AS CHAR EXTENT 31 
    FIELD not-used          AS CHAR EXTENT 31
    .

DEFINE WORKFILE k-list 
  FIELD gastnr          AS INTEGER 
  FIELD bediener-nr     AS INTEGER 
  FIELD kontcode        AS CHAR 
  FIELD ankunft         AS DATE 
  FIELD zikatnr         AS INTEGER 
  FIELD argt            AS CHAR 
  FIELD zimmeranz       AS INTEGER EXTENT 31 
  FIELD erwachs         AS INTEGER 
  FIELD kind1           AS INTEGER 
  FIELD ruecktage       AS INTEGER 
  FIELD overbooking     AS INTEGER 
  FIELD abreise         AS DATE 
  FIELD useridanlage    AS CHAR 
  FIELD resdate         AS DATE 
  FIELD bemerk          AS CHAR
  . 
 
DEFINE WORKFILE res-list 
  FIELD flag            AS CHAR 
  FIELD count           AS INTEGER 
  FIELD s1              AS CHAR FORMAT "x(108)". 

DEFINE BUFFER usr FOR bediener. 
DEFINE WORKFILE allot-list LIKE kontline. 

/**/
DEFINE INPUT  PARAMETER pvILanguage         AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER delflag             AS LOGICAL.
DEFINE INPUT  PARAMETER from-date           AS DATE.
DEFINE INPUT  PARAMETER to-date             AS DATE.
DEFINE INPUT  PARAMETER ci-date             AS DATE.
DEFINE INPUT  PARAMETER resflag1            AS LOGICAL.
DEFINE INPUT  PARAMETER gflag               AS LOGICAL.
DEFINE INPUT  PARAMETER cflag               AS LOGICAL.
DEFINE INPUT  PARAMETER from-name           AS CHAR.
DEFINE INPUT  PARAMETER to-name             AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR str-detail.
DEFINE OUTPUT PARAMETER TABLE FOR str-summary.
DEFINE OUTPUT PARAMETER TABLE FOR sum-list.

/*
DEFINE VARIABLE pvILanguage     AS INTEGER   INIT 0.
DEFINE VARIABLE delflag         AS LOGICAL   INIT TRUE.
DEFINE VARIABLE from-date       AS DATE      INIT 12/01/21.
DEFINE VARIABLE to-date         AS DATE      INIT 12/31/21.
DEFINE VARIABLE ci-date         AS DATE      INIT 01/14/19.
DEFINE VARIABLE resflag1        AS LOGICAL   INIT FALSE.
DEFINE VARIABLE gflag           AS LOGICAL   INIT TRUE.
DEFINE VARIABLE cflag           AS LOGICAL   INIT TRUE.
DEFINE VARIABLE from-name       AS CHARACTER INIT " ".
DEFINE VARIABLE to-name         AS CHARACTER INIT "ZZ".
*/

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "glores-review". 

RUN create-list (delflag).

CREATE str-summary.
DEFINE VARIABLE loopi AS INT.
DEFINE VARIABLE str-parse AS CHAR.

FOR EACH output-list:
    IF output-list.str MATCHES "*total reserve*" THEN
    DO:
        str-parse = SUBSTRING(output-list.str,15).
        DO loopi = 1 TO NUM-ENTRIES(str-parse," "):
            IF loopi LE 31 THEN
            str-summary.total-reserve[loopi] = ENTRY(loopi,str-parse," ").
        END.
    END.
    ELSE IF output-list.str MATCHES "*used reserve*" THEN
    DO:
        str-parse = SUBSTRING(output-list.str,15).
        DO loopi = 1 TO NUM-ENTRIES(str-parse," "):
            IF loopi LE 31 THEN
            str-summary.used-reserve[loopi] = ENTRY(loopi,str-parse," ").
        END.
    END.
    ELSE IF output-list.str MATCHES "*not used*" THEN
    DO:
        str-parse = SUBSTRING(output-list.str,15).
        DO loopi = 1 TO NUM-ENTRIES(str-parse," "):
            IF loopi LE 31 THEN
            str-summary.not-used[loopi] = ENTRY(loopi,str-parse," ").
        END.
    END.
END.
/*
CURRENT-WINDOW:WIDTH = 200.
FOR EACH str-detail:
   DISP str-detail.dates-str[1]
        str-detail.dates-str[2]
        str-detail.dates-str[3]
        str-detail.dates-str[4]
        str-detail.dates-str[5]
        str-detail.dates-str[6]
        str-detail.dates-str[7]
        str-detail.dates-str[8]
        str-detail.dates-str[9]
        str-detail.dates-str[10]
        str-detail.dates-str[11]
        str-detail.dates-str[12]
        str-detail.dates-str[13]
        str-detail.dates-str[14]
        str-detail.dates-str[15]
        str-detail.dates-str[16]
        str-detail.dates-str[17]
        str-detail.dates-str[18]
        str-detail.dates-str[19]
        str-detail.dates-str[20]
        str-detail.dates-str[21]
        str-detail.dates-str[22]
        str-detail.dates-str[23]
        str-detail.dates-str[24]
        str-detail.dates-str[25]
        str-detail.dates-str[26]
        str-detail.dates-str[27]
        str-detail.dates-str[28]
        str-detail.dates-str[29]
        str-detail.dates-str[30]
        str-detail.dates-str[31] WITH WIDTH 198.
END.
FOR EACH str-summary:
    DISP str-summary.
END.
*/
PROCEDURE create-list:
DEFINE INPUT PARAMETER del-flag AS LOGICAL.
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE usr-init        AS CHAR. 
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE count           AS INTEGER. 
DEFINE VARIABLE currResnr       AS INTEGER INITIAL 0.
DEFINE VARIABLE anz1            AS INTEGER EXTENT 31. 
DEFINE VARIABLE anz2            AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz0          AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz1          AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz2          AS INTEGER EXTENT 31. 
DEFINE VARIABLE avail-allotm    AS INTEGER EXTENT 31. 
DEFINE VARIABLE overbook        AS INTEGER EXTENT 31. 
DEFINE VAR do-it AS LOGICAL. /* Malik serverless */
DEFINE VARIABLE wday            AS CHAR FORMAT "x(2)" EXTENT 8 
  INITIAL ["SU", "MO", "TU", "WE", "TH", "FR", "SA", "SU"]. 
  
  IF del-flag THEN
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
 
  FOR EACH allot-list: 
    DELETE allot-list. 
  END. 
 
  FOR EACH k-list: 
    DELETE k-list. 
  END. 
 
  FOR EACH res-list: 
    DELETE res-list. 
  END. 
  FOR EACH sum-list:
    DELETE sum-list.
  END.
  DO i = 1 TO 31: 
    t-anz0[i] = 0. 
    t-anz1[i] = 0. 
    t-anz2[i] = 0. 
    avail-allotm[i] = 0. 
    overbook[i] = 0. 
  END. 
 
  RUN create-alist. 
  /* Malik Serverless */
  FIND FIRST k-list NO-LOCK NO-ERROR.
  IF AVAILABLE k-list THEN
  DO:
    do-it = YES.
  END.
  ELSE
  DO:
    do-it = NO.
  END.
  

  IF do-it THEN 
  DO:
    FOR EACH k-list: 
      FIND FIRST guest WHERE guest.gastnr = k-list.gastnr NO-LOCK NO-ERROR. 
      FIND FIRST usr WHERE usr.nr = k-list.bediener-nr NO-LOCK NO-ERROR. 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = k-list.zikatnr NO-LOCK NO-ERROR. 

      CREATE str-detail.
  
      create output-list. 
      STR = translateExtended ("Company  Name  :",lvCAREA,"") + " " + guest.name + ", " + guest.anredefirma. 
      create output-list. 
      STR = translateExtended ("Address        :",lvCAREA,"") + " " + guest.adresse1 + " " + guest.adresse2. 
      create output-list. 
      STR = translateExtended ("City           :",lvCAREA,"") + " " + guest.wohnort + " " + guest.plz. 
      create output-list. 
      STR = translateExtended ("Code           :",lvCAREA,"") + " " + k-list.kontcode + "         " + translateExtended ("PriceCode :",lvCAREA,"") + " ". 
      FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
      IF AVAILABLE guest-pr THEN STR = STR + guest-pr.code. 
      create output-list. 
      STR = translateExtended ("Start",lvCAREA,"") + "  " + STRING(k-list.ankunft) + "  " + translateExtended ("Pax",lvCAREA,"") + " " 
        + STRING(k-list.erwachs) + "/" + STRING(k-list.kind1). 
      create output-list. 
      STR = translateExtended ("Ending",lvCAREA,"") + " " + STRING(k-list.abreise) + "  " + translateExtended ("RmCat",lvCAREA,"") + " ". 
      IF AVAILABLE zimkateg THEN STR = STR + STRING(zimkateg.kurzbez, "x(6)"). 
      ELSE STR = STR + "      ". 
  
      IF AVAILABLE usr THEN usr-init = usr.userinit. 
      ELSE usr-init = "  ". 
  
      STR = STR + "  " + translateExtended ("Arg",lvCAREA,"") + " " + STRING(k-list.argt, "x(5)") 
        + "  " + translateExtended ("ID",lvCAREA,"") + " " + STRING(usr-init) + "  " + translateExtended ("ChgID",lvCAREA,"") + " " 
        + STRING(k-list.useridanlage, "x(2)") 
        + "  " + translateExtended ("Date",lvCAREA,"") + " " + STRING(k-list.resdat). 
  
      IF k-list.bemerk NE "" THEN 
      DO: 
        create output-list. 
        STR = translateExtended ("Comment        :",lvCAREA,"") + " " + k-list.bemerk. 
      END. 
      create output-list. 
      STR = translateExtended ("Dates          :",lvCAREA,"") + " " + STRING(from-date) + " - " 
        + STRING(to-date). 

      /*custom by masdod*/
      ASSIGN 
          str-detail.company-name = guest.name
          str-detail.address      = guest.adresse1
          str-detail.city         = guest.wohnort + " " + guest.plz
          str-detail.glorescode   = k-list.kontcode
          str-detail.pricecode    = guest-pr.code
          str-detail.start-date   = STRING(k-list.ankunft)
          str-detail.pax          = STRING(k-list.erwachs) + "/" + STRING(k-list.kind1)
          str-detail.ending-date  = STRING(k-list.abreise)
          str-detail.rmcat        = STRING(zimkateg.kurzbez, "x(6)")
          str-detail.argt         = STRING(k-list.argt, "x(5)") 
          str-detail.id           = STRING(usr-init)
          str-detail.chgID        = STRING(k-list.useridanlage, "x(2)")
          str-detail.create-date  = STRING(k-list.resdat)
          str-detail.comments     = k-list.bemerk
          str-detail.dates-period = STRING(from-date) + " - " + STRING(to-date). 
          .

      create output-list. 
      STR = "                ". 
      datum = from-date. 
      DEF VAR loopdatum AS INT.
      loopdatum = 0.
      DO WHILE datum LE to-date: 
          STR = STR + STRING(day(datum),"99 "). 
          /*custom by masdod*/
          loopdatum = loopdatum + 1.
          ASSIGN 
          str-detail.dates-number[loopdatum] = STRING(day(datum),"99").

          datum = datum + 1. 
      END. 

      create output-list. 
      STR = "                ". 
      datum = from-date. 
      DEF VAR loopdatstr AS INT.
      loopdatstr = 0.
      DO WHILE datum LE to-date: 
          STR = STR + wday[weekday(datum)] + " ". 
          /*custom by masdod*/
          loopdatstr = loopdatstr + 1.
          ASSIGN 
          str-detail.dates-str[loopdatstr] = wday[weekday(datum)].
          datum = datum + 1. 
      END. 
      create output-list. 
      DO i = 1 TO 108: 
          STR = STR + "-". 
      END. 

      create output-list. 
      STR = STRING(translateExtended ("Reserved Room",lvCAREA,""),"x(15)"). 
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
          IF datum GE k-list.ankunft AND datum LE k-list.abreise AND datum GE (ci-date /*+ k-list.ruecktage*/) THEN 
          DO: 
              t-anz0[i] = t-anz0[i] + k-list.zimmeranz[i]. 
              STR = STR + STRING(k-list.zimmeranz[i],"-99"). 
              /*custom by masdod*/
              ASSIGN 
              str-detail.reserved-room[i] = STRING(k-list.zimmeranz[i],"-99").
          END. 
          ELSE
          DO:
              STR = STR + " 00". 
              str-detail.reserved-room[i] = "00".
          END.
          i = i + 1. 
          datum = datum + 1. 
      END. 
  
      DO i = 1 TO 31: 
        anz1[i] = 0. 
        anz2[i] = 0. 
      END. 
  
      FOR EACH res-line WHERE res-line.gastnr =  k-list.gastnr 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT from-date) 
        AND res-line.resstatus LE 6 AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.kontignr = 0 NO-LOCK BY res-line.resnr: 
        DO datum = from-date TO to-date:
          IF res-line.ankunft LE datum AND res-line.abreise GT datum THEN
          DO:
            FIND FIRST sum-list WHERE sum-list.datum = datum
              AND sum-list.gastnr = res-line.gastnr
              AND sum-list.zikatnr = res-line.zikatnr
              AND sum-list.erwachs GE res-line.erwachs USE-INDEX idx2 NO-ERROR.
            IF NOT AVAILABLE sum-list THEN
            FIND FIRST sum-list WHERE sum-list.datum = datum
              AND sum-list.gastnr = res-line.gastnr
              AND sum-list.zikatnr = res-line.zikatnr
              USE-INDEX idx3 NO-ERROR.
            IF AVAILABLE sum-list THEN 
            ASSIGN sum-list.resAnz   = sum-list.resAnz + res-line.zimmeranz.
            IF currResNr NE res-line.resnr THEN 
            DO:    
              currResNr = res-line.resnr.
              ASSIGN sum-list.resnrStr = sum-list.resnrStr 
                + TRIM(STRING(res-line.resnr,">>>>>>>9")) + "; ".
            END.
          END.
        END.
      END.
      count = 0. 
      FOR EACH res-line WHERE res-line.gastnr =  k-list.gastnr 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT from-date) 
        AND res-line.resstatus LE 6 AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.kontignr LT 0 NO-LOCK, 
        FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
        AND kontline.kontcode = k-list.kontcode 
        AND kontline.betriebsnr = 1 
        AND kontline.kontstatus = 1 NO-LOCK BY res-line.ankunft 
        BY res-line.abreise BY res-line.resnr: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
        DO datum = from-date TO to-date:
          IF res-line.ankunft LE datum AND res-line.abreise GT datum THEN
          DO:
            FIND FIRST sum-list WHERE sum-list.datum = datum
              AND sum-list.gastnr = res-line.gastnr
              AND sum-list.kontcode = k-list.kontcode USE-INDEX idx1 NO-ERROR.
            IF AVAILABLE sum-list THEN 
              ASSIGN sum-list.gresAnz = sum-list.gresAnz + res-line.zimmeranz.
          END.
        END.
        IF resflag1 AND res-line.active-flag = 0 THEN 
        DO: 
          CREATE res-list. 
            res-list.flag = "r". 
            count = count + 1. 
            res-list.count = count. 
            s1 = "   " + translateExtended ("ResNo",lvCAREA,"") + " " + STRING(res-line.resnr, ">>>>>>9") 
            + " " + translateExtended ("Arrival",lvCAREA,"") + " " + STRING(res-line.ankunft) 
            + "  " + translateExtended ("Qty",lvCAREA,"") + " " + STRING(res-line.zimmeranz,"99") + "  " + translateExtended ("Pax",lvCAREA,"") + " " 
            + STRING(res-line.erwachs) + "/" + STRING(res-line.kind1) 
            + "  " + translateExtended ("Departure",lvCAREA,"") + " " + STRING(res-line.abreise) 
            + "  " + translateExtended ("ID",lvCAREA,"") + " " + STRING(reservation.useridanlage,"x(2)") + "  " + translateExtended ("ChgID",lvCAREA,"") + " " 
            + STRING(res-line.changed-id, "x(2)"). 
          IF res-line.bemerk NE "" THEN 
          DO: 
            create res-list. 
            count = count + 1. 
            res-list.flag = "r". 
            s1 = translateExtended ("Comment        :",lvCAREA,"") + " " + res-line.bemerk. 
          END. 
        END. 
        IF gflag AND res-line.active-flag = 2 THEN 
        DO: 
          create res-list. 
            res-list.flag = "g". 
            count = count + 1. 
            res-list.count = count. 
            s1 = "   " + translateExtended ("ResNo",lvCAREA,"") + " " + STRING(res-line.resnr, ">>>>>>9") 
            + " " + translateExtended ("Arrival",lvCAREA,"") + " " + STRING(res-line.ankunft) 
            + "  " + translateExtended ("Qty",lvCAREA,"") + " " + STRING(res-line.zimmeranz,"99") + "  " + translateExtended ("Pax",lvCAREA,"") + " " 
            + STRING(res-line.erwachs) + "/" + STRING(res-line.kind1) 
            + "  " + translateExtended ("Departure",lvCAREA,"") + " " + STRING(res-line.abreise) 
            + "  " + translateExtended ("ID",lvCAREA,"") + " " + STRING(reservation.useridanlage,"x(2)") + "  " + translateExtended ("ChgID",lvCAREA,"") + " " 
            + STRING(res-line.changed-id, "x(2)"). 
          IF res-line.bemerk NE "" THEN 
          DO: 
            create res-list. 
            count = count + 1. 
            res-list.flag = "g". 
            s1 = translateExtended ("Comment        :",lvCAREA,"") + " " + res-line.bemerk. 
          END. 
        END. 
        datum = from-date. 
        i = 1. 
        DO WHILE datum LE to-date: 
          IF datum GE res-line.ankunft AND datum LT res-line.abreise THEN 
            anz1[i] = anz1[i] + res-line.zimmeranz. 
          i = i + 1. 
          datum = datum + 1. 
        END. 
      END. 
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
        anz2[i] = k-list.zimmeranz[i] - anz1[i]. 
        i = i + 1. 
        datum = datum + 1. 
      END. 
  
      i = 1. 
      datum = from-date. 
      DO WHILE datum LE to-date: 
        t-anz1[i] = t-anz1[i] + anz1[i]. 
        t-anz2[i] = t-anz2[i] + anz2[i]. 
        i = i + 1. 
        datum = datum + 1. 
      END. 
  
      create output-list. 
      output-list.str = STRING(translateExtended ("Used Rservation",lvCAREA,""), "x(15)"). 
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
          STR = STR + STRING(anz1[i],"-99"). 
          /*custom by masdod*/
          ASSIGN 
          str-detail.used-reservation[i] = STRING(anz1[i],"-99").

          i = i + 1. 
          datum = datum + 1. 
      END. 
  
      create output-list. 
      STR = STRING(translateExtended ("Not used",lvCAREA,""),"x(15)"). 
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
          IF anz2[i] GT 0 THEN
          DO:
              STR = STR + STRING(anz2[i],"-99").      
              /*custom by masdod*/
              ASSIGN 
              str-detail.not-used[i] = STRING(anz2[i],"-99").
          END.
          ELSE
          DO:
              STR = STR + " 00".
              /*custom by masdod*/
              ASSIGN 
              str-detail.not-used[i] = "00".
          END.
          i = i + 1. 
          datum = datum + 1. 
      END. 

      create output-list. 
      STR = STRING(translateExtended ("Available",lvCAREA,""),"x(15)"). 
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
          IF datum GE (ci-date + k-list.ruecktage) THEN 
          DO: 
          IF anz2[i] GT 0 THEN 
          DO: 
              avail-allotm[i] = anz2[i]. 
              STR = STR + STRING(avail-allotm[i],"-99"). 
              /*custom by masdod*/
              ASSIGN 
              str-detail.avail-room[i] = STRING(avail-allotm[i],"-99").
          END. 
          ELSE 
          DO: 
              avail-allotm[i] = 0. 
              STR = STR + " 00". 
              /*custom by masdod*/
              ASSIGN 
              str-detail.avail-room[i] = "00".
          END. 
          END. 
          ELSE 
          DO: 
              avail-allotm[i] = 0. 
              STR = STR + " 00". 
              /*custom by masdod*/
              ASSIGN 
              str-detail.avail-room[i] = "00".
          END. 
          i = i + 1. 
          datum = datum + 1. 
      END. 
  
      create output-list. 
      STR = STRING(translateExtended ("Overbooking",lvCAREA,""),"x(15)"). 
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
          IF datum GE (ci-date + k-list.ruecktage) THEN 
          DO: 
              IF anz2[i] LT 0 THEN 
              DO: 
                  overbook[i] = - anz2[i]. 
                  STR = STR + STRING(overbook[i],"-99"). 
                  /*custom by masdod*/
                  ASSIGN 
                  str-detail.overbooking[i] = STRING(overbook[i],"-99").
              END. 
              ELSE 
              DO: 
                  overbook[i] = 0. 
                  STR = STR + " 00". 
                  /*custom by masdod*/
                  ASSIGN 
                  str-detail.overbooking[i] = "00".
              END. 
          END. 
          ELSE 
          DO: 
              overbook[i] = 0. 
              STR = STR + " 00". 
              /*custom by masdod*/
              ASSIGN 
              str-detail.overbooking[i] = "00".
          END. 
          i = i + 1. 
          datum = datum + 1. 
      END. 
  
      IF resflag1 THEN 
      DO: 
          i = 1. 
          create output-list. 
          STR = translateExtended ("Reservations :",lvCAREA,"") + " ". 
          FOR EACH res-list WHERE res-list.flag = "r" NO-LOCK BY res-list.count: 
              IF i GT 1 THEN 
              DO: 
                  create output-list. 
                  STR = "             " + s1. 
              END. 
              ELSE STR = STR + s1. 
              i = i + 1.
              /*custom by masdod*/
              ASSIGN 
              str-detail.reservations = s1.
          END. 
      END. 
      IF gflag THEN 
      DO: 
          i = 1. 
          create output-list. 
          STR = translateExtended ("Residents   :",lvCAREA,"") + " ". 
          FOR EACH res-list WHERE res-list.flag = "g" NO-LOCK BY res-list.count: 
              IF i GT 1 THEN 
              DO: 
                  create output-list. 
                  STR = "             " + s1. 
              END. 
              ELSE STR = STR + s1. 
              i = i + 1.
              /*custom by masdod*/
              ASSIGN 
              str-detail.residents = s1.
          END. 
      END. 
      IF cflag THEN 
      DO: 
        FOR EACH res-line WHERE res-line.kontignr LT 0 AND 
          res-line.gastnr = kontline.gastnr AND res-line.resstatus = 9 NO-LOCK, 
          FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
          AND kontline.kontcode = k-list.kontcode 
          AND kontline.betriebsnr = 1 
          AND kontline.kontstatus = 1 NO-LOCK 
          BY res-line.ankunft BY res-line.abreise BY res-line.resnr: 
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
          create res-list. 
          res-list.flag = "c". 
          count = count + 1. 
          res-list.count = count. 
          s1 = "   " + translateExtended ("ResNo",lvCAREA,"") + " " + STRING(res-line.resnr, ">>>>>>9") 
          + " " + translateExtended ("Arrival",lvCAREA,"") + " " + STRING(res-line.ankunft) 
          + "  " + translateExtended ("Qty",lvCAREA,"") + " " + STRING(res-line.zimmeranz,"99") + "  " + translateExtended ("Pax",lvCAREA,"") + " " 
          + STRING(res-line.erwachs) + "/" + STRING(res-line.kind1) 
          + "  " + translateExtended ("Departure",lvCAREA,"") + " " + STRING(res-line.abreise) 
          + "  " + translateExtended ("ID",lvCAREA,"") + " " + STRING(reservation.useridanlage,"x(2)") + "  " + translateExtended ("ChgID",lvCAREA,"") + " " 
          + STRING(res-line.changed-id, "x(2)"). 
          IF res-line.bemerk NE "" THEN 
          DO: 
            create res-list. 
            count = count + 1. 
            res-list.flag = "r". 
            s1 = translateExtended ("Comment        :",lvCAREA,"") + " " + res-line.bemerk. 
          END. 
        END. 
        i = 1. 
        create output-list. 
        STR = translateExtended ("Cancelled   :",lvCAREA,"") + " ". 
        FOR EACH res-list WHERE res-list.flag = "c" NO-LOCK BY res-list.count: 
            IF i GT 1 THEN 
            DO: 
                create output-list. 
                STR = "             " + s1. 
            END. 
            ELSE STR = STR + s1. 
            
            /*custom by masdod*/
            ASSIGN 
            str-detail.cancel-res = s1.
            i = i + 1. 
        END. 
      END. 
      create output-list. 
      DO i = 1 TO 108: 
        STR = STR + "=". 
      END. 
      create output-list. 
    END. 
  END.
  /* END Malik */
 
 
  count = 2. 
  DO i = 1 TO 31: 
    IF t-anz0[i] GE 100 THEN count = 3. 
  END. 
  IF count = 3 THEN 
  DO: 
    i = 1. 
    datum = from-date. 
    create output-list. 
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN STR = STRING(translateExtended ("Total Reserve",lvCAREA,""),"x(14)") + STRING(t-anz0[i], "->>>9"). 
      ELSE STR = STR + STRING(t-anz0[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
    i = 2. 
    datum = from-date + 1. 
    create output-list. 
    STR = "               ". 
    DO WHILE datum LE to-date: 
      STR = STR + STRING(t-anz0[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
  END. 
  ELSE 
  DO: 
    i = 1. 
    datum = from-date. 
    create output-list. 
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN STR = STRING(translateExtended ("Total Reserve",lvCAREA,""),"x(15)") + STRING(t-anz0[i], "->9"). 
      ELSE STR = STR + STRING(t-anz0[i], "->9"). 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
 
  count = 2. 
  DO i = 1 TO 31: 
    IF t-anz1[i] GE 100 THEN count = 3. 
  END. 
  IF count = 3 THEN 
  DO: 
    i = 1. 
    datum = from-date. 
    create output-list. 
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN STR = STRING(translateExtended ("Used Reserve",lvCAREA,""),"x(15)") + STRING(t-anz1[i], "->>>>9"). 
      ELSE STR = STR + STRING(t-anz1[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
    i = 2. 
    datum = from-date + 1. 
    create output-list. 
    STR = "         ". 
    DO WHILE datum LE to-date: 
      STR = STR + STRING(t-anz1[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
  END. 
  ELSE 
  DO: 
    i = 1. 
    datum = from-date. 
    create output-list. 
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN STR = STRING(translateExtended ("Used Reserve",lvCAREA,""),"x(15)") + STRING(t-anz1[i], "->9"). 
      ELSE STR = STR + STRING(t-anz1[i], "->9"). 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
 
  count = 2. 
  DO i = 1 TO 31: 
    IF t-anz2[i] GE 100 THEN count = 3. 
  END. 
  IF count = 3 THEN 
  DO: 
    i = 1. 
    datum = from-date. 
    create output-list. 
    DO WHILE datum LE to-date: 
      IF t-anz2[i] GT 0 THEN 
      DO: 
        IF i LE 1 THEN STR = STRING(translateExtended ("Not used",lvCAREA,""),"x(15)") + STRING(t-anz2[i], "->>>>9"). 
        ELSE STR = STR + STRING(t-anz2[i], "->>>>9"). 
      END. 
      ELSE 
      DO: 
        IF i LE 1 THEN STR = STRING(translateExtended ("Not used",lvCAREA,""),"x(15)") + STRING(0, "->>>>9"). 
        ELSE STR = STR + STRING(0, "->>>>9"). 
      END. 
      i = i + 2. 
      datum = datum + 2. 
    END. 
    i = 2. 
    datum = from-date + 1. 
    create output-list. 
    STR = "         ". 
    DO WHILE datum LE to-date: 
      STR = STR + STRING(t-anz2[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
  END. 
  ELSE 
  DO: 
    i = 1. 
    datum = from-date. 
    create output-list. 
    DO WHILE datum LE to-date: 
      IF t-anz2[i] GT 0 THEN 
      DO: 
        IF i LE 1 THEN STR = STRING(translateExtended ("Not used",lvCAREA,""),"x(15)") + STRING(t-anz2[i], "->9"). 
        ELSE STR = STR + STRING(t-anz2[i], "->9"). 
      END. 
      ELSE 
      DO: 
        IF i LE 1 THEN STR = STRING(translateExtended ("Not used",lvCAREA,""),"x(15)") + STRING(0, "->9"). 
        ELSE STR = STR + STRING(0, "->9"). 
      END. 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
END. 
 
PROCEDURE create-alist: 
DEFINE VARIABLE curr-code AS CHAR INITIAL "". 
DEFINE VARIABLE d AS DATE. 
DEFINE VARIABLE d1 AS DATE. 
DEFINE VARIABLE d2 AS DATE. 
DEFINE VARIABLE i AS INTEGER.
  FOR EACH kontline WHERE kontline.betriebsnr = 1
    AND NOT (kontline.ankunft GT to-date)
    AND NOT (kontline.abreise LT from-date) 
    AND kontline.kontstatus = 1 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = kontline.gastnr 
      AND guest.name GE from-name AND guest.name LE to-name NO-LOCK 
    BY guest.name BY kontline.kontcode BY kontline.ankunft: 
    
    IF curr-code NE kontline.kontcode THEN 
    DO: 
      FIND FIRST usr WHERE usr.nr = kontline.bediener-nr NO-LOCK NO-ERROR. 
      curr-code = kontline.kontcode. 
      create k-list. 
      ASSIGN 
        k-list.gastnr = guest.gastnr 
        k-list.kontcode = curr-code 
        k-list.ankunft = kontline.ankunft 
        k-list.zikatnr = kontline.zikatnr 
        k-list.argt = kontline.arrangement 
        k-list.erwachs = kontline.erwachs 
        k-list.kind1 = kontline.kind1 
        k-list.ruecktage = kontline.ruecktage 
        k-list.overbooking = kontline.overbooking 
        k-list.abreise = kontline.abreise 
        k-list.useridanlage = kontline.useridanlage 
        k-list.resdat = kontline.resdat 
        k-list.bemerk = kontline.bemerk. 
      IF AVAILABLE usr THEN k-list.bediener-nr = usr.nr. 
    END. 
    ELSE k-list.abreise = kontline.abreise. 
    IF from-date GT kontline.ankunft THEN d1 = from-date. 
    ELSE d1 = kontline.ankunft. 
    IF to-date LT kontline.abreise THEN d2 = to-date. 
    ELSE d2 = kontline.abreise. 
    i = d1 - from-date. 
    DO d = d1 TO d2: 
      CREATE sum-list.
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = k-list.zikatnr 
        NO-LOCK NO-ERROR.
      ASSIGN
        sum-list.datum  = d
        sum-list.gastnr = kontline.gastnr
        sum-list.firma  = guest.NAME
        sum-list.kontcode = kontline.kontcode
        sum-list.zikatnr  = kontline.zikatnr
        sum-list.gloAnz   = kontline.zimmeranz
        sum-list.erwachs  = kontline.erwachs
        sum-list.kind1    = kontline.kind1
      .
      IF AVAILABLE zimkateg THEN  ASSIGN sum-list.kurzbez  = zimkateg.kurzbez.
      i = i + 1. 
      IF d GE kontline.ankunft AND d LE kontline.abreise THEN 
        k-list.zimmeranz[i] = kontline.zimmeranz. 
    END. 
  END. 
END. 
