
INSERT INTO progfile (bezeich) VALUES
('1;1;Print Room Revenue Breakdown;Room Revenue Breakdown;Print Room Revenue Breakdown;True'),
('2;1;Check Opened Master Bill;Opened Master Bill;Check Ther Master Bill of The Guest Who Has Checked Out;True'),
('3;1;Check Nation & Country;Check Nation & Country;Check Nation And Country of In house Guest;True'),
('4;1;Check Outlet Occupied Table;Occupied Table;Check The Outlet Where The Table Is Still Occupied;True'),
('6;1;Print Today Departed Guest;Departure Guest;Print Today Departed Guest;True'),
('5;1;Print Arrival Guest;Arrival Guest;Print Arrival Guest;True'),
('7;2;Competitor Setup;Competitor Statistic Entry;Competitor Entry;True'),
('8;2;Competitor Report;Hotel Competitor Statistic With Indexes;Check Competitor Statistic;True'),
('9;2;Print Daily Revenue Report;Daily Report;Print Daily Revenue Report;True');


update htparam set fchar='Asia/Jakarta' where paramnr=91;