<!-- markdownlint-disable -->
## Role Variables

| Variable     | Default Value  | Description  |
| ------------ | -------------- | ------------ |
| terraform_module_backend_config | `{"local" : {}}` | The backend configuration to use. |
| terraform_module_inputs | `{}` | The inputs to pass to the Terraform module. |
| terraform_module_outputs_var | `"terraform_module_outputs"` | The name of a host variable to store the outputs of the Terraform module. |
| terraform_module_source | **REQUIRED** | The source of the Terraform module to use (either a Terraform registry path, or a relative filesystem path). |
| terraform_module_version | ~ | The version of the Terraform module to use when using a module from the Terraform registry. |
| terraform_module_workdir | ~ | The location where the Terraform files will be templated. By default a temporary directory is created. The location should be an empty directory that already exists. |
| terraform_module_workdir_clean_enabled | `true` | Whether to clean the Terraform module work directory after execution. |
<!-- markdownlint-enable -->
