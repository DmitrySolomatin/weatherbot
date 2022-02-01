TAG ?= latest
REGISTRY_ID ?= 978552764709
REPOSITORY_REGION ?= eu-north-1
APP_NAME ?= weatherbot
ENV_NAME ?= dev
REPO_NAME = $(REGISTRY_ID).dkr.ecr.$(REPOSITORY_REGION).amazonaws.com/${APP_NAME}-${ENV_NAME}

.PHONY: build
build:
	$(MAKE) docker-login
	docker build --build-arg token="5178612806:AAEJekQWaHQ03qegyFKPbgScSHQOq6EGbTE" --build-arg api_key="de1f2fc1fa7776253c482950f5de0956" -t $(REPO_NAME):$(TAG) .
	#docker tag ${APP_NAME}-${ENV_NAME}:$(TAG) $(REGISTRY_ID).dkr.ecr.$(REPOSITORY_REGION).amazonaws.com/${APP_NAME}-${ENV_NAME}:$(TAG)
	docker push $(REGISTRY_ID).dkr.ecr.$(REPOSITORY_REGION).amazonaws.com/${APP_NAME}-${ENV_NAME}:$(TAG)
 
  #docker build -t weatherbot-dev .
  #docker tag weatherbot-dev:latest 978552764709.dkr.ecr.eu-north-1.amazonaws.com/weatherbot-dev:latest
  #docker push 978552764709.dkr.ecr.eu-north-1.amazonaws.com/weatherbot-dev:latest
  
.PHONY: docker-login
docker-login:
	aws ecr get-login-password --region $(REPOSITORY_REGION) | docker login --username AWS --password-stdin $(REGISTRY_ID).dkr.ecr.$(REPOSITORY_REGION).amazonaws.com
