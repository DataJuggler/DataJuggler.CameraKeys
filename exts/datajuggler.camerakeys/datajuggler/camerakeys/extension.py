import typing
import omni.ext
import omni.ui as ui
import omni.timeline
import math
from omni.kit.viewport.utility import get_active_viewport
from pxr import Sdf, Usd, UsdGeom, Gf


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
            resolution = active_viewport.resolution
            camera_path = active_viewport.camera_path
        else:
            # Otherwise, create a camera that will be used to frame the prim_to_frame
            camera_path = "/World/Camera"
            UsdGeom.Camera.Define(stage, camera_path)

        print (camera_path)

        # Start at 100
        self._MovementValue = 100
        self._label = None        

        self._window = ui.Window("Camera Keys", width=600, height=300)
        with self._window.frame:
            with ui.VStack():
                
                label = ui.Label("Make sure your project has a camera named Camera at the World level '/World/Camera'")
                self._label = label
                

                def XAxisDown_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    pose = omni.usd.utils.get_world_transform_matrix(camera, current_frame)
                    print("Matrix Form:", pose)
                    transform = pose.ExtractTranslation()

                    print("Translation: ", transform)
                    
                    transformX = transform[0]
                    transformY = transform[1]
                    transformZ = transform[2]   

                    # set the new transofrmX value
                    newTransformX = transformX - self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved down on the X Axis to " + str(round(newTransformX, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),value=Gf.Vec3d(newTransformX, transformY, transformZ),prev=Gf.Vec3d(transformX, transformY, transformZ))
                
                def XAxisUp_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    pose = omni.usd.utils.get_world_transform_matrix(camera, current_frame)
                    print("Matrix Form:", pose)
                    transform = pose.ExtractTranslation()

                    print("Translation: ", transform)
                    
                    transformX = transform[0]
                    transformY = transform[1]
                    transformZ = transform[2]   

                    # set the new transofrmX value
                    newTransformX = transformX + self._MovementValue

                    # q = pose.ExtractRotation().GetQuaternion()

                    # rawX = q.GetImaginary()[0] * 360 / math.pi

                    # rotationX = round(rawX, 1)
                    # rotationY = q.GetImaginary()[1] * 180 / math.pi
                    # rotationZ = q.GetImaginary()[2] * 180 / math.pi
                    
                    # display the result
                    label.text = "The Camera object was moved up on the X Axis to " + str(round(newTransformX, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),value=Gf.Vec3d(newTransformX, transformY, transformZ),prev=Gf.Vec3d(transformX, transformY, transformZ))

                
                def YAxisUp_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    pose = omni.usd.utils.get_world_transform_matrix(camera, current_frame)
                    print("Matrix Form:", pose)
                    transform = pose.ExtractTranslation()

                    print("Translation: ", transform)
                    
                    transformX = transform[0]
                    transformY = transform[1]
                    transformZ = transform[2]   

                    # go up 10 unites
                    newTransformY = transformY + self._MovementValue
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),value=Gf.Vec3d(transformX, newTransformY, transformZ),prev=Gf.Vec3d(transformX, transformY, transformZ))                 
                    
                    label.text = "Camera was moved up"

                def YAxisDown_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    pose = omni.usd.utils.get_world_transform_matrix(camera, current_frame)
                    print("Matrix Form:", pose)
                    transform = pose.ExtractTranslation()

                    print("Translation: ", transform)
                    
                    transformX = transform[0]
                    transformY = transform[1]
                    transformZ = transform[2]   

                    # go down 10 units
                    newTransformY = transformY - self._MovementValue
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),value=Gf.Vec3d(transformX, newTransformY, transformZ),prev=Gf.Vec3d(transformX, transformY, transformZ))                 
                    
                    label.text = "Camera Was Moved Down on the Y Axis to " + str(round(newTransformY, 1))                

                def ZAxisDown_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    pose = omni.usd.utils.get_world_transform_matrix(camera, current_frame)
                    print("Matrix Form:", pose)
                    transform = pose.ExtractTranslation()

                    print("Translation: ", transform)
                    
                    transformX = transform[0]
                    transformY = transform[1]
                    transformZ = transform[2]   

                    ## set the new transofrmz value
                    newTransformZ = transformZ - self._MovementValue
                    
                    # display the new result
                    label.text = "The Camera object was moved down on the Z Axis to " + str(round(newTransformZ, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),value=Gf.Vec3d(transformX, transformY, newTransformZ),prev=Gf.Vec3d(transformX, transformY, transformZ))
                
                def ZAxisUp_Click():

                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()
                    active_viewport = get_active_viewport()
                    camera_path = active_viewport.camera_path
                    camera = stage.GetPrimAtPath(camera_path)                    
                    timeline = omni.timeline.get_timeline_interface()
                    current_frame = timeline.get_current_time() * timeline.get_time_codes_per_seconds()

                    pose = omni.usd.utils.get_world_transform_matrix(camera, current_frame)
                    print("Matrix Form:", pose)
                    transform = pose.ExtractTranslation()

                    print("Translation: ", transform)
                    
                    transformX = transform[0]
                    transformY = transform[1]
                    transformZ = transform[2]   

                    # set the new transofrmX value
                    newTransformZ = transformZ + self._MovementValue

                    # q = pose.ExtractRotation().GetQuaternion()

                    # rawX = q.GetImaginary()[0] * 360 / math.pi

                    # rotationX = round(rawX, 1)
                    # rotationY = q.GetImaginary()[1] * 180 / math.pi
                    # rotationZ = q.GetImaginary()[2] * 180 / math.pi
                    
                    label.text = "The Camera object was moved up on the Z Axis to " + str(round(newTransformZ, 1))
                    
                    # move the camera up
                    omni.kit.commands.execute('ChangeProperty',prop_path=Sdf.Path('/World/Camera.xformOp:translate'),value=Gf.Vec3d(transformX, transformY, newTransformZ),prev=Gf.Vec3d(transformX, transformY, transformZ))

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
                    
                    label.text = "6 Keys Were Set at frane " + str(frame)

                # add an IntSlider for Strength
                ui.Label("Camera Movement Amount")
                self._movementSlider = ui.IntSlider(min = 10, max = 1000, step=10)                
                self._movementSlider.model.set_value(100)
                self._MovementValue = 100
                self._movementSlider.model.add_value_changed_fn(self._on_value_changed)

                with ui.HStack():
                    xAxisButtonUp = ui.Button("X +", clicked_fn=XAxisUp_Click)
                    yAxisButtonUp = ui.Button("Y +", clicked_fn=YAxisUp_Click)
                    zAxisButtonUp = ui.Button("Z +", clicked_fn=ZAxisUp_Click)                    

                with ui.HStack():
                    xAxisButtonDown = ui.Button("X -", clicked_fn=XAxisDown_Click)
                    yAxisButtonDown = ui.Button("Y -", clicked_fn=YAxisDown_Click)
                    zAxisButtonDown = ui.Button("Z -", clicked_fn=ZAxisDown_Click)   
                    
                ui.Label("Change the timeline to the desired frame before clicking the Set Keys button.")
                ui.Button("Set Keys", clicked_fn=SetKeys_Click)
                
    def _on_value_changed(self, model: ui.SimpleIntModel):

        self._MovementValue = model.get_value_as_int()
        self._label.text = "Camera movement value = " + str(self._MovementValue)
            
        #if self._on_value_changed_fn:
        #    self._on_value_changed_fn(scale)

    def on_shutdown(self):
        print("[datajuggler.camerakeys] datajuggler camerakeys shutdown")
