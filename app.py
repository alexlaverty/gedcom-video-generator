from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from moviepy.editor import * 
import speech
from pathlib import Path

clips = []
starting_id = "@I0000@"
video_width = 1920 
video_height = 1080
pause = 1
margin = 40
# Path to your `.ged` file
file_path = 'example.ged'

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)

root_child_elements = gedcom_parser.get_root_child_elements()


def get_obje_path(id):
    for e in root_child_elements:
       # print(e)
        if e.get_pointer() == id:
            for f in e.get_child_elements():
                if f.get_tag() == "FILE":
                    return f.get_value()

def get_file_list(element):
    files = []
    element_children = element.get_child_elements()
    for element in element_children:
        if element.get_tag() == "OBJE":
            print(element)
            files.append(get_obje_path(element.get_value()))
    return files

def get_images(element):
    files = []
    print(" ".join(element.get_name()))
    element_children = element.get_child_elements()
    for element in element_children:
        if element.get_tag() == "OBJE":
            for e in root_child_elements:
            # print(e)
                if e.get_pointer() == element.get_value():
                    for f in e.get_child_elements():
                        if f.get_tag() == "FILE":
                            #print(f.get_value())
                            for t in f.get_child_elements():
                                t_val = ""
                                if t.get_tag() == "TITL":
                                    t_val = t.get_value()
                                    for c in t.get_child_elements():
                                        if c.get_tag() == "CONC":
                                            t_val += c.get_value()
                                    
                            files.append({'path':f.get_value(),'description':t_val})
    return files





def generate_story(element):
    text = ""
    (first, last) = element.get_name()
    #firstname = first.split(" ")[0]
    text += f"{first} {last}"
    
    (first, last) = element.get_name()

    fullname = " ".join(element.get_name())

    birth_data = element.get_birth_data()
    birth_year = element.get_birth_year()
    birth_date = birth_data[0] if 0 < len(birth_data) else None
    birth_place = birth_data[1] if 1 < len(birth_data) else None
    if birth_date:
        text += f" was born in {birth_year}"
    if birth_place:
        text += f", {birth_place}"
    text += ".\n"

    #spouse = get_spouse(element)


    return text

def get_clip(name, element, image, text):
    print("image")
    print(image)

    title_audio_path = str(Path("assets", element.get_pointer().replace("@","") + "_" + name + ".mp3"))
    speech.create_audio(title_audio_path, text)
    title_audio = AudioFileClip(title_audio_path).volumex(2)
    duration = title_audio.duration + pause
    scene_clips = []

    clip_background = TextClip("", size=(video_width,video_height), 
                            bg_color="white", 
                            method="caption")\
                            .set_duration(duration)
    scene_clips.append(clip_background)

    background_file = str(Path("assets", "background01.jpg"))
    clip_background_photo = ImageClip(background_file)\
                            .set_duration(duration)\
                            .set_position(("center","center"))\
                            .resize(width=video_width)                             
    scene_clips.append(clip_background_photo)

    clip_photo = ImageClip(image)\
                            .set_duration(duration)\
                            .set_position((0 + margin,"center"))\
                            .resize(width=video_width/2 - margin)
    clip_photo_with_borders = clip_photo.margin(top=20, left=20, right=20, bottom=80, color=(255, 255, 255))                           
    scene_clips.append(clip_photo_with_borders)

    clip_text = TextClip(text, 
                        size=(video_width/2 - 200,None), 
                        fontsize = 35,
                        color="#3D2918",
                        bg_color="#D4C1A6", 
                        align='center',
                        font='Georgia',
                        method="caption")\
                        .set_duration(duration)\
                        .set_position((video_width/2 + 100,"center"))\
                        .set_audio(title_audio)\
                        .margin(top=2, left=2, right=2, bottom=2, color=(178, 144, 103))     

    scene_clips.append(clip_text)
    scene = CompositeVideoClip(scene_clips)
    return scene

def get_individual_clips(element):
    iclips = []
    image_list = get_images(element)

    image = image_list[0]['path']
    text = generate_story(element)

    default_story_clip = get_clip("default",element, image, text)
    iclips.append(default_story_clip)
    del image_list[0]

    for count, image in enumerate(image_list):
        iclips.append(get_clip(str(count), element, image['path'], image['description']))

    return iclips


def process_individual(element):
    (first, last) = element.get_name()
    print(first + " " + last)
  
    individual_clips = get_individual_clips(element)
    for individual_clip in individual_clips:
        clips.append(individual_clip)

    parents = gedcom_parser.get_parents(element)
    for parent in parents:
        if parent.get_gender() == "M":
            print("processing father")
            process_individual(parent)

# Iterate through all root child elements
for element in root_child_elements:
    if isinstance(element, IndividualElement):
        if starting_id == element.get_pointer():
            process_individual(element)

final_clip = concatenate_videoclips(clips)
video_final_path = str(Path("final.mp4"))

musicfile = AudioFileClip("music.mp3")
musicclip = afx.audio_loop(musicfile, duration=final_clip.duration)
#final_video = final_clip.set_audio(audioclip)
final_audio = CompositeAudioClip([final_clip.audio.volumex(1), musicclip.volumex(0.6)])
final_video = final_clip.set_audio(final_audio)

final_video.write_videofile(video_final_path, fps=5)