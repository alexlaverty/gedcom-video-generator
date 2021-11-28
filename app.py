from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from moviepy.editor import * 
import speech
from pathlib import Path

clips = []
starting_id = "@I0000@"
video_width = 1920 
video_height = 1080
pause = 2

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
            #print(element.get_value())
            files.append(get_obje_path(element.get_value()))
    return files

def process(element):
    (first, last) = element.get_name()
    print(first + " " + last)
    
    person_clip = generate(element)
    clips.append(person_clip)


    parents = gedcom_parser.get_parents(element)
    for parent in parents:
        if parent.get_gender() == "M":
            process(parent)



def generate_story(element):
    text = ""
    (first, last) = element.get_name()
    #firstname = first.split(" ")[0]
    text += f"{first} {last}"
    
    (first, last) = element.get_name()

    fullname = " ".join(element.get_name())

    birth_data = element.get_birth_data()
    birth_date = birth_data[0] if 0 < len(birth_data) else None
    birth_place = birth_data[1] if 1 < len(birth_data) else None
    if birth_date:
        text += f" was born on {birth_date}"
    if birth_place:
        text += f", {birth_place}"
    text += ".\n"

    parents = gedcom_parser.get_parents(element)
    father = ""
    mother = ""
    for parent in parents:
        if parent.get_gender() == "M":
            father = " ".join(parent.get_name())
        if parent.get_gender() == "F":
            mother = " ".join(parent.get_name())
    if parents:
        if father:
            text += f"{first}'s father is {father}.\n"
        if mother:
            text += f"{first}'s mother is {mother}.\n"

    return text

def generate(element):
    clips = []
    title_audio_path = str(Path("assets", element.get_pointer().replace("@","") + ".mp3"))
    narration_text = generate_story(element)
    speech.create_audio(title_audio_path, narration_text)
    title_audio = AudioFileClip(title_audio_path).volumex(2)
    duration = title_audio.duration + pause
    file_list = get_file_list(element)
    (firstname, surname) = element.get_name()
    
    clip_background = TextClip("", size=(video_width,video_height), 
                            bg_color="white", 
                            method="caption")\
                            .set_duration(duration)
    clips.append(clip_background)

    if file_list:
        clip_photo = ImageClip(file_list[0])\
                                .set_duration(duration)\
                                .set_position(("left","center"))\
                                .resize(width=500,height=None)                             
        clips.append(clip_photo)

    clip_name = TextClip(f"{firstname} {surname}", 
                        size=(600,None), 
                        fontsize = 30,
                        bg_color="grey", 
                        align='West',
                        method="caption")\
                        .set_duration(duration)\
                        .set_position(("left", 50))\
                        .set_audio(title_audio)
    clips.append(clip_name)

    clip_text = TextClip(narration_text, 
                        size=(800,None), 
                        fontsize = 30,
                        bg_color="grey", 
                        align='West',
                        method="caption")\
                        .set_duration(duration)\
                        .set_position(("right","center"))\
                        .set_audio(title_audio)
    clips.append(clip_text)

    final_video = CompositeVideoClip(clips)
    return final_video


# Iterate through all root child elements
for element in root_child_elements:
    if isinstance(element, IndividualElement):
        if starting_id == element.get_pointer():
            process(element)

final_clip = concatenate_videoclips(clips)
video_final_path = str(Path("final.mp4"))
final_clip.write_videofile(video_final_path, fps=5)