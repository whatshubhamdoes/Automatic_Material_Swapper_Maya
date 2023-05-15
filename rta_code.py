import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.mel as mel
import os
import sys

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
    

    
convert_PxrSurface_material()