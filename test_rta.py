import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import unittest
from rta_code import convert_PxrSurface_material

class TestConvertMaterial(unittest.TestCase):
    def setUp(self):
        self.selected_objects = cmds.ls(selection=True)

    def test_convert_PxrSurface_material(self):
        # Create a test PxrSurface material and assign it to a sphere
        cmds.polySphere()
        mat = cmds.shadingNode('PxrSurface', asShader=True)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=mat+'SG')
        cmds.connectAttr(mat+'.outColor', sg+'.surfaceShader', force=True)
        rman_metallic_shader = cmds.shadingNode('PxrMetallicWorkflow', asShader=True)
        cmds.connectAttr(rman_metallic_shader+'.resultDiffuseRGB',mat+'.diffuseColor',force=True)
        cmds.connectAttr(rman_metallic_shader+'.resultSpecularEdgeRGB',mat+'.specularEdgeColor',force=True)
        cmds.connectAttr(rman_metallic_shader+'.resultSpecularFaceRGB',mat+'.specularFaceColor',force=True)
        cmds.select('pSphere1')
        cmds.sets(forceElement=sg)
        cmds.setAttr(rman_metallic_shader+'.baseColor', 1, 0, 0, type='double3')
        cmds.setAttr(mat+'.specularRoughness', 0.5)
        cmds.setAttr(rman_metallic_shader+'.metallic', 0)
        cmds.setAttr(mat+'.bumpNormal', 1, 0, 0, type='double3')
        
        # Run the function
        convert_PxrSurface_material()

        # Check if the new aiStandard Surface material was created and connected correctly
        new_mat = cmds.ls(type='aiStandardSurface')
        self.assertTrue(new_mat)
        new_sg = cmds.listConnections(new_mat, type='shadingEngine')
        self.assertTrue(new_sg)
        
        # Check if the new material's attributes were set correctly
        self.assertEqual(cmds.getAttr(new_mat[0]+'.baseColor'), [(1.0, 0.0, 0.0)])
        self.assertEqual(cmds.getAttr(new_mat[0]+'.specularColor'), [(0.51999999955, 0.51999999955, 0.51999999955)])
        self.assertEqual(cmds.getAttr(new_mat[0]+'.specularRoughness'), 0.5)
        self.assertEqual(cmds.getAttr(new_mat[0]+'.metallic'), 0)
        self.assertEqual(cmds.getAttr(new_mat[0]+'.normalCamera'), [(1.0, 0.0, 0.0)])
        
    def tearDown(self):
        cmds.select(self.selected_objects, replace=True)

if __name__ == '__main__':
    unittest.main()
