from flask_nav import Nav
from flask_bootstrap.nav import BootstrapRenderer

# To keep things clean, we keep our Flask-Nav instance in here. We will define
# frontend-specific navbars in the respective frontend, but it is also possible
# to put share navigational items in here.

#nav = Nav()


#custom navbar
def dynamic_navbar():
	navbar = Navbar(title='navbar_titel')
	navbar.items = [View('FirstPage', 'first_page')]   
	navbar.items.append(
	Subgroup('Dropdown1',
		View('Sub1', 'sub1_page'),
		View('Sub2', 'sub2_page'),
		View('Sub3', 'sub3_page')
					)
			)       
	navbar.items.append(View('SecondPage', 'second_page'))
	return navbar

#register navbar to app    
nav.register_element('topp', dynamic_navbar)


