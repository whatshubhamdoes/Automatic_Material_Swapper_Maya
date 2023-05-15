import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.mel as mel
import os
import sys

# Function to convert aiStandardSurface to PxrSurface
def convert_aiStandardSurface_material() :
    # get selected object and if not selected prompt user to select an object#
    sel = cmds.ls(sl=True)
    if not sel :
        cmds.confirmDialog(title='Error', message='Please select an object', button=['OK'], defaultButton='OK')
        cmds.warning("Error : Please select an object")
        return
    
    for obj in sel :
        # get the selected object's material and if not material prompt user to assign a material#
        theNodes = cmds.ls(sl = True, dag = True, s = True)
        shadeEng = cmds.listConnections(theNodes , type = 'shadingEngine')
        print(shadeEng)
        if shadeEng :
            for sg in shadeEng :
                arnold_mat = cmds.ls(cmds.listConnections(shadeEng), materials = True)
                if cmds.nodeType(arnold_mat) != 'aiStandardSurface' :
                    cmds.confirmDialog(title='Error', message='Selected object does not have an Arnold Standard Surface material applied.', button=['OK'], defaultButton='OK')
                    cmds.warning("Error : Selected object does not have an Arnold Standard Surface material applied.")
                    return
                if arnold_mat :
                    # Create a new RenderMan PxrSurface material
                    renderman_shader = cmds.shadingNode('PxrSurface', asShader=True)
                    shading_group = cmds.sets(renderman_shader, renderable=True, noSurfaceShader=True, empty=True, name=renderman_shader + 'SG')
                    cmds.connectAttr(renderman_shader + '.outColor', shading_group + '.surfaceShader', force=True)
                    components_arnold= ['.baseColor','.specularColor','.specularRoughness','.metalness','.normalCamera']

                    for attr in components_arnold :
                        arnold_mat_new=''.join(arnold_mat)
                        value = cmds.getAttr(arnold_mat_new + attr )
                        file_node=cmds.connectionInfo(arnold_mat_new + attr, sourceFromDestination=True)
                        
                        # checking each attribute and attaching them to PxrSurface
                        if attr == '.baseColor' :
                            renderman_shader=''.join(renderman_shader)
                            renderman_shader_new=renderman_shader + '.diffuseColor'
                            cmds.setAttr(renderman_shader_new,value[0][0],value[0][1],value[0][2],type='double3')
                            if file_node:
                                file_path = cmds.listConnections(arnold_mat_new + attr,type='file')
                                file_path=''.join(file_path)
                                cmds.connectAttr(file_path + '.outColor',renderman_shader_new)
                        if attr == '.specularColor' :
                            renderman_shader=''.join(renderman_shader)
                            renderman_shader_new_1=renderman_shader + '.specularFaceColor'
                            cmds.setAttr(renderman_shader_new_1,value[0][0],value[0][1],value[0][2],type='double3')
                            renderman_shader_new_2=renderman_shader + '.specularEdgeColor'
                            cmds.setAttr(renderman_shader_new_2,value[0][0],value[0][1],value[0][2],type='double3')
                            if file_node:
                                file_path = cmds.listConnections(arnold_mat_new + attr,type='file')
                                file_path=''.join(file_path)
                                cmds.connectAttr(file_path + '.outColor',renderman_shader_new_1)
                                cmds.connectAttr(file_path + '.outColor',renderman_shader_new_2)
                        if attr == '.specularRoughness' :
                            renderman_shader=''.join(renderman_shader)
                            renderman_shader_new=renderman_shader + '.specularRoughness'
                            cmds.setAttr(renderman_shader_new,value)
                            if file_node:
                                file_path = cmds.listConnections(arnold_mat_new + attr)
                                file_path=''.join(file_path)
                                cmds.connectAttr(file_path + '.outAlpha',renderman_shader_new)
                        if attr == '.metalness' :
                            # as explained in this - https://rmanwiki.pixar.com/display/REN24/PxrMetallicWorkflow
                            renderman_shader=''.join(renderman_shader)
                            rman_metallic_shader = cmds.shadingNode('PxrMetallicWorkflow', asShader=True)
                            if file_node:
                                file_path_bColor = cmds.listConnections(arnold_mat_new + '.baseColor',type='file')
                                file_path_bColor=''.join(file_path_bColor)
                                cmds.connectAttr(file_path_bColor + '.outColor',rman_metallic_shader + '.baseColor')
                                file_path_metallic = cmds.listConnections(arnold_mat_new + attr,type='file')
                                file_path_metallic=''.join(file_path_metallic)
                                cmds.connectAttr(file_path_metallic + '.outAlpha',rman_metallic_shader + '.metallic')
                            else:
                                file_node_new=cmds.connectionInfo(arnold_mat_new + '.baseColor', sourceFromDestination=True)
                                if file_node_new:
                                    file_path_bColor = cmds.listConnections(arnold_mat_new + '.baseColor',type='file')
                                    file_path_bColor=''.join(file_path_bColor)
                                    cmds.connectAttr(file_path_bColor + '.outColor',rman_metallic_shader + '.baseColor')
                                    metalness = cmds.getAttr(arnold_mat_new + attr )
                                    cmds.setAttr(rman_metallic_shader + '.metallic',metalness)
                                else:       
                                    diffuse_color = cmds.getAttr(arnold_mat_new + '.baseColor' )
                                    cmds.setAttr(rman_metallic_shader + '.baseColor',diffuse_color[0][0],diffuse_color[0][1],diffuse_color[0][2],type='double3')
                                    metalness = cmds.getAttr(arnold_mat_new + attr )
                                    cmds.setAttr(rman_metallic_shader + '.metallic',metalness)
                            cmds.connectAttr(rman_metallic_shader + '.resultDiffuseRGB',renderman_shader + '.diffuseColor',force=True)
                            cmds.connectAttr(rman_metallic_shader + '.resultSpecularEdgeRGB',renderman_shader + '.specularEdgeColor',force=True)
                            cmds.connectAttr(rman_metallic_shader + '.resultSpecularFaceRGB',renderman_shader + '.specularFaceColor',force=True)
                    
                        if attr == '.normalCamera' :
                            renderman_shader=''.join(renderman_shader)
                            renderman_shader_new=renderman_shader + '.bumpNormal'
                            if file_node:
                                file_path = cmds.listConnections(arnold_mat_new + attr)
                                file_path=''.join(file_path)
                                cmds.connectAttr(file_path + '.outValue',renderman_shader_new)

                    cmds.sets(sel[0], edit=True, forceElement=shading_group)

# Function to convert PxrSurface to aiStandardSurface

def convert_PxrSurface_material() :
    # get selected object and if not selected prompt user to select an object#
    sel = cmds.ls(sl=True)
    if not sel :
        cmds.confirmDialog(title='Error', message='Please select an object', button=['OK'], defaultButton='OK')
        cmds.warning("Error : Please select an object")
        return
    
    for obj in sel :
        # get the selected object's material and if not material prompt user to assign a material#
        theNodes = cmds.ls(sl = True, dag = True, s = True)
        shadeEng = cmds.listConnections(theNodes , type = 'shadingEngine')
        print(shadeEng)
        if shadeEng :
            for sg in shadeEng :
                pxr_mat = cmds.ls(cmds.listConnections(shadeEng), materials = True)
                print(pxr_mat)
                if cmds.nodeType(pxr_mat) != 'PxrSurface' :
                    cmds.confirmDialog(title='Error', message='Selected object does not have a PxrSurface material applied.', button=['OK'], defaultButton='OK')
                    cmds.warning("Error : Selected object does not have an PxrSurface material applied.")
                    return
                if pxr_mat :
                    # Create a new aiStandardSurface material
                    arnold_shader = cmds.shadingNode('aiStandardSurface', asShader=True)
                    shading_group = cmds.sets(arnold_shader, renderable=True, noSurfaceShader=True, empty=True, name=arnold_shader + 'SG')
                    cmds.connectAttr(arnold_shader + '.outColor', shading_group + '.surfaceShader', force=True)
                    components_pxrmat= ['.diffuseColor','.specularFaceColor','.specularRoughness','.metallic','.bumpNormal']

                    for attr in components_pxrmat :
                        pxr_mat_new=''.join(pxr_mat)

                        # checking each attribute and attaching them to PxrSurface
                        if(attr=='.metallic'):
                            # as explained in this - https://rmanwiki.pixar.com/display/REN24/PxrMetallicWorkflow
                            arnold_shader=''.join(arnold_shader)
                            arnold_shader_new=arnold_shader + '.metalness'
                            #print(arnold_shader_new)
                            file_paths = cmds.listConnections(pxr_mat_new+'.diffuseColor')
                            #print(file_paths)
                            try:
                                file_paths=''.join(file_paths)
                                file_paths = cmds.getAttr(file_paths+attr)
                                cmds.setAttr(arnold_shader_new,file_paths)
                            except:
                                pass
                        else:
                            value = cmds.getAttr(pxr_mat_new + attr )
                            file_node=cmds.connectionInfo(pxr_mat_new + attr, sourceFromDestination=True)
                            if attr == '.diffuseColor' or attr == '.resultDiffuseRGB':
                                arnold_shader=''.join(arnold_shader)
                                arnold_shader_new=arnold_shader + '.baseColor'
                                cmds.setAttr(arnold_shader_new,value[0][0],value[0][1],value[0][2],type='double3')
                                file_paths = cmds.listConnections(pxr_mat_new+'.diffuseColor')
                                if file_node:
                                    file_paths=''.join(file_paths)
                                    if "Metallic" in file_paths:
                                        try:
                                            file_paths = cmds.listConnections(file_paths+'.baseColor')
                                            print(file_paths)
                                            file_paths=''.join(file_paths)
                                            cmds.connectAttr(file_paths + '.outColor', arnold_shader_new)
                                        except:
                                            print("except")
                                            print(file_paths)
                                            file_paths=cmds.getAttr(file_paths +'.baseColor')
                                            cmds.setAttr(arnold_shader_new,file_paths)
                                    else:
                                        cmds.connectAttr(file_paths + '.outColor', arnold_shader_new)    
                            if attr == '.specularFaceColor' :
                                arnold_shader=''.join(arnold_shader)
                                arnold_shader_new=arnold_shader + '.specularColor'
                                cmds.setAttr(arnold_shader_new,value[0][0],value[0][1],value[0][2],type='double3')
                                if file_node:
                                    if (True):
                                        file_paths_face = cmds.getAttr('PxrMetallicWorkflow*'+'.resultSpecularFaceRGB')
                                        file_paths_edge = cmds.getAttr('PxrMetallicWorkflow*'+'.resultSpecularEdgeRGB')
                                        cmds.setAttr(arnold_shader_new,((file_paths_face[0][0]+file_paths_edge[0][0])/2),((file_paths_face[0][1]+file_paths_edge[0][1])/2),((file_paths_face[0][2]+file_paths_edge[0][2])/2),type='double3')
                            if attr == '.specularRoughness' :
                                arnold_shader=''.join(arnold_shader)
                                arnold_shader_new=arnold_shader + '.specularRoughness'
                                cmds.setAttr(arnold_shader_new,value)
                                if file_node:
                                    file_path = cmds.listConnections(pxr_mat_new + attr)
                                    file_path=''.join(file_path)
                                    cmds.connectAttr(file_path + '.outAlpha',arnold_shader_new)
                            if attr == '.bumpNormal' :
                                arnold_shader=''.join(arnold_shader)
                                arnold_shader_new=arnold_shader + '.normalCamera'
                                if file_node:
                                    file_path = cmds.listConnections(pxr_mat_new + attr)
                                    file_path=''.join(file_path)
                                    cmds.connectAttr(file_path + '.outValue',arnold_shader_new)

                    cmds.sets(sel[0], edit=True, forceElement=shading_group)


# Function to create the UI and run the functions according to the selection on radio buttons
def createUI():
    
    # Function to call the selected conversion function
    def convert_selected(conversion_group):
        selected_button = cmds.radioCollection(conversion_group, query=True, select=True)
        selected_button_f = cmds.radioButton(selected_button, query=True, label=True)
        print(f"{selected_button_f=}")
        if selected_button_f == "Arnold to Renderman (aiStandardSurface to PxrSurface)":
            convert_aiStandardSurface_material()
        elif selected_button_f == "Renderman to Arnold (PxrSurface to aiStandardSurface)":
            convert_PxrSurface_material()
    
    window_name = "Automatic_Material_Swapper"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
        
    cmds.window(window_name, title="Automatic Material Swapper : Maya",widthHeight=(500, 200))

    # Creating a radio button group to choose the conversion function
    layout=cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="Please select the object and then select the conversion function:")
    conversion_group = cmds.radioCollection()
    arnold_to_renderman_button = cmds.radioButton(label="Arnold to Renderman (aiStandardSurface to PxrSurface)")
    print(f"{arnold_to_renderman_button=}")
    renderman_to_arnold_button = cmds.radioButton(label="Renderman to Arnold (PxrSurface to aiStandardSurface)")
    print(f"{renderman_to_arnold_button=}")

    # Creating a button to trigger the selected conversion function
    cmds.button(label="Convert", command=lambda *args: convert_selected(conversion_group))
    cmds.showWindow(window_name)

# Calling the createUI function
createUI()