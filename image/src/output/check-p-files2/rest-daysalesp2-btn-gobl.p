
DEFINE TEMP-TABLE other-art
    FIELD artnr         AS INTEGER.

DEFINE TEMP-TABLE temp
    FIELD rechnr      AS INTEGER.

DEFINE TEMP-TABLE t-tot-betrag
    FIELD tot-betrag1 AS DECIMAL
    FIELD tot-betrag2 AS DECIMAL
    FIELD tot-betrag3 AS DECIMAL
    FIELD tot-betrag4 AS DECIMAL
    FIELD tot-betrag5 AS DECIMAL
    FIELD tot-betrag6 AS DECIMAL
    FIELD tot-betrag7 AS DECIMAL
    FIELD tot-betrag8 AS DECIMAL
    FIELD tot-betrag9 AS DECIMAL
    FIELD tot-betrag10 AS DECIMAL
/*extent 10 gerald 4A7817*/
    FIELD tot-betrag11 AS DECIMAL
    FIELD tot-betrag12 AS DECIMAL
    FIELD tot-betrag13 AS DECIMAL
    FIELD tot-betrag14 AS DECIMAL
    FIELD tot-betrag15 AS DECIMAL
    FIELD tot-betrag16 AS DECIMAL
    FIELD tot-betrag17 AS DECIMAL
    FIELD tot-betrag18 AS DECIMAL
    FIELD tot-betrag19 AS DECIMAL
    FIELD tot-betrag20 AS DECIMAL.

DEFINE TEMP-TABLE t-nt-betrag
    FIELD nt-betrag1 AS DECIMAL
    FIELD nt-betrag2 AS DECIMAL
    FIELD nt-betrag3 AS DECIMAL
    FIELD nt-betrag4 AS DECIMAL
    FIELD nt-betrag5 AS DECIMAL
    FIELD nt-betrag6 AS DECIMAL
    FIELD nt-betrag7 AS DECIMAL
    FIELD nt-betrag8 AS DECIMAL
    FIELD nt-betrag AS DECIMAL
    FIELD nt-betrag10 AS DECIMAL
    /*extent 10 gerald 4A7817*/
    FIELD nt-betrag11 AS DECIMAL
    FIELD nt-betrag12 AS DECIMAL
    FIELD nt-betrag13 AS DECIMAL
    FIELD nt-betrag14 AS DECIMAL
    FIELD nt-betrag15 AS DECIMAL
    FIELD nt-betrag16 AS DECIMAL
    FIELD nt-betrag17 AS DECIMAL
    FIELD nt-betrag18 AS DECIMAL
    FIELD nt-betrag19 AS DECIMAL
    FIELD nt-betrag20 AS DECIMAL.

define TEMP-TABLE bline-list 
  field selected as logical initial yes 
  field depart as char 
  field dept as integer 
  field knr as integer 
  field bl-recid as integer. 

define TEMP-TABLE outstand-list 
  field name as char format "x(16)" 
  field rechnr as integer format "->,>>>,>>9"
  field foreign as decimal format "->,>>>,>>9.99" 
  field saldo as decimal format "->>>,>>>,>>9.99". 

define TEMP-TABLE pay-list 
  field compli as logical initial no 
  field person as integer 
  field flag as integer /* 1 cash  2 room  3 CC  4 EL  5 CL  6 Comp  */ 
  field bezeich as char format "x(24)" 
  field artnr as integer format ">>>>9 " 
  field rechnr as integer format ">>>>>>9 " 
  field foreign as decimal format "->,>>>,>>9.99" 
  field saldo as decimal format "->>>,>>>,>>9.99". 

DEFINE BUFFER pay-listbuff FOR pay-list.

define TEMP-TABLE turnover 
  field departement     like h-bill.departement 
  field kellner-nr      like h-bill.kellner-nr 
  field name            like kellner.kellnername 
  field tischnr         like h-bill.tischnr column-label "Tbl" 
  field rechnr          as char format "x(7)" column-label "Bill-No" 
  field belegung        as integer format "->>>>>>9" column-label "Pax" 
  field artnr           like h-bill-line.artnr 
  field info            as char format "x(6)"        label "Info" 
  /*FIELD betrag          AS DECIMAL EXTENT 10 FORMAT "->>>,>>>,>>9"  
  FIELD other           AS DECIMAL FORMAT "->>>,>>>,>>9" 
  field t-service       as decimal format "->>>,>>>,>>9"  column-label "Service" 
  field t-tax           as decimal format "->>>,>>>,>>9"  column-label "Tax"   
  field t-debit         as decimal format "->>>,>>>,>>9" label "Total" 
  field t-credit        as decimal format "->>>,>>>,>>9"  
  field p-cash          as decimal format "->>>,>>>,>>9"  
  field p-cash1         as decimal format "->>>,>>>,>>9.99"  
  field r-transfer      as decimal format "->>>,>>>,>>9" label "Transfer" 
  field c-ledger        as decimal format "->>>,>>>,>>9" label "CC / CL" */
  FIELD betrag          AS DECIMAL EXTENT 20    /*extent 10 gerald 4A7817*/
  FIELD other           AS DECIMAL 
  field t-service       as decimal 
  field t-tax           as decimal 
  field t-debit         as decimal 
  field t-credit        as decimal 
  field p-cash          as decimal 
  field p-cash1         as decimal 
  field r-transfer      as decimal 
  field c-ledger        as decimal 
  FIELD compli          AS LOGICAL INITIAL NO
  FIELD flag            AS INTEGER INITIAL 0
  FIELD gname           AS CHAR FORMAT "x(16)" COLUMN-LABEL "Guest Name"
  FIELD int-rechnr      AS INT
  FIELD st-comp         AS INT INIT 0
  FIELD p-curr          AS CHAR
  FIELD t-vat           AS DECIMAL COLUMN-LABEL "Other Tax".

DEF INPUT PARAMETER TABLE FOR bline-list.
DEF INPUT PARAMETER disc-art1 AS INT.
DEF INPUT PARAMETER disc-art2 AS INT.
DEF INPUT PARAMETER disc-art3 AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER all-user AS LOGICAL.
DEF INPUT PARAMETER shift AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER art-str AS CHAR.
DEF INPUT PARAMETER voucher-art AS INT.
DEF INPUT PARAMETER zero-vat-compli AS LOGICAL.
DEF INPUT PARAMETER show-fbodisc AS LOGICAL.

DEF OUTPUT PARAMETER t-betrag AS DECIMAL.
DEF OUTPUT PARAMETER t-foreign AS DECIMAL.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.
DEF OUTPUT PARAMETER tot-serv     as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-tax      as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-debit    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-cash     as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-cash1    as decimal format "->>,>>>,>>>,>>9". /*"->>>,>>9.99".*/ 
DEF OUTPUT PARAMETER tot-trans    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-ledger   as decimal format "->>>,>>>,>>9". /*MT*/
DEF OUTPUT PARAMETER tot-cover    as integer format ">>>9".
DEF OUTPUT PARAMETER nt-cover    as integer format ">>>9". 
DEF OUTPUT PARAMETER tot-other    AS DECIMAL FORMAT "->>>,>>>,>>9".
DEF OUTPUT PARAMETER nt-other     AS DECIMAL FORMAT "->>>,>>>,>>9".
DEF OUTPUT PARAMETER nt-serv     as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-tax      as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-debit    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-cash     as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-cash1    as decimal format "->>,>>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-trans    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-ledger   as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-vat    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-vat     as decimal format "->>>,>>>,>>9". 

DEF OUTPUT PARAMETER avail-outstand-list AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR turnover.
DEF OUTPUT PARAMETER TABLE FOR t-tot-betrag.
DEF OUTPUT PARAMETER TABLE FOR t-nt-betrag.
DEF OUTPUT PARAMETER TABLE FOR outstand-list.
DEF OUTPUT PARAMETER TABLE FOR pay-list.

DEFINE VARIABLE tot-betrag   AS DECIMAL EXTENT 20 FORMAT "->>>,>>>,>>9".    /*extent 10 gerald 4A7817*/
DEFINE VARIABLE nt-betrag    AS DECIMAL EXTENT 20 FORMAT "->>>,>>>,>>9".    /*extent 10 gerald 4A7817*/

define variable t-cash1    as decimal format "->>,>>>,>>>,>>9".

DEFINE VARIABLE tt-other     AS DECIMAL FORMAT "->>>,>>>,>>9".


define variable anz-comp as integer format ">>9". 
define variable val-comp as decimal format "->,>>>,>>9.99". 
define variable anz-coup as integer format ">>9". 
define variable val-coup as decimal format "->,>>>,>>9.99". 
/*wenni*/
DEFINE VARIABLE total-Fdisc     AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 NO-UNDO.
DEFINE VARIABLE total-Bdisc     AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 NO-UNDO.
DEFINE VARIABLE total-Odisc     AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0 NO-UNDO.
/*end wenni*/
define variable t-serv     as decimal format "->>>,>>>,>>9". 
define variable t-tax      as decimal format "->>>,>>>,>>9". 
define variable t-debit    as decimal format "->>>,>>>,>>9". 
define variable t-cash     as decimal format "->>>,>>>,>>9". 
define variable t-trans    as decimal format "->>>,>>>,>>9". 
define variable t-ledger   as decimal format "->>>,>>>,>>9". 
define variable t-cover    as integer format ">>>9". 

DEF VAR fo-disc1 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR fo-disc2 AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR fo-disc3 AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE tt-betrag    AS DECIMAL EXTENT 20 FORMAT "->>>,>>>,>>9".    /*extent 10 gerald 4A7817*/
DEFINE VARIABLE multi-vat    AS LOGICAL NO-UNDO.

DEF VAR i AS INT.
define variable artnr-list as integer extent 20.        /*extent 10 gerald 4A7817*/ 
DO i = 1 TO NUM-ENTRIES(art-str, ","):
    IF i GT 21 THEN .
    ELSE
        artnr-list[i] = INTEGER(ENTRY(i, art-str, ",")).
END.
FIND FIRST htparam WHERE htparam.paramnr = 271 NO-LOCK NO-ERROR.
ASSIGN multi-vat = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK no-error. 
IF AVAILABLE waehrung then exchg-rate = waehrung.ankauf / waehrung.einheit. 
ELSE exchg-rate = 1.

FOR EACH temp:
    DELETE temp.
END.

IF NOT all-user THEN RUN daysale-list. 
ELSE RUN daysale-list1.

DEFINE VARIABLE pax-cash AS INT.
DEFINE VARIABLE pax      AS INT.
DEFINE VARIABLE pax2     AS INT INIT 0.

FOR EACH turnover NO-LOCK:
    FIND FIRST h-bill WHERE h-bill.rechnr = INT(turnover.rechnr)
        AND h-bill.departement =  curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill AND turnover.p-cash NE 0 THEN
        pax-cash = pax-cash + turnover.belegung.
        /*pax-cash = pax-cash + h-bill.belegung.*/
    IF AVAILABLE h-bill THEN turnover.belegung = h-bill.belegung.
END.

FOR EACH pay-list WHERE pay-list.flag = 1 AND pay-list.foreign NE 0:
    pax2 = pax2 + 1.
END.

FIND FIRST turnover NO-LOCK NO-ERROR.
IF AVAILABLE turnover THEN
DO:
    FIND FIRST pay-list WHERE pay-list.flag = 1 AND pay-list.saldo NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE pay-list THEN pay-list.person = pax-cash.
    
    FIND FIRST pay-list WHERE pay-list.flag = 1 AND pay-list.foreign NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE pay-list THEN pay-list.person = pax2.

    FOR EACH pay-list WHERE pay-list.flag NE 2 NO-LOCK:
        pax = pax + pay-list.person.
    END.
    
    FIND FIRST turnover WHERE turnover.rechnr = "G-Total" NO-LOCK NO-ERROR.
    IF AVAILABLE turnover THEN
    DO:
        FIND FIRST pay-list WHERE pay-list.flag = 2 NO-LOCK NO-ERROR.
        IF AVAILABLE pay-list THEN
            pay-list.person = turnover.belegung - pax.
    END.                                              
    
    IF AVAIL outstand-list THEN
        avail-outstand-list = YES.
    
    CREATE t-tot-betrag.                                
    ASSIGN
        t-tot-betrag.tot-betrag1    = tot-betrag[1]
        t-tot-betrag.tot-betrag2    = tot-betrag[2]
        t-tot-betrag.tot-betrag3    = tot-betrag[3]
        t-tot-betrag.tot-betrag4    = tot-betrag[4]
        t-tot-betrag.tot-betrag5    = tot-betrag[5]
        t-tot-betrag.tot-betrag6    = tot-betrag[6]
        t-tot-betrag.tot-betrag7    = tot-betrag[7]
        t-tot-betrag.tot-betrag8    = tot-betrag[8]
        t-tot-betrag.tot-betrag9    = tot-betrag[9]
        t-tot-betrag.tot-betrag10   = tot-betrag[10]
        t-tot-betrag.tot-betrag11   = tot-betrag[11]
        t-tot-betrag.tot-betrag12   = tot-betrag[12]
        t-tot-betrag.tot-betrag13   = tot-betrag[13]
        t-tot-betrag.tot-betrag14   = tot-betrag[14]
        t-tot-betrag.tot-betrag15   = tot-betrag[15]
        t-tot-betrag.tot-betrag16   = tot-betrag[16]
        t-tot-betrag.tot-betrag17   = tot-betrag[17]
        t-tot-betrag.tot-betrag18   = tot-betrag[18]
        t-tot-betrag.tot-betrag19   = tot-betrag[19]
        t-tot-betrag.tot-betrag20   = tot-betrag[20].
    
    CREATE t-nt-betrag.
    ASSIGN
        t-nt-betrag.nt-betrag1    = nt-betrag[1]
        t-nt-betrag.nt-betrag2    = nt-betrag[2]
        t-nt-betrag.nt-betrag3    = nt-betrag[3]
        t-nt-betrag.nt-betrag4    = nt-betrag[4]
        t-nt-betrag.nt-betrag5    = nt-betrag[5]
        t-nt-betrag.nt-betrag6    = nt-betrag[6]
        t-nt-betrag.nt-betrag7    = nt-betrag[7]
        t-nt-betrag.nt-betrag8    = nt-betrag[8]
        t-nt-betrag.nt-betrag     = nt-betrag[9]
        t-nt-betrag.nt-betrag10   = nt-betrag[10]
        t-nt-betrag.nt-betrag11   = nt-betrag[11]
        t-nt-betrag.nt-betrag12   = nt-betrag[12]
        t-nt-betrag.nt-betrag13   = nt-betrag[13]
        t-nt-betrag.nt-betrag14   = nt-betrag[14]
        t-nt-betrag.nt-betrag15   = nt-betrag[15]
        t-nt-betrag.nt-betrag16   = nt-betrag[16]
        t-nt-betrag.nt-betrag17   = nt-betrag[17]
        t-nt-betrag.nt-betrag18   = nt-betrag[18]
        t-nt-betrag.nt-betrag19   = nt-betrag[19]
        t-nt-betrag.nt-betrag10   = nt-betrag[20].
END.                                              
/*========================================================================================================*/
procedure daysale-list1: 
define variable curr-s  as integer. 
define variable billnr  as integer. 
define variable dept    as integer format ">>9" initial 1. 
define variable d-name  as character format "x(24)". 
define variable usr-nr as integer. 
define variable d-found as logical initial "no". 
define variable c-found as logical initial "no". 
define variable vat     as decimal. 
define variable vat2    as decimal. 
define variable service as decimal.
DEFINE VARIABLE fact      AS DECIMAL. 
define variable netto   as decimal. 
define variable i       as integer. 
DEFINE VARIABLE pos     AS INTEGER.
DEFINE VARIABLE bill-no AS INTEGER.
DEFINE VARIABLE guestname AS CHAR.
define variable found   as logical initial no. 
DEF BUFFER tlist FOR turnover.
DEF BUFFER h-bline FOR h-bill-line.

  t-betrag = 0. 
  t-foreign = 0. 
 
  for each turnover: 
    delete turnover. 
  end. 
  for each pay-list: 
    delete pay-list. 
  end. 
  for each outstand-list: 
    delete outstand-list. 
  end. 
  
  DO i = 1 TO 20:
      tot-betrag[i] = 0.
  END.
  
  tot-cover = 0. 
  tot-other = 0.
  tot-serv = 0. 
  tot-tax = 0. 
  tot-debit = 0. 
  tot-cash1 = 0. 
  tot-cash = 0. 
  tot-trans = 0. 
  tot-ledger = 0.
  tot-vat = 0.
 
  nt-cover = 0. 
  DO i = 1 TO 20:
      nt-betrag[i] = 0.
  END.
  nt-other = 0.
  nt-serv = 0. 
  nt-tax = 0. 
  nt-debit = 0. 
  nt-cash1 = 0. 
  nt-cash = 0. 
  nt-trans = 0. 
  nt-vat = 0.

  for each h-bill where h-bill.flag EQ 0 and h-bill.saldo NE 0 
    and h-bill.departement = curr-dept 
      no-lock use-index dept_ix by h-bill.rechnr: 
    find first kellner where kellner.kellner-nr = h-bill.kellner-nr  
    no-lock no-error. 
    create outstand-list. 
    outstand-list.rechnr = h-bill.rechnr. 
    if available kellner then 
      outstand-list.name = kellner.kellnername. 
    for each h-bill-line where h-bill-line.rechnr = h-bill.rechnr 
      and h-bill-line.departement = curr-dept no-lock: 
      outstand-list.saldo = outstand-list.saldo + h-bill-line.betrag. 
      outstand-list.foreign = outstand-list.foreign  
        + h-bill-line.fremdwbetrag. 
    end. 
  end. 
  /*FT
  for each kellner where kellner.departement = curr-dept no-lock: 
    FIND FIRST h-bill where h-bill.kellner-nr = kellner.kellner-nr 
      and h-bill.flag = 1  and h-bill.departement = curr-dept  
      use-index dept1_ix NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN   */
    for each h-bill where /*h-bill.kellner-nr = kellner.kellner-nr 
      and*/ h-bill.flag = 1  and h-bill.departement = curr-dept  
      no-lock use-index dept1_ix by h-bill.rechnr: 
      IF shift = 0 THEN
        FIND FIRST h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        AND h-bill-line.bill-datum GE from-date
        AND h-bill-line.bill-datum LE to-date
        AND h-bill-line.departement = curr-dept USE-INDEX rechnr_index /*bildat_index*/ NO-LOCK NO-ERROR. 
      ELSE
        FIND first h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        AND h-bill-line.bill-datum GE from-date
        AND h-bill-line.bill-datum LE to-date
        AND h-bill-line.departement = curr-dept
        AND h-bill-line.betriebsnr = shift USE-INDEX rechnr_index /*bildat_index*/ NO-LOCK NO-ERROR. 
      do while available h-bill-line:           
        find first turnover where turnover.departement = curr-dept 
        /* and turnover.kellner-nr = integer(curr-dept) */ 
          and turnover.rechnr = string(h-bill.rechnr) no-error. 
        if not available turnover then 
        do:
          pos = 0.
          bill-no = 0.
          guestname = "".
          IF shift = 0 THEN
            FIND FIRST h-bline WHERE h-bline.rechnr = h-bill.rechnr 
            AND h-bline.bill-datum GE from-date 
            AND h-bline.bill-datum LE to-date
            AND h-bline.departement = curr-dept 
            AND h-bline.artnr = 0 NO-LOCK NO-ERROR. 
          ELSE
            FIND first h-bline WHERE h-bline.rechnr = h-bill.rechnr 
            AND h-bline.bill-datum GE from-date 
            AND h-bline.bill-datum LE to-date
            AND h-bline.departement = curr-dept
            AND h-bline.betriebsnr = shift 
            AND h-bline.artnr = 0 NO-LOCK NO-ERROR. 
          
          IF AVAILABLE h-bline THEN
          DO: 
              pos = INDEX( h-bline.bezeich, "*").
              IF pos NE 0 THEN
                  bill-no = INTEGER(SUBSTR(h-bline.bezeich, pos,
                                           (LENGTH(h-bline.bezeich) - pos + 1))).
              IF bill-no NE 0 THEN
              DO:
                  FIND FIRST bill WHERE bill.rechnr = bill-no NO-LOCK NO-ERROR.
                  IF AVAILABLE bill THEN
                  DO:
                      FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND 
                          res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                      IF AVAILABLE res-line THEN
                          guestname = res-line.NAME.
                  END.
              END.
          END.
          IF guestname = "" THEN guestname = h-bill.bilname.
          create turnover. 
          turnover.departement = curr-dept. 
/*        turnover.kellner-nr = integer(curr-dept). */ 
          turnover.tischnr = h-bill.tischnr. 
          turnover.belegung = h-bill.belegung. 
          turnover.rechnr = string(h-bill.rechnr). 
          turnover.gname = guestname.
          tot-cover = tot-cover + h-bill.belegung. 
        end. 
        if h-bill-line.artnr NE 0 then 
          find first h-artikel where h-artikel.artnr = h-bill-line.artnr 
            and h-artikel.departement = curr-dept no-lock no-error.         
        if h-bill-line.artnr = 0 then    /* room or bill transfer */ 
        do: 
          find first pay-list where pay-list.flag = 2 no-error. 
          if not available pay-list then 
          do: 
            create pay-list. 
            pay-list.flag = 2. 
            pay-list.bezeich = "Room / Bill Transfer". 
          end. 
/*      pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag.  
*/ 
          pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
          
          t-betrag = t-betrag - h-bill-line.betrag. 
/*      t-foreign = t-foreign - h-bill-line.fremwbetrag. */ 
 
          turnover.r-transfer = turnover.r-transfer - h-bill-line.betrag. 
          turnover.compli = NO.
          i = 0. 
          found = no. 
          do while not found: 
            i = i + 1. 
            if substr(h-bill-line.bezeich, i, 1) = "*" then found = yes. 
          end. 
 
          billnr = integer(substr(h-bill-line.bezeich, i + 1,  
                  length(h-bill-line.bezeich) - i)).     
 
          find first bill where bill.rechnr = billnr no-error. 
 
          if available bill then turnover.info = bill.zinr. 
          turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
          tot-trans = tot-trans - h-bill-line.betrag. 
        end. 
        else 
        if h-artikel.artart = 11 or h-artikel.artart = 12 then 
      /* complimentary or meal coupon */ 
        do: 
          if h-artikel.artart = 11 then 
          do: 
            find first pay-list where pay-list.flag = 6 no-error. 
            if not available pay-list then 
            do: 
              create pay-list. 
              pay-list.flag = 6. 
              pay-list.compli = yes. 
              pay-list.bezeich = "Compliment". 
            end. 
/*          pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. */ 
            pay-list.saldo = pay-list.saldo - h-bill-line.betrag - turnover.t-service - turnover.t-tax. 
            if h-bill-line.betrag LT 0 then 
              pay-list.person = pay-list.person + h-bill.belegung. 
            else if h-bill-line.betrag GT 0 then 
            DO:
              IF h-bill.belegung > 0 then
                  pay-list.person = pay-list.person - h-bill.belegung. 
              ELSE pay-list.person = pay-list.person + h-bill.belegung. 
            END.
            t-betrag = t-betrag - h-bill-line.betrag. 
/*        t-foreign = t-foreign - h-bill-line.fremwbetrag. */ 
 
            anz-comp = anz-comp + 1. 
            val-comp = val-comp - h-bill-line.betrag. 
            turnover.st-comp = 1. 
          end. 
          else if h-artikel.artart = 12 then 
          do: 
            find first pay-list where pay-list.flag = 7  
              and pay-list.bezeich = h-artikel.bezeich no-error. 
            if not available pay-list then 
            do: 
              create pay-list. 
              pay-list.compli = yes. 
              pay-list.flag = 7. 
              pay-list.bezeich = h-artikel.bezeich. 
            end. 
/*        pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. */ 
            pay-list.saldo = pay-list.saldo - h-bill-line.betrag - turnover.t-service - turnover.t-tax. 
            
            if h-bill-line.betrag LT 0 then 
              pay-list.person = pay-list.person + h-bill.belegung. 
            else if h-bill-line.betrag GT 0 then 
            DO:
              IF h-bill.belegung > 0 then
                  pay-list.person = pay-list.person - h-bill.belegung. 
              ELSE pay-list.person = pay-list.person + h-bill.belegung. 
            END.
            
            t-betrag = t-betrag - h-bill-line.betrag. 
/*        t-foreign = t-foreign - h-bill-line.fremwbetrag.  */ 
 
            anz-coup = anz-coup + 1. 
            val-coup = val-coup - h-bill-line.betrag. 
            turnover.st-comp = 2.
          end. 

          turnover.compli = NOT turnover.compli.
          turnover.r-transfer = turnover.r-transfer -  h-bill-line.betrag. 
          if h-artikel.artart = 11 then turnover.info = "Comp". 
          else if h-artikel.artart = 12 then turnover.info  
            = /* "Cpon" */ substr(h-artikel.bezeich,1,4). 
          tot-trans = tot-trans - h-bill-line.betrag. 
          
          IF turnover.p-cash1 NE 0 THEN
            turnover.p-cash1 = turnover.p-cash1 - turnover.t-service - turnover.t-tax.

          IF turnover.p-cash NE 0 THEN
            turnover.p-cash = turnover.p-cash - turnover.t-service - turnover.t-tax.

          IF turnover.r-transfer NE 0 THEN
            turnover.r-transfer = turnover.r-transfer - turnover.t-service - turnover.t-tax.

          IF turnover.c-ledger NE 0 THEN
            turnover.c-ledger = turnover.c-ledger - turnover.t-service - turnover.t-tax.
                      
          ASSIGN
            turnover.t-debit = turnover.t-debit - turnover.t-service - turnover.t-tax
            turnover.t-service = 0
            turnover.t-tax = 0.
        end. 
        else 
        do:    /* i.e h-bill-line.artnr NE 0  */ 
          find first h-artikel where h-artikel.artnr = h-bill-line.artnr 
            and h-artikel.departement = curr-dept no-lock no-error. 
          if h-artikel.artart = 0 then /* s
          ales articles */  
            find first artikel where artikel.departement = curr-dept and 
            artikel.artnr = h-artikel.artnrfront no-lock no-error. 
          else /* city ledger */  
            find first artikel where artikel.departement = 0 and 
              artikel.artnr = h-artikel.artnrfront no-error. 
          if h-artikel.artart = 0  /* turnover articles */ then  
          do: 
            service = 0. 
            vat = 0. 
            vat2 = 0.

            /*RUN calc-servvat.p(artikel.departement, artikel.artnr, h-bill-line.bill-datum, 
                   artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).*/

            RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                                    h-bill-line.bill-datum, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
            IF multi-vat = NO THEN ASSIGN vat = vat + vat2.
          /*
            find first htparam where  
              paramnr = artikel.service-code no-lock no-error. 
            if available htparam then service = 0.01 * htparam.fdecimal. 
            find first htparam where  
              paramnr = artikel.mwst-code no-lock no-error. 
            if available htparam then  
            do: 
              if serv-taxable then 
                vat = 0.01 * htparam.fdecimal * (1 + service). 
              else vat = 0.01 * htparam.fdecimal. 
            end. 
            */            
            
            netto = h-bill-line.betrag / (1 + vat + vat2 + service). 
            turnover.t-service = turnover.t-service + netto * service. 
            turnover.t-tax = turnover.t-tax + netto * vat. 
            turnover.t-vat = turnover.t-vat + netto * vat2.
            turnover.t-debit = turnover.t-debit + h-bill-line.betrag. 
            tot-serv = tot-serv + netto * service.  
            tot-tax = tot-tax + netto * vat.  
            tot-debit = tot-debit + h-bill-line.betrag. 
            tot-vat = tot-vat + netto * vat2.  
         
            /*Debug
            IF turnover.rechnr = "38899" THEN
            DO:
                MESSAGE 
                    "ART NO = " h-artikel.artnr SKIP
                    "DESC = " h-artikel.bezeich SKIP
                    "SERV TAX = " 1 + vat + vat2 + service SKIP
                    "FACT = " fact SKIP
                    "NETTO = " netto SKIP
                    "BETRAG = " h-bill-line.betrag
                    VIEW-AS ALERT-BOX INFO BUTTONS OK.
            END.*/

            /*if h-bill-line.fremdwbetrag NE 0 then 
              exchg-rate = h-bill-line.betrag / h-bill-line.fremdwbetrag.*/ 
 
            if artikel.artnr = artnr-list[1] then 
            do: 
              turnover.betrag[1] = turnover.betrag[1] + netto. 
              tot-betrag[1] = tot-betrag[1] + netto.
            end. 
            else if artikel.artnr = artnr-list[2] then 
            do: 
              turnover.betrag[2] = turnover.betrag[2] + netto. 
              tot-betrag[2] = tot-betrag[2] + netto. 
            end. 
            else if artikel.artnr = artnr-list[3] then  
            do: 
              turnover.betrag[3] = turnover.betrag[3] + netto. 
              tot-betrag[3] = tot-betrag[3] + netto. 
            end. 
            else if artikel.artnr = artnr-list[4] then  
            do: 
              turnover.betrag[4] = turnover.betrag[4] + netto. 
              tot-betrag[4] = tot-betrag[4] + netto. 
            end. 
            else if artikel.artnr = artnr-list[5] then  
            do: 
              turnover.betrag[5] = turnover.betrag[5] + netto. 
              tot-betrag[5] = tot-betrag[5] + netto. 
            end. 
            else if artikel.artnr = artnr-list[6] then 
            do: 
              turnover.betrag[6] = turnover.betrag[6] + netto. 
              tot-betrag[6] = tot-betrag[6] + netto. 
            end. 
            else if artikel.artnr = artnr-list[7] then  
            do: 
              turnover.betrag[7] = turnover.betrag[7] + netto. 
              tot-betrag[7] = tot-betrag[7] + netto. 
            end. 
            else if artikel.artnr = artnr-list[8] then  
            do: 
              turnover.betrag[8] = turnover.betrag[8] + netto. 
              tot-betrag[8] = tot-betrag[8] + netto. 
            end. 
            else if artikel.artnr = artnr-list[9] then  
            do: 
              turnover.betrag[9] = turnover.betrag[9] + netto. 
              tot-betrag[9] = tot-betrag[9] + netto. 
            end. 
            else if artikel.artnr = artnr-list[10] then  
            do: 
              turnover.betrag[10] = turnover.betrag[10] + netto. 
              tot-betrag[10] = tot-betrag[10] + netto. 
            end. 
            /*extent 10 gerald 4A7817*/
            ELSE if artikel.artnr = artnr-list[11] then 
            do: 
              turnover.betrag[11] = turnover.betrag[11] + netto. 
              tot-betrag[11] = tot-betrag[11] + netto.
            end. 
            else if artikel.artnr = artnr-list[12] then 
            do: 
              turnover.betrag[12] = turnover.betrag[12] + netto. 
              tot-betrag[12] = tot-betrag[12] + netto. 
            end. 
            else if artikel.artnr = artnr-list[13] then  
            do: 
              turnover.betrag[13] = turnover.betrag[13] + netto. 
              tot-betrag[13] = tot-betrag[13] + netto. 
            end. 
            else if artikel.artnr = artnr-list[14] then  
            do: 
              turnover.betrag[14] = turnover.betrag[14] + netto. 
              tot-betrag[14] = tot-betrag[14] + netto. 
            end. 
            else if artikel.artnr = artnr-list[15] then  
            do: 
              turnover.betrag[5] = turnover.betrag[15] + netto. 
              tot-betrag[15] = tot-betrag[15] + netto. 
            end. 
            else if artikel.artnr = artnr-list[16] then 
            do: 
              turnover.betrag[16] = turnover.betrag[16] + netto. 
              tot-betrag[16] = tot-betrag[16] + netto. 
            end. 
            else if artikel.artnr = artnr-list[17] then  
            do: 
              turnover.betrag[17] = turnover.betrag[17] + netto. 
              tot-betrag[17] = tot-betrag[17] + netto. 
            end. 
            else if artikel.artnr = artnr-list[18] then  
            do: 
              turnover.betrag[18] = turnover.betrag[18] + netto. 
              tot-betrag[18] = tot-betrag[18] + netto. 
            end. 
            else if artikel.artnr = artnr-list[19] then  
            do: 
              turnover.betrag[19] = turnover.betrag[19] + netto. 
              tot-betrag[19] = tot-betrag[19] + netto. 
            end. 
            else if artikel.artnr = artnr-list[20] then  
            do: 
              turnover.betrag[20] = turnover.betrag[20] + netto. 
              tot-betrag[20] = tot-betrag[20] + netto. 
            end. 
            /*end geral*/
            ELSE
            DO:
                FOR EACH other-art:
                    IF artikel.artnr = other-art.artnr THEN
                        ASSIGN
                        turnover.other = turnover.other + netto
                        tot-other = tot-other + netto.
                END.
            END.            
          end.  
          else if h-artikel.artart = 6  then    /* cash */ 
          do: 
            find first artikel where artikel.artnr = h-artikel.artnrfront 
              and artikel.departement = 0 no-lock. 
 
            find first pay-list where pay-list.flag = 1 
              AND pay-list.bezeich = artikel.bezeich no-error. 
            if not available pay-list then 
            do: 
              create pay-list. 
              pay-list.flag = 1. 
              pay-list.bezeich = artikel.bezeich. 
            end.   
            if artikel.pricetab then 
            do: 
              pay-list.foreign = pay-list.foreign -  h-bill-line.fremdwbetrag. 
              t-foreign = t-foreign - h-bill-line.fremdwbetrag. 
            end. 
            else  
            do: 
              pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
              t-betrag = t-betrag - h-bill-line.betrag. 
            end. 

            FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
              NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN turnover.p-curr = waehrung.wabkurz. 
            
            if artikel.pricetab then  
            do: 
              turnover.p-cash1 = turnover.p-cash1 -  h-bill-line.fremdwbetrag. 
              tot-cash1 = tot-cash1 - h-bill-line.fremdwbetrag. 
            end. 
            ELSE IF h-artikel.artnr = voucher-art THEN  
            DO: 
              turnover.p-cash1 = turnover.p-cash1 - h-bill-line.betrag. 
              t-cash1 = t-cash1 - h-bill-line.betrag. 
              tot-cash1 = tot-cash1 - h-bill-line.betrag. 
            END. 
            else  
            do: 
              turnover.p-cash = turnover.p-cash - h-bill-line.betrag. 
              tot-cash = tot-cash - h-bill-line.betrag. 
            end. 
            turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
          end. 
          else if h-artikel.artart = 7  /* city ledger */ 
          or      h-artikel.artart = 2  /* city ledger */ then 
          do: 
            if h-artikel.artart = 7 then 
            do: 
              find first pay-list where pay-list.flag = 3 no-error. 
              if not available pay-list then 
              do: 
                create pay-list. 
                pay-list.flag = 3. 
                pay-list.bezeich = "Credit Card". 
              end. 
            end. 
            else if h-artikel.artart = 2 then 
            do: 
              find first pay-list where pay-list.flag = 5 no-error. 
              if not available pay-list then 
              do: 
                create pay-list. 
                pay-list.flag = 5. 
                pay-list.bezeich = "City- & Employee Ledger". 
              end. 
            end. 
/*        pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. */ 
            pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 

            pay-list.person = pay-list.person + h-bill.belegung. 

            /*IF h-bill-line.betrag LT 0 THEN /*FT*/
               pay-list.person = pay-list.person + h-bill.belegung. 
            ELSE IF h-bill-line.betrag GT 0 THEN
            DO:
              IF h-bill.belegung > 0 then
                pay-list.person = pay-list.person - h-bill.belegung. 
              ELSE pay-list.person = pay-list.person + h-bill.belegung. 
            END.*/

            t-betrag = t-betrag - h-bill-line.betrag. 
/*        t-foreign = t-foreign - h-bill-line.fremwbetrag.  */ 
 
            turnover.info = string(h-artikel.artnr, ">>>9"). 
            turnover.artnr = artikel.artnr. 
            turnover.c-ledger = turnover.c-ledger - h-bill-line.betrag. 
            turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
            tot-ledger = tot-ledger - h-bill-line.betrag. 
          end.
        end.  
       
       IF shift = 0 THEN
          FIND NEXT h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
          AND h-bill-line.bill-datum GE from-date  
          AND h-bill-line.bill-datum LE to-date  
          AND h-bill-line.departement = curr-dept USE-INDEX rechnr_index /*bildat_index*/  NO-LOCK NO-ERROR. 
        ELSE
          FIND NEXT h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
          AND h-bill-line.bill-datum GE from-date  
          AND h-bill-line.bill-datum LE to-date  
          AND h-bill-line.departement = curr-dept
          AND h-bill-line.betriebsnr = shift USE-INDEX rechnr_index /*bildat_index*/  NO-LOCK NO-ERROR. 
          
      end. 
    end. 
    /*
    find first turnover where turnover.departement = curr-dept 
    /* and turnover.kellner-nr = integer(curr-dept) */ 
      and turnover.rechnr = string(h-bill.rechnr) no-error. 
    RUN cal-FBOdisc.
    IF total-Bdisc NE 0 AND total-Odisc NE 0 THEN
    DO:
      DO i = 1 TO 10:
          IF artnr-list[i] = disc-art1 THEN
              turnover.betrag[i] = total-Fdisc.
          ELSE IF artnr-list[i] = disc-art2 THEN
              turnover.betrag[i] = total-Bdisc.
          ELSE IF artnr-list[i] = disc-art3 THEN
              turnover.betrag[i] = total-Odisc.
      END.
    END.
    */
  /*END.*/ 
  /* when compliment assign tax and service = 0*/
  IF zero-vat-compli THEN
  FOR EACH tlist WHERE tlist.comp:
      FIND FIRST pay-list WHERE pay-list.flag = 6 NO-LOCK NO-ERROR.
      IF AVAILABLE pay-list AND tlist.st-comp = 1 THEN
          ASSIGN 
          pay-list.saldo = pay-list.saldo - tlist.t-service - tlist.t-tax
          t-betrag = t-betrag - tlist.t-service - tlist.t-tax.
      IF tlist.r-transfer NE 0 AND tlist.t-debit NE 0 THEN
          ASSIGN
          tlist.r-transfer   = tlist.r-transfer     - tlist.t-service - tlist.t-tax
          tlist.t-debit      = tlist.t-debit        - tlist.t-service - tlist.t-tax
          tot-trans          = tot-trans            - tlist.t-service - tlist.t-tax
          tot-debit          = tot-debit            - tlist.t-service - tlist.t-tax.
    ASSIGN                 
        tot-serv        = tot-serv - tlist.t-service
        tot-tax         = tot-tax - tlist.t-tax
        tot-vat         = tot-vat - tlist.t-vat
        tlist.t-service = 0
        tlist.t-tax     = 0
        .
  END.

  IF show-fbodisc THEN
  DO:
    RUN fo-discArticle.
    FOR EACH tlist:
      RUN cal-FBOdisc(tlist.rechnr).
      IF total-Fdisc NE 0 OR total-Bdisc NE 0 OR total-Odisc NE 0 THEN
      DO:
        DO i = 1 TO 20:
          IF artnr-list[i] NE 0 THEN
          DO:
            IF artnr-list[i] = fo-disc1 THEN
                tlist.betrag[i] = total-Fdisc.
            ELSE IF artnr-list[i] = fo-disc2 THEN
                tlist.betrag[i] = total-Bdisc.
            ELSE IF artnr-list[i] = fo-disc3 THEN
                tlist.betrag[i] = total-Odisc.
          END.
        END.
      END.
    END.
  END.
  
  CREATE turnover.
  ASSIGN
    turnover.rechnr     = "G-TOTAL"
    turnover.flag       = 2
  .
  FOR EACH tlist WHERE tlist.flag = 0:
      turnover.belegung = turnover.belegung + tlist.belegung. 
      DO i = 1 TO 20:
        ASSIGN
          turnover.betrag[i] = turnover.betrag[i] + tlist.betrag[i]
          /*tot-betrag[i]      = tot-betrag[i] + tlist.betrag[i]*/
        . 
      END.
      turnover.other        = turnover.other + tlist.other. 
      turnover.t-service    = turnover.t-service + tlist.t-service. 
      turnover.t-tax        = turnover.t-tax + tlist.t-tax. 
      turnover.t-debit      = turnover.t-debit + tlist.t-debit. 
      turnover.p-cash       = turnover.p-cash + tlist.p-cash.  
      turnover.p-cash1      = turnover.p-cash1 + tlist.p-cash1.  
      turnover.r-transfer   = turnover.r-transfer + tlist.r-transfer. 
      turnover.c-ledger     = turnover.c-ledger + tlist.c-ledger. 
      turnover.t-vat        = turnover.t-vat + tlist.t-vat. 
  END.

  CREATE turnover. 
  turnover.rechnr = "R-TOTAL".
  turnover.flag = 3.

  FOR EACH tlist WHERE tlist.flag = 0 AND NOT tlist.compli:
      turnover.belegung = turnover.belegung + tlist.belegung. 
      turnover.betrag[1] = turnover.betrag[1] + tlist.betrag[1]. 
      turnover.betrag[2] = turnover.betrag[2] + tlist.betrag[2].
      turnover.betrag[3] = turnover.betrag[3] + tlist.betrag[3]. 
      turnover.betrag[4] = turnover.betrag[4] + tlist.betrag[4].  
      turnover.betrag[5] = turnover.betrag[5] + tlist.betrag[5]. 
      turnover.betrag[6] = turnover.betrag[6] + tlist.betrag[6]. 
      turnover.betrag[7] = turnover.betrag[7] + tlist.betrag[7]. 
      turnover.betrag[8] = turnover.betrag[8] + tlist.betrag[8]. 
      turnover.betrag[9] = turnover.betrag[9] + tlist.betrag[9]. 
      turnover.betrag[10] = turnover.betrag[10] + tlist.betrag[10]. 
      /*extent 10 gerald 4A7817*/
      turnover.betrag[11] = turnover.betrag[11] + tlist.betrag[11]. 
      turnover.betrag[12] = turnover.betrag[12] + tlist.betrag[12].
      turnover.betrag[13] = turnover.betrag[13] + tlist.betrag[13]. 
      turnover.betrag[14] = turnover.betrag[14] + tlist.betrag[14].  
      turnover.betrag[15] = turnover.betrag[15] + tlist.betrag[15]. 
      turnover.betrag[16] = turnover.betrag[16] + tlist.betrag[16]. 
      turnover.betrag[17] = turnover.betrag[17] + tlist.betrag[17]. 
      turnover.betrag[18] = turnover.betrag[18] + tlist.betrag[18]. 
      turnover.betrag[19] = turnover.betrag[19] + tlist.betrag[19]. 
      turnover.betrag[20] = turnover.betrag[20] + tlist.betrag[20]. 
      /*end geral*/
      turnover.other     = turnover.other + tlist.other. 
      turnover.t-service = turnover.t-service + tlist.t-service. 
      turnover.t-tax = turnover.t-tax + tlist.t-tax. 
      turnover.t-debit = turnover.t-debit + tlist.t-debit. 
      turnover.p-cash = turnover.p-cash + tlist.p-cash.  
      turnover.p-cash1 = turnover.p-cash1 + tlist.p-cash1.  
      turnover.r-transfer = turnover.r-transfer + tlist.r-transfer. 
      turnover.c-ledger = turnover.c-ledger + tlist.c-ledger.
      turnover.t-vat = turnover.t-vat + tlist.t-vat. 
  END.
  nt-cover = turnover.belegung.
  nt-betrag[1] = turnover.betrag[1].
  nt-betrag[2] = turnover.betrag[2].
  nt-betrag[3] = turnover.betrag[3].
  nt-betrag[4] = turnover.betrag[4].
  nt-betrag[5] = turnover.betrag[5].
  nt-betrag[6] = turnover.betrag[6].
  nt-betrag[7] = turnover.betrag[7].
  nt-betrag[8] = turnover.betrag[8].
  nt-betrag[9] = turnover.betrag[9].
  /*extent 10 gerald 4A7817*/
  nt-betrag[10] = turnover.betrag[10].
  nt-betrag[11] = turnover.betrag[11].
  nt-betrag[12] = turnover.betrag[12].
  nt-betrag[13] = turnover.betrag[13].
  nt-betrag[14] = turnover.betrag[14].
  nt-betrag[15] = turnover.betrag[15].
  nt-betrag[16] = turnover.betrag[16].
  nt-betrag[17] = turnover.betrag[17].
  nt-betrag[18] = turnover.betrag[18].
  nt-betrag[19] = turnover.betrag[19].
  nt-betrag[20] = turnover.betrag[20].
  /*end geral*/
  nt-serv = turnover.t-service.
  nt-tax = turnover.t-tax.
  nt-debit = turnover.t-debit.
  nt-cash = turnover.p-cash.
  nt-cash1 = turnover.p-cash1.
  nt-trans = turnover.r-transfer.
  nt-ledger = turnover.c-ledger.
  nt-vat = turnover.t-vat.
  
end.  

procedure daysale-list: 
define variable curr-s      as integer. 
define variable billnr      as integer. 
define variable dept        as integer format ">>9" initial 1. 
define variable d-name      as character format "x(24)". 
define variable usr-nr      as integer. 
define variable d-found     as logical initial "no". 
define variable c-found     as logical initial "no". 
define variable vat         as decimal.
define variable vat2        as decimal.
define variable service     AS decimal.
DEFINE VARIABLE fact        AS DECIMAL. 
define variable netto       as decimal. 
define variable i           as integer. 
define variable found       as logical initial no. 
define variable compli      as logical.  
DEFINE VARIABLE guestname   AS CHAR. 
DEFINE VARIABLE bill-no     AS INTEGER.
DEFINE VARIABLE pos         AS INTEGER.

DEF BUFFER kellner1 FOR kellner. 
DEF BUFFER tlist    FOR turnover.
DEF BUFFER h-bline  FOR h-bill-line.

  for each turnover: 
    delete turnover. 
  end. 
  for each pay-list: 
    delete pay-list. 
  end. 
  for each outstand-list: 
    delete outstand-list. 
  end. 
 
  t-betrag = 0. 
  t-foreign = 0. 
 
  DO i = 1 TO 20:
      tot-betrag[i] = 0.
  END.
  
  tot-cover = 0. 
  tot-serv = 0. 
  tot-tax = 0. 
  tot-debit = 0. 
  tot-cash1 = 0. 
  tot-cash = 0. 
  tot-trans = 0. 
  tot-ledger = 0.
  tot-vat = 0.
 
  DO i = 1 TO 20:
      nt-betrag[i] = 0.
  END.
  nt-cover = 0. 
  nt-serv = 0. 
  nt-tax = 0. 
  nt-debit = 0. 
  nt-cash1 = 0. 
  nt-cash = 0. 
  nt-trans = 0. 
  nt-ledger = 0. 
  nt-vat = 0.
    
    
  for each bline-list where bline-list.selected = YES , 
    first kellner where recid(kellner) = bline-list.bl-recid 
    and kellner.departement = curr-dept 
    by kellner.departement by kellner.kellnername: 
 
    for each h-bill where h-bill.flag EQ 0 and h-bill.saldo NE 0 
      and h-bill.departement = bline-list.dept  
  /*  and h-bill.kellner-nr = kellner.kellner-nr */  
      no-lock use-index dept1_ix by h-bill.rechnr: 
      create outstand-list. 
      find first kellner1 where kellner1.kellner-nr = h-bill.kellner-nr 
        and kellner1.departement = h-bill.departement no-lock no-error. 
      outstand-list.rechnr = h-bill.rechnr. 
      if available kellner1 then  
        outstand-list.name = kellner1.kellnername. 
      else outstand-list.name = string(h-bill.kellner-nr). 
      for each h-bill-line where h-bill-line.rechnr = h-bill.rechnr 
        and h-bill-line.departement = curr-dept no-lock: 
        outstand-list.saldo = outstand-list.saldo + h-bill-line.betrag. 
        outstand-list.foreign = outstand-list.foreign  
          + h-bill-line.fremdwbetrag. 
      end. 
    end. 
 
    for each h-bill where h-bill.flag EQ 1 
      and h-bill.departement = bline-list.dept  
      and h-bill.kellner-nr = kellner.kellner-nr  
      no-lock use-index dept1_ix by h-bill.rechnr:         
      IF shift = 0 THEN
        FIND FIRST h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        AND h-bill-line.bill-datum GE from-date  
        AND h-bill-line.bill-datum LE to-date  
        AND h-bill-line.departement = curr-dept NO-LOCK NO-ERROR. 
      ELSE
        FIND first h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        AND h-bill-line.bill-datum GE from-date  
        AND h-bill-line.bill-datum LE to-date  
        AND h-bill-line.departement = curr-dept
        AND h-bill-line.betriebsnr = shift NO-LOCK NO-ERROR. 
      DO WHILE AVAILABLE h-bill-line:  
        FIND FIRST turnover where turnover.departement = curr-dept AND 
          turnover.kellner-nr = kellner.kellner-nr AND 
          turnover.rechnr = STRING(h-bill.rechnr) NO-ERROR. 
        IF NOT AVAILABLE turnover THEN 
        DO: 
          pos = 0.
          bill-no = 0.
          guestname = "".
          IF shift = 0 THEN
            FIND FIRST h-bline WHERE h-bline.rechnr = h-bill.rechnr 
            AND h-bline.bill-datum GE from-date  
            AND h-bline.bill-datum LE to-date  
            AND h-bline.departement = curr-dept 
            AND h-bline.artnr = 0 NO-LOCK NO-ERROR. 
          ELSE
            FIND first h-bline WHERE h-bline.rechnr = h-bill.rechnr 
            AND h-bline.bill-datum GE from-date  
            AND h-bline.bill-datum LE to-date  
            AND h-bline.departement = curr-dept
            AND h-bline.betriebsnr = shift 
            AND h-bline.artnr = 0 NO-LOCK NO-ERROR. 
          IF AVAILABLE h-bline THEN
          DO: 
              pos = INDEX( h-bline.bezeich, "*").
              IF pos NE 0 THEN
                  bill-no = INTEGER(SUBSTR(h-bline.bezeich, pos,
                                           (LENGTH(h-bline.bezeich) - pos + 1))).
              IF bill-no NE 0 THEN
              DO:
                  FIND FIRST bill WHERE bill.rechnr = bill-no NO-LOCK NO-ERROR.
                  IF AVAILABLE bill THEN
                  DO:
                      FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND 
                          res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                      IF AVAILABLE res-line THEN
                          guestname = res-line.NAME.
                  END.
              END.
          END.
          IF guestname = "" THEN guestname = h-bill.bilname.
          CREATE turnover. 
          turnover.departement = kellner.departement. 
          turnover.kellner-nr = kellner.kellner-nr. 
          turnover.name = kellner.kellnername. 
          turnover.tischnr = h-bill.tischnr. 
          turnover.belegung = h-bill.belegung. 
          turnover.rechnr = string(h-bill.rechnr).
          turnover.gname = guestname.
          tot-cover = tot-cover + h-bill.belegung. 
          t-cover = t-cover + h-bill.belegung. 
        end. 
        if h-bill-line.artnr = 0 then    /* room or bill transfer */ 
        do: 
          turnover.r-transfer = turnover.r-transfer - h-bill-line.betrag. 
          turnover.compli = NO.

          FIND FIRST pay-list where pay-list.flag = 2 no-error. 
          IF NOT AVAILABLE pay-list THEN
          DO: 
            CREATE pay-list. 
            pay-list.flag = 2. 
            pay-list.bezeich = "Room / Bill Transfer". 
          END. 
          pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 

          t-betrag = t-betrag - h-bill-line.betrag. 
 
          i = 0. 
          found = no. 
          do while not found: 
            i = i + 1. 
            if substr(h-bill-line.bezeich, i, 1) = "*" then found = yes. 
          end. 
 
          billnr = integer(substr(h-bill-line.bezeich, i + 1,  
            length(h-bill-line.bezeich) - i)).     
 
          find first bill where bill.rechnr = billnr no-lock no-error. 
 
          if available bill then turnover.info = bill.zinr. 
          turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
          t-trans = t-trans - h-bill-line.betrag. 
          tot-trans = tot-trans - h-bill-line.betrag. 
        end. 
        else 
        do:    /* i.e h-bill-line.artnr NE 0  */ 
          find first h-artikel where h-artikel.artnr = h-bill-line.artnr 
            and h-artikel.departement = curr-dept no-lock no-error. 
          if h-artikel.artart = 11 or h-artikel.artart = 12 then 
       /* complimentary or meal coupon */ 
          do: 
            if h-artikel.artart = 11 then 
            do: 
              find first pay-list where pay-list.flag = 6 no-error. 
              if not available pay-list then 
              do: 
                create pay-list. 
                pay-list.flag = 6. 
                pay-list.compli = yes. 
                pay-list.bezeich = "Compliment". 
              end. 
              pay-list.saldo = pay-list.saldo - h-bill-line.betrag - turnover.t-service - turnover.t-tax. 
              if h-bill-line.betrag LT 0 then 
                pay-list.person = pay-list.person + h-bill.belegung. 
              else if h-bill-line.betrag GT 0 then 
              DO:
                IF h-bill.belegung > 0 then
                    pay-list.person = pay-list.person - h-bill.belegung. 
                ELSE pay-list.person = pay-list.person + h-bill.belegung. 
              END.
              t-betrag = t-betrag - h-bill-line.betrag. 
/*            t-foreign = t-foreign - h-bill-line.fremwbetrag. */ 
              anz-comp = anz-comp + 1. 
              val-comp = val-comp - h-bill-line.betrag.
              turnover.st-comp = 1.
            end. 
            else if h-artikel.artart = 12 then 
            do: 
              find first pay-list where pay-list.flag = 7  
                and pay-list.bezeich = h-artikel.bezeich no-error. 
              if not available pay-list then 
              do: 
                create pay-list. 
                pay-list.flag = 7. 
                pay-list.compli = yes. 
                pay-list.bezeich = h-artikel.bezeich. 
              end. 
/*            pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. */ 
              pay-list.saldo = pay-list.saldo - h-bill-line.betrag - turnover.t-service - turnover.t-tax. 
              if h-bill-line.betrag LT 0 then 
                pay-list.person = pay-list.person + h-bill.belegung. 
              else if h-bill-line.betrag GT 0 then 
              DO:
                IF h-bill.belegung > 0 then
                    pay-list.person = pay-list.person - h-bill.belegung. 
                ELSE pay-list.person = pay-list.person + h-bill.belegung. 
              END.

              t-betrag = t-betrag - h-bill-line.betrag. 
/*            t-foreign = t-foreign - h-bill-line.fremwbetrag.  */ 
              anz-coup = anz-coup + 1. 
              val-coup = val-coup - h-bill-line.betrag. 
              turnover.st-comp = 2.
            end. 

            turnover.compli = NOT turnover.compli.
            turnover.r-transfer = turnover.r-transfer - h-bill-line.betrag. 
            if h-artikel.artart = 11 then turnover.info = "Comp". 
            else if h-artikel.artart = 12 then turnover.info  
              = /* "Cpon" */ substr(h-artikel.bezeich, 1, 4). 
            tot-trans = tot-trans - h-bill-line.betrag. 
            
            /*FT tax&serv untuk comp&mealcoupon = 0*/
            IF turnover.p-cash1 NE 0 THEN
                turnover.p-cash1 = turnover.p-cash1 - turnover.t-service - turnover.t-tax.

            IF turnover.p-cash NE 0 THEN
                turnover.p-cash = turnover.p-cash - turnover.t-service - turnover.t-tax.

            IF turnover.r-transfer NE 0 THEN
                turnover.r-transfer = turnover.r-transfer - turnover.t-service - turnover.t-tax.
                
            IF turnover.c-ledger NE 0 THEN
                turnover.c-ledger = turnover.c-ledger - turnover.t-service - turnover.t-tax.
          
            ASSIGN
                turnover.t-debit = turnover.t-debit - turnover.t-service - turnover.t-tax
                turnover.t-service = 0
                turnover.t-tax = 0.
            
            /*endFT*/

          end. 
          else if h-artikel.artart = 0 then /* sales articles */  
          do: 
            find first artikel where artikel.departement = curr-dept 
              and artikel.artnr = h-artikel.artnrfront no-lock no-error. 
             IF AVAILABLE artikel THEN
            service = 0. 
            vat = 0. 
            vat2 = 0.

            /*find first htparam where  
              paramnr = artikel.service-code no-lock no-error. 
            if available htparam then service = 0.01 * htparam.fdecimal. 
            find first htparam where  
              paramnr = artikel.mwst-code no-lock no-error. 
            if available htparam then  
            do: 
              if serv-taxable then 
                vat = 0.01 * htparam.fdecimal * (1 + service). 
              else vat = 0.01 * htparam.fdecimal. 
            end. */

            /*RUN calc-servvat.p(artikel.departement, artikel.artnr, h-bill-line.bill-datum, 
                   artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).*/
            RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                                    h-bill-line.bill-datum, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
            IF multi-vat = NO THEN ASSIGN vat = vat + vat2.
            
            
            netto = h-bill-line.betrag / (1 + vat + vat2 + service). 
            turnover.t-service = turnover.t-service + netto * service. 
            turnover.t-tax = turnover.t-tax + netto * vat. 
            turnover.t-vat = turnover.t-vat + netto * vat2.
            turnover.t-debit = turnover.t-debit + h-bill-line.betrag. 
            /*t-serv = t-serv + netto * service.  
            t-tax = t-tax + netto * vat. 
            t-vat = t-vat + netto * vat2. 
            t-debit = t-debit + h-bill-line.betrag. */
            tot-serv = tot-serv + netto * service.  
            tot-tax = tot-tax + netto * vat. 
            tot-vat = tot-vat + netto * vat2. 
            tot-debit = tot-debit + h-bill-line.betrag. 
            
            /*if h-bill-line.fremdwbetrag NE 0 then 
              exchg-rate = h-bill-line.betrag / h-bill-line.fremdwbetrag. */
 
            if artikel.artnr = artnr-list[1] then 
            do: 
                turnover.betrag[1] = turnover.betrag[1] + netto. 
                tt-betrag[1] = tt-betrag[1] + netto. 
                tot-betrag[1] = tot-betrag[1] + netto.
              end. 
              else if artikel.artnr = artnr-list[2] then 
              do: 
                turnover.betrag[2] = turnover.betrag[2] + netto. 
                tt-betrag[2] = tt-betrag[2] + netto. 
                tot-betrag[2] = tot-betrag[2] + netto. 
              end. 
              else if artikel.artnr = artnr-list[3] then  
              do: 
                turnover.betrag[3] = turnover.betrag[3] + netto. 
                tt-betrag[3] = tt-betrag[3] + netto. 
                tot-betrag[3] = tot-betrag[3] + netto. 
              end. 
              else if artikel.artnr = artnr-list[4] then  
              do: 
                turnover.betrag[4] = turnover.betrag[4] + netto. 
                tt-betrag[4] = tt-betrag[4] + netto. 
                tot-betrag[4] = tot-betrag[4] + netto. 
              end. 
              else if artikel.artnr = artnr-list[5] then  
              do: 
                turnover.betrag[5] = turnover.betrag[5] + netto. 
                tt-betrag[5] = tt-betrag[5] + netto. 
                tot-betrag[5] = tot-betrag[5] + netto. 
              end. 
              else if artikel.artnr = artnr-list[6] then 
              do: 
                  turnover.betrag[6] = turnover.betrag[6] + netto. 
                  tt-betrag[6]  = tt-betrag[6] + netto.
                  tot-betrag[6] = tot-betrag[6] + netto. 
              end. 
              else if artikel.artnr = artnr-list[7] then  
              do: 
                  turnover.betrag[7] = turnover.betrag[7] + netto. 
                  tt-betrag[7]  = tt-betrag[7] + netto.
                  tot-betrag[7] = tot-betrag[7] + netto. 
              end. 
              else if artikel.artnr = artnr-list[8] then  
              do: 
                  turnover.betrag[8] = turnover.betrag[8] + netto. 
                  tt-betrag[8]  = tt-betrag[8] + netto.
                  tot-betrag[8] = tot-betrag[8] + netto. 
              end. 
              else if artikel.artnr = artnr-list[9] then  
              do: 
                  turnover.betrag[9] = turnover.betrag[9] + netto. 
                  tt-betrag[9]  = tt-betrag[9] + netto.
                  tot-betrag[9] = tot-betrag[9] + netto. 
              end. 
              else if artikel.artnr = artnr-list[10] then  
              do: 
                  turnover.betrag[10] = turnover.betrag[10] + netto. 
                  tt-betrag[10]  = tt-betrag[10] + netto.
                  tot-betrag[10] = tot-betrag[10] + netto. 
              end. 
              /*extent 10 gerald 4A7817*/
              ELSE if artikel.artnr = artnr-list[11] then 
              do: 
                turnover.betrag[11] = turnover.betrag[11] + netto. 
                tt-betrag[11] = tt-betrag[11] + netto. 
                tot-betrag[11] = tot-betrag[11] + netto.
              end. 
              else if artikel.artnr = artnr-list[12] then 
              do: 
                turnover.betrag[12] = turnover.betrag[12] + netto. 
                tt-betrag[12] = tt-betrag[12] + netto. 
                tot-betrag[12] = tot-betrag[12] + netto. 
              end. 
              else if artikel.artnr = artnr-list[13] then  
              do: 
                turnover.betrag[13] = turnover.betrag[13] + netto. 
                tt-betrag[13] = tt-betrag[13] + netto. 
                tot-betrag[13] = tot-betrag[13] + netto. 
              end. 
              else if artikel.artnr = artnr-list[14] then  
              do: 
                turnover.betrag[14] = turnover.betrag[14] + netto. 
                tt-betrag[14] = tt-betrag[14] + netto. 
                tot-betrag[14] = tot-betrag[14] + netto. 
              end. 
              else if artikel.artnr = artnr-list[15] then  
              do: 
                turnover.betrag[15] = turnover.betrag[15] + netto. 
                tt-betrag[15] = tt-betrag[15] + netto. 
                tot-betrag[15] = tot-betrag[15] + netto. 
              end. 
              else if artikel.artnr = artnr-list[16] then 
              do: 
                  turnover.betrag[16] = turnover.betrag[16] + netto. 
                  tt-betrag[16]  = tt-betrag[16] + netto.
                  tot-betrag[16] = tot-betrag[16] + netto. 
              end. 
              else if artikel.artnr = artnr-list[17] then  
              do: 
                  turnover.betrag[17] = turnover.betrag[17] + netto. 
                  tt-betrag[17]  = tt-betrag[17] + netto.
                  tot-betrag[17] = tot-betrag[17] + netto. 
              end. 
              else if artikel.artnr = artnr-list[18] then  
              do: 
                  turnover.betrag[18] = turnover.betrag[18] + netto. 
                  tt-betrag[18]  = tt-betrag[18] + netto.
                  tot-betrag[18] = tot-betrag[18] + netto. 
              end. 
              else if artikel.artnr = artnr-list[19] then  
              do: 
                  turnover.betrag[19] = turnover.betrag[19] + netto. 
                  tt-betrag[19]  = tt-betrag[19] + netto.
                  tot-betrag[19] = tot-betrag[19] + netto. 
              end. 
              else if artikel.artnr = artnr-list[20] then  
              do: 
                  turnover.betrag[20] = turnover.betrag[20] + netto. 
                  tt-betrag[20]  = tt-betrag[20] + netto.
                  tot-betrag[20] = tot-betrag[20] + netto. 
              end. 
              ELSE
              DO:
                  FOR EACH other-art:
                      IF artikel.artnr = other-art.artnr THEN
                          ASSIGN
                            turnover.other = turnover.other + netto
                            tt-other  = tt-other + netto.
                            tot-other = tot-other + netto.
                  END.
              END.
            end.  
            else /* city ledger or cash */  
              find first artikel where artikel.departement = 0 and 
               artikel.artnr = h-artikel.artnrfront no-error. 
            if h-artikel.artart = 6  then    /* cash */ 
            do: 
              find first artikel where artikel.artnr = h-artikel.artnrfront 
                and artikel.departement = 0 no-lock. 
 
              find first pay-list where pay-list.flag = 1 
                AND pay-list.bezeich = artikel.bezeich no-error. 
              if not available pay-list then 
              do: 
                create pay-list. 
                pay-list.flag = 1. 
                pay-list.bezeich = artikel.bezeich. 
              end.   
              if artikel.pricetab then 
              do: 
                pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. 
                t-foreign = t-foreign - h-bill-line.fremdwbetrag.   
              end. 
              else  
              do: 
                pay-list.saldo = pay-list.saldo - h-bill-line.betrag. 
                t-betrag = t-betrag - h-bill-line.betrag. 
              end. 

              FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
                NO-LOCK NO-ERROR.
              IF AVAILABLE waehrung THEN turnover.p-curr = waehrung.wabkurz. 
 
              if artikel.pricetab then  
              do: 
                turnover.p-cash1 = turnover.p-cash1 - h-bill-line.fremdwbetrag. 
                t-cash1 = t-cash1 - h-bill-line.fremdwbetrag. 
                /*F tot-cash1 = tot-cash1 - h-bill-line.fremdwbetrag. F*/
              end. 
               /*****/
              ELSE IF h-artikel.artnr = voucher-art THEN  
                DO: 
                  turnover.p-cash1 = turnover.p-cash1 - h-bill-line.betrag. 
                  t-cash1 = t-cash1 - h-bill-line.betrag. 
                  tot-cash1 = tot-cash1 - h-bill-line.betrag. 
                END. 
              /*****/
              else 
              do: 
                turnover.p-cash = turnover.p-cash - h-bill-line.betrag. 
                t-cash = t-cash - h-bill-line.betrag. 
                /*F tot-cash = tot-cash - h-bill-line.betrag.  F*/
              end. 
              turnover.t-credit = turnover.t-credit - h-bill-line.betrag.
              turnover.info = " ".
            end. 
            else if h-artikel.artart = 7  /* city ledger */ 
            or      h-artikel.artart = 2  /* city ledger */  then 
            do: 
              if h-artikel.artart = 7 then 
              do: 
                find first pay-list where pay-list.flag = 3 no-error. 
                if not available pay-list then 
                do: 
                  create pay-list. 
                  pay-list.flag = 3. 
                  pay-list.bezeich = "Credit Card". 
                end. 
              end. 
              else if h-artikel.artart = 2 then 
              do: 
                find first pay-list where pay-list.flag = 5 no-error. 
                if not available pay-list then 
                do: 
                  create pay-list. 
                  pay-list.flag = 5. 
                  pay-list.bezeich = "City- & Employee Ledger". 
                end. 
              end. 
/*          pay-list.foreign = pay-list.foreign - h-bill-line.fremdwbetrag. */ 
              pay-list.saldo = pay-list.saldo - h-bill-line.betrag.
              
              /*pay-list.person = pay-list.person - h-bill.belegung. */
              pay-list.person = pay-list.person + h-bill.belegung. 

              t-betrag = t-betrag - h-bill-line.betrag. 
/*          t-foreign = t-foreign - h-bill-line.fremwbetrag.  */ 
 
             turnover.info = string(h-artikel.artnr, ">>>9"). 
             turnover.artnr = artikel.artnr. 
             turnover.c-ledger = turnover.c-ledger - h-bill-line.betrag. 
             turnover.t-credit = turnover.t-credit - h-bill-line.betrag. 
             t-ledger = t-ledger - h-bill-line.betrag. 
             tot-ledger = tot-ledger - h-bill-line.betrag. 
          end. 
        end.  
        IF shift = 0 THEN
          FIND NEXT h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
          AND h-bill-line.bill-datum GE from-date  
          AND h-bill-line.bill-datum LE to-date  
          AND h-bill-line.departement = curr-dept NO-LOCK NO-ERROR. 
        ELSE
          FIND NEXT h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
          AND h-bill-line.bill-datum GE from-date  
          AND h-bill-line.bill-datum LE to-date  
          AND h-bill-line.departement = curr-dept
          AND h-bill-line.betriebsnr = shift NO-LOCK NO-ERROR. 
      end. 
    end. 
    IF zero-vat-compli THEN
    FOR EACH tlist WHERE tlist.comp:
      FIND FIRST pay-list WHERE pay-list.flag = 6 NO-LOCK NO-ERROR.
      IF AVAILABLE pay-list THEN
          ASSIGN 
          pay-list.saldo = pay-list.saldo - tlist.t-service - tlist.t-tax
          t-betrag = t-betrag - tlist.t-service - tlist.t-tax.

      IF tlist.r-transfer NE 0 AND tlist.t-debit NE 0 THEN
          ASSIGN
          tlist.r-transfer   = tlist.r-transfer     - tlist.t-service - tlist.t-tax
          tlist.t-debit      = tlist.t-debit        - tlist.t-service - tlist.t-tax
          tot-trans          = tot-trans            - tlist.t-service - tlist.t-tax
          tot-debit          = tot-debit            - tlist.t-service - tlist.t-tax.
      ASSIGN                 
        tot-serv        = tot-serv - tlist.t-service
        tot-tax         = tot-tax - tlist.t-tax
        tot-vat         = tot-vat - tlist.t-vat
        tlist.t-service = 0
        tlist.t-tax     = 0
        tlist.t-vat     = 0
        .
    END.

    IF show-fbodisc THEN
    DO:
      RUN fo-discArticle.
      FOR EACH tlist:
        RUN cal-FBOdisc(tlist.rechnr).
        IF total-Fdisc NE 0 OR total-Bdisc NE 0 OR total-Odisc NE 0 THEN
        DO:
          DO i = 1 TO 20:
            IF artnr-list[i] NE 0 THEN
            DO:
              IF artnr-list[i] = fo-disc1 THEN
                  tlist.betrag[i] = total-Fdisc.
              ELSE IF artnr-list[i] = fo-disc2 THEN
                  tlist.betrag[i] = total-Bdisc.
              ELSE IF artnr-list[i] = fo-disc3 THEN
                  tlist.betrag[i] = total-Odisc.
            END.
          END.
        END.
      END.
    END.
/*    
    create turnover. 
    turnover.name = kellner.kellnername. 
    turnover.rechnr = "TOTAL". 
    turnover.belegung =  t-cover. 
    turnover.betrag[1] = tt-betrag[1]. 
    turnover.betrag[2] = tt-betrag[2]. 
    turnover.betrag[4] = tt-betrag[3]. 
    turnover.betrag[3] = tt-betrag[3].  
    turnover.betrag[5] = tt-betrag[5]. 
    turnover.betrag[6] = tt-betrag[6]. 
    turnover.betrag[7] = tt-betrag[7]. 
    turnover.betrag[8] = tt-betrag[8]. 
    turnover.betrag[9] = tt-betrag[9].  
    turnover.betrag[10] = tt-betrag[10]. 
    turnover.other     = tt-other.
    turnover.t-service = t-serv. 
    turnover.t-tax = t-tax. 
    turnover.t-debit = t-debit. 
    turnover.p-cash = t-cash.  
    turnover.p-cash1 = t-cash1.  
    turnover.r-transfer = t-trans. 
    turnover.c-ledger = t-ledger.  
    turnover.flag = 1.
*/    
  END. 

  DO i = 1 TO 20:
      ASSIGN tot-betrag[i] = 0.
  END.

  CREATE turnover.
  ASSIGN
    turnover.rechnr     = "G-TOTAL"
    turnover.flag       = 2
  .
  FOR EACH tlist WHERE tlist.flag = 0:
      turnover.belegung = turnover.belegung + tlist.belegung. 
      DO i = 1 TO 20:
        ASSIGN
          turnover.betrag[i] = turnover.betrag[i] + tlist.betrag[i]
          tot-betrag[i]      = tot-betrag[i] + tlist.betrag[i]
        . 
      END.
      turnover.other        = turnover.other + tlist.other. 
      turnover.t-service    = turnover.t-service + tlist.t-service. 
      turnover.t-tax        = turnover.t-tax + tlist.t-tax. 
      turnover.t-debit      = turnover.t-debit + tlist.t-debit. 
      turnover.p-cash       = turnover.p-cash + tlist.p-cash.  
      turnover.p-cash1      = turnover.p-cash1 + tlist.p-cash1.  
      turnover.r-transfer   = turnover.r-transfer + tlist.r-transfer. 
      turnover.c-ledger     = turnover.c-ledger + tlist.c-ledger.  
      turnover.t-vat        = turnover.t-vat + tlist.t-vat.
  END.
  
  CREATE turnover. 
  turnover.rechnr = "R-TOTAL".
  turnover.flag = 3.
  
  FOR EACH tlist WHERE tlist.flag = 0 AND NOT tlist.compli:
      turnover.belegung = turnover.belegung + tlist.belegung. 
      turnover.betrag[1] = turnover.betrag[1] + tlist.betrag[1]. 
      turnover.betrag[2] = turnover.betrag[2] + tlist.betrag[2].
      turnover.betrag[3] = turnover.betrag[3] + tlist.betrag[3]. 
      turnover.betrag[4] = turnover.betrag[4] + tlist.betrag[4].  
      turnover.betrag[5] = turnover.betrag[5] + tlist.betrag[5]. 
      turnover.betrag[6] = turnover.betrag[6] + tlist.betrag[6]. 
      turnover.betrag[7] = turnover.betrag[7] + tlist.betrag[7].
      turnover.betrag[8] = turnover.betrag[8] + tlist.betrag[8]. 
      turnover.betrag[9] = turnover.betrag[9] + tlist.betrag[9].  
      turnover.betrag[10] = turnover.betrag[10] + tlist.betrag[10]. 
      /*extent 10 gerald 4A7817*/
      turnover.betrag[11] = turnover.betrag[11] + tlist.betrag[11]. 
      turnover.betrag[12] = turnover.betrag[12] + tlist.betrag[12].
      turnover.betrag[13] = turnover.betrag[13] + tlist.betrag[13]. 
      turnover.betrag[14] = turnover.betrag[14] + tlist.betrag[14].  
      turnover.betrag[15] = turnover.betrag[15] + tlist.betrag[15]. 
      turnover.betrag[16] = turnover.betrag[16] + tlist.betrag[16]. 
      turnover.betrag[17] = turnover.betrag[17] + tlist.betrag[17].
      turnover.betrag[18] = turnover.betrag[18] + tlist.betrag[18]. 
      turnover.betrag[19] = turnover.betrag[19] + tlist.betrag[19].  
      turnover.betrag[20] = turnover.betrag[20] + tlist.betrag[20]. 
      turnover.other      = turnover.other + tlist.other. 
      turnover.t-service = turnover.t-service + tlist.t-service. 
      turnover.t-tax = turnover.t-tax + tlist.t-tax. 
      turnover.t-debit = turnover.t-debit + tlist.t-debit. 
      turnover.p-cash = turnover.p-cash + tlist.p-cash.  
      turnover.p-cash1 = turnover.p-cash1 + tlist.p-cash1.  
      turnover.r-transfer = turnover.r-transfer + tlist.r-transfer. 
      turnover.c-ledger = turnover.c-ledger + tlist.c-ledger. 
      turnover.t-vat = turnover.t-vat + tlist.t-vat. 
  END.

  nt-cover = turnover.belegung.
  nt-betrag[1] = turnover.betrag[1].
  nt-betrag[2] = turnover.betrag[2].
  nt-betrag[3] = turnover.betrag[3].
  nt-betrag[4] = turnover.betrag[4].
  nt-betrag[5] = turnover.betrag[5].
  nt-betrag[6] = turnover.betrag[6].
  nt-betrag[7] = turnover.betrag[7].
  nt-betrag[8] = turnover.betrag[8].
  nt-betrag[9] = turnover.betrag[9].
  nt-betrag[10] = turnover.betrag[10].
  /*extent 10 gerald 4A7817*/
  nt-betrag[11] = turnover.betrag[11].
  nt-betrag[12] = turnover.betrag[12].
  nt-betrag[13] = turnover.betrag[13].
  nt-betrag[14] = turnover.betrag[14].
  nt-betrag[15] = turnover.betrag[15].
  nt-betrag[16] = turnover.betrag[16].
  nt-betrag[17] = turnover.betrag[17].
  nt-betrag[18] = turnover.betrag[18].
  nt-betrag[19] = turnover.betrag[19].
  nt-betrag[20] = turnover.betrag[20].
  nt-other = turnover.other.
  nt-serv = turnover.t-service.
  nt-tax = turnover.t-tax.
  nt-debit = turnover.t-debit.
  nt-cash = turnover.p-cash.
  nt-cash1 = turnover.p-cash1.
  nt-trans = turnover.r-transfer.
  nt-ledger = turnover.c-ledger.
  nt-vat = turnover.t-vat.
end.  


PROCEDURE fo-discArticle:
    ASSIGN
        fo-disc1 = 0
        fo-disc2 = 0
        fo-disc3 = 0
    .
    FIND FIRST h-artikel WHERE h-artikel.artnr = disc-art1 
        AND h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
          AND artikel.departement = curr-dept NO-LOCK NO-ERROR.
      IF AVAILABLE artikel THEN fo-disc1 = artikel.artnr.
    END.
    FIND FIRST h-artikel WHERE h-artikel.artnr = disc-art2
        AND h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
          AND artikel.departement = curr-dept NO-LOCK NO-ERROR.
      IF AVAILABLE artikel THEN fo-disc2 = artikel.artnr.
    END.
    FIND FIRST h-artikel WHERE h-artikel.artnr = disc-art3 
        AND h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
          AND artikel.departement = curr-dept NO-LOCK NO-ERROR.
      IF AVAILABLE artikel THEN fo-disc3 = artikel.artnr.
    END.
END.


PROCEDURE cal-FBOdisc:
    DEFINE INPUT PARAMETER billno AS INTEGER.
    
    ASSIGN total-Fdisc = 0
        total-Bdisc = 0
        TOTAL-Odisc = 0.
  IF NOT show-fbodisc THEN RETURN.
        
  /*FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
    AND vhp.h-bill-line.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.
  IF NOT AVAILABLE vhp.h-bill-line THEN RETURN.
  ASSIGN billdate = vhp.h-bill-line.bill-datum.*/
  
  FOR EACH vhp.h-journal WHERE vhp.h-journal.bill-datum GE from-date
    AND vhp.h-journal.bill-datum LE to-date
    AND vhp.h-journal.departement = curr-dept
    AND vhp.h-journal.rechnr = billno NO-LOCK,
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-journal.artnr
      AND vhp.h-artikel.departement = vhp.h-journal.departement 
      AND vhp.h-artikel.artart = 0 NO-LOCK:  

    IF vhp.h-artikel.artnr = disc-art1 THEN
        total-Fdisc = total-Fdisc + vhp.h-journal.epreis.
    ELSE IF vhp.h-artikel.artnr = disc-art2 THEN
        total-Bdisc = total-Bdisc + vhp.h-journal.epreis.
    ELSE IF vhp.h-artikel.artnr = disc-art3 THEN  
        total-Odisc = total-Odisc + vhp.h-journal.epreis.
  END.
  
END.

