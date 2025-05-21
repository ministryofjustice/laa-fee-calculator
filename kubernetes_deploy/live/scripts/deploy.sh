#!/bin/sh
function _deploy() {
  usage="deploy -- deploy image from current commit to an environment
  Usage: kubernetes_deploy/live/scripts/deploy.sh environment [image-tag]
  Where:
    environment [dev|staging|production]
    [image_tag] any valid ECR image tag for app
  Example:
    # deploy image for current commit to staging
    deploy.sh staging

    # deploy latest image of main to staging
    deploy.sh staging latest

    # deploy latest branch image to staging
    deploy.sh staging <branch-name>-latest

    # deploy specific image (based on commit sha)
    deploy.sh staging <commit-sha>
    "

  if [ $# -gt 2 ]
  then
    echo "$usage"
    return 0
  fi

  case "$1" in
    dev | staging | production)
      environment=$1
      ;;
    *)
      echo "$usage"
      return 0
      ;;
  esac

  if [ -z "$2" ]
  then
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    current_version=$(git rev-parse $current_branch)
  else
    current_version=$2
  fi

  context='live'
  component=app
  docker_registry=754256621582.dkr.ecr.eu-west-2.amazonaws.com/laa-get-paid/laa-fee-calculator
  docker_image_tag=${docker_registry}:${component}-${current_version}

  kubectl config set-context ${context} --namespace=laa-fee-calculator-${environment}
  kubectl config use-context ${context}

  printf "\e[33m--------------------------------------------------\e[0m\n"
  printf "\e[33mContext: $context\e[0m\n"
  printf "\e[33mEnvironment: $environment\e[0m\n"
  printf "\e[33mDocker image: $docker_image_tag\e[0m\n"
  printf "\e[33m--------------------------------------------------\e[0m\n"

  # TODO: check if image exists and if not offer to build or abort

  # apply image specific config
  kubectl set image -f kubernetes_deploy/${context}/${environment}/deployment.yaml app=${docker_image_tag} --local --output yaml | kubectl apply -f -

  # get ip addresses for allowlists
  LAA_IPS=$(curl -s https://raw.githubusercontent.com/ministryofjustice/laa-ip-allowlist/main/cidrs.txt | tr -d ' ' | tr '\n' ',')
  PINGDOM_IPS=$(curl -s https://my.pingdom.com/probes/ipv4 | tr -d ' ' | tr '\n' ',')
  COMBINED_IPS="${PINGDOM_IPS}${LAA_IPS}"

  # populate ingress file with ip addresses
  sed -i -e "s#<allowlist-populated-by-deploy-script>#${COMBINED_IPS}#" kubernetes_deploy/${context}/${environment}/ingress.yaml;

  # apply non-image specific config
  kubectl apply \
    -f kubernetes_deploy/${context}/${environment}/service.yaml \
    -f kubernetes_deploy/${context}/${environment}/ingress.yaml

  # Forcibly restart the app regardless of whether
  # there are changes to apply new secrets, at least.
  # - requires kubectl verion 1.15+
  #
  kubectl annotate deployments/laa-fee-calculator kubernetes.io/change-cause="$(date) - deploying: $docker_image_tag"
  kubectl rollout restart deployments/laa-fee-calculator

}

_deploy $@
