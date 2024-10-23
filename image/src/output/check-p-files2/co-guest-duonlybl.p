
DEFINE TEMP-TABLE cl-list 
    FIELD flag       AS INTEGER INITIAL 0 
    FIELD reihe      AS INTEGER INITIAL 0
    FIELD zinr       LIKE res-line.zinr 
    FIELD name       AS CHAR FORMAT "x(24)" COLUMN-LABEL "Guest Name" 
    FIELD zipreis    LIKE res-line.zipreis FORMAT ">>>,>>>,>>9.99" 
    FIELD s-zipreis  AS CHAR FORMAT "x(12)" INITIAL "" LABEL "   Room-Rate" 
    FIELD rechnr     LIKE bill.rechnr FORMAT ">>>,>>>,>>>" 
    FIELD ankunft    LIKE res-line.ankunft INITIAL ? 
    FIELD abreise    LIKE res-line.abreise INITIAL ? 
    FIELD cotime     AS CHAR FORMAT "x(5)" COLUMN-LABEL "CO-Time" 
    FIELD deposit    AS DECIMAL FORMAT ">,>>>,>>>,>>9"   COLUMN-LABEL "Deposit" 
    FIELD s-deposit  AS CHAR FORMAT "x(17)" COLUMN-LABEL "Deposit" 
    FIELD cash       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Cash" 
    FIELD s-cash     AS CHAR FORMAT "x(17)" COLUMN-LABEL "Cash" 
    FIELD cc         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL "CreditCard" 
    FIELD s-cc       AS CHAR FORMAT "x(17)" COLUMN-LABEL "CreditCard" 
    FIELD cl         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL "CityLedger" 
    FIELD s-cl       AS CHAR FORMAT "x(17)" COLUMN-LABEL "CityLedger"
    FIELD tot        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Total" 
    FIELD s-tot      AS CHAR FORMAT "x(17)" COLUMN-LABEL "Total" 
    FIELD resnr      AS INTEGER FORMAT ">>>>>>>" INITIAL 0 COLUMN-LABEL "ResNo"
    FIELD company    AS CHAR FORMAT "x(24)" COLUMN-LABEL "Company"
    FIELD bill-balance AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Bill Balance" 
    FIELD reslin-no  AS INTEGER
    .

DEFINE TEMP-TABLE cl-list1 LIKE cl-list.

DEFINE INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR cl-list.

DEF VARIABLE t-deposit AS DECIMAL.
DEF VARIABLE t-cash AS DECIMAL.
DEF VARIABLE t-cc AS DECIMAL.
DEF VARIABLE t-cl AS DECIMAL.
DEF VARIABLE t-tot AS DECIMAL.
DEF VARIABLE t-rm AS INTEGER.

DEF VARIABLE counter AS INT.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "co-guest".

EMPTY TEMP-TABLE cl-list1.

FOR EACH cl-list WHERE cl-list.flag = 1:
    counter = counter + 1.
    CREATE cl-list1.
    BUFFER-COPY cl-list TO cl-list1.
    ASSIGN
        cl-list1.s-deposit = STRING(cl-list.deposit,"->,>>>,>>9.99")
        cl-list1.s-cc = STRING(cl-list.cc,"->,>>>,>>9.99")
        cl-list1.s-cl = STRING(cl-list.cl,"->,>>>,>>9.99") 
        cl-list1.s-cash = STRING(cl-list.cash,"->,>>>,>>9.99") 
        cl-list1.s-tot = STRING(cl-list.tot,"->,>>>,>>9.99") 
        cl-list1.reihe = counter
    .
    ASSIGN
        t-deposit = t-deposit + cl-list.deposit
        t-cash = t-cash + cl-list.cash
        t-cc = t-cc + cl-list.cc
        t-cl = t-cl + cl-list.cl
        t-tot = t-tot + cl-list.tot
        t-rm = t-rm + 1
    .
END.

counter = counter + 1.
CREATE cl-list1. 
ASSIGN 
  cl-list1.reihe        = counter
  cl-list1.NAME         = translateExtended ("Total C/O Room(s)",lvCAREA,"") 
  cl-list1.s-zipreis    = STRING(t-rm,">>>>>>>>>>>9") 
  cl-list1.s-deposit    = STRING(t-deposit,"->,>>>,>>9.99")
  cl-list1.s-cash       = STRING(t-cash,"->,>>>,>>9.99") 
  cl-list1.s-cc         = STRING(t-cc,"->,>>>,>>9.99")
  cl-list1.s-cl         = STRING(t-cl,"->,>>>,>>9.99") 
  cl-list1.s-tot        = STRING(t-tot,"->,>>>,>>9.99").

counter = counter + 1.
CREATE cl-list1. 
cl-list1.reihe     = counter.

counter = counter + 1.
CREATE cl-list1. 
ASSIGN 
    cl-list1.reihe    = counter
    cl-list1.NAME     = translateExtended ("Additional Day Use",lvCAREA,"")
    t-deposit         = 0
    t-cc              = 0
    t-cl              = 0
    t-cash            = 0
    t-tot             = 0
    t-rm              = 0
.

FOR EACH cl-list WHERE cl-list.flag = 0:
    counter = counter + 1.
    CREATE cl-list1.
    BUFFER-COPY cl-list TO cl-list1.
    ASSIGN
        cl-list1.reihe = counter
        cl-list1.s-deposit = STRING(cl-list.deposit,"->,>>>,>>9.99")
        cl-list1.s-cc = STRING(cl-list.cc,"->,>>>,>>9.99")
        cl-list1.s-cl = STRING(cl-list.cl,"->,>>>,>>9.99") 
        cl-list1.s-cash = STRING(cl-list.cash,"->,>>>,>>9.99") 
        cl-list1.s-tot = STRING(cl-list.tot,"->,>>>,>>9.99") 
    .
    ASSIGN
        t-deposit = t-deposit + cl-list.deposit
        t-cash = t-cash + cl-list.cash
        t-cc = t-cc + cl-list.cc
        t-cl = t-cl + cl-list.cl
        t-tot = t-tot + cl-list.tot
        t-rm = t-rm + 1
    .
END.

counter = counter + 1.
CREATE cl-list1. 
ASSIGN 
  cl-list1.reihe     = counter
  cl-list1.NAME      = translateExtended ("Total C/O Room(s)",lvCAREA,"") 
  cl-list1.s-zipreis = STRING(t-rm,">>>>>>>>>>>9") 
  cl-list1.s-deposit   = STRING(t-deposit,"->,>>>,>>9.99")
  cl-list1.s-cash      = STRING(t-cash,"->,>>>,>>9.99") 
  cl-list1.s-cc        = STRING(t-cc,"->,>>>,>>9.99")
  cl-list1.s-cl        = STRING(t-cl,"->,>>>,>>9.99") 
  cl-list1.s-tot       = STRING(t-tot,"->,>>>,>>9.99").
    
counter = counter + 1.
CREATE cl-list1.
cl-list1.reihe = counter.

FIND FIRST cl-list WHERE cl-list.flag = 2 NO-LOCK NO-ERROR.
IF AVAILABLE cl-list THEN
DO:
    counter = counter + 1.
    CREATE cl-list1.
    BUFFER-COPY cl-list TO cl-list1.
    cl-list1.reihe = counter.
END.

EMPTY TEMP-TABLE cl-list.
FOR EACH cl-list1:
    CREATE cl-list.
    BUFFER-COPY cl-list1 TO cl-list.
END.

/*OPEN QUERY q1 FOR EACH cl-list BY cl-list.reihe.*/
