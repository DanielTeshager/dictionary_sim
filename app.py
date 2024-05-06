from flask import Flask, render_template, request, jsonify
import random
import string
from dictionary import Dictionary

app = Flask(__name__)
my_dict = Dictionary()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/simulate', methods=['POST'])
def simulate():
    dict_string = request.form['dict_string']
    my_dict.dict_string = dict_string
    my_dict.reset()
    my_dict.split_string()

    response = {
        'hashing': [],
        'modulo': [],
        'dkIndices': [],
        'dkEntries': [],
        'memoryReferences': []
    }

    for key in my_dict.keys:
        if key is not None:
            hash_value = hash(key)
            response['hashing'].append({'key': key, 'hash': hash_value})
            slot = my_dict.find_slot(key)
            print(slot)
            dk_size = Dictionary.DK_INDICES
            quadratic_probing = "(bucket_idx + i^2) % dk_indices_size"
            response['modulo'].append(
                {'hash': hash_value, 'slot': slot, 'quadraticProbing': quadratic_probing, 'dk_size': dk_size})
            response['dkIndices'].append({'hash': hash_value, 'slot': slot})
            response['dkEntries'].append({
                'hashVal': hash_value,
                'keyRef': f"0x{id(key):x}",
                'valRef': f"0x{id(my_dict.get_value(key)):x}",
                "slot": slot
            })
            response['memoryReferences'].append({
                'address': f"0x{id(key):x}",
                'value': key
            })
            response['memoryReferences'].append({
                'address': f"0x{id(my_dict.get_value(key)):x}",
                'value': my_dict.get_value(key)
            })

    return jsonify(response)


@app.route('/lookup', methods=['POST'])
def lookup_value():
    key = request.form['dict_string']
    size = len([x for x in my_dict.keys if x is not None])
    if size > 0:
        # find slot
        try:
            slot = my_dict.keys.index(key)
        except ValueError:
            return jsonify({"error": True, "message": "The key is not in the dictionary"})
        print(slot, key)
        hash_val = hash(key)
        valRef = f"0x{id(my_dict.get_value(key)):x}"
        return jsonify({"error": False, "hasValue": True, "slot": slot, "hash_val": hash_val, "valRef": valRef})
    else:
        return jsonify({"error": True, "message": "There's no dictionary"})


@app.route('/delete', methods=['POST'])
def delete_key_val():
    key = request.form['dict_string']
    size = len([x for x in my_dict.keys if x is not None])
    if size > 0:
        # find slot
        try:
            slot = my_dict.keys.index(key)
        except ValueError:
            return jsonify({"error": True, "message": "The key is not in the dictionary"})
        print(slot, key)
        hash_val = hash(key)
        valRef = f"0x{id(my_dict.get_value(key)):x}"
        isDeleted = my_dict.delete_value(key)
        return jsonify({"error": False, "hasValue": True, "slot": slot, "hash_val": hash_val, "valRef": valRef, "deleted": isDeleted})
    else:
        return jsonify({"error": True, "message": "There's no dictionary"})


if __name__ == '__main__':
    app.run(debug=True)
