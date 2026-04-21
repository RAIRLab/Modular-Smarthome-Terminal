# HOW TO MAKE A PLUGIN

## File Structure


**├─** SMTplugins/

**│ └──** &lt;NAME OF PLUGIN FOLDER&gt;/

**│ │ ├─** &lt;NAME OF PLUGIN&gt;\_route.py

**│ │ ├─** &lt;NAME OF PLUGIN&gt;\_widget.py

**│ │ └─** Data.json (Optional)

**│ └─** pluginImport.py

**├─** static/

**│ ├─** js/

**│ │ ├─** plugins/

**│ │ │ └─** &lt;NAME OF PLUGIN&gt;\_script.js

**│ │ └─** main.js  
**│ ├─** widgetCSS/  
**│ │** **└─** &lt;NAME OF PLUGIN&gt;\_widget.css

**│ ├─** stylesheet.css

**│ └─** settings_stylesheet.css

**├─** templates/

**│ ├─** index.html

**│ └─** setttingspage.html

**├─** layout_client.json

**└─** flaskServer.py

…


## Actually Making a Plugin

1)  Inside of SMTplugins/ you must put a folder with your plugins name EX: \`\`\`Weather\`\`\`. This folder will contain the routing and code for the widget, inherited widget class from 'Widget.py', and an optional 'data.json'.

2) In the route file, you must use the library Blueprint from Flask.

```
from flask import Blueprint
weather_bp = Blueprint('weather_bp', \__name_\_)

@weather_bp.route('…..')
```

3) In 'pluginImport.py' you must add your blueprint:
```
from SMTplugins.Weatherr.weather_route import weather_bp
```

4)  Then register that route in the flask server file:
```
App.register_blueprint(weather_bp)
```

5)  Add you widget to the layout_client.json
```
{
"id": "weather",
"name": "Weather",
"class": "weather-widget",
"css_name": "weather_widget.css",
"row": 1,
"col": 3
}
```

6)  In ```/js/plugins/``` add your js file ```weather_script.js```

```
setInterval(updateWeather, 15000); //Update Every 15 seconds, each is different
updateWeather();
```

7) Now in \`\`\`main.js\`\`\` add your widget script

		```import {} from './plugins/weather_script.js' ```

8) Now in the widgetCSS folder, add your css file named &lt;Name of Widget&gt;\_widget.css