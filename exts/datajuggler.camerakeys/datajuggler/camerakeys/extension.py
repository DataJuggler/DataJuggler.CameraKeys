import omni.ext
import omni.ui as ui
import omni.timeline
import math
from omni.kit.viewport.utility import get_active_viewport
from pxr import Sdf, Usd, UsdGeom, Gf
import omni.usd

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class DatajugglerCamerakeysExtension(omni.ext.IExt):

    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[datajuggler.camerakeys] datajuggler camerakeys startup")
       
        # Get the stage
        stage = omni.usd.get_context().get_stage()

        active_viewport = get_active_viewport()
        if active_viewport:
            # Pull meaningful information from the Viewport to frame a specific prim
            time = active_viewport.time            
            camera_path = active_viewport.camera_path
        else:
            # Otherwise, create a camera that will be used to frame the prim_to_frame
            camera_path = "/World/Camera"
            UsdGeom.Camera.Define(stage, camera_path)

        print(camera_path)

        # Start at 100
        self._MovementValue = 100
        self._RotationValue = 5
        self._label = None        

        self._window = ui.Window("Camera Keys", width=600, height=660)
        with self._window.frame:
            with ui.VStack():
                
                label = ui.Label("Make sure your project has a camera named Camera at the World level '/World/Camera'")
                self._label = label

                def get_local_rot(prim: Usd.Prim):
                    return prim.GetAttribute("xformOp:rotateXYZ").Get()

                def decompose_matrix(mat: Gf.Matrix4d):
                    reversed_ident_mtx = reversed(Gf.Matrix3d())

                    translate = mat.ExtractTranslation()
                    scale = Gf.Vec3d(*(v.GetLength() for v in mat.ExtractRotationMatrix()))
                    #must remove scaling from mtx before calculating rotations
                    mat.Orthonormalize()
                    # without reversed this seems to return angles in ZYX order
                    rotate = Gf.Vec3d(*reversed(mat.ExtractRotation().Decompose(*reversed_ident_mtx)))
                    return translate, rotate, scale
                
                def Left_Click():
                    
                    stage = omni.usd.get_context().get_stage()
                    camera = stage.GetPrimAtPath("/World/Camera")
                    xform = UsdGeom.Xformable(camera)
                    local_transformation: Gf.Matrix4d = xform.GetLocalTransformation()
                    # Apply the local matrix to the start and end points of the camera's default forward vector (-Z)
                    a: Gf.Vec4d = Gf.Vec4d(0,0,0,1) * local_transformation
                    b: Gf.Vec4d = Gf.Vec4d(-1,0,0,1) * local_transformation
                    # Get the vector between those two points to get the camera's current forward vector
                    cam_fwd_vec = b-a
                    # Convert to Vec3 and then normalize to get unit vector
                    cam_fwd_unit_vec = Gf.Vec3d(cam_fwd_vec[:3]).GetNormalized()
                    # Multiply the forward direction vector with how far forward you want to move
                    # forward_step = cam_fwd_unit_vec * 100
                    forward_step = cam_fwd_unit_vec * self._MovementValue
                    # Create a new matrix with the translation that you want to perform
                    offset_mat = Gf.Matrix4d()
                    offset_mat.SetTranslate(forward_step)
                    # Apply the translation to the current local transform
                    new_transform = local_transformation * offset_mat
                    # Extract the new translation
                    translate: Gf.Vec3d = new_transform.ExtractTranslation()
                    # Update the attribute
                    camera.GetAttribute("xformOp:translate").Set(translate)
                
                def Forward_Click():
                    
                    stage = omni.usd.get_context().get_stage()
                    camera = stage.GetPrimAtPath("/World/Camera")
                    xform = UsdGeom.Xformable(camera)
                    local_transformation: Gf.Matrix4d = xform.GetLocalTransformation()
                    # Apply the local matrix to the start and end points of the camera's default forward vector (-Z)
                    a: Gf.Vec4d = Gf.Vec4d(0,0,0,1) * local_transformation
                    b: Gf.Vec4d = Gf.Vec4d(0,0,-1,1) * local_transformation
                    # Get the vector between those two points to get the camera's current forward vector
                    cam_fwd_vec = b-a
                    # Convert to Vec3 and then normalize to get unit vector
                    cam_fwd_unit_vec = Gf.Vec3d(cam_fwd_vec[:3]).GetNormalized()
                    # Multiply the forward direction vector with how far forward you want to move
                    # forward_step = cam_fwd_unit_vec * 100
                    forward_step = cam_fwd_unit_vec * self._MovementValue
                    # Create a new matrix with the translation that you want to perform
                    offset_mat = Gf.Matrix4d()
                    offset_mat.SetTranslate(forward_step)
                    # Apply the translation to the current local transform
                    new_transform = local_transformation * offset_mat
                    # Extract the new translation
                    translate: Gf.Vec3d = new_transform.ExtractTranslation()
                    # Update the attribute
                    camera.GetAttribute("xformOp:translate").Set(translate)

                def Back_Click():
                    
                    stage = omni.usd.get_context().get_stage()
                    camera = stage.GetPrimAtPath("/World/Camera")
                    xform = UsdGeom.Xformable(camera)
                    local_transformation: Gf.Matrix4d = xform.GetLocalTransformation()
                    # Apply the local matrix to the start and end points of the camera's default forward vector (-Z)
                    a: Gf.Vec4d = Gf.Vec4d(0,0,0,1) * local_transformation
                    b: Gf.Vec4d = Gf.Vec4d(0,0,1,1) * local_transformation
                    # Get the vector between those two points to get the camera's current forward vector
                    cam_fwd_vec = b-a
                    # Convert to Vec3 and then normalize to get unit vector
                    cam_fwd_unit_vec = Gf.Vec3d(cam_fwd_vec[:3]).GetNormalized()
                    # Multiply the forward direction vector with how far forward you want to move
                    # forward_step = cam_fwd_unit_vec * 100
                    forward_step = cam_fwd_unit_vec * self._MovementValue
                    # Create a new matrix with the translation that you want to perform
                    offset_mat = Gf.Matrix4d()
                    offset_mat.SetTranslate(forward_step)
                    # Apply the translation to the current local transform
                    new_transform = local_transformation * offset_mat
                    # Extract the new translation
                    translate: Gf.Vec3d = new_transform.ExtractTranslation()
                    # Update the attribute
                    camera.GetAttribute("xformOp:translate").Set(translate)

                def Right_Click():
                    
                    stage = omni.usd.get_context().get_stage()
                    camera = stage.GetPrimAtPath("/World/Camera")
                    xform = UsdGeom.Xformable(camera)
                    local_transformation: Gf.Matrix4d = xform.GetLocalTransformation()
                    # Apply the local matrix to the start and end points of the camera's default forward vector (-Z)
                    a: Gf.Vec4d = Gf.Vec4d(-1,0,0,1) * local_transformation
                    b: Gf.Vec4d = Gf.Vec4d(0,0,0,1) * local_transformation
                    # Get the vector between those two points to get the camera's current forward vector
                    cam_fwd_vec = b-a
                    # Convert to Vec3 and then normalize to get unit vector
                    cam_fwd_unit_vec = Gf.Vec3d(cam_fwd_vec[:3]).GetNormalized()
                    # Multiply the forward direction vector with how far forward you want to move
                    # forward_step = cam_fwd_unit_vec * 100
                    forward_step = cam_fwd_unit_vec * self._MovementValue
                    # Create a new matrix with the translation that you want to perform
                    offset_mat = Gf.Matrix4d()
                    offset_mat.SetTranslate(forward_step)
                    # Apply the translation to the current local transform
                    new_transform = local_transformation * offset_mat
                    # Extract the new translation
                    translate: Gf.Vec3d = new_transform.ExtractTranslation()
                    # Update the attribute
                    camera.GetAttribute("xformOp:translate").Set(translate)

                def XRotateUp_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath("/World/Camera")                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    xForm = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xForm.GetLocalTransformation()                    
                    decomposed_Transform = decompose_matrix(local_transform)
                    
                     # local_rotate = get_local_rot(camera)
                    rotationX = round(decomposed_Transform[1][0], 1)
                    rotationY = round(decomposed_Transform[1][1], 1)
                    rotationZ = round(decomposed_Transform[1][2], 1)

                    # calculate the new value
                    newRotationX = round(rotationX + self._RotationValue, 1)

                    omni.kit.commands.execute('ChangeProperty',
	                    prop_path=Sdf.Path('/World/Camera.xformOp:rotateYXZ'),
	                    value=Gf.Vec3f(newRotationX, rotationY, rotationZ),
	                    prev=Gf.Vec3f(rotationX, rotationY, rotationZ))

                    label.text = "New Rotation X = " + str(newRotationX)

                def XRotateDown_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath("/World/Camera")                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    xForm = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xForm.GetLocalTransformation()                    
                    decomposed_Transform = decompose_matrix(local_transform)
                    
                    # local_rotate = get_local_rot(camera)
                    rotationX = round(decomposed_Transform[1][0], 1)
                    rotationY = round(decomposed_Transform[1][1], 1)
                    rotationZ = round(decomposed_Transform[1][2], 1)

                    # calculate the new value
                    newRotationX = round(rotationX - self._RotationValue,1)

                    omni.kit.commands.execute('ChangeProperty',
	                    prop_path=Sdf.Path('/World/Camera.xformOp:rotateYXZ'),
	                    value=Gf.Vec3f(newRotationX, rotationY, rotationZ),
	                    prev=Gf.Vec3f(rotationX, rotationY, rotationZ))

                    label.text = "New Rotation X = " + str(newRotationX) 

                def YRotateUp_Click():
                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath("/World/Camera")                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    xForm = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xForm.GetLocalTransformation()                    
                    decomposed_Transform = decompose_matrix(local_transform)
                    
                    # local_rotate = get_local_rot(camera)
                    rotationX = round(decomposed_Transform[1][0], 1)
                    rotationY = round(decomposed_Transform[1][1], 1)
                    rotationZ = round(decomposed_Transform[1][2], 1)

                    # label.text = "Old Rotation Y = " + str(rotationY)

                    # calculate the new value
                    newRotationY = round(rotationY + self._RotationValue, 1)

                    omni.kit.commands.execute('ChangeProperty',
	                    prop_path=Sdf.Path('/World/Camera.xformOp:rotateYXZ'),
	                    value=Gf.Vec3f(rotationX, newRotationY, rotationZ),
	                    prev=Gf.Vec3f(rotationX, rotationY, rotationZ))

                    label.text = "New Rotation Y = " + str(newRotationY)


                def YRotateDown_Click():
                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath("/World/Camera")                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    xForm = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xForm.GetLocalTransformation()                    
                    decomposed_Transform = decompose_matrix(local_transform)
                    
                   # local_rotate = get_local_rot(camera)
                    rotationX = round(decomposed_Transform[1][0], 1)
                    rotationY = round(decomposed_Transform[1][1], 1)
                    rotationZ = round(decomposed_Transform[1][2], 1)

                    # calculate the new value
                    newRotationY = round(rotationY - self._RotationValue, 1)

                    omni.kit.commands.execute('ChangeProperty',
	                    prop_path=Sdf.Path('/World/Camera.xformOp:rotateYXZ'),
	                   value=Gf.Vec3f(rotationX, newRotationY, rotationZ),
	                    prev=Gf.Vec3f(rotationX, rotationY, rotationZ))

                    label.text = "New Rotation Y = " + str(newRotationY)

                def ZRotateUp_Click():
                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath("/World/Camera")                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    xForm = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xForm.GetLocalTransformation()                    
                    decomposed_Transform = decompose_matrix(local_transform)
                    
                    # local_rotate = get_local_rot(camera)
                    rotationX = round(decomposed_Transform[1][0], 1)
                    rotationY = round(decomposed_Transform[1][1], 1)
                    rotationZ = round(decomposed_Transform[1][2], 1)

                    # calculate the new value
                    newRotationZ = round(rotationZ + self._RotationValue, 1)

                    omni.kit.commands.execute('ChangeProperty',
	                    prop_path=Sdf.Path('/World/Camera.xformOp:rotateYXZ'),
	                    value=Gf.Vec3f(rotationX, rotationY, newRotationZ),
	                    prev=Gf.Vec3f(rotationX, rotationY, rotationZ))

                    label.text = "New RotationZY = " + str(newRotationZ)

                def ZRotateDown_Click():
                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath("/World/Camera")                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    xForm = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xForm.GetLocalTransformation()                    
                    decomposed_Transform = decompose_matrix(local_transform)
                    
                     # local_rotate = get_local_rot(camera)
                    rotationX = round(decomposed_Transform[1][0], 1)
                    rotationY = round(decomposed_Transform[1][1], 1)
                    rotationZ = round(decomposed_Transform[1][2], 1)

                    # calculate the new value
                    newRotationZ = round(rotationZ - self._RotationValue, 1)

                    omni.kit.commands.execute('ChangeProperty',
	                    prop_path=Sdf.Path('/World/Camera.xformOp:rotateYXZ'),
	                    value=Gf.Vec3f(rotationX, rotationY, newRotationZ),
	                    prev=Gf.Vec3f(rotationX, rotationY, rotationZ))

                    label.text = "New Rotation Y = " + str(newRotationZ)


                def XAxisDown_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)

                    xform = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xform.GetLocalTransformation()
                    decomposed_Transform = decompose_matrix(local_transform)
                   
                    transformX = round(decomposed_Transform[0][0], 1)
                    transformY = round(decomposed_Transform[0][1], 1)
                    transformZ = round(decomposed_Transform[0][2], 1)

                    # set the new transofrmX value
                    newTransformX = transformX - self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved down on the X Axis to " + str(round(newTransformX, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                        value=Gf.Vec3d(newTransformX, transformY, transformZ),
                        prev=Gf.Vec3d(transformX, transformY, transformZ))
                
                def XAxisUp_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    
                    xform = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xform.GetLocalTransformation()
                    decomposed_Transform = decompose_matrix(local_transform)
                   
                    transformX = round(decomposed_Transform[0][0], 1)
                    transformY = round(decomposed_Transform[0][1], 1)
                    transformZ = round(decomposed_Transform[0][2], 1)

                    # set the new transofrmX value
                    newTransformX = transformX + self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved up on the X Axis to " + str(round(newTransformX, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                        value=Gf.Vec3d(newTransformX, transformY, transformZ),
                        prev=Gf.Vec3d(transformX, transformY, transformZ))

                def YAxisUp_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    
                    xform = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xform.GetLocalTransformation()
                    decomposed_Transform = decompose_matrix(local_transform)
                   
                    transformX = round(decomposed_Transform[0][0], 1)
                    transformY = round(decomposed_Transform[0][1], 1)
                    transformZ = round(decomposed_Transform[0][2], 1)

                    # set the new transofrmX value
                    newTransformY = transformY + self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved up on the Y Axis to " + str(round(newTransformY, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                        value=Gf.Vec3d(transformX, newTransformY, transformZ),
                        prev=Gf.Vec3d(transformX, transformY, transformZ))

                def YAxisDown_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    
                    xform = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xform.GetLocalTransformation()
                    decomposed_Transform = decompose_matrix(local_transform)
                   
                    transformX = round(decomposed_Transform[0][0], 1)
                    transformY = round(decomposed_Transform[0][1], 1)
                    transformZ = round(decomposed_Transform[0][2], 1)

                    # set the new transofrmX value
                    newTransformY = transformY - self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved down on the Y Axis to " + str(round(newTransformY, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                        value=Gf.Vec3d(transformX, newTransformY, transformZ),
                        prev=Gf.Vec3d(transformX, transformY, transformZ))              

                def ZAxisDown_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    
                    xform = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xform.GetLocalTransformation()
                    decomposed_Transform = decompose_matrix(local_transform)
                   
                    transformX = round(decomposed_Transform[0][0], 1)
                    transformY = round(decomposed_Transform[0][1], 1)
                    transformZ = round(decomposed_Transform[0][2], 1)

                    # set the new transofrmX value
                    newTransformZ = transformZ - self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved down on the Z Axis to " + str(round(newTransformZ, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                        value=Gf.Vec3d(transformX, transformY, newTransformZ),
                        prev=Gf.Vec3d(transformX, transformY, transformZ))

                def ZAxisUp_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    
                    xform = UsdGeom.Xformable(camera)
                    local_transform: Gf.Matrix4d = xform.GetLocalTransformation()
                    decomposed_Transform = decompose_matrix(local_transform)
                   
                    transformX = round(decomposed_Transform[0][0], 1)
                    transformY = round(decomposed_Transform[0][1], 1)
                    transformZ = round(decomposed_Transform[0][2], 1)

                    # set the new transofrmX value
                    newTransformZ = transformZ + self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved up on the Z Axis to " + str(round(newTransformZ, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                        value=Gf.Vec3d(transformX, transformY, newTransformZ),
                        prev=Gf.Vec3d(transformX, transformY, transformZ))

                def SetKeys_Click():
                    
                    omni.kit.commands.execute('SetAnimCurveKeys',
                        paths=['/World/Camera.xformOp:translate|x'])
                    
                    omni.kit.commands.execute('SetAnimCurveKeys',
                        paths=['/World/Camera.xformOp:translate|y'])
                    
                    omni.kit.commands.execute('SetAnimCurveKeys',
                        paths=['/World/Camera.xformOp:translate|z'])
                    
                    omni.kit.commands.execute('SetAnimCurveKeys',
                        paths=['/World/Camera.xformOp:rotateYXZ|x'])
                    
                    omni.kit.commands.execute('SetAnimCurveKeys',
                        paths=['/World/Camera.xformOp:rotateYXZ|y'])
                    
                    omni.kit.commands.execute('SetAnimCurveKeys',
                        paths=['/World/Camera.xformOp:rotateYXZ|z'])

                    timeline = omni.timeline.get_timeline_interface()
                    
                    time = timeline.get_current_time()

                    fps = timeline.get_time_codes_per_seconds()

                    frame = time * fps
                    
                    label.text = "6 Keys Were Set at frame " + str(frame)

                # add an IntSlider for translate Strength
                ui.Label("Camera Rotation Amount")
                self._rotationSlider = ui.IntSlider(min = 1, max = 90, step=5)                
                self._rotationSlider.model.set_value(5)
                self._rotationValue = 5
                self._rotationSlider.model.add_value_changed_fn(self._onrotation_value_changed)

                with ui.HStack(height=40):                    
                    xAxisButtonUp = ui.Button("X +", clicked_fn=XRotateUp_Click)
                    yAxisButtonUp = ui.Button("Y +", clicked_fn=YRotateUp_Click)
                    zAxisButtonUp = ui.Button("Z +", clicked_fn=ZRotateUp_Click)  

                with ui.HStack(height=40):
                    xAxisButtonDown = ui.Button("X -", clicked_fn=XRotateDown_Click)
                    yAxisButtonDown = ui.Button("Y -", clicked_fn=YRotateDown_Click)
                    zAxisButtonDown = ui.Button("Z -", clicked_fn=ZRotateDown_Click)                     
                
                # add an IntSlider for translate Strength
                ui.Label("Camera Movement Amount")
                self._movementSlider = ui.IntSlider(min = 10, max = 1000, step=10)                
                self._movementSlider.model.set_value(100)
                self._MovementValue = 100
                self._movementSlider.model.add_value_changed_fn(self._on_value_changed)

                with ui.HStack(height=54):
                    leftButton = ui.Button("Left", clicked_fn=Left_Click)
                    forwardButton = ui.Button("Forward", clicked_fn=Forward_Click)
                    yAxisButtonUp = ui.Button("Back", clicked_fn=Back_Click)
                    rightButton = ui.Button("Right", clicked_fn=Right_Click)

                with ui.HStack(height=54):
                    xAxisButtonUp = ui.Button("X +", clicked_fn=XAxisUp_Click)
                    yAxisButtonUp = ui.Button("Y +", clicked_fn=YAxisUp_Click)
                    zAxisButtonUp = ui.Button("Z +", clicked_fn=ZAxisUp_Click)

                with ui.HStack(height=54):
                    xAxisButtonDown = ui.Button("X -", clicked_fn=XAxisDown_Click)
                    yAxisButtonDown = ui.Button("Y -", clicked_fn=YAxisDown_Click)
                    zAxisButtonDown = ui.Button("Z -", clicked_fn=ZAxisDown_Click)   

                # with ui.VStack(height=54):
                #    ui.Label("Shaky Cam Movement Amount - Only Applies To Forward")
                #    # add an IntSlider for translate Strength                
                #    self._ShakySlider = ui.IntSlider(min = 1, max = 100, step=1)
                #    self._ShakySlider.model.set_value(0)
                #    self._ShakyValue = 0
                #    self._ShakySlider.model.add_value_changed_fn(self._on_shakyvalue_changed)

                with ui.VStack(height=40):
                    ui.Label("")                   
                    ui.Label("Change the timeline to the desired frame before clicking the Set Keys button.")
                
                with ui.VStack(height=60):
                    ui.Button("Set Keys", clicked_fn=SetKeys_Click)
                
    def _on_value_changed(self, model: ui.SimpleIntModel):

        self._MovementValue = model.get_value_as_int()
        self._label.text = "Camera movement value = " + str(self._MovementValue)

    def _onrotation_value_changed(self, model: ui.SimpleIntModel):

        self._RotationValue = model.get_value_as_int()
        self._label.text = "Camera rotation value = " + str(self._Rotation_Value)

    #def _on_shakyvalue_changed(self, model: ui.SimpleIntModel):

    #    self._ShakyValue =  model.get_value_as_int()
    #    self._label.text = "Camera shaky value = " + str(self._Shaky_Value)

    def on_shutdown(self):
        print("[datajuggler.camerakeys] datajuggler camerakeys shutdown")