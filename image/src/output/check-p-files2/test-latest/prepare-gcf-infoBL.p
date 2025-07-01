DEFINE TEMP-TABLE output-list
    FIELD nr          AS INTEGER  FORMAT "99"
    FIELD dept        AS INTEGER 
    FIELD rechnr      AS INTEGER
    FIELD datum       AS DATE
    FIELD str         AS CHAR     FORMAT "x(94)"
    .


DEF TEMP-TABLE t-guest          LIKE guest.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER gastnr  AS INTEGER.
DEF OUTPUT PARAMETER payment AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-guest.
DEF OUTPUT PARAMETER TABLE FOR output-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "prepare-gcf-info".

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
IF AVAILABLE guest THEN
DO:
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.

    IF guest.zahlungsart  > 0 THEN 
    DO: 
      FIND FIRST artikel WHERE departement = 0 AND 
        artikel.artnr = guest.zahlungsart NO-ERROR. 
      IF AVAILABLE artikel THEN 
        payment = STRING(guest.zahlungsart) + "  -  " + artikel.bezeich. 
    END. 
END.

RUN create-list.

PROCEDURE create-list:
    DEFINE BUFFER reslin FOR res-line.
    DEFINE BUFFER htldpt FOR hoteldpt.
    DEFINE BUFFER ginfo FOR guest-queasy.       
    DEF VAR str1        AS CHAR NO-UNDO.
    DEF VAR i           AS INTEGER NO-UNDO INITIAL 0.
    DEF VAR dept-str    AS CHAR FORMAT "x(24)"      NO-UNDO.
    DEF VAR cistr       AS CHAR FORMAT "x(8)"       NO-UNDO.
    DEF VAR costr       AS CHAR FORMAT "x(8)"       NO-UNDO.
    DEF VAR curr-dept   AS INTEGER                  NO-UNDO.
    DEF VAR sub-tot     AS DECIMAL                  NO-UNDO.
    DEF VAR sub-str     AS CHAR    FORMAT "x(24)"   NO-UNDO.
    DEF VAR it-exists   AS LOGICAL INITIAL NO.
    DEF VAR rmno        AS CHAR    INITIAL "".
    DEF VAR rmcat       AS CHAR    INITIAL "".

    DEF VAR invDept     AS INTEGER                  NO-UNDO.
    DEF VAR invNo       AS INTEGER                  NO-UNDO.
    DEF VAR invDate     AS DATE                     NO-UNDO.

    sub-str = translateExtended("SUBTOTAL", lvCAREA, "").

    FOR EACH output-list:
        DELETE output-list.
    END.

    FOR EACH ginfo WHERE ginfo.KEY = "gast-info" AND ginfo.gastnr = gastnr
        NO-LOCK BY ginfo.number1 BY ginfo.date1:
        IF curr-dept NE ginfo.number1 AND curr-dept NE 0 THEN
        DO:
            i = i + 1.
            str1 = FILL("-", 94).
            RUN add-line(i, str1, 0, 0, ?).

            i = i + 1.
            str1 = STRING(sub-str, "x(24)") + STRING(sub-tot, "->>>,>>>,>>9").
            ASSIGN
              invDept  = ginfo.number1
              invNo    = INTEGER(ginfo.char1)
              invDate  = ginfo.date1
            .
            RUN add-line(i, str1, invDept, invNo, invDate).
/*
            i = i + 1.
            RUN add-line(i, " ", 0, 0, ?).
*/
            sub-tot = 0.
        END.
        
        it-exists = YES.

        i = i + 1.
        FIND FIRST htldpt WHERE htldpt.num = ginfo.number1 NO-LOCK NO-ERROR.
        IF AVAILABLE htldpt THEN
            dept-str = htldpt.depart.
        ELSE dept-str = "UNKNOWN".

        ASSIGN cistr = STRING(ginfo.date1, "99/99/99")
               costr = cistr
        .

        FIND FIRST reslin WHERE reslin.resnr = ginfo.number2 AND reslin.reslinnr = 
            ginfo.number3 USE-INDEX relinr_index NO-LOCK NO-ERROR.
        IF AVAILABLE reslin THEN
        DO:
            cistr = STRING(reslin.ankunft, "99/99/99").
            costr = STRING(reslin.abreise, "99/99/99").
            rmno  = reslin.zinr.
            FIND FIRST zimmer WHERE zimmer.zinr = rmno NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer THEN 
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr
                NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN
                    rmcat = zimkateg.kurzbez.
        END.
        ELSE
        DO:
            FIND FIRST history WHERE history.gastnr = gastnr AND history.resnr = 
                ginfo.number2 AND history.reslinnr = ginfo.number3 USE-INDEX res_ix
                NO-LOCK NO-ERROR.
            IF AVAILABLE history THEN
            DO:
                cistr   = STRING(history.ankunft, "99/99/99").
                costr   = STRING(history.abreise, "99/99/99").
                rmno    = history.zinr.
                FIND FIRST zimmer WHERE zimmer.zinr = rmno NO-LOCK NO-ERROR.
                IF AVAILABLE zimmer THEN 
                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN
                        rmcat = zimkateg.kurzbez.
            END.
            ELSE
            DO:
                rmno  = "".
                rmcat = "".
            END.
        END.

        str1 = STRING(dept-str, "x(24)") + STRING(ginfo.deci3, "->>>,>>>,>>9") + 
            STRING(cistr, "x(8)") + STRING(costr, "x(8)") + STRING(ginfo.deci1, "->>>,>>>,>>9")
            + STRING(ginfo.deci2, "->>>,>>>,>>9") + STRING(rmno, "x(6)") 
            + STRING(rmcat, "x(4)") .
        ASSIGN
          invDept  = ginfo.number1
          invNo    = INTEGER(ginfo.char1)
          invDate  = ginfo.date1
        .
        RUN add-line(i, str1, invDept, invNo, invDate).
        curr-dept = ginfo.number1.
        sub-tot = sub-tot + ginfo.deci3.
    END.

    IF it-exists THEN
    DO:
        i = i + 1.
        str1 = FILL("-", 94).
        RUN add-line(i, str1, 0, 0, ?).
    
        i = i + 1.
        str1 = STRING(sub-str, "x(24)") + STRING(sub-tot, "->>>,>>>,>>9").
        RUN add-line(i, str1, 0, 0, ?).
    END.
END.


/*MTPROCEDURE count-proz:
    IF guest.gesamtumsatz = 0 THEN proz[1] = 0.
    ELSE proz[1] = 100.
    IF guest.argtumsatz = 0 THEN proz[2] = 0.
    ELSE 
        proz[2] = guest.argtumsatz / guest.gesamtumsatz * 100.
    IF guest.f-b-umsatz = 0 THEN proz[3] = 0.
    ELSE
        proz[3] = guest.f-b-umsatz / guest.gesamtumsatz * 100.
    IF guest.sonst-umsatz = 0 THEN proz[4] = 0.
    ELSE
        proz[4] = guest.sonst-umsatz / guest.gesamtumsatz * 100.
END.*/


PROCEDURE add-line:
    DEFINE INPUT PARAMETER nr       AS INTEGER.
    DEFINE INPUT PARAMETER str1     AS CHAR FORMAT "x(64)".
    DEFINE INPUT PARAMETER dept     AS INTEGER.
    DEFINE INPUT PARAMETER rechnr   AS INTEGER.
    DEFINE INPUT PARAMETER datum    AS DATE.
    CREATE output-list.
    ASSIGN output-list.nr  = nr
        output-list.str    = str1
        output-list.dept   = dept
        output-list.rechnr = rechnr
        output-list.datum  = datum.
END.
