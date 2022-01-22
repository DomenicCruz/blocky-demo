from ursina import *
from ursina import collider
from random import uniform
from ursina.input_handler import Keys  
from additional_code.first_person_ctr_custom import CustomFirstPersonController
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

app = Ursina()
# Settings
window.fps_counter.enabled = False
window.exit_button.visible = False
window.title = "Blocky"
window.borderless = False
#Mouse
mouse.enabled = True 
mouse.visible = False
mouse.locked = True

# Textures
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
block_texture_arr = [grass_texture, stone_texture, brick_texture, dirt_texture]
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')

# Sound
punch_sound = Audio('assets/punch_sound.wav', loop=False, autoplay=False)
# world_sound = Audio('night_sky')
# world_sound.play()

# Globals General
block_pick = 0
block_arr_max_idx = len(block_texture_arr) - 1
camera_position = Vec3(0,0,0)

# Classes
class Voxel(Button):
    #Blocks
    def __init__(self, position = (0,0,0), texture = grass_texture):
        super().__init__(
                parent = scene,
                position = position,
                model = 'assets/block',
                origin_y = 0.5,
                texture = texture,
                color = color.color(0, 0, uniform(0.9,1)),
                scale = 0.5,
                collider = 'box', #Change
                collision=True,
                )

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                global block_pick
                #Prevent the player from placing blocks to high
                if player.move and player.y < 70:
                    voxel = Voxel(position = self.position + mouse.normal, texture=block_texture_arr[block_pick])
                punch_sound.play()
            if key == "right mouse down":
                destroy(self)
                punch_sound.play()

class Sky(Entity):
    def __init__(self):
        super().__init__(
                parent = scene,
                model = 'sphere',
                texture = sky_texture,
                scale = 180,
                double_sided = True,
                )


class Hand(Entity):
    def __init__(self):
        super().__init__(
                parent = camera.ui,
                model = 'assets/arm',
                texture = arm_texture,
                scale = 0.2,
                rotation = Vec3(140, -10, 0),
                position = Vec2(0.4, -0.6))

    def active(self):
        self.position = Vec2(0.3, -0.4)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

class UiBlock(Entity):
    #For the ui
    def __init__(self, texture = grass_texture, position=(-.80,-.4)):
        super().__init__(
                parent =  camera.ui,
                model = 'assets/block',
                scale = 0.05,
                position = position,                                        
                texture = texture,                                     
                rotation = Vec3(-4, -10, -4),
                )

    def change_texture(self, texture):
        self.texture = texture

# My functions #
def choose_block(key):
    """Used to change player voxel (block) spawn choice
    changes global var block_pick, also uses block_texture_arr
    """
    global block_pick
    if key == '1': block_pick = 0
    if key == '2': block_pick = 1
    if key == '3': block_pick = 2
    if key == '4': block_pick = 3
    if key == 'scroll up':
        block_pick += 1
        block_pick = 0 if block_pick >= block_arr_max_idx else block_pick
    if key == 'scroll down':
        block_pick -= 1
        block_pick = block_arr_max_idx if block_pick <= 0 else block_pick

        
## Main automatically called functions ##
def input(key):
    #Change block choice on user input
    choose_block(key)
    # Change Chosen block in the ui
    chosen_block.change_texture(block_texture_arr[block_pick])

     
    if key == Keys.escape:#NOTE Better is to add the menu_active variable 
        # Toggle the menu, mouse lock & visibility to click on the menu
        mouse.visible = not mouse.visible 
        #mouse.locked = not mouse.locked 
        menu.visible = mouse.visible 
        if menu.visible: # if menu is active
            player.on_disable()
        else: 
            player.on_enable()

    # #Move Hand on the mouse click
    # if key == Keys.left_mouse_down or key == Keys.right_mouse_down: hand.active()
    # else: hand.passive()

#NOTE held_keys inside update to see pressed keys
def update():
    #Move Hand on the mouse click
    if held_keys['left mouse'] or held_keys['right mouse']: hand.active()
    else: hand.passive()

    #Rotate chosen_block in the ui
    chosen_block.rotation_y = (0 if chosen_block.rotation_y >= 360 else chosen_block.rotation_y) + 50 * time.dt

    #Teleport player if it is to low
    if player.y <= -75:
        player.position = (0,0,0)

    #Move player back if it to far from the x=0 z=0
    if player.x > 50: player.x = player.x - player.speed
    if player.z > 50: player.z = player.z - player.speed




#Create Voxel field
for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x,0,z)) 

#Place other objects
#player = CustomFirstPersonController(visible=False, model='cube',texture='white_cube', collider='box', collision=True, scale=2)
#Player
player = CustomFirstPersonController(width=.8)

#Menu
menu = DropdownMenu('Menu', visible = False, buttons=(
    DropdownMenuButton('Exit', on_click=application.quit),
))


sky = Sky()
#ui
hand = Hand()
chosen_block = UiBlock()

#Place this at the end
app.run()
