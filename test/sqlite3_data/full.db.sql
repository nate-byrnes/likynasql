BEGIN TRANSACTION;
INSERT INTO "cmdseq" ("id","name","overssh","ssh_as")
VALUES
(1,'ironfish',0,NULL);
INSERT INTO "batch" ("id", "name", "cmdseq_id")
VALUES
(1,'Rack A - Shelf 1',1),
(2,'Rack A - Shelf 2',1),
(3,'Rack A - Shelf 3',1),
(4,'Rack A - Shelf 4',1),
(5,'Rack B - Shelf 1',1),
(6,'Rack B - Shelf 2',1),
(7,'Rack B - Shelf 3',1),
(8,'Rack B - Shelf 4',1),
(9,'Rack C - Shelf 1',1),
(10,'Rack C - Shelf 2',1),
(11,'Rack C - Shelf 3',1),
(12,'Rack C - Shelf 4',1),
(13,'Rack D - Shelf 1',1),
(14,'Rack D - Shelf 2',1),
(15,'Rack D - Shelf 3',1),
(16,'Rack D - Shelf 4',1),
(17,'Rack E - Shelf 1',1),
(18,'Rack E - Shelf 2',1),
(19,'Rack E - Shelf 3',1),
(20,'Rack E - Shelf 4',1),
(21,'Rack F - Shelf 1',1),
(22,'Rack F - Shelf 2',1),
(23,'Rack F - Shelf 3',1),
(24,'Rack F - Shelf 4',1);
INSERT INTO "carrier" ("id", "mac_addr", "ip_addr", "serno", "detected_ts", "batch_id")
VALUES
(1, '5C:23:16:00:51:2A', '172.24.0.14', '4260440c185', '2024-01-15 11:22:22', 1),
(2, '5C:23:16:00:61:1C', '172.24.0.11', '725344Vc375', '2024-01-15 11:22:23', 1);
INSERT INTO "selector" ("id","name","matchattr","matchstr")
VALUES
(1,'PLACEHOLDER', NULL, NULL),
(2,'VCCINT', 'IPADDR', '172.24.0.14'), -- so 0.80 will be default, and this IP gets 0.44 if higher priority
(3,'VCCHBM',NULL,NULL),
(4,'VCCBRAM',NULL,NULL),
(5, 'Algorithm',NULL,NULL),
(6, 'Pool',NULL,NULL),
(7, 'PoolUser',NULL,NULL),
(8, 'PoolPass',NULL,NULL),
(9, 'HW-Type',NULL,NULL),
(10, 'fpga_tcore_limit',NULL,NULL),
(11, 'fpga_clk_core',NULL,NULL),
(12, 'fpga_max_jtag_mhz',NULL,NULL),
(13, 'IPLIST',NULL,NULL),
(14, 'IPADDR',NULL,NULL)
;
INSERT INTO "setting" ("id", "name","value","selector_id", "priority", "forattrn", "forattrv")
VALUES
(1, 'VCCINT', '0.80', 2, 0, NULL, NULL),
(2, 'VCCHBM', '1.05', 3, 0, NULL, NULL),
(3, 'VCCBRAM', '0.80', 4, 0, NULL, NULL),
(4, 'Algorithm', 'ironfish', 5, 0, NULL, NULL),
(5, 'Pool', 'stratum+tcp://us2.ironfish.herominers.com:1145', 6, 0, NULL, NULL),
(6, 'PoolUser', 'a642c55c4da184f3470a48db9affa9ea42c85f271fb7d39b8f6cae90fb4a56d0', 7, 0, NULL, NULL),
(7, 'PoolPass', 'x', 8, 0, NULL, NULL),
(8, 'HW-Type', 'fpga', 9, 0, NULL, NULL),
(9, 'fpga_tcore_limit', '85', 10, 0, NULL, NULL),
(10, 'fpga_clk_core', '700', 11, 0, NULL, NULL),
(11, 'fpga_max_jtag_mhz', '15', 12, 0, NULL, NULL),
(12, 'IPLIST', 'COMMA', 13, 0, NULL, NULL),
(13, 'IPADDR', 'SINGLE', 14,0, NULL, NULL),
(14, 'VCCINT_172.24.0.14', '0.44', 2, -1, 'IPADDR', '172.24.0.14'); -- 0.80 should override this value at -1 and this should override it when selected
INSERT INTO "argument" ("id","argstr","command_id", "selector_id","priority","separator") 
VALUES 
 (1,'-x',1,NULL,0,' '),
 (2,'-q',1,NULL,1,' '),
 (3,'-v',1,2,2,' '),
 (4,'-w',1,3,3,' '),
 (5,'-y',1,4,4,' '),
 (6,'-c',1,14,5,' '),
 (7,'-a',2,5,0,' '),
 (8,'-o',2,6,1,' '),
 (9,'-u',2,7,3,' '),
 (10,'-p',2,8,4,' '),
 (11,'--debug',2,NULL,5,' '),
 (12,'--hardware',2,9,6,'='),
 (13,'--fpga_tcore_limit',2,10,7,'='),
 (14,'--fpga_clk_core',2,11,8,'='),
 (15,'--fpga_max_jtag_mhz',2,12,9,'='),
 (16,'--fpga_jc_addr',2,13,10,'=')
 ;
INSERT INTO "command" ("id","path","executable","static_args","killaftersecs","killaftertxt","stdoutscraper","stderrscraper","autorestarttimes","enabled","cmdseq_id","priority","ssh", "ssh_as") 
VALUES 
 (1,'./test/scripts/','sqrl_bridge_2.2.0',NULL,5,'SQRL JTAG Board 0 Device 1 setting HBM voltage','bridge','bridge', NULL,1,1,1,NULL,NULL),
 (2,'./test/scripts/','teamredminer',NULL,NULL,NULL,'miner','miner',NULL,1,1,2,NULL,NULL);
INSERT INTO "threshold" ("id","level","direction","message")
VALUES
(2,0.5,'ABOVE_OK','Temperature on core to high'),
(1,5.0,'UNDER_OK','Supervisor not updating its metric');
COMMIT;
