DEFINE TEMP-TABLE str-list 
  FIELD zero-rate   AS LOGICAL INITIAL NO 
  FIELD c-recid     AS INTEGER 
  FIELD destination AS CHAR FORMAT "x(16)"          COLUMN-LABEL "Destination" 
  FIELD rechnr      AS INTEGER FORMAT ">>>>>>>>>"   COLUMN-LABEL "BillNo" 
  /*FIELD s           AS CHAR FORMAT "x(135)"*/
  FIELD nebenstelle AS CHAR FORMAT "x(6)"           LABEL "ExtNo"
  FIELD datum       AS DATE                         LABEL "Date"
  FIELD rufnummer   AS CHAR FORMAT "x(16)"          LABEL "Dialed Number"
  FIELD username    AS CHAR FORMAT "x(16)"          LABEL "User Name"
  FIELD guest-rate  AS DECIMAL  FORMAT ">>>,>>>,>>9.99"                    COLUMN-LABEL "Guest Rate"
  FIELD pabx-rate   AS DECIMAL  FORMAT ">>>,>>>,>>9.99"                    COLUMN-LABEL "PABX Rate"
  FIELD zeit        AS CHARACTER
  FIELD dauer       AS CHARACTER
  FIELD zinr        AS CHARACTER
  FIELD impulse     AS INTEGER
  FIELD leitung     AS INTEGER
  FIELD sequence    AS INTEGER
  FIELD print       AS CHAR
  . 

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER last-sort AS INTEGER.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER from-ext  AS CHAR.
DEFINE INPUT PARAMETER to-ext    AS CHAR.
DEFINE INPUT PARAMETER stattype  AS INTEGER.
DEFINE INPUT PARAMETER price-decimal    AS INTEGER.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL.
DEFINE INPUT PARAMETER fr-number AS CHAR.
DEFINE INPUT PARAMETER to-number AS CHAR.
DEFINE INPUT PARAMETER dialed-nr AS CHAR.
DEFINE OUTPUT PARAMETER amount1   AS DECIMAL. 
DEFINE OUTPUT PARAMETER amount2   AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE OUTPUT PARAMETER tot-pulse AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE ext-amt1  AS DECIMAL. 
DEFINE VARIABLE ext-amt2  AS DECIMAL. 
DEFINE VARIABLE i         AS INTEGER. 
DEFINE VARIABLE d         AS DATE NO-UNDO. 
DEFINE VARIABLE last-ext  AS CHAR. 
DEFINE VARIABLE prstr     AS CHAR FORMAT "x(3)" EXTENT 2 INITIAL ["NO", "YES"]. 

IF case-type = 0 THEN RUN create-list.
ELSE IF case-type = 1 THEN RUN create-list1.
ELSE IF case-type = 2 THEN RUN create-list2.

PROCEDURE create-list:

IF last-sort = 1 THEN 
DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        USE-INDEX nebenst_ix NO-LOCK BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
      ELSE 
      DO:
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE 
    DO: 
      DO d = to-date TO from-date BY -1: 
        FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum = d AND calls.zeit GE 0 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
    END. 
END. 
 
/* BY Extension */ 
ELSE IF last-sort = 2 THEN 
DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        USE-INDEX nebenst_ix NO-LOCK BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        last-ext = "". 
        ext-amt1 = 0. 
        ext-amt2 = 0. 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.nebenstelle 
          BY calls.zeit descending: 
          IF last-ext = "" THEN last-ext = calls.nebenstelle. 
          IF last-ext NE calls.nebenstelle THEN 
          DO: 
            create str-list. 
            /*DO i = 1 TO 34: 
              str-list.s = str-list.s + " ". 
            END. 
            str-list.s = str-list.s 
              + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
            str-list.destination = "T O T A L  ". 
            IF price-decimal = 0 THEN 
            DO: 
              IF ext-amt1 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
              ELSE
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            END. 
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            IF double-currency OR price-decimal NE 0 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
            DO: 
              IF ext-amt2 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
            END. 
            /*str-list.s = str-list.s + STRING(" ", "x(12)") 
              + STRING(tot-pulse,">>>>>9").*/ 
            str-list.impulse = tot-pulse. 
 
            create str-list. 
            last-ext = calls.nebenstelle. 
            ext-amt1 = 0. 
            ext-amt2 = 0. 
          END. 
          ext-amt1 = ext-amt1 + calls.pabxbetrag. 
          ext-amt2 = ext-amt2 + calls.gastbetrag. 
          RUN create-record. 
        END. 
        create str-list. 
        /*DO i = 1 TO 34: 
          str-list.s = str-list.s + " ". 
        END.*/ 
        /*str-list.s = str-list.s 
          + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
        str-list.destination = "T O T A L  ". 
        IF price-decimal = 0 THEN 
        DO: 
          IF ext-amt1 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        END. 
        ELSE
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        IF double-currency OR price-decimal NE 0 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
        END. 
        /*str-list.s = str-list.s + STRING(" ", "x(12)") 
          + STRING(tot-pulse,">>>>>9").*/ 
        str-list.impulse = tot-pulse. 
        create str-list. 
      END. 
      ELSE 
      DO: 
        last-ext = "". 
        ext-amt1 = 0. 
        ext-amt2 = 0. 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.nebenstelle 
          BY calls.zeit descending: 
          IF last-ext NE calls.nebenstelle THEN 
          DO: 
            create str-list. 
            /*DO i = 1 TO 34: 
              str-list.s = str-list.s + " ". 
            END.*/ 
            /*str-list.s = str-list.s 
              + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
            str-list.destination = "T O T A L  ". 
            IF price-decimal = 0 THEN 
            DO: 
              IF ext-amt1 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            END. 
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            IF double-currency OR price-decimal NE 0 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
            DO: 
              IF ext-amt2 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
            END. 
            /*str-list.s = str-list.s + STRING(" ", "x(12)") 
              + STRING(tot-pulse,">>>>>9").*/ 
            str-list.impulse = tot-pulse. 
            create str-list. 
            last-ext = calls.nebenstelle. 
            ext-amt1 = 0. 
            ext-amt2 = 0. 
          END. 
          ext-amt1 = ext-amt1 + calls.pabxbetrag. 
          ext-amt2 = ext-amt2 + calls.gastbetrag. 
          RUN create-record. 
        END. 
        create str-list. 
        /*DO i = 1 TO 34: 
          str-list.s = str-list.s + " ". 
        END.*/ 
        /*str-list.s = str-list.s 
          + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
        str-list.destination = "T O T A L  ". 
        IF price-decimal = 0 THEN 
        DO: 
          IF ext-amt1 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        END. 
        ELSE 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        IF double-currency OR price-decimal NE 0 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
        END. 
        /*str-list.s = str-list.s + STRING(" ", "x(12)") 
          + STRING(tot-pulse,">>>>>9").*/ 
        str-list.impulse = tot-pulse. 
        create str-list. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
END. 
ELSE 
DO: 
/** Print Total per extension **/ 
      last-ext = "". 
      ext-amt1 = 0. 
      ext-amt2 = 0. 
 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.nebenstelle 
        BY calls.datum descending BY calls.zeit descending: 
        IF last-ext = "" THEN last-ext = calls.nebenstelle. 
        IF last-ext NE calls.nebenstelle THEN 
        DO: 
          create str-list. 
          /*DO i = 1 TO 34: 
            str-list.s = str-list.s + " ". 
          END.*/ 
          /*str-list.s = str-list.s 
            + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
          str-list.destination = "T O T A L  ". 
          IF price-decimal = 0 THEN 
          DO: 
            IF ext-amt1 LE 999999999 THEN 
                ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
            ELSE 
                ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
          END. 
          ELSE
              ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
          IF double-currency OR price-decimal NE 0 THEN 
              ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                  str-list.guest-rate = ext-amt2.
          ELSE 
          DO: 
            IF ext-amt2 LE 999999999 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
          END. 
          /*str-list.s = str-list.s + STRING(" ", "x(12)") 
            + STRING(tot-pulse,">>>>>9").*/ 
          str-list.impulse = tot-pulse. 
          create str-list. 
          last-ext = calls.nebenstelle. 
          ext-amt1 = 0. 
          ext-amt2 = 0. 
        END. 
        ext-amt1 = ext-amt1 + calls.pabxbetrag. 
        ext-amt2 = ext-amt2 + calls.gastbetrag. 
        RUN create-record. 
      END. 
      create str-list. 
      /*DO i = 1 TO 34: 
        str-list.s = str-list.s + " ". 
      END.*/ 
      /*str-list.s = str-list.s 
        + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
      str-list.destination = "T O T A L  ". 
      IF price-decimal = 0 THEN 
      DO: 
        IF ext-amt1 LE 999999999 THEN 
            ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
              /*str-list.guest-rate = ext-amt1.*/
              str-list.pabx-rate = ext-amt1.
        ELSE 
            ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
              /*str-list.guest-rate = ext-amt1.*/
              str-list.pabx-rate = ext-amt1.
      END. 
      ELSE 
          ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
              /*str-list.guest-rate = ext-amt1.*/
              str-list.pabx-rate = ext-amt1.
      IF double-currency OR price-decimal NE 0 THEN 
          ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
              str-list.guest-rate = ext-amt2.
      ELSE 
      DO: 
        IF ext-amt2 LE 999999999 THEN 
            ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
              str-list.guest-rate = ext-amt2.
        ELSE 
            ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
              str-list.guest-rate = ext-amt2.
      END. 
      /*str-list.s = str-list.s + STRING(" ", "x(12)") 
        + STRING(tot-pulse,">>>>>9").*/ 
      str-list.impulse = tot-pulse. 
      create str-list. 
    END. 
  END. 
 
  ELSE IF last-sort = 3 THEN 
  DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        USE-INDEX nebenst_ix NO-LOCK 
        BY calls.rufnummer BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.rufnummer 
          BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
      ELSE 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
          BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
        BY calls.datum descending BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
        BY calls.datum descending BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
END. 
END.

PROCEDURE create-list1:
IF last-sort = 1 THEN 
DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX nebenst_ix NO-LOCK BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
      ELSE 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
END. 
 
/* BY Extension */ 
ELSE IF last-sort = 2 THEN 
DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX nebenst_ix NO-LOCK BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        last-ext = "". 
        ext-amt1 = 0. 
        ext-amt2 = 0. 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.nebenstelle 
          BY calls.zeit descending: 
          IF last-ext = "" THEN last-ext = calls.nebenstelle. 
          IF last-ext NE calls.nebenstelle THEN 
          DO: 
            create str-list. 
            /*DO i = 1 TO 34: 
              str-list.s = str-list.s + " ". 
            END.*/ 
            /*str-list.s = str-list.s 
              + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
            str-list.destination = "T O T A L  ". 
            IF price-decimal = 0 THEN 
            DO: 
              IF ext-amt1 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            END. 
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            IF double-currency OR price-decimal NE 0 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
            DO: 
              IF ext-amt2 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
            END. 
            /*str-list.s = str-list.s + STRING(" ", "x(12)") 
              + STRING(tot-pulse,">>>>>9").*/ 
            str-list.impulse = tot-pulse. 
            create str-list. 
            last-ext = calls.nebenstelle. 
            ext-amt1 = 0. 
            ext-amt2 = 0. 
          END. 
          ext-amt1 = ext-amt1 + calls.pabxbetrag. 
          ext-amt2 = ext-amt2 + calls.gastbetrag. 
          RUN create-record. 
        END. 
        create str-list. 
        /*DO i = 1 TO 34: 
          str-list.s = str-list.s + " ". 
        END.*/ 
        /*str-list.s = str-list.s 
          + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
        str-list.destination = "T O T A L  ". 
        IF price-decimal = 0 THEN 
        DO: 
          IF ext-amt1 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        END. 
        ELSE 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        IF double-currency OR price-decimal NE 0 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
          ELSE
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
        END. 
        /*str-list.s = str-list.s + STRING(" ", "x(12)") 
          + STRING(tot-pulse,">>>>>9").*/ 
        str-list.impulse = tot-pulse. 
        create str-list. 
      END. 
      ELSE 
      DO: 
        last-ext = "". 
        ext-amt1 = 0. 
        ext-amt2 = 0. 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.nebenstelle 
          BY calls.zeit descending: 
          IF last-ext NE calls.nebenstelle THEN 
          DO: 
            create str-list. 
            /*DO i = 1 TO 34: 
              str-list.s = str-list.s + " ". 
            END.*/ 
            /*str-list.s = str-list.s 
              + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
            str-list.destination = "T O T A L  ". 
            IF price-decimal = 0 THEN 
            DO: 
              IF ext-amt1 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            END. 
            ELSE
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            IF double-currency OR price-decimal NE 0 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
            DO: 
              IF ext-amt2 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
            END. 
            /*str-list.s = str-list.s + STRING(" ", "x(12)") 
              + STRING(tot-pulse,">>>>>9").*/ 
            str-list.impulse = tot-pulse. 
            create str-list. 
            last-ext = calls.nebenstelle. 
            ext-amt1 = 0. 
            ext-amt2 = 0. 
          END. 
          ext-amt1 = ext-amt1 + calls.pabxbetrag. 
          ext-amt2 = ext-amt2 + calls.gastbetrag. 
          RUN create-record. 
        END. 
        create str-list. 
        /*DO i = 1 TO 34: 
          str-list.s = str-list.s + " ". 
        END.*/ 
        /*str-list.s = str-list.s 
          + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
        str-list.destination = "T O T A L  ". 
        IF price-decimal = 0 THEN 
        DO: 
          IF ext-amt1 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        END. 
        ELSE 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        IF double-currency OR price-decimal NE 0 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
        END. 
        /*str-list.s = str-list.s + STRING(" ", "x(12)") 
          + STRING(tot-pulse,">>>>>9").*/ 
        str-list.impulse = tot-pulse. 
        create str-list. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
END. 
ELSE 
DO: 
/** Print Total per extension **/ 
      last-ext = "". 
      ext-amt1 = 0. 
      ext-amt2 = 0. 
 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.nebenstelle 
        BY calls.datum descending BY calls.zeit descending: 
        IF last-ext = "" THEN last-ext = calls.nebenstelle. 
        IF last-ext NE calls.nebenstelle THEN 
        DO: 
          create str-list. 
          /*DO i = 1 TO 34: 
            str-list.s = str-list.s + " ". 
          END.*/ 
          /*str-list.s = str-list.s 
            + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
          str-list.destination = "T O T A L  ". 
          IF price-decimal = 0 THEN 
          DO: 
            IF ext-amt1 LE 999999999 THEN 
                ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
            ELSE 
                ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
          END. 
          ELSE 
              ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
          IF double-currency OR price-decimal NE 0 THEN 
              ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                  str-list.guest-rate = ext-amt2.
          ELSE 
          DO: 
            IF ext-amt2 LE 999999999 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
          END. 
          /*str-list.s = str-list.s + STRING(" ", "x(12)") 
            + STRING(tot-pulse,">>>>>9").*/ 
          str-list.impulse = tot-pulse. 
          create str-list. 
          last-ext = calls.nebenstelle. 
          ext-amt1 = 0. 
          ext-amt2 = 0. 
        END. 
        ext-amt1 = ext-amt1 + calls.pabxbetrag. 
        ext-amt2 = ext-amt2 + calls.gastbetrag. 
        RUN create-record. 
      END. 
      create str-list. 
      /*DO i = 1 TO 34: 
        str-list.s = str-list.s + " ". 
      END.*/ 
      /*str-list.s = str-list.s 
        + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
      str-list.destination = "T O T A L  ". 
      IF price-decimal = 0 THEN 
      DO: 
        IF ext-amt1 LE 999999999 THEN 
            ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
              /*str-list.guest-rate = ext-amt1.*/
              str-list.pabx-rate = ext-amt1.
       ELSE 
            ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
              /*str-list.guest-rate = ext-amt1.*/
              str-list.pabx-rate = ext-amt1.
      END. 
      ELSE 
          ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
              /*str-list.guest-rate = ext-amt1.*/
              str-list.pabx-rate = ext-amt1.
      IF double-currency OR price-decimal NE 0 THEN 
          ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
              str-list.guest-rate = ext-amt2.
      ELSE 
      DO: 
        IF ext-amt2 LE 999999999 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
      END. 
      /*str-list.s = str-list.s + STRING(" ", "x(12)") 
        + STRING(tot-pulse,">>>>>9").*/ 
      str-list.impulse = tot-pulse. 
      create str-list. 
    END. 
END. 
 
ELSE IF last-sort = 3 THEN 
DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX nebenst_ix NO-LOCK 
        BY calls.rufnummer BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.rufnummer 
          BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
      ELSE 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
          BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
        BY calls.datum descending BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer GE fr-number AND calls.rufnummer LT to-number 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
        BY calls.datum descending BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
  END. 
END.


PROCEDURE create-list2:
  IF last-sort = 1 THEN 
  DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX nebenst_ix NO-LOCK BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer = dialed-nr 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
      ELSE 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer = dialed-nr 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
  END. 
 
/* BY Extension */ 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX nebenst_ix NO-LOCK BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        last-ext = "". 
        ext-amt1 = 0. 
        ext-amt2 = 0. 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer = dialed-nr 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.nebenstelle 
          BY calls.zeit descending: 
          IF last-ext = "" THEN last-ext = calls.nebenstelle. 
          IF last-ext NE calls.nebenstelle THEN 
          DO: 
            create str-list. 
            /*DO i = 1 TO 34: 
              str-list.s = str-list.s + " ". 
            END.*/ 
            /*str-list.s = str-list.s 
              + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
            str-list.destination = "T O T A L  ". 
            IF price-decimal = 0 THEN 
            DO: 
              IF ext-amt1 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            END. 
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            IF double-currency OR price-decimal NE 0 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
            DO: 
              IF ext-amt2 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
            END. 
            /*str-list.s = str-list.s + STRING(" ", "x(12)") 
              + STRING(tot-pulse,">>>>>9").*/ 
            str-list.impulse = tot-pulse. 
            create str-list. 
            last-ext = calls.nebenstelle. 
            ext-amt1 = 0. 
            ext-amt2 = 0. 
          END. 
          ext-amt1 = ext-amt1 + calls.pabxbetrag. 
          ext-amt2 = ext-amt2 + calls.gastbetrag. 
          RUN create-record. 
        END. 
        create str-list. 
        /*DO i = 1 TO 34: 
          str-list.s = str-list.s + " ". 
        END.*/ 
        /*str-list.s = str-list.s 
          + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
        str-list.destination = "T O T A L  ". 
        IF price-decimal = 0 THEN 
        DO: 
          IF ext-amt1 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        END. 
        ELSE 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        IF double-currency OR price-decimal NE 0 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
        END. 
        /*str-list.s = str-list.s + STRING(" ", "x(12)") 
          + STRING(tot-pulse,">>>>>9").*/ 
        str-list.impulse = tot-pulse. 
        create str-list. 
      END. 
      ELSE 
      DO: 
        last-ext = "". 
        ext-amt1 = 0. 
        ext-amt2 = 0. 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer = dialed-nr 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.nebenstelle 
          BY calls.zeit descending: 
          IF last-ext NE calls.nebenstelle THEN 
          DO: 
            create str-list. 
            /*DO i = 1 TO 34: 
              str-list.s = str-list.s + " ". 
            END.*/ 
            /*str-list.s = str-list.s 
              + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
            str-list.destination = "T O T A L  ". 
            IF price-decimal = 0 THEN 
            DO: 
              IF ext-amt1 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            END. 
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                    /*str-list.guest-rate = ext-amt1.*/
                    str-list.pabx-rate = ext-amt1.
            IF double-currency OR price-decimal NE 0 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
            DO: 
              IF ext-amt2 LE 999999999 THEN 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
              ELSE 
                  ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
            END. 
            /*str-list.s = str-list.s + STRING(" ", "x(12)") 
              + STRING(tot-pulse,">>>>>9").*/ 
            str-list.impulse = tot-pulse. 
            create str-list. 
            last-ext = calls.nebenstelle. 
            ext-amt1 = 0. 
            ext-amt2 = 0. 
          END. 
          ext-amt1 = ext-amt1 + calls.pabxbetrag. 
          ext-amt2 = ext-amt2 + calls.gastbetrag. 
          RUN create-record. 
        END. 
        create str-list. 
        /*DO i = 1 TO 34: 
          str-list.s = str-list.s + " ". 
        END.*/ 
        /*str-list.s = str-list.s 
          + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
        str-list.destination = "T O T A L  ". 
        IF price-decimal = 0 THEN 
        DO: 
          IF ext-amt1 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        END. 
        ELSE 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                /*str-list.guest-rate = ext-amt1.*/
                str-list.pabx-rate = ext-amt1.
        IF double-currency OR price-decimal NE 0 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
          ELSE 
              ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
        END. 
        /*str-list.s = str-list.s + STRING(" ", "x(12)") 
          + STRING(tot-pulse,">>>>>9").*/ 
        str-list.impulse = tot-pulse. 
        create str-list. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.datum descending 
        BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE 
    DO: 
/** Print Total per extension **/ 
      last-ext = "". 
      ext-amt1 = 0. 
      ext-amt2 = 0. 
 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.nebenstelle 
        BY calls.datum descending BY calls.zeit descending: 
        IF last-ext = "" THEN last-ext = calls.nebenstelle. 
        IF last-ext NE calls.nebenstelle THEN 
        DO: 
          create str-list. 
          /*DO i = 1 TO 34: 
            str-list.s = str-list.s + " ". 
          END.*/ 
          /*str-list.s = str-list.s 
            + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
          str-list.destination = "T O T A L  ". 
          IF price-decimal = 0 THEN 
          DO: 
            IF ext-amt1 LE 999999999 THEN 
                ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
            ELSE 
                ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
          END. 
          ELSE 
              ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
                  /*str-list.guest-rate = ext-amt1.*/
                  str-list.pabx-rate = ext-amt1.
          IF double-currency OR price-decimal NE 0 THEN 
              ASSIGN
                  /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
                  str-list.guest-rate = ext-amt2.
          ELSE 
          DO: 
            IF ext-amt2 LE 999999999 THEN 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                    str-list.guest-rate = ext-amt2.
            ELSE 
                ASSIGN
                    /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                    str-list.guest-rate = ext-amt2.
          END. 
          /*str-list.s = str-list.s + STRING(" ", "x(12)") 
            + STRING(tot-pulse,">>>>>9").*/ 
          str-list.impulse = tot-pulse. 
          create str-list. 
          last-ext = calls.nebenstelle. 
          ext-amt1 = 0. 
          ext-amt2 = 0. 
        END. 
        ext-amt1 = ext-amt1 + calls.pabxbetrag. 
        ext-amt2 = ext-amt2 + calls.gastbetrag. 
        RUN create-record. 
      END. 
      create str-list. 
      /*DO i = 1 TO 34: 
        str-list.s = str-list.s + " ". 
      END.*/ 
      /*str-list.s = str-list.s 
        + STRING(("T O T A L  " + last-ext), "x(16)").*/ 
      str-list.destination = "T O T A L  ". 
      IF price-decimal = 0 THEN 
      DO: 
        IF ext-amt1 LE 999999999 THEN 
            ASSIGN
              /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>,>>>,>>9")*/
              /*str-list.guest-rate = ext-amt1.*/
              str-list.pabx-rate = ext-amt1.
       ELSE 
           ASSIGN
             /*str-list.s = str-list.s + STRING(ext-amt1, "   >>>>>>>>>>9")*/
             /*str-list.guest-rate = ext-amt1.*/
             str-list.pabx-rate = ext-amt1.
      END. 
      ELSE 
          ASSIGN
             /*str-list.s = str-list.s + STRING(ext-amt1, ">>>,>>>,>>9.99")*/
             /*str-list.guest-rate = ext-amt1.*/
             str-list.pabx-rate = ext-amt1.
      IF double-currency OR price-decimal NE 0 THEN 
          ASSIGN
             /*str-list.s = str-list.s + STRING(ext-amt2, ">>>,>>>,>>9.99")*/
             str-list.guest-rate = ext-amt2.
      ELSE 
      DO: 
        IF ext-amt2 LE 999999999 THEN 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>,>>>,>>9")*/
                str-list.guest-rate = ext-amt2.
        ELSE 
            ASSIGN
                /*str-list.s = str-list.s + STRING(ext-amt2, "   >>>>>>>>>>9")*/
                str-list.guest-rate = ext-amt2.
      END. 
      /*str-list.s = str-list.s + STRING(" ", "x(12)") 
        + STRING(tot-pulse,">>>>>9").*/ 
      str-list.impulse = tot-pulse. 
      create str-list. 
    END. 
  END. 
 
  ELSE IF last-sort = 3 THEN 
  DO: 
    IF from-date = to-date AND from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.nebenstelle = from-ext 
        AND calls.datum EQ from-date AND calls.zeit GE 0 
        AND calls.buchflag = stattype 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX nebenst_ix NO-LOCK 
        BY calls.rufnummer BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE IF from-date = to-date THEN 
    DO: 
      IF from-ext = "0" AND to-ext = "99999" THEN 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer = dialed-nr 
          USE-INDEX key-book-date_ix NO-LOCK BY calls.rufnummer 
          BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
      ELSE 
      DO: 
        FOR EACH calls WHERE calls.key = 1 
          AND calls.buchflag = stattype 
          AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
          AND calls.datum EQ from-date 
          AND calls.zeit GE 0 
          AND calls.rufnummer = dialed-nr 
          USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
          BY calls.zeit descending: 
          RUN create-record. 
        END. 
      END. 
    END. 
    ELSE IF from-ext = to-ext THEN 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle EQ from-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
        BY calls.datum descending BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
    ELSE 
    DO: 
      FOR EACH calls WHERE calls.key = 1 AND calls.buchflag = stattype 
        AND calls.nebenstelle GE from-ext AND calls.nebenstelle LE to-ext 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        AND calls.rufnummer = dialed-nr 
        USE-INDEX key-book-nebst_ix NO-LOCK BY calls.rufnummer 
        BY calls.datum descending BY calls.zeit descending: 
        RUN create-record. 
      END. 
    END. 
  END. 
END.
/* sampe sini - assign dari str-list.s jadi field temp-table */
PROCEDURE create-record: 
DEFINE VARIABLE i AS INTEGER. 
  /*IF calls.betriebsnr = 0 THEN i = 1. 
  ELSE i = 2.*/ 
  CREATE str-list. 
  ASSIGN
    str-list.zero-rate      = (calls.gastbetrag = 0)
    str-list.c-recid        = RECID(calls)
    str-list.destination    = STRING(calls.satz-id, "x(16)")
    str-list.rechnr         = calls.rechnr
    str-list.nebenstelle    = calls.nebenstelle
    str-list.datum          = calls.datum
    str-list.rufnummer      = calls.rufnummer
    str-list.zeit           = STRING(calls.zeit, "HH:MM")
    /*str-list.s = STRING(calls.nebenstelle, "x(5)") 
      + STRING(calls.datum) 
      + STRING(calls.zeit, "HH:MM") 
      + STRING(calls.rufnummer, "x(16)") 
      + STRING(calls.satz-id, "x(16)")*/
  . 
  IF calls.betriebsnr = 0 THEN str-list.print = "NO". 
  ELSE str-list.print = "YES". 
 
  IF calls.aufschlag NE 0 THEN
  DO:
    FIND FIRST bediener WHERE bediener.nr = INTEGER(calls.aufschlag) 
        NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN ASSIGN str-list.username = bediener.username.
  END.
  
  IF double-currency THEN 
  DO: 
    IF calls.leitung GE 10000 THEN
        /*ASSIGN
            str-list.s = str-list.s + STRING(calls.pabxbetrag, "   >>>,>>>,>>9") 
              + STRING(calls.gastbetrag, ">>>,>>>,>>9.99") 
              + STRING(calls.dauer, "HH:MM:SS") 
              + STRING(calls.zinr, "x(6)") 
              + STRING(calls.impulse, ">>>>>9") 
              + STRING(STRING(calls.leitung), "x(4)") /* reduce max length to 4 digits */
              + prstr[i] 
              + STRING(calls.sequence,">>>>>>9")
            str-list.guest-rate = calls.gastbetrag
            str-list.pabx-rate = calls.pabxbetrag. 
    ELSE
        ASSIGN
            str-list.s = str-list.s + STRING(calls.pabxbetrag, "   >>>,>>>,>>9") 
              + STRING(calls.gastbetrag, ">>>,>>>,>>9.99") 
              + STRING(calls.dauer, "HH:MM:SS") 
              + STRING(calls.zinr, "x(6)") 
              + STRING(calls.impulse, ">>>>>9") 
              + STRING(calls.leitung, ">>>>") /* reduce max length to 4 digits */
              + prstr[i] 
              + STRING(calls.sequence,">>>>>>9")
            str-list.guest-rate = calls.gastbetrag
            str-list.pabx-rate = calls.pabxbetrag.*/
        ASSIGN
            str-list.dauer = STRING(calls.dauer, "HH:MM:SS") 
            str-list.zinr = calls.zinr
            str-list.impulse = calls.impulse
            str-list.leitung = calls.leitung
              /*+ prstr[i] 
              + STRING(calls.sequence,">>>>>>9")*/
            str-list.guest-rate = calls.gastbetrag
            str-list.pabx-rate = calls.pabxbetrag. 
    ELSE
        ASSIGN
            str-list.dauer = STRING(calls.dauer, "HH:MM:SS") 
            str-list.zinr = calls.zinr
            str-list.impulse = calls.impulse
            str-list.leitung = calls.leitung
              /*+ prstr[i] 
              + STRING(calls.sequence,">>>>>>9")*/
            str-list.guest-rate = calls.gastbetrag
            str-list.pabx-rate = calls.pabxbetrag.
  END. 
  ELSE 
  DO: 
    IF price-decimal = 0 THEN 
        ASSIGN
            /*str-list.s = str-list.s + STRING(calls.pabxbetrag, "   >>>,>>>,>>9")
                       + STRING(calls.gastbetrag, "   >>>,>>>,>>9")*/
            str-list.guest-rate = calls.gastbetrag
            str-list.pabx-rate = calls.pabxbetrag.
    ELSE 
        ASSIGN
            /*str-list.s = str-list.s + STRING(calls.pabxbetrag, ">>>,>>>,>>9.99")
                       + STRING(calls.gastbetrag, ">>>,>>>,>>9.99")*/
            str-list.guest-rate = calls.gastbetrag
            str-list.pabx-rate = calls.pabxbetrag.
    IF calls.leitung GE 10000 THEN
    /*str-list.s = str-list.s 
      + STRING(calls.dauer, "HH:MM:SS") 
      + STRING(calls.zinr, "x(6)") 
      + STRING(calls.impulse, ">>>>>9") 
      + STRING(STRING(calls.leitung), "x(4)") 
      + prstr[i] 
      + STRING(calls.sequence,">>>>>>9")*/ 
        ASSIGN str-list.dauer = STRING(calls.dauer, "HH:MM:SS") 
        str-list.zinr = calls.zinr
        str-list.impulse = calls.impulse
        str-list.leitung = calls.leitung
          /*+ prstr[i] 
          + STRING(calls.sequence,">>>>>>9")*/
        .
    ELSE
    /*str-list.s = str-list.s 
      + STRING(calls.dauer, "HH:MM:SS") 
      + STRING(calls.zinr, "x(6)") 
      + STRING(calls.impulse, ">>>>>9") 
      + STRING(calls.leitung, ">>>>") 
      + prstr[i] 
      + STRING(calls.sequence,">>>>>>9")*/ 
        ASSIGN str-list.dauer = STRING(calls.dauer, "HH:MM:SS") 
        str-list.zinr = calls.zinr
        str-list.impulse = calls.impulse
        str-list.leitung = calls.leitung
          /*+ prstr[i] 
          + STRING(calls.sequence,">>>>>>9")*/
        .
  END. 
  
  amount1 = amount1 + calls.pabxbetrag. 
  amount2 = amount2 + calls.gastbetrag. 
  tot-pulse = tot-pulse + calls.impulse. 
  
END. 
