import pygame
import buttons
from gui import GUI
from tape import Tape

gui = GUI()
tape = Tape()

clock = pygame.time.Clock()

done = False

state = "Stop"
track_manip = "None"

while not done:
    for event in pygame.event.get():
        # Check for exit
        if event.type == pygame.QUIT:
            tape.close()
            done = True

        # Check for fast-forward/rewind states
        if track_manip == "None":
            pass
        elif event.type == pygame.KEYDOWN and buttons.right_pressed(event.key) and track_manip == "FF":
            pass
        elif event.type == pygame.KEYDOWN and buttons.left_pressed(event.key) and track_manip == "RW":
            pass
        else:
            track_manip = "None"
            if state == "Play":
                tape.play()
            elif state == "Reverse":
                tape.reverse()
            elif state == "Pause":
                tape.pause()
            else:
                raise Exception("Track state is not valid after a speed change: " + state)

        # Switch between other tape states determined by key presses
        if event.type == pygame.KEYDOWN:
            key = event.key
            mods = pygame.key.get_mods()

            if state == "Stop":
                print("Checking moves from state: Stop")
                if buttons.play_pressed(key):
                    state = "Play"
                    tape.play()
                elif buttons.record_pressed(key):
                    state = "Arm Record"
                elif buttons.right_pressed(key):
                    state = "Pause"
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Play":
                print("Checking moves from state: Play")
                if buttons.play_pressed(key) and buttons.shift_pressed(mods):
                    state = "Reverse"
                    tape.reverse()
                elif buttons.play_pressed(key):
                    state = "Pause"
                    tape.pause()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    tape.stop()
                elif buttons.record_pressed(key):
                    state = "Play and Record"
                    tape.record()
                elif buttons.left_pressed(key):
                    track_manip = "RW"
                    tape.rewind()
                elif buttons.right_pressed(key):
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Play and Record":
                if buttons.play_pressed(key) and buttons.shift_pressed(mods):
                    state = "Reverse"
                    tape.reverse()
                elif buttons.play_pressed(key):
                    state = "Play"
                    tape.play()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    tape.stop()
                print("Checking moves from state: Play and Record")
            elif state == "Pause":
                print("Checking moves from state: Pause")
                if buttons.play_pressed(key) and buttons.shift_pressed(mods):
                    state = "Reverse"
                    tape.reverse()
                elif buttons.play_pressed(key):
                    state = "Play"
                    tape.play()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    tape.stop()
                elif buttons.record_pressed(key):
                    state = "Arm Record"
                elif buttons.left_pressed(key):
                    track_manip = "RW"
                    tape.rewind()
                elif buttons.right_pressed(key):
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Arm Record":
                # FIXME
                print("Checking moves from state: Arm Record")
            elif state == "Reverse":
                print("Checking moves from state: Reverse")
                if buttons.play_pressed(key) and not buttons.shift_pressed(mods):
                    state = "Play"
                    tape.play()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    tape.stop()
                elif buttons.record_pressed(key):
                    state = "Reverse and Record"
                    tape.record_reverse()
                elif buttons.left_pressed(key):
                    track_manip = "RW"
                    tape.rewind()
                elif buttons.right_pressed(key):
                    track_manip = "FF"
                    tape.fast_forward()
            elif state == "Reverse and Record":
                # FIXME
                if buttons.play_pressed(key) and buttons.shift_pressed(mods):
                    state = "Reverse"
                    tape.reverse()
                elif buttons.play_pressed(key):
                    state = "Play"
                    tape.play()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    tape.stop()
                elif buttons.left_pressed(key):
                    state = "RW"
                    tape.rewind()
                elif buttons.right_pressed(key):
                    track_manip = "FF"
                    tape.fast_forward()
                print("Checking moves from state: Reverse and Record")
            else:
                raise Exception("State not recognized: "+state)

    gui.clear_screen()

    if state == "Stop":
        gui.update_clock("00:00:00")
        gui.render_pause()
    else:
        gui.update_clock(tape.get_time_string())
        if track_manip == "FF":
            gui.render_ff()
        elif track_manip == "RW":
            gui.render_rw()
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

    gui.display()
    clock.tick(60)
