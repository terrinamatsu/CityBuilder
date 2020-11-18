# CityBuilder
Generates custom cities in Maya based on input heightmap, written in Python.


There are several options available to manipulate the city building program to create different looking cities. 

First is the file dialog box, so you can select a file to use as the heightmap for the city’s landscape generation. 

Next are a series of sliders, which give finer control over the scale of the city. These include tree, city, and road density, which gives the general estimation of the number of each component in the city, in relation to the city size, which is controlled individually in width and height by the next set of sliders. 

Finally is the slider for the road length, which can control how spread out the city and its roads are. Beyond the sliders are a series of radio buttons, which control the climate (colour, presence of trees, and map height), and the city type (low houses or skyscrapers).

Beyond these options, the next bar is a progress bar that shows the completion of the generation of the city when in progress, and the final buttons clear the scene, generate road and building placement maps, city and map generation, and then the cancel button.

So, simply alter the sliders and buttons, and then press the ‘Landscape OK’ button to generate, but make sure to pull the camera back to get a view of the city being generated. 
Also, depending on city size, it may take from 2 to about 10 minutes to generate fully.
