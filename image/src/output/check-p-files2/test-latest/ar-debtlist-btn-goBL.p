DEFINE TEMP-TABLE output-list 
  FIELD ar-recid AS INTEGER 
  FIELD info AS CHAR 
  FIELD wabkurz AS CHAR FORMAT "x(4)" 
  FIELD maildate AS DATE LABEL "MailDate" INITIAL ? 
  FIELD inv-no AS CHAR FORMAT "x(9)"
  FIELD STR AS CHAR
  FIELD ref-no1 AS INTEGER FORMAT ">>>>>>9"     LABEL "Comp-No"
  FIELD ref-no2 AS CHAR    FORMAT "x(32)"       LABEL "Ref-No"
  FIELD ci-date AS DATE    FORMAT "99/99/99"    LABEL "C/I Date"
  FIELD co-date AS DATE    FORMAT "99/99/99"    LABEL "C/O Date"
  FIELD nights  AS INTEGER FORMAT ">>>"         LABEL "Nights"
    . 

DEFINE TEMP-TABLE edit-list
    FIELD rechnr    AS INTEGER FORMAT ">>>>>>>>>9"
    FIELD datum     AS DATE FORMAT "99/99/99"
    FIELD zinr      LIKE zimmer.zinr
    FIELD billname  AS CHAR FORMAT "x(32)"
    FIELD lamt      AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD famt      AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD fcurr     AS CHAR FORMAT "x(4)"
    FIELD ar-recid  AS INTEGER
    FIELD amt-change AS LOGICAL INITIAL NO
    FIELD curr-change AS LOGICAL INITIAL NO
    FIELD curr-nr   AS INTEGER
    .


DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER  from-name   AS CHAR.
DEFINE INPUT PARAMETER  to-name     AS CHAR.
DEFINE INPUT PARAMETER  from-date   AS DATE.
DEFINE INPUT PARAMETER  to-date     AS DATE.
DEFINE INPUT PARAMETER  from-art    AS INTEGER.
DEFINE INPUT PARAMETER  to-art      AS INTEGER.
DEFINE INPUT PARAMETER  tot-flag    AS LOGICAL.
DEFINE INPUT PARAMETER  lesspay     AS LOGICAL.
DEFINE INPUT PARAMETER  show-inv    AS LOGICAL.
DEFINE OUTPUT PARAMETER d-rechnr    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR edit-list.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR NO-UNDO.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "ar-debtlist". 

RUN ar-debtlistbl.p(from-name, to-name, from-date, to-date, from-art, to-art,
                    tot-flag, lesspay, show-inv, OUTPUT d-rechnr, OUTPUT TABLE output-list,
                    OUTPUT TABLE edit-list).

IF show-inv AND d-rechnr NE 0 THEN
DO:
    msg-str = translateExtended("Bill ", lvCAREA, "") + STRING(d-rechnr) + " " +
              translateExtended("no longer exists.", lvCAREA, "").
END.
