#### Function that take Pep Object and transform it to json schema
import json
from datetime import datetime

def serialize(pep):
    data = dict()

    ### person details
    data["person"] = {
        "list_name": pep.list_name,
        "person_type": pep.person_type,
        "sanction_list_type": pep.sanction_list_type,
    }

    ##category
    if (pep.category):
        data["person_category"] = [{"type": None, "category": cat} for cat in pep.category]
    ### image
    if pep.image_url:
        data["image"] = [{"image_url": pep.image_url}]

    ### source name
    if pep.source_name:
        data["source_description"] = [
            {"source_name": source} for source in pep.source_name
        ]

    ### keywords
    if pep.keyword:
        data["keyword"] = [{"name": keyword} for keyword in pep.keyword]

    ### birthplace
    if pep.birth_place:
        data["birth_place"] = [{"place": pep.birth_place, "main_entry": True}]

    ### description
    if pep.description:
        data["description"] = [{"description_value": pep.description}]

    ### country membership
    if pep.country_code:
        data["country_membership_info"] = [
            {"country_code": code, "country_membership": "CITIZEN"}
            for code in pep.country_code
        ]

    ### Birthdate
    if pep.birth_date:
        data["birth_date"] = [
            {
                "birth_date": pep.birth_date.strftime("%Y-%m-%d"),
                "exact_date": True,
                "date_long": None,
                "interval_max_date": None,
                "interval_min_date": None,
                "type": None,
            }
        ]

    ### person info
    data["person_info"] = [
        {
            "action": pep.action,
            "active_status": pep.active_status,
            "deceased": pep.deceased,
            "gender": pep.gender,
            "person_type": pep.person_type,
            "profile_notes": pep.profile_notes,
        }
    ]

    ### sanctions
    data["sanctions"] = []
    for sanction in pep.sanctions:
        data["sanctions"].append(sanction.to_dict())

    ### ID Number
    data["id_number_info"] = []
    for id_number in pep.identities:
        data["id_number_info"].append(id_number.to_dict())

    ### Person roles
    data["person_roles"] = []
    for role in pep.roles:
        data["person_roles"].append(role.to_dict())

    ### names
    data["name"] = []
    for name in pep.names:
        data["name"].append(name.to_dict())

    ### adresses
    data["adress"] = []
    for adress in pep.adresses:
        data["adress"].append(adress.to_dict())
    
    return data

def generate_json_rows(peps):
    l = []
    for pep in peps:
        l.append(serialize(pep))
    filename: str = f"data_{int(datetime.timestamp(datetime.now()))}.json"
    with open(filename, "w") as f:
        json.dump(l, f)
    return filename
