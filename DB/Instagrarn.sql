use InstagrarnDB;

create table Insta_user(
	idx int(9) NOT NULL auto_increment,
	email VARCHAR(300),
    phone VARCHAR(300),
    full_name VARCHAR(300),
    id VARCHAR(300),
    pwd VARCHAR(300),
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Insta_likes(
	idx int(9) NOT NULL auto_increment,
	user_idx int(9) NOT NULL,
	board_idx int(9) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Insta_reply(
	idx int(9) NOT NULL auto_increment,
    board_idx int(9) NOT NULL,
	user_idx int(9) NOT NULL,
	reply int(9) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Insta_alert(
	idx int(9) NOT NULL auto_increment,
	from_user_idx int(9) NOT NULL,
	to_user_idx int(9) NOT NULL,
    alert_type int(9) NOT NULL,
	PRIMARY KEY(idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create view Insta_reply_view as select u.id, r.board_idx, r.reply
        from Insta_reply as r, Insta_user as u where r.user_idx = u.idx;
        
create view Insta_alert_view as select u.id, a.from_user_idx, a.to_user_idx, a.alert_type
        from Insta_alert as a, Insta_user as u where a.from_user_idx = u.idx;