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
    compression = unpack(">I", f.read(4))[0]>>16
    framerate = unpack(">f", f.read(4))[0]
    boneCount = unpack("B", f.read(1))[0]
    type1 = unpack("B", f.read(1))[0]
    type2 = unpack("B", f.read(1))[0]
    type3 = unpack("B", f.read(1))[0]

    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_current = 0
    bpy.context.scene.frame_end = int(framerate*30)

    bpy.context.scene.render.fps = 30
    bpy.context.scene.render.fps_base = 1
    bpy.context.scene.unit_settings.system_rotation = 'RADIANS'
    #bpy.context.scene.unit_settings.system_rotation = 'DEGREES'

    index = 2

    magic_index_num_1 = 10

    bone_i_22 = 20

    

    for pbone in ob.pose.bones:
        pbone.rotation_mode = "XYZ"

    for i in range(boneCount):
        compression_off = unpack(">H", f.read(2))[0]
        bone_id = unpack(">H", f.read(2))[0]
        maximum_keyframe_id = unpack(">H", f.read(2))[0]
        size_off = unpack(">H", f.read(2))[0]
        for i in range(maximum_keyframe_id):
            compression_on = unpack(">H", f.read(2))[0]
            key_index = unpack(">H", f.read(2))[0]
            unk = unpack(">H", f.read(2))[0]
            size_on = unpack(">H", f.read(2))[0]
            entrysize.append([key_index, size_on, bone_id, compression_on])
        
    for i, entry_size in enumerate(entrysize):
        if entry_size[1]:
            startFrame = unpack(">f", f.read(4))[0]
            endFrame = unpack(">f", f.read(4))[0]
            type1_ = f.read(4)
            #16 bytes
            if type1_ == b"\x00\x01\x00\x01":
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
                    if entry_size[2] == index:
                        ob.pose.bones[entry_size[2]].location[0] = XPos
                        index+=1
                    for i in range(1):
                        if entry_size[2] == 0:
                            ob.pose.bones[entry_size[2]].location[0] = XPos
                    for i in range(1):
                        if entry_size[2] == 1:
                            ob.pose.bones[entry_size[2]].location[0] = XPos
                elif entry_size[0] == 4:
                    YPos = unpack(">f", f.read(4))[0]
                    if entry_size[2] == index:
                        ob.pose.bones[entry_size[2]].location[1] = YPos
                        index+=1
                    for i in range(1):
                        if entry_size[2] == 0:
                            ob.pose.bones[entry_size[2]].location[1] = YPos
                    for i in range(1):
                        if entry_size[2] == 1:
                            ob.pose.bones[entry_size[2]].location[1] = YPos
                elif entry_size[0] == 5:
                    ZPos = unpack(">f", f.read(4))[0]
                    if entry_size[2] == index:
                        ob.pose.bones[entry_size[2]].location[2] = ZPos
                        index+=1
                    for i in range(1):
                        if entry_size[2] == 0:
                            ob.pose.bones[entry_size[2]].location[2] = ZPos
                    for i in range(1):
                        if entry_size[2] == 1:
                            ob.pose.bones[entry_size[2]].location[2] = ZPos
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
                #startframe = unpack(">f", f.read(4))[0]
                #start = int(startframe*30)
                pass
                
            elif type1_ == b"\x00\x04\x00\x01":
                pass
            elif type1_ == b"\x00\x04\x00\x02":
                pass
            elif type1_ == b"\x33\x04\x00\x02":
                if entry_size[0] == 0:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        XScale = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].scale[0] = XScale
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="scale", index=entry_size[0], frame=start)
                elif entry_size[0] == 1:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        YScale = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].scale[1] = YScale
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="scale", index=entry_size[0], frame=start)
                elif entry_size[0] == 2:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        ZScale = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].scale[2] = ZScale
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="scale", index=entry_size[0], frame=start)
                elif entry_size[0] == 3:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        XPos = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[0] = XPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)
                elif entry_size[0] == 4:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        YPos = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[1] = YPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)
                elif entry_size[0] == 5:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        ZPos = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[2] = ZPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)

                elif entry_size[0] == 6:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        XRot = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].rotation_euler[0] = XRot
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)
                elif entry_size[0] == 7:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        YRot = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].rotation_euler[1] = YRot
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)
                elif entry_size[0] == 8:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        ZRot = unpack(">f", f.read(4))[0] / 10000000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].rotation_euler[2] = ZRot
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)

            elif type1_ == b"\x33\x04\x00\x03":
                if entry_size[0] == 0:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        XScale = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].scale[0] = XScale
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="scale", index=entry_size[0], frame=start)
                elif entry_size[0] == 1:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        YScale = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].scale[1] = YScale
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="scale", index=entry_size[0], frame=start)
                elif entry_size[0] == 2:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        ZScale = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].scale[2] = ZScale
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="scale", index=entry_size[0], frame=start)
                elif entry_size[0] == 3:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        XPos = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[0] = XPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)
                elif entry_size[0] == 4:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        YPos = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[1] = YPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)
                elif entry_size[0] == 5:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        ZPos = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[2] = ZPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)

                elif entry_size[0] == 6:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        XRot = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].rotation_euler[0] = XRot
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)
                elif entry_size[0] == 7:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        YRot = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].rotation_euler[1] = YRot
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)
                elif entry_size[0] == 8:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        ZRot = unpack(">f", f.read(4))[0] / 1000000.0
                        unk = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].rotation_euler[2] = ZRot
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)
                
            elif type1_ == b"\x00\x04\x00\x04":
                if entry_size[0] == 4:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        YPos = unpack(">f", f.read(4))[0] / 1000000.0
                        unknown = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[1] = YPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)
                elif entry_size[0] == 5:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        ZPos = unpack(">f", f.read(4))[0] / 1000000.0
                        unknown = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].location[2] = ZPos
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)

                elif entry_size[0] == 6:
                    
                    for i in range(int(framerate*30)):
                        startframe = unpack(">f", f.read(4))[0]
                        start = int(startframe*30)
                        XRot = unpack(">f", f.read(4))[0] / 1000000.0
                        unknown = unpack(">f", f.read(4))[0]
                        if entry_size[2]:
                            
                            ob.pose.bones[entry_size[2]].rotation_euler[0] = XRot
                            ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)
                elif type1_ == b"\x33\x04\x00\x04":
                    if entry_size[0] == 3:
                        
                        for i in range(int(framerate*30)):
                            startframe = unpack(">f", f.read(4))[0]
                            start = int(startframe*30)
                            XPos = unpack(">f", f.read(4))[0] / 1000000.0
                            unknown = unpack(">f", f.read(4))[0]
                            if entry_size[2]:
                                
                                ob.pose.bones[entry_size[2]].location[0] = XPos
                                ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)
                    elif entry_size[0] == 4:
                        
                        for i in range(int(framerate*30)):
                            startframe = unpack(">f", f.read(4))[0]
                            start = int(startframe*30)
                            YPos = unpack(">f", f.read(4))[0] / 1000000.0
                            unknown = unpack(">f", f.read(4))[0]
                            if entry_size[2]:
                                
                                ob.pose.bones[entry_size[2]].location[1] = YPos
                                ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)
                    elif entry_size[0] == 5:
                        
                        for i in range(int(framerate*30)):
                            startframe = unpack(">f", f.read(4))[0]
                            start = int(startframe*30)
                            ZPos = unpack(">f", f.read(4))[0] / 1000000.0
                            unknown = unpack(">f", f.read(4))[0]
                            if entry_size[2]:
                                
                                ob.pose.bones[entry_size[2]].location[2] = ZPos
                                ob.pose.bones[entry_size[2]].keyframe_insert(data_path="location", index=entry_size[0]-3, frame=start)

                    elif entry_size[0] == 6:
                        
                        for i in range(int(framerate*30)):
                            startframe = unpack(">f", f.read(4))[0]
                            start = int(startframe*30)
                            XRot = unpack(">f", f.read(4))[0] / 1000000.0
                            unknown = unpack(">f", f.read(4))[0]
                            if entry_size[2]:
                                
                                ob.pose.bones[entry_size[2]].rotation_euler[0] = XRot
                                ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)

                    elif entry_size[0] == 7:
                        
                        for i in range(int(framerate*30)):
                            startframe = unpack(">f", f.read(4))[0]
                            start = int(startframe*30)
                            YRot = unpack(">f", f.read(4))[0] / 1000000.0
                            unknown = unpack(">f", f.read(4))[0]
                            if entry_size[2]:
                                
                                ob.pose.bones[entry_size[2]].rotation_euler[1] = YRot
                                ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)

                    elif entry_size[0] == 8:
                        
                        for i in range(int(framerate*30)):
                            startframe = unpack(">f", f.read(4))[0]
                            start = int(startframe*30)
                            ZRot = unpack(">f", f.read(4))[0] / 1000000.0
                            unknown = unpack(">f", f.read(4))[0]
                            if entry_size[2]:
                                
                                ob.pose.bones[entry_size[2]].rotation_euler[2] = ZRot
                                ob.pose.bones[entry_size[2]].keyframe_insert(data_path="rotation_euler", index=entry_size[0]-6, frame=start)
            elif type1_ == b"\x00\x04\x00\x05":
                pass
            elif type1_ == b"\x00\x04\x00\x06":
                pass
            elif type1_ == b"\x00\x04\x00\x07":
                pass
            elif type1_ == b"\x00\x04\x00\x08":
                pass
            elif type1_ == b"\x00\x04\x00\x09":
                pass
            elif type1_ == b"\x00\x04\x00\x0A":
                pass
            elif type1_ == b"\x00\x04\x00\x0B":
                pass
            elif type1_ == b"\x00\x04\x00\x0C":
                pass
            elif type1_ == b"\x00\x04\x00\x11":
                pass
            elif type1_ == b"\x00\x04\x00\x12":
                pass
            elif type1_ == b"\x00\x04\x00\x13":
                pass
            elif type1_ == b"\x00\x04\x00\x14":
                pass
            elif type1_ == b"\x00\x04\x00\x16":
                pass
            elif type1_ == b"\x00\x04\x00\x17":
                pass
            elif type1_ == b"\x00\x04\x00\x1A":
                pass
            elif type1_ == b"\x00\x04\x00\x1C":
                pass
            elif type1_ == b"\x00\x04\x00\x1D":
                pass
            elif type1_ == b"\x00\x04\x00\x1E":
                pass
            elif type1_ == b"\x00\x04\x00\x22":
                pass
            elif type1_ == b"\x00\x04\x00\x26":
                pass
            elif type1_ == b"\x00\x04\x00\x28":
                pass
            elif type1_ == b"00\x04\x00\x2C":
                pass
            elif type1_ == b"00\x04\x00\x2D":
                pass

def WritepAnimGameCube(f):
    ob = bpy.context.object
    f.write(pack(">I", 16+8*len(ob.pose.bones)))
    f.write(pack(">I", 4096<<16))
    f.write(pack(">f", bpy.context.scene.frame_end/30.0))
    f.write(pack("B", len(ob.pose.bones)))
    f.write(pack("B", 0))
    f.write(pack("B", 0))
    f.write(pack("B", 0))
    bone_id = 0
    total_of_keyframe = 9
    for pbone in ob.pose.bones:
        f.write(pack(">H", 0))
        f.write(pack(">H", bone_id))
        f.write(pack(">H", total_of_keyframe))
        f.write(pack(">H", 0))
        bone_id+=1

def WritepAnimPS2(f):
    ob = bpy.context.object
    f.write(pack("<I", 16+8*len(ob.pose.bones)))
    f.write(pack("<I", 4096<<16))
    f.write(pack("<f", bpy.context.scene.frame_end/30.0))
    f.write(pack("B", len(ob.pose.bones)))
    f.write(pack("B", 0))
    f.write(pack("B", 0))
    f.write(pack("B", 0))
    bone_id = 0
    total_of_keyframe = 8
    index_key=0
    
    for pbone in ob.pose.bones:
        f.write(pack("<H", 0))
        f.write(pack("<H", bone_id))
        f.write(pack("<H", total_of_keyframe))
        f.write(pack("<H", 0))
        bone_id+=1
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 3))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 4))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 5))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 6))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 7))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 8))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 1))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
        for i in range(1):
            f.write(pack("<H", 4096))
            f.write(pack("<H", 2))
            f.write(pack("<H", 0))
            f.write(pack("<H", 0))
            

def pAnim_importing(filepath):
    with open(filepath, "rb") as f:
        ReadpAnim(f, filepath)

def pAnim_exporting(filepath):
    with open(filepath, "wb") as f:
        WritepAnimPS2(f)
        
    
