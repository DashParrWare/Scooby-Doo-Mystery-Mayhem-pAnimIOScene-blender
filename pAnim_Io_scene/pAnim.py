from struct import unpack, pack
import bpy
import os
import mathutils
import math

entrysize = []
entryBoneData = []
positionx = []
positiony = []
positionz = []
rotationx = []
rotationy = []
rotationz = []
rotations=[]

#EXPORT SOON

def ReadpAnim(f, filepath):
    
    ob = bpy.context.object
    FileSize = unpack(">I", f.read(4))[0]
    fourthousandnintysix = unpack(">H", f.read(2))[0]
    compression = unpack(">H", f.read(2))[0]
    framerate = unpack(">f", f.read(4))[0]
    boneCount = unpack("B", f.read(1))[0]
    type1 = unpack("B", f.read(1))[0]
    type2 = unpack("B", f.read(1))[0]
    type3 = unpack("B", f.read(1))[0]

    bpy.context.scene.render.fps = 30
    bpy.context.scene.render.fps_base = 1
    bpy.context.scene.unit_settings.system_rotation = 'RADIANS'

    rotx_index = 0

    #Velma bone 39
    clean_rotations_x = -0.098094

    

    for pbone in ob.pose.bones:
        pbone.rotation_mode = "XYZ"

    for i in range(boneCount):
        fourthousandnintysix_off = unpack(">H", f.read(2))[0]
        bone_id = unpack(">H", f.read(2))[0]
        maximum_keyframe_id = unpack(">H", f.read(2))[0]
        size_off = unpack(">H", f.read(2))[0]
        for i in range(maximum_keyframe_id):
            fourthousandnintysix_on = unpack(">H", f.read(2))[0]
            key_index = unpack(">H", f.read(2))[0]
            unk = unpack(">H", f.read(2))[0]
            size_on = unpack(">H", f.read(2))[0]
            entrysize.append([key_index, size_on, bone_id])
        
    for i, entry_size in enumerate(entrysize):
        if entry_size[1]:
            startFrame = unpack(">f", f.read(4))[0]
            endFrame = unpack(">f", f.read(4))[0]
            bone_num = unpack("B", f.read(1))[0]
            type1_ = f.read(3)
            #16 bytes
            if type1_ == b"\x01\x00\x01":
                rotx_index += 1
                if entry_size[0] == 0:
                    XScale = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].scale[0] = XScale
                elif entry_size[0] == 1:
                    YScale = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].scale[1] = YScale
                elif entry_size[0] == 2:
                    ZScale = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].scale[2] = ZScale
                elif entry_size[0] == 3:
                    XPos = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].location[0] = XPos / compression
                elif entry_size[0] == 4:
                    YPos = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].location[1] = YPos / compression
                elif entry_size[0] == 5:
                    ZPos = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].location[2] = ZPos / compression
                elif entry_size[0] == 6:
                    XRot = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].rotation_euler[0] = XRot
                        
                elif entry_size[0] == 7:
                    YRot = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].rotation_euler[1] = YRot
                elif entry_size[0] == 8:
                    ZRot = unpack(">f", f.read(4))[0]
                    if entry_size[2]:
                        ob.pose.bones[entry_size[2]].rotation_euler[2] = ZRot
            elif type1_ == b"\x02\x00\x01":
                pass
            elif type1_ == b"\x04\x00\x01":
                pass
            elif type1_ == b"\x04\x00\x02":
                pass
            elif type1_ == b"\x04\x00\x03":
                pass
            elif type1_ == b"\x04\x00\x04":
                pass
            elif type1_ == b"\x04\x00\x05":
                pass
            elif type1_ == b"\x04\x00\x06":
                pass
            elif type1_ == b"\x04\x00\x07":
                pass
            elif type1_ == b"\x04\x00\x08":
                pass
            elif type1_ == b"\x04\x00\x09":
                pass
            elif type1_ == b"\x04\x00\x0A":
                pass
            elif type1_ == b"\x04\x00\x0B":
                pass
            elif type1_ == b"\x04\x00\x0C":
                pass
            elif type1_ == b"\x04\x00\x11":
                pass
            elif type1_ == b"\x04\x00\x12":
                pass
            elif type1_ == b"\x04\x00\x13":
                pass
            elif type1_ == b"\x04\x00\x14":
                pass
            elif type1_ == b"\x04\x00\x16":
                pass
            elif type1_ == b"\x04\x00\x17":
                pass
            elif type1_ == b"\x04\x00\x1A":
                pass
            elif type1_ == b"\x04\x00\x1C":
                pass
            elif type1_ == b"\x04\x00\x1D":
                pass
            elif type1_ == b"\x04\x00\x1E":
                pass
            elif type1_ == b"\x04\x00\x22":
                pass
            elif type1_ == b"\x04\x00\x26":
                pass
            elif type1_ == b"\x04\x00\x28":
                pass
            elif type1_ == b"\x04\x00\x2C":
                pass
            elif type1_ == b"\x04\x00\x2D":
                pass

def WritepAnimGameCube(f):
    ob = bpy.context.object
    f.write(pack(">I", 16+8*len(ob.pose.bones)))
    f.write(pack(">H", 4096))
    f.write(pack(">H", 0))
    f.write(pack("B", len(ob.pose.bones)))
    f.write(pack("B", 0))
    f.write(pack("B", 0))
    f.write(pack("B", 0))
    bone_id = 0
    total_of_keyframe = 0
    for pbone in ob.pose.bones:
        f.write(pack(">H", 0))
        f.write(pack(">H", bone_id))
        f.write(pack(">H", total_of_keyframe))
        f.write(pack(">H", 0))
        bone_id+=1

def WritepAnimPS2(f):
    ob = bpy.context.object
    f.write(pack(">I", 16))
    

def pAnim_importing(filepath):
    with open(filepath, "rb") as f:
        ReadpAnim(f, filepath)
        
    
