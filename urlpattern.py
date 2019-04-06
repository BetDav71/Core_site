from views import *
urlpattern = {
	'/login' : login().render,
	'/regestration' : register().render,
	'/comments' : comments().render,
	'/' : articles().render,
	'/articles/add' : articles_add().render,
	'/articles/detail' : articles_detail().render,
	'/articles/delete' : articles_delete().render,
	'/articles/update' : articles_update().render,
	'/logout' : logout().render,
	'/articles/search' : articles_search().render,
	'/account' : user().render
}

