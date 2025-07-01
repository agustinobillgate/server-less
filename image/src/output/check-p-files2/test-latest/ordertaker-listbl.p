/*DEFINE TEMP-TABLE output-list 
  FIELD STR AS CHAR.*/ 

DEFINE TEMP-TABLE odtaker-list
  FIELD datum         AS DATE
  FIELD tableno       AS CHAR
  FIELD billno        AS INTEGER
  FIELD artno         AS INTEGER
  FIELD bezeich       AS CHAR
  FIELD qty           AS INTEGER
  FIELD amount        AS DECIMAL
  FIELD departement   AS CHARACTER
  FIELD zeit          AS CHAR
  FIELD id            AS CHAR
  FIELD tb            AS CHAR
.

DEFINE INPUT PARAMETER usr-nr    AS INTEGER INITIAL 0. 
DEFINE INPUT PARAMETER from-date AS DATE LABEL "&From Date". 
DEFINE INPUT PARAMETER to-date   AS DATE LABEL "T&o Date". 
DEFINE OUTPUT PARAMETER TABLE FOR odtaker-list.

/*DEFINE VARIABLE long-digit AS LOGICAL INIT NO.*/ 

DEFINE VARIABLE long-digit AS LOGICAL. 
DEFINE VARIABLE qty        AS INTEGER INITIAL 0. 
DEFINE VARIABLE sub-tot    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot        AS DECIMAL INITIAL 0. 
DEFINE VARIABLE curr-date  AS DATE. 
DEFINE VARIABLE count-data AS INTEGER INITIAL 0.

FIND FIRST htparam WHERE paramnr EQ 246 NO-LOCK. 
long-digit = htparam.flogical. 

/* not used */
/* RUN rest-odtakerlist-btn-gobl.p (from-date, to-date, usr-nr, long-digit, OUTPUT TABLE output-list). */
 
FOR EACH odtaker-list:
    DELETE odtaker-list.
END.

/* FOR EACH output-list:
    CREATE odtaker-list.
    ASSIGN 
    datum       = DATE(substring(output-list.str,1,8)) 
    tableno     = substring(output-list.str,9,4) 
    billno      = int(substring(output-list.str,13,9)) 
    artno       = int(substring(output-list.str,22,5)) 
    bezeich     = substring(output-list.str,27,28) 
    qty         = int(substring(output-list.str,75,5)) 
    amount      = decimal(substring(output-list.str,80,17)) 
    departement = substring(output-list.str,55,20) 
    zeit        = substring(output-list.str,97,5) 
    id          = substring(output-list.str,102,3) 
    tb          = substring(output-list.str,105,3) 
    .
END. */

/* not used */
/* FOR EACH output-list:
    CREATE odtaker-list.
    ASSIGN 
        odtaker-list.datum       = output-list.datum 
        odtaker-list.billno      = output-list.rechnr 
        odtaker-list.artno       = output-list.artnr 
        odtaker-list.bezeich     = output-list.bezeich 
        odtaker-list.qty         = output-list.anzahl 
        odtaker-list.amount      = output-list.betrag 
        odtaker-list.departement = output-list.dept  
    .

    IF output-list.tischnr EQ 0 THEN odtaker-list.tableno = "".
    ELSE odtaker-list.tableno = STRING(output-list.tischnr, ">>>9").

    IF output-list.zeit EQ 0 THEN odtaker-list.zeit = "".
    ELSE odtaker-list.zeit = STRING(output-list.zeit, "HH:MM").

    IF output-list.kellnr1 EQ 0 THEN odtaker-list.id = "".
    ELSE odtaker-list.id = STRING(output-list.kellnr1, ">9").

    IF output-list.kellnr2 EQ 0 THEN odtaker-list.tb = "".
    ELSE odtaker-list.tb = STRING(output-list.kellnr2, ">9").
END. */

/* Oscar (04/12/24) - D9CBFF - add validation to retrieve 
   all order that have order taker */
IF usr-nr EQ 0 THEN
DO:
  FOR EACH h-journal WHERE h-journal.bill-datum GE from-date 
    AND h-journal.bill-datum LE to-date NO-LOCK,
    FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr
    AND h-artikel.departement EQ h-journal.departement 
    AND h-artikel.artart EQ 0 NO-LOCK,
    FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr 
    AND h-bill.departement EQ h-journal.departement 
    AND h-bill.betriebsnr GT 0 NO-LOCK
    BY h-journal.rechnr BY h-journal.sysdate BY h-journal.zeit: 

      RUN create-list. 

      qty = qty + h-journal.anzahl. 
      sub-tot = sub-tot + h-journal.betrag. 
      tot = tot + h-journal.betrag.
      count-data = count-data + 1.
  END.
END.
ELSE
DO:
  FOR EACH h-journal WHERE h-journal.bill-datum GE from-date 
    AND h-journal.bill-datum LE to-date NO-LOCK,
    FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr
    AND h-artikel.departement EQ h-journal.departement 
    AND h-artikel.artart EQ 0 NO-LOCK,
    FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr 
    AND h-bill.departement EQ h-journal.departement 
    AND h-bill.betriebsnr EQ usr-nr NO-LOCK 
    BY h-journal.rechnr BY h-journal.sysdate BY h-journal.zeit: 

      RUN create-list.

      qty = qty + h-journal.anzahl. 
      sub-tot = sub-tot + h-journal.betrag. 
      tot = tot + h-journal.betrag.
      count-data = count-data + 1.
  END.
END.


IF count-data GT 0 THEN
DO:
  CREATE odtaker-list.

  ASSIGN 
    odtaker-list.datum       = ?
    odtaker-list.tableno     = "" 
    odtaker-list.billno      = 0
    odtaker-list.artno       = 0
    odtaker-list.bezeich     = "T O T A L"
    odtaker-list.departement = ""
    odtaker-list.qty         = qty
    odtaker-list.amount      = tot
    odtaker-list.zeit        = "" 
    odtaker-list.id          = ""
    odtaker-list.tb          = ""
  .
END.

PROCEDURE create-list:
  CREATE odtaker-list. 

  FIND FIRST hoteldpt WHERE hoteldpt.num EQ h-journal.departement NO-LOCK NO-ERROR.

  ASSIGN 
    odtaker-list.datum       = h-journal.bill-datum 
    odtaker-list.tableno     = STRING(h-journal.tischnr, ">>>9")
    odtaker-list.billno      = h-journal.rechnr
    odtaker-list.artno       = h-journal.artnr 
    odtaker-list.bezeich     = h-journal.bezeich 
    odtaker-list.qty         = h-journal.anzahl 
    odtaker-list.amount      = h-journal.betrag
    odtaker-list.zeit        = STRING(h-journal.zeit, "HH:MM")
    odtaker-list.id          = STRING(h-bill.betriebsnr, ">>>9")
    odtaker-list.tb          = STRING(h-bill.kellner-nr, ">>>9")
    odtaker-list.departement = hoteldpt.depart
  .
END.
