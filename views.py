from jinja2 import Template , Environment,FileSystemLoader
from models import Model_Comment,Model_User,Model_Article
from cookies import *

env = Environment(loader=FileSystemLoader('templates'))


class comments():
	def __init__(self):
		self.template = 'templates/comments_page.html'
	
	def db_work(self,params):
		global cookies_param
		a = Model_Comment()
		if 'body' in params:
			a.add_comment(cookies_param['user'],params['body'])
		else:
			pass
		coments = a.get_all_comments()
		return coments

	def form_coment(self,params):
		html = open(self.template,'r').read()
		template_r = Template(html)
		params['coments'] = self.db_work(params)
		return template_r.render(params)



	def render(self,get_params,post_params):
		params = {**get_params,**post_params}
		header = ''
		if params != '':
			return self.form_coment(params)
		else:
			with open(self.template) as template_r:
				return template_r.read()


# def index(params):
# 	with open('templates/index.html') as template:
# 		return template.read() 



# def blog(params):
# 	with open('templates/blog.html') as template:
# 		if params != '':
# 	 		if 'name' in params and 'body' in params:
# 	 			html = template.read()
# 	 			template_r = Template(html)
# 	 			a = Model_Comment()
# 	 			a.add_comment(params['name'],params['body'])
# 	 			coments = a.get_all_comments()
# 	 			params['coments'] = coments
# 	 			return template_r.render(params)
# 	 		else:
# 	 			return template.read()
# 	 	else:
# 	 		return template.read()


class login():
	def __init__(self):
		self.template = 'login.html'

	def login_user(self,params):
		a = Model_User()
		print(a.get_all_users())
		if 'username' in params and 'password' in params:
			ans = a.isset_user(params['username'],params['password'])
			if ans != None:
				return ( ans[0] ,'Hello ' + ans[-2])
			else:
				user = ''
				return (user ,'Enter right username and password')
		else:
			user = ''
			return (user,'Enter field')
	def render(self,get_params,post_params):
		global cookies_param
		if cookies_param['user'] != '':
			ans = 'You have been authoresated ' + cookies_param['user']
		else:	
			if post_params != '':
				user , ans = self.login_user(post_params)
				
				cookies_param['user'] = user
			else:
				ans = ''	

		global env
		template_b = env.get_template(self.template)
		params = {'status':ans,**cookies_param}
		return template_b.render(params)


class register():
	def __init__(self):
		self.template = 'register.html'

	def create_user(self,params):
		a = Model_User()
		status = ''
		if 'username' in params and 'password' in params and 'email' in params and 'name' in params and 'surename' in params:
			a.create_user(params['username'],params['password'],params['email'],params['name'],params['surename'])
			status = 'Sucsses'
		else:
			status = 'Fall'
		return status

	def render(self,get_params,post_params):
		if post_params != '':
			status = self.create_user(post_params)	
		else:
			status = 'Enter Field'
		global cookies_param
		params = {'status':status,**cookies_param}
		global env
		template_b = env.get_template(self.template)
		return template_b.render(params)

class articles():
	def __init__(self):
		self.template = 'articles.html'

	def all(self):
		a = Model_Article()
		all_articles = a.get_all_articles()
		t = []
		for i in all_articles:
			a = i[0].replace('+',' ')
			b = i[1].replace('+',' ')
			t.append((a,b,i[-1]))

		return t

	def render(self,get_params,post_params):
		global cookies_param
		global env
		template_b = env.get_template(self.template)
		params = {'articles':self.all(),**cookies_param}
		return template_b.render(params)


class articles_add():
	def __init__(self):
		self.template = 'articles_add.html'
	
	def db_work(self,params):
		a = Model_Article()
		if 'title' in params and 'body' in params:
			try:
				a.add_article(params['title'],params['body'])
				status = 'OK'
			except:
				status = 'Error'
		else:
			status = 'Enter Field'
		return status


	def render(self,get_params,post_params):
		status = ''
		status = self.db_work(post_params)
		global env
		global cookies_param

		template_b = env.get_template(self.template)
		params = {'status':status,**cookies_param}
		return template_b.render(params)


class articles_detail():
	def __init__(self):
		self.template = 'articles_detail.html'

	def db_work(self,params,id):
		global cookies_param
		a = Model_Comment()
		if 'think' in params:
			a.add_comment(cookies_param['user'],params['think'],id)
		else:
			print('faaaal')
		coments = a.get_all_comments(id)
		print(coments)
		return coments

	def article_params(self,params):
		id = params['id']
		a = Model_Article()
		try:
			title , body , baz , idi = a.get_by_id(id)
			bod = body.replace('+',' ')
			tit = title.replace('+',' ')
			req = {'title':tit,'body':bod,'baz':baz,'id':idi}
		except:
			title ='' 
			body = '' 
			baz = ''
			idi = ''
			req = {'title':title,'body':body,'baz':baz,'id':idi}

		return req

	def render(self,get_params,post_params):
		if 'id' not in get_params:
			return 'Article not found'
		else:
			params = self.article_params(get_params)
			params['coments'] = self.db_work(post_params,get_params['id'])
		global env
		global cookies_param
		paramsa={**params,**cookies_param}
		template_b = env.get_template(self.template)
		return template_b.render(paramsa)



class articles_delete():
	def __init__(self):
		self.template = 'articles_delete.html'

	def article_delite(self,params):
		a = Model_Article()
		try:
			a.delete_by_id(params['id'])
			status = 'Deleted'
		except:
			status = 'Error'
		return status

	def render(self,get_params,post_params):
		global cookies_param

		if 'id' not in get_params:
			return 'Article not found'
		else:
			status = self.article_delite(get_params)
		params = {'status' : status}
		global env
		template_b = env.get_template(self.template)
		params['user'] = cookies_param['user']
		return template_b.render(params)


class articles_update():
	def __init__(self):
		self.template = 'articles_update.html'

	def articles_update(self,id,title,body):
		a = Model_Article()
		a.update_by_id(title,body,id)
		status = 'Updated'

		return status

	def render(self,get_params,post_params):
		global cookies_param
		if 'id' not in get_params:
			return 'Article not found'
		else:
			a = Model_Article()
			title , body , baz , idi = a.get_by_id(get_params['id'])
			params = {'title':title,'body':body,**cookies_param}
			if 'title' in post_params and 'body' in post_params:
				status = self.articles_update(get_params['id'],post_params['title'],post_params['body'])
			else:
				status = 'Enter Field'
		

		global env
		template_b = env.get_template(self.template)
		params['status'] = status
		return template_b.render(params)

class logout(object):
	def __init__(self):
		self.template = 'logout.html'

	def render(self,get_params,post_params):
		global cookies_param
		global env
		cookies_param['user'] = ''
		params = {**cookies_param}
		template_b = env.get_template(self.template)
		return template_b.render(params)



class articles_search():
	def __init__(self):
		self.template = 'articles_search.html'
	def s_f(self,params):
		a = Model_Article()
		ans = a.search(params['s'])
		return ans
	def render(self,get_params,post_params):
		global cookies_param
		global env
		ans = self.s_f(get_params)
		params = {**cookies_param,'ans':ans}
		template_b = env.get_template(self.template)
		return template_b.render(params)




class user():
	def __init__(self):
		self.template = 'user.html'

	def render(self,get_params,post_params):
		global cookies_param
		global env
		a = Model_User()
		b = a.info(cookies_param['user'])
		params = {**cookies_param,'info':b}
		template_b = env.get_template(self.template)
		return template_b.render(params)
