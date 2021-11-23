import pysubs2
import pathlib,bpy

info = "\x1b[38;2;254;211;48m"
error ="\x1b[38;2;235;59;90;48m"
rs = "\x1b[0m"

def subImport(filepath,  framerate):
    #region inits

    subtitle_exists = False
    subtitles = None
    test_framerate = None
    topmost_channel = None
    editor = None
    box_color = None
    position = None
    box_margin = 0.01
    offset = 0

    file_is_real = False
    file = ""

    if len(filepath)>0:
        file = filepath
        if pathlib.Path(file).is_file():
            file_is_real = True
            if pathlib.Path(file).suffix not in pysubs2.formats.FILE_EXTENSION_TO_FORMAT_IDENTIFIER:
                print(f"{info}Unable to load subs from {pathlib.Path(file).name} {rs}:")
                print(f"{info} - {pathlib.Path(file).suffix} {rs}{error} is not supported by pysubs2 at the moment. If it is, ask for the module to be updated in this addon{rs}!")
                return
        else: file_is_real = False
    else:
        print("No file path or file not found")
        file_is_real = False

    if file_is_real:
        test_framerate = framerate
        editor = bpy.data.scenes[0].sequence_editor

        subtitles = pysubs2.load(file, encoding="utf-8")


        topmost_channel = 0
        for i in range(len(editor.sequences_all)):
            if topmost_channel < editor.sequences_all[i].channel:
                topmost_channel = editor.sequences_all[i].channel

        position = (.5, .1)

        box_color = (0.13,0.13,0.13,.83)
        offset = position[1]
    #endregion

    if file_is_real:

        # Check if we already have imported subtitles in our way - checking for the "Sub." prefix
        for sequence in editor.sequences:
            if sequence.type == 'TEXT':
                if "Sub." in sequence.name:
                    subtitle_exists = True
                    break

        # ----------------- Create -----------------------------------
        if not subtitle_exists:
            for i,line in enumerate(subtitles):
                text = line.text
                start = pysubs2.time.ms_to_frames(line.start, test_framerate)
                end = pysubs2.time.ms_to_frames(line.end, test_framerate)


                if r"\N" in text:
                    edited = text.split(r"\N")
                    editor.sequences.new_effect(f"Sub.{i}-a", "TEXT", topmost_channel + 2, frame_start=start, frame_end=end)
                    editor.sequences.new_effect(f"Sub.{i}-b", "TEXT", topmost_channel + 1, frame_start=start, frame_end=end)

                    editor.sequences_all[f"Sub.{i}-a"].text = edited[0]
                    editor.sequences_all[f"Sub.{i}-b"].text = edited[1]

                    editor.sequences_all[f"Sub.{i}-a"].use_box = True
                    editor.sequences_all[f"Sub.{i}-b"].use_box = True

                    editor.sequences_all[f"Sub.{i}-a"].box_color = box_color
                    editor.sequences_all[f"Sub.{i}-b"].box_color = box_color

                    editor.sequences_all[f"Sub.{i}-a"].location = (position[0],position[1] +(offset - 2*box_margin))
                    editor.sequences_all[f"Sub.{i}-b"].location = position

                else:
                    editor.sequences.new_effect(f"Sub.{i}", "TEXT", topmost_channel + 1, frame_start=start, frame_end=end)
                    editor.sequences_all[f"Sub.{i}"].text = text
                    editor.sequences_all[f"Sub.{i}"].location = position
                    editor.sequences_all[f"Sub.{i}"].use_box = True
                    editor.sequences_all[f"Sub.{i}"].box_color = box_color

                    pass
        # ------------- Update ------------------------------
        else:
            for i,line in enumerate(subtitles):
                text = line.text
                start = pysubs2.time.ms_to_frames(line.start, test_framerate)
                end = pysubs2.time.ms_to_frames(line.end, test_framerate)

                if editor.sequences_all[f"Sub.{i}"]: # Check if there is such Text Sequence
                    # region Did Time change?

                    start_changed = False if editor.sequences_all[f"Sub.{i}"].frame_start == start else True
                    end_changed = False if editor.sequences_all[f"Sub.{i}"].frame_final_end == end else True
                    print(f"for{i} \n\tstart Changed {start_changed} | end changed {end_changed}")
                    # endregion
                    #region Did Text Changed?
                    text_changed = False
                    if r"\N" in text:
                        edited = text.split(r"\N")
                        if edited[0] != editor.sequences_all[f"Sub.{i}-b"].text:
                            text_changed = True
                        if edited[1] != editor.sequences_all[f"Sub.{i}-a"].text:
                            text_changed = True
                        else:
                            text_changed = False
                    else:
                        if text != editor.sequences_all[f"Sub.{i}"].text:
                            text_changed = True
                        else:
                            text_changed = False
                    #endregion

                    if   start_changed and not end_changed and not text_changed:
                        if r"\N" in text:
                            editor.sequences_all[f"Sub.{i}-a"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-a"].frame_final_end = end
                            editor.sequences_all[f"Sub.{i}-b"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-b"].frame_final_end = end
                        else:
                            editor.sequences_all[f"Sub.{i}"].frame_start = start
                            editor.sequences_all[f"Sub.{i}"].frame_final_end = end
                    elif start_changed and end_changed and not text_changed:
                        if r"\N" in text:
                            editor.sequences_all[f"Sub.{i}-a"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-a"].frame_final_end = end
                            editor.sequences_all[f"Sub.{i}-b"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-b"].frame_final_end = end
                        else:
                            editor.sequences_all[f"Sub.{i}"].frame_start = start
                            editor.sequences_all[f"Sub.{i}"].frame_final_end = end
                    elif start_changed and end_changed and text_changed:
                        if r"\N" in text:
                            edited = text.split(r"\N")
                            editor.sequences_all[f"Sub.{i}-a"].text = edited[0]
                            editor.sequences_all[f"Sub.{i}-a"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-a"].frame_final_end = end
                            editor.sequences_all[f"Sub.{i}-b"].text = edited[1]
                            editor.sequences_all[f"Sub.{i}-b"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-b"].frame_final_end = end
                        else:
                            editor.sequences_all[f"Sub.{i}"].text = text
                            editor.sequences_all[f"Sub.{i}"].frame_start = start
                            editor.sequences_all[f"Sub.{i}"].frame_final_end = end
                    elif not start_changed and end_changed and text_changed:
                        if r"\N" in text:
                            edited = text.split(r"\N")
                            editor.sequences_all[f"Sub.{i}-a"].text = edited[0]
                            editor.sequences_all[f"Sub.{i}-a"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-a"].frame_final_end = end
                            editor.sequences_all[f"Sub.{i}-b"].text = edited[1]
                            editor.sequences_all[f"Sub.{i}-b"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-b"].frame_final_end = end
                        else:
                            editor.sequences_all[f"Sub.{i}"].text = text
                            editor.sequences_all[f"Sub.{i}"].frame_start = start
                            editor.sequences_all[f"Sub.{i}"].frame_final_end = end
                    elif not start_changed and end_changed and not text_changed:
                        if r"\N" in text:
                            editor.sequences_all[f"Sub.{i}-a"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-a"].frame_final_end = end
                            editor.sequences_all[f"Sub.{i}-b"].frame_start = start
                            editor.sequences_all[f"Sub.{i}-b"].frame_final_end = end
                        else:
                            editor.sequences_all[f"Sub.{i}"].frame_start = start
                            editor.sequences_all[f"Sub.{i}"].frame_final_end = end
                    elif not start_changed and not end_changed and not text_changed:pass

                else:                               # if there is no longer such text Sequence, create a new one.
                    if r"\N" in text:
                        edited = text.split(r"\N")
                        editor.sequences.new_effect(f"Sub.{i}-a", "TEXT", topmost_channel + 2, frame_start=start,
                                                    frame_end=end)
                        editor.sequences.new_effect(f"Sub.{i}-b", "TEXT", topmost_channel + 1, frame_start=start,
                                                    frame_end=end)

                        editor.sequences_all[f"Sub.{i}-a"].text = edited[0]
                        editor.sequences_all[f"Sub.{i}-b"].text = edited[1]

                        editor.sequences_all[f"Sub.{i}-a"].use_box = True
                        editor.sequences_all[f"Sub.{i}-b"].use_box = True

                        editor.sequences_all[f"Sub.{i}-a"].box_color = box_color
                        editor.sequences_all[f"Sub.{i}-b"].box_color = box_color

                        editor.sequences_all[f"Sub.{i}-a"].location = (
                        position[0], position[1] + (offset - 2 * box_margin))
                        editor.sequences_all[f"Sub.{i}-b"].location = position

                    else:
                        editor.sequences.new_effect(f"Sub.{i}", "TEXT", topmost_channel + 1, frame_start=start,
                                                    frame_end=end)
                        editor.sequences_all[f"Sub.{i}"].text = text
                        editor.sequences_all[f"Sub.{i}"].location = position
                        editor.sequences_all[f"Sub.{i}"].use_box = True
                        editor.sequences_all[f"Sub.{i}"].box_color = box_color



            print(f"Subtitle is already in scene - Updating from file")


def updateSub(pos, font, font_size, boxMargin):
    width = bpy.context.scene.render.resolution_x
    height = bpy.context.scene.render.resolution_y

    margin_to_pixels = boxMargin * width * 2
    font_box = margin_to_pixels + font_size
    doubble_line_offset = (font_box/2)/height

    sequences = [sequence for sequence in bpy.data.scenes[0].sequence_editor.sequences if sequence.type == 'TEXT' and 'Sub.' in sequence.name]

    for i , sequence in enumerate(sequences):
        font_changed = True if font != sequence.font else False
        if "-a" in sequence.name:
            sequence.location = (pos[0], pos[1] + doubble_line_offset)
            sequence.font_size = font_size
            sequence.box_margin = boxMargin
            if font_changed:
                sequence.font = font
        elif "-b" in sequence.name:
            sequence.location = (pos[0], pos[1] - doubble_line_offset)
            sequence.font_size = font_size
            sequence.box_margin = boxMargin
            if font_changed:
                sequence.font = font
        else:
            sequence.location = pos
            sequence.font_size = font_size
            sequence.box_margin = boxMargin
            if font_changed:
                sequence.font = font

