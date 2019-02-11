def spacy_datetime(input_from_spacy)
    """Function that splits the input string into two dates, parses them and calculates their difference in years
       input:string from spacy (string)
       output:years(float)
    """
    from dateutil.parser import *
    from dateutil.tz import *
    from datetime import *
    import re
    input_from_spacy = re.sub("present",str(datetime.today().year),input_from_spacy,flags=re.IGNORECASE)
    input_from_spacy = re.sub("today",str(datetime.today().year),input_from_spacy,flags=re.IGNORECASE)
    dates_in_datetime = []
    #Assume dates are separated by -
    if len(input_from_spacy.split("-"))==2:
        for index,items in enumerate(input_from_spacy.split("-")):
            #Check if there is only Month and not year in the first split
            if((index==0) and (len(re.findall(r'\w+', items))))==1:
                #Year from second date in case first is missing
                try:
                    year = parse(input_from_spacy.split("-")[1], fuzzy=True).year
                    dates_in_datetime.append(parse(str(items)+str(year), fuzzy=True))
                except ValueError:
                    dates_in_datetime.append(datetime.today())
            else:
                try:
                    dates_in_datetime.append(parse(items, fuzzy=True))
                except ValueError:
                    dates_in_datetime.append(datetime.today())
        return(((dates_in_datetime[1]-dates_in_datetime[0]).days)/365)

    #Assume dates are separated by -
    elif len(input_from_spacy.split(" to"))==2:
        for index, items in enumerate(input_from_spacy.split(" to")):
            #Check if there is only Month and not year in the first split
            if((index==0) and (len(re.findall(r'\w+', items))))==1:
                #Year from second date in case first is missing
                try:
                    year = parse(input_from_spacy.split(" to")[1], fuzzy=True).year
                    dates_in_datetime.append(parse(str(items)+str(year), fuzzy=True))
                except ValueError:
                    dates_in_datetime.append(datetime.today())
            else:
                try:
                    dates_in_datetime.append(parse(items, fuzzy=True))
                except ValueError:
                    dates_in_datetime.append(datetime.today())
        return(((dates_in_datetime[1]-dates_in_datetime[0]).days)/365)

    #Return no experience if it does not match to known patterns to avoid raising errors
    else:
        return(0)
