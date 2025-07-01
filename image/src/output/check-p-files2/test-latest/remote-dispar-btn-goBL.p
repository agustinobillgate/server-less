DEFINE TEMP-TABLE age-list
   field artnr           as integer
   field rechnr          as integer
   field counter         as integer
   field gastnr          as integer
   field rgdatum         as date
   field gastname        as character format "x(34)"
   field p-bal           as decimal format "->>>,>>>,>>9" initial 0
   field debit           as decimal format "->>>,>>>,>>9" initial 0
   field credit          as decimal format "->>>,>>>,>>9" initial 0
   field saldo           as decimal format "->>>,>>>,>>9" initial 0 
   field debt0           as decimal format "->>>,>>>,>>9" initial 0 
   field debt1           as decimal format "->>>,>>>,>>9" initial 0 
   field debt2           as decimal format "->>>,>>>,>>9" initial 0 
   field debt3           as decimal format "->>>,>>>,>>9" initial 0 
  field tot-debt        as decimal format "->>>,>>>,>>9" initial 0. 

define TEMP-TABLE ledger
  field artnr           as integer
  field bezeich         as character format "x(24)" initial "?????"
  field p-bal           as decimal format "->>>,>>>,>>9" initial 0
  field debit           as decimal format "->>>,>>>,>>9" initial 0
  field credit          as decimal format "->>>,>>>,>>9" initial 0
  field debt0           as decimal format "->>>,>>>,>>9" initial 0 
       field debt1           as decimal format "->>>,>>>,>>9" initial 0 
  field debt2           as decimal format "->>>,>>>,>>9" initial 0 
  field debt3           as decimal format "->>>,>>>,>>9" initial 0 
  field tot-debt        as decimal format "->>>,>>>,>>9" initial 0. 

define TEMP-TABLE output-list
  field age1 as char format "x(18)"
  field age2 as char format "x(18)"
  field age3 as char format "x(18)"
  field age4 as char format "x(18)"
  field rechnr as char format "x(9)"
  field str as char.

DEFINE TEMP-TABLE output-list1
    FIELD str-counter   AS CHAR
    FIELD cust-name     AS CHAR
    FIELD prev-balance  AS DECIMAL 
    FIELD debit         AS DECIMAL
    FIELD credit        AS DECIMAL
    FIELD end-balance   AS DECIMAL
    FIELD age1          AS DECIMAL
    FIELD age2          AS DECIMAL
    FIELD age3          AS DECIMAL
    FIELD age4          AS DECIMAL
    FIELD rechnr        AS INTEGER
    FIELD str-pbalance  AS CHAR 
    FIELD str-debit     AS CHAR
    FIELD str-credit    AS CHAR
    FIELD str-ebalance  AS CHAR
    FIELD str-age1      AS CHAR
    FIELD str-age2      AS CHAR
    FIELD str-age3      AS CHAR
    FIELD str-age4      AS CHAR
    FIELD str-rechnr    AS CHAR.


DEFINE INPUT PARAMETER guestno      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER from-art     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER to-art       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER from-name    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER to-name      AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE NO-UNDO.
DEFINE INPUT PARAMETER day1         AS INTEGER NO-UNDO INITIAL 30.
DEFINE INPUT PARAMETER day2         AS INTEGER NO-UNDO INITIAL 30.
DEFINE INPUT PARAMETER day3         AS INTEGER NO-UNDO INITIAL 30.
DEFINE INPUT PARAMETER detailed     AS LOGICAL NO-UNDO INITIAL "no".

DEFINE OUTPUT PARAMETER TABLE FOR output-list1.

DEFINE VARIABLE from-date    AS DATE NO-UNDO.
DEFINE VARIABLE curr-bezeich AS CHAR NO-UNDO.
DEFINE VARIABLE guest-name   AS CHAR NO-UNDO.
DEFINE VARIABLE outlist      AS CHAR NO-UNDO.
DEFINE VARIABLE billname     AS CHAR NO-UNDO.
DEFINE VARIABLE bill-number  AS INTEGER INITIAL 0.
DEFINE VARIABLE long-digit   AS LOGICAL .

run age-list.

procedure age-list:
define variable curr-art as integer.
define variable billdate as date.
define variable counter as integer format ">>>9".
define variable t-comm       as decimal format "->,>>>,>>>,>>9" initial 0.
define variable t-adjust     as decimal format "->,>>>,>>>,>>9" initial 0.
define variable t-saldo      as decimal format "->>,>>>,>>>,>>9" initial 0.
define variable t-prev       as decimal format "->>,>>>,>>>,>>9" initial 0.
define variable t-debit      as decimal format "->,>>>,>>>,>>9" initial 0.
define variable t-credit     as decimal format "->,>>>,>>>,>>9" initial 0.
define variable t-debt0      as decimal format "->,>>>,>>>,>>9" initial 0.
define variable t-debt1      as decimal format "->,>>>,>>>,>>9" initial 0.
define variable t-debt2      as decimal format "->,>>>,>>>,>>9" initial 0.
define variable t-debt3      as decimal format "->,>>>,>>>,>>9" initial 0.
define variable tmp-saldo    as decimal format "->>>>>>>>>>9" initial 0.
define variable curr-name    as character format "x(24)".
define variable curr-gastnr  as integer.
define variable gastname     as character format "x(34)".
define variable p-bal        as decimal format "->>,>>>,>>9".
define variable debit        as decimal format "->>,>>>,>>9".
define variable credit       as decimal format "->>,>>>,>>9".
define variable debt0        as decimal format "->>,>>>,>>9".
define variable debt1        as decimal format "->>,>>>,>>9".
define variable debt2        as decimal format "->>,>>>,>>9".
define variable debt3        as decimal format "->>,>>>,>>9".
define variable tot-debt     as decimal format "->>>,>>>,>>9".
define variable i as integer.
define buffer debtrec for debitor.
define buffer debt for debitor.
define variable curr-counter as integer initial 0.

  for each ledger:
    delete ledger.
  end.
  for each age-list:
    delete age-list.
  end.
  for each output-list:
    delete output-list.
  end.

  from-date = date(month(to-date), 1, year(to-date)).
  for each artikel where (artikel.artart = 2 or artikel.artart = 7)
      and artikel.artnr GE from-art and artikel.artnr LE to-art
      and artikel.departement = 0
      no-lock by (string(artikel.artart) + string(artikel.artnr,"9999")):
      
    curr-bezeich = string(artikel.artnr, ">>>9") + " - " + artikel.bezeich.

    create ledger.
    ledger.artnr = artikel.artnr.
    ledger.bezeich = string(artikel.artnr) + "  -  " + artikel.bezeich. 
  end.

/* not paid or partial paid */      
  curr-art = 0.
  for each debitor where debitor.rgdatum LE to-date 
    and debitor.artnr GE from-art and debitor.artnr LE to-art 
    and debitor.opart LE 1 AND debitor.gastnr = guestno 
    no-lock use-index artdat_ix
    by debitor.artnr by debitor.zahlkonto: 

    if debitor.name GE from-name and debitor.name LE to-name then
    do:
      if curr-art NE debitor.artnr then
      do:
        curr-art = debitor.artnr.
        find first artikel where artikel.artnr = curr-art
           and artikel.departement = 0  no-lock no-error.
      end.
  
      if debitor.counter > 0 then find first age-list where 
        age-list.counter = debitor.counter
/*      and debitor.artnr = age-list.artnr
        and debitor.gastnr = age-list.gastnr 
        and debitor.rechnr = age-list.rechnr    */
        no-error.
      if (debitor.counter = 0) or (not available age-list) then
      do:
/* create aging record for a specific guest, based on A/R-debit record */    
        find first guest where guest.gastnr = debitor.gastnr no-lock.
        create age-list.
        age-list.artnr = debitor.artnr.
        age-list.rechnr = debitor.rechnr.
        age-list.rgdatum = debitor.rgdatum.
        age-list.counter = debitor.counter.
        age-list.gastnr = debitor.gastnr.
        age-list.tot-debt = 0.
        if artikel.artart = 2 then age-list.gastname = guest.name + ", " 
           + guest.vorname1 + guest.anredefirma + " " + guest.anrede1.
        else
        do:
          find first htparam where paramnr = 867 no-lock.
          if debitor.gastnr = htparam.finteger then
            age-list.gastname = "F&B " + artikel.bezeich.
          else age-list.gastname = "F/O " + artikel.bezeich.
        end.
        guest-name = guest.name + ", " + guest.vorname1 
          + guest.anredefirma + " " + guest.anrede1.
      end.
      age-list.tot-debt = age-list.tot-debt + debitor.saldo.
    
/* previous balance  */
      if debitor.rgdatum LT from-date and debitor.zahlkonto = 0 then
        age-list.p-bal = age-list.p-bal + debitor.saldo.

/* debit transaction */
      if debitor.rgdatum GE from-date and debitor.zahlkonto = 0 then
        age-list.debit = age-list.debit + debitor.saldo.

/* credit transaction */
      if debitor.rgdatum LT from-date and debitor.zahlkonto NE 0 then
        age-list.p-bal = age-list.p-bal + debitor.saldo.
      else
      do:
        if debitor.rgdatum GE from-date and debitor.zahlkonto NE 0 then
          age-list.credit = age-list.credit - debitor.saldo.
      end.
    end.
  end.

/*  within period's full paid transaction */
  for each artikel where (artikel.artart = 2 or artikel.artart = 7)
      and artikel.artnr GE from-art and artikel.artnr LE to-art
      and artikel.departement = 0 no-lock by artikel.artnr:

    curr-bezeich = string(artikel.artnr, ">>>9") + " - " + artikel.bezeich.
    
    curr-counter = 0.
    for each debitor where debitor.artnr = artikel.artnr
      and debitor.rgdatum LE to-date 
      and debitor.opart EQ 2 and debitor.zahlkonto EQ 0
      AND debitor.gastnr = guestno use-index artdat_ix no-lock:        
      if debitor.name GE from-name and debitor.name LE to-name then
      do:  
/* create aging record for a specific guest */    
        find first guest where guest.gastnr = debitor.gastnr no-lock.
        create age-list.
        age-list.artnr = debitor.artnr.
        age-list.rechnr = debitor.rechnr.
        age-list.rgdatum = debitor.rgdatum.
        age-list.counter = debitor.counter.
        age-list.gastnr = debitor.gastnr.
        age-list.tot-debt = debitor.saldo.
        if artikel.artart = 2 then age-list.gastname = guest.name + ", " 
          + guest.vorname1 + guest.anredefirma + " " + guest.anrede1.
        else
        do:
          find first htparam where paramnr = 867 no-lock.
          if debitor.gastnr = htparam.finteger then
            age-list.gastname = "F&B " + artikel.bezeich.
          else age-list.gastname = "F/O " + artikel.bezeich.
        end.
        guest-name = guest.name + ", " + guest.vorname1 
          + guest.anredefirma + " " + guest.anrede1.
        
        if debitor.rgdatum LT from-date then
            age-list.p-bal = age-list.p-bal + debitor.saldo.
        else if debitor.rgdatum GE from-date then
        age-list.debit = age-list.debit + debitor.saldo.
   
        for each debtrec where debtrec.counter = debitor.counter
          and debtrec.rechnr = debitor.rechnr and debtrec.zahlkonto GT 0
          and debtrec.rgdatum LE to-date no-lock use-index counter_ix:
          age-list.tot-debt = age-list.tot-debt + debtrec.saldo.
          if debtrec.rgdatum LT from-date then
            age-list.p-bal = age-list.p-bal + debtrec.saldo.
          else if debtrec.rgdatum GE from-date then
            age-list.credit = age-list.credit - debtrec.saldo.
        end.
      end.
    end.
  end.

  for each ledger by ledger.artnr:
     FIND FIRST age-list WHERE age-list.artnr = ledger.artnr NO-LOCK NO-ERROR.
     IF NOT AVAILABLE age-list THEN NEXT.
         
    /*outlist = "    " + caps(ledger.bezeich).
    run fill-in-list(NO).
    outlist = "".
    run fill-in-list(NO).  */

    CREATE output-list1.
    ASSIGN
      output-list1.str-counter      = " "
      output-list1.cust-name        = caps(ledger.bezeich).
          

    counter = 0.
    curr-gastnr = 0.
    for each age-list where age-list.artnr = ledger.artnr 
      /* and age-list.tot-debt NE 0 */ by age-list.gastname
      by age-list.rechnr:
      if to-date - age-list.rgdatum GT day3 
        then age-list.debt3 = age-list.tot-debt.
      else if to-date - age-list.rgdatum GT day2
        then age-list.debt2 = age-list.tot-debt.
      else if to-date - age-list.rgdatum GT day1
        then age-list.debt1 = age-list.tot-debt.
      else age-list.debt0 = age-list.tot-debt.
      
      ledger.tot-debt = ledger.tot-debt + age-list.tot-debt.
      ledger.p-bal = ledger.p-bal + age-list.p-bal.
      ledger.debit = ledger.debit + age-list.debit.
      ledger.credit = ledger.credit + age-list.credit.
      ledger.debt0 = ledger.debt0 + age-list.debt0.
      ledger.debt1 = ledger.debt1 + age-list.debt1.
      ledger.debt2 = ledger.debt2 + age-list.debt2.
      ledger.debt3 = ledger.debt3 + age-list.debt3.
      t-saldo  = t-saldo  + age-list.tot-debt.
      t-prev   = t-prev   + age-list.p-bal.
      t-debit  = t-debit  + age-list.debit.
      t-credit = t-credit + age-list.credit.
      t-debt0  = t-debt0 + age-list.debt0.
      t-debt1  = t-debt1 + age-list.debt1.
      t-debt2  = t-debt2 + age-list.debt2.
      t-debt3  = t-debt3 + age-list.debt3.
      if curr-gastnr = 0 then
      do:
        bill-number = age-list.rechnr.
        gastname = age-list.gastname.
        tot-debt = age-list.tot-debt.
        p-bal = age-list.p-bal.
        debit = age-list.debit.
        credit = age-list.credit.
        debt0 = age-list.debt0. 
        debt1 = age-list.debt1. 
        debt2 = age-list.debt2. 
        debt3 = age-list.debt3. 
        counter = counter + 1.
      end.
      ELSE if curr-name NE age-list.gastname then
      do:
        if p-bal NE 0 or debit NE 0 or credit NE 0 then
        do:
          CREATE output-list1.
          ASSIGN
              output-list1.str-counter      = STRING(counter, ">>>>>>9")
              output-list1.cust-name        = gastname
              output-list1.prev-balance     = p-bal
              output-list1.debit            = debit
              output-list1.credit           = credit
              output-list1.end-balance      = tot-debt
              output-list1.age1             = debt0 
              output-list1.age2             = debt1
              output-list1.age3             = debt2
              output-list1.age4             = debt3
              output-list1.rechnr           = age-list.rechnr
              output-list1.str-pbalance     = string(p-bal, "->>,>>>,>>>,>>9.99")
              output-list1.str-debit        = STRING(debit, "->>,>>>,>>>,>>9.99")
              output-list1.str-credit       = string(credit, "->>,>>>,>>>,>>9.99")
              output-list1.str-ebalance     = string(tot-debt, "->>,>>>,>>>,>>9.99") 
              output-list1.str-age1         = string(debt0, "->>,>>>,>>>,>>9.99") 
              output-list1.str-age2         = string(debt1, "->>,>>>,>>>,>>9.99")
              output-list1.str-age3         = string(debt2, "->>,>>>,>>>,>>9.99")
              output-list1.str-age4         = string(debt3, "->>,>>>,>>>,>>9.99")
              output-list1.str-rechnr       = string(age-list.rechnr, ">>>>>>9").

          /*if not long-digit then outlist = "  " + string(counter,">>>9 ")
             + string(gastname, "x(30)")
             + string(tot-debt, "->>,>>>,>>>,>>9.99") 
             + string(p-bal, "->>,>>>,>>>,>>9.99")
             + string(debit, "->>,>>>,>>>,>>9.99")
             + string(credit, "->>,>>>,>>>,>>9.99")
             + string(debt0, "->>,>>>,>>>,>>9.99")
             + string(debt1, "->>,>>>,>>>,>>9.99")
             + string(debt2, "->>,>>>,>>>,>>9.99")
             + string(debt3, "->>,>>>,>>>,>>9.99").
          else outlist = "  " + string(counter,">>>9 ")
             + string(gastname, "x(30)")
             + string(tot-debt, "->,>>>,>>>,>>>,>>9") 
             + string(p-bal, "->,>>>,>>>,>>>,>>9")
             + string(debit, "->,>>>,>>>,>>>,>>9")
             + string(credit, "->,>>>,>>>,>>>,>>9")
             + string(debt0, "->,>>>,>>>,>>>,>>9")
             + string(debt1, "->,>>>,>>>,>>>,>>9")
             + string(debt2, "->,>>>,>>>,>>>,>>9")
             + string(debt3, "->,>>>,>>>,>>>,>>9").
            run fill-in-list(YES).*/
        end.
        ELSE counter = counter - 1.
        bill-number = age-list.rechnr.
        gastname = age-list.gastname.
        tot-debt = age-list.tot-debt.
        p-bal = age-list.p-bal.
        debit = age-list.debit.
        credit = age-list.credit.
        debt0 = age-list.debt0. 
        debt1 = age-list.debt1. 
        debt2 = age-list.debt2. 
        debt3 = age-list.debt3. 
        counter = counter + 1. 
      end.
      ELSE DO:
        tot-debt = tot-debt + age-list.tot-debt.
        p-bal = p-bal + age-list.p-bal.
        debit = debit + age-list.debit.
        credit = credit + age-list.credit.
        debt0 = debt0 + age-list.debt0. 
        debt1 = debt1 + age-list.debt1. 
        debt2 = debt2 + age-list.debt2. 
        debt3 = debt3 + age-list.debt3. 
      end.
      curr-gastnr = age-list.gastnr.
      if not detailed then curr-name = age-list.gastname.
      delete age-list.
    end.
    if counter GT 0 and (p-bal NE 0 or debit NE 0 or credit NE 0) then
    do:
        CREATE output-list1.
        ASSIGN
              output-list1.str-counter      = STRING(counter, ">>>>>>9")
              output-list1.cust-name        = gastname
              output-list1.prev-balance     = p-bal
              output-list1.debit            = debit
              output-list1.credit           = credit
              output-list1.end-balance      = tot-debt
              output-list1.age1             = debt0 
              output-list1.age2             = debt1
              output-list1.age3             = debt2
              output-list1.age4             = debt3
              output-list1.rechnr           = bill-number
              output-list1.str-pbalance     = string(p-bal, "->>,>>>,>>>,>>9.99")
              output-list1.str-debit        = STRING(debit, "->>,>>>,>>>,>>9.99")
              output-list1.str-credit       = string(credit, "->>,>>>,>>>,>>9.99")
              output-list1.str-ebalance     = string(tot-debt, "->>,>>>,>>>,>>9.99") 
              output-list1.str-age1         = string(debt0, "->>,>>>,>>>,>>9.99") 
              output-list1.str-age2         = string(debt1, "->>,>>>,>>>,>>9.99")
              output-list1.str-age3         = string(debt2, "->>,>>>,>>>,>>9.99")
              output-list1.str-age4         = string(debt3, "->>,>>>,>>>,>>9.99")
              output-list1.str-rechnr       = string(bill-number, ">>>>>>9").

      /*if not long-digit then
      outlist = "  " + string(counter,">>>9 ")
           + string(gastname, "x(30)")
           + string(tot-debt, "->>,>>>,>>>,>>9.99")
           + string(p-bal, "->>,>>>,>>>,>>9.99")
           + string(debit, "->>,>>>,>>>,>>9.99")
           + string(credit, "->>,>>>,>>>,>>9.99")
           + string(debt0, "->>,>>>,>>>,>>9.99")
           + string(debt1, "->>,>>>,>>>,>>9.99")
           + string(debt2, "->>,>>>,>>>,>>9.99")
           + string(debt3, "->>,>>>,>>>,>>9.99").
      else outlist = "  " + string(counter,">>>9 ")
           + string(gastname, "x(30)")
           + string(tot-debt, "->,>>>,>>>,>>>,>>9")
           + string(p-bal, "->,>>>,>>>,>>>,>>9")
           + string(debit, "->,>>>,>>>,>>>,>>9")
           + string(credit, "->,>>>,>>>,>>>,>>9")
           + string(debt0, "->,>>>,>>>,>>>,>>9")
           + string(debt1, "->,>>>,>>>,>>>,>>9")
           + string(debt2, "->,>>>,>>>,>>>,>>9")
           + string(debt3, "->,>>>,>>>,>>>,>>9").
      run fill-in-list(YES).*/
   end.
   else counter = counter - 1.
    
    tmp-saldo = ledger.tot-debt.
    if tmp-saldo = 0 then tmp-saldo = 1.

    CREATE output-list1.
    ASSIGN
        output-list1.str-counter      = FILL("-",7)
        output-list1.cust-name        = FILL("-",30)
        output-list1.str-pbalance     = FILL("-",18)
        output-list1.str-debit        = FILL("-",18)
        output-list1.str-credit       = FILL("-",18)
        output-list1.str-ebalance     = FILL("-",18)
        output-list1.str-age1         = FILL("-",18) 
        output-list1.str-age2         = FILL("-",18)
        output-list1.str-age3         = FILL("-",18)
        output-list1.str-age4         = FILL("-",18)
        output-list1.str-rechnr       = FILL("-",7).

    CREATE output-list1.
    ASSIGN
          output-list1.str-counter      = " "
          output-list1.cust-name        = "T o t a l"
          output-list1.prev-balance     = ledger.p-bal
          output-list1.debit            = ledger.debit
          output-list1.credit           = ledger.credit
          output-list1.end-balance      = ledger.tot-debt
          output-list1.age1             = ledger.debt0 
          output-list1.age2             = ledger.debt1
          output-list1.age3             = ledger.debt2
          output-list1.age4             = ledger.debt3
          output-list1.rechnr           = 0
          output-list1.str-pbalance     = string(ledger.p-bal, "->>,>>>,>>>,>>9.99")
          output-list1.str-debit        = STRING(ledger.debit, "->>,>>>,>>>,>>9.99")
          output-list1.str-credit       = string(ledger.credit, "->>,>>>,>>>,>>9.99")
          output-list1.str-ebalance     = string(ledger.tot-debt, "->>,>>>,>>>,>>9.99") 
          output-list1.str-age1         = string(ledger.debt0, "->>,>>>,>>>,>>9.99") 
          output-list1.str-age2         = string(ledger.debt1, "->>,>>>,>>>,>>9.99")
          output-list1.str-age3         = string(ledger.debt2, "->>,>>>,>>>,>>9.99")
          output-list1.str-age4         = string(ledger.debt3, "->>,>>>,>>>,>>9.99")
          output-list1.str-rechnr       = " ".

    /*outlist =  
    "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------".
    run fill-in-list(NO).
    if not long-digit then
    outlist = "       " 
      + string(translateExtended ("T o t a l",lvCAREA,""), "x(30)")
      + string(ledger.tot-debt, "->>,>>>,>>>,>>9.99")
      + string(ledger.p-bal, "->>,>>>,>>>,>>9.99")
      + string(ledger.debit, "->>,>>>,>>>,>>9.99")
      + string(ledger.credit, "->>,>>>,>>>,>>9.99")
      + string(ledger.debt0, "->>,>>>,>>>,>>9.99")
      + string(ledger.debt1, "->>,>>>,>>>,>>9.99")
      + string(ledger.debt2, "->>,>>>,>>>,>>9.99")
      + string(ledger.debt3, "->>,>>>,>>>,>>9.99"). 
    else outlist = "       " 
      + string(translateExtended ("T o t a l",lvCAREA,""), "x(30)")
      + string(ledger.tot-debt, "->,>>>,>>>,>>>,>>9")
      + string(ledger.p-bal, "->,>>>,>>>,>>>,>>9")
      + string(ledger.debit, "->,>>>,>>>,>>>,>>9")
      + string(ledger.credit, "->,>>>,>>>,>>>,>>9")
      + string(ledger.debt0, "->,>>>,>>>,>>>,>>9")
      + string(ledger.debt1, "->,>>>,>>>,>>>,>>9")
      + string(ledger.debt2, "->,>>>,>>>,>>>,>>9")
      + string(ledger.debt3, "->,>>>,>>>,>>>,>>9"). 
    run fill-in-list(NO).*/

    CREATE output-list1.
    ASSIGN
          output-list1.str-counter      = " "
          output-list1.cust-name        = "Statistic Percentage (%) :"
          output-list1.prev-balance     = 0
          output-list1.debit            = 0
          output-list1.credit           = 0
          output-list1.end-balance      = 100.00
          output-list1.age1             = (ledger.debt0 / tmp-saldo * 100) 
          output-list1.age2             = (ledger.debt1 / tmp-saldo * 100)
          output-list1.age3             = (ledger.debt2 / tmp-saldo * 100)
          output-list1.age4             = (ledger.debt3 / tmp-saldo * 100)
          output-list1.rechnr           = 0
          output-list1.str-pbalance     = " "
          output-list1.str-debit        = " "
          output-list1.str-credit       = " "
          output-list1.str-ebalance     = string(100.00, "->>,>>>,>>>,>>9.99")
          output-list1.str-age1         = string((ledger.debt0 / tmp-saldo * 100), "->>,>>>,>>>,>>9.99") 
          output-list1.str-age2         = string((ledger.debt1 / tmp-saldo * 100), "->>,>>>,>>>,>>9.99")
          output-list1.str-age3         = string((ledger.debt2 / tmp-saldo * 100), "->>,>>>,>>>,>>9.99")
          output-list1.str-age4         = string((ledger.debt3 / tmp-saldo * 100), "->>,>>>,>>>,>>9.99")
          output-list1.str-rechnr       = " ".
    /*
    outlist = "       " 
        + string(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)")
        + "            100.00".

    do i = 1 to 54:
      outlist = outlist + " ".
    end.
    outlist = outlist 
      + string((ledger.debt0 / tmp-saldo * 100), "           ->>9.99") 
      + string((ledger.debt1 / tmp-saldo * 100), "           ->>9.99") 
      + string((ledger.debt2 / tmp-saldo * 100), "           ->>9.99")
      + string((ledger.debt3 / tmp-saldo * 100), "           ->>9.99").
    run fill-in-list(NO).
    outlist = "".
    run fill-in-list(NO).*/
  end.     

end.
 
procedure fill-in-list:
define input parameter fill-billno as logical.
  create output-list.
  if fill-billno /* and available age-list */
    then output-list.rechnr = string(bill-number,">>>>>>>>>").
  output-list.str = outlist.
  if substr(outlist,1,5) = "-----" then output-list.rechnr = "---------".
  output-list.age1 = substring(str,110, 18).
  output-list.age2 = substring(str,128, 18).
  output-list.age3 = substring(str,146, 18).
  output-list.age4 = substring(str,164, 18).
end.

