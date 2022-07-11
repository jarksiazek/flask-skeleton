# cloud-slack-bot

## Run
Launch dockerised server:

```bash
source env.sh && \
docker run -it --rm -p $SERVICE_PORT:$SERVICE_PORT \
-e SERVICE_NAME \
-e SERVICE_PORT \
-e SLACK_TOKEN \
-e SIGNING_SECRET \
-e DB_USER \
-e DB_PASSWD \
-e DB_HOST \
-e DB_DB \
-e DB_PORT \
-e WORKSPACE_NAME \
cloud-slack-bot
```
