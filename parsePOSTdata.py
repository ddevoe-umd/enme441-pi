def getPOSTdata(client_message):
    print(client_message)
    data_dict = {}
    data = str(client_message)   # convert from bytes, same as client_message.decode('utf-8')
    data = data[data.find('\\r\\n\\r\\n')+8 : -1]
    print(data)
    data_pairs = data.split('&')
    print(data_pairs)
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict
