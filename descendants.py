from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser
from moviepy.editor import * 
import speech
from pathlib import Path
import logging 
import gedcom.tags

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

file_path = 'C:\\Users\\laverty\\Documents\\gedcom-video-laverty\\laverty_full.ged'
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

# def process_families(family):
#     family_list = []
#     family_list.append(family)

#     father = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_HUSBAND)
#     mother = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_WIFE)
#     children = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_CHILD)
#     father_fullname = " ".join(father[0].get_name())
#     mother_fullname = " ".join(mother[0].get_name())

#     print(f"The family of {father_fullname} and {mother_fullname}")
#     for child in children:
#         print("child : " + " ".join(child.get_name()) )
#         family_spouse = gedcom_parser.get_families(child, gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE)
#         if family_spouse:
#             print("Skipping Clip")
#         else:
#             print("Create Clip")
#         for f in family_spouse:
#             family_list.extend(process_families(f))
#     return family_list

def get_family_clips(family):
    print("------------------------")
    #print(family)
    father = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_HUSBAND)
    mother = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_WIFE)
    children = gedcom_parser.get_family_members(family, gedcom.tags.GEDCOM_TAG_CHILD)
    
    father_fullname = " ".join(father[0].get_name())
    mother_fullname = " ".join(mother[0].get_name())
    father_shortname = father_fullname.split(" ")[0]
    mother_shortname = mother_fullname.split(" ")[0]

    print(f"The family of {father_fullname} and {mother_fullname}")

    father_birth_year = father[0].get_birth_year()
    if father_birth_year != -1:
        print(father_shortname + " was born in " + str(father[0].get_birth_year()) )

    mother_birth_year = mother[0].get_birth_year()
    if mother_birth_year != -1:
        print(mother_shortname + " was born in " + str(mother[0].get_birth_year()) )

    number_of_children = len(children)
    if number_of_children > 0:
        print(f"Together they had a total of {number_of_children} children.")
    for child in children:
        print("* " + child.get_name()[0].split(" ")[0] )

    father_death_year = father[0].get_death_year()
    if father_death_year != -1:
        print(father_shortname + " passed away in " + str(father_death_year) )

    mother_death_year = mother[0].get_death_year()
    if mother_death_year != -1:
        print(mother_shortname + " passed away in " + str(mother_death_year) )

if __name__ == "__main__":

    #starting_id = "@I0007@"
    starting_id = "@I282315998674@"
    #starting_id = "@I282315998663@"
    starting_family = "@F0002@"

    starting_individual = get_individual_from_id(starting_id)

    # descendants = get_descendants(starting_individual)
    # for descendant in descendants:
    #     print(descendant.get_name())

    starting_families = get_family_from_individual(starting_individual)
    descendant_families = get_descendant_families(starting_families[0])

    for family in descendant_families:
        get_family_clips(family)

