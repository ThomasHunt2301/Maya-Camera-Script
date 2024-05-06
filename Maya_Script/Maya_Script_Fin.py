import maya.cmds as cmds
import os
# Global variable to store the UI text display

def create_window():
    global focal_length, horizontal_aperture, focal_length_slider, aperture_slider, name_dropdown #Global variables


    if cmds.window("MyWindow", exists=True):
        cmds.deleteUI("MyWindow", window=True) #If window exists it will delete it and recreate it
        
    window = cmds.window("MyWindow", title="Camera Setup", widthHeight=(400, 200))#Creates Window With the Name Camera Setup with width set
    cmds.columnLayout(adjustableColumn=True)#Create column layout
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(200, 200))
    cmds.button(label="Create Lighting Setup", command=create_lighting_setup, width=200, height=30)#Creates Button for the lighting setup
    cmds.button(label="Create Test Geo", command=create_shapes_in_line, width=200, height=30)#Creates Button for the geometry
    cmds.setParent("..")  #Move back to the main column layout
   
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(80, 100, 200)) #creates the dropdown box for the cams
    cmds.text(label="Select Camera:")# Names the dropdown select camera

    #Read cameras from file
    Cameras_file_path = "D:\\Year 3\\Maya_Script\\20038581_ThomasHunt_InnovationVFX_2024\\Maya_Script\\Settings.txt"
    if os.path.exists(Cameras_file_path):#If it can reead the file it opens the file and then it looks for a line if the file with an "_" and reads that line and puts it into the dropdown box
        with open(Cameras_file_path, "r") as file:
            names = [line.strip() for line in file.readlines() if "_" in line]
            name_dropdown = cmds.optionMenu(width=200, changeCommand=slider_values)
    for name in names:
        cmds.menuItem(label=name)
    cmds.setParent("..")  #Move back to the column layout

    #Focal Length Section
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(80, 100, 200))
    cmds.text(label="Focal Length:")
    focal_length_slider = cmds.floatSlider(minValue=1.0, maxValue=200.0, value=50.0, step=0.1, width=200, dragCommand=update_focal_length)#Makes a slider and makes it so you can't go lower than 1 and about 200
    focal_length = cmds.text(label="50.0", align="left")#Puts the value of focal length next to the slider
    cmds.setParent("..")  #Move back to the column layout

    #Aperture Section
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(80, 100, 200))
    cmds.text(label="Aperture:")
    aperture_slider = cmds.floatSlider(minValue=0.1, maxValue=10.0, value=1.0, step=0.1, width=200, dragCommand=update_aperture)#Sets Min and max number for the slider
    horizontal_aperture = cmds.text(label="1.0", align="left")
    cmds.setParent("..")  #Move back to the column layout
    
    #Button layout creation
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
    cmds.text(label="")  #Empty column on the left
    Create_camera_Button = cmds.button(label="Create Camera", command=create_camera, width=200, height=30)#Makes a create camera button in the centre because of the empty columns
    cmds.button(Create_camera_Button, edit=True, bgc=(0.0, 1.0, 0.0))  #Set the color to green
    cmds.text(label="")  #Empty column on the right
    cmds.setParent("..")  #Move back to the column layout

    #Button to reset sliders
    cmds.button(label="Reset Sliders", command=reset_sliders, width=100, height=15)#Creates button that resets sliders using the reset command

    #Button to clear the scene
    clear_button = cmds.button(label="Clear Scene", command=clear_scene, width=200, height=30)
    cmds.button(clear_button, edit=True, bgc=(1.0, 0.0, 0.0))  #Set the color to red

    cmds.showWindow(window)


#Grabs the slider info from the settings file and then displays them
def slider_values(option):
    settings_file_path = "D:\\Year 3\\Maya_Script\\20038581_ThomasHunt_InnovationVFX_2024\\Maya_Script\\Settings.txt"
    if os.path.exists(settings_file_path):
        try:
            with open(settings_file_path, "r") as file:
                settings_data = file.read()
            # Split the settings data by camera settings
            camera_settings = settings_data.strip().split("\n\n")
            # Find the settings for the selected camera
            for settings_block in camera_settings:
                settings_lines = settings_block.strip().split("\n")
                if settings_lines[0] == option:  # first line of each block is the camera name
                    # Process the settings for the selected camera
                    for line in settings_lines[1:]:
                        setting_name, setting_value = line.split(":")#Looks for the : in the line and then after that it reads that as the data needed for the sliders
                        setting_name = setting_name.strip()
                        setting_value = float(setting_value.strip())
                        
                        if setting_name == "Focal Length":
                            cmds.floatSlider(focal_length_slider, edit=True, value=setting_value)
                            cmds.text(focal_length, edit=True, label=str(setting_value))
                        elif setting_name == "Aperture":
                            cmds.floatSlider(aperture_slider, edit=True, value=setting_value)
                            cmds.text(horizontal_aperture, edit=True, label=str(setting_value))
                        
                    break

        except Exception as e: #Finds if there are any erros and if there is any problems reading the file location
            print("Error reading settings file:", e)
    else:
        print("Settings file not found:", settings_file_path)

def reset_sliders(*args):
    # Reset focal length slider and display
    cmds.floatSlider(focal_length_slider, edit=True, value=50.0)
    cmds.text(focal_length, edit=True, label="50.0")
    # Reset Aperture slider and display
    cmds.floatSlider(aperture_slider, edit=True, value=1.0)
    cmds.text(horizontal_aperture, edit=True, label="1.0")


def update_aperture(value):
    camera = cmds.ls(type="camera", long=True)[0]
    cmds.setAttr(camera + ".horizontalFilmAperture", float(value))
    cmds.text(horizontal_aperture, edit=True, label=str(value))


def update_focal_length(value):
    camera = cmds.ls(type="camera", long=True)[0] # Assuming there is only one camera in the scene
    cmds.setAttr(camera + ".focalLength", float(value))
    cmds.text(focal_length, edit=True, label=str(value))
    
    

# Function to clear the scene 
def clear_scene(*args):
    cmds.delete(cmds.ls())

def create_camera(*args):#Creates the camera where the current perspective is
    current_camera = cmds.lookThru(q=True)
    selected_name_index = cmds.optionMenu(name_dropdown, query=True, select=True)
    selected_name = cmds.optionMenu(name_dropdown, query=True, value=True)
    
    if selected_name_index and selected_name:#When created it will change the name to the selected camera from the dropdown
        new_camera_name = selected_name.replace(" ", "_") 
        new_camera = cmds.duplicate(current_camera, name=new_camera_name)[0]
        
        # Get the current values from the sliders
        focal_length = cmds.floatSlider(focal_length_slider, query=True, value=True)
        horizontal_aperture = cmds.floatSlider(aperture_slider, query=True, value=True)
      
        # Set camera attributes to new created camera
        cmds.setAttr(new_camera + ".focalLength", focal_length)
        cmds.setAttr(new_camera + ".horizontalFilmAperture", horizontal_aperture)
        return new_camera

def create_shapes_in_line(*args):#If there are geo already it will delete old geo and replace it with new
    if cmds.objExists('Test_cube'):
        cmds.delete('Test_cube')
    if cmds.objExists('Test_sphere'):
        cmds.delete('Test_sphere')
    if cmds.objExists('Test_cone'):
        cmds.delete('Test_cone')    
    cube = cmds.polyCube(name='Test_cube')[0]#Create geo and moves it in a line
    cmds.move(-4, 1, 0, cube)  
    sphere = cmds.polySphere(name='Test_sphere')[0]
    cmds.move(0, 1, 0, sphere)  
    cone = cmds.polyCone(name='Test_cone')[0]
    cmds.move(4, 1, 0, cone)  

# Function to create a point light
def create_point_light(name, intensity, color, position):
    light = cmds.pointLight(name=name, intensity=intensity, rgb=color, position=position)
    return light

# Function to create a dome light
def create_dome_light(name, intensity, color, position):
    light = cmds.ambientLight(name=name, intensity=intensity, rgb=color, position=position)
    return light

    
# creates lighting setup with a key light, fill light, rim light and ambient light. can change translation,intensity and colour here.
def create_lighting_setup(*args):
    cmds.delete(cmds.ls(type='light'))
    key_light_intensity = 10.0
    key_light_color = (1.0, 1.0, 1.0)
    fill_light_intensity = 0.5
    fill_light_color = (0.5, 0.5, 0.5)
    rim_light_intensity = 2000.0
    rim_light_color = (0.2, 0.2, 0.2)
    ambient_light_intensity = 1000.0
    ambient_light_color = (1.0, 1.0, 1.0)
    key_light = create_point_light(name="keyLight", intensity=key_light_intensity, color=key_light_color, position=(5, 5, 5))
    fill_light = create_point_light(name="fillLight", intensity=fill_light_intensity, color=fill_light_color, position=(-5, 4, -5))
    rim_light = create_point_light(name="rimLight", intensity=rim_light_intensity, color=rim_light_color, position=(0, 0, -5))
    ambient_light = create_dome_light(name="ambientLight", intensity=ambient_light_intensity, color=ambient_light_color, position=(0, 0, 8))



# Run the function to create the window
create_window()

