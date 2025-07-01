DEFINE TEMP-TABLE str-list 
    FIELD nr       AS INTEGER
    FIELD bezeich  AS CHAR.

DEFINE OUTPUT PARAMETER TABLE FOR str-list.

FIND FIRST str-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE str-list THEN DO:
    CREATE str-list.
    ASSIGN str-list.nr      = 1
           str-list.bezeich = "Total Room".
    CREATE str-list.
    ASSIGN str-list.nr      = 2
           str-list.bezeich = "Rooms Available".
    CREATE str-list.
    ASSIGN str-list.nr      = 3
           str-list.bezeich = "Rooms Occupied".
    CREATE str-list.
    ASSIGN str-list.nr      = 4
           str-list.bezeich = "House Uses".
    CREATE str-list.
    ASSIGN str-list.nr      = 5
           str-list.bezeich = "Complimentary Room".
    CREATE str-list.
    ASSIGN str-list.nr      = 6
           str-list.bezeich = "Paying Room".
    CREATE str-list.
    ASSIGN str-list.nr      = 7
           str-list.bezeich = "OOO Room".
    CREATE str-list.
    ASSIGN str-list.nr      = 8
           str-list.bezeich = "Complimentary Paying Guest".
    CREATE str-list.
    ASSIGN str-list.nr      = 9
           str-list.bezeich = "Room Sold".
    CREATE str-list.
    ASSIGN str-list.nr      = 10
           str-list.bezeich = "Vacant Rooms".
    CREATE str-list.
    ASSIGN str-list.nr      = 11
           str-list.bezeich = "% Occupancy".
    CREATE str-list.
    ASSIGN str-list.nr      = 12
           str-list.bezeich = "% Occupancy with Comp and HU".
    CREATE str-list.
    ASSIGN str-list.nr      = 13
           str-list.bezeich = "Person In House".
    CREATE str-list.
    ASSIGN str-list.nr      = 14
           str-list.bezeich = "Out of Order Rooms".
    CREATE str-list.
    ASSIGN str-list.nr      = 15
           str-list.bezeich = "Average Room Rate Rp".
    CREATE str-list.
    ASSIGN str-list.nr      = 16
           str-list.bezeich = "Average Room Rate Foreign".
    CREATE str-list.
    ASSIGN str-list.nr      = 17
           str-list.bezeich = "RevPar".
END.
