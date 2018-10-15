
CREATE DATABASE dhcpdstat;
-- Create role. User: dhcpdagent, password: $]dQ-:JS2qaDjk{L
-- echo -n "$]dQ-:JS2qaDjk{Ldhcpdagent" | md5sum
CREATE ROLE dhcpdagent PASSWORD 'md5ef5bf8bed937b6e84196536cefc42e14' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
\c dhcpdstat

-- Active stat
CREATE TABLE active_stat (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    active_count bigint default 0,
    inacive_count bigint default 0
);
CREATE INDEx i1_active_stat on active_stat(tst,dhcpdhn);
GRANT ALL ON active_stat TO dhcpdagent;
GRANT ALL ON active_stat_id_seq TO dhcpdagent;

-- IP blocks stat
CREATE TABLE ipblock_stat (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    ipblock inet,
    active_count bigint default 0,
    inacive_count bigint default 0
);
CREATE INDEx i1_ipblock_stat on ipblock_stat(tst,dhcpdhn,ipblock);
GRANT ALL ON ipblock_stat TO dhcpdagent;
GRANT ALL ON ipblock_stat_id_seq TO dhcpdagent;

-- CPE stat
CREATE TABLE cpe_stat (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    dhcpdhn varchar,
    cpetype varchar,
    active_count bigint default 0,
    inacive_count bigint default 0
);
CREATE INDEx i1_cpe_stat on cpe_stat(tst,dhcpdhn,cpetype);
GRANT ALL ON cpe_stat TO dhcpdagent;
GRANT ALL ON cpe_stat_id_seq TO dhcpdagent;

-- IP blocks
CREATE TABLE ipblock (
    id serial PRIMARY KEY,
    tst timestamp DEFAULT now(),
    ipblock_net inet, -- network address
    ipblock_prefix smallint, -- prefix number
    usersegment varchar, -- (home,startup,business,industry,ONG,Government,mobile,m2m,iot,etc)
    att varchar, -- access technology type
    userlocation varchar,
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
