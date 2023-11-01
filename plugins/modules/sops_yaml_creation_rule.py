from ansible.module_utils.basic import AnsibleModule
#from ansible.module_utils.common import yaml
#from ansible.plugins.filter.core import to_nice_yaml
import yaml
import traceback
from pathlib import Path

DOCUMENTATION = r"""
---
module: sops_yaml_creation_rule
author: Abel Luck <abel@guardianproject.info>
short_description: Manage a .sops.yaml configuration file
description:
  - Manages a .sops.yaml configuration file by allowing you to add/remove creation-rules.
options:
  state:
    description:
      - Indicate desired state of the creation_rule
    default: present
    choices: ['present', 'absent']
    type: str
  path:
    description:
      - The path to the .sops.yaml file
    type: path
    required: true
  rule_id:
    description:
      - A unique identifier for this creation_rule
    type: str
    required: true
  path_regex:
    description:
      - The pattern to match when creating a  file
    type: str
    required: true
  pgp:
    description:
      - A list of PGP key ids
    type: list
    elements: str
    required: false
  age:
    description:
      - A list of age public keys
    type: list
    elements: str
    required: false
  kms:
    description:
      - A list of KMS options (refer to sops' docs)
    type: list
    elements: dict
    required: false
    suboptions:
      arn:
        required: true
        description: The KMS key ARN
        type: str
      role:
        required: false
        description: An optional role to assume
        type: str
      aws_profile:
        required: false
        description: An optional profile name to use
        type: str
    context:
        required: false
        type: dict
requirements:
  - "python >= 3.8"
"""
EXAMPLES = r"""
- name: add foobar creation rule
  sops_yaml_creation_rule:
    path: ../.sops.yml
    rule_id: foobar
    state: present
    path_regex: projects/foobar/.*\.sops\.yml
    kms:
      - arn: arn:aws:kms:eu-west-1:1234:key/aaaaaaaaa-11111-bbbbb-ccccc-xyzabcdew
        aws_profile: foobar
    pgp:
      - XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""


def create_sops_file(sops_yml_path):
  with open(sops_yml_path, "w") as f:
    f.write("---\ncreation_rules: []")


def read_sops_file(sops_yml_path):
  with open(sops_yml_path, "r") as f:
    yml_doc = yaml.safe_load(f)
    return yml_doc

def main():
    argument_spec = dict(
        path=dict(type="str", required=True),
        rule_id=dict(type="str", required=True),
        path_regex=dict(type="str", required=True),
        state=dict(
            type="str",
            default="present",
            choices=["absent", "present"],
        ),
        kms=dict(
            type="list",
            elements="dict",
            default=[],
            required=False,
            options=dict(
                arn=dict(type="str", required=True),
                aws_profile=dict(type="str", required=False),
                role=dict(type="str", required=False),
                context=dict(type="dict", required=False),
            ),
        ),
        pgp=dict(type="list", elements="str", required=False, default=[]),
        age=dict(type="list", elements="str", required=False, default=[])
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    state = module.params["state"]
    sops_yml_path = module.params["path"]
    rule_id = module.params["rule_id"]
    path_regex = module.params["path_regex"]

    sops_yml_file = Path(sops_yml_path)

    changed = False

    if not sops_yml_file.exists():
      if state == "present":
        try:
            create_sops_file()
            changed = True
        except:
          module.fail_json(
            msg="Failed to create sops configuration file",
            exception=traceback.format_exc()
          )
          return
      else:
        module.exit_json(changed=False, msg="The sops configuration file does not exist. No change necessary.")
        return

    elif sops_yml_file.is_dir():
      module.fail_json(
        msg="The sops configuration file is not a file, it is a directory."
      )
      return

    try:
      yml_doc = read_sops_file(sops_yml_path)
      if yml_doc is None:
        # This happens when the file exists but is empty
        create_sops_file(sops_yml_path)
        yml_doc = read_sops_file(sops_yml_path)
        changed = True
    except:
      module.fail_json(
        msg="Error loading sops configuration file '%s'" % (sops_yml_path),
        exception=traceback.format_exc()
      )
      return

    expected_rule = {"id": rule_id, "path_regex": path_regex}
    key_groups = []
    # only 1 key group supported for now
    key_group = {}
    if module.params["age"]:
      key_group["age"] = sorted(module.params["age"])

    if module.params["pgp"]:
      key_group["pgp"] = sorted(module.params["pgp"])

    if module.params["kms"]:
      key_group["kms"] = sorted(module.params["kms"], key=lambda d: d["arn"])

    key_groups.append(key_group)
    expected_rule["key_groups"] = key_groups


    existing_rules = yml_doc.get("creation_rules", [])
    filtered_rules = [rule for rule in existing_rules if rule.get("id") == rule_id]
    existing_rule = None
    if filtered_rules:
      existing_rule = filtered_rules[0]

    new_rules = existing_rules
    msg = ""
    if state == "absent" and not existing_rule:
      # rule does not exist, nothing to remove
      msg = "Rule does not exist."
    elif state == "absent" and existing_rule:
      # rule needs to be removed
      new_rules = [rule for rule in existing_rules if rule.get("id") != rule_id]
    elif state == "present":
      if existing_rule == expected_rule:
        # rule exists and does not need to be changed
        msg = "Rule %s exists." % (rule_id)
      elif existing_rule:
        # rule exists and needs to be changed
        new_rules = []
        for rule in existing_rules:
          if rule.get("id") == rule_id:
            new_rules.append(expected_rule)
        msg = "Rule updated"
      else:
        # rule does not exist, create it
        existing_rules.append(expected_rule)
        msg = "Rule created"


    if new_rules:
      changed=True
      yml_doc["creation_rules"] = new_rules
      try:
        with open(sops_yml_path, "w") as f:
          yaml.dump(yml_doc, f)
          #f.write(to_nice_yaml(yml_doc))
          changed = True
      except:
        module.fail_json(
          msg="Failed to write sops configuration file",
          exception=traceback.format_exc()
        )
        return

    module.exit_json(changed=changed, msg=msg)





    


if __name__ == "__main__":
    main()
