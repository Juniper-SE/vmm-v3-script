CRPD_NAME=${HOSTNAME}
# CRPD_IMAGE="localhost/crpd:22.2R1.9"
CRPD_IMAGE="${1}"
docker volume create ${CRPD_NAME}-config
docker volume create ${CRPD_NAME}-varlog
docker run --rm --detach --name ${CRPD_NAME} -h ${CRPD_NAME} --net=host --privileged -v ${CRPD_NAME}-config:/config -v ${CRPD_NAME}-varlog:/var/log -it ${CRPD_IMAGE}
