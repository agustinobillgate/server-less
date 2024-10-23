
DEF TEMP-TABLE bk-list 
  FIELD setup-id LIKE bk-setup.setup-id COLUMN-LABEL "Number " 
  FIELD bezeich  LIKE bk-setup.bezeich  COLUMN-LABEL "Description" FORMAT "x(26)" 
  FIELD pax      AS INTEGER             COLUMN-LABEL "MaxPax" FORMAT ">,>>9". 

DEF INPUT  PARAMETER room AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR bk-list.

FOR EACH bk-setup NO-LOCK BY bk-setup.setup-id: 
    CREATE bk-list. 
    ASSIGN 
      bk-list.setup-id = bk-setup.setup-id 
      bk-list.bezeich = bk-setup.bezeich. 
      IF room NE "" THEN 
      DO: 
        FIND FIRST bk-rset WHERE bk-rset.raum = room 
          AND bk-rset.setup-id = bk-setup.setup-id NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-rset THEN bk-list.pax = bk-rset.personen. 
      END. 
END. 

