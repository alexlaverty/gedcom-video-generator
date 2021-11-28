from moviepy.editor import * 
import speech
from pathlib import Path

video_width = 1920 
video_height = 1080
pause = 2

def generate_story(element):
    text = ""
    (first, last) = element.get_name()
    text += f"{first} {last}"
    return text

def generate(element):
    clips = []
    title_audio_path = str(Path("assets", element.get_pointer().replace("@","") + ".mp3"))
    narration_text = generate_story(element)
    speech.create_audio(title_audio_path, narration_text)
    title_audio = AudioFileClip(title_audio_path).volumex(2)
    duration = title_audio.duration + pause

    clip_background = TextClip("", size=(video_width,video_height), 
                            bg_color="white", 
                            method="caption")\
                            .set_duration(duration)
    clips.append(clip_background)

    clip_text = TextClip(narration_text, 
                        size=(600,None), 
                        fontsize = 25,
                        bg_color="grey", 
                        align='West',
                        method="caption")\
                        .set_duration(duration)\
                        .set_position((50, 50))\
                        .set_audio(title_audio)

    clip_photo = TextClip(narration_text, 
                        size=(600,None), 
                        fontsize = 25,
                        bg_color="grey", 
                        align='West',
                        method="caption")\
                        .set_duration(duration)\
                        .set_position((50, 50))\
                        .set_audio(title_audio)

    clips.append(clip_text)

    final_video = CompositeVideoClip(clips)
    return final_video

if __name__ == "__main__":

    class Person():
        id = "abc1234"
        name = ("Leonard James", "Laverty")

    text = """Leonard James Laverty was born 10 OCT 1911 at Macksville New South Wales, Australia. 
    his wife was Elsie Pearl McGree.
    Together they had 11 children.
    his father was Denis Michael Laverty.
    his mother was Honora (Nora) Goldspring.
    """
    #person = Person()
    #person_video = vi(person,text)
    #person_video.write_videofile("test.mp4", fps=5)