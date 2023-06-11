'''

 Supported : both Python 3 and 2
 lib used : optparse, sys, json, yaml

 run command:
 main.py --add --name Harvey_spectre --address Flat302,NY --phonenumber 88451226465 --sex Male --dataformat json

 list of args to add data:
 --add
     --name
     --address
     --phonenumber
     --sex

 list of query args:
 --query
    --name or --sex or both at a time
    --phonenumber
    --address

list of specific querylist data args:
--querylist
    --listallqueryformats
    --listallnames
    --listallphonenumber


Parser: args = parse_args_optparse()
Execute main function: run_program()

To know more and about extending the queries, format,
please refer to Readme.pdf file.
'''


from optparse import OptionParser
import os, sys, json
import yaml

# declare all the formats
# more data formats can be added here
all_data_store_formats = ["name", "address", "phonenumber", "sex"]
all_addon_query_formats = ["listallqueryformats", "listallnames", "listallphonenumber"]


# if linux, change "\\" to "/"
json_file = "database\\people_data.json"
yaml_file = "database\\people_data.yaml"


if not os.path.exists(json_file) and not os.path.exists(yaml_file):
    message = "File missing: " + json_file + " and " + yaml_file
    print ("Fix the file path")
    raise Exception(message)


def parse_args_optparse():
    '''
    All arguments
    Add more parsing args/options here for queries
    :return: dict:: {'adduser': True, 'name': 'Harvey_spectre', 'address': 'Flat302,NY', 'phonenumber': '884512264'}
    '''
    parser = OptionParser()
    parser.add_option('--add', dest='adduser', action="store_true")
    parser.add_option('--query', dest='querydata', action="store_true")
    parser.add_option('--querylist', dest='querydatalist', action="store_true")
    parser.add_option('--dataformat', dest='data_format', type=str)

    # take declared list of formats for parsing
    # eg: "--" + "name" = "--name"
    for each_format in all_data_store_formats:
        __arg = "--" + each_format
        parser.add_option(__arg, dest=each_format, type=str)

    # take declared list of addon query formats for parsing
    # eg: "--" + "listallqueryformats" = "--listallqueryformats"
    for each_format in all_addon_query_formats:
        __arg = "--" + each_format
        parser.add_option(__arg, dest=each_format, action="store_true")

    options, args = parser.parse_args()
    return options


class Person:
    '''
    Person stores all details.
    It creates a dict of all details and returns.
    '''
    def __init__(self, name):
        self.name = name

    def details(self, **kwargs):
        '''
        parse person details from user inputs
        and export to dict.
        :return: dict :: {'Name': 'Shankar', 'Address': 'Flat302,maithri', 'Phone number': 884512264}
        '''
        dict_data = {}
        dict_data["name"] = self.name
        print ("name: ", self.name)

        for key, value in kwargs.items():
            if value is None:
                value = "No Data"
            print (key, ": ", value )
            dict_data[key] = value
        return dict_data

class PersonAssistant:
    '''
    The Assistant has 3 atributes.
    It reads the person's database file.
    Save data to database.
    Also returns all persons names found in database.
    '''
    
    def __init__(self, file_path, data_format):
        self.file_path = file_path
        self.data_format = data_format
        
    def read_file(self):
        '''
        read json or yaml file.
        :param file_format: str:: "json" or "yaml"
        :param fire_to_read: str: "/database/people_data.json"
        :return: dict: {'Name': 'Shankar', 'Address': 'Flat302,maithri'}
        '''
        if self.data_format == "json":
            with open(self.file_path, "r") as file:
                try:
                    dict_data = json.load(file)
                except:
                    dict_data = {}
        else:
            with open(self.file_path, "r") as file:
                dict_data = yaml.safe_load(file)
        return dict_data

    def save_data(self, person_details):
        '''
        read the existing database json/yaml file.
        take new person details and append.
        save the file.
        :param data_format: string :: "yaml" or "json"
        :param file_path: string :: "/jobs/file.json"
        :param person_details: dict: person details from database
        :return: str:: "file.json"
        '''
        print("")
        print("Saving user details in database..")

        if self.data_format == "json":
            data = self.read_file()
            data[person_details["name"]] = person_details
            with open(self.file_path, "w") as file:
                 json.dump(data, file, indent=3)
        else:
            # if format : yaml
            # read existing yaml file and write new data
            data = self.read_file()
            if data is None:
                data = {}
            with open(self.file_path, 'w') as file:
                data[person_details["name"]] = person_details
                yaml.dump(data, file)

        print("")
        print("File format : ", self.data_format)

        print ("File has been saved: ", self.file_path)
        return self.file_path
        
    def list_persons(self, value):
        '''
        search for the value in the dict.
        if found, return parent key.
        :param dict_obj: dict :: {'Shankar': {'name': 'Shankar', 'address': 'spain,EU', 'phonenumber': '88451226402', 'Sex': 'Male'}}
        :param value: string:: "Male"
        :return: list: dict keys ['Shankar', 'Harvey_spectre']
        '''
        print("")
        print("Searching filters in database...")
        person_details = self.read_file()
        all_keys = []

        for key, val in person_details.items():
            if value in key:
                all_keys.append(key)
            iner_values = val.items()
            for inkey, inval in iner_values:
                if value in inval and key not in all_keys: all_keys.append(key)
                if value in inkey and key not in all_keys: all_keys.append(key)

        print ("Found persons.. ")
        return all_keys


class UserListQueries(PersonAssistant):
    '''
    queries list listallqueryformats, listallnames, listallphonenumber
    :return: list: list of data
    '''
    print("Querying data list...")
    print("")

    def listallqueryformats(self):
        print("Available supported query formats:")
        for each_format in all_addon_query_formats:
            print("--" + each_format)
        return all_addon_query_formats

    def listallnames(self):
        list_names = []
        dict_data = self.read_file()
        if dict_data:
            print("All Person names: ")
            for each_key in dict_data.keys():
                list_names.append(each_key)
                print(each_key)
            return list_names
        else:
            print("No data found")
            return None

    def listallphonenumber(self):
        dict_data = self.read_file()
        if dict_data:
            print("All Person Phone Numbers: ")
            for each_key in dict_data.keys():
                print (each_key, ":" , str(dict_data[each_key]["phonenumber"]))
            return dict_data
        else:
            print("No data found")
            return None

    # more queries like listallage, listalllanguage can be added
    # any format can be search in dict_data

def query_person_data():
    '''
    collects/Parse data from user inputs name, address, phone number
    and use those formats to look in to .json/yaml file.
    find the value and its parent key.
    :return: dict: {'Sapna_dalvi': {'Sex': 'No Data', 'phonenumber': '451226402', 'name': 'Sapna_dalvi', 'address': 'Goa,India'}}
    '''
    # active_filters are the input values we got from command line
    # eg: active_filters = ["Harvey_specter", "Female", "Spain" ]
    # persons_list = ['Shankar', 'Harvey_spectre']
    print("Querying data...")
    print("")

    # add more format filters as per requirement
    all_query_format_filters = [args.name, args.address, args.phonenumber, args.sex]
    active_filters = []
    persons_list = []

    # get data from PersonDataExchange
    if args.data_format == "json":
        file_path = json_file
    else:
        file_path = yaml_file
    
    person_assist = PersonAssistant(file_path=file_path, data_format=args.data_format)
    dict_data = person_assist.read_file()
    
    # query name, address, phonenumbers etc.
    for each_filter in all_query_format_filters:
        if each_filter: active_filters.append(each_filter)

    for each_filter in active_filters:
        persons_list = person_assist.list_persons(value=each_filter)

    if persons_list and dict_data:
        for each_person in persons_list:
            print("")
            print(each_person)
            for key, val in dict_data[each_person].items():
                print(key, ":", val)

    return dict_data


def run_program():
    '''
    main function to run the program
    :return: dict: data
    '''
    if args.data_format == "json":
        file_path = json_file
    else:
        file_path = yaml_file

    # record data in database
    if args.adduser and args.data_format:
        print("Collecting user inputs ...")
        print("")

        person = Person(name=args.name)
        user_input = person.details(address=args.address,
                                      phonenumber=args.phonenumber,
                                      Sex=args.sex)

        # get data from personAssistant
        # save person data in database
        person_assist = PersonAssistant(file_path=file_path, data_format=args.data_format)
        sdata = person_assist.save_data(person_details=user_input)
        return sdata

    # query list of data from database
    # these are specific args.
    elif args.querydatalist and args.data_format:
        addon_queries = UserListQueries(file_path, args.data_format)

        if args.listallqueryformats:
            addon_queries.listallqueryformats()

        if args.listallnames:
            addon_queries.listallnames()

        if args.listallphonenumber:
            addon_queries.listallphonenumber()

        # more queries like listallage, listalllanguage can be added
        # any format can be search in dict_data

    # query Person data ; Name or Age of a person
    # query filtered data; All 32 aged person, All "india" address Person.
    elif args.querydata and args.data_format:
        return query_person_data()
    else:
        raise Exception("Task Categorised argument missing: use '--add' or '--query' ")




if __name__ == "__main__":
    args = parse_args_optparse()
    run_program()
    sys.exit()





