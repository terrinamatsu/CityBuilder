'''
    This is a Maya Python script to generate simple cities based on input images.
    
    
    Written by Jacob Worgan as a Computer Animation: Technical Arts student @ Bournemouth University, Jan-May 2019.
    For 1st year, 2nd semester; Technical Arts Production Python Project.
    Ver 1.0, 10/5/2019 01:11
'''

import maya.cmds as cmds
import math as maths
import random
import sys
import os
sys.path.append("/usr/lib64/python2.7/site-packages/")



class ObjectWorks():
    ''' The ObjectWorks class is used to handle the creation and placement of the scene geometry, including the map planes,
        and any buildings, trees, or other objects that will be in the city scene.'''
    
    def __init__(me):
        ''' This procedure handles the creation of object instances of the ObjectWorks class.
            Because the geometry is created after the class has been initialised, this function
            is left empty.
        
            - no parameters, nor return'''
        
        a = 1
        
                
    def generateMap(me, img, imgValues, progBar, cityType, *_):
        ''' The gereateMap procedure is used to generate the map plane geometry for the scene.
            This includes the land plane, the water plane, and the colouring of said planes.
            
            img            :the map the geometry will be based on. (usually the imageworks blur image)
            imgValues      :the values from the img map having been loaded using the python image library for direct pixel access.
            progBar        :the progress bar ui element, to allow the bar to fill as the geometry is being placed.
            cityType       :the city type, based on the ui radiobuttons. From 1 to 4, meaning plane, desert, forest, and mountain respectively.
        
            - no return'''
        
        # clear scene
        cmds.select(all=True)
        cmds.delete()
        
        
        # create plane colour shaders
        me.WaterBlinn = cmds.shadingNode('blinn', asShader=True)
        cmds.setAttr(me.WaterBlinn + '.color', 0.3, 0.5, 1)   
        me.GroundBlinn = cmds.shadingNode('blinn', asShader=True)
        # check city location for ground plane colour & for steeper plane for mountainous cities
        if cityType == 2:
            #desert
            cmds.setAttr(me.GroundBlinn + '.color', 1, 1, 0.5)
            me.steepness = 1
        elif cityType == 1:
            #plains
            cmds.setAttr(me.GroundBlinn + '.color', 0.2, 0.9, 0.2)
            me.steepness = 1
        elif cityType == 3:
            #forest
            cmds.setAttr(me.GroundBlinn + '.color', 0.8, 1, 0.2)
            me.steepness = 1
        elif cityType == 4:
            #mountain
            cmds.setAttr(me.GroundBlinn + '.color', 0.65, 0.51, 0.39)
            me.steepness = 2

        # create water plane
        me.waterplane = cmds.polyPlane(n='water_plane', w=(img.size[1]), h=(img.size[0]))
        cmds.xform(me.waterplane, r=True, t=[0, 0.5, 0])
        # create heightmap plane
        me.landplane = cmds.polyPlane(n='ground_plane', sx=(img.size[1]-1), sy=(img.size[0]-1), w=(img.size[1]), h=(img.size[0]))
        
        # assign plane colour shaders
        cmds.select(me.waterplane)
        cmds.hyperShade(assign=me.WaterBlinn)
        cmds.select(me.landplane)
        cmds.hyperShade(assign=me.GroundBlinn)
        
        # move plane vertices
        for i in range(img.size[0]):
            cmds.progressBar(progBar, edit=True, step=1)
            for j in range(img.size[1]):
                cmds.xform( me.landplane[0]+".vtx["+str(i*img.size[1]+j)+"]", r=True, t=[0, imgValues[i,j][0]/(50/me.steepness), 0])
                cmds.refresh(f = True)
            
                
    def generateBuildings(me, img, okmapImgVal, popDensity, progBar, heightImg, roadmapImg, cityType, treeDensity, buildingType, *_):
        ''' The generate buildings procedure is used to create and place the scene's buildings,
            trees, and other geometry that is to be places onto the map planes.
        
            img            :the map with which the geometry will be placed in respect to. (usually the imageworks blur image)
            okmapImgVal    :the values from the okimg map having been loaded using the python image library,
                            with pixels either black, meaning nothing can be places on that tile, or white, meaning it can.
            popDensity     :the value from the population slider ui element, acting as a percentage chance of an ok tile having a building.
            progBar        :the progress bar ui element, to allow the bar to fill as the geometry is being placed.
            heightImg      :the values from the img map having been loaded using the python image library for direct pixel access.
            roadmapImg     :the map of the generated roads that buildings will be placed around.
            cityType       :the city type, based on the ui radiobuttons. From 1 to 4, meaning plane, desert, forest, and mountain respectively.
            treeDensity    :the percentage chance of a tree being placed on a given empty tile.
            buildingType   :flag for the hight of the buildings, 1 for max height 3, 2 for relative to city size (larger skyscrapers) 
        
            - no return'''
        
        # City buildings generation, grid based 
        me.newBuildings=[]
        me.newTrees=[]
                 
        # building shader blinn created
        me.BuildingBlinn = cmds.shadingNode('blinn', asShader=True)
        cmds.setAttr(me.BuildingBlinn + '.color', 0.5, 0.5, 0.5)
        # tree shader blinn created
        me.TreesBlinn = cmds.shadingNode('blinn', asShader=True)
        cmds.setAttr(me.TreesBlinn + '.color', 0.35, 0.6, 0.2)
    
        
        # for every pixel of the image map...            
        for i in range(0, img.size[0]):
            cmds.progressBar(progBar, edit=True, step=1)
            for j in range(0, img.size[1]):                  
                
                # check for a neighbouring road on the road map...
                neighbour = 0
                
                if (j < img.size[1] - 1):
                    if (roadmapImg[i,j+1] == (255,255,255)):
                        neighbour = 1
                        down = 0.6
                    else:
                        down = 0
                if (i < img.size[0] - 1):
                    if (roadmapImg[i+1,j] == (255,255,255)):
                        neighbour = 1
                        right = 0.6
                    else:
                        right = 0
                if (j > 0) & (i < img.size[0] - 1):
                    if (roadmapImg[i+1,j-1] == (255,255,255)):
                        neighbour = 1                    
                if (i > 0) & (j < img.size[1] - 1):
                    if (roadmapImg[i-1,j+1] == (255,255,255)):
                        neighbour = 1                    
                if (i < img.size[0] - 1) & (j < img.size[1] - 1):
                    if (roadmapImg[i+1,j+1] == (255,255,255)):
                        neighbour = 1                    
                if (i > 0):
                    if (roadmapImg[i-1,j] == (255,255,255)):
                        neighbour = 1
                if (j > 0):
                    if (roadmapImg[i,j-1] == (255,255,255)):
                        neighbour = 1
                if (i > 0) & (j > 0):
                    if (roadmapImg[i-1,j-1] == (255,255,255)):
                        neighbour = 1    

                # if the road is found, and the point is white on the ok map...
                if (okmapImgVal[i, j] == (255,255,255)) & (neighbour == 1):
                    # ...and given a random chance for a building, based on popDensity...
                    if popDensity > random.randint(1, 100):
                        # create the random building height, sloping up towards the map centre
                        if buildingType == 1:
                            w = random.randint(1,3)/2
                        else:
                            w = random.randint(1,(1 + (img.size[0]/2 + img.size[1]/2) / 5) - (abs(i - img.size[0]/2) + abs(j - img.size[1]/2)) / 5)/2
                        # create and move the building
                        newBuilding = cmds.polyCube(n='building_w'+str(i)+'_h'+str(j), h=w, w=1-right, d=1-down)
                        cmds.move((j) - img.size[1]/2,w/2 + w%0.5 + heightImg[i, j][0]/(50/me.steepness),-(i) + img.size[0]/2, newBuilding )
                        # add the building to the building array
                        me.newBuildings.append('building_w'+str(i)+'_h'+str(j))                    
                                                
                    else:
                        # if the building was not placed, and city is not a desert, give a chance for the placing of a tree
                        if (treeDensity >= random.randint(1, 100)) & (okmapImgVal[i, j] == (255,255,255)) & (cityType <> 2):
                            me.newTrees.append(me.createTree(i,j,img, heightImg))
                else:
                    # if the building was not placed, and city is not a desert, give a chance for the placing of a tree
                    if (treeDensity >= random.randint(1, 100)) & (okmapImgVal[i, j] == (255,255,255)) & (cityType <> 2):
                        me.newTrees.append(me.createTree(i,j,img, heightImg))
        
        # group the buildings, and apply the colour shader                        
        cmds.group(me.newBuildings, n='Buildings', w=True)
        cmds.select(me.newBuildings)
        cmds.hyperShade(assign=me.BuildingBlinn)
        
        if cityType <> 2:
            # if the city isn't a desert, group and shade the trees
            cmds.group(me.newTrees, n='Trees', w=True)
            cmds.select(me.newTrees)
            cmds.hyperShade(assign=me.TreesBlinn)
            
            # as city generation is done, make sure progress bar is full
            cmds.progressBar(progBar, edit=True, step=10000)


    def createTree(me, i, j, img, heightImg, *_):
        ''' Function to create and place a tree, made of a cylinder and cone,
             with randomised height and radius.
        
            i                :the location along the width of the map the tree will be placed on.
            j                :the location along the height of the map the tree will be placed on.
            img              :the map with which the geometry will be placed in respect to. (usually the imageworks blur image)
            heightImg        :the values from the img map having been loaded using the python image library for direct pixel access.
        
            Returns:     the created tree.'''
        
        # Random values for the tree's height and radius are calculated
        radiusRND = (0.2 + (random.randint(0, 2) * 0.15))
        heightRND = (0.7 + (random.randint(0, 5) * 0.1))
        
        # Then the tree is created and moved into place on the plane
        newTreeTop = cmds.polyCone(n='Tree_w'+str(i)+'_h'+str(j), r=radiusRND, h=heightRND)    
        newTreeBase = cmds.polyCylinder(n='Trunk_w'+str(i)+'_h'+str(j), r=radiusRND/3, h=0.3)
        cmds.move((j) - img.size[1]/2, heightRND/2 + 0.3 + heightImg[i, j][0]/(50/me.steepness), -(i) + img.size[0]/2, newTreeTop )
        cmds.move((j) - img.size[1]/2, 0.15+ heightImg[i, j][0]/(50/me.steepness), -(i) + img.size[0]/2, newTreeBase )
        
        return cmds.group(newTreeTop, newTreeBase, n='Tree_w'+str(i)+'_h'+str(j), w=True)


class ImageWorks():
    ''' The ImageWorks class deals with all of the image manipulation processes, based on the initial loaded heightmap image,
        as well as the storage of all of said images.'''

    def __init__(me):
        ''' This procedure handles the creation of object instances of the ImageWorks class.
            Because the images are created after the class has been initialised, this function
            is left empty.
        
            - no parameters, nor return'''
        
        a = 1
        
        
    def create(me, mapWidth, mapHeight, mapFile, *_):
        ''' This function handles the initialisation of all of the images the program will use to create the city.
        
            mapWidth            :the integer width of the city plane, based on the cityWidth slider ui element.
            mapHeight           :the integer height of the city plane, based on the cityHeight slider ui element.
            mapFile             :the string path to the image file loaded in the ui.
        
            - returns false if the image mapFile points to exits, true if not.'''
        
        # First loading the heightmap
        from PIL import Image
        imagePath = "/home/s5107963/Downloads/"
        imageFileName = imagePath + "rc.png"
        # Then they are loaded, if the file exists, else return False
        import os.path
        if os.path.isfile(mapFile):
            me.im = Image.open(mapFile)
            me.im = me.im.convert('RGB')
            me.im = me.im.resize((mapWidth,mapHeight))   
        else:
            return False         
        
        # Stores the image height and width to object-wide variables
        me.Width, me.Height = me.im.size
        me.imValues = me.im.load()
        
        # Then the blured image    
        me.blurIm = Image.new('RGB', (me.Width, me.Height))
        me.blurImValues = me.blurIm.load()
        
        # Then the gradient image
        me.gradIm = Image.new('RGB', (me.Width, me.Height))
        me.gradImValues = me.gradIm.load()
        
        # Then the ok area map
        me.okmapIm = Image.new('RGB', (me.Width, me.Height))
        me.okmapImValues = me.okmapIm.load()
        
        # Then the road map
        me.roadmapIm = Image.new('RGB', (me.Width, me.Height))
        me.roadmapImValues = me.roadmapIm.load()
        
        return True
        
        
    def roadMapImg(me, roadDensity, roadLength, *_):
        ''' The roadMapImg procedure handles the creation of the road map that will determine the 
            placement of buildings.
        
            roadDensity        :the number of reccursions for the roadMapReccursion algorithm, giving more roads on the map.
            roadLength         :the average length of the roads on the map
            
            - no return'''
        
        
        from PIL import ImageDraw
        # initialise the imageDraw image
        me.x = me.Width/2
        me.y = me.Height/2
        me.d= ImageDraw.Draw(me.roadmapIm)
        
        # call the reccursive raod drawing function
        me.roadMapReccursion(roadDensity, 'x', roadLength)
        
        # show the created road map    
        me.roadmapIm.show()
        
        
    def roadMapReccursion(me, depth, direction, roadLength, *_):
        ''' The roadMapReccursion function is a reccursive algorithm used to draw roads to a road map image.
            It repeatedly calls itself to draw from a point in the four directions while the depth is greater than 0,
            as it decreased with each reccursion.
            
            depth            :the number of reccursions levels left
            direction        :the current line direction.
            roadLength       :the average length of roads on the map.
        
            
            Return 0 when depth is 0 or all directions done, to exit reccursion.'''
        
        from PIL import ImageDraw
        
        # create coordinates for road end point
        x2=me.x
        y2=me.y
        # check direction, and add a random value to the end point to give final road end point
        if direction == 'u':
            y2=me.y+random.randint(roadLength, roadLength + (me.Width * me.Height / 20000))
        elif direction == 'd':
            y2=me.y-random.randint(roadLength, roadLength + (me.Width * me.Height / 20000))
        elif direction == 'l':
            x2=me.x-random.randint(roadLength, roadLength + (me.Width * me.Height / 20000))
        elif direction == 'r':
            x2=me.x+random.randint(roadLength, roadLength + (me.Width * me.Height / 20000))
            
        # check the values aren't outside city bounds...
        if x2 < 1:
            x2 = 1
        elif x2 > me.Width:
            x2 = me.Width
            
        if y2 < 1:
            y2 = 1
        elif y2 > me.Height:
            y2 = me.Height
        
        # draw the line to the road map
        me.d = ImageDraw.Draw(me.roadmapIm)
        me.d.line((me.x, me.y, x2, y2))
        
        # set current point to the new line end point
        me.x = x2
        me.y = y2        
        
        # check depth limit hasn't been reached, then give chance to reccursively call the function in each direction
        if depth <= 0:
            return 0
        else:
            depth -= 1
            if (direction != 'u') & (1 < random.randint(2,4)):
                me.roadMapReccursion(depth, 'u', roadLength)
            if (direction != 'd') & (1 < random.randint(2,4)):
                me.roadMapReccursion(depth, 'd', roadLength)
            if (direction != 'l') & (1 < random.randint(2,4)):
                me.roadMapReccursion(depth, 'l', roadLength)
            if (direction != 'r') & (1 < random.randint(2,4)):
                me.roadMapReccursion(depth, 'r', roadLength)
        return 0
        
        
    def blurImg(me, *_):
        ''' The blurImg procedure simply blurs the current image to the blur image,
            using a function part of the python image library.
            
            - no parameters, nor return'''
        
        # this is to blur the main image
        from PIL import ImageFilter
        me.blurIm= me.im.filter(ImageFilter.GaussianBlur(radius=1))
        me.blurImValues = me.blurIm.load()
        
        
    def gradientImg(me, img, *_):
        ''' The gradientImg procedure is used to find the gradient of the image at each point and print this to a gradient map.
            
            img     :a flag, 0 to find gradient based on original loaded image file, 1 to find it for the created blurred image.
            
            -no return'''
        
        # checks which image to create gradient image for, based on img parameter
        if img == 1:
            Values = me.blurImValues
        else:
            Values = me.imValues
        
        for i in range(0, me.Width):
            for j in range(0, me.Height):
                # For every pixel, compared to surrounding pixels to find greatest difference out of the 8 with the current pixel
                currentHeight = Values[i,j][0]
                highestHeight = 0
                
                if (i > 0):
                    if abs(Values[i-1,j][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i-1,j][0] - currentHeight)
                if (i > 0) & (j > 0):
                    if abs(Values[i-1,j-1][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i-1,j-1][0] - currentHeight)
                if (j > 0):
                    if abs(Values[i,j-1][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i,j-1][0] - currentHeight)
                if (i < me.Width - 1):
                    if abs(Values[i+1,j][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i+1,j][0] - currentHeight)
                if (i < me.Width - 1) & (j < me.Height - 1):
                    if abs(Values[i+1,j+1][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i+1,j+1][0] - currentHeight)  
                if (j < me.Height - 1):
                    if abs(Values[i,j+1][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i,j+1][0] - currentHeight)   
                if (i > 0) & (j < me.Height - 1):
                    if abs(Values[i-1,j+1][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i-1,j+1][0] - currentHeight)  
                if (j > 0) & (i < me.Width - 1):
                    if abs(Values[i+1,j-1][0] - currentHeight) > highestHeight:
                        highestHeight = abs(Values[i+1,j-1][0] - currentHeight)  
                         
                
                # adds the pixel to the file
                me.gradIm.putpixel((i,j), (highestHeight,0,0))  
         
                      
    def okmapImg(me, *_):
        ''' The okmapImg procedure generates the 'ok map' image, 
            which gives white on pixels where gradient is low (based on the current gradient image)
            and the point is above the water level (based on the current blur image).
            
            -no parameters, nor return'''
         
        # for each point...
        for i in range(0, me.Width):
            for j in range(0, me.Height):
                # ...check its gradient isn't too high, and it is above water level...
                if (me.gradImValues[i,j][0] < 20) & (me.blurImValues[i,j][0] >= 30):
                    # ...then place a white pixel at the point on the ok map
                    me.okmapIm.putpixel((i,j), (255,255,255))                      
                    
                      
    def showGradImg(me, *_):
        ''' The showGradImg function is to show the gradient image.
            
            -no parameters, nor return'''
            
        # show the gradient image
        me.gradIm.show()
        
        
    def showOkmapImg(me, *_):
        ''' The showOkmapImg function is to show the ok map image.
            
            -no parameters, nor return'''
            
        # show the ok map image
        me.okmapIm.show()



class MainWindow():
    ''' This class makes and handles the UI elements of the City Building program. '''
    
    def __init__(me):
        ''' This procedure handles the initialisation of the MainWindow objects,
            as well as the maya ui elements.
        
            - no parameters, nor return'''
        # creates window
        
        # UI element value stores
        me.PopSlider_Val = 100
        me.HeightSlider_Val = 100
        me.WidthSlider_Val = 100
        me.TreeDensitySlider_Val = 40
        me.CityRoadSpreadSlider_Val = 50
        me.CityRoadAmountSlider_Val = 4
        me.images = ImageWorks()
        me.objects = ObjectWorks()
        me.fileLocal = "/home/s5107963/Downloads/rc.png"
        
        # window creation
        me.windowID="Maya City Builder"
        me.windowTitle="City Builder"
        if cmds.window(me.windowID, exists=True):
            cmds.deleteUI(me.windowID)
        
        me.Window=cmds.window(me.windowID, title=me.windowTitle, widthHeight=(600,2000))
        
        # ____________start layout____________ #
        cmds.columnLayout(columnAttach=('both',5), rowSpacing=10, columnWidth=600)
        
        # city builder logo
        path = ''
        cmds.image(image=path + 'mayacitybuilser2.png', height=350, width=600)
        
        # city heightmap picture loading
        '''
        pictureFilter="*.png"
        cmds.fileBrowserDialog(fileFilter=pictureFilter, dialogStyle=2, operationMode=" * (Import")
        '''

        # heightmap image load field
        me.PicFileLoadButton = cmds.textFieldButtonGrp(label='City Height Map File', bl='Browse...', bc= me.fileDialogBox, width=400)
        
        
        # city grid size & city density sliders (10-200 blocks)
        me.PopSlider = cmds.intSliderGrp(label='City Building Density', field=True, min=10, max=100, value=60, step=1, dc= me.sliderUpdatePop)
        me.HeightSlider = cmds.intSliderGrp(label='City Height', field=True, min=50, max=200, value=100, step=1, dc= me.sliderUpdateHeight)
        me.WidthSlider = cmds.intSliderGrp(label='City Width', field=True, min=50, max=200, value=100, step=1, dc= me.sliderUpdateWidth)
        
        cmds.separator(style='shelf')
 
        # tree and road density/spread sliders
        me.TreeDensitySlider = cmds.intSliderGrp(label='Tree Density', field=True, min=0, max=100, value=40, step=1, dc= me.sliderUpdateTreeDensity)
        me.CitySpreadSlider = cmds.intSliderGrp(label='Minimum Road Length', field=True, min=1, max=10, value=5, step=1, dc= me.sliderUpdateCitySpread)
        me.CityRoadAmountSlider = cmds.intSliderGrp(label='City Road Amount', field=True, min=0, max=10, value=4, step=1, dc= me.sliderUpdateRoadAmount)
        
        cmds.separator(style='shelf')
        
        # terrain and city type options
        me.TerrainType = cmds.radioButtonGrp(label='Climate', labelArray4=['Plains','Desert','Forest','Mountainous'], numberOfRadioButtons=4, sl=1)
        me.BuildingType = cmds.radioButtonGrp(label='City Type', labelArray2=['Town', 'City'], numberOfRadioButtons=2, sl=2)
        
        cmds.separator(style='shelf')
                
        # progress bar to show city generation percentage completion
        me.ProgressBar = cmds.progressBar(maxValue=(me.HeightSlider_Val * 2))
                
        # button to clear maya scene
        cmds.button(label='delete scene', command= me.deleteAll, width=200)
                        
        # ok/cancel buttons
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(200,200,200))
        cmds.button(label='Images OK', c= me.imgProcessing, width=200)
        cmds.button(label='Landscape OK', c= me.landscapeButton, width=200)
        cmds.button(label='cancel', command="cmds.deleteUI('%s')" % me.Window, width=200)
                
        # show window
        cmds.showWindow(me.Window)
    
    
    def deleteAll(me, *_):
        ''' This is a simple function that selects, then deletes
            everything in the Maya scene.
            
            - no parameters, nor return'''
        
        # clear maya scene
        cmds.select(all=True)
        cmds.delete()
    
    
    def sliderUpdateTreeDensity(me, *_):
        ''' Called when city tree density slider is moved.
            Stores live value of slider into variable 'TreeDensitySlider_Val'. 
            
            - no parameters, nor return'''
        
        me.TreeDensitySlider_Val = cmds.intSliderGrp(me.TreeDensitySlider, q=True, v=True)
        
        
    def sliderUpdateCitySpread(me, *_):
        ''' Called when city spread slider is moved.
            Stores live value of slider into variable 'CityRoadSpreadSlider_Val'. 
            
            - no parameters, nor return'''
        
        me.CityRoadSpreadSlider_Val = cmds.intSliderGrp(me.CitySpreadSlider, q=True, v=True)


    def sliderUpdateRoadAmount(me, *_):
        ''' Called when city road amount slider is moved.
            Stores live value of slider into variable 'CityRoadAmountSlider_Val'. 
            
            - no parameters, nor return'''
        
        me.CityRoadAmountSlider_Val = cmds.intSliderGrp(me.CityRoadAmountSlider, q=True, v=True)
    
    
    def sliderUpdatePop(me, *_):
        ''' Called when city population density slider is moved.
            Stores live value of slider into variable 'PopSlider_Val'. 
            
            - no parameters, nor return'''
        
        me.PopSlider_Val = cmds.intSliderGrp(me.PopSlider, q=True, v=True)
        
        
    def sliderUpdateWidth(me, *_):
        ''' Called when city width slider is moved.
            Stores live value of slider into variable 'WidthSlider_Val'. 
            
            - no parameters, nor return'''
        
        me.WidthSlider_Val = cmds.intSliderGrp(me.WidthSlider, q=True, v=True)
    
    
    def sliderUpdateHeight(me, *_):
        ''' Called when city height slider is moved.
            Stores live value of slider into variable 'HeightSlider_Val'. 
            
            - no parameters, nor return'''
        
        me.HeightSlider_Val = cmds.intSliderGrp(me.HeightSlider, q=True, v=True)
    
    
    def fileDialogBox(me, *_):
        ''' A procedure that handles the dialog box that appears after pressing the button to 
            browse for a suitable .png image file to use as the city heightmap.
            
            - no parameters, nor return'''
        
        pictureFilter="*.png"
        #fileLocal = cmds.fileBrowserDialog(fileFilter=pictureFilter, dialogStyle=2, operationMode=" * (Import", fileMode=0)
        me.fileLocal = cmds.fileDialog2(cap='Import Height Map', ds=1, ff=pictureFilter, fm=1)
        me.fileLocal = str(me.fileLocal)[3:-2]
        cmds.textFieldButtonGrp(me.PicFileLoadButton, tx=str(me.fileLocal), e=True)
            
    
    def imgProcessing(me, *_):
        ''' The imgProcessing procedure is used to create the images used as reference for the generation of
            the city geometry.
        
            - no parameters, nor return'''
        
        # check and store value of load image field
        me.fileLocal = cmds.textFieldButtonGrp(me.PicFileLoadButton, tx=True, q=True)
        
        # generate the maps, if the image exists and is loaded correctly
        if (me.images.create(me.WidthSlider_Val, me.HeightSlider_Val, me.fileLocal)) <> False:
            me.images.blurImg()
            me.images.gradientImg(1)
            me.images.okmapImg()
            me.images.roadMapImg(me.CityRoadAmountSlider_Val, me.CityRoadSpreadSlider_Val)
            me.images.showOkmapImg()
            return True
        else:
            cmds.confirmDialog(title='Error', message='Image file doesn\'t exist. Please choose a valid .png file.')
            return False


    def landscapeButton(me, *_):
        ''' The landscapeButton function is called when the user presses the build landscape button.
            The function is used to call the landscapeProcessing function which builds the actual map,
            but first checks the size of the map, and if larger than default, asks the user to confirm they want
            to carry out the function as it may take a while.
            
            - no parameters, nor return'''
        
        confirmMssg='At these dimensions, the city building may take a while. Are you sure you want to start?'
        # check city size, and if too large, ask if user wants to generate city before doing so
        if me.WidthSlider_Val + me.HeightSlider_Val > 200:
            if cmds.confirmDialog(title='For eel?', message=confirmMssg, button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No') <> 'No':
                me.landscapeProcessing()
        else:
            me.landscapeProcessing()


    def landscapeProcessing(me, *_):
        ''' The landscapeProcessing procedure handles the calling of funcitons to create the city scene geometry.
        
            - no parameters, nor return'''
        
        # generate new image maps, and the city geometry
        cmds.progressBar(me.ProgressBar, edit=True, maxValue=(me.HeightSlider_Val + me.PopSlider_Val))
        cmds.progressBar(me.ProgressBar, edit=True, progress=0)
        if (me.imgProcessing()) <> False:
            me.objects.generateMap(me.images.blurIm, me.images.blurImValues, me.ProgressBar, cmds.radioButtonGrp(me.TerrainType, q=True, sl=True))
            me.objects.generateBuildings(me.images.blurIm, me.images.okmapImValues, me.PopSlider_Val, me.ProgressBar, me.images.blurImValues, me.images.roadmapImValues, cmds.radioButtonGrp(me.TerrainType, q=True, sl=True), me.TreeDensitySlider_Val, cmds.radioButtonGrp(me.BuildingType, q=True, sl=True))

        

# main program
if __name__=="__main__":
    main = MainWindow()
