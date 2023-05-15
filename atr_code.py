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
    

    
convert_aiStandardSurface_material()