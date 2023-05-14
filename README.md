# Automatic Material Swapper for Maya
## version 1.0

This tool can be used to automatically swap between Arnold and Renderman materials in Maya.  

Supported materials in both the render engines: 
* Arnold - aiStandardSurface
* Renderman - PxrSurface

## Installation
* Copy the code from Material_Swapper.py         
 
* Create a shelf button in Maya and paste the above copied code.  

## How to use
1. Open a scene with either Arnold (aiStandardSurface) or Renderman (PxrSurface) materials already applied to the objects.
2. Click on the shelf button to launch the tool  
3. Select the desired object.
4. Choose the correct option on the radio buttons.  
5. Click on Convert
6. Done.  
7. Repeat the same for all the other objects in the scene.  

## Features details

*   ##  Doesn't create new file nodes  
*   The tool doesn't create any new file nodes for the texture files.

*   ##  Error messages 
*   Error messages are shown if no object is selected or object with the wrong material is selected.

*  ##   The tool currently matches the below mentioned attributes between the two renderers.
*   Diffuse color
*   Specular color
*   Specular roughness
*   Metalness
*   Normal


## Credits
Created by Shubham Prabhakar    