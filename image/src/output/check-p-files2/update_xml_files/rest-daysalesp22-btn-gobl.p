define TEMP-TABLE bline-list 
  field selected    as logical initial yes 
  field depart      as char 
  field dept        as integer 
  field knr         as integer 
  field bl-recid    as integer. 

define TEMP-TABLE outstand-list 
  field name        as char format "x(16)" 
  field rechnr      as integer format "->,>>>,>>9"
  field foreign     as decimal format "->,>>>,>>9.99" 
  field saldo       as decimal format "->>>,>>>,>>9.99". 

define TEMP-TABLE pay-list 
  field compli      as logical initial no 
  field person      as integer 
  field flag        as integer /* 1 cash  2 room  3 CC  4 EL  5 CL  6 Comp  */ 
  field bezeich     as char format "x(24)" 
  field artnr       as integer format ">>>>9 " 
  field rechnr      as integer format ">>>>>>9 " 
  field foreign     as decimal format "->,>>>,>>9.99" 
  field saldo       as decimal format "->>>,>>>,>>9.99". 

define TEMP-TABLE turnover 
  field departement     as integer 
  field kellner-nr      as integer
  field name            as CHAR
  field tischnr         as integer
  field rechnr          as char format "x(7)" column-label "Bill-No" 
  field belegung        as integer format "->>9" column-label "Pax" 
  field artnr           as integer 
  field info            as char format "x(4)"        label "Info" 
  FIELD betrag          AS DECIMAL EXTENT 10
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

DEFINE TEMP-TABLE t-tot-betrag
    FIELD tot-betrag1  AS DECIMAL
    FIELD tot-betrag2  AS DECIMAL
    FIELD tot-betrag3  AS DECIMAL
    FIELD tot-betrag4  AS DECIMAL
    FIELD tot-betrag5  AS DECIMAL
    FIELD tot-betrag6  AS DECIMAL
    FIELD tot-betrag7  AS DECIMAL
    FIELD tot-betrag8  AS DECIMAL
    FIELD tot-betrag9  AS DECIMAL
    FIELD tot-betrag10 AS DECIMAL.

DEFINE TEMP-TABLE t-nt-betrag
    FIELD nt-betrag1  AS DECIMAL
    FIELD nt-betrag2  AS DECIMAL
    FIELD nt-betrag3  AS DECIMAL
    FIELD nt-betrag4  AS DECIMAL
    FIELD nt-betrag5  AS DECIMAL
    FIELD nt-betrag6  AS DECIMAL
    FIELD nt-betrag7  AS DECIMAL
    FIELD nt-betrag8  AS DECIMAL
    FIELD nt-betrag   AS DECIMAL
    FIELD nt-betrag10 AS DECIMAL.

DEF INPUT PARAMETER TABLE FOR bline-list.
DEF INPUT PARAMETER disc-art1       AS INT.
DEF INPUT PARAMETER disc-art2       AS INT.
DEF INPUT PARAMETER disc-art3       AS INT.
DEF INPUT PARAMETER curr-dept       AS INT.
DEF INPUT PARAMETER all-user        AS LOGICAL.
DEF INPUT PARAMETER shift           AS INT.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER art-str         AS CHAR.
DEF INPUT PARAMETER voucher-art     AS INT.
DEF INPUT PARAMETER zero-vat-compli AS LOGICAL.
DEF INPUT PARAMETER show-fbodisc    AS LOGICAL.
DEF INPUT PARAMETER exclude-compli  AS LOGICAL.

DEFINE OUTPUT PARAMETER errCode     AS CHAR.

DEF OUTPUT PARAMETER t-betrag   AS DECIMAL.
DEF OUTPUT PARAMETER t-foreign  AS DECIMAL.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.
DEF OUTPUT PARAMETER tot-serv   as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-tax    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-debit  as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-cash   as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-cash1  as decimal format "->>,>>>,>>>,>>9". /*"->>>,>>9.99".*/ 
DEF OUTPUT PARAMETER tot-trans  as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-ledger as decimal format "->>>,>>>,>>9". /*MT*/
DEF OUTPUT PARAMETER tot-cover  as integer format ">>>9".
DEF OUTPUT PARAMETER nt-cover   as integer format ">>>9". 
DEF OUTPUT PARAMETER tot-other  AS DECIMAL FORMAT "->>>,>>>,>>9".
DEF OUTPUT PARAMETER nt-other   AS DECIMAL FORMAT "->>>,>>>,>>9".
DEF OUTPUT PARAMETER nt-serv    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-tax     as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-debit   as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-cash    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-cash1   as decimal format "->>,>>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-trans   as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-ledger  as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER tot-vat    as decimal format "->>>,>>>,>>9". 
DEF OUTPUT PARAMETER nt-vat     as decimal format "->>>,>>>,>>9". 

DEF OUTPUT PARAMETER avail-outstand-list AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR turnover.
DEF OUTPUT PARAMETER TABLE FOR t-tot-betrag.
DEF OUTPUT PARAMETER TABLE FOR t-nt-betrag.
DEF OUTPUT PARAMETER TABLE FOR outstand-list.
DEF OUTPUT PARAMETER TABLE FOR pay-list.


FIND FIRST hoteldpt WHERE hoteldpt.num = curr-dept NO-LOCK NO-ERROR.
IF NOT AVAILABLE hoteldpt THEN
DO:
    errCode = "1 - Wrong department".
    RETURN.
END.

FIND FIRST bline-list NO-LOCK NO-ERROR.
IF AVAILABLE bline-list then  
DO: 
    FOR EACH turnover:
      DELETE turnover.
    END.
    
    RUN rest-daysalesp2-btn-go_webbl.p (INPUT TABLE bline-list, disc-art1, disc-art2,
                 disc-art3, curr-dept, all-user, shift, from-date, to-date, art-str, voucher-art, zero-vat-compli,
                 show-fbodisc,
                 OUTPUT t-betrag, OUTPUT t-foreign, OUTPUT exchg-rate,
                 OUTPUT tot-serv, OUTPUT tot-tax, OUTPUT tot-debit,
                 OUTPUT tot-cash, OUTPUT tot-cash1, OUTPUT tot-trans,
                 OUTPUT tot-ledger, OUTPUT tot-cover, OUTPUT nt-cover,
                 OUTPUT tot-other, OUTPUT nt-other, OUTPUT nt-serv,
                 OUTPUT nt-tax, OUTPUT nt-debit, OUTPUT nt-cash,
                 OUTPUT nt-cash1, OUTPUT nt-trans, OUTPUT nt-ledger,
                 OUTPUT tot-vat, OUTPUT nt-vat, OUTPUT avail-outstand-list,
                 OUTPUT TABLE turnover, OUTPUT TABLE t-tot-betrag,
                 OUTPUT TABLE t-nt-betrag, OUTPUT TABLE outstand-list,
                 OUTPUT TABLE pay-list).

    IF exclude-compli THEN
    FOR EACH turnover WHERE turnover.compli = YES:
        DELETE turnover.
    END.
    errCode = "0 - Retrieve Data Success".
END. 
ELSE  
DO: 
    errCode = "2 - Please select at least a user.".
    RETURN. 
END. 
 
