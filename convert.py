import os
import json
import converter

if __name__==  "__main__":
    ls = []
    ls_json = []
    for r, d, f, in os.walk("/Users/taylor/Desktop/hand-labels/manual_train/"):
        for x in f:
            ls.append(x)

    for val in ls:
        if ".json" in val:
            ls_json.append(val)


    #for val in ls_json:

    f = open("test/000648952_02_l copy.json")
    data = json.load(f)
    
    f.close()

    print(data)

    image_width, image_height = 1024, 768


    output_dir = "test"

    converter.convert_to_yolopose_format(data, image_width, image_height, output_dir)