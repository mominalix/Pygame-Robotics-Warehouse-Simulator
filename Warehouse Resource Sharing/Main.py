###### GUI IMPORTS ######
import pygame
import random
import string, sys
import math
from polygon import polygon
from robot import robot as Robot_sim
from rack import rack
from server import server
import time

###### COLOUR DEFINATIONS ######
BLACK = (0, 0, 0, 0)
WHITE = (255, 255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 255, 255)

###### SCREEN SIZE ######
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

###### Global Variables ######
global exit_flag
exit_flag = 0
#MAX_POLYGONS = 6
" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  main program screen !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


def main(RESOURCE_SHARING,start_time,MAX_POLYGONS,previous_time,previous_energy):
    """ Main Program """
    # Call this function so the Pygame library can initialize itself
    pygame.init()
    n_polygons = 0
    # Create an 800x600 sized screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    display_screen = pygame.display.set_mode(size)  # ,pygame.FULLSCREEN)
    screen_sizes = [[1600, 900], [1280, 720], [800, 450]]
    screen_index = 0
    screen = pygame.Surface(size).convert_alpha()

    img_addr = './data/'  # data directory

    background_image = pygame.image.load(img_addr + "map2.png")  # .convert_alpha()

    # Set Icon
    ##    icon = pygame.image.load(img_addr+"logo.png")#.convert_alpha()
    ##    pygame.display.set_icon(icon)

    # Set the title of the window
    pygame.display.set_caption('Resource Sharing Demo')

    # game name
    font = pygame.font.SysFont('Calibri', 22, False, False)
    font_1 = pygame.font.SysFont('Calibri', 24, True, False)
    #     font_2 = pygame.font.SysFont('Calibri', 21, True, False)

    # - Rack Classes
    red = rack(1)
    green = rack(2)
    blue = rack(3)

    # Software variables
    global exit_flag
    # Sim Objects
    Time=0
    server_text = server(display_screen)
    game_objects=pygame.sprite.Group()
    robot_list = pygame.sprite.Group()
    robot_safe_zone_list = pygame.sprite.Group()
    robot = Robot_sim([583, 300], 'R1', red, green, blue,server_text,RESOURCE_SHARING)
    robot.rover_heading = 0
    robot.move = 1
    robot_list.add(robot)
    game_objects.add(robot)
    robot2 = Robot_sim([863, 300], 'R2', red, green, blue,server_text,RESOURCE_SHARING)
    robot2.rover_heading = 0
    robot2.path_plan = 1
    robot_list.add(robot2)
    game_objects.add(robot2)
    robot3 = Robot_sim([1089, 300], 'R3', red, green, blue,server_text,RESOURCE_SHARING)
    robot3.rover_heading = 0
    robot3.path_plan = 1
    robot3.path_selected = 'D2'
    robot_list.add(robot3)
    game_objects.add(robot3)
    robot4 = Robot_sim([1342, 300], 'R4', red, green, blue,server_text,RESOURCE_SHARING)
    robot4.rover_heading = 0
    robot4.path_plan = 1
    robot_list.add(robot4)
    game_objects.add(robot4)
    robo_speed = [1, 1, 1]
    robo_speed_text = [font.render('Robot Move Speed : ' + str(robo_speed[0]), True, BLUE), \
                       font.render('Robot Rotate Speed : ' + str(robo_speed[1]), True, BLUE),
                       font.render('Arm Rotate Speed : ' + str(robo_speed[2]), True, BLUE)]

    i=0

    # -- Polygon initialization and spawning for first case
    block_list = pygame.sprite.Group()
    if previous_time == 0:
        while i!=MAX_POLYGONS:
            block_list = pygame.sprite.Group()
            polygon_file = open('polygons.txt', 'w')
            polygon_file.close()
            i=0
            polygon_file = open('polygons.txt', 'a')
            while i!=MAX_POLYGONS:

                polygon_id = random.choice(
                    ['red_pentagon', 'red_square', 'red_triangle', 'green_triangle', 'green_pentagon', 'green_square',
                     'blue_triangle', 'blue_pentagon', 'blue_square'])
                x = random.randint(450, 1500)
                y = random.randint(400, 800)
                coordinates=(x,y)
                obj = polygon(polygon_id, coordinates)
                polygons_hit_list = pygame.sprite.spritecollide(obj, block_list, True)
                if len(polygons_hit_list) <1:
                    n_polygons += 1
                    block_list.add(obj)
                    game_objects.add(obj)
                    x=str(x)
                    y=str(y)
                    polygon_file.write(str(polygon_id + ' ' + x + ' ' + y + '\n'))

                    i += 1
                else:
                    i-=1
                    obj.remove()
            polygon_file.close()
            i=0
            for block in block_list:
                i+=1
            print(i)
    # -- Polygon spawning for second case
        i = 0
        for block in block_list:
            i += 1
        print(i)
    else:
        polygon_file = open('polygons.txt')
        for i in range(0,MAX_POLYGONS):
            # print("polygon created")
            line=polygon_file.readline()
            words=line.split(' ')
            coordinates=[0,0]
            polygon_id=str(words[0])
            coordinates[0]=int(words[1])
            coordinates[1] = int(words[2])
            obj = polygon(polygon_id,coordinates)
            polygons_hit_list = pygame.sprite.spritecollide(obj, block_list, False)
            if len(polygons_hit_list) < 1:
                n_polygons += 1
                block_list.add(obj)
                game_objects.add(obj)
            else:
                i-=1
        polygon_file.close()
    # CLass objects
    # - Server Classes
    # Server = server(display_screen)
    # server_blink = server(display_screen)
    # server_sprite = pygame.sprite.Group()
    # server_sprite.add(Server)
    # server_sprite.add(server_blink)

    global color_count
    color_count = [0, 0, 0]
    # Path Visualize
    # R1 = [500,665][1105,195] R2 = [840,665][1109,195] R3 = [1220,665][1110,195]
    # D1 = [1350,195][681,665] D2 = [1350,195][1033,665] D3 = [1350,195][1419,665]
    R1 = [500, 665]
    R2 = [840, 665]
    R3 = [1220, 665]
    D1 = [1350, 195]
    D2 = [1350, 195]
    D3 = [1350, 195]
    show_path = 0

    # Loop until the user clicks the close button.
    done = False
    n_polygons = MAX_POLYGONS
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Mission Plan -------
    scenario = open('Scenario.txt', 'r')
    missions = []
    mission_state=0
    scenarios=0
    mission =''
    for mission in scenario:
        missions.append(mission)
        scenarios+=1

    # -------- Main Program Loop -----------
    print(missions)
    while n_polygons:
        if mission_state<scenarios:
            mission=missions[mission_state]

        if mission_state== scenarios:
            mission='1000 0 0'
            mission_state += 1
        # --- Main event loop
        mousepos = pygame.mouse.get_pos()
        #server_blink.blink()
        for obj in block_list:
            obj.update_position(robot_list)
        for Robot in robot_list:
            Robot.update_status(block_list, robot_safe_zone_list, robot_list,RESOURCE_SHARING)

        x = [0, 0]
        z = 0

        while z == 0:
            try:
                x = robot.Queue.pop(0)
                if f % 5 == 0:
                    pygame.draw.circle(display_screen, GREEN, x, 2)
                f += 1
            except:
                z = 1
        z = 0
        f = 0
        while z == 0:
            try:
                x = robot2.Queue.pop(0)
                if f % 5 == 0:
                    pygame.draw.circle(display_screen, GREEN, x, 2)
                f += 1
            except:
                z = 1
        z = 0
        f = 0
        while z == 0:
            try:
                x = robot3.Queue.pop(0)
                if f % 5 == 0:
                    pygame.draw.circle(display_screen, GREEN, x, 2)
                f += 1
            except:
                z = 1
        z = 0
        f = 0
        while z == 0:
            try:
                x = robot4.Queue.pop(0)
                if f % 5 == 0:
                    pygame.draw.circle(display_screen, GREEN, x, 2)
                f += 1
            except:
                z = 1
        pygame.display.flip()
        # if robot.capable_disable == 1 or robot2.capable_disable == 1 or robot3.capable_disable == 1 or robot4.capable_disable == 1:
        #     server_text.message_display('')
        # if robot.resource_sharing==0:
        #     server_text.message_display('Resource Sharing Disabled!')
        ##        obj2.rect.center = mousepos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.toggle_fullscreen()
                exit_flag = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_END:
                    pygame.display.toggle_fullscreen()
                    exit_flag = 1

                if event.key == pygame.K_UP:
                    robot.increment[0] = 0

                if event.key == pygame.K_DOWN:
                    robot.increment[0] = 0

                if event.key == pygame.K_LEFT:
                    robot.increment[1] = 0

                if event.key == pygame.K_RIGHT:
                    robot.increment[1] = 0

                if event.key == pygame.K_v:
                    screen_index = screen_index + 1
                    if screen_index > 2:
                        screen_index = 0
                    display_screen = pygame.display.set_mode(screen_sizes[screen_index])

                if event.key == pygame.K_e:
                    if show_path == 1:
                        show_path = 0
                    else:
                        show_path = 1

                if event.key == pygame.K_p:
                    robot.pick_process = 'pick'

                if event.key == pygame.K_o:
                    robot.pick_process = 'place'

                if event.key == pygame.K_c:
                    robo_speed[0] = robo_speed[0] + 5
                    if robo_speed[0] > 10:
                        robo_speed[0] = 1

                if event.key == pygame.K_x:
                    robo_speed[1] = robo_speed[1] + 5
                    if robo_speed[1] > 10:
                        robo_speed[1] = 1

                if event.key == pygame.K_z:
                    robo_speed[2] = robo_speed[2] + 5
                    if robo_speed[2] > 10:
                        robo_speed[2] = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    robot.increment[0] = robo_speed[0]  # + 1

                if event.key == pygame.K_DOWN:
                    robot.increment[0] = -robo_speed[0]  # -1

                if event.key == pygame.K_LEFT:
                    robot.increment[1] = robo_speed[1]  # -1

                if event.key == pygame.K_RIGHT:
                    robot.increment[1] = -robo_speed[1]  # +1

                if event.key == pygame.K_p:
                    robot.increment[2] = -robo_speed[2]  # +1

                if event.key == pygame.K_o:
                    robot.increment[2] = robo_speed[2]  # -1

            # Mouse Button Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mousepos[0] >= SCREEN_WIDTH - 30 and mousepos[0] <= SCREEN_WIDTH:
                    if mousepos[1] >= 0 and mousepos[1] <= 30:
                        pygame.display.toggle_fullscreen()
                        exit_flag = 1
            if event.type == pygame.MOUSEBUTTONUP:
                # --- Input Parameter Value Increment and Decrement
                ##                if mousepos[0] >= 180 and mousepos[0]<= 205:
                ##                    if mousepos[1]>= 64 and mousepos[1]<= 84:
                ##                        pass
                if mousepos[1] >= 64 and mousepos[1] <= 84:
                    # MV
                    if mousepos[0] >= 180 and mousepos[0] <= 205:
                        if robot.capable_available['CA'] == 0:
                            robot.capable_available['CA'] = 1
                        else:
                            robot.capable_available['CA'] = 0
                    if mousepos[0] >= 215 and mousepos[0] <= 240:
                        if robot2.capable_available['CA'] == 0:
                            robot2.capable_available['CA'] = 1
                        else:
                            robot2.capable_available['CA'] = 0
                    if mousepos[0] >= 250 and mousepos[0] <= 275:
                        if robot3.capable_available['CA'] == 0:
                            robot3.capable_available['CA'] = 1
                        else:
                            robot3.capable_available['CA'] = 0
                    if mousepos[0] >= 285 and mousepos[0] <= 310:
                        if robot4.capable_available['CA'] == 0:
                            robot4.capable_available['CA'] = 1
                        else:
                            robot4.capable_available['CA'] = 0
                if mousepos[1] >= 88 and mousepos[1] <= 108:
                    # PP
                    if mousepos[0] >= 180 and mousepos[0] <= 205:
                        if robot.capable_available['MV'] == 0:
                            robot.capable_available['MV'] = 1
                        else:
                            robot.capable_available['MV'] = 0
                    if mousepos[0] >= 215 and mousepos[0] <= 240:
                        if robot2.capable_available['MV'] == 0:
                            robot2.capable_available['MV'] = 1
                        else:
                            robot2.capable_available['MV'] = 0
                    if 250 <= mousepos[0] <= 275:
                        if robot3.capable_available['MV'] == 0:
                            robot3.capable_available['MV'] = 1
                        else:
                            robot3.capable_available['MV'] = 0
                    if 285 <= mousepos[0] <= 310:
                        if robot4.capable_available['MV'] == 0:
                            robot4.capable_available['MV'] = 1
                        else:
                            robot4.capable_available['MV'] = 0
                if mousepos[1] >= 113 and mousepos[1] <= 132:
                    # RD
                    if mousepos[0] >= 180 and mousepos[0] <= 205:
                        if robot.capable_available['CM'] == 0:
                            robot.capable_available['CM'] = 1
                        else:
                            robot.capable_available['CM'] = 0
                    if mousepos[0] >= 215 and mousepos[0] <= 240:
                        if robot2.capable_available['CM'] == 0:
                            robot2.capable_available['CM'] = 1
                        else:
                            robot2.capable_available['CM'] = 0
                    if mousepos[0] >= 250 and mousepos[0] <= 275:
                        if robot3.capable_available['CM'] == 0:
                            robot3.capable_available['CM'] = 1
                        else:
                            robot3.capable_available['CM'] = 0
                    if mousepos[0] >= 285 and mousepos[0] <= 310:
                        if robot4.capable_available['CM'] == 0:
                            robot4.capable_available['CM'] = 1
                        else:
                            robot4.capable_available['CM'] = 0
                if mousepos[1] >= 139 and mousepos[1] <= 159:
                    # RA
                    if mousepos[0] >= 180 and mousepos[0] <= 205:
                        if robot.capable_available['RA'] == 0:
                            robot.capable_available['RA'] = 1
                        else:
                            robot.capable_available['RA'] = 0
                    if mousepos[0] >= 215 and mousepos[0] <= 240:
                        if robot2.capable_available['RA'] == 0:
                            robot2.capable_available['RA'] = 1
                        else:
                            robot2.capable_available['RA'] = 0
                    if mousepos[0] >= 250 and mousepos[0] <= 275:
                        if robot3.capable_available['RA'] == 0:
                            robot3.capable_available['RA'] = 1
                        else:
                            robot3.capable_available['RA'] = 0
                    if mousepos[0] >= 285 and mousepos[0] <= 310:
                        if robot4.capable_available['RA'] == 0:
                            robot4.capable_available['RA'] = 1
                        else:
                            robot4.capable_available['RA'] = 0
                if mousepos[1] >= 164 and mousepos[1] <= 184:
                    # CA
                    if 180 <= mousepos[0] <= 205:
                        if robot.capable_available['OI'] == 0:
                            robot.capable_available['OI'] = 1
                        else:
                            robot.capable_available['OI'] = 0
                    if 215 <= mousepos[0] <= 240:
                        if robot2.capable_available['OI'] == 0:
                            robot2.capable_available['OI'] = 1
                        else:
                            robot2.capable_available['OI'] = 0
                    if mousepos[0] >= 250 and mousepos[0] <= 275:
                        if robot3.capable_available['OI'] == 0:
                            robot3.capable_available['OI'] = 1
                        else:
                            robot3.capable_available['OI'] = 0
                    if mousepos[0] >= 285 and mousepos[0] <= 310:
                        if robot4.capable_available['OI'] == 0:
                            robot4.capable_available['OI'] = 1
                        else:
                            robot4.capable_available['OI'] = 0
                if 208<=mousepos[1] <=220 and 183<=mousepos[0]<=302:
                    if RESOURCE_SHARING==1:
                        RESOURCE_SHARING=0
                    else:
                        RESOURCE_SHARING=1
                    print(RESOURCE_SHARING)

        # background image text
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        # -- Robo Capabilities
        cap_count = 0

        for cap in robot.capable:
            pygame.draw.rect(screen, [255 * (1 - robot.capable_available[cap]), 255 * robot.capable_available[cap], 0],
                             [184, 68 + 25 * cap_count, 15, 13])
            pygame.draw.rect(screen,
                             [255 * (1 - robot2.capable_available[cap]), 255 * robot2.capable_available[cap], 0],
                             [220, 68 + 25 * cap_count, 15, 13])
            pygame.draw.rect(screen,
                             [255 * (1 - robot3.capable_available[cap]), 255 * robot3.capable_available[cap], 0],
                             [255, 68 + 25 * cap_count, 15, 13])
            pygame.draw.rect(screen,
                             [255 * (1 - robot4.capable_available[cap]), 255 * robot4.capable_available[cap], 0],
                             [288, 68 + 25 * cap_count, 15, 13])
            cap_count = cap_count + 1
        pygame.draw.rect(screen,[255*(1-RESOURCE_SHARING),(255*RESOURCE_SHARING),0],[184,209,120,13])
        # -- Capability LED
        led = False
        for cap in robot.capable:
            if robot.capable_available[cap]==0:
                led = True
        if led == True:
            pygame.draw.circle(screen, RED, (robot.pos[0]-58,robot.pos[1]+57), 5)
        else:
            pygame.draw.circle(screen, GREEN, (robot.pos[0] - 58, robot.pos[1] + 57), 5)

        led = False
        for cap in robot2.capable:
            if robot2.capable_available[cap] == 0:
                led = True
        if led == True:
            pygame.draw.circle(screen, RED, (robot2.pos[0] - 58, robot2.pos[1] + 57), 5)
        else:
            pygame.draw.circle(screen, GREEN, (robot2.pos[0] - 58, robot2.pos[1] + 57), 5)

        led = False
        for cap in robot3.capable:
            if robot3.capable_available[cap] == 0:
                led = True
        if led == True:
            pygame.draw.circle(screen, RED, (robot3.pos[0] - 58, robot3.pos[1] + 57), 5)
        else:
            pygame.draw.circle(screen, GREEN, (robot3.pos[0] - 58, robot3.pos[1] + 57), 5)

        led = False
        for cap in robot4.capable:
            if robot4.capable_available[cap] == 0:
                led = True
        if led == True:
            pygame.draw.circle(screen, RED, (robot4.pos[0] - 58, robot4.pos[1] + 57), 5)
        else:
            pygame.draw.circle(screen, GREEN, (robot4.pos[0] - 58, robot4.pos[1] + 57), 5)

        # -- robot Position update
        robot_list.update(block_list, robot_safe_zone_list)

        for robo in robot_list:
            screen.blit(robo.surface, robo.rect)
        robot_safe_zone_list.update()
        # print("Updated list")
        block_list.update()
        block_list.draw(screen)
        #server_sprite.update()
        #server_sprite.draw(screen)
        #new_obj = 1
        #n_polygons = 0
        # for Polygon in block_list:
        #     n_polygons += 1
        # if n_polygons < MAX_POLYGONS:
        #     new_obj = 0

        #if new_obj == 0:
            # print("polygon created")
            # obj = polygon()
            # polygons_hit_list = pygame.sprite.spritecollide(obj, block_list, False)
            # if len(polygons_hit_list) < 1:
            #     n_polygons += 1
            #     block_list.add(obj)
            #     game_objects.add(obj)
        n_polygons= MAX_POLYGONS-red.shape_count - green.shape_count - blue.shape_count
        # -- Text update
        Time=int(time.time()-start_time)
        obj_count = [font.render(str(red.shape_count + green.shape_count + blue.shape_count), True, BLACK),
                     font.render(str(red.shape_count), True, BLACK),
                     font.render(str(green.shape_count), True, BLACK),
                     font.render(str(blue.shape_count), True, BLACK),
                     font.render(str('Time(seconds): '+str(Time)),True,BLACK)]
        ##        robo_speed_text = [font.render( 'Robot Move Speed : '+str(robo_speed[0]), True, BLUE),\
        ##                          font.render( 'Robot Rotate Speed : '+str(robo_speed[1]), True, BLUE),\
        ##                          font.render( 'Arm Rotate Speed : '+str(robo_speed[2]), True, BLUE)]
        # -- Text display
        screen.blit(obj_count[0], [50, 283])
        screen.blit(obj_count[1], [130, 283])
        screen.blit(obj_count[2], [195, 283])
        screen.blit(obj_count[2], [195, 283])
        screen.blit(obj_count[3], [265, 283])
        screen.blit(obj_count[4], [10,325])
        energy=str(int(400-robot.energy-robot2.energy-robot3.energy-robot4.energy))
        # Scenario
        task=mission.split(' ')
        if Time == int(task[0]):
            print("Mission is: ", mission)
            mission_state += 1
            for i in range (2,6):
                try:
                    if task[i][0]=='1':
                        if robot.capable_available[task[1]]==1:
                            robot.capable_available[task[1]]=0
                        else:
                            robot.capable_available[task[1]]=1
                            print('capable available enabled')
                    if task[i][0]=='2':
                        if robot2.capable_available[task[1]]==1:
                            robot2.capable_available[task[1]]=0
                        else:
                            robot2.capable_available[task[1]]=1
                    if task[i][0]=='3':
                        if robot3.capable_available[task[1]]==1:
                            robot3.capable_available[task[1]]=0
                        else:
                            robot3.capable_available[task[1]]=1
                    if task[i][0]=='4':
                        if robot4.capable_available[task[1]]==1:
                            robot4.capable_available[task[1]]=0
                        else:
                            robot4.capable_available[task[1]]=1
                except:
                    pass
        # Energy consumed
        energy_count=font.render(str("Total Energy consumed: "+energy), True, BLACK)
        screen.blit(energy_count,[10,400])
        # Robot energy displays
        i=1
        for Robo in robot_list:
            e=font.render(str("Robot "+str(i)+' energy: '+str(round(Robo.energy,5))),True,BLACK)
            screen.blit(e,[10,450+35*i])
            i+=1
        # Timer display of previous mission
        if previous_time!=0:
            old_time='Without resource sharing: '+str(previous_time)+' s'
            oldtimer=font.render(old_time,True,BLACK)
            screen.blit(oldtimer,[10,350])
            old_energy = 'Without resource sharing: '+str(previous_energy)+ ' E'
            oldenergy=font.render(old_energy,True,BLACK)
            screen.blit(oldenergy,[10,425])
        if n_polygons == 0:
            text=font.render(str('Task complete!'), True, BLACK)
            screen.blit(text, [900, 450])

        # Resource sharing capabilities
        if robot.resource_sharing == True:
            text2 = font.render(str('Search assist is active'), True, GREEN)
            screen.blit(text2, [10, 820])

        screeen_resize = pygame.transform.scale(screen, screen_sizes[screen_index])
        display_screen.blit(screeen_resize, [0, 0])



        # Collision avoidance map
        # for Obj in game_objects:
        #
        #     try:
        #         pos=Obj.pos
        #         pygame.draw.rect(display_screen, RED,[Obj.rect.center[0]-50,Obj.rect.center[1]-50,100,100])
        #         "Not drawing ofc"
        #     except:
        #         pygame.draw.rect(display_screen,BLUE,Obj.rect)
        #     #print("drawing ")

        #--- update the screen
        pygame.display.flip()

        # --- frames per second
        clock.tick(300)
        if n_polygons==0:
            time.sleep(5)
    print("Energy:",energy," Time:",Time)
    return [energy, Time]


if __name__ == "__main__":
    polygons=15
    start_time=time.time()
    Return=main(0,start_time,polygons,0,'0')
    energy=Return[0]
    time_without=Return[1]
    start_time = time.time()
    Return=main(1,start_time,polygons,time_without,energy)

exit_flag = 1

# Close the window and quit.
pygame.quit()
