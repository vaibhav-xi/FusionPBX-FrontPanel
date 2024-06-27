def DestinationPostData(key, value, des_data):
    
    php_array = {
        'destination_description': des_data["destination_description"],
        'destination_type': 'inbound',
        'destination_prefix': '49',
        'destination_number': des_data["destination_number"],
        'destination_caller_id_name': '',
        'destination_caller_id_number': '',
        'destination_context': 'public',
        'destination_conditions': [
            {
                'condition_field': '',
                'condition_expression': ''
            }
        ],
        'destination_actions[0]': [
            des_data["destination_action"],
        ],
        'user_uuid': '',
        'group_uuid': '',
        'destination_cid_name_prefix': '',
        'destination_record': '',
        'destination_hold_music': '',
        'destination_distinctive_ring': '',
        'destination_accountcode': '',
        'destination_type_voice': '1',
        'destination_type_text': '1',
        'domain_uuid': des_data["domain_uuid"],
        'destination_order': '100',
        'destination_enabled': 'true',
        key: value
    }
    
    return php_array