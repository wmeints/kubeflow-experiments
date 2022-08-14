#!/bin/bash -e
image_name=localhost:5000/fix-missing-values
image_tag=latest
full_image_name=${image_name}:${image_tag}

debug=0

while getopts d flag
do
    case "${flag}" in 
        d) debug=1;;
    esac
done

if [ $debug -gt 0 ]
then
    pushd "$(dirname "$0")" > /dev/null
    docker build -t "${full_image_name}" .
    docker push "$full_image_name"
    popd > /dev/null
else 
    pushd "$(dirname "$0")" > /dev/null
    docker build -t "${full_image_name}" . > /dev/null
    docker push "$full_image_name" > /dev/null
    popd > /dev/null
fi

# Output the strict image name, which contains the sha256 image digest
docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"
