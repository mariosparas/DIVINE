#!/usr/bin/env python
# coding: utf-8

# In[51]:


import sys
import re

def main():
    '''args = sys.argv[:]
    if len(args)>1:
        readFromJSON(args[0])
    else:'''
    readFromJSON("neuropublic_farm_calendar_data_2022.json")


# In[52]:


def readFromJSON(file):
    with open(file, 'r') as f:
        contents = f.readlines() 
        observation = "urn:demeter:observation"
        index_pattern = re.compile('.*"(.*)": \{')
        observation_pattern = re.compile('.*"(.*)": \[')
        tag_and_value_pattern = re.compile('.*"(.*)": "(.*)"')
        tag_and_number_pattern = re.compile('.*"(.*)": (\d+)')
        null_pattern = re.compile('.*"(.*)":.*')
        tag_count = 0
        observation_count = 0
        tag_count_list = []
        observation_count_list = []
        index_list = []
        observation_list = []
        values_list = []
        
        # parse file to extract the information to translate 
        for line in contents:
            #print(line)
            index_match = index_pattern.match(line)
            observation_match = observation_pattern.match(line)
            tag_and_value_match = tag_and_value_pattern.match(line)
            tag_and_number_match = tag_and_number_pattern.match(line)
            #print(len(tag_and_value_match.groups()))
            if index_match and index_match.groups():
                index = index_match.groups()[0]
                index_list.append(index)
                #print(index, "index found")
            elif observation_match and observation_match.groups():
                observation_ = observation_match.groups()[0]
                observation_list.append(observation_)
                if (observation_count > 0):
                    observation_count_list.append(observation_count)
                    observation_count = 0
                #print(observation_, "observation found")
            elif tag_and_value_match and tag_and_value_match.groups():
                tag = tag_and_value_match.groups()[0]
                value = tag_and_value_match.groups()[1]
                tag_count += 1
                values_list.append({tag: value})
                #print(tag, '****', value, "tag/value found")
            elif tag_and_number_match and tag_and_number_match.groups():
                tag = tag_and_number_match.groups()[0]
                number = tag_and_number_match.groups()[1]
                tag_count += 1
                values_list.append({tag: number})
                #print(tag, '****', number, "tag/value found")
            elif "null" in line:
                null_match = null_pattern.match(line)
                tag = null_match.groups()[0]
                values_list.append({tag: ""})
                tag_count += 1
            if not tag_and_value_match and not tag_and_number_match and "null" not in line and tag_count > 0:
                tag_count_list.append(tag_count)
                observation_count += tag_count
                tag_count = 0
        observation_count_list.append(observation_count)
        # print AIM-compliant JSON-LD file
        s = '''{
  "@context": [
    "https://w3id.org/demeter/agri-context.jsonld",
	  {    
      "qudt-unit": "http://qudt.org/vocab/unit/"
    }
   ],
   "@graph": [
  	{
      "@id": "urn:demeter:plot:abc",
      "@type": "Plot",
      "hasGeometry": {
        "@id": "urn:demeter:plot:geo:cba",
        "@type": "Polygon",
        "asWKT": "POLYGON (100 0, 101 0, 101 1, 100 1, 100 0)"
      },
      "area": 2012120,
      "description": "Maize plot",
      "category": "arable",
      "crop": {
        "@id": "urn:demeter:crop:xxx",
        "@type": "Crop",
        "cropSpecies": "urn:demeter:croptype:xxx",
        "cropStatus": "seeded",
        "lastPlantedAt": "2016-08-23T10:18:16Z"
      }      
    },
    {
      "@id": "urn:demeter:croptype:xxx",
      "@type": "CropType",
      "name": "Maize"
    },

      ['''
        
        print(s)
        #print(tag_count_list)
        for ind in index_list:
            observation += ('/' + ind)
        for obs, cnt in zip(observation_list,range(len(observation_list))):
            s2 = '''
            {
        "@id": "urn:demeter:observation-2016-'''+str(cnt+1)+''',
          "@type": "Observation",
          "observedProperty": "http://example.com/'''+obs+'''",
          "hasFeatureOfInterest": "urn:demeter:plot:abc",
          "madeBySensor": "sensor/35-207306-844818-0/BMP282",
          "hasResult": ['''
            print(s2)
            obs_cnt = observation_count_list[0]
            #obs_res_list = []
            for i in range(observation_count_list[0]//tag_count_list[0]):
                s3 = "\t\turn:demeter:observation-2016-"+str(cnt+1)+"/result"+str(i+1)+','
                if i+1 == observation_count_list[0]//tag_count_list[0]:
                    print(s3[:-1])
                else:
                    print(s3)
                #obs_res_list.append(s3[:-1])
            s4 = '''\t\t]
            },'''
            print(s4)
            for i in range(observation_count_list[0]//tag_count_list[0]):
                for j in range(tag_count_list[0]):
                    for k in values_list[0].keys():
                        identifier, value = k, values_list[0][k]
                    values_list.pop(0)
                    s5 = '''        {
          "@id": ''' + "urn:demeter:observation-2016-"+str(cnt+1)+"/result"+str(i+1) + ''',
          "@type": "QuantityValue",
          "identifier": "''' + identifier + '''",
          "value": "''' + value + '''",
          "unit": "qudt-unit:xyz"
        },'''
                    print(s5)
                    #obs_res_list.pop(0)
                tag_count_list.pop(0)
            
                
                
            observation_count_list.pop(0)
        s6 = '''\t\t]
    ]
}'''    
        print(s6)


# In[53]:


main()

