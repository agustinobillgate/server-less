DEFINE TEMP-TABLE t-bkqueasy
    FIELD key           AS INTEGER      FORMAT ">>>>>>>>9"                  LABEL "Key"                 COLUMN-LABEL "Key"
    FIELD number1       AS INTEGER      FORMAT "->,>>>,>>9"                 LABEL "Number"              COLUMN-LABEL "Number"
    FIELD number2       AS INTEGER      FORMAT "->,>>>,>>9"                 LABEL "Number 2"            COLUMN-LABEL "Number 2"
    FIELD number3       AS INTEGER      FORMAT "->,>>>,>>9"                 LABEL "Number3"             COLUMN-LABEL "Number3"
    FIELD date1         AS DATE         FORMAT "99/99/9999"                 LABEL "Date1"               COLUMN-LABEL "Date1"
    FIELD date2         AS DATE         FORMAT "99/99/9999"                 LABEL "Date2"               COLUMN-LABEL "Date2"
    FIELD date3         AS DATE         FORMAT "99/99/9999"                 LABEL "Date3"               COLUMN-LABEL "Date3"    
    FIELD char1         AS CHARACTER    FORMAT "x(256)"                     LABEL "Char1"               COLUMN-LABEL "Char1"
    FIELD char2         AS CHARACTER    FORMAT "x(256)"                     LABEL "Char2"               COLUMN-LABEL "Char2"
    FIELD char3         AS CHARACTER    FORMAT "x(256)"                     LABEL "Char3"               COLUMN-LABEL "Char3"
    FIELD deci1         AS DECIMAL      FORMAT "->>>,>>>,>>>,>>>,>>9.99"    LABEL "Decimal1"            COLUMN-LABEL "Decimal1"
    FIELD deci2         AS DECIMAL      FORMAT "->>>,>>>,>>>,>>>,>>9.99"    LABEL "Decimal2"            COLUMN-LABEL "Decimal2"
    FIELD deci3         AS DECIMAL      FORMAT "->>>,>>>,>>>,>>>,>>9.99"    LABEL "Decimal3"            COLUMN-LABEL "Decimal3"
    FIELD logi1         AS LOGICAL      FORMAT "yes/no"                     LABEL "Logical1"            COLUMN-LABEL "Logical1"
    FIELD logi2         AS LOGICAL      FORMAT "yes/no"                     LABEL "Logical2"            COLUMN-LABEL "Logical2"    
    FIELD logi3         AS LOGICAL      FORMAT "yes/no"                     LABEL "Logical3"            COLUMN-LABEL "Logical3"    
    FIELD betriebsnr    AS INTEGER      FORMAT ">>>>9"                      LABEL "Betriebs-Nummer"     COLUMN-LABEL "Betr.Nr.".

DEFINE INPUT PARAMETER package-nr       AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-bkqueasy.

FOR EACH bk-queasy WHERE bk-queasy.key EQ 11
    AND bk-queasy.number2 EQ package-nr:
    CREATE t-bkqueasy.
    ASSIGN 
        t-bkqueasy.key      = bk-queasy.key
        t-bkqueasy.number1  = bk-queasy.number1
        t-bkqueasy.number2  = bk-queasy.number2
        t-bkqueasy.number3  = bk-queasy.number3
        t-bkqueasy.char1    = bk-queasy.char1
        t-bkqueasy.char2    = bk-queasy.char2
        t-bkqueasy.char3    = bk-queasy.char3
        t-bkqueasy.deci1    = bk-queasy.deci1
        t-bkqueasy.deci2    = bk-queasy.deci2
        t-bkqueasy.deci3    = bk-queasy.deci3.
END.
