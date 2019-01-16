from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:a13342404594@localhost/web_im_flask'
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'user'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	username = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	phone = db.Column(db.String(11))
	country = db.Column(db.String(30))
	province = db.Column(db.String(30))
	city = db.Column(db.String(30))
	sex = db.Column(db.Integer)
	birthday = db.Column(db.Date, default=datetime.today)
	age = db.Column(db.Integer)
	signature = db.Column(db.Text, nullable=True, default='这个人懒得没有签名...')
	avatar = db.Column(db.String(128), default='/statics/img/default_avatar_male_180.gif')
	status = db.Column(db.Integer)
	created_time = db.Column(db.DateTime, default=datetime.now)
	
	def __repr__(self):
		return '<User %r>' % self.username


class Group(db.Model):
	'''
	好友分组，属于某个用户
	一个用户（User）有多个好友分组（Group），
	一个好友分组（Group）只属于一个用户（User）
	'''
	__tablename__ = 'group'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	name = db.Column(db.String(128))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	owner = db.relationship('User', backref=db.backref('groups', lazy=True))

	def __str__(self):
		return self.name


# 分组成员中间表
group_members = db.Table(
	'group_members',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)


class GroupChat(db.Model):
	'''
	群聊，独立于用户存在
	'''
	__tablename__ = 'group_chat'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	name = db.Column(db.String(128))
	group_chat_avatar = db.Column(db.String(128))


# 群聊管理员中间表
group_chat_admins = db.Table(
	'group_chat_admins',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('group_chat_id', db.Integer, db.ForeignKey('group_chat.id'), primary_key=True)
)


# 群聊成员中间表
group_chat_members = db.Table(
	'group_chat_members',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('group_chat_id', db.Integer, db.ForeignKey('group_chat.id'), primary_key=True)
)

if __name__ == '__main__':
	db.drop_all()
	
	db.create_all()
