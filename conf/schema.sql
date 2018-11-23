
CREATE DATABASE dhcpdstat;
-- Create role. User: dhcpdagent, password: $]dQ-:JS2qaDjk{L
-- echo -n "$]dQ-:JS2qaDjk{Ldhcpdagent" | md5sum
CREATE ROLE dhcpdagent PASSWORD 'md5ef5bf8bed937b6e84196536cefc42e14' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
\c dhcpdstat

-- Ojects
CREATE TABLE objects (
  id bigserial PRIMARY KEY,
  tst timestamp DEFAULT now() NOT NULL,
  obj_orig_id bigint NOT NULL,
  obj_orig_table varchar NOT NULL,
  obj_type varchar NOT NULL, -- server,ipblock,router,userseg,cpe,vlan
  obj_parent bigint,
  active Boolean DEFAULT True,
  alarm Boolean DEFAULT True
);
GRANT ALL ON objects TO dhcpdagent;
GRANT ALL ON objects_id_seq TO dhcpdagent;
CREATE INDEX i1_objects ON objects(obj_orig_id,obj_type,obj_parent,active);

-- Events definition
CREATE TABLE events (
  id bigserial PRIMARY KEY,
  event_obj_type varchar NOT NULL, -- server,ipblock,router,userseg,cpe,vlan
  event_obj_attr varchar NOT NULL, -- object attribute
  event_obj_attr_type varchar NOT NULL, -- text,int,float,array,boolean
  attr_table varchar,
  attr_column varchar,
  threshold_type varchar NOT NULL, -- fixed,relative,external
  threshold_op varchar NOT NULL, -- eq, lt, le, gt, ge, not
  threshold_int int,
  threshold_float real,
  threshold_text varchar,
  threshold_boolean Boolean,
  event_severity int NOT NULL, -- debug,info,notice,warning,err,crit,alert,emerg
  event_cause varchar NOT NULL,
  event_description varchar NOT NULL,
  relative_sql varchar
);
GRANT ALL ON events TO dhcpdagent;
GRANT ALL ON events_id_seq TO dhcpdagent;

-- Predefined events
INSERT INTO events(event_obj_type,event_obj_attr,event_obj_attr_type,attr_table,attr_column,threshold_type,event_severity,event_cause,event_description,threshold_op,threshold_int) VALUES
('server','actives','int','active_stat','active_count','fixed',2,'unknow','Server leases too low','eq',0),
('server','dhcpdiscover','int','active_stat','dhcpdiscover','fixed',2,'Clients reconnections','Server DHCPDISCOVER rate too high','ge',100),
('ipblock','actives','int','ipblock_stat','active_count','fixed',2,'unknow','IP block leases too low','eq',0),
('ipblock','dhcpdiscover','int','ipblock_stat','dhcpdiscover','fixed',2,'Clients reconnections','IP block DHCPDISCOVER rate too high','ge',100)
;
INSERT INTO events(event_obj_type,event_obj_attr,event_obj_attr_type,attr_table,attr_column,threshold_type,event_severity,event_cause,event_description,threshold_op,threshold_boolean,relative_sql) VALUES
('ipblock','actives','boolean',NULL,NULL,'relative',2,'Max leases','IP block leases too high','eq',True,$$SELECT (ipblock_maxleases-%(active_count)s)<10 AS column_0 FROM ipblock WHERE id=%(obj_orig_id)s$$),
('ipblock','dhcpdiscover','boolean',NULL,NULL,'relative',2,'DHCPDISCOVER greater than DHCPOFFER','DHCPDISCOVER greater then DHCPOFFER','eq',True,$$SELECT (%(dhcpdiscover)s>%(dhcpoffer)s) AS column_0$$)
('server','dhcpdiscover','boolean',NULL,NULL,'relative',2,'DHCPDISCOVER greater than DHCPOFFER','DHCPDISCOVER greater then DHCPOFFER','eq',True,$$SELECT (%(dhcpdiscover)s>%(dhcpoffer)s) AS column_0$$)
;

-- Event log
CREATE TABLE event_log (
  id bigserial PRIMARY KEY,
  raise_time timestamp DEFAULT NOW(),
  clear_time timestamp,
  active Boolean DEFAULT True,
  acknowledged Boolean DEFAULT False,
  notified Boolean DEFAULT False,
  obj_id bigint,
  event_id bigint,
  threshold_text varchar,
  threshold_int bigint,
  threshold_float real,
  threshold_boolean Boolean,
  raise_value_text varchar,
  raise_value_int bigint,
  raise_value_float real,
  raise_value_boolean Boolean,
  recovery_value_text varchar,
  recovery_value_int bigint,
  recovery_value_float real,
  recovery_value_boolean Boolean
);
GRANT ALL ON event_log TO dhcpdagent;
GRANT ALL ON event_log_id_seq TO dhcpdagent;
CREATE INDEX i1_event_log ON event_log(obj_id,event_id);
CREATE INDEX i2_event_log ON event_log(raise_time,clear_time);
CREATE INDEX i3_event_log ON event_log(active,acknowledged,notified);

-- Servers
CREATE TABLE servers (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    hostname varchar UNIQUE NOT NULL,
    active Boolean DEFAULT True,
    report Boolean DEFAULT True,
    alarms Boolean DEFAULT True,
    emailfrom varchar DEFAULT 'no-reply@intranet-stats.org' NOT NULL, -- no-reply@[hostname]
    emailrcp varchar,
    reportrcp varchar,
    eventrcp varchar,
    smtpserveraddress inet DEFAULT '127.0.0.1' NOT NULL,
    smtpserverport int DEFAULT 25 NOT NULL,
    remarks varchar
);
GRANT ALL ON servers TO dhcpdagent;
GRANT ALL ON servers_id_seq TO dhcpdagent;

-- Active stat
CREATE TABLE active_stat (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    active_count bigint default 0,
    inactive_count bigint default 0,
    dhcpdiscover bigint,
    dhcpoffer bigint,
    dhcprequest bigint,
    dhcpack bigint
);
CREATE INDEx i1_active_stat on active_stat(tst,dhcpdhn);
GRANT ALL ON active_stat TO dhcpdagent;
GRANT ALL ON active_stat_id_seq TO dhcpdagent;

-- Active stat history
CREATE TABLE active_stat_history (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    active_count_max bigint default 0,
    active_count_min bigint default 0,
    active_count_avg bigint default 0,
    inactive_count bigint default 0,
    dhcpdiscover bigint,
    dhcpoffer bigint,
    dhcprequest bigint,
    dhcpack bigint
);
CREATE INDEx i1_active_stat_history on active_stat_history(tst,dhcpdhn);
GRANT ALL ON active_stat_history TO dhcpdagent;
GRANT ALL ON active_stat_history_id_seq TO dhcpdagent;

-- IP blocks stat
CREATE TABLE ipblock_stat (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    ipblock inet,
    ipblock_prefix smallint,
    ipblock_maxleases int,
    active_count bigint default 0,
    inactive_count bigint default 0,
    dhcpdiscover bigint,
    dhcpoffer bigint,
    dhcprequest bigint,
    dhcpack bigint
);
CREATE INDEx i1_ipblock_stat on ipblock_stat(tst,dhcpdhn,ipblock);
GRANT ALL ON ipblock_stat TO dhcpdagent;
GRANT ALL ON ipblock_stat_id_seq TO dhcpdagent;

CREATE TABLE ipblock_stat_history (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    ipblock inet,
    ipblock_prefix smallint,
    active_count_max bigint default 0,
    active_count_min bigint default 0,
    active_count_avg bigint default 0,
    inactive_count bigint default 0,
    dhcpdiscover bigint,
    dhcpoffer bigint,
    dhcprequest bigint,
    dhcpack bigint
);
CREATE INDEx i1_ipblock_stat_history on ipblock_stat_history(tst,dhcpdhn,ipblock);
GRANT ALL ON ipblock_stat_history TO dhcpdagent;
GRANT ALL ON ipblock_stat_history_id_seq TO dhcpdagent;

-- CPE stat
CREATE TABLE cpe_stat (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    cpevendormodel varchar,
    active_count bigint default 0,
    inactive_count bigint default 0,
    dhcpdiscover bigint,
    dhcpoffer bigint,
    dhcprequest bigint,
    dhcpack bigint
);
CREATE INDEx i1_cpe_stat on cpe_stat(tst,dhcpdhn,cpevendormodel);
GRANT ALL ON cpe_stat TO dhcpdagent;
GRANT ALL ON cpe_stat_id_seq TO dhcpdagent;

-- CPE stat history
CREATE TABLE cpe_stat_history (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    cpevendormodel varchar,
    active_count_max bigint default 0,
    active_count_min bigint default 0,
    active_count_avg bigint default 0,
    inactive_count bigint default 0,
    dhcpdiscover bigint,
    dhcpoffer bigint,
    dhcprequest bigint,
    dhcpack bigint
);
CREATE INDEx i1_cpe_stat_history on cpe_stat_history(tst,dhcpdhn,cpevendormodel);
GRANT ALL ON cpe_stat_history TO dhcpdagent;
GRANT ALL ON cpe_stat_history_id_seq TO dhcpdagent;

-- IP blocks
CREATE TABLE ipblock (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    ipblock_net inet, -- network address
    ipblock_prefix smallint, -- prefix number
    ipblock_maxleases int,
    server_name varchar,
    usersegment varchar, -- (home,startup,business,industry,ONG,Government,mobile,m2m,iot,etc)
    att varchar, -- access technology type
    userlocation varchar,
    routername varchar,
    vlanname varchar,
    others varchar
);
CREATE UNIQUE INDEX i1_ipblock on ipblock(ipblock_net,ipblock_prefix);
GRANT ALL ON ipblock TO dhcpdagent;
GRANT ALL ON ipblock_id_seq TO dhcpdagent;

-- CPE mac
CREATE TABLE cpe_mac (
    tst timestamp DEFAULT now(),
    mac_prefix varchar PRIMARY KEY,
    vendor_name varchar,
    model_name varchar,
    release timestamp,
    eol timestamp,
    eos timestamp
);
GRANT ALL ON cpe_mac TO dhcpdagent;
