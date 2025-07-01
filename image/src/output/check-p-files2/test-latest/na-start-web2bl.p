
DEFINE TEMP-TABLE na-list 
  FIELD reihenfolge AS INTEGER 
  FIELD flag AS INTEGER 
  FIELD anz AS INTEGER 
  FIELD bezeich LIKE nightaudit.bezeichnung. 

DEF TEMP-TABLE t-nightaudit
    FIELD bezeichnung   LIKE nightaudit.bezeichnung
    FIELD hogarest      LIKE nightaudit.hogarest
    FIELD reihenfolge   LIKE nightaudit.reihenfolge
    FIELD programm      LIKE nightaudit.programm
    FIELD abschlussart  LIKE nightaudit.abschlussart.

DEFINE INPUT PARAMETER language-code  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER htparam-recid  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init      AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER ans-arrguest   AS LOGICAL NO-UNDO.

DEFINE OUTPUT PARAMETER printer-nr      AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL INIT NO.

DEFINE VARIABLE mn-stopped      AS LOGICAL INIT NO.
DEFINE VARIABLE stop-it         AS LOGICAL INIT NO.
DEFINE VARIABLE arrival-guest   AS LOGICAL INIT NO.
DEFINE VARIABLE msg-str         AS CHAR.
DEFINE VARIABLE mess-str        AS CHAR.
DEFINE VARIABLE crm-license     AS LOGICAL INIT NO.
DEFINE VARIABLE banquet-license AS LOGICAL INIT NO.
DEFINE VARIABLE na-date1        AS DATE.
DEFINE VARIABLE na-time1        AS INTEGER.
DEFINE VARIABLE na-name1        AS CHAR.
DEFINE VARIABLE mnstart-flag AS LOGICAL NO-UNDO.
DEFINE VARIABLE store-flag   AS LOGICAL INITIAL NO NO-UNDO.
DEFINE VARIABLE billdate     AS DATE. 
DEFINE VARIABLE na-date      AS DATE. 
DEFINE VARIABLE na-time      AS INTEGER. 
DEFINE VARIABLE na-name      AS CHAR FORMAT "x(16)". 
DEFINE VARIABLE lic-nr       AS CHAR NO-UNDO.
DEFINE STREAM s1.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR.
IF AVAILABLE paramtext THEN 
    RUN decode-string(paramtext.ptexte, OUTPUT lic-nr).

FOR EACH queasy WHERE queasy.KEY = 232:
    DELETE queasy.
END.

IF ans-arrguest THEN 
    RUN prepare-mn-startbl.p(2, language-code, OUTPUT mn-stopped, OUTPUT stop-it,  
                         OUTPUT arrival-guest, OUTPUT msg-str, OUTPUT mess-str,  
                         OUTPUT crm-license, OUTPUT banquet-license, OUTPUT TABLE na-list). 
MESSAGE mn-stopped ans-arrguest VIEW-AS ALERT-BOX INFO.
IF mn-stopped THEN.
ELSE DO:
    RUN midnite-prog.   
    RUN mn-chg-sysdatesbl.p. 
    RUN na-startbl.p(2, user-init, htparam-recid, 
                     OUTPUT mnstart-flag, OUTPUT store-flag,
                     OUTPUT printer-nr, OUTPUT TABLE t-nightaudit,
                     OUTPUT na-date1, OUTPUT na-time1, OUTPUT na-name1).
END.

RUN na-prog.
RUN na-startbl.p (3, user-init, htparam-recid, 
                  OUTPUT mnstart-flag, OUTPUT store-flag,
                  OUTPUT printer-nr, OUTPUT TABLE t-nightaudit,
                  OUTPUT na-date, OUTPUT na-time, OUTPUT na-name).

ASSIGN success-flag = YES.
FOR EACH queasy WHERE queasy.KEY = 232
    AND queasy.date1 = TODAY:
    DELETE queasy.
END.


PROCEDURE na-prog:
    DEFINE VARIABLE night-type   AS INTEGER NO-UNDO.
    DEFINE VARIABLE mn-stopped   AS LOGICAL NO-UNDO.
    DEFINE VARIABLE a            AS INTEGER NO-UNDO.
    DEFINE VARIABLE session-parameter AS CHAR.
    DEFINE VARIABLE i            AS INTEGER NO-UNDO.
    DEFINE VARIABLE success-flag AS LOGICAL.
    
    i = 0. 

    FOR EACH t-nightaudit BY (1 - t-nightaudit.hogarest) 
      BY t-nightaudit.reihenfolge:
      i = i + 1.
        
      RUN cqueasy(STRING(t-nightaudit.bezeichnung, "x(40)"), "PROCESS").
      
      IF store-flag THEN 
      DO: 
        IF t-nightaudit.hogarest = 0 THEN night-type = 0. 
        ELSE night-type = 2.
        RUN delete-nitestorbl.p (1, night-type, t-nightaudit.reihenfolge,
                                OUTPUT success-flag).
      END. 

      DO:
          IF t-nightaudit.programm MATCHES ("*bl.p*") THEN
              RUN VALUE(LC(t-nightaudit.programm)).
          ELSE 
          DO:
              IF INT(t-nightaudit.abschlussart) = 1 THEN
              RUN VALUE(LC(t-nightaudit.programm)).
              ELSE 
              DO:
                a = R-INDEX (t-nightaudit.programm, ".p").
                RUN VALUE(SUBSTR(LC(t-nightaudit.programm), 1, a - 1) + "bl.p").
              END.
          END.
      END.
      PAUSE 0.

      IF store-flag THEN 
          RUN delete-nitehistbl.p(1, billdate, t-nightaudit.reihenfolge, OUTPUT success-flag).

      RUN cqueasy(STRING(t-nightaudit.bezeichnung, "x(40)"), "DONE").      
    END.
END.


PROCEDURE midnite-prog:  
    DEFINE VARIABLE i AS INTEGER NO-UNDO.
    DEFINE VARIABLE j AS INTEGER NO-UNDO.
    DEFINE VARIABLE k AS INTEGER NO-UNDO.
  
    /* no-show list   ********/   
      RUN cqueasy("No Show List", "PROCESS").
      RUN mn-noshowbl.p(language-code, OUTPUT i, OUTPUT msg-str). 
      RUN cqueasy("No Show List", "DONE").
        
    /* Extend Departure DATE   ********/   
      RUN cqueasy("Extending Departure Date", "PROCESS").
      RUN mn-extend-departurebl.p(OUTPUT i).  
      RUN cqueasy("Extending Departure Date", "DONE").
      
    /* CRM online questionnair   ********/   
      IF crm-license THEN  
      DO:  
        RUN cqueasy("CRM questionnair - C/O Guests", "PROCESS").
        RUN mn-crm-checkoutbl.p.
        RUN cqueasy("CRM questionnair - C/O Guests", "DONE").        
      END.  
      
    /* Early Checkout   ********/   
      RUN cqueasy("Early Checkout", "PROCESS").
      RUN mn-early-checkoutbl.p(OUTPUT i).  
      RUN cqueasy("Early Checkout", "DONE"). 
      
    /* UPDATE HouseKeeping Status   ********/  
      RUN cqueasy("Updating Room Status", "PROCESS").
      RUN mn-update-zistatusbl.p(language-code, OUTPUT i, OUTPUT msg-str).  
      RUN cqueasy("Updating Room Status", "DONE"). 
      
    /* Correct bill.datum   ********/   
      RUN cqueasy("Correcting bill date", "PROCESS").
      RUN mn-fix-bill-datumbl.p.  
      RUN cqueasy("Correcting bill date", "DONE"). 
      
    /* Delete old bills   ********/  
      RUN cqueasy("Deleting old bills", "PROCESS").
      RUN mn-del-old-billsbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old bills", "DONE"). 
      
    /* Delete old billjournals   ********/ 
      RUN cqueasy("Deleting old bill journals", "PROCESS").
      RUN mn-del-old-billjournalbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old bill journals", "DONE").
      
    /* Delete old Reservation   ********/  
      RUN cqueasy("Deleting old reservations", "PROCESS").
      RUN mn-del-old-resbl.p(OUTPUT i, OUTPUT j, OUTPUT k). 
      RUN cqueasy("Deleting old reservations", "DONE").
      
    /* Delete old Resplan AND zimplan   ********/ 
      RUN cqueasy("Deleting old roomplans", "PROCESS").
      RUN mn-del-old-roomplanbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old roomplans", "DONE").
      
      
    /* Delete old paid debts   ********/  
      RUN cqueasy("Deleting old paid debts", "PROCESS").
      RUN mn-del-old-debtbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old paid debts", "DONE").
      
      
    /* Delete old paid A/P ********/   
      RUN cqueasy("Deleting old paid A/P", "PROCESS").
      RUN mn-del-old-apbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old paid A/P", "DONE").
      
    /* Delete old Rest Bills   ********/   
      RUN cqueasy("Deleting old restaurant bills", "PROCESS").
      RUN mn-del-old-rbillbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old restaurant bills", "DONE").
      
    /* Delete old rest bill journals   ********/   
      RUN cqueasy("Deleting old rest.journals", "PROCESS").
      RUN mn-del-old-rjournalbl.p(OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old rest.journals", "DONE").
      
      
    /* Delete old kitchen bon records  ********/ 
      RUN cqueasy("Deleting old rest.journals", "PROCESS").
      RUN mn-del-old-bonsbl.p.  
      RUN cqueasy("Deleting old rest.journals" , "DONE").
      
      
    /* Delete old kitchen bon records  ********/  
      RUN cqueasy("Deleting old outlet turnovers", "PROCESS").
      RUN mn-del-old-outlet-umsatzbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old outlet turnovers" , "DONE").
      
    /* Delete old calls   ********/   
      RUN cqueasy("Deleting old calls", "PROCESS").
      RUN mn-del-old-callsbl.p(OUTPUT i).  
      RUN cqueasy("Deleting old calls" , "DONE").
      
    /* Delete old l-order & l-orderhdr   ********/ 
      RUN cqueasy("Deleting old purchase orders", "PROCESS").
      RUN mn-del-old-pobl.p(OUTPUT i).  
      RUN cqueasy("Deleting old purchase orders" , "DONE").
      
    /* Delete old stock movings  ********/ 
      RUN cqueasy("Deleted old stock moving journals", "PROCESS").
      RUN mn-del-old-l-opbl.p(OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleted old stock moving journals" , "DONE").
      
    /* Delete old zinrstat  ********/ 
      RUN cqueasy("Deleting old room number statistics", "PROCESS").
      RUN mn-del-old-statbl.p(1, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old room number statistics" , "DONE").
      
    /* Delete old zkstat  ********/   
      RUN cqueasy("Deleting old room catagory statistics", "PROCESS").
      RUN mn-del-old-statbl.p(2, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old room catagory statistics" , "DONE").
      
    /* Delete old sources  ********/ 
      RUN cqueasy("Deleting old room catagory statistics", "PROCESS").
      RUN mn-del-old-statbl.p(3, OUTPUT i, OUTPUT j). 
      RUN cqueasy("Deleting old source statistics" , "DONE").
      
    /* Delete old segmentstat  ********/
      RUN cqueasy("Deleting old segment statistics", "PROCESS").
      RUN mn-del-old-statbl.p(4, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old segment statistics", "DONE").
      
      
    /* Delete old market segment statistic  ********/ 
      RUN cqueasy("Deleting old market segment statistics", "PROCESS").
      RUN mn-del-old-statbl.p(41, OUTPUT i, OUTPUT j). 
      RUN cqueasy("Deleting old market segment statistics", "DONE").
      
    /* Delete old nationstat  ********/   
      RUN cqueasy("Deleting old nation statistics", "PROCESS").
      RUN mn-del-old-statbl.p(5, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old nation statistics", "DONE").
      
    /* Delete old umsatz  ********/ 
      RUN cqueasy("Deleting old turnover statistics", "PROCESS").
      RUN mn-del-old-statbl.p(6, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old turnover statistics", "DONE").
      
    /* Delete old h-umsatz ********/   
      RUN cqueasy("Deleting old restaurant turnover statistics", "PROCESS").
      RUN mn-del-old-statbl.p(7, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old restaurant turnover statistics", "DONE").
      
      
    /* Delete old h-cost ********/   
      RUN cqueasy("Deleting old F&B Costs", "PROCESS").
      RUN mn-del-old-statbl.p(8, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old F&B Costs", "DONE").
      
    /* Delete old exchange rates ********/   
      RUN cqueasy("Deleting old Exchange Rates", "PROCESS").
      RUN mn-del-old-statbl.p(9, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old Exchange Rates", "DONE").
      
    /* Delete NOT used allotments ********/   
      RUN cqueasy("Deleting expired allotments", "PROCESS").
      RUN del-allotment. /*MT gada isi */  
      RUN cqueasy("Deleting expired allotments", "DONE").
      
    /* Delete old DML-list ********/  
      RUN cqueasy("Deleting old DML-Articles", "PROCESS").
      RUN mn-del-old-statbl.p(999, OUTPUT i, OUTPUT j).  
      RUN cqueasy("Deleting old DML-Articles", "DONE").
      
    
    /* Delete old OLD Interface Records ********/   
      RUN cqueasy("Deleting old Interface Records", "PROCESS").
      RUN mn-del-interfacebl.p(1).  
      RUN cqueasy("Deleting old Interface Records", "DONE").
      
    /* Delete old OLD nitehist records ********/  
      RUN cqueasy("Deleting old nithist Records", "PROCESS").
      RUN mn-del-nitehistbl.p.  
      RUN cqueasy("Deleting old nithist Records", "DONE").
      
      
    /* CREATE Banquet history, AND delete old Banquet Reservation   ********/   
      IF banquet-license THEN   
      DO:      
        RUN cqueasy("Deleted old Banquet Reservations", "PROCESS").
        RUN mn-del-old-baresbl.p(OUTPUT i).  
        RUN cqueasy("Deleted old Banquet Reservations", "DONE").        
      END.   
       
      
    /* Move reslin-queasy.char1 OF Reservation Changes TO char3 ********/  
      RUN cqueasy("Updating logfile records", "PROCESS").
      RUN mn-update-logfile-recordsbl.p.  
      RUN cqueasy("Updating logfile records", "DONE").     
      
    /* Delete old h-compliment ********/  
      RUN cqueasy("Deleting old F&B Compliments", "PROCESS").
      RUN mn-del-oldbl.p(1, OUTPUT i).  
      RUN cqueasy("Deleting old F&B Compliments", "DONE").  
      
    /* Delete old work order ********/  
      RUN cqueasy("Deleting old Work Order Records", "PROCESS").
      RUN mn-del-oldbl.p(2, OUTPUT i).  
      RUN cqueasy("Deleting old Work Order Records", "DONE"). 

    /* Delete Quotation Attachment ********/ /*FDL Ticket EA3FF3*/ 
      RUN cqueasy("Deleting old Quotation Attachment Records", "PROCESS").
      RUN mn-del-oldbl.p(4, OUTPUT i).  
      RUN cqueasy("Deleting old Quotation Attachment Records", "DONE"). 
      
    /* Club Software ********/  
      RUN mn-club-softwarebl.p.  
END.   

PROCEDURE del-allotment:   
END. 


PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 

PROCEDURE cqueasy:
    DEFINE INPUT PARAMETER bezeich     AS CHAR NO-UNDO.
    DEFINE INPUT PARAMETER str-process AS CHAR NO-UNDO.

    FIND FIRST queasy WHERE queasy.KEY = 232
        AND queasy.char2 = bezeich 
        AND queasy.date1 = TODAY NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY     = 232
            queasy.char1   = "LOG NIGHT AUDIT"
            queasy.char2   = bezeich
            queasy.char3   = str-process
            queasy.date1   = TODAY
            queasy.number1 = TIME
         .
    END.
    ELSE DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN queasy.char3 = str-process.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
END.
