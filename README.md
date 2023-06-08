# Backend Engineering Take-Home Challenge

### Instructions
- There are three scripts related to the ETL process: `pre_setting.sh`, `etl_trigger.sh`, and `result_queries.sh`
- In order to build the docker containers, directly run `./pre_setting.sh`. This will build and run the two containers, one for flask and one postgresql
- After both containers are up, directly run `./etl_trigger.sh`. This will `curl` the API and trigger the ETL process
- In the `result_queries.sh`, there are 5 commands that might need manually entered one by one to get the result from the Postgresql database