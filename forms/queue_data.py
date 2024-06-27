import uuid

def generate_call_center_tiers(num_tiers):
    call_center_tiers = []
    for _ in range(num_tiers):
        tier_uuid = str(uuid.uuid4())
        tier = {
            "call_center_tier_uuid": tier_uuid,
            "call_center_agent_uuid": "",
            "tier_level": 0,
            "tier_position": 0
        }
        call_center_tiers.append(tier)
    return call_center_tiers

def CallCenterData(key, value, queue_data):
    call_center_tiers = generate_call_center_tiers(5)

    php_array = {
        "queue_name": queue_data["queue_name"],
        "queue_extension": queue_data["queue_extension"],
        "queue_greeting": "",
        "queue_strategy": "ring-all",
        "call_center_tiers": call_center_tiers,
        "queue_moh_sound": queue_data["queue_moh_sound"],
        "queue_record_template": "",
        "queue_time_base_score": "system",
        "queue_time_base_score_sec": "",
        "queue_max_wait_time": 900000,
        "queue_max_wait_time_with_no_agent": 900000,
        "queue_max_wait_time_with_no_agent_time_reached": 900000,
        "queue_timeout_action": "hangup:",
        "queue_tier_rules_apply": False,
        "queue_tier_rule_wait_second": 30,
        "queue_tier_rule_wait_multiply_level": True,
        "queue_tier_rule_no_agent_no_wait": True,
        "queue_discard_abandoned_after": 900,
        "queue_abandoned_resume_allowed": False,
        "queue_cid_prefix": queue_data["queue_cid_prefix"],
        "queue_announce_sound": "",
        "queue_announce_frequency": "",
        "queue_cc_exit_keys": "",
        'queue_context':"138.201.188.127",
        "queue_description": queue_data["queue_description"],
        key: value
    }
    
    return php_array
