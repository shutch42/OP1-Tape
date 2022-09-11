import pygame
from buttons import Key, Mod
from gui import GUI
from tape import Tape

# Key bindings are set here. In the future, change this to GPIO pins.
keys = {"Play": Key(pygame.K_SPACE),
        "Stop": Key(pygame.K_BACKSPACE),
        "Record": Key(pygame.K_r),
        "Shift": Mod(pygame.KMOD_SHIFT),
        "Left": Key(pygame.K_LEFT),
        "Right": Key(pygame.K_RIGHT)}

gui = GUI()
tape = Tape()

clock = pygame.time.Clock()

done = False

state = "Stop"
track_manip = "None"

while not done:

    #######################################################################################
    # The scary-looking section below is for handling key presses and tape state changes
    #######################################################################################

    for event in pygame.event.get():
        # Check for exit
        if event.type == pygame.QUIT:
            tape.close()
            done = True

        # Check for temporary states
        if track_manip == "None":
            pass
        elif keys["Record"].pressed() and track_manip == "Record":
            pass
        elif keys["Right"].pressed() and track_manip == "FF":
            pass
        elif keys["Left"].pressed() and track_manip == "RW":
            pass
        else:
            track_manip = "None"
            if state == "Play":
                tape.play()
            elif state == "Reverse":
                tape.reverse()
            elif state == "Pause":
                tape.pause()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            mods = pygame.key.get_mods()

            # Switch out of temporary recording if necessary
            if track_manip == "Record":
                if keys["Shift"].pressed() and keys["Play"].pressed():
                    state = "Reverse and Record"
                    tape.record_reverse()
                elif keys["Play"].pressed():
                    state = "Play and Record"
                    tape.record()

            elif state == "Stop":
                print("Checking moves from state: Stop")
                if keys["Play"].pressed():
                    state = "Play"
                    tape.play()
                elif keys["Record"].pressed():
                    # state = "Arm Record"
                    track_manip = "Record"
                elif keys["Right"].pressed():
                    state = "Pause"
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Play":
                print("Checking moves from state: Play")
                if keys["Play"].pressed() and keys["Shift"].pressed():
                    state = "Reverse"
                    tape.reverse()
                elif keys["Play"].pressed():
                    state = "Pause"
                    tape.pause()
                elif keys["Stop"].pressed():
                    state = "Stop"
                    tape.stop()
                elif keys["Record"].pressed():
                    track_manip = "Record"
                    tape.record()
                elif keys["Left"].pressed():
                    track_manip = "RW"
                    tape.rewind()
                elif keys["Right"].pressed():
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Play and Record":
                if keys["Play"].pressed() and keys["Shift"].pressed():
                    state = "Reverse"
                    tape.reverse()
                elif keys["Play"].pressed():
                    state = "Play"
                    tape.play()
                elif keys["Stop"].pressed():
                    state = "Stop"
                    tape.stop()
                print("Checking moves from state: Play and Record")
            elif state == "Pause":
                print("Checking moves from state: Pause")
                if keys["Play"].pressed() and keys["Shift"].pressed():
                    state = "Reverse"
                    tape.reverse()
                elif keys["Play"].pressed():
                    state = "Play"
                    tape.play()
                elif keys["Stop"].pressed():
                    state = "Stop"
                    tape.stop()
                elif keys["Record"].pressed():
                    # state = "Arm Record"
                    track_manip = "Record"
                elif keys["Left"].pressed():
                    track_manip = "RW"
                    tape.rewind()
                elif keys["Right"].pressed():
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Reverse":
                print("Checking moves from state: Reverse")
                if keys["Play"].pressed() and not keys["Shift"].pressed():
                    state = "Play"
                    tape.play()
                elif keys["Stop"].pressed():
                    state = "Stop"
                    tape.stop()
                elif keys["Record"].pressed():
                    state = "Reverse and Record"
                    tape.record_reverse()
                elif keys["Left"].pressed():
                    track_manip = "RW"
                    tape.rewind()
                elif keys["Right"].pressed():
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Reverse and Record":
                if keys["Play"].pressed() and keys["Shift"].pressed():
                    state = "Reverse"
                    tape.reverse()
                elif keys["Play"].pressed():
                    state = "Play"
                    tape.play()
                elif keys["Stop"].pressed():
                    state = "Stop"
                    tape.stop()
                elif keys["Left"].pressed():
                    state = "RW"
                    tape.rewind()
                elif keys["Right"].pressed():
                    track_manip = "FF"
                    tape.fast_forward()
                print("Checking moves from state: Reverse and Record")
            else:
                raise Exception("State not recognized: "+state)

    #######################################################################################################
    # At this point, the button presses are handled and the updated state should be set
    # Now, we just need to take this state information and display it in the GUI
    # Note: This CANNOT be handled in the states above, since they are only accessed during a button press
    # FIXME: Integrate the gui into the tape class for cleaner code
    #######################################################################################################

    gui.clear_screen()

    if state == "Stop":
        gui.update_clock("00:00:00")
        if track_manip == "Record":
            gui.render_arm_record()
        else:
            gui.render_pause()
    else:
        gui.update_clock(tape.get_time_string())
        if track_manip == "FF":
            gui.render_ff()
        elif track_manip == "RW":
            gui.render_rw()
        elif track_manip == "Record" and state == "Play":
            gui.render_record()
        elif track_manip == "Record" and (state == "Pause" or state == "Stop"):
            gui.render_arm_record()
        elif state == "Play":
            gui.render_play()
        elif state == "Pause":
            gui.render_pause()
        elif state == "Reverse":
            gui.render_reverse()
        elif state == "Play and Record":
            gui.render_record()
        elif state == "Reverse and Record":
            gui.render_record_reverse()
        elif state == "Arm Record":
            gui.render_arm_record()

    gui.display()
    clock.tick(60)
