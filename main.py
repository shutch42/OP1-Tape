import pygame
import buttons
from gui import GUI
from track import Track

gui = GUI()
track = Track()

clock = pygame.time.Clock()

done = False

state = "Stop"

while not done:
    track_manip = "None"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            track.close()
            done = True

        if event.type == pygame.KEYDOWN:
            key = event.key
            mods = pygame.key.get_mods()
            if state == "Stop":
                print("Checking moves from state: Stop")
                if buttons.play_pressed(key):
                    state = "Play"
                    track.play()
                elif buttons.record_pressed(key):
                    state = "Arm Record"
                elif buttons.right_pressed(key):
                    state = "Play"
                    track_manip = "FF"
                    track.fast_forward()
            elif state == "Play":
                print("Checking moves from state: Play")
                if buttons.play_pressed(key) and buttons.shift_pressed(mods):
                    state = "Reverse"
                    # FIXME: Reverse needs to be added in track / switched to rewind
                elif buttons.play_pressed(key):
                    state = "Pause"
                    track.pause()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    track.stop()
                elif buttons.record_pressed(key):
                    state = "Play and Record"
                elif buttons.left_pressed(key):
                    track_manip = "RW"
                    track.reverse()
                elif buttons.right_pressed(key):
                    track_manip = "FF"
                    track.fast_forward()
            elif state == "Play and Record":
                # FIXME: Add this function
                print("Checking moves from state: Play and Record")
            elif state == "Pause":
                print("Checking moves from state: Pause")
                if buttons.play_pressed(key) and buttons.shift_pressed(mods):
                    # FIXME
                    state = "Reverse"
                elif buttons.play_pressed(key):
                    state = "Play"
                    track.play()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    track.stop()
                elif buttons.record_pressed(key):
                    state = "Arm Record"
                elif buttons.left_pressed(key):
                    track_manip = "RW"
                    track.reverse()
                elif buttons.right_pressed(key):
                    track_manip = "FF"
                    track.fast_forward()
            elif state == "Arm Record":
                # FIXME
                print("Checking moves from state: Arm Record")
            elif state == "Reverse":
                print("Checking moves from state: Reverse")
                if buttons.play_pressed(key) and not buttons.shift_pressed(mods):
                    state = "Play"
                    track.play()
                elif buttons.stop_pressed(key):
                    state = "Stop"
                    track.stop()
                elif buttons.record_pressed(key):
                    state = "Reverse and Record"
                elif buttons.left_pressed(key):
                    track_manip = "RW"
                    track.reverse()
                elif buttons.right_pressed(key):
                    track_manip = "FF"
                    track.fast_forward()
            elif state == "Reverse and Record":
                # FIXME
                print("Checking moves from state: Reverse and Record")
            else:
                raise Exception("State not recognized: "+state)


    gui.clear_screen()

    if state == "Stop":
        gui.update_clock("00:00:00")
        gui.render_pause()
    else:
        gui.update_clock(track.get_time_string())
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
    # if stop:
    #     gui.update_clock("00:00:00")
    #     gui.render_pause()
    # else:
    #     gui.update_clock(track.get_time_string())
    #     if play:
    #         gui.render_play()
    #     else:
    #         gui.render_pause()

    gui.display()
    clock.tick(60)
