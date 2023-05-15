import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import unittest
from atr_code import convert_aiStandardSurface_material


class TestConvertMaterial(unittest.TestCase):
    def setUp(self):
        self.selected_objects = cmds.ls(selection=True)

    def test_convert_aiStandardSurface_material(self):
        # Create a test aiStandardSurface material and assign it to a sphere
        cmds.polySphere()
        mat = cmds.shadingNode('aiStandardSurface', asShader=True)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=mat+'SG')
        cmds.connectAttr(mat+'.outColor', sg+'.surfaceShader', force=True)
        cmds.select('pSphere1')
        cmds.sets(forceElement=sg)
        cmds.setAttr(mat+'.baseColor', 1, 0, 0, type='double3')
        cmds.setAttr(mat+'.specularColor', 0, 1, 0, type='double3')
        cmds.setAttr(mat+'.specularRoughness', 0.5)
        cmds.setAttr(mat+'.metalness', 1)
        cmds.setAttr(mat+'.normalCamera', 1, 0, 0, type='double3')
        
        # Run the function
        convert_aiStandardSurface_material()

        # Check if the new RenderMan PxrSurface material was created and connected correctly
        new_mat = cmds.ls(type='PxrSurface')
        self.assertTrue(new_mat)
        new_sg = cmds.listConnections(new_mat, type='shadingEngine')
        self.assertTrue(new_sg)
        
        # Check if the new material's attributes were set correctly
        self.assertEqual(cmds.getAttr('PxrMetallicWorkflow*'+'.baseColor'), [(1.0, 0.0, 0.0)])
        self.assertEqual(cmds.getAttr('PxrMetallicWorkflow*'+'.resultSpecularFaceRGB'), [(0.03999999910593033, 0.03999999910593033, 0.03999999910593033)])
        self.assertEqual(cmds.getAttr('PxrMetallicWorkflow*'+'.resultSpecularEdgeRGB'), [(1, 1, 1)])
        self.assertEqual(cmds.getAttr(new_mat[0]+'.specularRoughness'), 0.5)
        self.assertEqual(cmds.getAttr('PxrMetallicWorkflow*'+'.metallic'), 1)
        
    def tearDown(self):
        cmds.select(self.selected_objects, replace=True)

if __name__ == '__main__':
    unittest.main()
