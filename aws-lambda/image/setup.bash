docker build --provenance=false -t kitchlah .
docker tag kitchlah:latest 355511497657.dkr.ecr.ap-southeast-1.amazonaws.com/kitchlah:latest
docker push 355511497657.dkr.ecr.ap-southeast-1.amazonaws.com/kitchlah:latest