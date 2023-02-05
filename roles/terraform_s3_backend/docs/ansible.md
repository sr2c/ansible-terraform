## Ansible Variables

| Variable                              | Default Value                          | Description                                                           |
|---------------------------------------|----------------------------------------|-----------------------------------------------------------------------|
| `terraform_state_s3_bucket_name`      | randomly generated                     | Name of the S3 bucket to create to hold the Terraform state remotely. |
| `terraform_state_dynamodb_table_name` | `{{ terraform_state_s3_bucket_name }}` | Name of the DynamoDB table to create to facilitate state locking.     |
