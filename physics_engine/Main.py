import pygame, sys, math, tkinter

from Assets.forumulas import formulas as formula

print(
    'all code can be found on https://github.com/JGreyScales/School-11/tree/main/physics_engine',
    '\n\n' + '-' * 50 +
    '\nThe following program is a simple to use physics engine.'
    '\nJust start by clicking or clicking and draging around the screen to summon or grab the block,' 
    '\nafter this you can throw the block around or drop it, by unclicking. You can also change the gravity, mass, and air drag in the simulation by clicking the appropirate button and changing the value in the console.'
)

# function definements
formula = formula()

root = tkinter.Tk()
root.withdraw()


# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()


# Set up the window.
start_width, start_height = round(root.winfo_screenwidth() * 0.9), round(root.winfo_screenheight() * 0.9)
windowSurface = pygame.display.set_mode((start_width, start_height), pygame.RESIZABLE)
pygame.display.set_caption('Physics engine')
current_width = start_width
current_height = start_height




def gameloop():
    global current_height, current_width
    ## defines player start position and size (Width, Height)
    player = pygame.Rect(current_width // 2, current_height // 2, 20, 20)
    # UI
    width_size, height_size = 1,1

    #velocity
    vertical_velocity = 0
    horizontal_velocity = 0
    
    # is a counter for when to reset velocity
    velocity_reset_tick = 0

    #acceleration
    acceleration_count = 0
    acceleration_list = []
    acceleration = 0

    #displacement
    current_pos = player.center
    old_pos = (0, 0)
    displacement = 0.1
    # is a counter to reset displacement amount
    tick_count_displacement = 0

    #gravity
    mass = 300  #
    delta_time = 0.0
    gravity_acceleration = 9.81  #
    velocity = 0
    air_density = 1.225  #
    projected_area = math.sqrt(list(player)[2] * list(player)[3])
    terminal_velocity = formula.calculate_terminal_velocity(
        mass, gravity_acceleration, 1.05, air_density, projected_area)

    #font to use for entire game
    font = pygame.font.Font('freesansbold.ttf', 15)
    button_font = pygame.font.Font('freesansbold.ttf', 10)

    # temp strings to increase range of list
    screens = [
        'Time_delta', 'Gravity Acceleration', 'Displacement', 'acceleration',
        'GA', 'MS', 'AD'
    ]

    # these screens in milliseconds not in frames so must be redefined before the render is called
    screens[2] = [
        font.render('Displacement between frames:' + str(displacement), True,
                    (0, 0, 0)), (0, 30)
    ]
    screens[3] = [
        font.render(f'Average Velocity is: {acceleration}pixels/2.5seconds',
                    True, (128, 45, 45)), (0, 45)
    ]

    # gets the amount of ticks that occured last frame
    get_ticks_last_frame = pygame.time.get_ticks()



    #main gameloop
    while True:
        current_pos = player.center
        box_width, box_height = 56, 26

        b1 = pygame.Rect(current_width - 63, 7, box_width, box_height)
        b2 = pygame.Rect(current_width - 63, 42, box_width, box_height)
        b3 = pygame.Rect(current_width - 63, 77, box_width, box_height)


        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.WINDOWSIZECHANGED:
                current_width = windowSurface.get_size()[0]
                current_height = windowSurface.get_size()[1]
                width_size, height_size = current_width / start_width, current_height / start_height
                if height_size < 0:
                    height_size = formula.inverse(10 / height_size)
                if width_size < 0:
                    width_size = formula.inverse(10 / width_size) + 1

                font = pygame.font.Font('freesansbold.ttf', round(15 * (width_size * height_size)))
                button_font = pygame.font.Font('freesansbold.ttf', round(10 * (width_size * height_size)))

            #updates cube onto mouse position
            if event.type == pygame.MOUSEBUTTONDOWN:
                #updates variable and recalculates terminal_velocity

                if b1.collidepoint(event.pos):
                    try:
                        gravity_acceleration = float(
                            input(
                                "What do you want the Gravity Acceleration to be? "
                            ))
                        
                    except (ValueError):
                        print('Please use a float')

                elif b2.collidepoint(event.pos):
                  while True:
                    try:
                        mass = float(
                            input("What do you want the Mass to be? "))
                        if mass < 1:
                          continue
                        break
            
                    except (ValueError):
                        print('please use a float')

                elif b3.collidepoint(event.pos):
                  while True:
                    try:
                        air_density = float(
                            input("What do you want the Air Density to be? "))
                        if air_density < 1:
                          continue
                        break

                    except (ValueError):
                        print('please use a float')

                # physics object or "player" will move to mouse position and resets the velocity on object
                else:
                    player.center = pygame.mouse.get_pos()
                    velocity = 0
                    vertical_velocity = 0
                    horizontal_velocity = 0
                    
                terminal_velocity = formula.calculate_terminal_velocity(
                mass, gravity_acceleration, 1.05, air_density,
                projected_area)

            # checks if player is holding down left click
        if pygame.mouse.get_pressed()[0]:
            player.center = pygame.mouse.get_pos()
            velocity = 0
            vertical_velocity = 0
            horizontal_velocity = 0
            movement = pygame.mouse.get_rel() 
            if movement != (0, 0):
              vertical_velocity = movement[1]
              horizontal_velocity = movement[0]
            
        else:
          if vertical_velocity != 0:
            if vertical_velocity > 0 :
              player.y += vertical_velocity
              vertical_velocity -= air_density + gravity_acceleration

            else:
              player.y += vertical_velocity
              vertical_velocity += gravity_acceleration * air_density
              if vertical_velocity >= 0:
                vertical_velocity = 0
          if horizontal_velocity != 0:
            if horizontal_velocity > 0:
              player.x += horizontal_velocity / 1.5
              horizontal_velocity -= air_density
              if horizontal_velocity <= 0:
                horizontal_velocity = 0
            else:
              player.x += horizontal_velocity / 1.5
              horizontal_velocity += air_density + gravity_acceleration
              if horizontal_velocity >= 0:
               horizontal_velocity = 0


          #code to reset velocities if not movng
          if old_pos == current_pos and velocity_reset_tick > 0.3: 
            vertical_velocity = 0
            horizontal_velocity = 0
            velocity_reset_tick = 0

          

        # if the player is not on the bottom of the screen
        if player.bottom < current_height:

            # if velocity has hit or is equal to terminal_velocity
            if velocity <= -terminal_velocity:
                velocity = -terminal_velocity * delta_time
                player.y -= velocity

                # if velocity is less then terminal_velocity
            elif velocity > -terminal_velocity:
                velocity -= gravity_acceleration * delta_time / 1.05
                player.y -= velocity

        # is a check to stop clipping through the bottom of the screen
        elif player.bottom > current_height:
            player.bottom = current_height

        if player.right > current_width:
            player.right = current_width

        elif player.left < 0:
            player.left = 0

        # basic time delta script to calculate the delta between frames
        t = pygame.time.get_ticks()
        delta_time = (t - get_ticks_last_frame) / 1000.0
        get_ticks_last_frame = t

        tick_count_displacement += delta_time
        acceleration_count += delta_time
        velocity_reset_tick += delta_time

        # Draw the white background onto the surface.
        windowSurface.fill((255, 255, 255))

        # calculates the displacement between frames
        displacement = math.sqrt((current_pos[0] - old_pos[0])**2 +
                                 (current_pos[1] - old_pos[1])**2)
        if displacement != 0:
            if displacement < -0:
                acceleration_list.append(formula.inverse(displacement))

            else:
                acceleration_list.append(displacement)
        old_pos = current_pos

        # every 2.5 seconds will update the average accelearation the physiscs object has moved in pixels
        if acceleration_count > 2.5:

            for displacement in acceleration_list:
                acceleration += displacement

            if len(acceleration_list) != 0:
                acceleration /= len(acceleration_list)
                acceleration = round(acceleration / 2.5, 2)

            else:
                acceleration = 0

            screens[3] = [
                font.render(
                    f'Average Acceleration is: {acceleration}pixels/2.5seconds',
                    True, (128, 0, 0)), (0, round(45 * (width_size * height_size)))
            ]

            acceleration_list = []
            acceleration_count = 0
  
            #button creation
        bd1 = pygame.Rect((current_width - 65), 5, 60, 30)

        bd2 = pygame.Rect(current_width - 65, 40, 60, 30)

        bd3 = pygame.Rect(current_width - 65, 75, 60, 30)

        # Draw the player onto the surface.
        pygame.draw.rect(windowSurface, (0, 0, 0), player)
        #updates text on screen blits
        screens[0] = [
            font.render('Delta Time:' + str(delta_time), True, (0, 0, 0)),
            (0, 0)
        ]
        screens[1] = [
            font.render('Gravity Acceleration:' + str(gravity_acceleration),
                        True, (0, 0, 0)), (0, round(15 * (width_size * height_size)))
        ]

        #updates displacement on change or every 0.35 seconds
        if displacement > 3 or displacement < 0 or tick_count_displacement > 0.35:
            screens[2] = [
                font.render(
                    'Displacement between frames:' +
                    str(round(displacement, 2)), True, (0, 0, 0)), (0, round(30 * (width_size * height_size)))
            ]

            tick_count_displacement = 0

    # font rendering for buttons
        screens[4] = [
            button_font.render('Gravity', True, (0, 0, 0)),
            (b1.centerx - 15, b1.centery - 5)
        ]
        screens[5] = [
            button_font.render(f'Mass: {round(mass)} ', True, (0, 0, 0)),
            (b2.centerx - 24, b2.centery - 5)
        ]
        screens[6] = [
            button_font.render('Air Drag', True, (0, 0, 0)),
            (b3.centerx - 20, b3.centery - 5)
        ]

        #renders buttons on the screen
        pygame.draw.rect(windowSurface, (0, 0, 0), bd1)
        pygame.draw.rect(windowSurface, (255, 255, 255), b1)

        pygame.draw.rect(windowSurface, (0, 0, 0), bd2)
        pygame.draw.rect(windowSurface, (255, 255, 255), b2)

        pygame.draw.rect(windowSurface, (0, 0, 0), bd3)
        pygame.draw.rect(windowSurface, (255, 255, 255), b3)

        # render loop (will iterate through all items that need to be rendered and render them)
        for i in range(len(screens)):
          windowSurface.blit(screens[i][0], screens[i][1])


            # Draw the window onto the screen.
        pygame.display.update()
        mainClock.tick(70)
            
# init of gameloop
gameloop()