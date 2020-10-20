# Requirements
This script is made for Python 3 or later in Windows systems.
All the libraries imported in the manuscript should be installed beforehand.
You only have to prepare 'recipe_example.csv' file in the same directory and excute 'async_dashboard.py' on a command prompt.
# Purposes and Feartures
This script is intended to serve as an interactive dahboard that can manage asynchronous coroutines, and has the feartures below. 

- All you need is one .py script and one recipe file.
- The script construsts a server in localhost and GUIs are viwed by using browsers.
- When you click 'START', the asynchronous processes are commenced. If you click 'STOP' during operation, all the process loop are terminated, and after that, the GUI becomes reusable.
- You can edit 'measure.excute' method to realize the processes you want. The content of 'recipe.csv' can be used to configure the processes.

For a simple demonstration, 'async_dashboard.py' measures time intervals between 50-ms-long asynchronous sleeps, from which you can evaluate the time precision of this dashboard.

# Structures
This code is a modified code from [bokeh/examples/howto/server_embed/standalone_embed.py](https://github.com/bokeh/bokeh/blob/branch-2.3/examples/howto/server_embed/standalone_embed.py).

- class status() preserves the ON/OFF status of the process.
- class graph() plots a interactivegrash using bokeh. Method .excute() collects date from tornado.Queue. Method .update updates the graph.
- class measure() describes the process you need to do. Method .excute() measures the time intervals and input the date to tornado.Queue. Here is where you should edit to add functions that you want to implement.
- class starter() preserves the number of running coroutines to manage ON/OFF status properly.

Just inside bkapp(doc), you should add widgets as many as you want. The Bokeh library provides wide variety of widgets, e.g. a folder locator and a slider. 


# References
- [github.com/bokeh/bokeh/tree/branch-2.3/examples/howto/server_embed](https://github.com/bokeh/bokeh/tree/branch-2.3/examples/howto/server_embed)
- [docs.bokeh.org/en/latest/docs/user_guide/server.html](https://docs.bokeh.org/en/latest/docs/user_guide/server.html)