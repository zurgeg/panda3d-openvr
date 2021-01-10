import openvr # For good measure :D
from p3dopenvr.p3dopenvr import P3DOpenVR
from direct.showbase.ShowBase import ShowBase 
class VRBackend(P3DOpenVR):
  def init_action(self):
      filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "newfirehawk.txt")
      self.load_action_manifest(filename, "/actions/main")
      self.source_right = self.vr_input.getInputSourceHandle('/user/hand/right')
      self.action_pose_right = self.vr_input.getActionHandle('/actions/main/in/RightHand')
      self.pos = None
      self.right_hand = None
  def update_action(self):
      dt = globalClock.getDt()
      if not self.did_show_dir:
          self.did_show_dir = True
      pos = self.get_action_pose(self.action_pose_right)
      right_matrix = self.get_pose_modelview(pos.pose)

      if self.right_hand is None:
          self.right_hand = self.tracking_space.attach_new_node('right-hand')
          model = loader.loadModel("box")
          model.reparent_to(self.right_hand)
          model.set_scale(0.1)
          self.right_hand.show()
      self.right_hand.set_mat(right_matrix)

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__() # Setup renderer
        self.vr = VRBackend()
        self.vr.init()
        self.rh = render.attachNewNode('rh')
        self.rControllerRay.setOrigin(0,0,0)
        self.rControllerRay.setDirection(0, 1, 0)
        self.rControllerCol = CollisionNode('ControllerRay')
        self.rControllerCol.addSolid(self.rControllerRay)
        self.rControllerCol.setFromCollideMask(CollideMask.bit(0))
        self.rControllerCol.setIntoCollideMask(CollideMask.allOff())
        self.rControllerColNp = self.rh.attachNewNode(self.rControllerCol)
        self.rControllerHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.rControllerColNp, self.rControllerHandler)
        self.lControllerColNp.show() # In the case of a game menu, we most likely will want to show the controller ray.
        self.callbacks = {'mytext':self.button_callback}
        mytext = TextNode('mytext')
        mytext.setText("Click me!!")
        mytext.reparentTo(render)
        taskMgr.add(self.collision, "collisionTask")
    def collision(self, task):
        controller_collisions = list(self.lControllerHandler.getEntries())
        controller_collisions.sort(key=lambda x: x.getSurfacePoint(render).getZ())
        self.rh.setPos(self.vr.right_hand.getPos(render))
        if len(controller_collisions) > 0:
          name = controller_collisions[0].getIntoNode().getName()
          if name in self.callbacks.keys():
            self.callbacks[name]()
        return task.cont
          
            
    def button_callback():
      print('clickity click')
