/* SY 27/08/2014 
VHP: key = 1 Language code, 
2 pricecode, 3 = kitchenprint, 4 = POS billprint, 5 = POS shift, 
6 = NatRegion, 7 = lost+found, 8 = reserved
9 = Bill Instruction, 10 = Order Taker, 11 = Rest Cancel Reason,
12 = Order Request Text, 13 = Relation to Guest, 
14 = Room Rate, 15 = menu layout bgcolor 
16 = Magnet Card, 17 = Infotel Additional Program 
18 Currency in reservation, 19 Users department
20 container in l-artikel setup
21 cure equipment, 22 masseur treatment skill, 23 masseur eqipment skill, 24 = HK Guest Preference
25 = Floor Plan, 26 = Segment Group, 27 = GCF Docu Type, 
28 = Work Order, 29 = main group of l-untergrup,
30 = keycard, 
31 = Table Plan,
32 = cancel reservation reason
33 = table reservation plan
34 = SMS report (for receiver)
35 = SMS (eng)
36 = remote approval
37 = micros - PMS IF /* SY 08 NOV 2015 */
101-104 = payroll, 105 = Officer Cheque, 106 = Recurring G/L Acct
107 = G/C Cash Accounts, 108 = G/L help accounts for consolidation, 111 - 120 reserved for Club SW, 117 = Club Locker,
130-135 = reserved for Engineering, 136 = Group Hotel Name, 137 = Linen Maintenance Setup (HK)
140 = Print Option Setup
141 = Guest Titles
142 = storing restaurant menus future new price
143 = Purpose of Stay
147 = for global allotment
153 = dashboard
154 = guest comment
155 = for GL sub-department setup
157 = auto updata
158 = Club SW, reason of freeze status
159 = Booking Engine Mapping Setup
160 = Guest Preference Setup for web c/i
161 = siteminder booking engine
162 = Queuing room number               SY 12Sept2015 
163 = Online tax: last read date & time SY 11/11/2015
164-166 = used for web check-in
167 = guest's note for web check-in
168 = VHP - IDeaS integration

170 = booking engine rate
171 = booking engine availability
172 = booking engine selling rate
173 = A/P Approval UID data Per-Voucher Number
174 = restriction booking engine
175 = update restriction booking engine
176 = Dump breakfast key data
177 = Cash flow
178 = Emergency Report
179 = Room Maid
180-185 = MIS Consolidate
186 = Group Selection for G/L
187 = Diskon Artikel Restaurant*
*/


DEF TEMP-TABLE t-queasy    LIKE queasy.
DEF TEMP-TABLE t-queasy1   LIKE queasy.

DEF INPUT  PARAMETER case-type    AS INTEGER            NO-UNDO.
DEF INPUT  PARAMETER TABLE        FOR t-queasy.
DEF INPUT  PARAMETER TABLE        FOR t-queasy1.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.

DEFINE BUFFER qbuff FOR queasy.
DEFINE VARIABLE curr-count AS INTEGER NO-UNDO.

FIND FIRST t-queasy NO-ERROR.
CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY 
      AND queasy.number1 = t-queasy.number1 EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      BUFFER-COPY t-queasy TO queasy.
      FIND CURRENT queasy NO-LOCK.
      success-flag = YES.
    END.
  END.
  WHEN 2 THEN 
  DO:    
    FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY 
      AND queasy.number1 = t-queasy.number1 EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN CREATE queasy.
    DO:
      BUFFER-COPY t-queasy TO queasy.
      FIND CURRENT queasy NO-LOCK.
      success-flag = YES.
    END.
  END.
  WHEN 3 THEN 
  DO:
      FOR EACH t-queasy :
          CREATE queasy.
          BUFFER-COPY t-queasy TO queasy.
          FIND CURRENT queasy NO-LOCK.
          RELEASE queasy.
      END.
      success-flag = YES.
  END. 
  WHEN 4 THEN
  DO:
      RELEASE t-queasy.

      FOR EACH t-queasy NO-LOCK :
          FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY
              AND queasy.number1 = t-queasy.number1 EXCLUSIVE-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              BUFFER-COPY t-queasy TO queasy.
              FIND CURRENT queasy NO-LOCK.
              success-flag = YES.
          END.
      END.
  END.
    WHEN 5 THEN
    DO:
        FIND FIRST t-queasy1 NO-LOCK.
        FIND FIRST queasy WHERE queasy.KEY = t-queasy1.KEY
            AND queasy.number1    = t-queasy1.number1
            AND queasy.char1      = t-queasy1.char1 
            AND queasy.betriebsnr  = t-queasy.betriebsnr
            AND queasy.deci1      = t-queasy1.deci1
            AND queasy.date1      = t-queasy.date1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            BUFFER-COPY t-queasy TO queasy.
            FIND CURRENT queasy NO-LOCK.
            success-flag = YES.
        END.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST t-queasy1 NO-LOCK.
        FIND FIRST queasy WHERE queasy.KEY = t-queasy1.KEY
            AND queasy.char1      = t-queasy1.char1 
            AND queasy.betriebsnr  = t-queasy.betriebsnr
            AND queasy.deci1      = t-queasy1.deci1
            AND queasy.date1      = t-queasy.date1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            BUFFER-COPY t-queasy TO queasy.
            FIND CURRENT queasy NO-LOCK.
            success-flag = YES.
        END.
    END.
    WHEN 7 THEN 
    DO:    
        FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY 
          AND queasy.number3 = t-queasy.number3 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
          BUFFER-COPY t-queasy TO queasy.
          FIND CURRENT queasy NO-LOCK.
          success-flag = YES.
        END.
    END.
    WHEN 11 THEN  /* special for hk-preference !!!! */ 
    DO:    
      FIND FIRST queasy WHERE RECID(queasy) = t-queasy.number3
        EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
        BUFFER-COPY t-queasy EXCEPT number3 TO queasy.
        FIND CURRENT queasy NO-LOCK.
        success-flag = YES.
      END.
    END.
    WHEN 12 THEN 
    DO:    
      FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY 
        AND queasy.number1 = t-queasy.number1 EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
        DELETE queasy.
        RELEASE queasy.
        success-flag = YES.
      END.
    END.
    WHEN 13 THEN
    DO:
        /* auto update */
        FIND FIRST queasy WHERE queasy.KEY = 157
            AND queasy.date1 = TODAY NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.number1 GE 1 THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN queasy.number1 = queasy.number1 - 1.
            FIND CURRENT queasy NO-LOCK.
        END.
        success-flag = YES.
    END.
    WHEN 14 THEN 
    DO:
        curr-count = t-queasy.number1.
        FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY 
          AND queasy.number1 LE t-queasy.number1 
          AND queasy.betriebsnr = 1 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE queasy:
            FIND FIRST qbuff WHERE RECID(qbuff) = RECID(queasy)
                EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qbuff THEN DO:
                DELETE qbuff.
                RELEASE qbuff.
                success-flag = YES.
            END.
            FIND NEXT queasy WHERE queasy.KEY = t-queasy.KEY 
              AND queasy.number1 LE t-queasy.number1 
              AND queasy.betriebsnr = 1  NO-LOCK NO-ERROR.
        END.
    END.
    WHEN 15 THEN 
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 37
          AND queasy.betriebsnr = 2 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE queasy:
            FIND FIRST qbuff WHERE RECID(qbuff) = RECID(queasy)
                EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qbuff THEN DO:
                DELETE qbuff.
                RELEASE qbuff.
                success-flag = YES.
            END.
            FIND NEXT queasy WHERE queasy.KEY = 37
              AND queasy.betriebsnr = 2 NO-LOCK NO-ERROR.
        END.
    END.
/* SY JUL 16/2017 setup floor plan and room plan REMOVE */
    WHEN 16 THEN   
    FOR EACH t-queasy:
        FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY
            AND queasy.number1 = t-queasy.number1 
            AND queasy.number2 = t-queasy.number2
            AND queasy.char1   = t-queasy.char1
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
            success-flag = YES.
        END.
    END.
/* SY JUL 16/2017 setup floor plan and room plan MOVE */
    WHEN 17 THEN   
    FOR EACH t-queasy:
        FIND FIRST queasy WHERE queasy.KEY = t-queasy.KEY
            AND queasy.number1 = t-queasy.number1 
            AND queasy.number2 = t-queasy.number2
            AND queasy.char1   = t-queasy.char1
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            BUFFER-COPY t-queasy TO queasy.
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
            success-flag = YES.
        END.
    END.

END CASE.
