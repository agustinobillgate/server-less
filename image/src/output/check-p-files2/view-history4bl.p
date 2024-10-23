DEF TEMP-TABLE debit-list
  FIELD artnr           AS INTEGER FORMAT ">>>9"                COLUMN-LABEL "ArtNo" 
  FIELD gname           AS CHAR FORMAT "x(28)"                  COLUMN-LABEL "Guest Name" 
  FIELD saldo           AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL "Amount" 
  FIELD vesrdep         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL "Foreign Amt" 
  FIELD betrieb-gastmem AS INTEGER FORMAT ">>>9"                COLUMN-LABEL "Curr" 
  FIELD zahlkonto       AS INTEGER FORMAT ">>>9"                COLUMN-LABEL "PayArt" 
  FIELD rgdatum         AS DATE                                 COLUMN-LABEL "BillDate" 
  FIELD transzeit       AS INTEGER
  FIELD userinit        AS CHAR FORMAT "x(4)"                   COLUMN-LABEL "ID" 
  FIELD vesrcod         AS CHAR FORMAT "x(16)"                  COLUMN-LABEL "Remark" 
  FIELD receiver        AS CHAR FORMAT "x(24)"                  COLUMN-LABEL "Receiver" 
.

DEF INPUT  PARAMETER artNo   AS INTEGER           NO-UNDO.
DEF INPUT  PARAMETER rechNo  AS INTEGER           NO-UNDO.
DEF OUTPUT PARAMETER balance AS DECIMAL INITIAL 0 NO-UNDO.
DEF OUTPUT PARAMETER TABLE   FOR debit-list.

DEF BUFFER gast FOR guest.
DEF BUFFER usr  FOR bediener.
 
FOR EACH debitor WHERE debitor.artnr = artNo 
  AND debitor.rechnr = rechNo NO-LOCK, 
  FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK, 
  FIRST usr WHERE usr.nr = debitor.bediener-nr NO-LOCK 
  BY debitor.zahlkonto BY debitor.rgdatum:
  balance = balance + debitor.saldo.
  CREATE debit-list.
  BUFFER-COPY debitor TO debit-list.
  ASSIGN
    debit-list.gname    = gast.NAME
    debit-list.userinit = usr.userinit
    debit-list.receiver = debitor.NAME.
END.
