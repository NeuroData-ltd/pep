import jwt
import os
import logging
import json
import csv
from datetime import datetime
import logging

class AbstractHandler(object):
    def __init__(self,next):
        self._next = next
    
    def handle(self,request):
        handled = self.process_request(request)
        if not handled:
            self._next.handle(request)

    def process_request(self,request):
        
        """throws a NotImplementedError"""

        raise NotImplementedError('First implement it !')

class RequestContentHandler(AbstractHandler):
    """
        this class used to verify headers and queries of the request
    """
    def process_request(self,request):
        print("=== processing request content ===")
        if not request.headers.has_key("X-API-Key") :
            raise Exception(400,"X-API-Key header Not found")
        
        necessary_queries = ["firstname", "lastname", "citizenship"]
        for query in necessary_queries:
            if query not in request.args:
                raise Exception(400,f"{query} query should be specified")
            
class AuthenticationHandler(AbstractHandler):
    """
        as the name indicate , this class used to authenticate the client
    """
    def process_request(self,request):
        try :
            print("=== processing authentication and rate limiting ===")
            jwt_decoded = jwt.decode(request.headers['X-API-Key'].encode('utf-8').strip(),os.getenv('JWT_SECRET_KEY'),["HS256"])
            result = self.__check_limit(user_email=jwt_decoded['user_email'],api_ref=jwt_decoded['api_ref'])
            if result is not False:
                raise Exception(403,"Api usage exceeded rate limit")
        except jwt.exceptions.PyJWTError:
            raise Exception(400,"API-Key Failed")
        return True
            
    def __check_limit(self,user_email: str, api_ref: str):
        inputs = (user_email, api_ref)
        result = None
        update_statement = "UPDATE `tokens` SET usage_rate = usage_rate + 1 WHERE user_email=%s AND api_ref=%s"
        query = "SELECT usage_rate FROM tokens WHERE user_email = %s AND api_ref = %s"
        try :
            with self._db_connection.cursor() as cursor:
                cursor.execute(update_statement,inputs)
                cursor.execute(query,inputs)
                data = cursor.fetchone()['usage_rate']
                if (data > int(os.getenv("RATE_LIMIT"))):
                    result = True
                else:
                    result = False
                self._db_connection.commit()
                return result
        except Exception as e:
            logging.error(e)
    
    def set_db_connection(self,connection):
        self._db_connection = connection

def sanitize_data(data: dict) -> dict:

    ### birthdate control
    if data["birthdate"]:   
        data["birthdate"] = data["birthdate"].strptime(format="%d/%m/%Y")

    data.pop('photo_link')

    ### deserialize non - string fields 
    for key,val in data.items():
        if key in ['sanctions_details','spouses','children','citizenships','positions', 'addresses', 'occupations','other_informations', 'other_names' ,'links']:
            try:
                data[key] = [item['value'] for item in json.loads(val)] 
            except json.JSONDecodeError as e:
                data[key] = []
    return data

AMI_INSURANCE_HEADERS_PEP =  [
        "ID",
        "FIRST_NAME",
        "SECOND_NAME",
        "THIRD_NAME",
        "WHOLE_NAME",
        "ORIGINAL_SCRIPT_FIRST_NAME",
        "ORIGINAL_SCRIPT_LAST_NAME",
        "ORIGINAL_SCRIPT_WHOLE_NAME",
        "MAIDEN_NAME",
        "LAST_MODIFIED_ON",
        "LISTED_ON",
        "COMMENTS", 
        "NATIONALITY",
        "ALIAS_NAME",
        "DATE_OF_BIRTH",
        "TYPE_OF_DOCUMENT",
        "DOC_NO",
        "ENTITY_TYPE",
        "ADDRESS",
        "LIST_ID",
        "VERSIONNUM",
        "BLACKLISTED",
        "IS_PEP",
        "CUSTOM_MSG" 
]

CITIZENSHIPS = {
'AW':'ARUBA',
'AF':'AFGHANE',
'AO':'ANGOLAISE',
'AI':'ANGUILLA',
'AX':'ÅLAND ISLANDS',
'AL':'ALBANAISE',
'AD':'ANDORRANE',
'AE':'ÉMIRATIE',
'AR':'ARGENTINE',
'AM':'ARMÉNIENNE',
'AS':'AMERICAN SAMOA',
'AQ':'ANTARCTICA',
'TF':'FRENCH SOUTHERN TERRITORIES',
'AG':'ANTIGUAISE',
'AU':'AUSTRALIENNE',
'AT':'AUTRICHIENNE',
'AZ':'AZÉRIE',
'BI':'BURUNDAISE',
'BE':'BELGE',
'BJ':'BÉNINOISE',
'BQ':'BONAIRE SINT EUSTATIUS AND SABA',
'BF':'BURKINABÈ',
'BD':'BANGLADAISE',
'BG':'BULGARE',
'BH':'BAHREÏNIENNE',
'BS':'BAHAMIENNE',
'BA':'BOSNIENNE',
'BL':'SAINT BARTHÉLEMY',
'BY':'BIÉLORUSSE',
'BZ':'BÉLIZIENNE',
'BM':'BERMUDA',
'BO':'BOLIVIENNE',
'BR':'BRÉSILIENNE',
'BB':'BARBADIENNE',
'BN':'BRUNÉIENNE',
'BT':'BHOUTANAISE',
'BV':'BOUVET ISLAND',
'BW':'BOTSWANAISE',
'CF':'CENTRAL AFRICAN REPUBLIC',
'CA':'CANADIENNE',
'CC':'COCOS (KEELING) ISLANDS',
'CH':'SUISSE',
'CL':'CHILIENNE',
'CN':'CHINOISE',
'CI':'IVOIRIENNE',
'CM':'CAMEROUNAISE',
'CD':'CONGOLAISE',
'CG':'CONGOLAISE',
'CK':'COOK ISLANDS',
'CO':'COLOMBIENNE',
'KM':'COMORIENNE',
'CV':'CAP-VERDIENNE',
'CR':'COSTARICAINE',
'CU':'CUBAINE',
'CW':'CURAÇAO',
'CX':'CHRISTMAS ISLAND',
'KY':'CAYMAN ISLANDS',
'CY':'CHYPRIOTE',
'CZ':'TCHÈQUE',
'DE':'ALLEMANDE',
'DJ':'DJIBOUTIENNE',
'DM':'DOMINICAINE',
'DK':'DANOISE',
'DO':'DOMINICAN REPUBLIC',
'DZ':'ALGÉRIENNE',
'EC':'ÉQUATORIENNE',
'EG':'ÉGYPTIENNE',
'ER':'ÉRYTHRÉENNE',
'EH':'WESTERN SAHARA',
'ES':'ESPAGNOLE',
'EE':'ESTONIENNE',
'ET':'ÉTHIOPIENNE',
'FI':'FINLANDAISE',
'FJ':'FIDJIENNE',
'FK':'FALKLAND ISLANDS (MALVINAS)',
'FR':'FRANÇAISE',
'FO':'FAROE ISLANDS',
'FM':'MICRONÉSIENNE',
'GA':'GABONAISE',
'GB':'BRITANNIQUE',
'GE':'GÉORGIENNE',
'GG':'GUERNSEY',
'GH':'GHANÉENNE',
'GI':'GIBRALTAR',
'GN':'GUINÉENNE',
'GP':'GUADELOUPE',
'GM':'GAMBIENNE',
'GW':'BISSAU-GUINÉENNE',
'GQ':'ÉQUATO-GUINÉENNE',
'GR':'GRECQUE',
'GD':'GRENADIENNE',
'GL':'GREENLAND',
'GT':'GUATÉMALTÈQUE',
'GF':'FRENCH GUIANA',
'GU':'GUAM',
'GY':'GUYANAISE',
'HK':'HONG KONG',
'HM':'HEARD ISLAND AND MCDONALD ISLANDS',
'HN':'HONDURIENNE',
'HR':'CROATE',
'HT':'HAÏTIENNE',
'HU':'HONGROISE',
'ID':'INDONÉSIENNE',
'IM':'ISLE OF MAN',
'IN':'INDIENNE',
'IO':'BRITISH INDIAN OCEAN TERRITORY',
'IE':'IRLANDAISE',
'IR':'IRANIENNE',
'IQ':'IRAKIENNE',
'IS':'ISLANDAISE',
'IL':'ISRAÉLIENNE',
'IT':'ITALIENNE',
'JM':'JAMAÏCAINE',
'JE':'JERSEY',
'JO':'JORDANIENNE',
'JP':'JAPONAISE',
'KZ':'KAZAKHE',
'KE':'KÉNYANE',
'KG':'KIRGHIZE',
'KH':'CAMBODGIENNE',
'KI':'KIRIBATIENNE',
'KN':'SAINT-KITTSIENNE',
'KR':'SUD-CORÉENNE',
'KW':'KOWEÏTIENNE',
'LA':'LAOTIENNE',
'LB':'LIBANAISE',
'LR':'LIBÉRIENNE',
'LY':'LIBYENNE',
'LC':'SAINT-LUCIENNE',
'LI':'LIECHTENSTEINOISE',
'LK':'SRI LANKAISE',
'LS':'LESOTHANE',
'LT':'LITUANIENNE',
'LU':'LUXEMBOURGEOISE',
'LV':'LETTONE',
'MO':'MACAO',
'MF':'SAINT MARTIN (FRENCH PART)',
'MA':'MAROCAINE',
'MC':'MONÉGASQUE',
'MD':'MOLDAVE',
'MG':'MALGACHE',
'MV':'MALDIVIENNE',
'MX':'MEXICAINE',
'MH':'MARSHALLAISE',
'MK':'MACÉDONIENNE',
'ML':'MALIENNE',
'MT':'MALTAISE',
'MM':'BIRMANE',
'ME':'MONTÉNÉGRINE',
'MN':'MONGOLE',
'MP':'NORTHERN MARIANA ISLANDS',
'MZ':'MOZAMBICAINE',
'MR':'MAURITANIENNE',
'MS':'MONTSERRAT',
'MQ':'MARTINIQUE',
'MU':'MAURICIENNE',
'MW':'MALAWIENNE',
'MY':'MALAISIENNE',
'YT':'MAYOTTE',
'NA':'NAMIBIENNE',
'NC':'NEW CALEDONIA',
'NE':'NIGÉRIENNE',
'NF':'NORFOLK ISLAND',
'NG':'NIGÉRIANE',
'NI':'NICAÉENNE',
'NU':'NIOUÉENNE',
'NL':'NÉERLANDAISE',
'NO':'NORVÉGIENNE',
'NP':'NÉPALAISE',
'NR':'NAURUANE',
'NZ':'NÉO-ZÉLANDAISE',
'OM':'OMANAISE',
'PK':'PAKISTANAISE',
'PA':'PANAMÉENNE',
'PN':'PITCAIRN',
'PE':'PÉRUVIENNE',
'PH':'PHILIPPINNE',
'PW':'PALAOSIENNE',
'PG':'GUINÉE (PG) - PAPOUASIENNE',
'PL':'POLONAISE',
'PR':'PUERTO RICO',
'KP':'NORD-CORÉENNE',
'PT':'PORTUGAISE',
'PY':'PARAGUAYENNE',
'PS':'PALESTINIENNE',
'PF':'FRENCH POLYNESIA',
'QA':'QATARIENNE',
'RE':'RÉUNION',
'RO':'ROUMAINE',
'RU':'RUSSE',
'RW':'RWANDAISE',
'SA':'SAOUDIENNE',
'SD':'SOUDANAISE',
'SN':'SÉNÉGALAISE',
'SG':'SINGAPOURIENNE',
'GS':'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS',
'SH':'SAINT HELENA ASCENSION AND TRISTAN DA CUNHA',
'SJ':'SVALBARD AND JAN MAYEN',
'SB':'SALOMONIENNE',
'SL':'SIERRA-LÉONAISE',
'SV':'SALVADORIENNE',
'SM':'SAINT-MARINAISE',
'SO':'SOMALIENNE',
'PM':'SAINT PIERRE AND MIQUELON',
'RS':'SERBE',
'SS':'SUD-SOUDANAISE',
'ST':'SANTOMÉENNE',
'SR':'SURINAMAISE',
'SK':'SLOVAQUE',
'SI':'SLOVÈNE',
'SE':'SUÉDOISE',
'SZ':'ESWATINI',
'SX':'SINT MAARTEN (DUTCH PART)',
'SC':'SEYCHELLOISE',
'SU':'',
'SY':'SYRIENNE',
'TC':'TURKS AND CAICOS ISLANDS',
'TD':'TCHADIENNE',
'TG':'TOGOLAISE',
'TH':'THAÏLANDAISE',
'TJ':'TADJIKE',
'TK':'TOKELAU',
'TM':'TURKMÈNE',
'TL':'TIMORAISE',
'TO':'TONGIENNE',
'TT':'TRINIDADIENNE',
'TN':'TUNISIENNE',
'TR':'TURQUE',
'TV':'TUVALUANE',
'TW':'TAIWAN PROVINCE OF CHINA',
'TZ':'TANZANIENNE',
'UG':'OUGANDAISE',
'UA':'UKRAINIENNE',
'UM':'UNITED STATES MINOR OUTLYING ISLANDS',
'UY':'URUGUAYENNE',
'US':'AMÉRICAINE',
'UZ':'OUZBÈKE',
'VA':'VATICANAISE',
'VC':'GRENADINES (VC) - SAINT-VINCENTAISE',
'VE':'VÉNÉZUÉLIENNE',
'VG':'VIRGIN ISLANDS BRITISH',
'VI':'VIRGIN ISLANDS U.S.',
'VN':'VIETNAMIENNE',
'VU':'VANUATUANE',
'WF':'WALLIS AND FUTUNA',
'WS':'SAMOANE',
'YE':'YÉMÉNITE',
'ZA':'SUD-AFRICAINE',
'ZM':'ZAMBIENNE',
'ZW':'ZIMBABWÉENNE',
'EU':'EUROPE',
'UK':'UNITED KINGDOM',
}

def adapter(row: dict) -> dict:
    ID = row['id']
    FIRSTNAME = row['firstname']
    LASTNAME = row['lastname']
    THIRDNAME = row['thirdname']
    WHOLENAME = row['fullname']
    BIRTHDATE = row['birthdate']
    ENTITY_TYPE = row['entity_type']    
    BLACKLISTED = "FALSE"
    IS_PEP = "FALSE"
    CUSTOM_MSG = ""

    CITIZENSHIP = CITIZENSHIPS[row['citizenships'][0]] if len(row['citizenships'][0]) > 0 else ''
    ADDRESS = ADDRESS = "/".join(row['addresses']) if row['addresses'] else ""
    TYPE_OF_DOCUMENT = "CIN" if (row['entity_type'].upper() == "PERSON") else "MF"

    if row['source_type'] == "SANCTION":
        BLACKLISTED = "TRUE"
        CUSTOM_MSG = "SANCTION" 

    if row['source_type'] == "PEP":
        IS_PEP = "TRUE"
        CUSTOM_MSG = "PEP"

    ### entity type 
    if (row['entity_type'].upper() == "ENTITY"):
        FIRSTNAME = ""
        LASTNAME = ""

    if (row['entity_type'].upper() == "PERSON"):
        WHOLENAME = ""

    cleaned_row = {
        "ID" : ID,
        "FIRST_NAME" : FIRSTNAME,
        "SECOND_NAME" : LASTNAME,
        "THIRD_NAME" : THIRDNAME,
        "WHOLE_NAME" : WHOLENAME,
        "ORIGINAL_SCRIPT_FIRST_NAME" : "",
        "ORIGINAL_SCRIPT_LAST_NAME" : "",
        "ORIGINAL_SCRIPT_WHOLE_NAME" : "",
        "MAIDEN_NAME" :"",
        "LAST_MODIFIED_ON" : "",
        "LISTED_ON" : "",
        "COMMENTS" : "Fraud on list intern", 
        "NATIONALITY" : CITIZENSHIP,
        "ALIAS_NAME" : "" ,
        "DATE_OF_BIRTH" : BIRTHDATE,
        "TYPE_OF_DOCUMENT" : TYPE_OF_DOCUMENT,
        "DOC_NO" : "",
        "ENTITY_TYPE" : ENTITY_TYPE,
        "ADDRESS" : ADDRESS,
        "LIST_ID" : 'LISTE INTERNE',
        "VERSIONNUM" : "",
        "BLACKLISTED" : BLACKLISTED,
        "IS_PEP" : IS_PEP,
        "CUSTOM_MSG" : CUSTOM_MSG 
    }
    return cleaned_row

def generate_csv_db(records: list[dict]) -> str:
    date = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    data = list(map(adapter,records))
    filepath = os.path.join("csv",f"pep_list_{date}.csv")
    header = "ID;FIRST_NAME;SECOND_NAME;THIRD_NAME;WHOLE_NAME;ORIGINAL_SCRIPT_FIRST_NAME;ORIGINAL_SCRIPT_LAST_NAME;ORIGINAL_SCRIPT_WHOLE_NAME;MAIDEN_NAME;LAST_MODIFIED_ON;LISTED_ON;COMMENTS;NATIONALITY;ALIAS_NAME;DATE_OF_BIRTH;TYPE_OF_DOCUMENT;DOC_NO;ENTITY_TYPE;ADDRESS;LIST_ID;VERSIONNUM;BLACKLISTED;IS_PEP;CUSTOM_MSG\n"
    with open(filepath,"w") as file:
        file.write(header)
        output = csv.DictWriter(file,fieldnames=AMI_INSURANCE_HEADERS_PEP,delimiter=";",doublequote=True)
        output.writerows(data)
    return filepath
