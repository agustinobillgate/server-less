DEFINE TEMP-TABLE output-list 
  FIELD bezeich AS CHAR FORMAT "x(40)" /* Naufal Afthar - AFB4A4*/
  FIELD STR AS CHAR. 
DEFINE TEMP-TABLE sum-list
    FIELD datum   AS DATE
    FIELD artnr   AS INTEGER
    FIELD bezeich AS CHAR
    FIELD anzahl  AS INTEGER
    FIELD betrag  AS DECIMAL
    FIELD usrNo   AS INTEGER
.

DEF INPUT PARAMETER sumFlag AS LOGICAL.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER usr-init AS CHAR.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER TABLE FOR output-list.

FIND FIRST hoteldpt WHERE hoteldpt.num = curr-dept.
IF NOT sumFlag THEN RUN journal-list. 
ELSE RUN journal-sumlist.

PROCEDURE journal-list: 
  DEFINE VARIABLE qty AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
  DEFINE VARIABLE sub-tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE curr-date AS DATE. 
  /* Malik Serverless 385 */
  DEFINE VARIABLE h-journal-tischnr AS CHAR. 
  DEFINE VARIABLE h-journal-rechnr AS CHAR. 
  DEFINE VARIABLE h-journal-artnr AS CHAR. 
  DEFINE VARIABLE hoteldpt-depart-journal-list AS CHAR. 
  DEFINE VARIABLE h-journal-anzahl AS CHAR. 
  DEFINE VARIABLE h-journal-betrag AS CHAR. 
  DEFINE VARIABLE h-journal-zeit AS CHAR. 
  DEFINE VARIABLE h-journal-kellner-nr AS CHAR. 
  DEFINE VARIABLE h-bill-kellner-nr AS CHAR. 
  DEFINE VARIABLE h-journal-betrag-no-coma AS CHAR. 
  DEFINE VARIABLE qty-total AS CHAR. 
  DEFINE VARIABLE sub-tot-total AS CHAR. 
  DEFINE VARIABLE sub-tot-total-no-coma AS CHAR. 
  /* END Malik */

 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  DO curr-date = from-date TO to-date: 
    FOR EACH h-journal WHERE h-journal.kellner-nr = INTEGER(usr-init)
        AND h-journal.departement = curr-dept
        AND bill-datum = curr-date, 
      FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
        AND h-bill.departement = h-journal.departement NO-LOCK 
        BY h-journal.rechnr BY h-journal.sysdate BY h-journal.zeit: 

      /* Malik Serverless 385 */
      h-journal-tischnr = STRING(h-journal.tischnr, ">>>>>9"). /* 9E5FE6 RULITA 12/01/2023 | muncul pop up eror ketika Show as Summary by article di ceklist */
      h-journal-rechnr = STRING(h-journal.rechnr, "9,999,999").
      h-journal-artnr = STRING(h-journal.artnr, ">>>>>>>>>"). /*william add >>>> 756C87*/
      hoteldpt-depart-journal-list = SUBSTRING(hoteldpt.depart,1, 12).
      h-journal-anzahl = STRING(h-journal.anzahl, "-9999").
      h-journal-betrag = STRING(h-journal.betrag, "->,>>>,>>>,>>9.99").
      h-journal-zeit = STRING(h-journal.zeit, "HH:MM").
      h-journal-kellner-nr = STRING(h-journal.kellner-nr, "9999"). /*bernatd 683B73*/
      h-bill-kellner-nr = STRING(h-bill.kellner-nr, "9999"). /*bernatd 683B73*/
      h-journal-betrag-no-coma = STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9").
      /* END Malik */
      /* Malik Serverless 385 comment
      CREATE output-list. 
      IF price-decimal = 2 THEN STR = STRING(bill-datum) 
                    + STRING(h-journal.tischnr, ">>>>>9")       /* 9E5FE6 RULITA 12/01/2023 | muncul pop up eror ketika Show as Summary by article di ceklist */
                    + STRING(h-journal.rechnr, "9,999,999")
                    + STRING(h-journal.artnr, ">>>>>>>>>") /*william add >>>> 756C87*/
                    + STRING(h-journal.bezeich, "x(28)")
                    + STRING(hoteldpt.depart, "x(12)")
                    + STRING(h-journal.anzahl, "-9999")
                    + STRING(betrag, "->,>>>,>>>,>>9.99")
                    + STRING(zeit, "HH:MM")
                    + STRING(h-journal.kellner-nr, "999")
                    + STRING(h-bill.kellner-nr, "999")
          . 
      ELSE STR = STRING(bill-datum) 
                    + STRING(h-journal.tischnr, ">>>>>9")       /* 9E5FE6 RULITA 12/01/2023 | muncul pop up eror ketika Show as Summary by article di ceklist */
                    + STRING(h-journal.rechnr, "9,999,999")
                    + STRING(h-journal.artnr, ">>>>>>>>>") /*william add >>>> 756C87*/
                    + STRING(h-journal.bezeich, "x(28)")
                    + STRING(hoteldpt.depart, "x(12)")
                    + STRING(h-journal.anzahl, "-9999")
                    + STRING(betrag, " ->>>,>>>,>>>,>>9")
                    + STRING(zeit, "HH:MM")
                    + STRING(h-journal.kellner-nr, "999")
                    + STRING(h-bill.kellner-nr, "999")
          . 
      */
      /* Malik Serverless 385 */    
      CREATE output-list. 
      IF price-decimal = 2 THEN output-list.str = STRING(h-journal.bill-datum) 
                    + STRING(h-journal-tischnr, "x(6)") 
                    + STRING(h-journal-rechnr, "x(9)") 
                    + STRING(h-journal-artnr, "x(9)") 
                    + STRING(h-journal.bezeich, "x(28)")
                    + STRING(hoteldpt-depart-journal-list, "x(12)") 
                    + STRING(h-journal-anzahl, "x(5)") 
                    + STRING(h-journal-betrag, "x(17)") 
                    + h-journal-zeit 
                    + STRING(h-journal-kellner-nr, "x(5)") 
                    + STRING(h-bill-kellner-nr, "x(5)") 
          . 
      ELSE output-list.str = STRING(h-journal.bill-datum) 
                    + STRING(h-journal-tischnr, "x(6)") 
                    + STRING(h-journal-rechnr, "x(9)") 
                    + STRING(h-journal-artnr, "x(9)") 
                    + STRING(h-journal.bezeich, "x(28)")
                    + STRING(hoteldpt-depart-journal-list, "x(12)") 
                    + STRING(h-journal-anzahl, "x(5)") 
                    + STRING(h-journal-betrag-no-coma, "x(17)") 
                    + h-journal-zeit
                    + STRING(h-journal-kellner-nr, "x(5)") 
                    + STRING(h-bill-kellner-nr, "x(5)") 
          . 
      ASSIGN output-list.bezeich = h-journal.bezeich. /* Naufal Afthar - AFB4A4*/

      qty = qty + h-journal.anzahl. 
      sub-tot = sub-tot + h-journal.betrag. 
      tot = tot + h-journal.betrag. 
    END. 
  END. 
  /* Malik Serverless 385 */
  qty-total = STRING(qty, "-9999").
  sub-tot-total = STRING(sub-tot, "->,>>>,>>>,>>9.99").
  sub-tot-total-no-coma = STRING(sub-tot, " ->>>,>>>,>>>,>>>").
  /* END Malik */
  /* Malik Serverless 385 Comment         
  CREATE output-list.
  IF price-decimal = 2 THEN STR = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty, "-9999")
          + STRING(sub-tot, "->,>>>,>>>,>>9.99").
  ELSE STR = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty, "-9999")
          + STRING(sub-tot, " ->>>,>>>,>>>,>>>").
  */        
  CREATE output-list.
  IF price-decimal = 2 THEN output-list.str = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty-total, "x(5)") 
          + STRING(sub-tot-total, "x(17)"). 
  ELSE output-list.str = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty-total, "x(5)") 
          + STRING(sub-tot-total-no-coma, "x(17)"). 

  ASSIGN output-list.bezeich = "T O T A L".
END. 
 

PROCEDURE journal-sumlist: 
  DEFINE VARIABLE qty AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
  DEFINE VARIABLE sub-tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE curr-date AS DATE. 
  /* Malik Serverless 385 */
  DEFINE VARIABLE sum-list-artnr AS CHAR. 
  DEFINE VARIABLE sum-list-anzahl AS CHAR. 
  DEFINE VARIABLE sum-list-betrag AS CHAR. 
  DEFINE VARIABLE sum-list-usrno AS CHAR. 
  DEFINE VARIABLE sum-list-betrag-no-coma AS CHAR. 
  DEFINE VARIABLE qty-total AS CHAR. 
  DEFINE VARIABLE sub-tot-total AS CHAR. 
  DEFINE VARIABLE sub-tot-total-no-coma AS CHAR. 
  DEFINE VARIABLE hoteldpt-depart AS CHAR. 
  /* END Malik */
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
 
  FOR EACH sum-list:
      DELETE sum-list.
  END.

  DO curr-date = from-date TO to-date: 
    FOR EACH h-journal WHERE h-journal.kellner-nr = INTEGER(usr-init) 
        AND h-journal.departement = curr-dept 
        AND bill-datum = curr-date, 
      FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
        AND h-bill.departement = h-journal.departement NO-LOCK 
        BY h-journal.rechnr BY h-journal.sysdate BY h-journal.zeit: 

      FIND FIRST sum-list WHERE sum-list.artnr = h-journal.artnr
          AND sum-list.bezeich = h-journal.bezeich 
          AND sum-list.datum = h-journal.bill-datum NO-ERROR.
      IF NOT AVAILABLE sum-list THEN
      DO:
          CREATE sum-list.
          ASSIGN
              sum-list.datum   = h-journal.bill-datum
              sum-list.artnr   = h-journal.artnr
              sum-list.bezeich = h-journal.bezeich
              sum-list.usrno   = h-journal.kellner-nr /* Malik Serverless 385 : sum-list.usrNo -> sum-list.usrno */
          .
      END.
      ASSIGN 
          qty             = qty + h-journal.anzahl
          sum-list.anzahl = sum-list.anzahl + h-journal.anzahl
          sum-list.betrag = sum-list.betrag + h-journal.betrag
      .
    END.
  END.

  FOR EACH sum-list BY sum-list.datum BY sum-list.artnr:
      /* Malik Serverless 385 */
      sum-list-artnr = STRING(sum-list.artnr, ">>>>>>>>>"). /* 87886E RULITA 06/01/2023 | fix bug TbNo format 6 digit */
      sum-list-anzahl = STRING(sum-list.anzahl, "-9999").
      sum-list-betrag = STRING(sum-list.betrag, "->,>>>,>>>,>>9.99").
      sum-list-usrno = STRING(sum-list.usrno, "999").
      sum-list-betrag-no-coma = STRING(sum-list.betrag, " ->>>,>>>,>>>,>>9").
      hoteldpt-depart = SUBSTRING(hoteldpt.depart,1, 12).
      /* END Malik */
      /* Malik Serverless 385 Comment 
      CREATE output-list. 
      IF price-decimal = 2 THEN STR = STRING(sum-list.datum) 
                    + STRING("", "x(6)")
                    + STRING("", "x(9)")
                    + STRING(sum-list.artnr, ">>>>>>>>>") /*william add >>>> 756C87*/               /* 87886E RULITA 06/01/2023 | fix bug TbNo format 6 digit */
                    + STRING(sum-list.bezeich, "x(28)")
                    + STRING(hoteldpt.depart, "x(12)")
                    + STRING(sum-list.anzahl, "-9999")
                    + STRING(sum-list.betrag, "->,>>>,>>>,>>9.99")
                    + STRING("", "x(5)")
                    + STRING(sum-list.usrNo, "999")
                    + STRING("", "x(3)")
          . 
      ELSE STR = STRING(sum-list.datum) 
                    + STRING("", "x(6)") 
                    + STRING("", "x(9)")
                    + STRING(sum-list.artnr, ">>>>>>>>>") /*william add >>>> 756C87*/               /* 87886E RULITA 06/01/2023 | fix bug TbNo format 6 digit */
                    + STRING(sum-list.bezeich, "x(28)")
                    + STRING(hoteldpt.depart, "x(12)")
                    + STRING(sum-list.anzahl, "-9999")
                    + STRING(sum-list.betrag, " ->>>,>>>,>>>,>>9")
                    + STRING("", "x(5)")
                    + STRING(sum-list.usrNo, "999")
                    + STRING("", "x(3)")
          . 
      */    
      /* Malik Serverless 385 */
      CREATE output-list. 
      IF price-decimal = 2 THEN output-list.str = STRING(sum-list.datum) /*william add >>>> 756C87*/
                    + STRING("", "x(6)")
                    + STRING("", "x(9)")
                    + STRING(sum-list-artnr, "x(9)")               
                    + STRING(sum-list.bezeich, "x(28)") 
                    + STRING(hoteldpt-depart, "x(12)") 
                    + STRING(sum-list-anzahl, "x(5)") 
                    + STRING(sum-list-betrag, "x(17)") 
                    + STRING("", "x(5)")
                    + STRING(sum-list-usrno, "x(3)") 
                    + STRING("", "x(3)")
          . 
      ELSE output-list.str = STRING(sum-list.datum) 
                    + STRING("", "x(6)")
                    + STRING("", "x(9)")
                    + STRING(sum-list-artnr, "x(9)") 
                    + STRING(sum-list.bezeich, "x(28)") 
                    + STRING(hoteldpt-depart, "x(12)") 
                    + STRING(sum-list-anzahl, "x(5)") 
                    + STRING(sum-list-betrag-no-coma, "x(17)") 
                    + STRING("", "x(5)")
                    + STRING(sum-list-usrno, "x(3)") 
                    + STRING("", "x(3)")
          . 
      ASSIGN output-list.bezeich = sum-list.bezeich. /* Naufal Afthar - AFB4A4*/

      sub-tot = sub-tot + sum-list.betrag. 
      tot = tot + sum-list.betrag. 

  END.
  /* Malik Serverless 385 */
  qty-total = STRING(qty, "-9999").
  sub-tot-total = STRING(sub-tot, "->,>>>,>>>,>>9.99").
  sub-tot-total-no-coma = STRING(sub-tot, " ->>>,>>>,>>>,>>>").
  /* END Malik */
  /* Malik Serverless 385 Comment 
  CREATE output-list.
  IF price-decimal = 2 THEN STR = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty, "-9999")
          + STRING(sub-tot, "->,>>>,>>>,>>9.99").
  ELSE STR = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty, "-9999")
          + STRING(sub-tot, " ->>>,>>>,>>>,>>>").
  */        
  CREATE output-list.
  IF price-decimal = 2 THEN output-list.str = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty-total, "x(5)") 
          + STRING(sub-tot-total, "x(17)"). 
  ELSE output-list.str = STRING("", "x(33)")
          + STRING("T O T A L   ", "x(27)")
          + STRING("", "x(11)")
          + STRING(qty-total, "x(5)") 
          + STRING(sub-tot-total-no-coma, "x(17)"). 
  ASSIGN output-list.bezeich = "T O T A L".
END. 





