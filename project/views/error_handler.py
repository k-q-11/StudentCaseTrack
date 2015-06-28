from project import myapp
from flask import request, render_template, flash, g
'''
@myapp.errorhandler(404)
def page_not_exist(e):
	path = request.path
	# go through each blueprint to find the prefix that matches the path
	# can't use request.blueprint since the routing didn't match anything
	for bp_name, bp in myapp.blueprints.items():
	    if path.startswith(bp.url_prefix):
	        # get the 404 handler registered by the blueprint
	        handler = app.error_handler_spec.get(bp_name, {}).get(403)

	        if handler is not None:
	            # if a handler was found, return it's response
	            #return render_template('access_deny.html', privileges=current_privileges())
	            return handler(e)
	return render_template('access_deny.html', privileges=current_privileges())
	# return a default response
	#return render_template('404.html'), 404	
'''	