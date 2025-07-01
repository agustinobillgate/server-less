
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER t-resnr        AS INT.
DEF INPUT  PARAMETER t-reslinnr     AS INT.
DEF OUTPUT PARAMETER mainres-recid  AS INT.
DEF OUTPUT PARAMETER msg-str1       AS CHAR INIT "".
DEF OUTPUT PARAMETER msg-str2       AS CHAR INIT "".
DEF OUTPUT PARAMETER msg-str3       AS CHAR INIT "".

DEFINE BUFFER resline    FOR bk-reser.
DEFINE BUFFER bk-resline FOR bk-reser. 
DEFINE BUFFER mainres    FOR bk-veran.
DEFINE BUFFER gast       FOR guest. 

DEF VAR ci-date AS DATE.

{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "ba-plan".

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

FIND FIRST resline WHERE resline.veran-nr = t-resnr 
  AND resline.veran-resnr = t-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE resline THEN 
DO: 
    IF resline.datum GT ci-date THEN 
    DO: 
        msg-str1 = translateExtended ("This a banquet reservation for 
                                      coming day(s), closing not possible.",
                                      lvCAREA,"").
        RETURN. 
    END. 
    FIND FIRST bk-resline WHERE bk-resline.veran-nr = resline.veran-nr 
      AND bk-resline.resstatus LE 2 AND bk-resline.datum GT ci-date 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-resline THEN 
    DO: 
        msg-str1 = translateExtended ("Active banquet reservation later than 
                                      TODAY exists.",lvCAREA,"").
        RETURN. 
    END.

    FIND FIRST mainres WHERE mainres.veran-nr = resline.veran-nr 
      USE-INDEX vernr-ix NO-LOCK. 
    IF mainres.rechnr = 0 THEN 
    DO: 
        msg-str2 = "&W" + translateExtended ("Banquet Bill does not exist.",lvCAREA,"").
    END. 
    ELSE 
    DO: 
        FIND FIRST bill WHERE bill.rechnr = mainres.rechnr NO-LOCK. 
        IF bill.saldo NE 0 THEN 
        DO: 
            msg-str1 = translateExtended ("Banquet Bill not balanced.",
                                          lvCAREA,"").
            RETURN. 
        END. 
        IF bill.gesamtumsatz = 0 THEN 
        DO: 
            msg-str2 = "&W" + translateExtended ("Banquet Bill has ZERO sales.",
                                          lvCAREA,"").
        END. 
    END. 

    
    FIND FIRST gast WHERE gast.gastnr = mainres.gastnr NO-LOCK. 
    msg-str3 = "&Q" + translateExtended ("Do you really want to close the banquet 
                                  reservation of",lvCAREA,"") 
             + CHR(10)
             + gast.name + translateExtended (" - ResNo:",lvCAREA,"") 
             + " " + STRING(resline.veran-nr) + " ?".
    mainres-recid = RECID(mainres).
    /*MT
    answer = NO. 
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Do you really want to close the banquet reservation of",lvCAREA,"") 
        SKIP 
        gast.name + translateExtended (" - ResNo:",lvCAREA,"") + " " + STRING(resline.veran-nr) + " ?" 
        VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer.
    IF NOT answer THEN RETURN. 
    
    DO TRANSACTION: 
        FIND CURRENT mainres EXCLUSIVE-LOCK. 
        mainres.activeflag = 1. 
        FIND CURRENT mainres NO-LOCK. 

        FIND FIRST bk-resline WHERE bk-resline.veran-nr = resline.veran-nr 
          AND bk-resline.resstatus = 1 NO-LOCK NO-ERROR. 
        DO WHILE AVAILABLE bk-resline: 
            FIND CURRENT bk-resline EXCLUSIVE-LOCK. 
            bk-resline.resstatus = 8. 
            FIND CURRENT bk-resline NO-LOCK. 
            FIND NEXT bk-resline WHERE bk-resline.veran-nr = resline.veran-nr 
              AND bk-resline.resstatus = 1 NO-LOCK NO-ERROR. 
        END. 

        FIND FIRST bk-func WHERE bk-func.veran-nr = resline.veran-nr 
          AND bk-func.resstatus = 1 NO-LOCK NO-ERROR. 
        DO WHILE AVAILABLE bk-func: 
            RUN create-bahistory. 
            FIND CURRENT bk-func EXCLUSIVE-LOCK. 
            ASSIGN 
              bk-func.resstatus = 8 
              bk-func.c-resstatus[1] = "I" 
              bk-func.r-resstatus[1] = 8 
            . 
            FIND CURRENT bk-func NO-LOCK. 

            FIND NEXT bk-func WHERE bk-func.veran-nr = resline.veran-nr 
              AND bk-func.resstatus = 1 NO-LOCK NO-ERROR. 
        END. 

        IF mainres.rechnr > 0 THEN 
        DO: 
            FIND CURRENT bill EXCLUSIVE-LOCK. 
            ASSIGN 
              bill.flag = 1 
              bill.datum = ci-date 
              bill.vesrcod = user-init 
            . 
            FIND CURRENT bill NO-LOCK. 
        END. 

        b1-resnr = 0. 
        b1-reslinnr = 0. 

        IF curr-view = "daily" THEN RUN create-dlist. 
        ELSE IF curr-view = "weekly" THEN RUN create-wlist. 
        info3 = "". 
        DISP info3 WITH FRAME frame1. 
        RUN disp-it. 

    END. 
    */
END. 
