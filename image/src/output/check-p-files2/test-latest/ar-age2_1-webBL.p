DEFINE TEMP-TABLE age-list 
  FIELD artnr           AS INTEGER 
  FIELD rechnr          AS INTEGER 
  FIELD inv-no           AS INTEGER
  FIELD counter         AS INTEGER 
  FIELD gastnr          AS INTEGER 
  FIELD creditlimit     AS DECIMAL 
  FIELD rgdatum         AS DATE 
  FIELD gastname        AS CHARACTER FORMAT "x(34)" 
  FIELD fbetrag         AS DECIMAL 
  FIELD saldo           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0
  FIELD curr            AS CHAR FORMAT "x(4)"
  FIELD inv-soa         AS INTEGER. 
 
DEFINE TEMP-TABLE ledger 
  FIELD artnr           AS INTEGER 
  FIELD bezeich         AS CHARACTER FORMAT "x(24)" INITIAL "?????" 
  FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0. 
 
DEFINE TEMP-TABLE output-list 
  FIELD inv-no      AS CHAR FORMAT "x(9) "
  FIELD fbetrag     AS CHAR FORMAT "x(15)" 
  FIELD creditlimit AS CHAR
  FIELD curr        AS CHAR FORMAT "x(4)"
  FIELD str         AS CHAR
  FIELD inv-soa     AS CHAR
  FIELD bill-no     AS CHAR
  FIELD g-name      AS CHAR
  FIELD check-in    AS CHAR
  FIELD check-out   AS CHAR
  FIELD outstand    AS CHAR
  FIELD age         AS CHAR
  FIELD day1        AS CHAR
  FIELD day2        AS CHAR
  FIELD day3        AS CHAR
  FIELD day4        AS CHAR
. 
 
DEFINE INPUT  PARAMETER pvILanguage AS INTEGER         NO-UNDO.
DEFINE INPUT  PARAMETER curr-gastnr AS INTEGER         NO-UNDO.
DEFINE INPUT  PARAMETER from-art    AS INTEGER         NO-UNDO.
DEFINE INPUT  PARAMETER disptype    AS INTEGER         NO-UNDO.
DEFINE INPUT  PARAMETER to-date     AS DATE            NO-UNDO.
DEFINE INPUT  PARAMETER show-inv    AS LOGICAL         NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR INITIAL "" NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE       FOR output-list.

DEFINE VARIABLE day1            AS INTEGER INITIAL 30 NO-UNDO. 
DEFINE VARIABLE day2            AS INTEGER INITIAL 30 NO-UNDO. 
DEFINE VARIABLE day3            AS INTEGER INITIAL 30 NO-UNDO.

DEFINE VARIABLE price-decimal   AS INTEGER          NO-UNDO. 
DEFINE VARIABLE default-fcurr   AS CHAR             NO-UNDO.
DEFINE VARIABLE outlist         AS CHAR             NO-UNDO.
DEFINE VARIABLE fremdwbetrag    AS DECIMAL          NO-UNDO.

DEF BUFFER debt FOR debitor.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ar-age2". 

/*****************************************************************************/
RUN htpchar.p (143, OUTPUT default-fcurr).
RUN htpint.p  (491, OUTPUT price-decimal).
RUN htpint.p  (330, OUTPUT day1).
RUN htpint.p  (331, OUTPUT day2).
RUN htpint.p  (332, OUTPUT day3).
day2 = day2 + day1. 
day3 = day3 + day2. 

RUN age-list.

PROCEDURE age-list: 
DEFINE VARIABLE curr-art     AS INTEGER. 
DEFINE VARIABLE billdate     AS DATE. 
DEFINE VARIABLE ct           AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE gastName     AS CHAR    NO-UNDO.
DEFINE VARIABLE t-debet      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-comm       AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE creditlimit  AS DECIMAL. 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-debt     AS DECIMAL FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE t-fdebt      AS DECIMAL INITIAL 0. 
DEFINE VARIABLE ar-saldo     AS DECIMAL. 

DEFINE BUFFER debt FOR debitor. 
  
  FIND FIRST artikel WHERE artikel.artnr EQ from-art 
    AND artikel.departement EQ 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel THEN RETURN. 
 
  FIND FIRST guest WHERE guest.gastnr EQ curr-gastnr NO-LOCK.
  gastname = guest.name + ", " + guest.vorname1 + " " 
    + guest.anrede1 + guest.anredefirma. 

  CREATE output-list.
  ASSIGN
    output-list.bill-no = STRING(artikel.artnr,">>>>>>>>9") + " - "
    output-list.g-name = STRING(artikel.bezeich)    
  .

  CREATE output-list.
  CREATE output-list.
  output-list.g-name = "(" + TRIM(STRING(gastname)) + ")".

/**** unpaid / partial paid A/R records *****/ 
  ASSIGN curr-art = 0. 
  FOR EACH debitor WHERE debitor.artnr EQ from-art 
    AND debitor.rgdatum LE to-date AND debitor.opart EQ 0 
    AND debitor.gastnr = curr-gastnr NO-LOCK 
    USE-INDEX artdat_ix BY debitor.rgdatum: 
    DO: 
      IF curr-art NE debitor.artnr THEN 
      DO: 
        curr-art = debitor.artnr. 
        FIND FIRST artikel WHERE artikel.artnr = curr-art 
          AND artikel.departement = 0  NO-LOCK NO-ERROR. 
      END. 
 
      IF disptype = 0 THEN ar-saldo = debitor.saldo. 
      ELSE ar-saldo = debitor.vesrdep.
      IF debitor.counter NE 0 THEN 
      DO: 
        FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
          AND debt.counter = debitor.counter AND debt.opart = 1 
          AND debt.zahlkonto NE 0 
          AND debt.rgdatum LE to-date NO-LOCK USE-INDEX deb-rechnr_ix: 
          IF disptype = 0 THEN
            ar-saldo = ar-saldo + debt.saldo. 
          ELSE
            ar-saldo = ar-saldo + debt.vesrdep.
        END. 
      END. 
      FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
      CREATE age-list. 
      ASSIGN
        age-list.artnr       = debitor.artnr
        age-list.rechnr      = debitor.rechnr 
        age-list.rgdatum     = debitor.rgdatum 
        age-list.counter     = debitor.counter
        age-list.gastnr      = debitor.gastnr 
        age-list.creditlimit = guest.kreditlimit 
        age-list.tot-debt    = ar-saldo
        age-list.gastname    = debitor.vesrcod
        age-list.creditlimit = guest.kreditlimit
        age-list.fbetrag     = age-list.fbetrag + debitor.vesrdep
        age-list.inv-soa     = debitor.debref. 

      FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR.
      IF AVAILABLE waehrung THEN age-list.curr = waehrung.wabkurz.
      ELSE age-list.curr = default-fcurr.
 
      IF to-date - age-list.rgdatum GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 

       IF show-inv THEN
       DO:
           FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
           IF NOT AVAILABLE bill THEN 
             msg-str = msg-str + translateExtended("Bill", lvCAREA, "") 
                + " " + translateExtended("not found.", lvCAREA, "") + CHR(2).
           ELSE age-list.inv-no = bill.rechnr2.
       END.
    END. 
  END. 
 
/**** Full paid A/R records *****/ 
  curr-art = 0. 
  FOR EACH debitor WHERE debitor.artnr EQ from-art 
    AND debitor.rgdatum LE to-date AND debitor.opart EQ 2 
    AND debitor.zahlkonto = 0 AND debitor.gastnr = curr-gastnr 
    NO-LOCK USE-INDEX artdat_ix BY debitor.rgdatum: 
    FIND FIRST debt WHERE debt.rechnr = debitor.rechnr 
      AND debt.counter = debitor.counter AND debt.opart = 2 
      AND debt.zahlkonto NE 0 AND debt.rgdatum GT to-date 
      NO-LOCK USE-INDEX deb-rechnr_ix NO-ERROR. 
    IF AVAILABLE debt AND debitor.gastnr EQ curr-gastnr 
    THEN DO: 
      IF curr-art NE debitor.artnr THEN 
      DO: 
        curr-art = debitor.artnr. 
        FIND FIRST artikel WHERE artikel.artnr = curr-art 
          AND artikel.departement = 0  NO-LOCK NO-ERROR. 
      END. 
 
      IF disptype = 0 THEN
        ar-saldo = debitor.saldo. 
      ELSE
        ar-saldo = debitor.vesrdep. 
      FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
        AND debt.counter = debitor.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date 
        NO-LOCK USE-INDEX deb-rechnr_ix: 
        IF disptype = 0 THEN
            ar-saldo = ar-saldo + debt.saldo. 
        ELSE ar-saldo = ar-saldo + debt.vesrdep.
      END. 
      FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
      CREATE age-list. 
      ASSIGN
        age-list.artnr          = debitor.artnr
        age-list.rechnr         = debitor.rechnr 
        age-list.rgdatum        = debitor.rgdatum 
        age-list.counter        = debitor.counter 
        age-list.gastnr         = debitor.gastnr 
        age-list.creditlimit    = guest.kreditlimit 
        age-list.tot-debt       = ar-saldo
        age-list.gastname       = debitor.vesrcod
        age-list.creditlimit    = guest.kreditlimit 
        age-list.fbetrag        = age-list.fbetrag + debitor.vesrdep
        age-list.inv-soa     = debitor.debref.

      FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem
          NO-LOCK NO-ERROR.
      IF AVAILABLE waehrung THEN age-list.curr = waehrung.wabkurz.
      ELSE age-list.curr = default-fcurr.
 
      IF to-date - age-list.rgdatum GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 
       IF show-inv THEN
       DO:
           FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
           IF NOT AVAILABLE bill THEN
             msg-str = msg-str + translateExtended("Bill", lvCAREA, "") 
               + " " + translateExtended("not found.", lvCAREA, "") + CHR(2).
           ELSE age-list.inv-no = bill.rechnr2.
       END.
    END. 
  END. 
 
  FOR EACH age-list WHERE age-list.tot-debt NE 0: 
    ASSIGN
      t-saldo  = t-saldo + age-list.tot-debt
      t-debt0  = t-debt0 + age-list.debt0
      t-debt1  = t-debt1 + age-list.debt1 
      t-debt2  = t-debt2 + age-list.debt2 
      t-debt3  = t-debt3 + age-list.debt3
    . 

    fremdwbetrag = age-list.fbetrag. 

    CREATE output-list.
    IF price-decimal EQ 0 THEN 
    DO:
        ASSIGN            
            output-list.bill-no     = STRING(age-list.rechnr,">>>>>>>>9")
            output-list.inv-no      = STRING(age-list.inv-no, ">>>>>>>>>")
            output-list.inv-soa     = STRING(age-list.inv-soa, ">>>>>>>>>")
            output-list.g-name      = STRING(age-list.gastname, "x(30)") 
            output-list.curr        = age-list.curr            
            output-list.outstand    = STRING(age-list.tot-debt, "->>>,>>>,>>>,>>>,>>9") 
            output-list.age         = STRING(to-date - age-list.rgdatum, ">>9") 
            output-list.day1        = STRING(age-list.debt0, "->>>,>>>,>>>,>>>,>>9") 
            output-list.day2        = STRING(age-list.debt1, "->>>,>>>,>>>,>>>,>>9") 
            output-list.day3        = STRING(age-list.debt2, "->>>,>>>,>>>,>>>,>>9") 
            output-list.day4        = STRING(age-list.debt3, "->>>,>>>,>>>,>>>,>>9")
        . 

        IF fremdwbetrag NE 0 THEN output-list.fbetrag = STRING(fremdwbetrag,"->>>,>>>,>>>,>>>,>>9"). 
    END.         
    ELSE
    DO:
        ASSIGN         
            output-list.bill-no     = STRING(age-list.rechnr,">>>>>>>>9")
            output-list.inv-no      = STRING(age-list.inv-no, ">>>>>>>>>")
            output-list.inv-soa     = STRING(age-list.inv-soa, ">>>>>>>>>")
            output-list.g-name      = STRING(age-list.gastname, "x(30)") 
            output-list.curr        = age-list.curr            
            output-list.outstand    = STRING(age-list.tot-debt, "->,>>>,>>>,>>>,>>9.99") 
            output-list.age         = STRING(to-date - age-list.rgdatum, ">>9") 
            output-list.day1        = STRING(age-list.debt0, "->,>>>,>>>,>>>,>>9.99") 
            output-list.day2        = STRING(age-list.debt1, "->,>>>,>>>,>>>,>>9.99") 
            output-list.day3        = STRING(age-list.debt2, "->,>>>,>>>,>>>,>>9.99") 
            output-list.day4        = STRING(age-list.debt3, "->,>>>,>>>,>>>,>>9.99")
        . 

        IF fremdwbetrag NE 0 THEN output-list.fbetrag = STRING(fremdwbetrag,"->,>>>,>>>,>>>,>>9.99").
    END.
    
    t-fdebt = t-fdebt + fremdwbetrag.     
  END. 
 
  fremdwbetrag = 0.   
    
  CREATE output-list.
  IF price-decimal EQ 0 THEN 
  DO:
      ASSIGN         
            output-list.g-name      = translateExtended ("T O T A L  A/R:",lvCAREA,"")          
            output-list.outstand    = STRING(t-saldo, "->>>,>>>,>>>,>>>,>>9")  
            output-list.day1        = STRING(t-debt0, "->>>,>>>,>>>,>>>,>>9") 
            output-list.day2        = STRING(t-debt1, "->>>,>>>,>>>,>>>,>>9") 
            output-list.day3        = STRING(t-debt2, "->>>,>>>,>>>,>>>,>>9") 
            output-list.day4        = STRING(t-debt3, "->>>,>>>,>>>,>>>,>>9")
        . 
  END.   
  ELSE 
  DO:
      ASSIGN         
            output-list.g-name      = translateExtended ("T O T A L  A/R:",lvCAREA,"")          
            output-list.outstand    = STRING(t-saldo, "->>>,>>>,>>>,>>>,>>9.99")  
            output-list.day1        = STRING(t-debt0, "->>>,>>>,>>>,>>>,>>9.99") 
            output-list.day2        = STRING(t-debt1, "->>>,>>>,>>>,>>>,>>9.99") 
            output-list.day3        = STRING(t-debt2, "->>>,>>>,>>>,>>>,>>9.99") 
            output-list.day4        = STRING(t-debt3, "->>>,>>>,>>>,>>>,>>9.99")
        . 
  END.

  CREATE output-list.
END. 
