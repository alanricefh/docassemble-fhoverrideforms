from typing import Dict, List, Tuple, Set
from docassemble.base.util import space_to_underscore, value, define, log, validation_error, DAFile, DATemplate, send_email, word
from collections import defaultdict
from datetime import date
from babel.dates import format_date
import unicodedata

CANADA_LIFE_ANNUITY_MAP = {
    0: 0.00,
   25: 6.25,
   50: 12.50,
   55: 13.75,
   60: 15.00,
   65: 16.25,
   70: 17.50,
   75: 18.75,
   80: 20.00,
   85: 21.25,
   90: 22.50,
   95: 23.75,
  100: 25.00,
  105: 26.25,
  110: 27.50,
  115: 28.75,
  120: 30.00,
  125: 31.25,
  130: 32.50,
  135: 33.75,
  140: 35.00,
  150: 37.50,
  155: 38.75,
  160: 40.00,
  165: 41.25,
  170: 42.50,
  175: 43.75,
  180: 45.00,
  190: 47.50,
  195: 48.75,
  200: 50.00,
}

CANADA_LIFE_EQUITY_MAP = {
  70: 0.00,
  71: 2.29,
  72: 3.71,
  73: 4.86,
  74: 6.00,
  75: 7.14,
  76: 9.43,
  77: 10.86,
  78: 12.00,
  79: 13.14,
  80: 14.29,
  81: 16.57,
  82: 18.00,
  83: 19.14,
  84: 20.29,
  85: 21.43,
  86: 23.71,
  87: 25.14,
  88: 26.29,
  89: 27.43,
  90: 28.57,
  91: 30.86,
  92: 32.29,
  93: 33.43,
  94: 34.57,
  95: 35.71,
  96: 38.00,
  97: 39.43,
  98: 40.57,
  99: 41.71,
  100: 42.86,
}
  
EMPIRE_BRANCH_CODE_MAP = {
  "Barrie": "A13346",
  "Burlington": "A32284",
  "Calgary": "A31833",
  "Edmonton": "A31833",
  "Fredericton": "B17727",
  "Halifax-Dartmouth": "A39745",
  "Kingston": "A16441",
  "Kitchener": "A13346",
  "London": "A16087",
  "Moncton": "B17727",
  "Ottawa": "A47737",
  "Saskatoon": "A13951",
  "Sudbury": "A42697",
  "Toronto": "A35326",
  "Vancouver": "A54066",
  "Victoria": "B12121",
  "Winnipeg": "A14237",
  "Richmond": "",
  "Markham": "",
}

EQUITABLE_BRANCH_CODE_MAP = {
  "Barrie": "6G8H1",
  "Burlington": "6G8G1",
  "Calgary": "6G8Z1",
  "Edmonton": "6G8Z1",
  "Fredericton": "6G8Z6",
  "Halifax-Dartmouth": "6G8J1",
  "Kingston": "6G8V1",
  "Kitchener": "6G8A1",
  "London": "6G8I1",
  "Moncton": "6G8Z6",
  "Ottawa": "6G8V1",
  "Saskatoon": "611C9",
  "Sudbury": "6G8K1",
  "Toronto": "6G8B1",
  "Vancouver": "6G8E1",
  "Victoria": "611M1",
  "Winnipeg": "6G8Z1",
  "Richmond": "",
  "Markham": "",
}

SSQ_BRANCH_CODE_MAP = {
  "Barrie": "253606",
  "Burlington": "253600",
  "Calgary": "253373",
  "Edmonton": "253374",
  "Fredericton": "253607",
  "Halifax-Dartmouth": "253607",
  "Kingston": "253602",
  "Kitchener": "253609",
  "London": "253608",
  "Moncton": "253607",
  "Ottawa": "253610",
  "Saskatoon": "253375",
  "Sudbury": "253603",
  "Toronto": "253606",
  "Vancouver": "253700",
  "Victoria": "214000",
  "Winnipeg": "268000",
  "Richmond": "",
  "Markham": "",
}

IA_MONEY_PRODUCTS_RATE_MAP = {
    0: ('00', '00'),
   72: ('00', '01'),
   73: ('00', '02'),
   74: ('00', '04'),
   75: ('00', '05'),
   76: ('00', '06'),
   77: ('00', '08'),
   78: ('00', '09'),
   79: ('00', '11'),
   80: ('00', '12'),
   81: ('01', '13'),
   82: ('03', '15'),
   83: ('04', '16'),
   84: ('05', '18'),
   85: ('06', '19'),
   86: ('08', '20'),
   87: ('09', '22'),
   88: ('10', '23'),
   89: ('11', '25'),
   90: ('13', '26'),
   91: ('14', '27'),
   92: ('15', '29'),
   93: ('16', '30'),
   94: ('18', '32'),
   95: ('19', '33'),
   96: ('20', '34'),
   97: ('21', '36'),
   98: ('23', '37'),
   99: ('24', '39'),
  100: ('25', '40'),
}

MANULIFE_BRANCH_CODE_MAP = {
  "Barrie": "1268",
  "Burlington": "1268",
  "Calgary": "3241",
  "Edmonton": "3241",
  "Fredericton": "3248",
  "Halifax-Dartmouth": "2794",
  "Kingston": "1270",
  "Kitchener": "1268",
  "London": "1269",
  "Moncton": "3248",
  "Ottawa": "1270",
  "Saskatoon": "3241",
  "Sudbury": "1268",
  "Toronto": "1271",
  "Vancouver": "3249",
  "Victoria": "1649",
  "Winnipeg": "3241",
  "Richmond": "",
  "Markham": "",
}

OVERRIDE_CHANGE_TYPE_CARRIER_MAP = {
  'Life_Rounded': [
    'Assumption',
    'BMO',
    'Canada Life',
    'CPP',
    'Foresters',
    'Ivari',
    'RBC',
    'Specialty Life',
    'SSQ',
    'Sun Life',
    'UV',
  ],
  'Life_Any': [
    'Desjardins',
    'Empire',
    'Equitable',
    'IA',
    'La Capitale',
    'Penncorp',
    'Manulife'
  ],
  'Money': [
    "Canada Life",
    "Desjardins",
    "Empire",
    "IA",
    "Manulife",
  ],
}

WS_CARRIER_NAME_MAP = {
    'Assumption Life / Assomption Vie': 'Assumption',
    'BMO Insurance / BMO Assurance': 'BMO',
    'Canada Life / Canada-Vie': 'Canada Life',
    'CPP / PPC': 'CPP',
    'Desjardins Insurance / Desjardins Assurances': 'Desjardins',
    'Empire Life / Empire Vie': 'Empire',
    'Equitable Life / Équitable Vie': 'Equitable',
    'Foresters / Foresters': 'Foresters',
    'Industrial Alliance Insurance/Industrielle Alliance Assurance': 'IA',
    'ivari / ivari': 'Ivari',
    'La Capitale Fin Security(formerly Penncorp) / La Capitale (Penncorp)': 'Penncorp', # Special case
    'La Capitale Insurance / La Capitale Assurance': 'La Capitale',
    'Manulife / Manuvie': 'Manulife',
    'RBC Insurance / RBC Assurances': 'RBC',
    'Specialty Life / Specialite Vie': 'Specialty Life',
    'SSQ Life Insurance / SSQ Assurance Vie': 'SSQ',
    'Sun Life / Sun Life': 'Sun Life',
    'UV Insurance/ UV Assurance': 'UV',
}

# Some carriers ask for codes that appear on WS under a different name
# For example, La Capitale also asks us to provide Penncorp codes if applicable
# (La Capitale acquired Penncorp in 2006).
# The below map ties carrier alises (i.e. Penncorp) to carrier names (i.e. La Capitale)
# which will later be used to generate La Capitale forms when Penncorp codes are selected
CARRIER_ALIAS_MAP = {
  'Penncorp': 'La Capitale'
}

ACTIVE_STATUSES = ('Active', 'Actif')
PENDING_STATUSES = ('Active', 'Pend-Carr', 'Actif', 'En attente - Assureur')

CODE_TYPE_MAP = {
    'Personnel': 'Personal',
    'Corporatif': 'Corporate',
}

DEBUG_EMAIL = True
DEBUG_EMAIL_ADDRESS = 'benjamin.sengupta@financialhorizons.com'

CARRIER_EMAIL_ADDRESS_MAP = {
  'EN': {
    'Assumption':     'contrats@assomption.ca',
    'BMO':            'insurance.agencyservices@bmo.com',
    'Canada Life':    'CanadaLife.Contracts&Licensing@canadalife.com',
    'CPP':            'contracting@cpp.ca',
    'Desjardins':     'compensation@dfs.ca',
    'Empire':         'contracting@empire.ca',
    'Equitable':      'fieldpayroll@equitable.ca',
    'Foresters':      'info@foresters.com',
    'IA':             'iat-compensation@ia.ca',
    'Ivari':          'distributioncompensation@ivari.ca',
    'La Capitale':    'contrat.remuneration@lacapitale.com',
    'Manulife':       'dccpsa2@manulife.ca',
    'RBC':            'inslccs@rbc.com',
    'Specialty Life': 'contracting.compensation@slinsurance.ca',
    'SSQ':            'compensation@ssq.ca',
    'Sun Life':       'REMUN@sunlife.com',
    'UV':             'ind.remuneration@uvassurance.ca',
  },
  'FR': {
    'Assumption':     'contrats@assomption.ca',
    'BMO':            'insurance.agencyservices@bmo.com',
    'Canada Life':    'CanadaLife.Contracts&Licensing@canadalife.com',
    'CPP':            'misesouscontrat@ppcqc.ca',
    'Desjardins':     'compensation@dfs.ca',
    'Empire':         'contracting@empire.ca',
    'Equitable':      'fieldpayroll@equitable.ca',
    'Foresters':      'info@foresters.com',
    'IA':             'iat-compensation@ia.ca',
    'Ivari':          'distributioncompensation@ivari.ca',
    'La Capitale':    'contrat.remuneration@lacapitale.com',
    'Manulife':       'dccpsa2@manulife.ca',
    'RBC':            'inslccs@rbc.com',
    'Specialty Life': 'contracting.compensation@slinsurance.ca',
    'SSQ':            'compensation@ssq.ca',
    'Sun Life':       'REMUN@sunlife.com',
    'UV':             'ind.remuneration@uvassurance.ca',
  },
}

# Returns today's date, i.e. 'August 29, 2022' 
def get_today_date(language: str) -> str:
  return format_date(date.today(), locale=language.lower(), format='long')
# Returns today's month, i.e. 'August'
def get_today_month(language: str) -> str:
  return format_date(date.today(), locale=language.lower(), format='MMMM')
# Returns today's month, i.e. '22'
def get_today_year_suffix(language: str) -> str:
  return format_date(date.today(), locale=language.lower(), format='yy')

# Rounds down a float to the nearest multiple of 5.
# Useful for rounding percentages down to intervals of 5%
def round_to_interval(n: float) -> int:
  return int(n // 5 * 5)

# Returns the CL annuity rate for the given life rate
def canada_life_annuity(life_rate: float) -> int:
  # Ensure life rate is within [0; 200] range before proceeding
  if life_rate < 0 or life_rate > 200:
    raise ValueError("Invalid life rate: expected interval between 0 and 200.")
  # Round life_rate to nearest 5% interval
  rounded_rate = round_to_interval(life_rate)
  # Search through CL Annuity Map for closest Override Rate
  for ovr in sorted(CANADA_LIFE_ANNUITY_MAP.keys(), reverse=True):
    if ovr <= rounded_rate:
      return CANADA_LIFE_ANNUITY_MAP[ovr]

# Returns the CL equity rate for the given money rate
def canada_life_equity(money_rate: float) -> int:
  # Ensure money rate is within [0; 100] range before proceeding
  if money_rate < 0 or money_rate > 100:
    raise ValueError("Invalid money rate: expected interval between 0 and 100.")
  if money_rate < 70:
    return 0.00
  # Round money_rate down to an integer
  rounded_rate = int(money_rate)
  # Return associated CL equity rate
  return CANADA_LIFE_EQUITY_MAP[rounded_rate]

# Returns true if the number is whole
def is_whole(n: float):
    return n % 1 == 0

# Returns the Empire MGA code for the given FH Branch
def empire_mga_code(branch: str):
  return EMPIRE_BRANCH_CODE_MAP[branch]

# Returns the Equitable MGA code for the given FH Branch
def equitable_mga_code(branch: str):
  return EQUITABLE_BRANCH_CODE_MAP[branch]

# Returns the SSQ MGA code for the given FH Branch
def ssq_mga_code(branch: str):
  return SSQ_BRANCH_CODE_MAP[branch]

# Returns the IA money product rates for the given money rate
def ia_money_product_rates(money_rate: float) -> int:
  # Ensure money rate is within [0; 100] range before proceeding
  if money_rate < 0 or money_rate > 100:
    raise ValueError("Invalid money rate: expected interval between 0 and 100.")
  if money_rate < 72:
    return ('00', '00')
  # Round money_rate down to an integer
  rounded_rate = int(money_rate)
  # Return associated IA money product rates
  return IA_MONEY_PRODUCTS_RATE_MAP[rounded_rate]

# Returns the Manulife MGA code for the given FH Branch
def manulife_mga_code(branch: str):
  return MANULIFE_BRANCH_CODE_MAP[branch]

# Converts dictionary of booleans to a list
# ex: { "cat": True, "dog": True, "squirrel": False } becomes ["cat", "dog"]
def dict_of_bools_to_list(d: Dict[str, bool]) -> List[str]:
  return [k for k in d if d[k]]

# Returns the intersection of two lists
# ex: a = [1, 2, 3] b = [2, 3, 4]
#     list_intersection(a, b) # [2, 3]
def list_intersection(a: List[any], b: List[any]) -> List[any]:
  return [e for e in a if e in b]

# Returns carriers that ask for selected override change
# ex: Since La Capitale only asks for life rates, it will not be returned in the list for changes to money only.
def carriers_by_ovr_change_type(ovr_change_type: Dict[str, bool]) -> Set[str]:
  carriers = []
  if ovr_change_type['Life_Any']:
    carriers.extend(OVERRIDE_CHANGE_TYPE_CARRIER_MAP['Life_Any'])
  if ovr_change_type['Life_Rounded']:
    carriers.extend(OVERRIDE_CHANGE_TYPE_CARRIER_MAP['Life_Rounded'])
  if ovr_change_type['Money']:
    carriers.extend(OVERRIDE_CHANGE_TYPE_CARRIER_MAP['Money'])
  # Remove duplicate strings by converting carriers to a set
  unique_carriers = set(carriers)
  return unique_carriers

# Returns an empty string if var is None, otherwise returns var
def suppress_none(var: any) -> any:
  if var is None:
    return ""
  return var

# Removes all French accents from a string. Useful to fix pdf fields with bad UTF-8 support
def strip_accents(s: str):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# Parse WS Carrier Table into a list of codes with elements in the form
# (Carrier, Code, Code_Status)
def parse_ws_carrier_table(input_string: str) -> List[Tuple[str, str, str, str]]:
    lines = input_string.split('\n')
    
    # Skip first row if it's the header row
    first_line = lines[0].strip()
    if first_line.startswith('Carrier Name') or first_line.startswith("Nom de l'assureur"):
        lines = lines[1:]
    
    # Remove empty lines at the end
    while lines != [] and lines[-1].strip() == "":
        lines = lines[:-1]
    
    codes = []
    for row in lines:
        # Split line into parts by tabs
        line_parts = [col.strip() for col in row.strip().split('\t')]
        if len(line_parts) < 6:
          # Invalid table
          raise ValueError('Invalid WS carrier table')
        carrier_name_ws = line_parts[0]
        # Translate to English if code_type is in French
        code_type = CODE_TYPE_MAP.get(line_parts[1], line_parts[1])
        code = line_parts[2]
        status = line_parts[5]
        if carrier_name_ws in WS_CARRIER_NAME_MAP and (status in ACTIVE_STATUSES or status in PENDING_STATUSES):
            carrier_name = WS_CARRIER_NAME_MAP[carrier_name_ws]
            codes.append((carrier_name, code_type, status, code))
    return codes

# Validates WS Carrier Table Input field by passing it to the parsing function
# and seeing if it raises an exception
def validate_ws_carrier_table(input_string: str) -> bool:
  try:
    parse_ws_carrier_table(input_string)
  except ValueError:
    validation_error(word('Invalid WS Carrier table'))
  return True

# Returns variables needed for the multiple choice question of selecting codes from a list
def get_codes_mcq_variable(codes: List[Tuple[str, str, str, str]], ovr_change_type: Dict[str, bool]) -> List[List[any]]:
  # Create labels for all codes
  choice_labels = [f'[{word(status)}] [{word(code_type)}] {word(carrier)} - {code or word("(No Code)")}' for (carrier, code_type, status, code) in codes]
  
  # Returns True for a code when the carrier should be notified of the override change
  def should_code_be_selected(code: Tuple[str, str, str, str]) -> bool:
    carrier_name = code[0]
    status = code[2]
    carrier_code = code[3]
    # Ensures the status is 'Active'
    if status not in ACTIVE_STATUSES:
      return False
    # Ensures carriers should be notified of this change
    if carrier_name not in carriers_by_ovr_change_type(ovr_change_type):
      return False
    # Ensures that a carrier code exists
    if carrier_code == '':
      return False
    # If all the above are true, then select this code
    return True
  
  # Create question variable for docassemble
  codes_mcq = [[i, label, should_code_be_selected(codes[i])] for i, label in enumerate(choice_labels)]
  return codes_mcq

# Parse answer for codes multiple choice question into a tuple of (broker_list, codes)
# where broker_list is a list of broker strings
#   and codes is a dict of shape { Carrier: { Code_Type: Codes } }
def parse_codes_mcq_answer(codes_answer: Dict[str, bool], codes_list: List[Tuple[str, str, str, str]]) -> Dict[str, Dict[str, str]]:
  codes_dict = defaultdict(dict)
  for x in dict_of_bools_to_list(codes_answer):
    carrier_name, code_type, status, code = codes_list[int(x)]
    # Merge 'AGA' codes with 'Corporate' codes
    if code_type == 'AGA':
      code_type = 'Corporate'
    # If multiple 'Personal' or 'Corporate' codes selected, concatenate them into one string
    if code_type in codes_dict[carrier_name]:
      codes_dict[carrier_name][code_type] += ' ' + code
    else:
      codes_dict[carrier_name][code_type] = code
  return codes_dict

# Returns all carriers that handled from this form from codes dictionary
def get_handled_carriers_from_codes(codes_dict: Dict[str, Dict[str, str]]) -> List[str]:
  carriers = codes_dict.keys()
  # Converts all carrier aliases to proper carrier names for get_attachment_list to know which
  # documents to generate
  carriers = [CARRIER_ALIAS_MAP.get(c, c) for c in carriers]
  return carriers

# Returns a list of corresponding docassemble attachments for a given list of carriers and language
def get_attachment_list(carriers: List[str], language: str) -> List[str]:
  # Converts spaces to underscores for all carriers names in the list
  attachments = [space_to_underscore(c) + '_' + language for c in carriers]
  # Fetches attachment variables, for later use with docassemble's attachment list
  attachments = [value(a) for a in attachments]
  return attachments

# Send all emails to carriers, returns a string displaying the status of all emails
def send_carrier_emails(carriers_and_attachments: List[Tuple[str, DAFile]], codes: Dict[str, Dict[str, str]], template: DATemplate, language: str) -> str:
  # List of (carrier, boolean) representing success/failure of sending emails
  email_statuses = []
  for carrier, attachment in carriers_and_attachments:
    carrier_email_name = carrier
    if DEBUG_EMAIL:
      carrier_email_address = DEBUG_EMAIL_ADDRESS
    else:
      carrier_email_address = CARRIER_EMAIL_ADDRESS_MAP[language][carrier]
    # Concatinate all codes
    all_codes = [codes[carrier].get('Personal', ''), codes[carrier].get('Corporate', '')]
    carrier_email_code = ' '.join(all_codes)
    
    # Defines variables so that template can access them
    define('carrier_email_name', carrier_email_name)
    define('carrier_email_code', carrier_email_code)
    
    is_ok = send_email(
      to=carrier_email_address,
      cc=carrier_email_address,
      attachments=[attachment],
      template=template,
    )
    email_statuses.append((carrier, is_ok))
  result = ''
  for carrier, is_ok in email_statuses:
    if is_ok:
      result += f'<span class="email-success">[{word("Sent")}] {word(carrier)} - {carrier_email_address}</span><br>'
    else:
      result += f'<span class="email-failure">[{word("Failure")}] {word(carrier)} - {carrier_email_address} - {word("Failed to send")}</span><br>'
  return result
