USE AirdndDB;

create table airdnd_picture(
	idx int(9) NOT NULL auto_increment,
	home_idx int(9) NOT NULL,
	url VARCHAR(300) NOT NULL,
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

commit;