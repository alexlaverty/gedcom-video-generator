from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser
from moviepy.editor import * 
import speech
from pathlib import Path
import logging 
import gedcom.tags
import video

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

file_path = 'C:\\Users\\laverty\\Documents\\gedcom-video-laverty\\laverty.ged'
family_list = []
gedcom_parser = Parser()
gedcom_parser.parse_file(file_path)
root_child_elements = gedcom_parser.get_root_child_elements()

def get_individual_from_id(id):
    for element in root_child_elements:
        if isinstance(element, IndividualElement):
            if element.get_pointer() == id:
                return element

def get_family_from_id(id):
    for element in root_child_elements:
        if isinstance(element, FamilyElement):
            if element.get_pointer() == id:
                return element

def get_family_from_individual(individual):
    return gedcom_parser.get_families(individual)


# starting_families = gedcom_parser.get_families(starting_individual)

# if starting_families:
#     for family in starting_families:
#         family_list.append(family)
#         #starting_family_elements = family.get_child_elements()


# def get_descendant_families(individual):
#     descendant_families = []
#     starting_family = get_family_from_individual(individual)
#     descendant_families.append(starting_family)
#     children_families = get_children_families(starting_family)

#     return descendant_families

# for e in starting_family_elements:
#     #print(e.get_tag())
#     family_element = get_individual_from_id( e.get_value() )
#     if family_element:
#         print(family_element.get_name())
#         if e.get_tag() == "CHIL":
#             person_families = gedcom_parser.get_families(family_element)
#             for person_family in person_families:
#                 family_list.append(person_family)

def get_children(individual):
    """Return elements corresponding to parents of an individual
    Optional parent_type. Default "ALL" returns all parents. "NAT" can be
    used to specify only natural (genetic) parents.
    :type individual: IndividualElement
    :type parent_type: str
    :rtype: list of IndividualElement
    """

    children = []
    families = gedcom_parser.get_families(individual, gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE)

    for family in families:
        children += gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_CHILD)
        # for family_member in family_members:
        #     print(family_member.get_tag())

    return children

def get_descendants( individual):
    """Return elements corresponding to ancestors of an individual
    Optional `ancestor_type`. Default "ALL" returns all ancestors, "NAT" can be
    used to specify only natural (genetic) ancestors.
    :type individual: IndividualElement
    :type ancestor_type: str
    :rtype: list of Element
    """

    children = get_children(individual)
    descendants = []
    descendants.extend(children)

    for child in children:
        descendants.extend(get_descendants(child))
        #print(descendants)

    return descendants

# def get_descendant_families(family):
#     families = []

#     children = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_CHILD)

#     for child in children:
#         #print(child)
#         family_spouse = gedcom_parser.get_families(child, gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE)
#         families.extend(family_spouse)

#     return families

def get_descendant_families(family):
    family_list = []
    family_list.append(family)
    # father = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_HUSBAND)
    # mother = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_WIFE)
    children = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_CHILD)
    # if father:
    #     print("father : " + " ".join(father[0].get_name()) )
    # if mother:
    #     print("mother : " + " ".join(mother[0].get_name()) )
    for child in children:
        #print("child : " + " ".join(child.get_name()) )
        family_spouse = gedcom_parser.get_families(child, gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE)
        # if family_spouse:
        #     print("Skipping Clip")
        # else:
        #     print("Create Clip")
        for f in family_spouse:
            family_list.extend(get_descendant_families(f))
    return family_list


def get_individual_gallery_files(element):
    files = []
    element_children = element.get_child_elements()
    for element in element_children:
        if element.get_tag() == "OBJE":
            for e in root_child_elements:
                if e.get_pointer() == element.get_value():
                    for f in e.get_child_elements():
                        if f.get_tag() == "FILE":
                            for t in f.get_child_elements():
                                t_val = ""
                                if t.get_tag() == "TITL":
                                    t_val = t.get_value()
                                    for c in t.get_child_elements():
                                        if c.get_tag() == "CONC":
                                            t_val += c.get_value()
                                    
                            files.append({'path':f.get_value(),'description':t_val})
    return files

def get_individual_clips(individual):
    individual_clips = []

    individual_gallery_files = get_individual_gallery_files(individual)
    individual_profile_photo = None
    individual_fullname = " ".join(individual.get_name())
    individual_shortname = individual_fullname.split(" ")[0]

    if individual_gallery_files:
        individual_profile_photo = individual_gallery_files[0]['path']

    individual_default_text = f"{individual_fullname}\n "

    individual_birth_year = individual.get_birth_year()

    if individual_birth_year != -1:
        individual_default_text += f"was born in {individual_birth_year}\n "

    individual_default_clip = video.get_clip(f"{individual.get_pointer()}_default", individual_default_text, image=individual_profile_photo)

    individual_clips.append(individual_default_clip)

    return individual_clips


def get_family_clips(family):
    print("------------------------")
    #print(family)
    family_clips = []
    father = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_HUSBAND)
    mother = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_WIFE)
    children = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_CHILD)
    
    father_fullname = " ".join(father[0].get_name())
    mother_fullname = " ".join(mother[0].get_name())
    father_shortname = father_fullname.split(" ")[0]
    mother_shortname = mother_fullname.split(" ")[0]

    family_intro_text = f"{father_fullname}\n and \n{mother_fullname}"
    print(family_intro_text)
    family_intro = video.get_family_intro_clip("family_intro", family_intro_text, image=None)
    family_clips.append(family_intro)

    father_clip = get_individual_clips(father[0])
    family_clips.extend(father_clip)

    mother_clip = get_individual_clips(mother[0])
    family_clips.extend(mother_clip)

    number_of_children = len(children)
    if number_of_children > 0:
        child_word = "children"
        if number_of_children == 1:
            child_word = "child"
        children_text = f"Together they had {number_of_children} {child_word}.\n"

        for child in children:
            children_text += child.get_name()[0].split(" ")[0] + ", "
        children_text = children_text.rstrip(', ')

        children_clip = video.get_clip(f"{father_fullname}_children", children_text, image=None)
        family_clips.append(children_clip)

    father_gallery_files = get_individual_gallery_files(father[0])
    if len(father_gallery_files) > 1:
        del father_gallery_files[0]
        for count, father_gallery_file in enumerate(father_gallery_files):
            father_gallery_clip = video.get_clip(father_fullname + str(count), father_gallery_file['description'], image=father_gallery_file['path'])
            family_clips.append(father_gallery_clip)

    mother_gallery_files = get_individual_gallery_files(mother[0])
    if len(mother_gallery_files) > 1:
        del mother_gallery_files[0]
        for count, mother_gallery_file in enumerate(mother_gallery_files):
            mother_gallery_clip = video.get_clip(mother_fullname + str(count), mother_gallery_file['description'], image=mother_gallery_file['path'])
            family_clips.append(mother_gallery_clip)

    # father_death_year = father[0].get_death_year()
    # if father_death_year != -1:
    #     print(father_shortname + " passed away in " + str(father_death_year) )

    # mother_death_year = mother[0].get_death_year()
    # if mother_death_year != -1:
    #     print(mother_shortname + " passed away in " + str(mother_death_year) )

    return family_clips

if __name__ == "__main__":
    clips = []
    starting_id = "@I0007@"
    #starting_id = "@I282315998674@"
    #starting_id = "@I282315998663@"
    starting_family = "@F0002@"

    starting_individual = get_individual_from_id(starting_id)

    # descendants = get_descendants(starting_individual)
    # for descendant in descendants:
    #     print(descendant.get_name())

    starting_families = get_family_from_individual(starting_individual)
    descendant_families = get_descendant_families(starting_families[0])

    for family in descendant_families:
        family_clips = get_family_clips(family)
        for family_clip in family_clips:
            clips.append(family_clip)

    if clips:
        final_clip = concatenate_videoclips(clips)
        video_final_path = str(Path("descendants.mp4"))

        musicfile = AudioFileClip("music.mp3")
        musicclip = afx.audio_loop(musicfile, duration=final_clip.duration)
        #final_video = final_clip.set_audio(audioclip)
        final_audio = CompositeAudioClip([final_clip.audio.volumex(1), musicclip.volumex(0.6)])
        final_video = final_clip.set_audio(final_audio)

        final_video.write_videofile(video_final_path, fps=5)
    else:
        print("No Clips Generated!")