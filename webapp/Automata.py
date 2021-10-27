import Page1
import Page2
import Page3

from multiapp import MultiApp

app = MultiApp()
app.add_app("Introduction to CA", Page1.app)
app.add_app("Explore Elementary CA", Page2.app)
app.add_app("The Majority Problem", Page3.app)
app.run()