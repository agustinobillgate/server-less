
DEFINE TEMP-TABLE k-list 
  FIELD gastnr      AS INTEGER 
  FIELD bediener-nr AS INTEGER 
  FIELD kontcode    AS CHAR
  FIELD global-flag AS LOGICAL INIT NO
  FIELD global-str  AS CHAR INIT ""
  FIELD ankunft     AS DATE 
  FIELD zikatnr     AS INTEGER 
  FIELD argt        AS CHAR 
  FIELD zimmeranz   AS INTEGER EXTENT 31 
  FIELD erwachs     AS INTEGER 
  FIELD kind1       AS INTEGER 
  FIELD ruecktage   AS INTEGER 
  FIELD overbooking AS INTEGER 
  FIELD abreise     AS DATE 
  FIELD useridanlage AS CHAR 
  FIELD resdate     AS DATE 
  FIELD bemerk      AS CHAR. 

DEFINE TEMP-TABLE res-list
  FIELD resNO    AS INTEGER
  FIELD reslinnr AS INTEGER
  FIELD flag     AS CHAR 
  FIELD count    AS INTEGER 
  FIELD s1       AS CHAR FORMAT "x(108)". 

DEFINE TEMP-TABLE output-list 
  FIELD reihe    AS INTEGER
  FIELD resNo    AS INTEGER INITIAL 0
  FIELD reslinnr AS INTEGER
  FIELD STR      AS CHAR FORMAT "x(123)". 

DEF TEMP-TABLE allot-list LIKE kontline.
DEF BUFFER usr FOR bediener.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER from-name      AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER to-name        AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER from-date      AS DATE     NO-UNDO.
DEF INPUT  PARAMETER to-date        AS DATE     NO-UNDO.
DEF INPUT  PARAMETER resFlag        AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER gFlag          AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER cFlag          AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER detailFlag     AS LOGICAL  NO-UNDO.
DEF INPUT  PARAMETER curr-rmType    AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR output-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "allotm-review". 

RUN create-list.

PROCEDURE create-list: 
DEFINE VARIABLE curr-reihe              AS INTEGER NO-UNDO.
DEFINE VARIABLE i                       AS INTEGER. 
DEFINE VARIABLE datum                   AS DATE. 
DEFINE VARIABLE ci-date                 AS DATE.
DEFINE VARIABLE count                   AS INTEGER. 
DEFINE VARIABLE anz1                    AS INTEGER EXTENT 31. 
DEFINE VARIABLE anz2                    AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz0                  AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz1                  AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz2                  AS INTEGER EXTENT 31. 
DEFINE VARIABLE avail-allotm            AS INTEGER EXTENT 31. 
DEFINE VARIABLE totavail-allotm         AS INTEGER EXTENT 31. 
DEFINE VARIABLE overbook                AS INTEGER EXTENT 31. 
DEFINE VARIABLE wday                    AS CHAR FORMAT "x(2)" EXTENT 8 
  INITIAL ["SU", "MO", "TU", "WE", "TH", "FR", "SA", "SU"]. 
 
  RUN htpdate.p (87, OUTPUT ci-date).
 
  DO i = 1 TO 31: 
    t-anz0[i] = 0. 
    t-anz1[i] = 0. 
    t-anz2[i] = 0. 
    avail-allotm[i] = 0. 
    totavail-allotm[i] = 0. 
    overbook[i] = 0. 
  END. 

  ASSIGN curr-reihe = 0.
  IF from-name = "" AND to-name = "zz" THEN RUN create-alllist. 
  ELSE RUN create-alist.
   
  IF NOT detailFlag THEN 
  DO:
    CREATE output-list. 
    ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = translateExtended( "Dates          :",lvCAREA,"") + " " + STRING(from-date) + " - " 
          + STRING(to-date). 
    CREATE output-list. 
    ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = "                 ". 
    
    datum = from-date. 
    DO WHILE datum LE to-date: 
      str = str + STRING(day(datum),"99 "). 
      datum = datum + 1. 
    END. 

    CREATE output-list. 
    ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = "                 ". 
    
    datum = from-date. 
    DO WHILE datum LE to-date: 
      str = str + wday[weekday(datum)] + " ". 
      datum = datum + 1. 
    END. 
  END.



  FOR EACH k-list, 
    FIRST guest WHERE guest.gastnr = k-list.gastnr NO-LOCK, 
    FIRST usr WHERE usr.nr = k-list.bediener-nr NO-LOCK 
    BY guest.name BY k-list.ankunft: 
 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = k-list.zikatnr 
      NO-LOCK NO-ERROR. 
 
    CREATE output-list. 
    ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = translateExtended( "Company  Name  :",lvCAREA,"") + " " + guest.name + ", " + guest.anredefirma. 
    /* &&& */
    IF NOT detailFlag THEN
    DO:
      output-list.str = output-list.str + "; " + translateExtended( "Code:",lvCAREA,"") + " " + k-list.kontcode. 
      IF AVAILABLE zimkateg THEN str = str + "; " + translateExtended( "RmType:",lvCAREA,"") + " " + zimkateg.kurzbez. 
      IF k-list.argt NE ""  THEN str = str + "; " + translateExtended( "Arg:",lvCAREA,"")    + " " + k-list.argt. 
      IF k-list.erwachs > 0 THEN str = str + "; " + translateExtended( "Pax:",lvCAREA,"")    + " " + STRING(k-list.erwachs). 
    END.
    ELSE 
    DO:
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = translateExtended( "Address        :",lvCAREA,"") + " " + guest.adresse1 + " " + guest.adresse2. 
    
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = translateExtended( "City           :",lvCAREA,"") + " " + guest.wohnort + " " + guest.plz. 
    
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.STR = translateExtended( "Allotm Code    :",lvCAREA,"") + " " + k-list.kontcode.
    
      IF k-list.global-flag THEN
        output-list.str = output-list.str + "[*]". 
      output-list.str = output-list.str + "         " + translateExtended ("RateCode :", lvCAREA,"") + " ".
      
      FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK: 
        str = str + guest-pr.CODE + "; ". 
      END.
    
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
      str = STRING(translateExtended( "Start   ",lvCAREA,""),"x(8)") + STRING(k-list.ankunft) + "  Pax " 
        + STRING(k-list.erwachs) + "/" + STRING(k-list.kind1) 
        + "    " + translateExtended( "ConfirmDays:",lvCAREA,"") + " ". 
      str = str + STRING(k-list.ruecktage) 
        + "    " + translateExtended( "Overbooking:",lvCAREA,"") + " " + STRING(k-list.overbooking). 
    
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = STRING(translateExtended( "Ending",lvCAREA,""),"x(8)") + STRING(k-list.abreise) + "  RmCat ". 

      IF AVAILABLE zimkateg THEN str = str + STRING(zimkateg.kurzbez, "x(6)"). 
      ELSE str = str + "      ". 
      str = str + "  " + translateExtended( "Arg",lvCAREA,"") + " " + STRING(k-list.argt, "x(5)") 
        + "  " + translateExtended( "ID",lvCAREA,"") + " " + STRING(usr.userinit) 
        + "  " + translateExtended( "ChgID",lvCAREA,"") + " " 
        + STRING(k-list.useridanlage, "x(2)") 
        + "  " + translateExtended( "Date",lvCAREA,"") + " " + STRING(k-list.resdat). 
      IF k-list.bemerk NE "" THEN 
      DO: 
        CREATE output-list. 
        ASSIGN 
          curr-reihe = curr-reihe + 1
          output-list.reihe = curr-reihe
          output-list.str = translateExtended( "Comment        :",lvCAREA,"") + " " + k-list.bemerk. 
      END. 

      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = translateExtended( "Dates          :",lvCAREA,"") + " " + STRING(from-date) + " - " 
          + STRING(to-date). 
    
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = "                 ". 
    
      datum = from-date. 
      DO WHILE datum LE to-date: 
        str = str + STRING(day(datum),"99 "). 
        datum = datum + 1. 
      END. 

      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = "                 ". 
    
      datum = from-date. 
      DO WHILE datum LE to-date: 
        str = str + wday[weekday(datum)] + " ". 
        datum = datum + 1. 
      END. 

      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
      DO i = 1 TO 109: 
        str = str + "-". 
      END. 
    END.

    CREATE output-list. 
    ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = STRING(translateExtended( "Allotment Room",lvCAREA,""),"x(16)"). 
    datum = from-date. 
    i = 1. 
    DO WHILE datum LE to-date: 
      IF datum GE k-list.ankunft AND datum LT k-list.abreise 
        AND datum GE (ci-date /*+ k-list.ruecktage*/) THEN 
      DO: 
        t-anz0[i] = t-anz0[i] + k-list.zimmeranz[i]. 
        str = str + STRING(k-list.zimmeranz[i],"-99"). 
      END. 
      ELSE str = str + " 00". 
      i = i + 1. 
      datum = datum + 1. 
    END. 
    DO i = 1 TO 31: 
      anz1[i] = 0. 
      anz2[i] = 0. 
    END. 
    count = 0. 
    FOR EACH res-line WHERE res-line.kontignr GT 0 
      AND res-line.gastnr =  k-list.gastnr AND res-line.active-flag LT 2 
      AND NOT (res-line.ankunft GT to-date) 
      AND NOT (res-line.abreise LT from-date) 
      AND res-line.resstatus LT 11 
      AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
      FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
      AND kontline.kontcode = k-list.kontcode 
      AND kontline.kontstat = 1 NO-LOCK BY res-line.ankunft 
      BY res-line.abreise BY res-line.resnr: 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
      IF resflag AND res-line.active-flag = 0 THEN 
      DO: 
        create res-list. 
          res-list.flag = "r". 
          count = count + 1.
          ASSIGN
            res-list.count = count
            res-list.resNo = res-line.resnr
            res-list.reslinnr = res-line.reslinnr
            s1 = "   " + translateExtended( "ResNo",lvCAREA,"") + " " + STRING(res-line.resnr, ">>>>>>9") 
              + " " + translateExtended( "Arrival",lvCAREA,"") + " " + STRING(res-line.ankunft) 
              + "  " + translateExtended( "Qty",lvCAREA,"") + " " + STRING(res-line.zimmeranz,"99") + "  Pax " 
              + STRING(res-line.erwachs) + "/" + STRING(res-line.kind1) 
              + "  " + translateExtended( "Departure",lvCAREA,"") + " " + STRING(res-line.abreise) 
              + "  " + translateExtended( "ID",lvCAREA,"") + " " + STRING(reservation.useridanlage,"x(2)") + "  ChgID " 
              + STRING(res-line.changed-id, "x(2)")
        . 
        res-list.s1 = STRING(reservation.NAME,"x(22)") + "  " + res-list.s1.

        IF res-line.bemerk NE "" THEN 
        DO: 
          create res-list. 
          count = count + 1. 
          res-list.flag = "r". 
          s1 = translateExtended( "Comment        :",lvCAREA,"") + " " + res-line.bemerk. 
        END. 
      END. 
      IF gflag AND res-line.active-flag = 2 THEN 
      DO: 
        create res-list. 
        ASSIGN
          res-list.resNo = res-line.resnr
          res-list.reslinnr = res-line.reslinnr
          res-list.flag = "g" 
          count = count + 1
          res-list.count = count 
          s1 = "   " + translateExtended( "ResNo",lvCAREA,"") + " " + STRING(res-line.resnr, ">>>>>>9") 
            + " " + translateExtended( "Arrival",lvCAREA,"") + " " + STRING(res-line.ankunft) 
            + "  " + translateExtended( "Qty",lvCAREA,"") + " " + STRING(res-line.zimmeranz,"99") + "  Pax " 
            + STRING(res-line.erwachs) + "/" + STRING(res-line.kind1) 
            + "  " + translateExtended( "Departure",lvCAREA,"") + " " + STRING(res-line.abreise) 
            + "  " + translateExtended( "ID",lvCAREA,"") + " " + STRING(reservation.useridanlage,"x(2)") + "  ChgID " 
            + STRING(res-line.changed-id, "x(2)")
        . 
        IF res-line.bemerk NE "" THEN 
        DO: 
          create res-list. 
          count = count + 1. 
          res-list.flag = "g". 
          s1 = translateExtended( "Comment        :",lvCAREA,"") + " " + res-line.bemerk. 
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
 
    CREATE output-list. 
    ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = STRING(translateExtended( "Used Allotment",lvCAREA,""),"x(16)"). 
    
    datum = from-date. 
    i = 1. 
    DO WHILE datum LE to-date: 
      str = str + STRING(anz1[i],"-99"). 
      i = i + 1. 
      datum = datum + 1. 
    END. 

    IF detailFlag THEN
    DO:
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = STRING(translateExtended( "Not used      :",lvCAREA,""),"x(16)"). 
    
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
        IF anz2[i] GT 0 THEN str = str + STRING(anz2[i],"-99"). 
        ELSE str = str + " 00". 
        i = i + 1. 
        datum = datum + 1. 
      END. 
    END.

    CREATE output-list. 
    ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = STRING(translateExtended( "Available     :",lvCAREA,""),"x(16)"). 
    
    datum = from-date. 
    i = 1. 
    DO WHILE datum LE to-date: 
      IF datum GE (ci-date + k-list.ruecktage) THEN 
      DO: 
        IF anz2[i] GT 0 THEN 
        DO: 
          avail-allotm[i] = anz2[i]. 
          totavail-allotm[i] = totavail-allotm[i] + anz2[i]. 
          str = str + STRING(avail-allotm[i],"-99"). 
        END. 
        ELSE 
        DO: 
          avail-allotm[i] = 0. 
          str = str + " 00". 
        END. 
      END. 
      ELSE 
      DO: 
        avail-allotm[i] = 0. 
        str = str + " 00". 
      END. 
      i = i + 1. 
      datum = datum + 1. 
    END. 
 
    IF detailFlag THEN
    DO:
      CREATE output-list. 
      ASSIGN 
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = STRING(translateExtended( "Overbooking   :",lvCAREA,""),"x(16)"). 
    
      datum = from-date. 
      i = 1. 
      DO WHILE datum LE to-date: 
        IF datum GE (ci-date + k-list.ruecktage) THEN 
        DO: 
          IF anz2[i] LT 0 THEN 
          DO: 
            overbook[i] = - anz2[i]. 
            str = str + STRING(overbook[i],"-99"). 
          END. 
          ELSE 
          DO: 
            overbook[i] = 0. 
            str = str + " 00". 
          END. 
        END. 
        ELSE 
        DO: 
          overbook[i] = 0. 
          str = str + " 00". 
        END. 
        i = i + 1. 
        datum = datum + 1. 
      END. 
    END.

    IF resflag THEN 
    DO: 
      i = 1. 
      CREATE output-list. 
      ASSIGN 
          curr-reihe = curr-reihe + 1
          output-list.reihe = curr-reihe
          output-list.str = "Reservations:". 
      
      FOR EACH res-list WHERE res-list.flag = "r" NO-LOCK BY res-list.count: 
        IF i GT 1 THEN 
        DO: 
          CREATE output-list. 
          ASSIGN
              curr-reihe = curr-reihe + 1
              output-list.reihe = curr-reihe
              output-list.resNo = res-list.resNo
              output-list.reslinnr = res-list.reslinnr
              output-list.str = "             " + res-list.s1. 
        END. 
        ELSE
        ASSIGN
            output-list.resNo = res-list.resNo
            output-list.reslinnr = res-list.reslinnr
            output-list.str = output-list.str + res-list.s1. 
        i = i + 1. 
      END. 
    END. 
    IF gflag THEN 
    DO: 
      i = 1. 

      CREATE output-list. 
      ASSIGN
          curr-reihe = curr-reihe + 1
          output-list.reihe = curr-reihe
          output-list.str = "Residents   :". 
      
      FOR EACH res-list WHERE res-list.flag = "g" NO-LOCK BY res-list.count: 
        IF i GT 1 THEN 
        DO: 
          CREATE output-list. 
          ASSIGN
              curr-reihe = curr-reihe + 1
              output-list.reihe = curr-reihe
              output-list.resNo = res-list.resNo
              output-list.reslinnr = res-list.reslinnr
              output-list.str = "             " + res-list.s1. 
        END. 
        ELSE
        ASSIGN
            curr-reihe = curr-reihe + 1
            output-list.reihe = curr-reihe
            output-list.resNo = res-list.resNo
            output-list.reslinnr = res-list.reslinnr
            output-list.str = output-list.str + res-list.s1. 
        i = i + 1. 
      END. 
    END. 
    IF cflag THEN 
    DO: 
      FOR EACH res-line WHERE res-line.kontignr GT 0 
        AND res-line.resstatus = 9 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
        FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
        AND kontline.kontcode = k-list.kontcode 
        AND kontline.kontstat = 1 NO-LOCK 
        BY res-line.ankunft BY res-line.abreise BY res-line.resnr: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
        create res-list. 
        ASSIGN
          res-list.flag = "c"
          count = count + 1
          res-list.count = count 
          res-list.resNo = - res-line.resnr
          res-list.reslinnr = res-line.reslinnr
          s1 = "   " + translateExtended( "ResNo",lvCAREA,"") + " " + STRING(res-line.resnr, ">>>>>>9") 
            + " " + translateExtended( "Arrival",lvCAREA,"") + " " + STRING(res-line.ankunft) 
            + "  " + translateExtended( "Qty",lvCAREA,"") + " " + STRING(res-line.zimmeranz,"99") + "  Pax " 
            + STRING(res-line.erwachs) + "/" + STRING(res-line.kind1) 
            + "  " + translateExtended( "Departure",lvCAREA,"") + " " + STRING(res-line.abreise) 
            + "  " + translateExtended( "ID",lvCAREA,"") + " " + STRING(reservation.useridanlage,"x(2)") + "  ChgID " 
            + STRING(res-line.changed-id, "x(2)")
        . 
        res-list.s1 = STRING(reservation.NAME,"x(22)") + "  " + res-list.s1.
        
        IF res-line.bemerk NE "" THEN 
        DO: 
          create res-list. 
          count = count + 1. 
          res-list.flag = "r". 
          s1 = translateExtended( "Comment        :",lvCAREA,"") + " " + res-line.bemerk. 
        END. 
      END. 
      i = 1. 
      CREATE output-list. 
      ASSIGN
          curr-reihe = curr-reihe + 1
          output-list.reihe = curr-reihe
          output-list.str = translateExtended( "Cancelled   :",lvCAREA,""). 
      
      FOR EACH res-list WHERE res-list.flag = "c" NO-LOCK BY res-list.count: 
        IF i GT 1 THEN 
        DO: 
          CREATE output-list. 
          ASSIGN
              curr-reihe = curr-reihe + 1
              output-list.reihe = curr-reihe
              output-list.resNo = res-list.resNo
              output-list.reslinnr = res-list.reslinnr
              output-list.str = "             " + res-list.s1. 
        END. 
        ELSE
        ASSIGN
            output-list.resNo = res-list.resNo
            output-list.reslinnr = res-list.reslinnr
            output-list.str = output-list.str + res-list.s1. 
        i = i + 1. 
      END. 
    END. 
    
    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO i = 1 TO 109: 
      str = str + "=". 
    END. 
    
    IF detailFlag THEN
    DO:
      CREATE output-list. 
      ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    END.
  END.
 
  count = 2. 
  DO i = 1 TO 31: 
    IF t-anz0[i] GE 100 THEN count = 3. 
  END. 
  IF count = 3 THEN 
  DO: 
    i = 1. 
    datum = from-date. 
    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN str = STRING(translateExtended( "Total Allotm",lvCAREA,""),"x(12)") + STRING(t-anz0[i], "->>>>9"). 
      ELSE str = str + STRING(t-anz0[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
    i = 2. 
    datum = from-date + 1. 

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = "               ". 
    
    DO WHILE datum LE to-date: 
      str = str + STRING(t-anz0[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
  END. 
  ELSE 
  DO: 
    i = 1. 
    datum = from-date.

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN str = STRING(translateExtended( "Total Allotm",lvCAREA,""),"x(16)") + STRING(t-anz0[i], "->9"). 
      ELSE str = str + STRING(t-anz0[i], "->9"). 
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

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN str = STRING(translateExtended( "Used Allotm",lvCAREA,""),"x(16)") + STRING(t-anz1[i], "->>>>9"). 
      ELSE str = str + STRING(t-anz1[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
    i = 2. 
    datum = from-date + 1.

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = "         ". 
    DO WHILE datum LE to-date: 
      str = str + STRING(t-anz1[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
  END. 
  ELSE 
  DO: 
    i = 1. 
    datum = from-date. 
    
    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN str = STRING(translateExtended( "Used Allotm   :",lvCAREA,""),"x(16)") + STRING(t-anz1[i], "->9"). 
      ELSE str = str + STRING(t-anz1[i], "->9"). 
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
    
    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF t-anz2[i] GT 0 THEN 
      DO: 
        IF i LE 1 THEN str = STRING(translateExtended( "Not used   :",lvCAREA,""),"x(16)") + STRING(t-anz2[i], "->>>>9"). 
        ELSE str = str + STRING(t-anz2[i], "->>>>9"). 
      END. 
      ELSE 
      DO: 
        IF i LE 1 THEN str = STRING(translateExtended( "Not used   :",lvCAREA,""),"x(16)") + STRING(0, "->>>>9"). 
        ELSE str = str + STRING(0, "->>>>9"). 
      END. 
      i = i + 2. 
      datum = datum + 2. 
    END. 
    i = 2. 
    datum = from-date + 1. 

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe
        output-list.str = "         ". 
    DO WHILE datum LE to-date: 
      str = str + STRING(t-anz2[i], "->>>>9"). 
      i = i + 2. 
      datum = datum + 2. 
    END. 
    i = 1. 
    datum = from-date.

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN str = STRING(translateExtended( "Avail Allotm  :",lvCAREA,""),"x(15)") + STRING(totavail-allotm[i], "->9"). 
      ELSE str = str + STRING(totavail-allotm[i], "->9"). 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
  ELSE 
  DO: 
    i = 1. 
    datum = from-date.

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF t-anz2[i] GT 0 THEN 
      DO: 
        IF i LE 1 THEN str = STRING(translateExtended( "Not used      :",lvCAREA,""),"x(16)") + STRING(t-anz2[i], "->9"). 
        ELSE str = str + STRING(t-anz2[i], "->9"). 
      END. 
      ELSE str = str + STRING(0, "->9"). 
      i = i + 1. 
      datum = datum + 1. 
    END. 
    i = 1. 
    datum = from-date.

    CREATE output-list. 
    ASSIGN
        curr-reihe = curr-reihe + 1
        output-list.reihe = curr-reihe.
    DO WHILE datum LE to-date: 
      IF i LE 1 THEN str = STRING(translateExtended( "Avail Allotm  :",lvCAREA,""),"x(16)") + STRING(totavail-allotm[i], "->9"). 
      ELSE str = str + STRING(totavail-allotm[i], "->9"). 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
END. 
 
PROCEDURE create-alllist: 
DEFINE VARIABLE curr-code   AS CHAR INITIAL "". 
DEFINE VARIABLE d           AS DATE. 
DEFINE VARIABLE d1          AS DATE. 
DEFINE VARIABLE d2          AS DATE. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  FOR EACH kontline WHERE kontline.betriebsnr = 0 
    AND kontline.kontstat = 1  
    AND NOT (kontline.ankunft GT to-date)
    AND NOT (kontline.abreise LT from-date) NO-LOCK, 
    FIRST guest WHERE guest.gastnr = kontline.gastnr NO-LOCK, 
    FIRST usr WHERE usr.nr = kontline.bediener-nr NO-LOCK 
    BY guest.name BY kontline.kontcode BY kontline.ankunft: 

    do-it = YES.
    IF curr-rmType MATCHES ("*-ALL-*") THEN .
    ELSE IF kontline.zikatnr = 0 THEN .
    ELSE DO:
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = curr-rmType NO-LOCK.
      do-it = kontline.zikatnr = zimkateg.zikatnr.
    END.
    IF do-it THEN
    DO:
      IF curr-code NE kontline.kontcode THEN 
      DO: 
        curr-code = kontline.kontcode. 
        CREATE k-list. 
        ASSIGN 
          k-list.gastnr = guest.gastnr 
          k-list.bediener-nr = usr.nr 
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
          k-list.bemerk = kontline.bemerk
        . 
        FIND FIRST queasy WHERE queasy.KEY = 147 
            AND queasy.number1 = kontline.gastnr
            AND queasy.char1 = kontline.kontcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        ASSIGN
            k-list.global-flag = YES
            k-list.global-str  = queasy.char3
        .

      END. 
      ELSE k-list.abreise = kontline.abreise. 
      IF from-date GT kontline.ankunft THEN d1 = from-date. 
      ELSE d1 = kontline.ankunft. 
      IF to-date LT kontline.abreise THEN d2 = to-date. 
      ELSE d2 = kontline.abreise. 
      i = d1 - from-date. 
      DO d = d1 TO d2: 
        i = i + 1. 
        IF d GE kontline.ankunft AND d LE kontline.abreise THEN 
          k-list.zimmeranz[i] = kontline.zimmeranz. 
      END. 
    END. 
  END. 
END.

PROCEDURE create-alist: 
DEFINE VARIABLE curr-code   AS CHAR INITIAL "". 
DEFINE VARIABLE d           AS DATE. 
DEFINE VARIABLE d1          AS DATE. 
DEFINE VARIABLE d2          AS DATE. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.

  FOR EACH kontline WHERE kontline.betriebsnr = 0 
    AND kontline.kontstat = 1 
    AND NOT (kontline.ankunft GT to-date)
    AND NOT (kontline.abreise LT from-date) NO-LOCK, 
    FIRST guest WHERE guest.gastnr = kontline.gastnr 
      AND guest.name GE from-name AND guest.name LE to-name NO-LOCK, 
    FIRST usr WHERE usr.nr = kontline.bediener-nr NO-LOCK 
    BY guest.name BY kontline.kontcode BY kontline.ankunft:

    do-it = YES.
    IF curr-rmType MATCHES ("*-ALL-*") THEN .
    ELSE IF kontline.zikatnr = 0 THEN .
    ELSE DO:
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = curr-rmType NO-LOCK.
      do-it = kontline.zikatnr = zimkateg.zikatnr.
    END.
    IF do-it THEN
    DO:
      IF curr-code NE kontline.kontcode THEN 
      DO: 
        curr-code = kontline.kontcode. 
        CREATE k-list. 
        ASSIGN 
          k-list.gastnr = guest.gastnr 
          k-list.bediener-nr = usr.nr 
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
          k-list.bemerk = kontline.bemerk
        . 
        FIND FIRST queasy WHERE queasy.KEY = 147 
            AND queasy.number1 = kontline.gastnr
            AND queasy.char1 = kontline.kontcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        ASSIGN
            k-list.global-flag = YES
            k-list.global-str  = queasy.char3
        .
      END. 
      ELSE k-list.abreise = kontline.abreise. 
      IF from-date GT kontline.ankunft THEN d1 = from-date. 
      ELSE d1 = kontline.ankunft. 
      IF to-date LT kontline.abreise THEN d2 = to-date. 
      ELSE d2 = kontline.abreise. 
      i = d1 - from-date. 
      DO d = d1 TO d2: 
        i = i + 1. 
        IF d GE kontline.ankunft AND d LE kontline.abreise THEN 
          k-list.zimmeranz[i] = kontline.zimmeranz. 
      END. 
    END. 
  END. 
END.
