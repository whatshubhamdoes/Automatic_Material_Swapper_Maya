import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.mel as mel
import os
import sys

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
        if shadeEng :
            for sg in shadeEng :
                arnold_mat = cmds.ls(cmds.listConnections(shadeEng), materials = True)
                if cmds.nodeType(arnold_mat) != 'aiStandardSurface':
                    cmds.confirmDialog(title='Error', message='Selected object does not have an Arnold Standard Surface material applied.', button=['OK'], defaultButton='OK')
                    cmds.warning("Error : Selected object does not have an Arnold Standard Surface material applied.")
                    return
                #print(arnold_mat)
                if arnold_mat :
                    # Create a new RenderMan PxrSurface material
                    renderman_shader = cmds.shadingNode('PxrSurface', asShader=True)
                    #print(renderman_shader)
                    shading_group = cmds.sets(renderman_shader, renderable=True, noSurfaceShader=True, empty=True, name=renderman_shader + 'SG')
                    #print(shading_group)
                    cmds.connectAttr(renderman_shader + '.outColor', shading_group + '.surfaceShader', force=True)
                    #renderman_attributes=cmds.listAttr(renderman_shader)
                    #print(renderman_attributes)

                    #components_arnold_og= ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership', 'outColor', 'outColorR', 'outColorG', 'outColorB', 'outAlpha', 'outTransparency', 'outTransparencyR', 'outTransparencyG', 'outTransparencyB', 'normalCamera', 'normalCameraX', 'normalCameraY', 'normalCameraZ', 'aiEnableMatte', 'aiMatteColor', 'aiMatteColorR', 'aiMatteColorG', 'aiMatteColorB', 'aiMatteColorA', 'base', '.baseColor', 'baseColorR', 'baseColorG', 'baseColorB', 'diffuseRoughness', 'specular', 'specularColor', 'specularColorR', 'specularColorG', 'specularColorB', 'specularRoughness', 'specularIOR', 'specularAnisotropy', 'specularRotation', 'metalness', 'transmission', 'transmissionColor', 'transmissionColorR', 'transmissionColorG', 'transmissionColorB', 'transmissionDepth', 'transmissionScatter', 'transmissionScatterR', 'transmissionScatterG', 'transmissionScatterB', 'transmissionScatterAnisotropy', 'transmissionDispersion', 'transmissionExtraRoughness', 'transmitAovs', 'subsurface', 'subsurfaceColor', 'subsurfaceColorR', 'subsurfaceColorG', 'subsurfaceColorB', 'subsurfaceRadius', 'subsurfaceRadiusR', 'subsurfaceRadiusG', 'subsurfaceRadiusB', 'subsurfaceScale', 'subsurfaceAnisotropy', 'subsurfaceType', 'sheen', 'sheenColor', 'sheenColorR', 'sheenColorG', 'sheenColorB', 'sheenRoughness', 'thinWalled', 'tangent', 'tangentX', 'tangentY', 'tangentZ', 'coat', 'coatColor', 'coatColorR', 'coatColorG', 'coatColorB', 'coatRoughness', 'coatIOR', 'coatAnisotropy', 'coatRotation', 'coatNormal', 'coatNormalX', 'coatNormalY', 'coatNormalZ', 'thinFilmThickness', 'thinFilmIOR', 'emission', 'emissionColor', 'emissionColorR', 'emissionColorG', 'emissionColorB', 'opacity', 'opacityR', 'opacityG', 'opacityB', 'caustics', 'internalReflections', 'exitToBackground', 'indirectDiffuse', 'indirectSpecular', 'dielectricPriority', 'aovId1', 'id1', 'id1R', 'id1G', 'id1B', 'aovId2', 'id2', 'id2R', 'id2G', 'id2B', 'aovId3', 'id3', 'id3R', 'id3G', 'id3B', 'aovId4', 'id4', 'id4R', 'id4G', 'id4B', 'aovId5', 'id5', 'id5R', 'id5G', 'id5B', 'aovId6', 'id6', 'id6R', 'id6G', 'id6B', 'aovId7', 'id7', 'id7R', 'id7G', 'id7B', 'aovId8', 'id8', 'id8R', 'id8G', 'id8B']
                    components_arnold= ['.baseColor']
                    #print(components_arnold)
                    """components_renderman_og = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership', 'inputMaterial', 'diffuseGain', 'diffuseColor', 'diffuseColorR', 'diffuseColorG', 'diffuseColorB', 'diffuseRoughness', 'diffuseExponent', 'diffuseBumpNormal', 'diffuseBumpNormalX', 'diffuseBumpNormalY', 'diffuseBumpNormalZ', 'diffuseDoubleSided', 'diffuseBackUseDiffuseColor', 'diffuseBackColor', 'diffuseBackColorR', 'diffuseBackColorG', 'diffuseBackColorB', 'diffuseTransmitGain', 'diffuseTransmitColor', 'diffuseTransmitColorR', 'diffuseTransmitColorG', 'diffuseTransmitColorB', 'specularFresnelMode', 'specularFaceColor', 'specularFaceColorR', 'specularFaceColorG', 'specularFaceColorB', 'specularEdgeColor', 'specularEdgeColorR', 'specularEdgeColorG', 'specularEdgeColorB', 'specularFresnelShape', 'specularIor', 'specularIorR', 'specularIorG', 'specularIorB', 'specularExtinctionCoeff', 'specularExtinctionCoeffR', 'specularExtinctionCoeffG', 'specularExtinctionCoeffB', 'specularRoughness', 'specularModelType', 'specularAnisotropy', 'specularAnisotropyDirection', 'specularAnisotropyDirectionX', 'specularAnisotropyDirectionY', 'specularAnisotropyDirectionZ', 'specularBumpNormal', 'specularBumpNormalX', 'specularBumpNormalY', 'specularBumpNormalZ', 'specularDoubleSided', 'roughSpecularFresnelMode', 'roughSpecularFaceColor', 'roughSpecularFaceColorR', 'roughSpecularFaceColorG', 'roughSpecularFaceColorB', 'roughSpecularEdgeColor', 'roughSpecularEdgeColorR', 'roughSpecularEdgeColorG', 'roughSpecularEdgeColorB', 'roughSpecularFresnelShape', 'roughSpecularIor', 'roughSpecularIorR', 'roughSpecularIorG', 'roughSpecularIorB', 'roughSpecularExtinctionCoeff', 'roughSpecularExtinctionCoeffR', 'roughSpecularExtinctionCoeffG', 'roughSpecularExtinctionCoeffB', 'roughSpecularRoughness', 'roughSpecularModelType', 'roughSpecularAnisotropy', 'roughSpecularAnisotropyDirection', 'roughSpecularAnisotropyDirectionX', 'roughSpecularAnisotropyDirectionY', 'roughSpecularAnisotropyDirectionZ', 'roughSpecularBumpNormal', 'roughSpecularBumpNormalX', 'roughSpecularBumpNormalY', 'roughSpecularBumpNormalZ', 'roughSpecularDoubleSided', 'clearcoatFresnelMode', 'clearcoatFaceColor', 'clearcoatFaceColorR', 'clearcoatFaceColorG', 'clearcoatFaceColorB', 'clearcoatEdgeColor', 'clearcoatEdgeColorR', 'clearcoatEdgeColorG', 'clearcoatEdgeColorB', 'clearcoatFresnelShape', 'clearcoatIor', 'clearcoatIorR', 'clearcoatIorG', 'clearcoatIorB', 'clearcoatExtinctionCoeff', 'clearcoatExtinctionCoeffR', 'clearcoatExtinctionCoeffG', 'clearcoatExtinctionCoeffB', 'clearcoatThickness', 'clearcoatAbsorptionTint', 'clearcoatAbsorptionTintR', 'clearcoatAbsorptionTintG', 'clearcoatAbsorptionTintB', 'clearcoatRoughness', 'clearcoatModelType', 'clearcoatAnisotropy', 'clearcoatAnisotropyDirection', 'clearcoatAnisotropyDirectionX', 'clearcoatAnisotropyDirectionY', 'clearcoatAnisotropyDirectionZ', 'clearcoatBumpNormal', 'clearcoatBumpNormalX', 'clearcoatBumpNormalY', 'clearcoatBumpNormalZ', 'clearcoatDoubleSided', 'specularEnergyCompensation', 'clearcoatEnergyCompensation', 'iridescenceFaceGain', 'iridescenceEdgeGain', 'iridescenceFresnelShape', 'iridescenceMode', 'iridescencePrimaryColor', 'iridescencePrimaryColorR', 'iridescencePrimaryColorG', 'iridescencePrimaryColorB', 'iridescenceSecondaryColor', 'iridescenceSecondaryColorR', 'iridescenceSecondaryColorG', 'iridescenceSecondaryColorB', 'iridescenceRoughness', 'iridescenceAnisotropy', 'iridescenceAnisotropyDirection', 'iridescenceAnisotropyDirectionX', 'iridescenceAnisotropyDirectionY', 'iridescenceAnisotropyDirectionZ', 'iridescenceBumpNormal', 'iridescenceBumpNormalX', 'iridescenceBumpNormalY', 'iridescenceBumpNormalZ', 'iridescenceCurve', 'iridescenceScale', 'iridescenceFlip', 'iridescenceThickness', 'iridescenceDoubleSided', 'fuzzGain', 'fuzzColor', 'fuzzColorR', 'fuzzColorG', 'fuzzColorB', 'fuzzConeAngle', 'fuzzBumpNormal', 'fuzzBumpNormalX', 'fuzzBumpNormalY', 'fuzzBumpNormalZ', 'fuzzDoubleSided', 'subsurfaceType', 'subsurfaceGain', 'subsurfaceColor', 'subsurfaceColorR', 'subsurfaceColorG', 'subsurfaceColorB', 'subsurfaceDmfp', 'subsurfaceDmfpColor', 'subsurfaceDmfpColorR', 'subsurfaceDmfpColorG', 'subsurfaceDmfpColorB', 'shortSubsurfaceGain', 'shortSubsurfaceColor', 'shortSubsurfaceColorR', 'shortSubsurfaceColorG', 'shortSubsurfaceColorB', 'shortSubsurfaceDmfp', 'longSubsurfaceGain', 'longSubsurfaceColor', 'longSubsurfaceColorR', 'longSubsurfaceColorG', 'longSubsurfaceColorB', 'longSubsurfaceDmfp', 'subsurfaceDirectionality', 'subsurfaceBleed', 'subsurfaceDiffuseBlend', 'subsurfaceResolveSelfIntersections', 'subsurfaceIor', 'subsurfacePostTint', 'subsurfacePostTintR', 'subsurfacePostTintG', 'subsurfacePostTintB', 'subsurfaceDiffuseSwitch', 'subsurfaceDoubleSided', 'subsurfaceTransmitGain', 'considerBackside', 'continuationRayMode', 'maxContinuationHits', 'followTopology', 'subsurfaceSubset', 'singlescatterGain', 'singlescatterColor', 'singlescatterColorR', 'singlescatterColorG', 'singlescatterColorB', 'singlescatterMfp', 'singlescatterMfpColor', 'singlescatterMfpColorR', 'singlescatterMfpColorG', 'singlescatterMfpColorB', 'singlescatterDirectionality', 'singlescatterIor', 'singlescatterBlur', 'singlescatterDirectGain', 'singlescatterDirectGainTint', 'singlescatterDirectGainTintR', 'singlescatterDirectGainTintG', 'singlescatterDirectGainTintB', 'singlescatterDoubleSided', 'singlescatterConsiderBackside', 'singlescatterContinuationRayMode', 'singlescatterMaxContinuationHits', 'singlescatterDirectGainMode', 'singlescatterSubset', 'irradianceTint', 'irradianceTintR', 'irradianceTintG', 'irradianceTintB', 'irradianceRoughness', 'unitLength', 'refractionGain', 'reflectionGain', 'refractionColor', 'refractionColorR', 'refractionColorG', 'refractionColorB', 'glassRoughness', 'glassRefractionRoughness', 'glassRefraction2Roughness', 'glassRefraction2Blend', 'glassRefraction2Tint', 'glassRefraction2TintR', 'glassRefraction2TintG', 'glassRefraction2TintB', 'glassAnisotropy', 'glassAnisotropyDirection', 'glassAnisotropyDirectionX', 'glassAnisotropyDirectionY', 'glassAnisotropyDirectionZ', 'glassBumpNormal', 'glassBumpNormalX', 'glassBumpNormalY', 'glassBumpNormalZ', 'glassIor', 'mwWalkable', 'mwIor', 'thinGlass', 'ignoreFresnel', 'ignoreAccumOpacity', 'blocksVolumes', 'volumeAggregate', 'volumeAggregateName', 'ssAlbedo', 'ssAlbedoR', 'ssAlbedoG', 'ssAlbedoB', 'extinction', 'extinctionR', 'extinctionG', 'extinctionB', 'g', 'g1', 'blend', 'volumeGlow', 'volumeGlowR', 'volumeGlowG', 'volumeGlowB', 'maxExtinction', 'multiScatter', 'enableOverlappingVolumes', 'glowGain', 'glowColor', 'glowColorR', 'glowColorG', 'glowColorB', 'bumpNormal', 'bumpNormalX', 'bumpNormalY', 'bumpNormalZ', 'shadowBumpTerminator', 'shadowColor', 'shadowColorR', 'shadowColorG', 'shadowColorB', 'shadowMode', 'presence', 'presenceCached', 'mwStartable', 'roughnessMollificationClamp', 'userColor', 'userColorR', 'userColorG', 'userColorB', 'utilityPattern', 'outColor', 'outColorR', 'outColorG', 'outColorB', 'outGlowColor', 'outGlowColorR', 'outGlowColorG', 'outGlowColorB', 'outMatteOpacity', 'outMatteOpacityR', 'outMatteOpacityG', 'outMatteOpacityB', 'outTransparency', 'outTransparencyR', 'outTransparencyG', 'outTransparencyB', 'attributeAliasList']
                    components_renderman = ['diffuseColor']
                    print(components_renderman)"""

                    for attr in components_arnold :
                        arnold_mat_new=''.join(arnold_mat)
                        value = cmds.getAttr(arnold_mat_new + attr )
                        #print(arnold_mat_new+attr)
                        file_node=cmds.connectionInfo(arnold_mat_new + attr, sourceFromDestination=True)
                        #print(file_node)
                        #print(value)
                        #print(attr)
                        #print(arnold_mat)
                        #print(arnold_mat_new)
                        if attr == '.baseColor' :
                            renderman_shader=''.join(renderman_shader)
                            renderman_shader_new=renderman_shader + '.diffuseColor'
                            cmds.setAttr(renderman_shader_new,value[0][0],value[0][1],value[0][2],type='double3')
                            if file_node:
                                # Get the file texture path and set it on PxrSurface1
                                #file_path = cmds.getAttr(arnold_mat_new + attr + '.fileTextureName')
                                file_path = cmds.listConnections(arnold_mat_new + attr,type='file')
                                #print(file_path)
                                file_path=''.join(file_path)
                                #print(cmds.getAttr(file_path + '.outColor'))
                                cmds.connectAttr(file_path + '.outColor',renderman_shader_new)
                            #print(renderman_shader)
                            #print(shading_group)
                    
                    cmds.sets(sel[0], edit=True, forceElement=shading_group)
    
convert_aiStandardSurface_material()