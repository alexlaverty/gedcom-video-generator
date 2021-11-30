from moviepy.editor import * 
import speech
from pathlib import Path

video_width = 1920 
video_height = 1080
pause = 2
margin = 40

def get_orientation(image):
    if image.h > image.w:
        return False
    else:
        return True

def get_family_intro_clip(filename, text, image=None):

    title_audio_path = str(Path("assets", filename + ".mp3"))
    speech_family_intro_text = "The family of " + text
    speech.create_audio(title_audio_path, speech_family_intro_text)
    title_audio = AudioFileClip(title_audio_path).volumex(2)
    duration = title_audio.duration + pause
    scene_clips = []

    clip_background = TextClip("", size=(video_width,video_height), 
                            bg_color="#2F2723", 
                            method="caption")\
                            .set_duration(duration)
    scene_clips.append(clip_background)

    clip_foreground = TextClip("", size=(video_width,video_height - 400), 
                            bg_color="#DCC9AF", 
                            method="caption")\
                            .set_duration(duration)\
                            .set_position(("center","center"))
    scene_clips.append(clip_foreground)

    # background_file = str(Path("assets", "background01.jpg"))
    # clip_background_photo = ImageClip(background_file)\
    #                         .set_duration(duration)\
    #                         .set_position(("center","center"))\
    #                         .resize(width=video_width)                             
    #scene_clips.append(clip_background_photo)
    if image:
        clip_photo = ImageClip(image)\
                                .set_duration(duration)\
                                .set_position((0 + margin,"center"))
                                
        orientation_is_landscape = get_orientation(clip_photo)

        if orientation_is_landscape:
            clip_photo = clip_photo.resize(width=video_width/2 - margin)
        else:
            clip_photo = clip_photo.resize(height=video_height - 100)

        clip_photo_with_borders = clip_photo.margin(top=20, left=20, right=20, bottom=80, color=(255, 255, 255))                           
        scene_clips.append(clip_photo_with_borders)

    clip_text_family_of = TextClip("The Family Of", 
                        #size=(video_width/2 - 200,None), 
                        fontsize = 45,
                        color="#3D2918",
                        #bg_color="#D4C1A6", 
                        align='center',
                        font='Georgia')\
                        .set_duration(duration)\
                        .set_position(("center", video_height / 2 - 200))\
                        .set_audio(title_audio)
                        #.margin(top=2, left=2, right=2, bottom=2, color=(178, 144, 103))
    scene_clips.append(clip_text_family_of)

    clip_text = TextClip(text, 
                        #size=(video_width/2 - 200,None), 
                        fontsize = 55,
                        color="#3D2918",
                        #bg_color="#D4C1A6", 
                        align='center',
                        font='Georgia-Bold')\
                        .set_duration(duration)\
                        .set_position(("center","center"))\
                        .set_audio(title_audio)
                        #.margin(top=2, left=2, right=2, bottom=2, color=(178, 144, 103))
                        

    scene_clips.append(clip_text)
    scene = CompositeVideoClip(scene_clips)
    return scene

def get_clip(filename, text, image=None):

    title_audio_path = str(Path("assets", filename + ".mp3"))
    speech.create_audio(title_audio_path, text)
    title_audio = AudioFileClip(title_audio_path).volumex(2)
    duration = title_audio.duration + pause
    scene_clips = []

    clip_background = TextClip("", size=(video_width,video_height), 
                            bg_color="#2F2723", 
                            method="caption")\
                            .set_duration(duration)
    scene_clips.append(clip_background)

    clip_foreground = TextClip("", size=(video_width,video_height - 400), 
                            bg_color="#DCC9AF", 
                            method="caption")\
                            .set_duration(duration)\
                            .set_position(("center","center"))
    scene_clips.append(clip_foreground)

    # background_file = str(Path("assets", "background01.jpg"))
    # clip_background_photo = ImageClip(background_file)\
    #                         .set_duration(duration)\
    #                         .set_position(("center","center"))\
    #                         .resize(width=video_width)                             
    #scene_clips.append(clip_background_photo)
    if image:
        clip_photo = ImageClip(image)\
                                .set_duration(duration)\
                                .set_position((0 + margin,"center"))
                                
        orientation_is_landscape = get_orientation(clip_photo)

        if orientation_is_landscape:
            clip_photo = clip_photo.resize(width=video_width/2 - margin)
        else:
            clip_photo = clip_photo.resize(height=video_height - 100)

        clip_photo_with_borders = clip_photo.margin(top=20, left=20, right=20, bottom=80, color=(255, 255, 255))                           
        scene_clips.append(clip_photo_with_borders)

    clip_text = TextClip(text, 
                        size=(video_width/2 - 200,None), 
                        fontsize = 45,
                        color="#3D2918",
                        #bg_color="#D4C1A6", 
                        align='center',
                        font='Georgia',
                        method="caption")\
                        .set_duration(duration)\
                        .set_position((video_width/2 + 100,"center"))\
                        .set_audio(title_audio)#\
                        #.margin(top=2, left=2, right=2, bottom=2, color=(178, 144, 103))     

    scene_clips.append(clip_text)
    scene = CompositeVideoClip(scene_clips)
    return scene

