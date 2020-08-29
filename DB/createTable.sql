USE AirdndDB;

create table airdnd_picture(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	url VARCHAR(300) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table airdnd_home_notice(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	home_notice_sort VARCHAR(100) NOT NULL,
    home_notice_content VARCHAR(300) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table airdnd_convenient_facility(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	facility VARCHAR(200) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table airdnd_review(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	user_name VARCHAR(200) NOT NULL,
	review_date DATE NOT NULL,
	review_content VARCHAR(10000) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table airdnd_attractions_distance(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	attractions_name VARCHAR(200) NOT NULL,
	attractions_distance VARCHAR(200) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table airdnd_use_rule(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	use_rule VARCHAR(200) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table airdnd_safety_rule(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	safety_rule VARCHAR(200) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table airdnd_bed(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	bed_room_name VARCHAR(200) NOT NULL,
	bed_room_option VARCHAR(200) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table airdnd_host(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	host_name varchar(100) NOT NULL,
	host_sign_in_date varchar(100) NOT NULL,
	check_superhost int(3) DEFAULT 0,
	check_certification int(3) DEFAULT 0,
	host_review_num int(3) DEFAULT 0,
	host_status_message VARCHAR(500),
	Interaction_with_guests VARCHAR(500),
	host_language VARCHAR(200),
	response_rate VARCHAR(200),
	response_time VARCHAR(200),
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

set foreign_key_checks = 0;
truncate table airdnd_home;
truncate table airdnd_home_attractions_distance;
truncate table airdnd_home_bed;
truncate table airdnd_home_convenient_facility;
truncate table airdnd_home_notice;
truncate table airdnd_home_picture;
truncate table airdnd_home_review;
truncate table airdnd_home_safety_rule;
truncate table airdnd_home_use_rule;
truncate table airdnd_host;
set foreign_key_checks = 1;


delete from AirdndDB.airdnd_home where home_idx = 44725172;
delete from AirdndDB.airdnd_home_attractions_distance where home_idx = 44725172;
delete from AirdndDB.airdnd_home_bed where home_idx = 44725172;
delete from AirdndDB.airdnd_home_convenient_facility where home_idx = 44725172;
delete from AirdndDB.airdnd_home_notice where home_idx = 44725172;
delete from AirdndDB.airdnd_home_picture where home_idx = 44725172;
delete from AirdndDB.airdnd_home_review where home_idx = 44725172;
delete from AirdndDB.airdnd_home_safety_rule where home_idx = 44725172;
delete from AirdndDB.airdnd_home_use_rule where home_idx = 44725172;
delete from AirdndDB.airdnd_host where home_idx = 44725172;


commit;