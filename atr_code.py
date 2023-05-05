import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import maya._OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

def convert_diffuse_material() :
    # get selected object and if not selected prompt user to select an object#
    sel = cmds.ls(sl=True)
    if not sel :
        cmds.confirmDialog(title='Error', message='Please select an object', button=['OK'], defaultButton='OK')
        return
    # get the selected object's material and if not material prompt user to assign a material#
    theNodes = cmds.ls(sl = True, dag = True, s = True)
    shadeEng = cmds.listConnections(theNodes , type = 'shadingEngine')
    arnold_mat = cmds.ls(cmds.listConnections(shadeEng), materials = True)
    if cmds.nodeType(arnold_mat) != 'aiStandardSurface':
        cmds.confirmDialog(title='Error', message='Selected object does not have an Arnold Standard Surface material applied.', button=['OK'], defaultButton='OK')
        cmds.warning("Selected object does not have an Arnold Standard Surface material applied.")
        return
    print(arnold_mat)
    
    # create a renderman shader and connect the arnold material attributes to the renderman shader attributes#
    renderman_shader = cmds.shadingNode('PxrDiffuse', asShader=True)
    cmds.rename(renderman_shader, 'rendermanDiffuse')
    shading_group = cmds.sets(renderman_shader, renderable=True, noSurfaceShader=True, empty=True, name=renderman_shader + 'SG')
    cmds.connectAttr(renderman_shader + '.outColor', shading_group + '.surfaceShader', force=True)

    arnold_color = cmds.getAttr(arnold_mat + '.baseColor')[0]
    cmds.setAttr(renderman_shader + '.diffuseColor', arnold_color[0], arnold_color[1], arnold_color[2], type='float3')

    #assign the renderman_shader to the selected object#
    cmds.select(sel[0])
    cmds.hyperShade(assign=renderman_shader)

    print("Arnold Standard Surface material successfully converted to RenderMan PxRDiffuse.")

convert_diffuse_material()
    



